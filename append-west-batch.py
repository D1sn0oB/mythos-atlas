import json,re,sys,pathlib,hashlib
base=pathlib.Path('/var/minis/workspace/mythos/story-addons-west.js')
prefix_len=28028
prefix_hash='7b4077b7c6898d092b688c0e33b678452d641931febbee5c4d7f5b7fe60a7a93'
assert hashlib.sha256(base.read_bytes()[:prefix_len]).hexdigest()==prefix_hash
items=json.loads(pathlib.Path(sys.argv[1]).read_text())
existing=base.read_text()
for x in items:
    assert x['id'] not in re.findall(r"id:\s*'([^']+)'",existing)
    assert len(x['paragraphs'])==len(x['en']['paragraphs'])==3
    han=lambda s:len(re.findall(r'[\u3400-\u9fff]',s))
    words=lambda s:len(s.split())
    counts=[han(x['summary'])]+list(map(han,x['paragraphs']))
    eng=[words(x['en']['summary'])]+list(map(words,x['en']['paragraphs']))
    print(x['id'],'Han:',counts,'English:',eng)
    assert 50<=counts[0]<=70,(x['id'],'summary',counts)
    assert all(90<=n<=130 for n in counts[1:]),(x['id'],'paragraphs',counts)
    assert 35<=eng[0]<=45,(x['id'],'en summary',eng)
    assert all(55<=n<=75 for n in eng[1:]),(x['id'],'en paragraphs',eng)
text=''
if len(sys.argv)>2:
    text+=sys.argv[2]
for x in items:
    text+=json.dumps(x,ensure_ascii=False,separators=(',',':'))+',\n'
with base.open('a') as f:f.write(text)
print('Appended',len(items),'entries; bytes',base.stat().st_size)
