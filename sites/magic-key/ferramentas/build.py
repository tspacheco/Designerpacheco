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

# Magazin: cartões gerados a partir de magazin/produse.json (preço nunca vem do fornecedor: «preț la cerere»)
import json, html, urllib.parse
def magazin(src):
    d = json.load(open('magazin/produse.json', encoding='utf-8'))
    esc = lambda x: html.escape(x, quote=True)
    tri = lambda v: v if isinstance(v, list) else [v, v, v]
    cats = [c for c in d['categorii'] if any(p['cat'] == c['id'] for p in d['produse'])]
    btn = '<button type="button" data-cat="toate" aria-pressed="true">{{Toate|All|Todos}}<small>%d</small></button>' % len(d['produse'])
    for c in cats:
        btn += '<button type="button" data-cat="%s" aria-pressed="false">{{%s|%s|%s}}<small>%d</small></button>' % (
            c['id'], c['ro'], c['en'], c['pt'], sum(p['cat'] == c['id'] for p in d['produse']))
    nume_cat = {c['id']: c for c in cats}
    li = []
    for i, p in enumerate(d['produse']):
        c = nume_cat[p['cat']]
        sp = tri(p.get('spec', ''))
        msg = 'Bună ziua! Aveți %s (%s)? Aș vrea să trec să o iau de la standul din Selgros Nicolina.' % (p['nume'], p['marca'])
        wa = 'https://wa.me/40747979810?text=' + urllib.parse.quote(msg)
        cauta = ' '.join([p['nume'], p['marca'], c['ro'], c['en']] + sp + p.get('cuvinte', [])).lower()
        cauta = ''.join(ch for ch in __import__('unicodedata').normalize('NFD', cauta) if __import__('unicodedata').category(ch) != 'Mn')
        img = ('<img src="%s" alt="%s" loading="lazy" decoding="async" width="400" height="400" onerror="this.remove()">' % (p['img'], esc(p['nume']))) if p.get('img') else ''
        li.append(
            '        <li class="prod rv%s" data-cat="%s" data-cauta="%s">'
            '<figure class="prod-foto"><svg viewBox="0 0 100 100" aria-hidden="true"><rect width="100" height="100" fill="#EFF2EC"/><text x="50" y="54" text-anchor="middle" font-family="monospace" font-size="9" fill="#9AA39A">%s</text></svg>%s'
            '<span class="prod-tag">{{%s|%s|%s}}</span></figure>'
            '<div class="prod-txt"><small>%s</small><h3>%s</h3>%s</div>'
            '<div class="prod-jos"><span class="pret">{{Preț la cerere|Price on request|Preço a pedido}}</span>'
            '<a class="btn btn-wa" href="%s" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>{{Rezervă<span class="lung"> pe WhatsApp</span>|Reserve<span class="lung"> on WhatsApp</span>|Reservar<span class="lung"> no WhatsApp</span>}}</a></div></li>' % (
                ' d%d' % (i % 3) if i % 3 else '', p['cat'], esc(cauta), esc(p['marca']), img,
                c['ro'], c['en'], c['pt'], esc(p['marca']), esc(p['nume']),
                ('<p>{{%s|%s|%s}}</p>' % tuple(esc(x) for x in sp)) if sp[0] else '', esc(wa)))
    return src.replace('__MAGCAT__', btn).replace('__MAGAZIN__', '\n'.join(li)).replace('__NPROD__', str(len(d['produse'])))
src = magazin(src)
src = re.sub(r'aria-label="' + T3 + '"', lambda m: 'aria-label="%s" data-aria="%s|%s|%s"' % (m[1], m[1], m[2], m[3]), src)
src = re.sub(T3, lambda m: '<span lang="ro">%s</span><span lang="en">%s</span><span lang="pt">%s</span>' % (m[1], m[2], m[3]), src, flags=re.S)
assert '{{' not in src, src[src.index('{{') - 80:src.index('{{') + 80]
out = src.replace('/*__FONTES__*/', open('_fontes/fontes.css', encoding='utf-8').read())
faltam = sorted({m for m in re.findall(r'media/([\w.-]+\.(?:webp|mp4|webm))', out) if not os.path.exists('media/' + m)})
open('index.html', 'w', encoding='utf-8').write(out.replace('__LSKEY__', SLUG + '.lang'))
pt = out.replace('<html lang="ro" data-lang="ro">', '<html lang="pt-PT" data-lang="pt" class="rev">', 1).replace('__LSKEY__', SLUG + '.lang.pt')
pt = pt.replace('<link rel="canonical" href="https://magickeyiasi.com/">', '<link rel="canonical" href="https://magickeyiasi.com/">\n<meta name="robots" content="noindex">', 1)  # pt.html é só para o Tomás: não indexar
assert 'data-lang="pt"' in pt
open('pt.html', 'w', encoding='utf-8').write(pt)
print('index.html %.0f KB' % (len(out.encode()) / 1024) + (' · faltam: ' + ', '.join(faltam) if faltam else ' · todas as fotos presentes'))
