#!/usr/bin/env python3
"""Tshirts do Sul · gera o site multipágina a partir de index.src.html.

Blocos marcados no src com <!-- @nome --> … <!-- @end -->. Cada página é um ficheiro HTML completo
(CSS/JS embutidos, só Google Fonts e o iframe do mapa por fora). preview/ é a mesma coisa para o Artifact.
"""
import re, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
src = (HERE / 'index.src.html').read_text('utf-8')
src = src.replace('{{LOGO}}', (HERE / 'marca/logos/logo-1.svg').read_text('utf-8'))
src = src.replace('{{BADGE}}', (HERE / 'marca/logos/logo-2.svg').read_text('utf-8'))

head, rest = src.split('<!-- @hero -->', 1); rest = '<!-- @hero -->' + rest
blocks = dict(re.findall(r'<!-- @([\w-]+) -->\n(.*?)\n<!-- @end -->', rest, flags=re.S))
tail = rest.split('<!-- @footer -->', 1)[1]  # footer + wa + drawer + modal + toast + script

def bi(x): return f'data-pt="{x[0]}" data-en="{x[1]}"'

def phero(theme, label, h1, lead, img=None, alt=''):
    im = f'<img src="media/{img}" alt="{alt}" width="1344" height="752" fetchpriority="high" onerror="this.remove()">' if img else ''
    return f'''<header class="phero phero-{theme}">{im}<div class="wrap">
  <span class="label" {bi(label)}>{label[0]}</span>
  <h1 {bi(h1)}>{h1[0]}</h1>
  <p class="lead" {bi(lead)}>{lead[0]}</p>
</div></header>'''

def page(name, title, desc, body):
    h = head.replace('<title>Tshirts do Sul · Estampado em Faro</title>', f'<title>{title}</title>')
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h)
    if name != 'index':
        h = h.replace(f'href="{name}.html"', f'href="{name}.html" aria-current="page"')
    html = h + body + '\n' + tail
    (HERE / f'{name}.html').write_text(html, 'utf-8')
    return html

# home: grelha limitada a 8 e ligação para a loja
home_loja = blocks['loja'].replace('<div class="grid rv d1" id="grid">', '<div class="grid rv d1" id="grid" data-limit="8">')
home_loja = home_loja.replace('data-pt="Peças que vais querer vestir" data-en="Pieces you\'ll want to be seen in">Peças que vais querer vestir', 'data-pt="Destaques da loja" data-en="Shop highlights">Destaques da loja')
home_loja = home_loja.replace('<button class="btn btn-ink" id="more" data-pt="Ver todas as peças" data-en="See all pieces">Ver todas as peças</button>', '<a class="btn btn-ink" href="loja.html" data-pt="Ver toda a loja" data-en="See the whole shop">Ver toda a loja</a>')

cta_medida = '''<section class="dark" id="cta-medida" style="background:var(--ria)">
  <div class="wrap band">
    <div class="txt">
      <span class="label" style="color:var(--areia)" data-pt="Impressão por medida" data-en="Custom printing">Impressão por medida</span>
      <h2 data-pt="Equipas, eventos, bares e marcas" data-en="Teams, events, bars and brands">Equipas, eventos, bares e marcas</h2>
      <p class="lead" data-pt="Diz-nos a peça, a quantidade e as cores. Respondemos com a técnica certa, prova digital e preço por peça." data-en="Tell us the garment, quantity and colours. We reply with the right method, a digital proof and a per-piece price.">Diz-nos a peça, a quantidade e as cores. Respondemos com a técnica certa, prova digital e preço por peça.</p>
      <div><a class="btn btn-sol" href="por-medida.html" data-pt="Pedir orçamento" data-en="Get a quote">Pedir orçamento</a></div>
    </div>
    <div class="ph"><img src="media/por-medida-staff.webp" alt="Pilha de t-shirts azul-marinho estampadas para a equipa de um restaurante" loading="lazy" width="896" height="1120" onerror="this.parentElement.style.background='#0E4851';this.remove()"></div>
  </div>
</section>'''
cta_tecnicas = cta_medida.replace('<section class="dark" id="cta-medida" style="background:var(--ria)">', '<section class="alt" id="cta-medida">').replace('<a class="btn btn-sol" href="por-medida.html" data-pt="Pedir orçamento" data-en="Get a quote">Pedir orçamento</a>', '<a class="btn btn-ink" href="estudio.html" data-pt="Conhecer as técnicas" data-en="See the methods">Conhecer as técnicas</a>').replace(' style="color:var(--areia)"', '')

PAGES = {}
PAGES['index'] = page('index', 'Tshirts do Sul · Estampado em Faro', 'T-shirts, sweats e bonés desenhados e estampados em Faro. Serigrafia, DTG e DTF em prensas próprias há mais de 30 anos. Loja online e impressão por medida.',
    '\n'.join([blocks['hero'], blocks['marquee'], blocks['trust'], home_loja, blocks['algarve'], cta_medida, blocks['estudio']]))
