from pathlib import Path
import json,subprocess,urllib.parse,re,html,time,sys
sys.path.insert(0,str(Path(__file__).parent))
from art_queries import QUERIES
ROOT=Path(__file__).parent;OUT=Path('/var/minis/workspace/mythos-art-research/v3');OUT.mkdir(parents=True,exist_ok=True)
IP='185.15.59.224'
def request(params,tries=5):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(tries):
  p=subprocess.run(['curl','-sS','--resolve',f'commons.wikimedia.org:443:{IP}','--connect-timeout','10','--max-time','45','-A','MythosAtlas/2.0 (educational artwork research)',u],capture_output=True,text=True)
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(2+n*4)
 raise RuntimeError('request failed')
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
def run(f):
 dest=OUT/(f['id']+'.json')
 if dest.exists():return 'cached'
 q=QUERIES.get(f['id'])
 if not q:return 'no query'
 res=request({'action':'query','generator':'search','gsrsearch':'"'+q+'" filetype:bitmap','gsrnamespace':'6','gsrlimit':'18','prop':'imageinfo','iiprop':'url|extmetadata|size|mime','iiurlwidth':'500','iiextmetadatafilter':'LicenseShortName|UsageTerms|Copyrighted|Artist|Credit|DateTimeOriginal|ImageDescription|ObjectName|Restrictions'})
 cands=[]
 for page in res.get('query',{}).get('pages',[]):
  for info in page.get('imageinfo',[]):
   meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
   lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
   if re.search(r'CC BY|CC-BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|\bCC0\b|PD',lic,re.I):continue
   if (info.get('width') or 0)<420:continue
   cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'meta':meta})
 cands.sort(key=lambda c:abs((c['w'] or 1)/(c['h'] or 1)-.78))
 dest.write_text(json.dumps({'id':f['id'],'name':f['name'],'en':f['en']['name'],'query':q,'candidates':cands[:6]},ensure_ascii=False,indent=1))
 return f'{len(cands)} pd'
if __name__=='__main__':
 figs=json.loads((ROOT/'figure-index.json').read_text())
 for f in figs:
  try:print(f['id'],run(f),flush=True)
  except Exception as e:print(f['id'],'ERROR',e,flush=True)
  time.sleep(.3)
