from pathlib import Path
import json,subprocess,urllib.parse,re,html,time,sys
ROOT=Path('/var/minis/workspace/mythos');OUT=Path('/var/minis/workspace/mythos-art-research');OUT.mkdir(exist_ok=True)
IP='185.15.59.224'
def request(params,tries=4):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(tries):
  p=subprocess.run(['curl','-sS','--resolve',f'commons.wikimedia.org:443:{IP}','--connect-timeout','10','--max-time','45','-A','MythosAtlas/2.0 (educational public-domain artwork research; contact: local)',u],capture_output=True,text=True)
  if p.returncode==0:
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(2+n*3)
 raise RuntimeError('request failed after retries')
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
def fetch(f):
 dest=OUT/(f['id']+'.json')
 if dest.exists():
  try:
   c=json.loads(dest.read_text())
   if c.get('query_version')==2:return 'cached'
  except Exception:pass
 name=f['en']['name']
 res=request({'action':'query','generator':'search','gsrsearch':'"'+name+'" filetype:bitmap','gsrnamespace':'6','gsrlimit':'14','prop':'imageinfo','iiprop':'url|extmetadata|size|mime','iiurlwidth':'640','iiextmetadatafilter':'LicenseShortName|LicenseUrl|UsageTerms|Copyrighted|AttributionRequired|Artist|Credit|DateTimeOriginal|ImageDescription|ObjectName|Restrictions'})
 cands=[]
 for page in res.get('query',{}).get('pages',[]):
  for info in page.get('imageinfo',[]):
   meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
   lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
   pd=bool(re.search(r'public domain|\bCC0\b|PD-',lic,re.I)) and not re.search(r'CC BY|CC-BY|share.?alike|fair use',lic,re.I)
   text=(page['title']+' '+meta.get('ImageDescription','')+' '+meta.get('ObjectName','')).lower()
   cands.append({'file':page['title'],'display_url':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'mime':info.get('mime'),'width':info.get('width'),'height':info.get('height'),'public_domain':pd,'name_match':name.lower() in text,'metadata':meta})
 cands.sort(key=lambda c:(not(c['public_domain'] and c['name_match']),not c['public_domain'],-(c['name_match']),abs((c['width'] or 1)/(c['height'] or 1)-.78)))
 dest.write_text(json.dumps({'query_version':2,'id':f['id'],'name':f['name'],'en':name,'candidates':cands},ensure_ascii=False,indent=1))
 return f'{len(cands)} candidates'
if __name__=='__main__':
 figures=json.loads((ROOT/'figure-index.json').read_text());todo=figures
 if len(sys.argv)>1:todo=[f for f in figures if f['myth'] in sys.argv[1:]]
 for f in todo:
  try:print(f['id'],fetch(f),flush=True)
  except Exception as e:print(f['id'],'ERROR',e,flush=True)
  time.sleep(.35)
