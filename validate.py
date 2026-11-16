from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,subprocess,collections
R=Path(__file__).parent;d=json.loads((R/'site-data.json').read_text());errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
check(len(d['myths'])==19,'Expected 19 traditions')
check(len(d['figures'])>=220,'Too few figures')
check(len({x['id'] for x in d['figures']})==len(d['figures']),'Duplicate figure IDs')
for m in d['myths']:
 check(len(m['stories'])==6,f'{m["id"]}: expected 6 stories, got {len(m["stories"])}')
 check(len([f for f in d['figures'] if f['myth']==m['id']])>=8,m['id']+': too few figures')
 for i,s in enumerate(m['stories']):
  check(len(s['paragraphs'])>=3,s['title']+': missing story body')
  check((R/'stories'/f'{m["id"]}-{i+1}.html').exists(),s['title']+': missing story file')
 for k in ['orientation','history','figures','cosmos','stories','context','sources']:check((R/'learn'/f'{m["id"]}-{k}.html').exists(),'Missing chapter '+m['id']+'-'+k)
for f in d['figures']:
 check((R/'assets/figures'/f'{f["id"]}.svg').exists(),'Missing portrait '+f['id'])
 check(len(f['sections'])==4 and len(f['en']['sections'])==4,'Missing bilingual figure sections '+f['id'])
 check((R/'figures'/f'{f["id"]}.html').exists(),'Missing dossier '+f['id'])
class Links(HTMLParser):
 def __init__(self,p):super().__init__();self.p=p
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k not in ['href','src'] or not v:continue
   u=urlsplit(v)
   if u.scheme or u.netloc or not u.path:continue
   p=self.p.parent/unquote(u.path)
   check(p.exists(),str(self.p.relative_to(R))+': missing '+v)
for p in R.rglob('*.html'):Links(p).feed(p.read_text())
for f in ['app.js','learning.js','data.js','data-en.js','data-tw.js','figures.js','figures-tw.js','i18n.js','i18n-tw.js','religion.js','religion-tw.js','curriculum.js','curriculum-tw.js','reading.js','reading-tw.js','study-i18n.js','study-i18n-tw.js','guides.js','guides-tw.js','story-addons.js','story-addons-tw.js','translation-fixes.js']:
 p=subprocess.run(['node','--check',str(R/f)],capture_output=True,text=True);check(p.returncode==0,f+': syntax error '+p.stderr[:200])
keys=set(re.findall(r'\bUI\.([a-zA-Z_][a-zA-Z0-9_]*)',(R/'app.js').read_text()+(R/'learning.js').read_text()))
check(not(keys-set(d['ui'])),f'Missing Chinese UI keys: {keys-set(d["ui"])}')
counts={'traditions':len(d['myths']),'figures':len(d['figures']),'stories':sum(len(m['stories']) for m in d['myths']),'chapters':len(list((R/'learn').glob('*.html'))),'html':len(list(R.rglob('*.html'))),'portraits':len(list((R/'assets/figures').glob('*.svg')))}
report={'pass':not errors,'counts':counts,'errors':errors}
(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
