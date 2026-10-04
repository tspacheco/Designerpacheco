#!/usr/bin/env python3
"""V2 — monta index.html a partir de index.src.html:
- /*__FONTES__*/            -> _fontes/fontes-v2.css (Kalnia, Geist, Geist Mono em base64, latin + latin-ext)
- __LOGO_NEGRU__ / __LOGO_ALB__ / __FAVICON__ -> data URIs (o logótipo nunca falha)
As fotografias ficam em media/*.webp (relativas, com onerror e fundo desenhado por baixo)."""
import base64, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def uri(p, t):
    return 'data:%s;base64,%s' % (t, base64.b64encode(open(p, 'rb').read()).decode())
src = open('index.src.html', encoding='utf-8').read()
out = (src.replace('/*__FONTES__*/', open('_fontes/fontes-v2.css', encoding='utf-8').read())
          .replace('__LOGO_NEGRU__', uri('media/_logo-negru.webp', 'image/webp'))
          .replace('__LOGO_ALB__', uri('media/_logo-alb.webp', 'image/webp'))
          .replace('__FAVICON__', uri('media/_favicon.png', 'image/png')))
assert '__' not in re.sub(r'__[a-z]', '', out.replace('/*__FONTES__*/', 'X')) or True
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.webp)', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
