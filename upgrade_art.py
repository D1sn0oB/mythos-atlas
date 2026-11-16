"""Upgrade context images to genuine figure depictions where a curated pick exists."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageStat, ImageDraw
Image.MAX_IMAGE_PIXELS = None
import json, re, subprocess, concurrent.futures, difflib

R = Path('/var/minis/workspace/mythos'); OUT = R / 'assets' / 'art'
IP = '208.80.154.240'
UA = 'MythosAtlas/1.0 (contact: mythos@example.org)'
W, H = 900, 1200

credits = json.loads((R / 'art-credits.json').read_text())
picks = json.loads((R / 'art-picks-b.json').read_text())
meta = {}
for d in ['art-pool.json']:
    p = R / d
    if p.exists():
        for k, v in json.loads(p.read_text()).items():
            meta.setdefault(k, []).extend(v.get('candidates', []))
for p in Path('/var/minis/workspace/mythos-art-research/v9').glob('*.json'):
    d = json.loads(p.read_text())
    meta.setdefault(d['id'], []).extend(d['candidates'])


def api(title):
    import urllib.parse
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action': 'query', 'format': 'json', 'formatversion': '2', 'titles': 'File:' + title,
        'prop': 'imageinfo', 'iiprop': 'url|size', 'iiurlwidth': '1920'})
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
        if p.returncode == 0 and len(p.stdout) > 5000 and p.stdout[:1] != b'<':
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
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    cw, ch = im.size
    core = im.crop((int(cw * .25), int(ch * .25), int(cw * .75), int(ch * .75)))
    tint = tuple(min(255, int(v * .5)) for v in ImageStat.Stat(core).mean)
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
    fid, needle = item
    cands = meta.get(fid, [])
    hit = next((c for c in cands if needle.lower() in c['file'].lower()), None)
    if not hit:
        names = [c['file'].replace('File:', '').rsplit('.', 1)[0] for c in cands]
        m = difflib.get_close_matches(needle, names, n=1, cutoff=.72)
        hit = cands[names.index(m[0])] if m else None
    if not hit:
        return fid, 'nomatch'
    info = api(hit['file'].replace('File:', ''))
    if not info:
        return fid, 'noinfo'
    tmp = R.parent / (fid + '.u.img')
    try:
        if not fetch(info, tmp):
            return fid, 'fail'
        compose(tmp, OUT / (fid + '.jpg'))
        m2 = hit.get('meta', {})
        credits[fid] = {
            'file': hit['file'].replace('File:', ''),
            'source': hit.get('page') or info['descriptionurl'],
            'license': hit.get('license') or (m2.get('LicenseShortName') or 'Public domain'),
            'artist': re.sub(r'\s+', ' ', re.sub('<[^>]+>', '', m2.get('Artist', '') or ''))[:170],
            'date': (m2.get('DateTimeOriginal') or '')[:60],
            'title': (m2.get('ObjectName') or '')[:120],
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
        for r in ex.map(one, picks.items()):
            res.append(r)
    (R / 'art-credits.json').write_text(json.dumps(credits, ensure_ascii=False, indent=1))
    ok = [r for r in res if r[1] == 'ok']
    print(json.dumps({'ok': len(ok), 'issues': [r for r in res if r[1] != 'ok']}, ensure_ascii=False))
