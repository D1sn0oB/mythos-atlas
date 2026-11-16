from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageStat, ImageDraw
Image.MAX_IMAGE_PIXELS = None
import json, re, subprocess, concurrent.futures

R = Path('/var/minis/workspace/mythos'); OUT = R / 'assets' / 'art'
IP = '208.80.154.240'
UA = 'MythosAtlas/1.0 (contact: mythos@example.org)'
W, H = 900, 1200

plan = json.loads((R / 'ctx-plan.json').read_text())
credits = json.loads((R / 'art-credits.json').read_text())
figs = {f['id']: f for f in json.loads((R / 'figure-index.json').read_text())}


def get(url, dest):
    for _ in range(2):
        p = subprocess.run(['curl', '-sS', '--resolve', 'upload.wikimedia.org:443:' + IP,
                            '--connect-timeout', '12', '--max-time', '120', '-A', UA, url],
                           capture_output=True)
        if p.returncode == 0 and len(p.stdout) > 5000 and p.stdout[:1] != b'<':
            dest.write_bytes(p.stdout)
            return True
    return False


def fetch(c, dest):
    url = c['thumb'].replace('https://thumb.wikimedia.org', 'https://upload.wikimedia.org').split('?')[0]
    if get(url, dest):
        return True
    m = re.search(r'/(\d+)px-', url)
    if m:
        for w in [1280, 1024, 960, 800, 640]:
            if get(re.sub(r'/\d+px-', '/%dpx-' % w, url), dest):
                return True
    return get(c['url'], dest)


def compose(src, dst):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    cw, ch = im.size
    core = im.crop((int(cw * .25), int(ch * .25), int(cw * .75), int(ch * .75)))
    avg = ImageStat.Stat(core).mean
    tint = tuple(min(255, int(v * .5)) for v in avg)
    canvas = Image.new('RGB', (W, H), (9, 14, 20))
    glow = Image.new('RGB', (W // 4, H // 4), (9, 14, 20))
    ImageDraw.Draw(glow).ellipse((-W // 12, -H // 12, W // 4 + W // 12, H // 4 + H // 12), fill=tint)
    glow = glow.filter(ImageFilter.GaussianBlur(40)).resize((W, H), Image.LANCZOS)
    canvas = Image.blend(canvas, glow, .55)
    plate = im.copy()
    plate.thumbnail((W - 24, H - 60), Image.LANCZOS)
    plate = ImageEnhance.Color(plate).enhance(.94)
    plate = ImageEnhance.Contrast(plate).enhance(1.02)
    x, y = (W - plate.width) // 2, (H - plate.height) // 2
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rectangle((x - 10, y - 10, x + plate.width + 10, y + plate.height + 10),
                                     fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(16))
    canvas = Image.alpha_composite(canvas.convert('RGBA'), shadow).convert('RGB')
    canvas.paste(plate, (x, y))
    canvas.save(dst, 'JPEG', quality=88, optimize=True, progressive=True)


def one(item):
    fid, c = item
    tmp = R.parent / (fid + '.c.img')
    try:
        if not fetch(c, tmp):
            return fid, 'fail'
        compose(tmp, OUT / (fid + '.jpg'))
        m = c.get('meta', {})
        credits[fid] = {
            'file': c['file'].replace('File:', ''),
            'source': c['page'],
            'license': c.get('license') or 'Public domain',
            'artist': re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', m.get('Artist', '') or ''))[:170],
            'date': (m.get('DateTimeOriginal') or '')[:60],
            'title': (m.get('ObjectName') or '')[:120],
            'context': True,
        }
        return fid, 'ok'
    except Exception as e:
        return fid, 'err ' + str(e)[:40]
    finally:
        if tmp.exists():
            tmp.unlink()


if __name__ == '__main__':
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for r in ex.map(one, plan.items()):
            res.append(r)
    (R / 'art-credits.json').write_text(json.dumps(credits, ensure_ascii=False, indent=1))
    ok = [r for r in res if r[1] == 'ok']
    print(json.dumps({'ok': len(ok), 'issues': [r for r in res if r[1] != 'ok'][:8]}, ensure_ascii=False))
