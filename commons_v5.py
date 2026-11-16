from pathlib import Path
import json,subprocess,urllib.parse,re,html,time,sys,concurrent.futures,threading
sys.path.insert(0,str(Path(__file__).parent))
from art_queries import QUERIES
ROOT=Path(__file__).parent;OUT=Path('/var/minis/workspace/mythos-art-research/v5');OUT.mkdir(exist_ok=True)
IP='185.15.59.224';LOCK=threading.Lock()
def request(params,tries=3):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(tries):
  p=subprocess.run(['curl','-sS','--resolve',f'commons.wikimedia.org:443:{IP}','--connect-timeout','12','--max-time','40','-A','MythosAtlas/2.0 (educational)',u],capture_output=True,text=True)
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(1+n*2)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
def collect(f):
 dest=OUT/(f['id']+'.json')
 if dest.exists():return 'cached'
 name=QUERIES[f['id']];seen=set();cands=[]
 for q in [f'"{name}" mythology engraving',f'"{name}" Meyers']:
  res=request({'action':'query','generator':'search','gsrsearch':q+' filetype:bitmap','gsrnamespace':'6','gsrlimit':'12','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'520','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
  for page in res.get('query',{}).get('pages',[]):
   if page['title'] in seen:continue
   for info in page.get('imageinfo',[]):
    meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
    lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
    if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
    if (info.get('width') or 0)<380:continue
    text=(page['title']+' '+meta.get('ObjectName','')+' '+meta.get('ImageDescription','')).lower()
    words=[w for w in re.sub(r'[^a-z0-9]+',' ',name.lower()).split() if len(w)>2]
    match=bool(words) and all(w in text for w in words)
    seen.add(page['title'])
    cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'match':match,'meta':meta})
  if sum(c['match'] for c in cands)>=3:break
 cands.sort(key=lambda c:(not c['match'],abs((c['w'] or 1)/(c['h'] or 1)-.78)))
 with LOCK:
  if not cands:return "EMPTY-retry-later"
  dest.write_text(json.dumps({'id':f['id'],'name':f['name'],'en':f['en']['name'],'candidates':cands[:8]},ensure_ascii=False,indent=1))
 return f"{sum(c['match'] for c in cands)} matched"
if __name__=='__main__':
 figs=json.loads((ROOT/'figure-index.json').read_text())
 def one(f):
  try:r=collect(f)
  except Exception as e:r='ERR '+str(e)[:60]
  print(f['id'],r,flush=True);return r
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(one,figs))
