from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
Image.MAX_IMAGE_PIXELS=None
import json,subprocess,re,html,concurrent.futures,difflib
R=Path('/var/minis/workspace/mythos');OUT=R/'assets'/'art';OUT.mkdir(parents=True,exist_ok=True)
IP='208.80.154.240'
pool=json.loads((R/'art-pool.json').read_text())
picks={}
for f in ['art-picks.json','art-picks-b.json']:
 p=R/f
 if p.exists():picks.update(json.loads(p.read_text()))
def dl(url,dest):
 base=url.replace('https://thumb.wikimedia.org','https://upload.wikimedia.org').split('?')[0]
 m=re.search(r'/(\d+)px-',base)
 name=base.split('/')[-1]
 tail=name.split('px-',1)[-1] if m else None
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
def resolve(fid,needle):
 cands=pool.get(fid,{}).get('candidates',[])
 if not needle:return None
 hit=next((c for c in cands if needle.lower() in c['file'].lower()),None)
 if hit:return hit
 names=[c['file'].replace('File:','').rsplit('.',1)[0] for c in cands]
 m=difflib.get_close_matches(needle,names,n=1,cutoff=.62)
 return cands[names.index(m[0])] if m else None
def one(item):
 fid,needle=item;dst=OUT/(fid+'.jpg')
 if dst.exists() and dst.stat().st_size>5000:return ('cached',fid)
 hit=resolve(fid,needle)
 if not hit:return ('notfound',fid)
 tmp=R.parent/(fid+'.img')
 try:
  if not dl(hit['thumb'],tmp):return ('download',fid)
  norm(tmp,dst);return ('ok',fid,hit)
 except Exception as e:return ('error',fid,str(e)[:50])
 finally:
  if tmp.exists():tmp.unlink()
credits={};miss=[]
if (R/'art-credits.json').exists():credits=json.loads((R/'art-credits.json').read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for res in ex.map(one,picks.items()):
  if res[0]=='ok':
   fid=res[1];hit=res[2];m=hit.get('meta',{})
   credits[fid]={'file':hit['file'].replace('File:',''),'source':hit['page'],'license':hit.get('license') or m.get('LicenseShortName','Public domain'),'artist':re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.get('Artist','') or ''))).strip()[:180],'date':m.get('DateTimeOriginal','')[:60],'title':(m.get('ObjectName') or '')[:120]}
  elif res[0]!='cached':miss.append(res)
(R/'art-credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=1))
print(json.dumps({'art_files':len(list(OUT.glob('*.jpg'))),'credits':len(credits),'issues':[m[:2] for m in miss]},ensure_ascii=False))
