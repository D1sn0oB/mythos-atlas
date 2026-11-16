"""Paced thumbnail fetch to avoid Wikimedia rate limiting."""
import json, glob, subprocess, time
from pathlib import Path
IP = '208.80.154.240'
TH = Path('/var/minis/workspace/mythos-art-research/thumbs3')
UA = 'MythosAtlas/1.0 (contact: mythos@example.org)'

def dl(url, dest):
    u = url.replace('https://thumb.wikimedia.org', 'https://upload.wikimedia.org').split('?')[0]
    for _ in range(2):
        p = subprocess.run(['curl', '-sS', '--resolve', 'upload.wikimedia.org:443:' + IP,
                            '--connect-timeout', '12', '--max-time', '90', '-A', UA, u],
                           capture_output=True)
        if p.returncode == 0 and len(p.stdout) > 1200 and p.stdout[:1] != b'<':
            dest.write_bytes(p.stdout)
            return True
        time.sleep(3)
    return False

todo = []
for path in sorted(glob.glob('/var/minis/workspace/mythos-art-research/v9/*.json')):
    d = json.load(open(path))
    for i, c in enumerate(d['candidates'][:3]):
        dest = TH / f"{d['id']}-{i}.img"
        if dest.exists() and dest.stat().st_size > 1200:
            with open(dest, 'rb') as fh:
                if fh.read(1) != b'<':
                    continue
        todo.append((c['thumb'], dest))

print('pending', len(todo), flush=True)
ok = 0
for url, dest in todo:
    if dl(url, dest):
        ok += 1
    time.sleep(0.8)
print('done', ok, 'of', len(todo), flush=True)
