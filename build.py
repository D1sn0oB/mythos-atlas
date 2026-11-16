from pathlib import Path
import html
import subprocess,json,re,zipfile,time
VERSION=str(time.time_ns())
R=Path(__file__).parent
NAMES={'christianity':'圣经叙事与基督教传统','china':'中国神话','japan':'日本神话','greek':'希腊神话','norse':'北欧神话','egypt':'埃及神话','celtic':'凯尔特神话','roman':'罗马神话','mesopotamia':'两河流域神话','india':'印度神话','persia':'波斯神话','maya':'玛雅神话','aztec':'阿兹特克神话','inca':'印加神话','yoruba':'约鲁巴神话','west-africa':'西非故事传统','polynesia':'波利尼西亚神话','aboriginal':'澳大利亚原住民传统','korea':'朝鲜半岛神话'}
base='''<!doctype html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="theme-color" content="#080c10"><meta name="description" content="{description}"><title>{title} — MYTHOS 神话星图</title><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"><link rel="stylesheet" href="{prefix}style.css"><script defer src="{prefix}data.js"></script><script defer src="{prefix}data-en.js"></script><script defer src="{prefix}translation-fixes.js"></script><script defer src="{prefix}data-tw.js"></script><script defer src="{prefix}religion.js"></script><script defer src="{prefix}religion-tw.js"></script><script defer src="{prefix}figures.js"></script><script defer src="{prefix}figures-tw.js"></script><script defer src="{prefix}i18n.js"></script><script defer src="{prefix}i18n-tw.js"></script><script defer src="{prefix}reading.js"></script><script defer src="{prefix}reading-tw.js"></script><script defer src="{prefix}story-addons.js"></script><script defer src="{prefix}story-addons-tw.js"></script><script defer src="{prefix}guides.js"></script><script defer src="{prefix}guides-tw.js"></script><script defer src="{prefix}curriculum.js"></script><script defer src="{prefix}curriculum-tw.js"></script><script defer src="{prefix}study-i18n.js"></script><script defer src="{prefix}study-i18n-tw.js"></script><script defer src="{prefix}art-manifest.js"></script><script defer src="{prefix}learning.js"></script><script defer src="{prefix}app.js"></script></head>
<body data-page="{page}" data-depth="{depth}" {extra}><a class="skip-link" href="#main">Skip to content / 跳至正文</a><canvas id="starfield" aria-hidden="true"></canvas><div class="wrap"><div id="header"></div><main id="main" tabindex="-1">{fallback}</main><div id="footer"></div></div><div class="toast" id="toast" role="status" aria-live="polite"></div><noscript><div class="noscript">请启用 JavaScript 以浏览星图。Please enable JavaScript to explore the atlas.</div></noscript></body></html>'''
def page(path,title,kind,extra='',fallback=''):
 p=R/path;p.parent.mkdir(exist_ok=True,parents=True);depth=1 if '/' in path else 0
 p.write_text(re.sub(r'((?:src|href)="[^"#]+\.(?:js|css|svg))"',lambda m:m.group(1)+'?v='+VERSION+'"',base.format(title=title,page=kind,depth=depth,prefix='../' if depth else '',extra=extra,fallback=fallback,description='跨越五大洲与十九个叙事传统，探索图文人物详解、传奇故事与分层学习章节。支持简体中文、繁體中文与 English。深空中的世界神话阅读地图。')))
for p,t,k in [('index.html','万神之境','home'),('stories.html','故事典藏','stories'),('saved.html','我的星藏','saved'),('about.html','关于星图','about'),('figures.html','人物列传','figures'),('learning.html','学习地图','learning')]:page(p,t,k)
for id,name in NAMES.items():
 page(f'worlds/{id}.html',name,'world',f'data-world="{id}"')
 for i in range(2):page(f'stories/{id}-{i+1}.html',name+' · 传奇故事','article',f'data-world="{id}" data-story="{i}"')
# Compile Traditional Chinese into ordinary JS so the site needs no runtime translation API.
ui=(R/'i18n.js').read_text().split('window.UI_EN=')[0].replace('window.UI_CN','window.UI_TW')
def traditional(txt):
 return subprocess.run(['opencc','-c','s2twp.json'],input=txt,text=True,capture_output=True,check=True).stdout
(R/'i18n-tw.js').write_text(traditional(ui))
if (R/'data.js').exists():
 text=(R/'data.js').read_text().replace('window.MYTHS =','window.MYTHS_TW =').replace('window.MYTHS=','window.MYTHS_TW=')
 (R/'data-tw.js').write_text(traditional(text))
