from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,subprocess,concurrent.futures,sys
ROOT=Path('/var/minis/workspace/mythos');CACHE=Path('/var/minis/workspace/mythos-art-research/v3');TH=Path('/var/minis/workspace/mythos-art-research/thumbs');TH.mkdir(exist_ok=True)
IP='208.80.154.240'
def download(url,dest):
 if dest.exists() and dest.stat().st_size>800:return True
 for n in range(3):
  p=subprocess.run(['curl','-sS','--resolve','upload.wikimedia.org:443:'+IP,'--connect-timeout','10','--max-time','60','-A','MythosAtlas/2.0',url],capture_output=True)
  if p.returncode==0 and len(p.stdout)>800:dest.write_bytes(p.stdout);return True
 return False
def get(cand,key):
 u=cand['thumb'].replace('https://thumb.wikimedia.org','https://upload.wikimedia.org').split('?')[0]
 dest=TH/(key+'.img');return dest if download(u,dest) else None
def font(sz):
 for p in ['/usr/share/fonts/TTF/DejaVuSans.ttf','/usr/share/fonts/dejavu/DejaVuSans.ttf']:
  if Path(p).exists():return ImageFont.truetype(p,sz)
 return ImageFont.load_default()
if __name__=='__main__':
 figs=json.loads((ROOT/'figure-index.json').read_text());groups={}
 for f in figs:groups.setdefault(f['myth'],[]).append(f)
 only=sys.argv[1:];outdir=Path('/var/minis/workspace/mythos-art-research/sheets');outdir.mkdir(exist_ok=True)
 for myth,items in groups.items():
  if only and myth not in only:continue
  ROW,COLW,IMH=252,300,196
  sheet=Image.new('RGB',(COLW*3+16,ROW*len(items)),'#10161b');dr=ImageDraw.Draw(sheet);small=font(14);big=font(19)
  for r,f in enumerate(items):
   y=r*ROW;d=json.loads((CACHE/(f['id']+'.json')).read_text())
   dr.text((6,y+5),f"{f['id']}  ·  {f['name']}",font=big,fill='#e3d5b3')
   for c,cand in enumerate(d['candidates'][:3]):
    x=8+c*COLW;img=get(cand,f"{f['id']}-{c}")
    if not img:continue
    try:
     im=Image.open(img);im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((COLW-24,IMH))
     sheet.paste(im,(x+(COLW-24-im.width)//2,y+34))
    except Exception:pass
    dr.text((x+4,y+IMH+40),f"{c+1}. {Path(cand['file']).stem[:33]}",font=small,fill='#95a5a2')
   dr.line((0,y+ROW-3,sheet.width,y+ROW-3),fill='#26333d')
  sheet.save(outdir/(myth+'.jpg'),quality=80);print(myth,len(items))
