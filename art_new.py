from pathlib import Path
import json, subprocess, urllib.parse, re, html, time
R = Path('/var/minis/workspace/mythos')
OUT = Path('/var/minis/workspace/mythos-art-research/v9'); OUT.mkdir(parents=True, exist_ok=True)
IP = '185.15.59.224'
UA = 'MythosAtlas/1.0 (contact: mythos@example.org)'
need = json.loads((R / 'need-art.json').read_text())

# Curated English search terms; Chinese names would not retrieve Western museum files.
TERMS = {
 'china-sunwukong': ['Sun Wukong', 'Monkey King painting', 'Xiyouji monkey'],
 'china-nezha': ['Nezha', 'Nezha deity'],
 'china-erlang': ['Erlang Shen', 'Erlang deity'],
 'china-kuafu': ['Kuafu', 'Kuafu chasing sun'],
 'china-jingwei': ['Jingwei bird', 'Jingwei mythology'],
 'china-chiyou': ['Chiyou', 'Chi You deity'],
 'china-xingtian': ['Xingtian', 'Xing Tian headless'],
 'china-bai-she': ['Legend of the White Snake', 'White Snake Lady painting'],
 'japan-yamatotakeru': ['Yamato Takeru', 'Yamatotakeru print'],
 'japan-yamata-no-orochi': ['Yamata no Orochi', 'Susanoo Orochi'],
 'japan-onamazu': ['Namazu', 'earthquake catfish print'],
 'japan-shuten': ['Shuten Doji', 'Shuten-doji'],
 'korea-bulgasari': ['Bulgasari', 'Korean bulgvari'],
 'korea-gumiho': ['Gumiho', 'nine tailed fox Korea'],
 'korea-choe-yeong': ['Cheoyong', 'Cheoyong mask'],
 'india-rama': ['Rama', 'Rama painting'],
 'india-krishna': ['Krishna', 'Krishna painting'],
 'india-garuda': ['Garuda', 'Garuda sculpture'],
 'india-yama': ['Yama', 'Yama Hindu god'],
 'india-agni': ['Agni', 'Agni deity'],
 'india-indra': ['Indra', 'Indra deity'],
 'india-nataraja': ['Nataraja', 'Shiva Nataraja bronze'],
 'greek-prometheus': ['Prometheus', 'Prometheus bound'],
 'greek-persephone': ['Persephone', 'Persephone Proserpina'],
 'greek-hercules': ['Heracles', 'Hercules Farnese'],
 'greek-theseus': ['Theseus', 'Theseus Minotaur'],
 'greek-orpheus': ['Orpheus', 'Orpheus Eurydice'],
 'greek-achilles': ['Achilles', 'Achilles painting'],
 'greek-icarus': ['Icarus', 'Fall of Icarus'],
 'norse-fenrir': ['Fenrir', 'Fenris wolf'],
 'norse-jormungandr': ['Jormungandr', 'Midgard serpent'],
 'norse-ymir': ['Ymir', 'Ymir giant'],
 'norse-idun': ['Idun', 'Idun apples'],
 'norse-brynhild': ['Brynhild', 'Sigurd Brynhild'],
 'roman-aeneas': ['Aeneas', 'Aeneas painting'],
 'roman-romulus': ['Romulus', 'Romulus Remus wolf'],
 'roman-cupid': ['Cupid', 'Cupid Psyche'],
 'celtic-finn': ['Fionn mac Cumhaill', 'Finn McCool'],
 'celtic-bran': ['Bendigeidfran', 'Bran the Blessed'],
 'celtic-aengus': ['Aengus', 'Oengus Og'],
 'egypt-sekhmet': ['Sekhmet', 'Sekhmet statue'],
 'egypt-ptah': ['Ptah', 'Ptah statue'],
 'egypt-nut': ['Nut goddess', 'Nut Egyptian sky'],
 'mesopotamia-tiamat': ['Tiamat', 'Tiamat Enuma Elish'],
 'mesopotamia-adapa': ['Adapa', 'Adapa Mesopotamian'],
 'mesopotamia-utnapishtim': ['Utnapishtim', 'Gilgamesh flood'],
 'mesopotamia-nergal': ['Nergal', 'Nergal god'],
 'persia-suhrab': ['Sohrab', 'Rustam Sohrab'],
 'persia-zahhak': ['Zahhak', 'Zahhak Shahnameh'],
 'persia-kay-khosrow': ['Kay Khosrow', 'Kai Khosrow'],
 'maya-kukulkan': ['Kukulkan', 'Chichen Itza serpent'],
 'aztec-xolotl': ['Xolotl', 'Xolotl dog'],
 'aztec-ehecatl': ['Ehecatl', 'Ehecatl wind god'],
 'inca-chasca': ['Quyllur', 'Inca Venus star'],
 'yoruba-yemoja': ['Yemoja', 'Yemanja'],
 'yoruba-oshosi': ['Oshosi', 'Oshossi'],
 'west-africa-adinkra': ['Adinkra symbols', 'Adinkra cloth'],
 'west-africa-sankofa': ['Sankofa', 'Sankofa bird'],
 'polynesia-kamapuaa': ['Kamapuaa', 'Kamapua a Hawaiian'],
 'polynesia-sina': ['Sina Samoa', 'Sina goddess'],
 'aboriginal-emu': ['Emu in the sky', 'Aboriginal astronomy emu'],
 'christianity-lucifer': ['Lucifer', 'falling Lucifer'],
 'christianity-eve': ['Eve', 'Eve temptation painting'],
 'christianity-david': ['David Michelangelo', 'King David'],
 'christianity-solomon': ['Solomon', 'Judgment of Solomon'],
 'christianity-judas': ['Judas Iscariot', 'Judas kiss'],
 'christianity-magdalene': ['Mary Magdalene', 'Magdalene painting'],
}
def req(params, tries=3):
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'format': 'json', 'formatversion': '2', **params})
    for n in range(tries):
        p = subprocess.run(['curl', '-sS', '--resolve', 'commons.wikimedia.org:443:' + IP,
                            '--connect-timeout', '12', '--max-time', '45', '-A', UA, u],
                           capture_output=True, text=True)
        if 'too many requests' in p.stdout.lower():
            time.sleep(25); continue
        if p.returncode == 0 and p.stdout.strip().startswith('{'):
            try:
                return json.loads(p.stdout)
            except Exception:
                pass
        time.sleep(6)
    return {}