(R/'assets/favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#080c10"/><g stroke="#c3a778" fill="none"><circle cx="32" cy="32" r="21"/><ellipse cx="32" cy="32" rx="27" ry="11" transform="rotate(-35 32 32)"/><path d="M32 15v34M15 32h34M32 23l2 7 7 2-7 2-2 7-2-7-7-2 7-2Z"/></g></svg>''')
print('Built main pages, tradition entrances, language resources, and favicon.')
# Religion has a separate register and is not presented as a polytheistic pantheon.
religion=(R/'religion.js').read_text().split('window.CHRISTIANITY_EN=')[0].replace('window.CHRISTIANITY_CN=','window.CHRISTIANITY_TW=')
(R/'religion-tw.js').write_text(traditional(religion))
# Keep authored batches separate; ship one validated, ordinary JS bundle.
chunks=[]
for part,var in [('east','EAST'),('west','WEST'),('americas','AMERICAS'),('south','SOUTH'),('extra-east','EXTRA_EAST'),('extra-west','EXTRA_WEST'),('extra-world','EXTRA_WORLD'),('more-a','MORE_A'),('more-b','MORE_B'),('more-c','MORE_C')]:
 p=R/f'figures-{part}.js'
 if p.exists():
  check=subprocess.run(['node','--check',str(p)],capture_output=True)
  if check.returncode==0:chunks.append(p.read_text())
  else:
   candidate=p.read_text().rstrip().rstrip(',')+'\n];'
   valid=subprocess.run(['node','--check'],input=candidate,text=True,capture_output=True).returncode==0
   chunks.append(candidate if valid else f'window.FIGURES_{var} = [];')
 else:chunks.append(f'window.FIGURES_{var} = [];')
figures_js='\n'.join(chunks)+'\nwindow.FIGURES_EAST.push(...window.FIGURES_EXTRA_EAST,...window.FIGURES_MORE_A);window.FIGURES_WEST.push(...window.FIGURES_EXTRA_WEST,...window.FIGURES_MORE_B);window.FIGURES_WORLD=[...window.FIGURES_AMERICAS,...window.FIGURES_SOUTH,...window.FIGURES_EXTRA_WORLD,...window.FIGURES_MORE_C];\n'
(R/'figures.js').write_text(figures_js)
tw=figures_js
for var in ['MORE_A','MORE_B','MORE_C','EXTRA_EAST','EXTRA_WEST','EXTRA_WORLD','EAST','WEST','AMERICAS','SOUTH','WORLD']:tw=tw.replace('window.FIGURES_'+var,'window.FIGURES_TW_'+var)
tw+='\nwindow.FIGURES_TW = [...window.FIGURES_TW_EAST,...window.FIGURES_TW_WEST,...window.FIGURES_TW_WORLD];\n'
(R/'figures-tw.js').write_text(traditional(tw))
runner="const fs=require('fs'),vm=require('vm'),w={};vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),{window:w});process.stdout.write(JSON.stringify([...(w.FIGURES_EAST||[]),...(w.FIGURES_WEST||[]),...(w.FIGURES_WORLD||[])]));"
figures=json.loads(subprocess.run(['node','-e',runner,str(R/'figures.js')],capture_output=True,text=True,check=True).stdout)
for f in figures:
 fallback='<article class="about-copy"><a href="../worlds/'+f['myth']+'.html">← '+html.escape(NAMES[f['myth']])+'</a><h1>'+html.escape(f['name'])+'</h1><p>'+html.escape(f['title'])+'</p>'
 for section in f['sections']:fallback+='<h2>'+html.escape(section['title'])+'</h2><p>'+html.escape(section['text'])+'</p>'
 fallback+='</article>'
 page(f"figures/{f['id']}.html",f['name']+' · '+NAMES[f['myth']],'figure',f'data-figure="{f["id"]}"',fallback)
print(f'Generated {len(figures)} full-text figure HTML files; total HTML files: {len(list(R.rglob("*.html")))}.')
(R/'reading-tw.js').write_text(traditional((R/'reading.js').read_text().replace('window.READING=','window.READING_TW=')))
page('christianity.html','圣经叙事与基督教传统','world','data-world="christianity"')
# Layered learning resources, compiled offline and isolated by language.
for filename,var in [('guides','GUIDES'),('curriculum','CURRICULUM')]:
 text=(R/f'{filename}.js').read_text()
 (R/f'{filename}-tw.js').write_text(traditional(text.replace('window.'+var,'window.'+var+'_TW')))
study=(R/'study-i18n.js').read_text().split('window.STUDY_UI_EN=')[0].replace('window.STUDY_UI_CN','window.STUDY_UI_TW')
(R/'study-i18n-tw.js').write_text(traditional(study))
chapters={'orientation':'全景导读','history':'历史与流传','figures':'人物与关系','cosmos':'世界与核心观念','stories':'故事与经典叙事','context':'文化与解释','sources':'原典与进阶阅读'}
for mid,name in NAMES.items():
 for key,label in chapters.items():page(f'learn/{mid}-{key}.html',name+' · '+label,'lesson',f'data-world="{mid}" data-chapter="{key}"')
# Only syntactically complete authored story batches are bundled.
parts=[]
for side in ['east','west','world']:
 p=R/f'story-addons-{side}.js';var='STORY_ADDONS_'+side.upper()
 if p.exists() and subprocess.run(['node','--check',str(p)],capture_output=True).returncode==0:parts.append(p.read_text())
 else:parts.append('window.'+var+'={};')
