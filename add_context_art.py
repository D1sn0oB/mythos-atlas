from pathlib import Path
from PIL import Image,ImageOps,ImageEnhance
Image.MAX_IMAGE_PIXELS=None
import json,re,html,subprocess
R=Path('/var/minis/workspace/mythos');OUT=R/'assets'/'art'
IP='208.80.154.240'
pool=json.loads((R/'art-pool.json').read_text())
ctx=json.loads((R/'art-context.json').read_text()) if (R/'art-context.json').exists() else {}
credits=json.loads((R/'art-credits.json').read_text())
extra={'celtic-rhiannon':('Pryderi and Rhiannon',False),
'persia-mithra':('Painting of Mithras and Sol',False),
'persia-simurgh':("Isfandiyar's Fifth Trial",False),
'polynesia-tane':('Tane Mahuta, 2016',True)}
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
def credit(fid,hit,is_ctx=False):
 m=hit.get('meta',{})
 credits[fid]={'file':hit['file'].replace('File:',''),'source':hit['page'],'license':hit.get('license') or m.get('LicenseShortName','Public domain'),'artist':re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.get('Artist','') or ''))).strip()[:180],'date':m.get('DateTimeOriginal','')[:60],'title':(m.get('ObjectName') or '')[:120]}
 if is_ctx:credits[fid]['context']=True
def grab(fid,hit,is_ctx=False):
 dst=OUT/(fid+'.jpg');tmp=R.parent/(fid+'.img')
 if dst.exists() and dst.stat().st_size>5000:
  credit(fid,hit,is_ctx);return 'cached'
 try:
  if not dl(hit['thumb'],tmp):return 'fail'
  norm(tmp,dst);credit(fid,hit,is_ctx);return 'ok'
 except Exception as e:return 'err '+str(e)[:40]
 finally:
  if tmp.exists():tmp.unlink()
log={}
for fid,hit in ctx.items():log[fid]=grab(fid,hit,True)
for fid,(needle,is_ctx) in extra.items():
 hit=next((c for c in pool[fid]['candidates'] if needle.lower() in c['file'].lower()),None)
 log[fid]=grab(fid,hit,is_ctx) if hit else 'nohit'
(R/'art-credits.json').write_text(json.dumps(credits,ensure_ascii=False,indent=1))
print(json.dumps({'files':len(list(OUT.glob('*.jpg'))),'credits':len(credits),'log':log},ensure_ascii=False))
