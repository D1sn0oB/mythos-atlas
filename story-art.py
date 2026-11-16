from pathlib import Path
import json,re,html,math
R=Path(__file__).parent;d=json.loads((R/'site-data.json').read_text());out=R/'assets/stories';out.mkdir(exist_ok=True)
def embed(file,prefix,x,y,w,h):
 s=file.read_text();s=re.sub(r'<svg\b[^>]*>',f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="'+('0 0 720 900' if file.parent.name=='figures' else '0 0 1200 900')+'">',s,count=1)
 s=re.sub(r'id="([^"]+)"',lambda m:'id="'+prefix+m.group(1)+'"',s);s=s.replace('url(#','url(#'+prefix);return s
n=0
for m in d['myths']:
 people=[f for f in d['figures'] if f['myth']==m['id']]
 for i,t in enumerate(m['stories']):
  text=t['title']+t['summary']+' '.join(t['paragraphs']);matches=[f for f in people if f['name'] in text]
  s=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="750" viewBox="0 0 1200 750"><defs><linearGradient id="veil" x2="0" y2="1"><stop stop-color="#080e16" stop-opacity="0"/><stop offset="1" stop-color="#080e16" stop-opacity=".9"/></linearGradient></defs>']
  s.append(embed(R/'assets'/f'{m["id"]}.svg','b-',-20,-90-i*8,1240,930))
  if matches:
   for j,f in enumerate(matches[:2]):s.append(embed(R/'assets/figures'/f'{f["id"]}.svg',f'p{j}-',180+j*410 if len(matches)>1 else 400,100,330,480))
  else:
   x=250+(i%4)*230;s.append(f'<circle cx="{x}" cy="240" r="{42+i*8}" fill="none" stroke="{m["color"]}" stroke-opacity=".45" stroke-width="1"/><circle cx="{x}" cy="240" r="{36+i*8}" fill="{m["color"]}" fill-opacity=".12"/>')
  s.append(f'<rect width="1200" height="750" fill="url(#veil)"/><path d="M60 650 H1140" stroke="{m["color"]}" stroke-opacity=".25"/><text x="65" y="690" font-family="serif" font-size="14" letter-spacing="4" fill="{m["color"]}">MYTHOS / {html.escape(m["en"])} / STORY {i+1:02}</text></svg>')
  (out/f'{m["id"]}-{i+1}.svg').write_text(''.join(s));n+=1
print(f'Created {n} original story compositions.')