addon='\n'.join(parts)+'\n'+((R/'story-fixes.js').read_text() if any('korea:' in t or 'korea: ' in t for t in parts) else '')+'\nwindow.STORY_ADDONS={...window.STORY_ADDONS_EAST,...window.STORY_ADDONS_WEST,...window.STORY_ADDONS_WORLD};\n'
(R/'story-addons.js').write_text(addon)
(R/'story-addons-tw.js').write_text(traditional(addon.replace('window.STORY_ADDONS','window.STORY_ADDONS_TW')))
runner2="const fs=require('fs'),vm=require('vm'),w={};vm.runInNewContext(fs.readFileSync(process.argv[1],'utf8'),{window:w});process.stdout.write(JSON.stringify(w.STORY_ADDONS));"
addons=json.loads(subprocess.run(['node','-e',runner2,str(R/'story-addons.js')],capture_output=True,text=True,check=True).stdout)
for mid,stories in addons.items():
 for i,s in enumerate(stories,2):
  fallback='<article class="article-body"><h1>'+html.escape(s['title'])+'</h1><p>'+html.escape(s['summary'])+'</p>'+''.join('<p>'+html.escape(t)+'</p>' for t in s['paragraphs'])+'</article>'
  page(f'stories/{mid}-{i+1}.html',s['title'],'article',f'data-world="{mid}" data-story="{i}"',fallback)
(R/'figure-index.json').write_text(json.dumps(figures,ensure_ascii=False))
subprocess.run(['python3',str(R/'portraits.py')],check=True)
subprocess.run(['python3',str(R/'make_manifest.py')],check=True)
print(f'Total: {len(list(R.rglob("*.html")))} HTML files; {len(figures)} figures, {38+sum(len(v) for v in addons.values())} stories, 133 chapters.')
# Put actual Chinese article text into every document as a resilient fallback.
subprocess.run(['node',str(R/'snapshot.js')],check=True)
snapshot=json.loads((R/'site-data.json').read_text())
def para(t):return '<p>'+html.escape(t)+'</p>'
def title(t):return '<h2>'+html.escape(t)+'</h2>'
for m in snapshot['myths']:
 people=[f for f in figures if f['myth']==m['id']]
 def person_links():return '<ul>'+''.join('<li><a href="../figures/'+f['id']+'.html">'+html.escape(f['name'])+' · '+html.escape(f['title'])+'</a></li>' for f in people)+'</ul>'
 def story_links():return '<ul>'+''.join('<li><a href="../stories/'+m['id']+'-'+str(j+1)+'.html">'+html.escape(s['title'])+'</a> — '+html.escape(s['summary'])+'</li>' for j,s in enumerate(m['stories']))+'</ul>'
 source_html=''.join(title(e[0])+para(e[2]) for e in snapshot['reading'].get(m['id'],[]))
 intro='<article class="about-copy"><h1>'+html.escape(m['name'])+'</h1>'+para(m['description'])+title('人物档案')+person_links()+title('故事')+story_links()+title('世界图景')+''.join(title(c['name'])+para(c['desc']) for c in m['cosmos'])+title('文献与版本')+source_html+'</article>'
 page('worlds/'+m['id']+'.html',m['name'],'world',f'data-world="{m["id"]}"',intro)
 for j,s in enumerate(m['stories']):
  fallback='<article class="article-body"><h1>'+html.escape(s['title'])+'</h1>'+para(s['summary'])+''.join(para(t) for t in s['paragraphs'])+'</article>'
  page('stories/'+m['id']+'-'+str(j+1)+'.html',s['title'],'article',f'data-world="{m["id"]}" data-story="{j}"',fallback)
 for k,label in chapters.items():
  intro='<article class="about-copy"><h1>'+html.escape(m['name']+' · '+label)+'</h1>'
  if k=='orientation':intro+=para(m['description'])+para(m['note'])
  elif k=='history':intro+=''.join(title(t[0])+para(t[2]) for t in snapshot['curriculum'][m['id']]['timeline'])
  elif k=='figures':intro+=person_links()
  elif k=='cosmos':intro+=''.join(title(t['name'])+para(t['desc']) for t in m['cosmos'])
  elif k=='stories':intro+=story_links()
  elif k=='context':
   g=snapshot['guides'].get(m['id']);intro+=para(g['lead'] if g else m['note'])
   if g:intro+=''.join(title(s['title'])+para(s['text']) for s in g['sections'])
   intro+=''.join(title(f['name'])+para(f['sections'][3]['text']) for f in people[:6])
  elif k=='sources':intro+=source_html
  page(f'learn/{m["id"]}-{k}.html',m['name']+' · '+label,'lesson',f'data-world="{m["id"]}" data-chapter="{k}"',intro+'</article>')
# Stable top-level entry for old previews, with the same updated resources.
page('christianity.html','圣经叙事与基督教传统','world','data-world="christianity"')
(R/'assets/celestial-still.svg').write_text((R/'assets/celestial.svg').read_text().replace('animation:spin 200s linear infinite','animation:none').replace('animation:pulse 4s ease-in-out infinite alternate','animation:none'))
subprocess.run(['python3',str(R/'story-art.py')],check=True)
