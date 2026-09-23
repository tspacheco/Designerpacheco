#!/usr/bin/env python3
"""Monta as páginas do site do CROAE Moita a partir de src/ (cada página fica um ficheiro HTML auto-contido)."""
import re, json, shutil, pathlib
RAIZ = pathlib.Path(__file__).resolve().parent.parent
SRC = RAIZ/'src'; PAG = SRC/'pages'

head = (SRC/'head.html').read_text(encoding='utf-8')
nav = (SRC/'nav.html').read_text(encoding='utf-8')
foot = (SRC/'footer.html').read_text(encoding='utf-8')
css = (SRC/'base.css').read_text(encoding='utf-8')
js = (SRC/'base.js').read_text(encoding='utf-8')

# ---- fragmentos SVG reutilizáveis ----
BANDANA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none"><path d="M3 6h18l-9 13z" fill="currentColor" opacity=".9"/><circle cx="12" cy="6" r="2.6" fill="currentColor"/><path d="M8.5 4.5 12 6l3.5-1.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
SETA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5 5L20 7"/></svg>'
ICO_PASSEIO = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20c2-6 5-9 9-9 3 0 5 2 7 5"/><path d="M13 11c0-3 2-6 5-7"/><circle cx="17" cy="4" r="1.4" fill="currentColor"/><path d="M6 20l3-4"/></svg>'
ICO_CASA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>'
PATA_ICO = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><ellipse cx="12" cy="15.5" rx="4.2" ry="3.4"/><circle cx="6.5" cy="10.5" r="2"/><circle cx="10" cy="7.5" r="2"/><circle cx="14" cy="7.5" r="2"/><circle cx="17.5" cy="10.5" r="2"/></svg>'
# ranhuras fixas: o cliente grava media/galeria/01.jpg … 30.jpg e media/parceiros/01.png … 12.png; as que faltam desaparecem
GALERIA = ''.join(f'<figure class="foto"><img src="media/galeria/{i:02d}.jpg" alt="Fotografia {i} do CROAE Moita" loading="lazy"></figure>' for i in range(1,31))
LOGOS = ''.join(f'<div class="logo-slot"><img src="media/parceiros/{i:02d}.png" alt="Logótipo de parceiro {i}" loading="lazy" onerror="this.parentElement.remove()"></div>' for i in range(1,13))
ICO_SACO = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 8h12l1 12H5z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/><path d="M9.5 14.5c.5-1.5 4.5-1.5 5 0"/></svg>'
def svg_fundo(cor1, cor2, forma):
    return f'<svg class="fundo" viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{cor1}"/><stop offset="1" stop-color="{cor2}"/></linearGradient></defs><rect width="400" height="500" fill="url(#g)"/>{forma}</svg>'
PATA = '<g fill="#F2B705" opacity=".55"><ellipse cx="200" cy="290" rx="52" ry="44"/><circle cx="135" cy="225" r="26"/><circle cx="178" cy="185" r="26"/><circle cx="222" cy="185" r="26"/><circle cx="265" cy="225" r="26"/></g>'
SVG_CAO = svg_fundo('#24364F','#1B2A41', PATA)
SVG_STAND = svg_fundo('#2E4468','#1B2A41', '<g fill="#F2B705" opacity=".5"><rect x="80" y="150" width="240" height="180" rx="14"/><rect x="60" y="120" width="280" height="30" rx="8"/></g>')
SVG_EQUIPA = svg_fundo('#6B4E2E','#1B2A41', '<g fill="#F2B705" opacity=".45"><circle cx="140" cy="220" r="34"/><circle cx="200" cy="200" r="34"/><circle cx="260" cy="220" r="34"/><rect x="90" y="270" width="220" height="90" rx="30"/></g>')


FRAG = dict(BANDANA=BANDANA, SETA=SETA, CHECK=CHECK, ICO_PASSEIO=ICO_PASSEIO, ICO_CASA=ICO_CASA, ICO_SACO=ICO_SACO, SVG_CAO=SVG_CAO, SVG_STAND=SVG_STAND, SVG_EQUIPA=SVG_EQUIPA, PATA_ICO=PATA_ICO, GALERIA=GALERIA, LOGOS=LOGOS)

JSONLD = {
  "@context":"https://schema.org","@type":"AnimalShelter","name":"CROAE Moita — Centro de Recolha Oficial de Animais Errantes",
  "telephone":["+351212806816","+351962049674"],"email":"gab.vetmun@cm-moita.pt",
  "address":{"@type":"PostalAddress","streetAddress":"Estrada Municipal do Pinhal do Forno, em frente ao Cemitério do Pinhal do Forno","addressLocality":"Moita","addressRegion":"Setúbal","addressCountry":"PT"},
  "parentOrganization":{"@type":"GovernmentOrganization","name":"Câmara Municipal da Moita","url":"https://www.cm-moita.pt/"},
  "sameAs":["https://www.instagram.com/croaemoita/","https://www.facebook.com/croaemoita/"],
  "foundingDate":"2024-03-12"
}

def bloco(txt, tag):
    m = re.search(rf'<!--{tag}-->(.*?)<!--/{tag}-->', txt, re.S)
    return (m.group(1).strip() if m else ''), (re.sub(rf'<!--{tag}-->.*?<!--/{tag}-->', '', txt, flags=re.S) if m else txt)

for f in sorted(PAG.glob('*.html')):
    txt = f.read_text(encoding='utf-8')
    mm = re.search(r'<!--META\n(.*?)-->', txt, re.S); meta_txt = mm.group(1); txt = txt[mm.end():]
    meta = dict(l.split(':',1) for l in meta_txt.splitlines() if ':' in l); meta = {k.strip():v.strip() for k,v in meta.items()}
    pcss, txt = bloco(txt, 'CSS'); pjs, txt = bloco(txt, 'JS')
    body = txt.strip()
    for k,v in FRAG.items(): body = body.replace('{{'+k+'}}', v)
    h = head.replace('{{TITULO}}', meta['titulo']).replace('{{DESC}}', meta['desc']).replace('{{JSONLD}}', json.dumps(JSONLD, ensure_ascii=False)).replace('{{CSS}}', css + '\n/* --- página --- */\n' + pcss)
    n = nav.replace(f'data-p="{meta["pagina"]}"', f'data-p="{meta["pagina"]}" aria-current="page"')
    out = h + n + '\n' + body + '\n' + foot + '\n<script>\n' + js + ('\n' + pjs if pjs else '') + '\n</script>\n</body>\n</html>\n'
    (RAIZ/f.name).write_text(out, encoding='utf-8')
    print('ok', f.name, len(out)//1024, 'KB')
