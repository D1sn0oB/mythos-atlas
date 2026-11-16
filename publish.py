from pathlib import Path
import json,shutil,zipfile
R=Path(__file__).parent
report=json.loads((R/'validation.json').read_text())
if not report['pass']:raise SystemExit('Refusing to publish: validation did not pass.')
P=Path('/var/minis/shared/mythos-atlas-v2');P.mkdir(parents=True,exist_ok=True)
# Only project resources and source code; external research snapshots stay outside the site.
allowed={'.html','.js','.css','.svg','.json','.md','.py','.jpg','.jpeg','.png','.webp','.gif','.ico'}
count=0
for p in R.rglob('*'):
 if p.is_file() and p.suffix in allowed and not p.name.endswith('-source.html') and '__pycache__' not in p.parts:
  t=P/p.relative_to(R);t.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(p,t);count+=1
Z=Path('/var/minis/shared/mythos-atlas-v2.zip')
with zipfile.ZipFile(Z,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for p in P.rglob('*'):
  if p.is_file():z.write(p,Path('mythos-atlas')/p.relative_to(P))
print(json.dumps({'published':str(P),'files':count,'zip':str(Z),'zip_bytes':Z.stat().st_size,'counts':report['counts']},ensure_ascii=False,indent=2))
