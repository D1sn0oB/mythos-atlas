from pathlib import Path
import math,random
ROOT=Path('/var/minis/workspace/mythos'); (ROOT/'assets').mkdir(parents=True,exist_ok=True)
styles={
'china':('#b2b99a','#a88853','MOUNTAINS'), 'japan':('#c76f62','#e0b59c','TORII'), 'greek':('#9baebf','#d2b896','TEMPLE'),
'norse':('#799b95','#bad4bc','TREE'),'egypt':('#c5a05c','#ddc38d','PYRAMID'),'celtic':('#7a9b80','#a9c8a2','KNOT'),
'roman':('#b28b7f','#d5bd9a','ROME'),'mesopotamia':('#b69a77','#d7bd86','ZIGGURAT'),'india':('#be8677','#e4b26a','LOTUS'),
'persia':('#8eabc1','#d5b989','WINGS'),'maya':('#82a698','#d4b787','MAYA'),'aztec':('#b28761','#e1b468','SUN'),
'inca':('#c5a267','#e3cda1','PEAKS'),'yoruba':('#b98b57','#e5c58c','MASK'),'west-africa':('#b48360','#dac696','BAOBAB'),
'polynesia':('#7bb6b9','#d0d5bb','WAVES'),'aboriginal':('#b17c65','#d6b58b','CIRCLES'),'korea':('#a6b2a5','#dfb891','KOREA')}
def line(d,stroke,sw=2,fill='none',extra=''):
 return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