PAGES['loja'] = page('loja', 'Loja · Tshirts do Sul', 'T-shirts 15 €, sweats 35 €, bonés 25 € e coleção Halloween, impressos em Faro em algodão de 190 g/m².',
    '\n'.join([phero('sol', ('Loja', 'Shop'), ('Peças que vais querer vestir', "Pieces you'll want to be seen in"), ('T-shirts de 190 g/m², sweats, bonés trucker e Halloween. Impresso em Faro, expedido em 5 dias úteis.', '190 gsm tees, sweats, trucker caps and Halloween. Printed in Faro, dispatched in 5 working days.'), 'varal-16x9.webp', 'Varal de t-shirts e sweats acabadas de estampar, à luz do fim da tarde'), blocks['loja'].replace('<div class="head rv">', '<div class="head rv" style="margin-bottom:1.4rem">').replace('<span class="label" data-pt="Loja" data-en="Shop">Loja</span>', '').replace('<h2 data-pt="Peças que vais querer vestir" data-en="Pieces you\'ll want to be seen in">Peças que vais querer vestir</h2>', '<h2 style="font-size:var(--fs-h3)" data-pt="Todas as peças" data-en="All pieces">Todas as peças</h2>'), blocks['algarve'], blocks['envios']]))
PAGES['por-medida'] = page('por-medida', 'Impressão por medida · Tshirts do Sul', 'Serigrafia, DTG e DTF para equipas, eventos, bares, clubes e marcas. Pede orçamento em três perguntas.',
    '\n'.join([phero('ria', ('Impressão por medida', 'Custom printing'), ('Equipas, eventos, bares, clubes e marcas', 'Teams, events, bars, clubs and brands'), ('Traz o teu design (ou pede-nos um) e diz-nos quantas peças. Em três perguntas dizemos-te a técnica certa e preparamos a proposta.', "Bring your design (or ask us for one) and tell us how many pieces. Three questions in, we'll tell you the right method and prepare your quote."), 'tinta-laranja-16x9.webp', 'Rácula a puxar tinta laranja sobre a tela'), blocks['por-medida'].replace('<div class="head rv">', '<div class="head rv" hidden>'), cta_tecnicas]))
PAGES['estudio'] = page('estudio', 'O estúdio · Tshirts do Sul', 'Mais de 30 anos a estampar em Faro: serigrafia, DTG e DTF em prensas próprias.',
    '\n'.join([phero('ink', ('O estúdio', 'The studio'), ('Começámos pelo gosto de imprimir bem', 'We started with a love of printing well'), ('Três técnicas, prensas próprias e um estúdio na Avenida Calouste Gulbenkian, em Faro.', 'Three methods, our own presses and a studio on Avenida Calouste Gulbenkian, Faro.'), 'hero-16x9.webp', 'Mãos a puxar a rácula sobre uma tela de serigrafia'), blocks['estudio'].replace('<span class="label" data-pt="O estúdio" data-en="The studio">O estúdio</span>', '').replace('<h2 data-pt="Começámos pelo gosto de imprimir bem" data-en="We started with a love of printing well">Começámos pelo gosto de imprimir bem</h2>', ''), blocks['trust'], cta_medida]))
PAGES['envios'] = page('envios', 'Envios e devoluções · Tshirts do Sul', 'Expedição em 5 dias úteis para Portugal, Europa e Reino Unido. 14 dias para trocar ou devolver.',
    '\n'.join([phero('areia', ('Envios e devoluções', 'Shipping and returns'), ('Sem surpresas no fim', 'No surprises at checkout'), ('Cada encomenda sai do estúdio em 5 dias úteis. Tens 14 dias para trocar ou devolver.', 'Every order leaves the studio within 5 working days. You have 14 days to exchange or return.')), blocks['envios'].replace('<div class="head rv">', '<div class="head rv" hidden>'), blocks['trust']]))
PAGES['contacto'] = page('contacto', 'Contacto · Tshirts do Sul', 'Tshirts do Sul, Avenida Calouste Gulbenkian 12A, Faro. WhatsApp +351 961 579 403.',
    '\n'.join([phero('ria', ('Contacto', 'Contact'), ('Passa pelo estúdio', 'Drop by the studio'), ('Avenida Calouste Gulbenkian 12A, Faro. WhatsApp, telefone ou email.', 'Avenida Calouste Gulbenkian 12A, Faro. WhatsApp, phone or email.')), blocks['contacto'].replace('<h2 style="margin-bottom:1.4rem" data-pt="Passa pelo estúdio" data-en="Drop by the studio">Passa pelo estúdio</h2>', '').replace('<span class="label" data-pt="Contacto" data-en="Contact">Contacto</span>', '')]))

# preview para o Artifact: index sem esqueleto, subpáginas completas, media ao lado, mapa como ligação
prev = HERE / 'preview'
if prev.exists(): shutil.rmtree(prev)
prev.mkdir(); (prev / 'media').mkdir()
for f in (HERE / 'media').glob('*.webp'): shutil.copy(f, prev / 'media' / f.name)
MAP = re.compile(r'<iframe title="Mapa[^>]*></iframe>')
MAPLINK = '<a class="btn btn-ink" href="https://maps.google.com/?q=Avenida+Calouste+Gulbenkian+12A,+8000-072+Faro" target="_blank" rel="noopener" style="align-self:start">Abrir no Google Maps</a>'
for name, html in PAGES.items():
    h = MAP.sub(MAPLINK, html)
    if name == 'index':
        h = re.sub(r'<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', h).replace('</head>\n<body>', '').replace('</body>\n</html>', '')
    (prev / f'{name}.html').write_text(h, 'utf-8')
print('páginas:', ', '.join(f'{n} {len(h)//1024} KB' for n, h in PAGES.items()))
