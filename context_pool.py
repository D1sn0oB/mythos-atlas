"""Assign a real public-domain cultural image to figures lacking a portrait.
Each image is a genuine Commons artwork/artifact from the same tradition, clearly
labelled as context rather than a portrait."""
from pathlib import Path
import json, subprocess, urllib.parse, re, html, time, hashlib

R = Path('/var/minis/workspace/mythos')
OUT = R / 'assets' / 'art'
RES = Path('/var/minis/workspace/mythos-art-research/ctx'); RES.mkdir(parents=True, exist_ok=True)
IP_COMMONS = '185.15.59.224'

# Broad, safe searches per tradition: temple art, manuscripts, sculpture.
POOL = {
 'china': ['Dunhuang mural Tang dynasty', 'Shanxi temple mural Ming', 'Chinese Buddhist stele Tang'],
 'japan': ['Heian period emaki scroll', 'Kasuga shrine deer painting', 'Muromachi ink painting figure'],
 'korea': ['Goryeo Buddhist painting', 'Joseon Dancheong', 'Silla gilt bronze figure'],
 'india': ['Mughal miniature court', 'Chola bronze deity', 'Rajasthani miniature'],
 'christianity': ['Byzantine mosaic angel', 'Gothic illuminated manuscript', 'Ethiopian icon'],
 'greek': ['Attic red figure pottery', 'Greek marble stele relief', 'Pompeii fresco figure'],
 'norse': ['Icelandic manuscript illumination', 'Gotland picture stone', 'Viking age tapestry'],
 'roman': ['Roman mosaic figure', 'Catacomb fresco Roman', 'Roman marble relief'],
 'celtic': ['Celtic stone carving', 'Insular manuscript illumination', 'Gundestrup cauldron panel'],
 'egypt': ['Egyptian tomb painting', 'Egyptian papyrus vignette', 'Egyptian bronze statuette'],
 'mesopotamia': ['Assyrian relief palace', 'Babylonian cylinder seal', 'Sumerian votive statue'],
 'persia': ['Persian miniature Shahnameh', 'Achaemenid relief Persepolis', 'Safavid painting'],
 'maya': ['Maya codex facsimile', 'Maya stela carving', 'Maya ceramic vessel scene'],
 'aztec': ['Codex Borgia facsimile', 'Aztec stone sculpture', 'Mexica codex illustration'],
 'inca': ['Inca textile pattern', 'Andean ceramic vessel', 'Inca stonework wall'],
 'yoruba': ['Yoruba carved door', 'Ife bronze head', 'Yoruba beadwork crown'],
 'west-africa': ['Akan goldweight collection', 'Ashanti kente cloth', 'Akan carved stool'],
 'polynesia': ['Maori carved wharenui panel', 'Hawaiian feather cloak', 'Marquesan tiki carving'],
 'aboriginal': ['Aboriginal bark painting public', 'Australian rock art public', 'Aboriginal dot painting public'],
}
TRAD = {'china': 'Chinese', 'japan': 'Japanese', 'korea': 'Korean', 'india': 'Indian',
        'christianity': 'Christian', 'greek': 'Greek', 'norse': 'Norse', 'roman': 'Roman',
        'celtic': 'Celtic', 'egypt': 'Egyptian', 'mesopotamia': 'Mesopotamian',
        'persia': 'Persian', 'maya': 'Maya', 'aztec': 'Aztec', 'inca': 'Inca',
        'yoruba': 'Yoruba', 'west-africa': 'Akan', 'polynesia': 'Polynesian',
        'aboriginal': 'Aboriginal Australian'}


def req(params, tries=4):
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'format': 'json', 'formatversion': '2', **params})
    for n in range(tries):
        p = subprocess.run(['curl', '-sS', '--resolve', 'commons.wikimedia.org:443:' + IP_COMMONS,
                            '--connect-timeout', '12', '--max-time', '45',
                            '-A', 'MythosAtlas/1.0 (contact: mythos@example.org)', u],
                           capture_output=True, text=True)
        if 'too many requests' in p.stdout.lower():
            time.sleep(22); continue
        if p.returncode == 0 and p.stdout.strip().startswith('{'):
            try:
                return json.loads(p.stdout)
            except Exception:
                pass
        time.sleep(5)
    return {}


def clean(v):
    return html.unescape(re.sub('<[^>]+>', ' ', str(v or ''))).strip()


def gather(trad):
    """Collect up to 6 PD images for one tradition."""
    out = []
    seen = set()
    for term in POOL[trad]:
        res = req({'action': 'query', 'generator': 'search',
                   'gsrsearch': term + ' filetype:bitmap', 'gsrnamespace': '6',
                   'gsrlimit': '8', 'prop': 'imageinfo',
                   'iiprop': 'url|extmetadata|size', 'iiurlwidth': '1200',
                   'iiextmetadatafilter': 'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ObjectName|ImageDescription'})
        for page in res.get('query', {}).get('pages', []):
            if page['title'] in seen:
                continue
            info = page['imageinfo'][0]
            meta = {k: clean(v.get('value')) for k, v in info.get('extmetadata', {}).items()}
            lic = meta.get('LicenseShortName', '') + ' ' + meta.get('UsageTerms', '')
            if re.search(r'CC BY|share.?alike|fair use', lic, re.I):
                continue
            if not re.search(r'public domain|CC0|PD|No restrictions', lic, re.I):
                continue
            if (info.get('width') or 0) < 600:
                continue
            seen.add(page['title'])
            out.append({'file': page['title'], 'thumb': info.get('thumburl') or info['url'],
                        'url': info['url'], 'page': info['descriptionurl'],
                        'license': meta.get('LicenseShortName') or 'Public domain', 'meta': meta})
        if len(out) >= 6:
            break
        time.sleep(1.5)
    return out[:6]


if __name__ == '__main__':
    need = json.loads((R / 'need-art.json').read_text())
    figures = json.loads((R / 'figure-index.json').read_text())
    missing = [f for f in figures if f['id'] not in json.loads((R / 'art-credits.json').read_text())]
    by_trad = {}
    for f in missing:
        by_trad.setdefault(f['myth'], []).append(f['id'])
    plan = {}
    for trad, ids in by_trad.items():
        cache = RES / (trad + '.json')
        if cache.exists():
            pool = json.loads(cache.read_text())
        else:
            pool = gather(trad)
            cache.write_text(json.dumps(pool, ensure_ascii=False, indent=1))
        if not pool:
            print(trad, 'NO POOL', flush=True)
            continue
        for i, fid in enumerate(ids):
            plan[fid] = pool[i % len(pool)]
        print(trad, len(pool), 'images ->', len(ids), 'figures', flush=True)
    (R / 'ctx-plan.json').write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print('planned', len(plan))
