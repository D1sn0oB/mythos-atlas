from pathlib import Path
import json,subprocess,urllib.parse,re,html,time
ROOT=Path('/var/minis/workspace/mythos');OUT=Path('/var/minis/workspace/mythos-art-research/v6');OUT.mkdir(exist_ok=True)
IP='185.15.59.224'
MISSING={
'greek-poseidon':'Poseidon','greek-hades':'Hades','norse-hel':'Hel Norse','japan-inari':'Inari',
'korea-hwanung':'Hwanung','korea-ungnyeo':'Ungnyeo','korea-jumong':'Jumong','korea-bari':'Bari','korea-haemosu':'Haemosu',
'maya-hun-hunahpu':'Hun Hunahpu','maya-xquic':'Ixquic','inca-mama-cocha':'Mama Cocha','west-africa-asase-yaa':'Asase',
'aboriginal-wagyl':'Wagyl','aboriginal-daramulum':'Daramulum','aboriginal-rainbow-serpent':'Rainbow Serpent',
'persia-anahita':'Anahita','yoruba-olodumare':'Olodumare','west-africa-aso':'Anansi','west-africa-ntikuma':'Anansi',
'west-africa-osebo':'Anansi','west-africa-mmoboro':'Anansi','polynesia-ruaumoko':'Ruaumoko','polynesia-hine-nui-te-po':'Hine-nui',
'maya-vucub-caquix':'Vucub Caquix','inca-mama-quilla':'Mama Quilla','celtic-manannan':'Manannan'}
def req(params):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(4):
  p=subprocess.run(['curl','-sS','--resolve','commons.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','45','-A','MythosAtlas/2.0 (educational; contact local)',u],capture_output=True,text=True)
  if 'too many requests' in p.stdout.lower():
   time.sleep(20+n*20);continue
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(8+n*8)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
for fid,term in MISSING.items():
 dest=OUT/(fid+'.json')
 if dest.exists():continue
 res=req({'action':'query','generator':'search','gsrsearch':f'"{term}" filetype:bitmap','gsrnamespace':'6','gsrlimit':'20','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'520','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
 cands=[]
 for page in res.get('query',{}).get('pages',[]):
  info=page['imageinfo'][0];meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
  lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
  if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
  if (info.get('width') or 0)<380:continue
  cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'meta':meta})
 cands.sort(key=lambda c:abs((c['w'] or 1)/(c['h'] or 1)-.78))
 if cands:dest.write_text(json.dumps({'id':fid,'candidates':cands[:8]},ensure_ascii=False,indent=1))
 print(fid,len(cands),flush=True);time.sleep(4)
