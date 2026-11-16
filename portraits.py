from pathlib import Path
import json,random,math,html
R=Path(__file__).parent; OUT=R/'assets'/'figures';OUT.mkdir(parents=True,exist_ok=True)
figures=json.loads((R/'figure-index.json').read_text())
FEMALE={'nuwa','change','xiwangmu','izanami','amaterasu','konohanasakuya','devi','ungnyeo','bari','mary','hera','athena','artemis','aphrodite','freyja','juno','minerva','venus','brigid','morrigan','rhiannon','isis','inanna','anahita','xquic','coatlicue','pachamama','mama-quilla','mama-ocllo','oshun','asase-yaa','aso','hina','pele'}
GOLD='#d3bd87'
def path(d,fill='none',stroke=GOLD,w=1,extra=''):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" {extra}/>'
def circle(x,y,r,fill='none',stroke=GOLD,opacity=1):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" opacity="{opacity}"/>'
# Original props; no copied ritual diagrams or restricted cultural designs.
def prop(kind,side=1):
 x=535 if side==1 else 185; out=['<g>']
 if kind in ['spear','staff','trident','hammer','axe','sword','bow','hook','flail','crook','torch','lily','key','wheat','branch','scroll','mirror','fan']:
  if kind not in ['bow','mirror','fan','scroll']:out.append(path(f'M{x} 755 L{x-12} 330',stroke='#bca77a',w=7))
 if kind=='spear':out.append(path(f'M{x-12} 330 L{x-38} 280 L{x-15} 190 L{x+14} 279 Z','url(#metal)',w=2))
 elif kind=='trident':out.append(path(f'M{x-13} 335 V220 M{x-60} 235 Q{x-57} 315 {x-13} 310 Q{x+30} 315 {x+35} 235 M{x-60} 235 L{x-68} 257 M{x+35} 235 L{x+43} 257',w=5))
 elif kind=='hammer':out.append(path(f'M{x-80} 245 L{x+46} 237 L{x+52} 309 L{x-73} 318 Z','url(#metal)',w=2));out.append(path(f'M{x-65} 258 L{x+30} 252 M{x-61} 301 L{x+35} 292',w=1))
 elif kind=='axe':out.append(path(f'M{x-15} 235 Q{x+72} 201 {x+75} 298 Q{x+15} 332 {x-13} 287 Z','url(#metal)',w=2))
 elif kind=='sword':out.append(path(f'M{x-25} 585 L{x-30} 285 L{x-15} 205 L{x+1} 285 L{x-3} 585 Z','url(#metal)',w=2));out.append(path(f'M{x-62} 590 L{x+32} 587',w=8))
 elif kind=='bow':out.append(path(f'M{x-20} 195 Q{x+110} 470 {x-8} 738 M{x-20} 195 L{x-8} 738',w=5));out.append(path(f'M{x-65} 745 L{x+37} 260 L{x+17} 280 M{x+37} 260 L{x+42} 289',w=3))
 elif kind=='hook':out.append(path(f'M{x-25} 640 Q{x+30} 540 {x+10} 415 Q{x-10} 320 {x-70} 345 Q{x-110} 364 {x-65} 407 L{x-60} 367',stroke='#d9cba7',w=17))
 elif kind=='crook':out.append(path(f'M{x-12} 340 Q{x-70} 345 {x-60} 282 Q{x-33} 247 {x-3} 280',w=9))
 elif kind=='flail':
  for d in [0,17,34]:out.append(path(f'M{x-15} 310 Q{x-75+d} 350 {x-49+d} 430',w=4))
 elif kind=='torch':out.append(path(f'M{x-30} 315 Q{x-70} 267 {x-13} 185 Q{x-25} 255 {x+15} 242 Q{x+55} 300 {x-30} 315Z','#c9935366',w=2))
 elif kind=='lily':
  for y in [300,350,400]:out.append(path(f'M{x-13} {y} q-50 -60 -45 -75 q45 0 45 40 q35 -50 60 -35 q-5 55 -60 70Z','#d1c7a377',w=1))
 elif kind=='key':out.append(circle(x-15,280,36,'#16212a',opacity=.9));out.append(path(f'M{x-13} 319 V480 H{x+20} V460 H{x-13}',w=7))
 elif kind=='wheat':
  for j in range(7):out.append(path(f'M{x-14} {300+j*18} q-35 -25 -28 -43 q25 5 28 25 q25 -20 29 -23 q8 25 -29 41','#aa9d6866',w=1))
 elif kind=='branch':
  for j in range(7):out.append(path(f'M{x-13} {300+j*31} q-70 -10 -65 -40 q30 -25 65 20 q45 -35 70 -25 q-10 40 -70 45','#74958666',w=1))
 elif kind=='scroll':out.append(path(f'M{x-70} 480 Q{x-50} 440 {x-25} 455 L{x+38} 468 V650 L{x-70} 632 Z','url(#cloth)',w=2));out.append(path(f'M{x-55} 493 l68 16 m-68 10 68 16 m-68 10 68 16 m-68 10 68 16',w=1))
 elif kind=='mirror':out.append(circle(x,460,55,'url(#halo)',opacity=.9));out.append(path(f'M{x} 515 V635',w=10));out.append(circle(x,460,47,stroke='#bfc2ae',opacity=.3))
 elif kind=='fan':out.append(path(f'M{x-60} 435 Q{x-30} 330 {x+50} 390 L{x} 520Z','url(#cloth)',w=2));out.append(path(f'M{x} 520 L{x-40} 418 M{x} 520 L{x-12} 391 M{x} 520 L{x+22} 387 M{x} 520 V610',w=2))
 out.append('</g>');return ''.join(out)
