from pathlib import Path
import json,subprocess,urllib.parse,re,html,time
R=Path('/var/minis/workspace/mythos');OUT=Path('/var/minis/workspace/mythos-art-research/v8');OUT.mkdir(parents=True,exist_ok=True)
IP='185.15.59.224'
Q={
'japan-inari':['Inari shrine fox statue','Fushimi Inari fox'],
'korea-hwanung':['Hwanung','Samseonggung'],
'korea-ungnyeo':['Ungnyeo','bear woman Korea'],
'korea-jumong':['Jumong statue','Dongmyeong'],
'korea-haemosu':['Haemosu','Jumong Yuhwa painting'],
'korea-bari':['Princess Bari','Bari shaman Korea'],
'korea-yuhwa':['Yuhwa','Lady Yuhwa'],
'christianity-abraham':['Abraham sacrifice Isaac Rembrandt','Abraham painting'],
'egypt-seth':['Set Egyptian god relief','Seth statue'],
'mesopotamia-anu':['Anu god relief','Anu cuneiform god'],
'mesopotamia-marduk':['Marduk relief','Marduk dragon'],
'norse-hel':['Hel Norse underworld','Hel goddess manuscript'],
'roman-saturn':['Saturn god relief','Saturnus'],
'roman-vulcan':['Vulcan god statue','Hephaestus forging'],
'celtic-boann':['Boann','Boyne river goddess'],
'mesopotamia-ereshkigal':['Ereshkigal relief','Underworld goddess Mesopotamian'],
'maya-xquic':['Ixquic','Xquic Popol Vuh'],
'inca-mama-quilla':['Mama Quilla','Inca moon goddess'],
'yoruba-olodumare':['Olodumare','Yoruba Ifa divination'],
'yoruba-ogun':['Ogun sculpture','Ogun iron deity'],
'west-africa-aso':['Akan goldweight spider','Ananse goldweight'],
'west-africa-ntikuma':['Akan goldweight','Ananse spider'],
'west-africa-osebo':['Akan goldweight leopard','leopard goldweight'],
'polynesia-maui':['Maui Maori carving','Maui fishhook'],
'polynesia-hina':['Hina Hawaiian','Hawaiian goddess image'],
'polynesia-tangaroa':['Tangaroa carving','Maori meeting house'],
'polynesia-pele':['Pele Hawaiian','Halemaumau lava'],
'aboriginal-bunjil':['Bunjil','Bunjil rock art'],
'aboriginal-waa':['Waa crow','Aboriginal rock art bird'],
'aboriginal-daramulum':['Aboriginal engraving Sydney','rock engraving Australia'],
'maya-hun-hunahpu':['Popol Vuh','Hero Twins Maya'],
'inca-mama-cocha':['Mama Cocha','Inca sea'],
'yoruba-oya':['Oya orisha','Oya Yoruba'],
'west-africa-onini':['Akan goldweight snake','python goldweight'],
'west-africa-mmoboro':['Akan goldweight insect','hornet goldweight'],
'aboriginal-wagyl':['Noongar','Swan River Perth']}
def req(params):
 u='https://commons.wikimedia.org/w/api.php?'+urllib.parse.urlencode({'format':'json','formatversion':'2',**params})
 for n in range(3):
  p=subprocess.run(['curl','-sS','--resolve','commons.wikimedia.org:443:'+IP,'--connect-timeout','12','--max-time','40','-A','MythosAtlas/1.0 (contact: mythos@example.org)',u],capture_output=True,text=True)
  if 'too many requests' in p.stdout.lower():time.sleep(25);continue
  if p.returncode==0 and p.stdout.strip().startswith('{'):
   try:return json.loads(p.stdout)
   except Exception:pass
  time.sleep(5)
 return {}
def clean(v):return html.unescape(re.sub('<[^>]+>',' ',str(v or ''))).strip()
for fid,terms in Q.items():
 dest=OUT/(fid+'.json')
 if dest.exists():continue
 cands=[]
 for term in terms:
  res=req({'action':'query','generator':'search','gsrsearch':f'"{term}" filetype:bitmap','gsrnamespace':'6','gsrlimit':'10','prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':'640','iiextmetadatafilter':'LicenseShortName|UsageTerms|Artist|DateTimeOriginal|ImageDescription|ObjectName'})
  for page in res.get('query',{}).get('pages',[]):
   info=page['imageinfo'][0];meta={k:clean(v.get('value')) for k,v in info.get('extmetadata',{}).items()}
   lic=meta.get('LicenseShortName','')+' '+meta.get('UsageTerms','')
   if re.search(r'CC BY|share.?alike|fair use',lic,re.I) or not re.search(r'public domain|CC0|PD|No restrictions',lic,re.I):continue
   if (info.get('width') or 0)<420:continue
   if any(c['file']==page['title'] for c in cands):continue
   cands.append({'file':page['title'],'thumb':info.get('thumburl') or info['url'],'url':info['url'],'page':info['descriptionurl'],'w':info.get('width'),'h':info.get('height'),'license':(meta.get('LicenseShortName') or 'Public domain'),'meta':meta})
  if len(cands)>=4:break
  time.sleep(1.5)
 if cands:dest.write_text(json.dumps({'id':fid,'candidates':cands[:4]},ensure_ascii=False,indent=1))
 print(fid,len(cands),flush=True);time.sleep(2)
