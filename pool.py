from pathlib import Path
import json,glob,re,collections
R=Path('/var/minis/workspace/mythos');res=Path('/var/minis/workspace/mythos-art-research')
pool=collections.defaultdict(dict)
for d in ['v3','v4','v5','v6','v7']:
 for p in glob.glob(str(res/d/'*.json')):
  try:o=json.load(open(p))
  except Exception:continue
  if 'id' not in o:continue
  for c in o.get('candidates',[]):
   lic=(c.get('meta') or {}).get('LicenseShortName','')+' '+(c.get('meta') or {}).get('UsageTerms','')
   if not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
   if re.search(r'CC BY|share.?alike|fair use',lic,re.I):continue
   c['license']=((c.get('meta') or {}).get('LicenseShortName') or 'Public domain').strip()
   pool[o['id']].setdefault(c['file'],c)
def score(c):
 t=c['file'].lower();s=0
 if c.get('match'):s+=6
 if re.search(r'mytholog|meyers|mkl|engrav|plate|dictionnaire|illustr|icon|painting|statue|bust|relief',t):s+=3
 if re.search(r'map|logo|flag|coin|stamp|screenshot|planet|globe|photo of|singer|actor|football|film',t):s-=8
 ar=(c.get('w') or 1)/(c.get('h') or 1)
 s-=abs(ar-.8)
 return s
figs=json.load(open(R/'figure-index.json'))
out={}
for f in figs:
 cs=sorted(pool.get(f['id'],{}).values(),key=score,reverse=True)
 out[f['id']]={'name':f['name'],'en':f['en']['name'],'myth':f['myth'],'candidates':cs[:6]}
(R/'art-pool.json').write_text(json.dumps(out,ensure_ascii=False,indent=1))
print('figures with candidates:',sum(1 for v in out.values() if v['candidates']))
print('none:',[k for k,v in out.items() if not v['candidates']])
