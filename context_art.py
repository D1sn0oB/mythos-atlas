from pathlib import Path
import json,subprocess,urllib.parse,re,html,time
R=Path('/var/minis/workspace/mythos');OUT=R/'assets'/'art';OUT.mkdir(parents=True,exist_ok=True)
IP='185.15.59.224'
# For figures with no surviving portrait-like depiction, use a real, openly licensed cultural artifact image.
CTX={
'christianity-mary':'Madonna and Child Duccio','celtic-rhiannon':'Rhiannon Celtic sculpture','mesopotamia-enlil':'Enlil tablet',
'persia-mithra':'Mithras tauroctony relief','persia-simurgh':'Simurgh Shahnameh miniature','maya-xquic':'Popol Vuh Ixquic',
'maya-hun-hunahpu':'Popol Vuh Hero Twins','inca-mama-quilla':'Mama Quilla Inca','inca-mama-cocha':'Mama Cocha Inca',
'yoruba-olodumare':'Yoruba Ifa divination tray','yoruba-ogun':'Ogun Yoruba sculpture','yoruba-oya':'Yoruba Oya sculpture',
'west-africa-aso':'Akan goldweight','west-africa-ntikuma':'Akan goldweight','west-africa-osebo':'Akan goldweight leopard',
'west-africa-onini':'Akan goldweight python','west-africa-mmoboro':'Akan goldweight','polynesia-maui':'Maori carving Maui',
'polynesia-hina':'Hawaiian kii sculpture','polynesia-tangaroa':'Maori meeting house carving','polynesia-tane':'Maori carving Tane',
'polynesia-pele':'Kilauea lava Hawaii','polynesia-tawhirimatea':'Maori carving','aboriginal-bunjil':'Bunjil rock art Victoria',
'aboriginal-waa':'Aboriginal rock art Victoria','aboriginal-daramulum':'Aboriginal rock engraving Sydney','aboriginal-wagyl':'Noongar art'}
def req(params):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(4):
  p=subprocess.run(['curl','-sS','--resolve','commons.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','40','-A','MythosAtlas/1.0 (contact: mythos@example.org)',u],capture_output=True,text=True)
  if 'too many requests' in p.stdout.lower():time.sleep(25);continue
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(6)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
out={}
for fid,term in CTX.items():
 res=req({'action':'query','generator':'search','gsrsearch':f'"{term}" filetype:bitmap','gsrnamespace':'6','gsrlimit':'12','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'960','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
 best=None
 for page in res.get('query',{}).get('pages',[]):
  info=page['imageinfo'][0];meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
  lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
  if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
  if (info.get('width') or 0)<500:continue
  best={'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'meta':meta,'license':(meta.get('LicenseShortName') or 'Public domain')}
  break
 if best:
  best['context']=True
  out[fid]=best
  print(fid,'OK',best['file'][:50],flush=True)
 else:print(fid,'none',flush=True)
 time.sleep(2)
(R/'art-context.json').write_text(json.dumps(out,ensure_ascii=False,indent=1))
print('context images',len(out))
