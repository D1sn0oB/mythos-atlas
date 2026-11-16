from pathlib import Path
import json
R=Path(__file__).parent
c=json.loads((R/'art-credits.json').read_text())
(R/'art-manifest.js').write_text('window.ART='+json.dumps(c,ensure_ascii=False,separators=(',',':'))+';')
print('manifest',len(c))
