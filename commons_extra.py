from pathlib import Path
import json,subprocess,urllib.parse,re,html,time
from art_queries import QUERIES
ROOT=Path(__file__).parent;OUT=Path('/var/minis/workspace/mythos-art-research/v4');OUT.mkdir(exist_ok=True)
IP='185.15.59.224'
EXTRA={
'greek-poseidon':'Poseidon Melos','greek-hades':'Hades Serapis','roman-venus':'Venus Kallipygos','roman-saturn':'Saturnus statue',
'roman-vulcan':'Vulcanus statue','norse-hel':'Hel Loki daughter','japan-inari':'Inari fox Kitsune shrine statue',
'korea-hwanung':'Hwanung','korea-ungnyeo':'Ungnyeo bear woman','korea-jumong':'Jumong statue','korea-haemosu':'Haemosu',
'korea-bari':'Bari princess shaman','korea-yuhwa':'Yuhwa','maya-hun-hunahpu':'Hun Hunahpu','inca-mama-cocha':'Mama Cocha',
'west-africa-asase-yaa':'Asase Yaa','west-africa-aso':'Anansi','west-africa-ntikuma':'Anansi','west-africa-osebo':'Anansi',
'west-africa-mmoboro':'Anansi','aboriginal-wagyl':'Wagyl','aboriginal-daramulum':'Daramulum','aboriginal-bunjil':'Bunjil',
'aboriginal-rainbow-serpent':'Rainbow Serpent','maya-xquic':'Ixquic','persia-anahita':'Anahita','yoruba-olodumare':'Olodumare'}
def request(params,tries=4):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(tries):
  p=subprocess.run(['curl','-sS','--resolve',f'commons.wikimedia.org:443:{IP}','--connect-timeout','10','--max-time','45','-A','MythosAtlas/2.0 (educational)',u],capture_output=True,text=True)
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(2+n*3)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
for fid,term in EXTRA.items():
 dest=OUT/(fid+'.json')
 if dest.exists():continue
 res=request({'action':'query','generator':'search','gsrsearch':'"'+term+'" filetype:bitmap','gsrnamespace':'6','gsrlimit':'20','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'500','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
 cands=[]
 for page in res.get('query',{}).get('pages',[]):
  for info in page.get('imageinfo',[]):
   meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
   lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
   if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD',lic,re.I):continue
   if (info.get('width') or 0)<400:continue
   cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'meta':meta})
 cands.sort(key=lambda c:abs((c['w'] or 1)/(c['h'] or 1)-.78))
 dest.write_text(json.dumps({'id':fid,'query':term,'candidates':cands[:6]},ensure_ascii=False,indent=1))
 print(fid,len(cands),flush=True);time.sleep(.3)