for idx,(name,(c,a,kind)) in enumerate(styles.items()):
 r=random.Random(idx+22); s=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#080e13"/><stop offset="1" stop-color="{c}" stop-opacity=".38"/></linearGradient><radialGradient id="glow"><stop stop-color="{a}" stop-opacity=".18"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient><linearGradient id="stone" x2="1" y2="1"><stop stop-color="{c}"/><stop offset="1" stop-color="#111b20"/></linearGradient><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".58" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".09"/></feComponentTransfer><feBlend in="SourceGraphic" mode="soft-light"/></filter></defs><rect width="1200" height="900" fill="url(#sky)"/><ellipse cx="630" cy="370" rx="650" ry="540" fill="url(#glow)"/>''']
 for i in range(100):
  x,y=r.randrange(30,1170),r.randrange(25,600); s.append(f'<circle cx="{x}" cy="{y}" r="{r.uniform(.5,1.8):.1f}" fill="#e8e0d1" opacity="{r.uniform(.12,.65):.2f}"/>')
 s.append(f'<circle cx="600" cy="310" r="177" fill="none" stroke="{a}" opacity=".15"/><circle cx="600" cy="310" r="166" fill="none" stroke="{a}" opacity=".07"/>')
 # Layered distant ridges.
 for j in range(3):
  pts=[(0,650+j*45)]+[(x,r.randint(410,620)+j*55) for x in range(0,1300,130)]+[(1200,900),(0,900)]
  s.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="{c}" opacity="{.065+j*.025}"/>')
 s.append('<g filter="url(#grain)">')
 if kind in ['MOUNTAINS','KOREA']:
  s.append(f'<circle cx="780" cy="240" r="67" fill="{a}" opacity=".7"/>')
  for x,y,w in [(180,340,210),(500,260,190),(750,480,210),(1040,360,220)]:
   s.append(line(f'M{x-w} 820 Q{x-w/2} {y+110} {x} {y} Q{x+30} {y+190} {x+w} 820 Z',c,1,'url(#stone)'))
   s.append(line(f'M{x} {y+10} Q{x-25} {y+180} {x-90} 740',a,1,extra='opacity=".22"'))
  for y in [610,700,760]: s.append(line(f'M0 {y} Q230 {y-45} 480 {y+10} T1200 {y-10}',a,3,extra='opacity=".18"'))
  if kind=='KOREA':s.append(line('M800 590 L940 590 M820 580 L920 580 M815 580 Q870 560 920 580 M830 590 V640 M905 590 V640',a,5))
 elif kind=='TORII':
  s.append(f'<circle cx="600" cy="300" r="132" fill="{c}" opacity=".62"/><path d="M150 720 L620 350 L1000 720" fill="#222f32"/><path d="M513 435 L620 350 L707 435 L656 415 L628 438 L596 412 L557 443Z" fill="#acb4ac" opacity=".6"/>')
  s.append(line('M260 355 Q600 400 940 355 L925 390 Q600 432 275 390 Z',a,1,'#2c2021'))
  s.append(line('M350 420 H850 V447 H350 Z M400 405 L380 770 H424 L442 410 M758 410 L776 770 H820 L800 405',c,3,'#493536'))
  s.append(line('M590 409 V449 M610 409 V449',a,4)); s.append(line('M170 785 Q600 745 1030 785',a,2,extra='opacity=".3"'))
 elif kind in ['TEMPLE','ROME']:
  s.append(f'<circle cx="600" cy="260" r="90" fill="{a}" opacity=".25"/>')
  s.append(line('M265 414 L600 245 L935 414 Z M290 430 H910 V456 H290 Z',a,2,'url(#stone)'))
  for x in range(335,900,95):
   s.append(line(f'M{x} 469 H{x+48} L{x+43} 715 H{x+5}Z',a,1,'url(#stone)'))
   for dx in [14,25,36]:s.append(line(f'M{x+dx} 480 V700',a,1,extra='opacity=".22"'))
  for j in range(4):s.append(line(f'M{280-j*20} {720+j*16} H{920+j*20} V{730+j*16} H{280-j*20}Z',c,1,'#263036'))
 elif kind=='TREE':
  s.append(f'<circle cx="600" cy="370" r="260" fill="none" stroke="{a}" opacity=".3"/>')
  s.append(line('M545 780 Q610 610 581 477 Q537 385 500 350 M655 780 Q578 604 620 461 Q680 382 730 353 M590 520 Q430 480 350 390 M610 526 Q780 490 852 390',c,18))
  for i in range(17):
   angle=i*math.tau/17; x=600+math.cos(angle)*r.randrange(110,260); y=360+math.sin(angle)*r.randrange(70,180)
   s.append(line(f'M600 490 Q{x} {y+110} {x} {y}',a,r.randrange(2,6),extra='opacity=".55"'))
   s.append(f'<ellipse cx="{x}" cy="{y}" rx="85" ry="53" fill="{c}" opacity=".1"/>')
  for x in range(370,900,70):s.append(line(f'M600 700 Q{x} 730 {x} 810',a,2,extra='opacity=".6"'))
 elif kind in ['PYRAMID','PEAKS','MAYA','ZIGGURAT']:
  s.append(f'<circle cx="600" cy="290" r="87" fill="{a}" opacity=".7"/>')
  if kind in ['PYRAMID','PEAKS']:
   for x,y,w in [(230,540,240),(870,460,330),(530,350,350)]:
    s.append(line(f'M{x-w} 775 L{x} {y} L{x+w} 775 Z',c,1,'url(#stone)'));s.append(line(f'M{x} {y} L{x+70} 775 L{x+w} 775 Z',a,0,'#101c23'))
  else:
   for j in range(7):
    w=320-j*38;y=740-j*47;s.append(line(f'M{600-w} {y} H{600+w} V{y+48} H{600-w}Z',a,1,'url(#stone)'))
   s.append(line('M550 408 V365 H650 V408 M550 365 L600 345 L650 365 M568 740 L588 410 H613 L634 740',a,2,'#303635'))
 elif kind in ['LOTUS','SUN','KNOT','CIRCLES','MASK','WINGS']:
  s.append(f'<circle cx="600" cy="440" r="215" fill="#0d171b" stroke="{a}" stroke-width="2"/>')
  for ring in [180,198,235,247]:s.append(f'<circle cx="600" cy="440" r="{ring}" fill="none" stroke="{a}" opacity=".35"/>')
  if kind=='LOTUS':
   for i in range(12):
    s.append(f'<g transform="rotate({i*30} 600 440)">'+line('M600 435 Q495 320 600 231 Q705 320 600 435Z',a,1,'url(#stone)')+'</g>')
   s.append(f'<circle cx="600" cy="440" r="60" fill="#22232a" stroke="{a}"/>')
  elif kind=='MASK':
   s.append(line('M503 281 Q600 240 697 281 L680 510 L600 605 L520 510Z',a,2,'url(#stone)'))
   s.append(line('M540 355 L575 375 L537 390 M660 355 L625 375 L663 390 M600 360 L580 457 L615 457 M562 497 Q600 516 638 497',a,5))
   for x in range(555,650,16):s.append(line(f'M{x} 290 V327',a,2))
  elif kind=='WINGS':
   s.append(f'<circle cx="600" cy="430" r="65" stroke="{a}" fill="none" stroke-width="8"/>')
   for flip in [1,-1]:
    s.append(f'<g transform="translate(600 0) scale({flip} 1)">')
    for j in range(8):s.append(line(f'M60 {400+j*12} L{255-j*15} {350+j*22} L{232-j*15} {389+j*22} L60 {420+j*12}',a,2,'url(#stone)'))
    s.append('</g>')
  elif kind=='KNOT':
   for deg in [0,120,240]:s.append(f'<g transform="rotate({deg} 600 440)">'+line('M600 610 C375 470 420 260 600 300 C780 260 825 470 600 610Z',a,9)+'</g>')
  elif kind=='CIRCLES':
   for x,y in [(600,440),(470,360),(730,360),(470,540),(730,540)]:
    for radius in [12,25,38]:s.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="none" stroke="{a}" stroke-width="2"/>')
   s.append(line('M470 360 L600 440 L730 360 M470 540 L600 440 L730 540',a,3,extra='stroke-dasharray="3 8"'))
  else:
   for i in range(24):s.append(f'<g transform="rotate({i*15} 600 440)">'+line('M590 267 L600 215 L610 267Z',a,1,'url(#stone)')+'</g>')
   s.append(f'<circle cx="600" cy="440" r="118" fill="url(#stone)" stroke="{a}"/>');s.append(line('M552 415 H573 M627 415 H648 M600 430 V470 M565 492 Q600 510 635 492',a,5))
 elif kind=='BAOBAB':
  s.append(line('M530 790 Q565 550 530 450 L490 390 M665 790 Q615 530 660 430 L715 365 M558 530 L400 400 M630 510 L820 390',c,32))
  for x,y in [(400,375),(530,330),(675,325),(815,370)]:s.append(f'<ellipse cx="{x}" cy="{y}" rx="115" ry="63" fill="url(#stone)" stroke="{c}" opacity=".85"/>')
  s.append(f'<circle cx="890" cy="290" r="58" fill="{a}" opacity=".5"/>')
 elif kind=='WAVES':
  s.append(f'<circle cx="740" cy="280" r="90" fill="{a}" opacity=".6"/>');s.append(line('M210 620 L520 355 L780 620Z',c,1,'url(#stone)'))
  for j in range(7):
   y=570+j*38;s.append(line(f'M-100 {y} Q80 {y-120} 250 {y} T600 {y} T950 {y} T1300 {y}',a,2,extra=f'opacity="{.2+j*.06}"'))
 s.append('</g><path d="M0 810 Q300 760 600 810 T1200 800 V900 H0Z" fill="#080e13" opacity=".65"/><rect width="1200" height="900" fill="none" stroke="#ffffff" stroke-opacity=".025"/></svg>')
 (ROOT/'assets'/f'{name}.svg').write_text(''.join(s))
print('Created 18 original mythology illustrations.')
