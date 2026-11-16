from pathlib import Path
import json,subprocess,urllib.parse,re,html,time,sys
sys.path.insert(0,'/var/minis/workspace/mythos')
from art_queries import QUERIES
ROOT=Path('/var/minis/workspace/mythos');OUT=Path('/var/minis/workspace/mythos-art-research/v7');OUT.mkdir(exist_ok=True)
IP='185.15.59.224'
def req(params):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(5):
  p=subprocess.run(['curl','-sS','--resolve','commons.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','45','-A','MythosAtlas/2.0 (educational research)',u],capture_output=True,text=True)
  if 'too many requests' in p.stdout.lower():time.sleep(25+n*25);continue
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(6+n*6)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
figs=json.loads((ROOT/'figure-index.json').read_text())
for f in figs:
 dest=OUT/(f['id']+'.json')
 if dest.exists():continue
 term=QUERIES[f['id']]
 res=req({'action':'query','generator':'search','gsrsearch':f'"{term}" filetype:bitmap','gsrnamespace':'6','gsrlimit':'22','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'520','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
 cands=[]
 for page in res.get('query',{}).get('pages',[]):
  info=page['imageinfo'][0];meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
  lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
  if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
  if (info.get('width') or 0)<380:continue
  text=(page['title']+' '+meta.get('ObjectName','')+' '+meta.get('ImageDescription','')).lower()
  words=[w for w in re.sub(r'[^a-z0-9]+',' ',term.lower()).split() if len(w)>2]
  match=bool(words) and all(w in text for w in words)
  cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'match':match,'meta':meta})
 cands.sort(key=lambda c:(not c['match'],abs((c['w'] or 1)/(c['h'] or 1)-.78)))
 if cands:dest.write_text(json.dumps({'id':f['id'],'candidates':cands[:6]},ensure_ascii=False,indent=1))
 print(f['id'],len(cands),sum(c['match'] for c in cands),flush=True)
 time.sleep(2.5)
