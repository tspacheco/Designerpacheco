#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (a mesma página a abrir em PT, para o Tomás rever)
a partir de index.src.html:
- /*__FONTES__*/ -> _fontes/fontes.css (Sansita Swashed, Instrument Sans, Caveat em base64, latin + latin-ext)
- __FUNDA__      -> o laço de cetim que fecha cada secção (SVG inline)
Fotos e vídeos ficam em media/ (relativos, com onerror e fundo desenhado por baixo)."""
import os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FUNDA = ('<svg viewBox="0 0 96 56" focusable="false">'
  '<defs><linearGradient id="__ID__" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F6CCD6"/>'
  '<stop offset=".55" stop-color="#E9A6B6"/><stop offset="1" stop-color="#C97A8E"/></linearGradient></defs>'
  '<path class="capat" d="M44 30 L34 54 L39 51 L42 55 L48 32 Z M52 30 L62 54 L57 51 L54 55 L48 32 Z" fill="#C97A8E"/>'
  '<path class="bucla st" d="M46 28 C34 10 10 6 8 20 C6 34 30 38 46 30 Z" fill="url(#__ID__)" stroke="#C97A8E" stroke-width="1"/>'
  '<path class="bucla st" d="M44 28 C32 18 18 16 16 22" fill="none" stroke="#FBE3E9" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>'
  '<path class="bucla dr" d="M50 28 C62 10 86 6 88 20 C90 34 66 38 50 30 Z" fill="url(#__ID__)" stroke="#C97A8E" stroke-width="1"/>'
  '<path class="bucla dr" d="M52 28 C64 18 78 16 80 22" fill="none" stroke="#FBE3E9" stroke-width="1.6" stroke-linecap="round" opacity=".8"/>'
  '<rect class="nod" x="42" y="22" width="12" height="13" rx="4" fill="url(#__ID__)" stroke="#C97A8E" stroke-width="1"/>'
  '</svg>')
src = open('index.src.html', encoding='utf-8').read()
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
n = [0]
def laço(m):
    n[0] += 1
    return FUNDA.replace('__ID__', 'fg%d' % n[0])
out = re.sub(r'__FUNDA__', laço, out)
media = set(re.findall(r'media/([\w.-]+\.(?:webp|mp4|webm))', out)) | {m + '.webp' for m in re.findall(r"img:'([\w-]+)'", out)}
for v in re.findall(r'data-video="([\w-]+)"', out):
    media |= {v + '.mp4', v + '.webm'}
faltam = sorted(f for f in media if not os.path.exists('media/' + f))
open('index.html', 'w', encoding='utf-8').write(out)
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt">', 1)
pt = pt.replace('<title>Laurinda · Cofetărie artizanală, torturi personalizate și candy bar în Iași</title>',
                '<title>Laurinda · Pastelaria artesanal, bolos personalizados e candy bar em Iași</title>', 1)
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print('index.html %.0f KB · pt.html · %d laços' % (len(out.encode()) / 1024, n[0]) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todos os ficheiros de media presentes'))
