#!/usr/bin/env python3
"""Monta index.html (RO, botão EN) e pt.html (a mesma página a abrir em PT, para o Tomás) a partir de index.src.html:
- /*__FONTES__*/          -> _fontes/fontes.css (fontes em base64, latin + latin-ext, com ă â î ș ț)
- {{ro|en|pt}}            -> <span lang="ro">…</span><span lang="en">…</span><span lang="pt">…</span>
- aria-label="{{ro|en|pt}}" -> aria-label="ro" data-aria="ro|en|pt" (o JS troca ao mudar de língua)
- __LSKEY__               -> chave do localStorage (diferente em cada ficheiro)
As fotografias ficam em media/*.webp (relativas, com onerror e desenho SVG por baixo)."""
import os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SLUG = os.path.basename(os.getcwd())
T3 = r'\{\{([^{}|]*?)\|([^{}|]*?)\|([^{}|]*?)\}\}'
src = open('index.src.html', encoding='utf-8').read()
src = re.sub(r'data-nml="' + T3 + '"', lambda m: 'data-nml="%s" data-nml3="%s|%s|%s"' % (m[1], m[1], m[2], m[3]), src)
src = re.sub(r'aria-label="' + T3 + '"', lambda m: 'aria-label="%s" data-aria="%s|%s|%s"' % (m[1], m[1], m[2], m[3]), src)
src = re.sub(T3, lambda m: '<span lang="ro">%s</span><span lang="en">%s</span><span lang="pt">%s</span>' % (m[1], m[2], m[3]), src, flags=re.S)
assert '{{' not in src, src[src.index('{{') - 80:src.index('{{') + 80]
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w./-]+\.(?:webp|mp4|webm))', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out.replace('__LSKEY__', SLUG + '.lang'))
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt" class="rev">', 1).replace('__LSKEY__', SLUG + '.lang.pt')
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
