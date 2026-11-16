from pathlib import Path
import math,random
r=random.Random(7)
s=['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 620"><defs><radialGradient id="planet"><stop stop-color="#69705a" stop-opacity=".10"/><stop offset=".7" stop-color="#71745b" stop-opacity=".08"/><stop offset=".95" stop-color="#b1a27d" stop-opacity=".12"/><stop offset="1" stop-color="#b1a27d" stop-opacity=".27"/></radialGradient><radialGradient id="halo"><stop stop-color="#b8aa79" stop-opacity=".17"/><stop offset="1" stop-color="#b8aa79" stop-opacity="0"/></radialGradient><clipPath id="sphere"><circle cx="310" cy="310" r="174"/></clipPath></defs><style>@keyframes spin{to{transform:rotate(360deg)}}@keyframes pulse{to{opacity:.3}}.slow{transform-origin:310px 310px;animation:spin 200s linear infinite}.blink{animation:pulse 4s ease-in-out infinite alternate}@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style><circle cx="310" cy="310" r="285" fill="url(#halo)"/><g stroke="#b6a37a" fill="none"><circle cx="310" cy="310" r="273" stroke-opacity=".12"/><circle cx="310" cy="310" r="265" stroke-opacity=".07"/><circle cx="310" cy="310" r="228" stroke-opacity=".18"/><circle cx="310" cy="310" r="224" stroke-opacity=".07"/><circle cx="310" cy="310" r="174" fill="url(#planet)" stroke-opacity=".35"/></g><g class="slow" stroke="#b6a37a">''']
for i in range(120):
 t=i*math.tau/120;outer=273;inner=265 if i%5==0 else 270
 s.append(f'<path d="M{310+inner*math.cos(t)} {310+inner*math.sin(t)}L{310+outer*math.cos(t)} {310+outer*math.sin(t)}" stroke-opacity="{.6 if i%10==0 else .22}" stroke-width=".6"/>')
s.append('</g><g fill="#b6a37a" font-size="9" font-family="Georgia,serif" text-anchor="middle">')
for i,txt in enumerate(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']):
 t=(i*30-90)*math.pi/180;x=310+247*math.cos(t);y=310+247*math.sin(t);s.append(f'<text x="{x}" y="{y+3}" opacity=".65">{txt}</text>')
s.append('</g><g clip-path="url(#sphere)" stroke="#b9b395" stroke-width=".6" fill="none" opacity=".14">')
for w in [45,90,135,170]:s.append(f'<ellipse cx="310" cy="310" rx="{w}" ry="174" transform="rotate(-24 310 310)"/>')
for dy in [-120,-70,0,70,120]:s.append(f'<ellipse cx="310" cy="{310+dy}" rx="174" ry="35" transform="rotate(-24 310 310)"/>')
s.append('</g><g fill="none" stroke="#c7b88f" stroke-width=".6"><ellipse cx="310" cy="310" rx="296" ry="101" transform="rotate(-32 310 310)" stroke-opacity=".3"/><ellipse cx="310" cy="310" rx="215" ry="66" transform="rotate(50 310 310)" stroke-opacity=".22"/><path d="M58 310 H562 M310 58 V562" stroke-opacity=".1" stroke-dasharray="2 7"/></g>')
pts=[(189,283),(242,236),(292,265),(333,208),(387,280),(433,323),(370,365),(320,347),(282,403),(230,365),(189,283)]
s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#c7b88f" stroke-opacity=".6" stroke-width=".8"/>')
s.append('<path d="M242 236 L230 365 L320 347 L292 265 L387 280 L370 365 M333 208 L320 347" fill="none" stroke="#c7b88f" stroke-opacity=".25" stroke-width=".7"/>')
for i,(x,y) in enumerate(pts[:-1]):
 s.append(f'<circle cx="{x}" cy="{y}" r="{2 if i%3 else 3}" fill="#dbcfab"/><circle cx="{x}" cy="{y}" r="7" fill="none" stroke="#c7b88f" stroke-opacity=".2"/>')
for i in range(60):
 x,y=r.randrange(80,540),r.randrange(80,540)
 if math.hypot(x-310,y-310)>160:s.append(f'<circle cx="{x}" cy="{y}" r="{r.uniform(.5,1.3):.1f}" fill="#dbcfab" opacity="{r.uniform(.15,.7):.2f}"/>')
s.append('''<g stroke="#dac79d" stroke-width=".7"><path d="M310 286 L314 306 L334 310 L314 314 L310 334 L306 314 L286 310 L306 306Z" fill="#c7b88f" fill-opacity=".15"/><circle cx="310" cy="310" r="13" fill="none" stroke-opacity=".4"/></g><g font-family="sans-serif" font-size="7" letter-spacing="3" fill="#b1a789"><text x="296" y="29">N</text><text x="592" y="313">E</text><text x="299" y="601">S</text><text x="12" y="313">W</text></g><circle cx="67" cy="453" r="4" fill="#dac79d"/><circle cx="67" cy="453" r="10" fill="none" stroke="#dac79d" stroke-opacity=".3"/><circle cx="506" cy="147" r="3" fill="#dac79d"/><path d="M476 111 L502 86 H550 M87 491 L114 520 H165" stroke="#b6a37a" stroke-opacity=".3" fill="none"/><g fill="#a29b83" font-family="sans-serif" font-size="7" letter-spacing="1.5"><text x="504" y="79">THE CELESTIAL</text><text x="116" y="535">A WORLD OF MYTHS</text></g></svg>''')
Path('/var/minis/workspace/mythos/assets/celestial.svg').write_text(''.join(s))
print('Celestial atlas generated.')
