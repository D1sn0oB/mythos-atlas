from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageStat, ImageDraw
Image.MAX_IMAGE_PIXELS = None
import json, re, subprocess, concurrent.futures
R = Path('/var/minis/workspace/mythos'); OUT = R / 'assets' / 'art'
OUT.mkdir(parents=True, exist_ok=True)
IP = '208.80.154.240'
CRED = json.loads((R / 'art-credits.json').read_text())
UA = 'MythosAtlas/1.0 (contact: mythos@example.org)'
W, H = 900, 1200

def api(title):
    import urllib.parse
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'titles': 'File:' + title, 'prop': 'imageinfo',
        'iiprop': 'url|size', 'iiurlwidth': '1920'})
    for _ in range(3):
        p = subprocess.run(['curl', '-sS', '--resolve', 'commons.wikimedia.org:443:185.15.59.224',
                            '--connect-timeout', '10', '--max-time', '40', '-A', UA, u],
                           capture_output=True, text=True)
        try:
            pg = json.loads(p.stdout)['query']['pages'][0]
            if 'imageinfo' in pg:
                return pg['imageinfo'][0]
        except Exception:
            pass
    return None

def get(url, dest):
    for _ in range(2):
        p = subprocess.run(['curl', '-sS', '--resolve', 'upload.wikimedia.org:443:' + IP,
                            '--connect-timeout', '12', '--max-time', '120', '-A', UA, url],
                           capture_output=True)
        if p.returncode == 0 and len(p.stdout) > 4000 and p.stdout[:1] != b'<':
            dest.write_bytes(p.stdout)
            return True
    return False

def fetch(info, dest):
    primary = (info.get('thumburl') or info['url']).replace('https://thumb.wikimedia.org', 'https://upload.wikimedia.org').split('?')[0]
    if get(primary, dest):
        return True
    m = re.search(r'/(\d+)px-', primary)
    if m:
        for w in [1280, 1024, 960, 800, 640, 500]:
            if get(re.sub(r'/\d+px-', '/%dpx-' % w, primary), dest):
                return True
    return get(info['url'], dest)

def compose(src, dst):
    """Full artwork, unobstructed. Solid dark ground with a tonal glow; no double image."""
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    # average colour of central region -> glow tint
    cw, chh = im.size
    core = im.crop((int(cw * .25), int(chh * .25), int(cw * .75), int(chh * .75)))
    avg = ImageStat.Stat(core).mean
    tint = tuple(min(255, int(v * .55)) for v in avg)

    canvas = Image.new('RGB', (W, H), (9, 14, 20))
    glow = Image.new('RGB', (W // 4, H // 4), (9, 14, 20))
    d = ImageDraw.Draw(glow)
    d.ellipse((-W // 12, -H // 12, W // 4 + W // 12, H // 4 + H // 12), fill=tint)
    glow = glow.filter(ImageFilter.GaussianBlur(40)).resize((W, H), Image.LANCZOS)
    canvas = Image.blend(canvas, glow, 0.55)

    plate = im.copy()
    plate.thumbnail((W - 24, H - 60), Image.LANCZOS)
    plate = ImageEnhance.Color(plate).enhance(0.94)
    plate = ImageEnhance.Contrast(plate).enhance(1.02)
    x = (W - plate.width) // 2
    y = (H - plate.height) // 2

    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((x - 10, y - 10, x + plate.width + 10, y + plate.height + 10),
                                     fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas.convert('RGBA'), shadow).convert('RGB')
    canvas.paste(plate, (x, y))
    canvas.save(dst, 'JPEG', quality=88, optimize=True, progressive=True)

def one(item):
    fid, c = item
    dst = OUT / (fid + '.jpg')
    info = api(c['file'].replace('File:', ''))
    if not info:
        return fid, 'noinfo'
    tmp = R.parent / (fid + '.img')
    try:
        if not fetch(info, tmp):
            return fid, 'fail'
        compose(tmp, dst)
        return fid, 'ok'
    except Exception as e:
        return fid, 'err ' + str(e)[:40]
    finally:
        if tmp.exists():
            tmp.unlink()

if __name__ == '__main__':
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one, CRED.items()):
            res.append(r)
    bad = [r for r in res if not r[1].startswith('ok')]
    print(json.dumps({'total': len(res), 'ok': len(res) - len(bad), 'bad': bad[:10]}, ensure_ascii=False))
