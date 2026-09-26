#!/usr/bin/env python3
"""Monta index.html (ficheiro único) a partir de index.src.html:
- /*__FONTES__*/  -> fontes em base64 de _fontes/fontes.css
- __MASCARA__     -> máscara SVG do "fade" (riscas cada vez mais finas, como uma passagem de máquina)
- src="media/x.jpg" -> data URI quando a foto existe (as que faltam ficam como caminho relativo, com onerror)"""
import base64, os, re, urllib.parse
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def mascara(y0=40.0, riscas=16, f0=.9, f1=.05):
    """y0 = % do topo que fica cheio; depois `riscas` faixas com cobertura de f0 a f1."""
    h = 100 - y0; b = h / riscas
    r = ['<rect width="100" height="%.2f"/>' % (y0 + .01)]
    for i in range(riscas):
        f = f0 - (f0 - f1) * i / (riscas - 1)
        r.append('<rect y="%.3f" width="100" height="%.3f"/>' % (y0 + i * b, b * f))
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">' + ''.join(r) + '</svg>'
    return 'data:image/svg+xml,' + urllib.parse.quote(svg)

src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
out = out.replace('__MASCARA__', mascara())
faltam = []
def emb(m):
    nome = m.group(1)
    if not os.path.exists('media/' + nome): faltam.append(nome); return m.group(0)
    return 'src="data:image/jpeg;base64,%s"' % base64.b64encode(open('media/' + nome, 'rb').read()).decode()
out = re.sub(r'src="media/([\w-]+\.jpg)"', emb, out)
assert '/*__FONTES__*/' not in out and '__MASCARA__' not in out
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · por enviar: ' + ', '.join(sorted(set(faltam))) if faltam else ''))
