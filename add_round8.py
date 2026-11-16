from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
Image.MAX_IMAGE_PIXELS=None
import json,re,html,subprocess
R=Path('/var/minis/workspace/mythos');OUT=R/'assets'/'art';IP='208.80.154.240'
credits=json.loads((R/'art-credits.json').read_text())
v8={p.stem:json.loads(p.read_text()) for p in (Path('/var/minis/workspace/mythos-art-research/v8')).glob('*.json')}
picks={'christianity-abraham':('Adriaen van der Werff',False),'korea-bari':('Princess Bari',False),
'maya-hun-hunahpu':('Popol vuh',False),'polynesia-pele':('defying Pele',False),
'roman-vulcan':('Venus at Forge of Vulcan',False),'polynesia-tangaroa':('MaoriMeetingHouse',True),
'korea-jumong':('Shrine of King Dongmyeong',True)}
def dl(url,dest):
 base=url.replace('https://thumb.wikimedia.org','https://upload.wikimedia.org').split('?')[0]
 m=re.search(r'/(\d+)px-',base)
 for w in [960,1280,800,640,500]:
  u=re.sub(r'/\d+px-','/%dpx-'%w,base) if m else base
  p=subprocess.run(['curl','-sS','--resolve','upload.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','90','-A','MythosAtlas/1.0 (contact: mythos@example.org)',u],capture_output=True)
  if p.returncode==0 and len(p.stdout)>3000 and p.stdout[:2]!=b'<!':
   dest.write_bytes(p.stdout);return True
 return False
def norm(src,dst):
 im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');w,h=im.size;t=3/4
 if w/h>t:
  nw=int(h*t);im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
 else:
  nh=int(w/t);top=max(0,int((h-nh)*.18));im=im.crop((0,top,w,top+nh))
 im=im.resize((760,1013),Image.LANCZOS)
 im=ImageEnhance.Color(im).enhance(.9);im=ImageEnhance.Contrast(im).enhance(1.03)
 im.save(dst,'JPEG',quality=86,optimize=True,progressive=True)
log={}
for fid,(needle,is_ctx) in picks.items():
 d=v8.get(fid)
 if not d:log[fid]='nodata';continue
 hit=next((c for c in d['candidates'] if needle.lower() in c['file'].lower()),None)
 if not hit:log[fid]='nohit';continue
 dst=OUT/(fid+'.jpg');tmp=R.parent/(fid+'.img')
 try:
  if not dl(hit['thumb'],tmp):log[fid]='fail';continue
  norm(tmp,dst)
  m=hit.get('meta',{})
  credits[fid]={'file':hit['file'].replace('File:',''),'source':hit['page'],'license':hit.get('license') or m.get('LicenseShortName','Public domain'),'artist':re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.get('Artist','') or ''))).strip()[:180],'date':m.get('DateTimeOriginal','')[:60],'title':(m.get('ObjectName') or '')[:120]}
  if is_ctx:credits[fid]['context']=True
  log[fid]='ok'
 except Exception as e:log[fid]='err '+str(e)[:30]
 finally:
  if tmp.exists():tmp.unlink()
(R/'art-credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=1))
print(json.dumps({'files':len(list(OUT.glob('*.jpg'))),'credits':len(credits),'log':log},ensure_ascii=False))