SPECIAL={
'pangu':('axe','beard'),'nuwa':('snake','female'),'fuxi':('snake','beard'),'jade-emperor':('scroll','emperor'),'houyi':('bow','warrior'),'change':('moon','female'),'xiwangmu':('branch','queen'),'dayu':('staff','beard'),
'izanagi':('spear','beard'),'izanami':('fan','female'),'amaterasu':('sun','queen'),'susanoo':('sword','warrior'),'tsukuyomi':('moon','court'),'okuninushi':('staff','court'),'inari':('wheat','fox'),'konohanasakuya':('branch','female'),
'brahma':('scroll','beard'),'vishnu':('disc','crown'),'shiva':('trident','beard'),'devi':('sword','queen'),'ganesha':('lotus','elephant'),'hanuman':('staff','monkey'),
'dangun':('staff','emperor'),'hwanung':('scroll','emperor'),'ungnyeo':('branch','female'),'jumong':('bow','warrior'),'haemosu':('bow','emperor'),'bari':('lily','female'),
'jesus':('cross','beard'),'mary':('lily','female'),'michael':('sword','angel'),'gabriel':('lily','angel'),'peter':('key','beard'),'paul':('scroll','beard'),'moses':('tablets','beard'),'abraham':('staff','beard'),
'zeus':('lightning','beard'),'hera':('staff','queen'),'athena':('spear','helmet'),'apollo':('lyre','youth'),'artemis':('bow','female'),'poseidon':('trident','beard'),'hades':('staff','beard'),'aphrodite':('shell','female'),
'odin':('spear','oneeye'),'thor':('hammer','beard'),'loki':('flame','youth'),'freyja':('mirror','queen'),'freyr':('sword','crown'),'tyr':('sword','warrior'),'baldr':('sun','youth'),'heimdall':('horn','warrior'),
'jupiter':('lightning','beard'),'juno':('staff','queen'),'minerva':('spear','helmet'),'mars':('sword','helmet'),'venus':('shell','female'),'janus':('key','janus'),
'dagda':('staff','beard'),'brigid':('torch','female'),'lugh':('spear','warrior'),'morrigan':('raven','queen'),'cu-chulainn':('spear','warrior'),'rhiannon':('branch','queen'),
'ra':('sun','falcon'),'osiris':('crook','osiris'),'isis':('wings','queen'),'horus':('spear','falcon'),'seth':('staff','seth'),'anubis':('staff','jackal'),
'anu':('staff','crown'),'enlil':('staff','crown'),'enki':('water','beard'),'inanna':('star','queen'),'marduk':('spear','crown'),'gilgamesh':('axe','beard'),
'ahura-mazda':('light','cosmic'),'angra-mainyu':('shadow','cosmic'),'mithra':('sun','crown'),'anahita':('water','queen'),'jamshid':('disc','emperor'),'rostam':('sword','warrior'),
'hunahpu':('ball','youth'),'xbalanque':('ball','warrior'),'xquic':('branch','female'),'maize-god':('wheat','youth'),'itzamna':('scroll','beard'),'chaac':('axe','rain'),
'quetzalcoatl':('feather','serpent'),'tezcatlipoca':('mirror','warrior'),'huitzilopochtli':('spear','crown'),'tlaloc':('water','rain'),'coatlicue':('snake','queen'),'mictlantecuhtli':('staff','skull'),
'inti':('sun','cosmic'),'viracocha':('staff','beard'),'pachamama':('earth','female'),'mama-quilla':('moon','queen'),'manco-capac':('staff','emperor'),'mama-ocllo':('cloth','female'),
'olodumare':('light','cosmic'),'obatala':('staff','white'),'ogun':('sword','warrior'),'shango':('doubleaxe','crown'),'oshun':('fan','queen'),'eshu':('staff','court'),
'anansi':('web','spider'),'nyame':('sun','cosmic'),'asase-yaa':('earth','female'),'aso':('scroll','headwrap'),'ntikuma':('pot','youth'),'osebo':('spots','leopard'),
'maui':('hook','warrior'),'hina':('cloth','female'),'tangaroa':('water','beard'),'tane':('branch','beard'),'pele':('flame','female'),'ruaumoko':('earth','cosmic'),
'bunjil':('sky','eagle'),'waa':('flame','crow'),'baiame':('land','cosmic'),'daramulum':('sky','cosmic'),'rainbow-serpent':('water','serpent'),'julunggul':('water','serpent')}
COLORS={'china':'#9cac92','japan':'#c18883','india':'#b697c0','korea':'#9caba8','christianity':'#a9a5c5','greek':'#a5b6c4','norse':'#8ca6a1','roman':'#bc9789','celtic':'#91ae95','egypt':'#c0a269','mesopotamia':'#b69a77','persia':'#8faac0','maya':'#84a497','aztec':'#bd996f','inca':'#c0a571','yoruba':'#bf9a70','west-africa':'#b58c69','polynesia':'#87b8bb','aboriginal':'#b58e7b'}
SPECIAL.update({'leigong':('hammer','warrior'),'zhurong':('torch','crown'),'uzume':('fan','female'),'ame-no-uzume':('fan','female'),'sarutahiko':('staff','warrior'),'lakshmi':('lotus','queen'),'saraswati':('lyre','female'),'yuhwa':('branch','female'),'geumwa':('sun','emperor'),'john-baptist':('crossstaff','beard'),'john-the-baptist':('crossstaff','beard'),'john-apostle':('scroll','youth'),'john-the-apostle':('scroll','youth'),'demeter':('wheat','female'),'hermes':('staff','youth'),'hel':('shadow','queen'),'frigg':('cloth','queen'),'saturn':('axe','beard'),'saturnus':('axe','beard'),'vulcan':('hammer','beard'),'vulcanus':('hammer','beard'),'manannan':('water','beard'),'boann':('water','female'),'amenouzume':('fan','female'),'thoth':('scroll','ibis'),'hathor':('sun','horned'),'ereshkigal':('staff','queen'),'dumuzi':('staff','youth'),'zal':('branch','white'),'simurgh':('sky','eagle'),'hun-hunahpu':('ball','warrior'),'vucub-caquix':('sun','eagle'),'xipe-totec':('wheat','warrior'),'xochiquetzal':('branch','female'),'illapa':('lightning','warrior'),'mama-cocha':('water','female'),'oya':('fan','queen'),'orunmila':('scroll','beard'),'onini':('earth','serpent'),'mmoboro':('sky','cosmic'),'tawhirimatea':('water','cosmic'),'hine-nui-te-po':('moon','female'),'wagyl':('water','serpent'),'ngalyod':('water','serpent')})
for idx,f in enumerate(figures):
 key=f['id'][len(f['myth'])+1:];kind,face=SPECIAL.get(key,('branch','female' if key in FEMALE else 'crown'));c=COLORS[f['myth']];r=random.Random(idx*41)
 s=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="720" height="900" viewBox="0 0 720 900" role="img"><title>{html.escape(f['name'])} — original symbolic illustration</title><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#0c131d"/><stop offset="1" stop-color="{c}" stop-opacity=".45"/></linearGradient><radialGradient id="halo"><stop stop-color="{c}" stop-opacity=".4"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient><linearGradient id="cloth" x2="1" y2="1"><stop stop-color="{c}"/><stop offset=".5" stop-color="#394551"/><stop offset="1" stop-color="#18242e"/></linearGradient><linearGradient id="skin" x2="1" y2="1"><stop stop-color="#d0b78e"/><stop offset=".5" stop-color="#b89a76"/><stop offset="1" stop-color="#72665a"/></linearGradient><linearGradient id="metal" x2="1" y2="1"><stop stop-color="#e0d5ae"/><stop offset=".45" stop-color="#8e8d82"/><stop offset="1" stop-color="#4e6269"/></linearGradient></defs><rect width="720" height="900" fill="#0a1018"/><rect width="720" height="900" fill="url(#bg)"/><ellipse cx="360" cy="360" rx="350" ry="390" fill="url(#halo)"/>''']
 for i in range(50):s.append(circle(r.randrange(30,690),r.randrange(30,800),r.uniform(.4,1.3),'#e0d3b2',stroke='none',opacity=r.uniform(.1,.5)))
 s.extend([circle(360,320,230,opacity=.14),circle(360,320,217,opacity=.08),path('M55 825 V280 Q55 115 360 38 Q665 115 665 280 V825',stroke=c,extra='opacity=".16"'),path('M40 840 H680 M40 855 H680',stroke=c,extra='opacity=".2"')])
 if face=='cosmic':
  for j in range(7):s.append(circle(360,400,45+j*24,stroke=c,opacity=.6-j*.07))
  if kind in ['earth','land']:
   s.append(path('M80 740 Q200 430 340 650 Q450 360 640 740Z','url(#cloth)',stroke=c));s.append(circle(360,260,63,'url(#halo)',opacity=.7))
  elif kind=='shadow':
   s.append(path('M200 650 Q260 470 300 390 Q280 250 360 170 Q440 250 420 390 Q500 500 520 650 Q360 590 200 650Z','#17202a',stroke=c,w=2))
  else:
   for j in range(12):s.append(f'<g transform="rotate({j*30} 360 400)">'+path('M360 180 L352 235 L368 235Z',c,stroke=c)+'</g>')
   s.append(path('M360 283 L375 381 L472 400 L375 419 L360 517 L345 419 L248 400 L345 381Z',c,stroke=c,w=1));s.append(circle(360,400,20,'#d9d0b5'))
 elif face in ['eagle','crow']:
  dark='#1b2834' if face=='crow' else '#726d60';s.append(path('M349 410 Q225 250 75 345 Q135 450 285 490 L205 715 L355 630 L440 720 L425 500 Q585 470 660 345 Q480 255 380 410Z','url(#cloth)',w=2))
  for sign in [-1,1]:
   for j in range(7):s.append(path(f'M{360+sign*40} 470 Q{360+sign*(140+j*12)} {360-j*4} {360+sign*(240-j*15)} {385+j*19}',stroke='#d5c49c',w=1,extra='opacity=".5"'))
  s.append(path('M330 430 Q300 350 347 305 Q385 285 422 330 L452 345 L418 362 Q406 410 375 440Z',dark,w=2));s.append(circle(392,333,6,'#d8bd7d',stroke='#0c1119'));s.append(path('M347 615 L320 757 M381 616 L404 757 M301 759 H341 M386 759 H426',w=5))
 elif face=='spider':
  s.append(circle(360,490,85,'url(#cloth)',opacity=1));s.append(circle(360,382,48,'url(#metal)'))
  for sign in [-1,1]:
   for j in range(4):s.append(path(f'M{360+sign*50} {410+j*30} L{360+sign*(170+j*8)} {315+j*85} L{360+sign*(230-j*5)} {420+j*92}',stroke=c,w=6))
  for j in range(8):s.append(path(f'M360 100 L{110+j*72} 810',stroke=c,extra='opacity=".09"'))
  s.append(circle(343,376,5,'#e0d4b2'));s.append(circle(377,376,5,'#e0d4b2'))
 elif face=='serpent':
  s.append(path('M180 760 C630 830 560 530 320 520 C150 510 230 315 410 350 C530 370 540 240 410 200',stroke=c,w=55));s.append(path('M180 760 C630 830 560 530 320 520 C150 510 230 315 410 350 C530 370 540 240 410 200',stroke=GOLD,w=2))
  for j in range(6) if kind=='feather' else []:s.append(path(f'M{415+j*13} {218+j*8} l{30+j*2} -60',stroke=c,w=5))
  s.append(path('M410 181 Q340 167 324 210 L360 238 L427 229Z','url(#metal)',w=2));s.append(circle(365,200,5,'#111923'))
 elif face=='leopard':
  s.append(path('M170 760 Q145 520 230 400 L270 300 Q360 250 450 300 L490 400 Q575 520 550 760Z','url(#cloth)',w=2));s.append(path('M235 395 L223 284 L300 322 M485 395 L500 284 L421 322','url(#cloth)',w=2))
  for j in range(65):
   x,y=r.randrange(210,510),r.randrange(360,750);s.append(circle(x,y,r.randrange(4,9),stroke='#12202a',opacity=.8))
  s.append(path('M280 421 L320 430 M400 430 L440 421 M336 475 L360 493 L384 475 M360 493 V520 M310 535 Q360 566 410 535',stroke='#d5c49c',w=5))
 else:
  female=key in FEMALE or face in ['female','queen','headwrap','horned'];skin='url(#skin)';cx=350+r.randrange(-12,13)
  if face=='angel':
   for sign in [-1,1]:
    s.append(path(f'M360 500 Q{360+sign*150} 180 {360+sign*290} 220 Q{360+sign*280} 480 {360+sign*105} 640Z','url(#cloth)',w=2))
    for j in range(9):s.append(path(f'M{360+sign*75} 535 Q{360+sign*(180+j*7)} {400-j*11} {360+sign*(265-j*10)} {245+j*17}',w=1,extra='opacity=".45"'))
  s.append(path(f'M{cx-130} 458 Q{cx-100} 411 {cx-50} 403 H{cx+48} Q{cx+98} 411 {cx+130} 458 L{cx+192} 808 Q{cx} 862 {cx-192} 808Z','url(#cloth)',stroke=c,w=2))
  s.append(path(f'M{cx-30} 397 V439 L{cx} 467 L{cx+34} 438 V397Z',skin,stroke='#8d806b'))
  # Sleeves and hands are readable silhouettes, not photorealistic skin.
  s.append(path(f'M{cx-110} 445 L{cx-170} 608 L{cx-145} 650 L{cx-76} 525 M{cx+107} 445 L{cx+160} 586 L{cx+136} 633 L{cx+72} 521','url(#cloth)',stroke=c,w=2))
  s.append(path(f'M{cx-167} 605 q-17 17 -4 34 q13 16 28 0 l8 -20Z',skin,stroke='#9c8f77'));s.append(path(f'M{cx+141} 582 q26 -10 29 9 q2 21 -22 31 l-13 -22Z',skin,stroke='#9c8f77'))
  for dx in [-97,-47,16,78]:s.append(path(f'M{cx+dx/2} 477 Q{cx+dx} 643 {cx+dx*1.35} 804',stroke='#d6c6a1',extra='opacity=".2"'))
  s.append(path(f'M{cx-105} 568 Q{cx} 602 {cx+108} 566 L{cx+111} 588 Q{cx} 623 {cx-110} 590Z','#95815c',stroke=GOLD,w=1))
  # Hair mass behind the face.
  s.append(path(f'M{cx-76} 382 Q{cx-111} 239 {cx} 223 Q{cx+110} 239 {cx+79} 388 L{cx+96} 458 L{cx-86} 458Z','#20232a',stroke=c))
  if face in ['falcon','ibis','jackal','seth','elephant','monkey','skull','rain']:
   if face=='elephant':s.append(path(f'M{cx-68} 288 Q{cx-143} 252 {cx-133} 342 Q{cx-128} 398 {cx-69} 382 M{cx+67} 288 Q{cx+143} 252 {cx+133} 342 Q{cx+128} 398 {cx+69} 382','url(#skin)',w=2));s.append(path(f'M{cx-63} 274 Q{cx} 235 {cx+63} 274 L{cx+48} 368 Q{cx+13} 385 {cx+29} 446 Q{cx+15} 484 {cx-6} 446 V366 Q{cx-54} 374 {cx-63} 274Z',skin,w=2))
   elif face in ['jackal','seth']:s.append(path(f'M{cx-58} 280 L{cx-80} 164 L{cx-22} 252 L{cx+18} 252 L{cx+65} 164 L{cx+50} 302 L{cx+103} 341 L{cx+68} 381 L{cx-20} 397 L{cx-59} 340Z','#283039',w=2))
   elif face=='ibis':s.append(path(f'M{cx-59} 372 L{cx-62} 290 Q{cx-32} 235 {cx+28} 264 Q{cx+54} 284 {cx+54} 315 Q{cx+141} 325 {cx+145} 440 Q{cx+118} 369 {cx+37} 343 L{cx+22} 394Z','url(#metal)',w=2));s.append(circle(cx+13,293,5,'#15212b'))
   elif face=='falcon':s.append(path(f'M{cx-61} 292 Q{cx-45} 231 {cx+24} 251 L{cx+61} 287 L{cx+117} 315 L{cx+62} 334 L{cx+29} 391 L{cx-53} 373Z','url(#metal)',w=2));s.append(path(f'M{cx+17} 281 L{cx+43} 289 L{cx+20} 300 M{cx+17} 300 l-6 33',stroke='#17232e',w=5))
   elif face=='skull':s.append(path(f'M{cx-60} 291 Q{cx} 240 {cx+60} 291 L{cx+45} 375 L{cx+24} 408 H{cx-24} L{cx-45} 375Z','#baa888',w=2));s.append(circle(cx-26,322,19,'#1d2630'));s.append(circle(cx+26,322,19,'#1d2630'));s.append(path(f'M{cx} 342 l-10 20 h20Z M{cx-28} 383 H{cx+28}',stroke='#1d2630',w=5))
   elif face=='rain':s.append(path(f'M{cx-65} 277 H{cx+65} V379 L{cx} 414 L{cx-65} 379Z','url(#cloth)',w=2));s.append(circle(cx-30,318,27,'#1b2935'));s.append(circle(cx+30,318,27,'#1b2935'));s.append(path(f'M{cx-30} 370 h60 M{cx-20} 370 v29 M{cx+20} 370 v29',w=8))
   else:s.append(path(f'M{cx-54} 280 Q{cx} 245 {cx+54} 280 L{cx+64} 351 L{cx+26} 402 H{cx-26} L{cx-64} 351Z',skin,w=2));s.append(path(f'M{cx-34} 318 Q{cx} 300 {cx+34} 318 L{cx+26} 378 H{cx-26}Z','#c9b693',w=1))
  else:
   s.append(path(f'M{cx-57} 284 Q{cx} 250 {cx+57} 284 L{cx+53} 355 Q{cx+30} 406 {cx} 410 Q{cx-30} 406 {cx-53} 355Z',skin,stroke='#b7a37c',w=1))
   s.append(path(f'M{cx-40} 322 q15 -9 29 0 M{cx+12} 322 q15 -9 29 0 M{cx+1} 326 l-7 31 14 1 M{cx-17} 377 q17 8 34 0',stroke='#4d504a',w=2))
   if face=='oneeye':s.append(path(f'M{cx-46} 310 L{cx-7} 336 M{cx-48} 334 L{cx-6} 310','#1a232b',stroke='#18212a',w=8))
   if face in ['beard','oneeye','emperor','osiris','janus']:
    s.append(path(f'M{cx-50} 350 Q{cx-37} 400 {cx} 378 Q{cx+37} 400 {cx+50} 350 Q{cx+65} 432 {cx} 475 Q{cx-65} 432 {cx-50} 350Z','#444b4a',stroke=c,w=1));s.append(path(f'M{cx-25} 401 L{cx-9} 447 M{cx} 402 V460 M{cx+25} 401 L{cx+9} 447',stroke='#b4a581',extra='opacity=".4"'))
  if face in ['crown','queen','emperor','osiris']:
   s.append(path(f'M{cx-75} 283 L{cx-76} 221 L{cx-39} 242 L{cx} 191 L{cx+39} 242 L{cx+76} 221 L{cx+75} 283Z','url(#metal)',w=2));s.append(path(f'M{cx-62} 267 H{cx+62}',w=3));s.append(circle(cx,239,8,'#647f86'))
  if face=='horned':s.append(path(f'M{cx-38} 262 Q{cx-125} 204 {cx-67} 151 Q{cx-85} 218 {cx} 230 Q{cx+85} 218 {cx+67} 151 Q{cx+125} 204 {cx+38} 262','url(#metal)',w=2));s.append(circle(cx,207,41,'#c7a565',opacity=.85))
  if face=='helmet':s.append(path(f'M{cx-75} 326 V284 Q{cx-70} 207 {cx} 209 Q{cx+70} 207 {cx+75} 284 V326 L{cx+52} 308 L{cx+40} 275 H{cx-40} L{cx-52} 308Z','url(#metal)',w=2));s.append(path(f'M{cx-32} 216 Q{cx-20} 115 {cx+27} 173 L{cx+52} 218','#857e69',w=2))
  if face in ['female','white','headwrap'] or key in ['mary','jesus']:
   s.append(path(f'M{cx-87} 443 Q{cx-115} 241 {cx} 222 Q{cx+115} 241 {cx+91} 447 L{cx+62} 426 Q{cx+74} 276 {cx} 258 Q{cx-74} 276 {cx-62} 426Z',('#c5c5b3' if face=='white' else 'url(#cloth)'),stroke=c,w=2))
  if kind in ['snake']:
   s.append(path(f'M{cx-68} 644 C50 780 160 893 400 806 C570 744 564 845 675 815',stroke=c,w=55));s.append(path(f'M{cx-68} 644 C50 780 160 893 400 806 C570 744 564 845 675 815',stroke=GOLD,w=2))
  if face=='janus':s.append(path(f'M{cx-50} 291 L{cx-94} 324 L{cx-76} 347 L{cx-64} 376',skin,w=2))
  if kind in ['sun','moon','star','disc','lightning','cross']:
   if kind=='moon':s.append(path('M478 113 A93 93 0 1 0 561 244 A77 77 0 0 1 478 113Z','#c6c8b4',stroke=GOLD,w=1,extra='opacity=".55"'))
   elif kind=='cross':s.append(circle(cx,303,111,opacity=.8));s.append(path(f'M{cx} 179 V216 M{cx-113} 303 H{cx-84} M{cx+84} 303 H{cx+113}',w=6))
   elif kind=='lightning':s.append(path('M560 260 L481 421 H535 L490 583 L607 380 H552Z','#d4c495',w=2))
   else:
    s.append(circle(cx,277,140,stroke=c,opacity=.6))
    if kind=='star':
     for j in range(8):s.append(f'<g transform="rotate({j*45} {cx} 277)">'+path(f'M{cx} 119 L{cx-5} 145 H{cx+5}Z',c)+'</g>')
  if kind=='crossstaff':s.append(prop('staff',side=1));s.append(path('M488 295 H559',w=6));s.append(circle(cx,300,110,opacity=.35))
  if kind=='lyre':s.append(path('M497 412 Q480 530 545 543 Q610 530 592 412 M499 428 H590 M517 430 V529 M533 430 V537 M551 430 V537 M569 430 V529','none',GOLD,5))
  if kind=='horn':s.append(path('M504 450 Q525 524 591 492 L620 450 L588 429 Q562 498 520 435Z','url(#metal)',w=2))
  if kind=='tablets':s.append(path('M487 492 V407 Q512 376 538 407 V492Z M546 492 V407 Q571 376 597 407 V492Z','url(#metal)',w=2));s.append(path('M499 421 h26 m-26 17 h26 m-26 17 h26 M558 421 h26 m-26 17 h26 m-26 17 h26',stroke='#43505a',w=2))
  if kind in ['cloth','pot','ball','shell','lotus','earth']:
   if kind=='pot':s.append(path('M151 567 Q114 585 140 656 Q182 677 220 656 Q246 585 210 567Z','url(#metal)',w=2));s.append(path('M146 562 H215',w=5))
   elif kind=='cloth':s.append(path('M153 488 L217 503 L231 689 L143 676Z','url(#cloth)',w=2));s.append(path('M156 521 L220 536 M156 552 L224 567 M153 586 L225 601',w=2))
   else:s.append(circle(181,556,43,'url(#halo)',opacity=.9));s.append(path('M147 556 Q181 514 215 556 Q181 598 147 556',stroke=c,w=2))
  if kind=='doubleaxe':s.append(prop('axe'));s.append(path('M510 235 Q430 201 427 298 Q487 332 516 287Z','url(#metal)',w=2))
  elif kind in ['spear','staff','trident','hammer','axe','sword','bow','hook','crook','torch','lily','key','wheat','branch','scroll','mirror','fan']:s.append(prop(kind,side=-1 if kind in ['staff','branch','scroll'] else 1))
  if kind in ['flame','water']:
   for j in range(4):
    y=700+j*23;s.append(path(f'M80 {y} Q190 {y-55} 305 {y} T530 {y} T740 {y}',stroke=('#cf9a6b' if kind=='flame' else '#91bdc3'),w=2,extra='opacity=".45"'))
 s.append(f'<rect x="20" y="20" width="680" height="860" rx="2" fill="none" stroke="{c}" stroke-opacity=".2"/><path d="M20 55 V20 H55 M665 20 H700 V55 M20 845 V880 H55 M665 880 H700 V845" fill="none" stroke="{c}" stroke-opacity=".65"/><rect y="815" width="720" height="85" fill="#090f18" opacity=".35"/><text x="45" y="853" fill="{c}" opacity=".65" font-family="serif" font-size="12" letter-spacing="3">MYTHOS / FIGURE {idx+1:03}</text></svg>')
 (OUT/f'{f["id"]}.svg').write_text(''.join(s))
print(f'Created {len(figures)} original individual symbolic portraits.')
