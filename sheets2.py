from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,subprocess,sys,concurrent.futures
R=Path('/var/minis/workspace/mythos');TH=Path('/var/minis/workspace/mythos-art-research/thumbs2');TH.mkdir(exist_ok=True)
IP='208.80.154.240'
def dl(url,dest):
 if dest.exists() and dest.stat().st_size>800:return dest
 u=url.replace('https://thumb.wikimedia.org','https://upload.wikimedia.org').split('?')[0]
 for n in range(2):
  p=subprocess.run(['curl','-sS','--resolve','upload.wikimedia.org:443:'+IP,'--connect-timeout','10','--max-time','45','-A','MythosAtlas/2.0',u],capture_output=True)
  if p.returncode==0 and len(p.stdout)>800:dest.write_bytes(p.stdout);return dest
 return None
def font(sz):
 for p in ['/usr/share/fonts/TTF/DejaVuSans.ttf','/usr/share/fonts/dejavu/DejaVuSans.ttf']:
  if Path(p).exists():return ImageFont.truetype(p,sz)
 return ImageFont.load_default()
pool=json.load(open(R/'art-pool.json'))
tasks=[]
for fid,v in pool.items():
 for i,c in enumerate(v['candidates'][:3]):tasks.append((fid,i,c))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:list(ex.map(lambda t:dl(t[2]['thumb'],TH/f"{t[0]}-{t[1]}.img"),tasks))
groups={}
for fid,v in pool.items():groups.setdefault(v['myth'],[]).append(fid)
outdir=Path('/var/minis/workspace/mythos-art-research/sheets2');outdir.mkdir(exist_ok=True)
want=sys.argv[1:]
for myth,ids in groups.items():
 if want and myth not in want:continue
 ROW,COLW,IMH=210,300,155
 sheet=Image.new('RGB',(COLW*3+16,ROW*len(ids)),'#0f151a');dr=ImageDraw.Draw(sheet);small=font(13);big=font(17)
 for r,fid in enumerate(ids):
  y=r*ROW;dr.text((6,y+3),fid,font=big,fill='#e6d8b6')
  for i,c in enumerate(pool[fid]['candidates'][:3]):
   x=8+i*COLW;img=TH/f"{fid}-{i}.img"
   if img.exists():
    try:
     im=Image.open(img);im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((COLW-20,IMH));sheet.paste(im,(x+(COLW-20-im.width)//2,y+26))
    except Exception:pass
   nm=Path(c['file']).stem[:31]
   dr.text((x+4,y+IMH+30),f"{i+1}. {nm}",font=small,fill='#93a3a0')
  dr.line((0,y+ROW-2,sheet.width,y+ROW-2),fill='#25313a')
 sheet.save(outdir/(myth+'.png'));print(myth,len(ids))