def clean(v):
    return html.unescape(re.sub('<[^>]+>', ' ', str(v or ''))).strip()

for f in need:
    fid = f['id']
    dest = OUT / (fid + '.json')
    if dest.exists():
        continue
    terms = TERMS.get(fid) or [f['en']]
    cands = []
    for term in terms:
        res = req({'action': 'query', 'generator': 'search',
                   'gsrsearch': '"' + term + '" filetype:bitmap', 'gsrnamespace': '6',
                   'gsrlimit': '12', 'prop': 'imageinfo',
                   'iiprop': 'url|extmetadata|size', 'iiurlwidth': '960',
                   'iiextmetadatafilter': 'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
        for page in res.get('query', {}).get('pages', []):
            info = page['imageinfo'][0]
            meta = {k: clean(v.get('value')) for k, v in info.get('extmetadata', {}).items()}
            lic = meta.get('LicenseShortName', '') + ' ' + meta.get('UsageTerms', '')
            if re.search(r'CC BY|share.?alike|fair use', lic, re.I):
                continue
            if not re.search(r'public domain|CC0|PD|No restrictions', lic, re.I):
                continue
            if (info.get('width') or 0) < 500:
                continue
            if any(c['file'] == page['title'] for c in cands):
                continue
            cands.append({'file': page['title'], 'thumb': info.get('thumburl') or info['url'],
                          'url': info['url'], 'page': info['descriptionurl'],
                          'w': info.get('width'), 'h': info.get('height'),
                          'license': (meta.get('LicenseShortName') or 'Public domain'), 'meta': meta})
        if len(cands) >= 3:
            break
        time.sleep(1.2)
    if cands:
        dest.write_text(json.dumps({'id': fid, 'candidates': cands[:4]}, ensure_ascii=False, indent=1))
    print(fid, len(cands), flush=True)
    time.sleep(1.5)
