from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
Image.MAX_IMAGE_PIXELS=None
import json,subprocess,re,html
R=Path('/var/minis/workspace/mythos');OUT=R/'assets'/'art';OUT.mkdir(parents=True,exist_ok=True)
IP='208.80.154.240'
pool=json.loads((R/'art-pool.json').read_text())
picks={}
for f in ['art-picks.json','art-picks-b.json']:
 p=R/f
 if p.exists():
  try:picks.update(json.loads(p.read_text()))
  except Exception as e:print('bad',f,e)
def dl(url,dest,orig=None):
 u=url.replace('https://thumb.wikimedia.org','https://upload.wikimedia.org').split('?')[0]
 u=u.replace('/520px-','/1200px-').replace('/500px-','/1200px-')
 if orig:u=orig
 for n in range(3):
  p=subprocess.run(['curl','-sS','--resolve','upload.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','90','-A','MythosAtlas/1.0 (contact: mythos@example.org)',u],capture_output=True)
  if p.returncode==0 and len(p.stdout)>2000:
   dest.write_bytes(p.stdout);return True
 return False
def norm(src,dst):
 im=Image.open(src);im=ImageOps.exif_transpose(im).convert('RGB')
 w,h=im.size;target=3/4
 if w/h>target:
  nw=int(h*target);im=im.crop(((w-nw)//2,0,(w-nw)//2+nw,h))
 else:
  nh=int(w/target);top=max(0,int((h-nh)*0.18));im=im.crop((0,top,w,top+nh))
 im=im.resize((750,1000),Image.LANCZOS)
 im=ImageEnhance.Color(im).enhance(0.88)
 im=ImageEnhance.Contrast(im).enhance(1.04)
 im.save(dst,'JPEG',quality=84,optimize=True,progressive=True)
credits={};ok=0;miss=[]
import concurrent.futures
def work(item):
 fid,needle=item
 if fid not in pool:continue
 cands=pool[fid]['candidates']
 hit=None
 if needle:
  hit=next((c for c in cands if needle.lower() in c['file'].lower()),None)
  if not hit:
   import difflib
   names=[c['file'].replace('File:','').rsplit('.',1)[0] for c in cands]
   m=difflib.get_close_matches(needle,names,n=1,cutoff=0.6)
   if m:hit=cands[names.index(m[0])]
 if not hit:
  miss.append((fid,needle,'not found'));continue
 dst=OUT/(fid+'.jpg');tmp=R.parent/'tmp-art.img'
 if not dst.exists():
  src=hit['thumb']
  if not dl(src,tmp):miss.append((fid,needle,'download failed'));continue
  try:norm(tmp,dst)
  except Exception as e:miss.append((fid,needle,'image error '+str(e)[:40]));continue
  finally:
   if tmp.exists():tmp.unlink()
 m=hit.get('meta',{})
 credits[fid]={'file':hit['file'].replace('File:',''),'source':hit['page'],'license':hit.get('license') or m.get('LicenseShortName','Public domain'),'artist':re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.get('Artist','') or ''))).strip()[:180],'date':m.get('DateTimeOriginal','')[:60],'title':(m.get('ObjectName') or '')[:120]}
 ok+=1
(R/'art-credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=1))
print(json.dumps({'with_art':ok,'total_picked':len(picks),'issues':miss[:15]},ensure_ascii=False,indent=1))
