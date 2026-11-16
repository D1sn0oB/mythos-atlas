from pathlib import Path
import math,random
s=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#0a0c17"/><stop offset="1" stop-color="#252030"/></linearGradient><radialGradient id="light"><stop stop-color="#e1c98e" stop-opacity=".4"/><stop offset="1" stop-color="#e1c98e" stop-opacity="0"/></radialGradient><linearGradient id="glass" x2="0" y2="1"><stop stop-color="#bbae91" stop-opacity=".15"/><stop offset=".5" stop-color="#a193b9" stop-opacity=".32"/><stop offset="1" stop-color="#303346" stop-opacity=".05"/></linearGradient></defs><rect width="1200" height="900" fill="url(#sky)"/><circle cx="600" cy="345" r="360" fill="url(#light)"/>''']
r=random.Random(11)
for i in range(100):s.append(f'<circle cx="{r.randrange(1200)}" cy="{r.randrange(700)}" r="{r.uniform(.5,1.5):.1f}" fill="#dbd4bf" opacity="{r.uniform(.1,.4):.2f}"/>')
for x in [180,1020]:s.append(f'<path d="M{x-85} 850 V330 Q{x-85} 235 {x} 170 Q{x+85} 235 {x+85} 330 V850Z" fill="#141622" stroke="#a799ad" stroke-opacity=".2"/>')
s.append('<path d="M390 805 V310 Q390 160 600 75 Q810 160 810 310 V805Z" fill="#121520" stroke="#baae91" stroke-opacity=".5" stroke-width="3"/><path d="M414 805 V313 Q414 182 600 104 Q786 182 786 313 V805Z" fill="url(#glass)" stroke="#baae91" stroke-opacity=".3"/>')
for x in [475,558,642,725]:s.append(f'<path d="M{x} 805 V365 Q{x} 310 600 155" fill="none" stroke="#c2b8a5" stroke-opacity=".26" stroke-width="2"/>')
s.append('<circle cx="600" cy="308" r="104" fill="#111824" stroke="#b2a4b6" stroke-opacity=".7"/><circle cx="600" cy="308" r="88" fill="none" stroke="#baae91" stroke-opacity=".4"/>')
for i in range(12):
 a=i*30;s.append(f'<g transform="rotate({a} 600 308)"><path d="M600 300 Q560 265 600 215 Q640 265 600 300Z" fill="{["#a299b8","#bfa46d","#7d96a5"][i%3]}" fill-opacity=".25" stroke="#c9bd99" stroke-opacity=".5"/></g>')
s.append('<circle cx="600" cy="308" r="28" fill="#caba90" fill-opacity=".4" stroke="#c9bd99" stroke-opacity=".6"/><path d="M600 439 V663 M538 504 H662" fill="none" stroke="#d4c69d" stroke-width="9" stroke-opacity=".8"/><path d="M600 439 V663 M538 504 H662" fill="none" stroke="#f0ddac" stroke-width="2"/><path d="M600 308 L340 900 H860Z" fill="#cfbd98" fill-opacity=".035"/>')
for y in [685,724,763]:s.append(f'<path d="M414 {y} H786" fill="none" stroke="#c9bd99" stroke-opacity=".2"/>')
for j in range(4):s.append(f'<path d="M{350-j*30} {805+j*17} H{850+j*30} V{822+j*17} H{350-j*30}Z" fill="#171d28" stroke="#bdad91" stroke-opacity=".2"/>')
s.append('<path d="M0 865 Q300 820 600 860 T1200 850 V900 H0Z" fill="#080e13" opacity=".8"/></svg>')
Path('/var/minis/workspace/mythos/assets/christianity.svg').write_text(''.join(s))
