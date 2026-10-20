#!/usr/bin/env python3
"""Gerador do site do Olá Kathmandu (Grândola). PT em / e EN em /en/.

  python3 build.py            -> site/     (links absolutos, pronto para Netlify)
  python3 build.py preview    -> preview/  (links relativos, abre de qualquer pasta)

Conceito "Lungta" (design/direcao-criativa.md). Factos: notas/00-recolha.md e data/negocio.json.
"""
import json, shutil, sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODE = 'preview' if len(sys.argv) > 1 and sys.argv[1] == 'preview' else 'site'
OUT = ROOT / ('preview' if MODE == 'preview' else 'site')
DOMAIN = 'https://olakathmandu.pt'
NEG = json.loads((HERE / 'data' / 'negocio.json').read_text(encoding='utf-8'))
MENU = json.loads((HERE / 'data' / 'menu.json').read_text(encoding='utf-8'))
SPRITE = (HERE / 'assets' / 'sprite.html').read_text(encoding='utf-8')
TEL = NEG['telefone']; TELF = NEG['telefone_fmt']; WA = TEL.lstrip('+'); EMAIL = NEG['email']; FB = NEG['facebook']
ADDR1, ADDR2 = 'Rua São João de Deus 21', '7570-308 Grândola'
MAPS_Q = 'Ol%C3%A1+Kathmandu+Rua+S%C3%A3o+Jo%C3%A3o+de+Deus+21+Gr%C3%A2ndola'
MAPS = f'https://www.google.com/maps/search/?api=1&query={MAPS_Q}'
# Plataformas: links para a pesquisa de cada app até o restaurante confirmar as lojas (notas/00-recolha.md)
APPS = [('glovo', 'Glovo', 'https://glovoapp.com/pt/pt/grandola/'), ('uber', 'Uber Eats', 'https://www.ubereats.com/pt/search?q=Ol%C3%A1%20Kathmandu'), ('bolt', 'Bolt Food', 'https://food.bolt.eu/pt-pt/')]

SLUGS = {'': '', 'carta': 'menu', 'entregas': 'delivery', 'reservas': 'reservations', 'historia': 'our-story', 'galeria': 'gallery',
         'contacto': 'contact', 'privacidade': 'privacy', 'termos': 'terms', 'obrigado': 'thanks'}
EN2PT = {v: k for k, v in SLUGS.items()}

T = {
'pt': dict(lang='pt-PT', other='en', other_label='EN', self_label='PT', site='Olá Kathmandu', tag='Nepalês · Grândola',
  nav=[('carta', 'Carta', 'momo · caril · tandoor'), ('entregas', 'Delivery', 'Glovo · Uber Eats · Bolt'), ('reservas', 'Reservas', 'WhatsApp · telefone'),
       ('historia', 'História', 'Kathmandu → Grândola'), ('galeria', 'Galeria', ''), ('contacto', 'Contacto', 'Rua São João de Deus')],
  skip='Saltar para o conteúdo', order='Pedir em casa', book='Reservar mesa', book_wa='Reservar no WhatsApp', menu='Carta', wa='WhatsApp',
  wa_text='Olá! Queria reservar uma mesa no Olá Kathmandu.', wa_order='Olá! Queria encomendar para take-away no Olá Kathmandu.', wa_group='Olá! Queria reservar para um grupo no Olá Kathmandu.',
  hours_short='Aberto todos os dias, 10:00–23:00', hours_line='Todos os dias 10:00–23:00', other_version='English version →', open_menu='Abrir o menu', close_menu='Fechar o menu',
  footer_welcome='Cozinha nepalesa e indiana em Grândola. Namaste: a mesa está posta.',
  f_visit='Visitar', f_talk='Falar connosco', f_pages='Páginas', f_how='Como chegar', privacy='Privacidade', terms='Termos e condições',
  livro='Livro de Reclamações', company='Denominação social · NIF · a confirmar', copy='Olá Kathmandu · Grândola', quick='Ações rápidas', lang_label='Língua / Language', main_nav='Principal',
  days=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'], home='Início', photo_tbc='foto real · a seguir', price_tbc='preço na carta', ai='imagem ilustrativa'),
'en': dict(lang='en', other='pt', other_label='PT', self_label='EN', site='Olá Kathmandu', tag='Nepali · Grândola',
  nav=[('menu', 'Menu', 'momo · curry · tandoor'), ('delivery', 'Delivery', 'Glovo · Uber Eats · Bolt'), ('reservations', 'Reservations', 'WhatsApp · phone'),
       ('our-story', 'Story', 'Kathmandu → Grândola'), ('gallery', 'Gallery', ''), ('contact', 'Contact', 'Rua São João de Deus')],
  skip='Skip to content', order='Order at home', book='Book a table', book_wa='Book on WhatsApp', menu='Menu', wa='WhatsApp',
  wa_text="Hello! I'd like to book a table at Olá Kathmandu.", wa_order="Hello! I'd like to order take-away from Olá Kathmandu.", wa_group="Hello! I'd like to book for a group at Olá Kathmandu.",
  hours_short='Open every day, 10:00–23:00', hours_line='Every day 10:00–23:00', other_version='Versão em português →', open_menu='Open menu', close_menu='Close menu',
  footer_welcome='Nepali and Indian cooking in Grândola, Alentejo. Namaste: the table is set.',
  f_visit='Visit', f_talk='Talk to us', f_pages='Pages', f_how='How to get here', privacy='Privacy', terms='Terms & conditions',
  livro='Complaints book', company='Company name · VAT no. · to be confirmed', copy='Olá Kathmandu · Grândola', quick='Quick actions', lang_label='Língua / Language', main_nav='Main',
  days=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], home='Home', photo_tbc='real photo · coming', price_tbc='price on the menu', ai='illustrative image'),
}

# ----------------------------------------------------------------------------- helpers
def wa_link(text): return f'https://wa.me/{WA}?text={quote(text)}'
def flags(): return '<span class="fl" aria-hidden="true"><i style="background:var(--f-azul)"></i><i style="background:var(--f-branco);outline:1px solid var(--line)"></i><i style="background:var(--f-vermelho)"></i><i style="background:var(--f-verde)"></i><i style="background:var(--f-amarelo)"></i></span>'

def lungta(words, n=18, cls=''):
    """Fio de bandeiras de oração: n bandeiras penduradas num fio que verga ao meio, cada uma com uma palavra."""
    W, H = 1200, 70
    out = [f'<svg class="lungta {cls}" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">',
           f'<path class="rope" d="M0 8 Q {W / 2} 34 {W} 8"/>']
    for i in range(n):
        x = (i + .5) * W / n
        t = x / W
        y = 8 + (34 - 8) * (1 - (2 * t - 1) ** 2)  # mesma parábola do fio
        w, h = W / n * .66, 40
        word = words[i % len(words)]
        out.append(f'<g transform="translate({x - w / 2:.1f} {y:.1f})"><g class="f c{i % 5 + 1}"><rect width="{w:.1f}" height="{h}" rx="1"/><text x="{w / 2:.1f}" y="{h / 2 + 3}" text-anchor="middle">{word}</text></g></g>')
    out.append('</svg>')
    return ''.join(out)

_pid = [0]
PALETTE = [('#C8521F', '#F2B51D'), ('#1C1915', '#C8521F'), ('#2F6FB7', '#1C1915'), ('#3C8A4E', '#F2B51D'), ('#F2B51D', '#D9382B'), ('#D9382B', '#1C1915')]
def media(ctx, ratio, file, alt, caption=True, w=800, h=1000, extra='', eager=False, ai=False):
    _pid[0] += 1
    a, b = PALETTE[_pid[0] % len(PALETTE)]
    rw, rh = {'4x5': (4, 5), '3x2': (3, 2), '1x1': (1, 1), '21x9': (21, 9), '16x9': (16, 9)}[ratio]
    ph = (f'<svg class="ph" viewBox="0 0 {rw} {rh}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="g{_pid[0]}" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="{rw}" height="{rh}" fill="url(#g{_pid[0]})"/></svg>')
    cap = f'<figcaption>{ctx.t["ai"] if ai else ctx.t["photo_tbc"]}</figcaption>' if caption else ''
    load = '' if eager else ' loading="lazy"'
    real = ' is-real' if ai else ''  # imagens geradas: não escondem a legenda "ilustrativa"
    return (f'<figure class="media media--{ratio} {extra}{"" if ai else ""}">{ph}'
            f'<img src="{ctx.u("media/foto/" + file)}" alt="{alt}" width="{w}" height="{h}"{load} decoding="async">{cap}</figure>')


class Ctx:
    def __init__(self, lang, slug):
        self.lang, self.slug, self.t = lang, slug, T[lang]
        self.pt_slug = slug if lang == 'pt' else EN2PT[slug]
        self.en_slug = SLUGS[self.pt_slug]
        self.rel = ([] if lang == 'pt' else ['en']) + ([slug] if slug else [])
        self.depth = len(self.rel)
    def page_path(self, lang, slug):
        parts = ([] if lang == 'pt' else ['en']) + ([slug] if slug else [])
        if MODE == 'site': return '/' + ''.join(p + '/' for p in parts)
        return '../' * self.depth + ''.join(p + '/' for p in parts) + 'index.html'
    def p(self, slug): return self.page_path(self.lang, slug)
    def twin(self):
        other = self.t['other']
        return self.page_path(other, self.en_slug if other == 'en' else self.pt_slug)
    def u(self, asset): return ('/' if MODE == 'site' else '../' * self.depth) + asset
    def abs(self, lang=None, slug=None):
        lang = lang or self.lang; slug = self.slug if slug is None else slug
        parts = ([] if lang == 'pt' else ['en']) + ([slug] if slug else [])
        return DOMAIN + '/' + ''.join(p + '/' for p in parts)


# ----------------------------------------------------------------------------- layout
def head(ctx, title, desc, jsonld=None):
    t = ctx.t
    ld = json.dumps(jsonld, ensure_ascii=False) if jsonld else ''
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#FBF6EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15120E" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{ctx.abs()}">
<link rel="alternate" hreflang="pt-PT" href="{ctx.abs('pt', ctx.pt_slug)}">
<link rel="alternate" hreflang="en" href="{ctx.abs('en', ctx.en_slug)}">
<link rel="alternate" hreflang="x-default" href="{ctx.abs('pt', ctx.pt_slug)}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta property="og:url" content="{ctx.abs()}"><meta property="og:image" content="{DOMAIN}/media/foto/og-inicio.jpg"><meta property="og:locale" content="{'pt_PT' if ctx.lang == 'pt' else 'en_GB'}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sahitya:wght@400;700&family=Mulish:ital,wght@0,400;0,700;0,800;1,400&display=swap" rel="stylesheet">
<link rel="icon" href="{ctx.u('favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{ctx.u('assets/site.css')}">
{('<script type="application/ld+json">' + ld + '</script>') if ld else ''}
</head>
<body data-wa="{WA}">
<a class="skip" href="#main">{t['skip']}</a>
<div class="grain" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg></div>
{SPRITE}
'''


def brand(ctx):
    return f'<a class="brand" href="{ctx.p("")}" aria-label="{ctx.t["site"]}, {ctx.t["home"]}"><svg class="mark"><use href="#i-horse"/></svg><span>Olá Kathmandu</span><small>{ctx.t["tag"]}</small></a>'


def lang_switch(ctx):
    t = ctx.t
    return (f'<nav class="lang" aria-label="{t["lang_label"]}">'
            f'<a href="{ctx.p(ctx.slug) if ctx.lang == "pt" else ctx.twin()}" hreflang="pt-PT" lang="pt-PT"{" aria-current=\"true\"" if ctx.lang == "pt" else ""}><span>PT</span></a>'
            f'<a href="{ctx.p(ctx.slug) if ctx.lang == "en" else ctx.twin()}" hreflang="en" lang="en"{" aria-current=\"true\"" if ctx.lang == "en" else ""}><span>EN</span></a></nav>')


def header(ctx, over_hero):
    t = ctx.t
    nav = ''.join(f'<a href="{ctx.p(s)}"{" aria-current=\"page\"" if s == ctx.slug else ""}>{lab}</a>' for s, lab, _ in t['nav'])
    sheet = ''.join(f'<a href="{ctx.p(s)}">{lab}{(" <small>" + sm + "</small>") if sm else ""}</a>' for s, lab, sm in t['nav'])
    order_href = ctx.p(t['nav'][1][0])
    return f'''<header class="header{' is-over-hero' if over_hero else ''}" id="header">
  <div class="container">
    {brand(ctx)}
    <nav class="nav" aria-label="{t['main_nav']}">{nav}</nav>
    <div class="header-actions">
      {lang_switch(ctx)}
      <a class="btn btn--wa" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span>{t['wa']}</span></a>
      <a class="btn btn--cta" href="{order_href}"><svg><use href="#i-scooter"/></svg>{t['order']}</a>
      <button class="icon-btn burger" type="button" aria-controls="sheet" aria-expanded="false" aria-label="{t['open_menu']}"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
    </div>
  </div>
</header>
<div class="sheet" id="sheet" aria-hidden="true">
  <button class="icon-btn close" type="button" aria-label="{t['close_menu']}"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
  <nav aria-label="{t['main_nav']} (mobile)">{sheet}</nav>
  <div class="sheet-foot">
    <p class="status js-status"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_short']}</span></p>
    <div class="row"><a class="btn btn--cta" href="{order_href}">{t['order']}</a><a class="btn btn--ghost" href="tel:{TEL}">{TELF}</a></div>
    <p><a class="link" href="{ctx.twin()}" hreflang="{t['other']}" lang="{t['other']}">{t['other_version']}</a></p>
  </div>
</div>
<main id="main">
'''


def footer(ctx):
    t = ctx.t
    pages = ''.join(f'<li><a href="{ctx.p(s)}">{lab}</a></li>' for s, lab, _ in t['nav'])
    priv, term = ('privacidade', 'termos') if ctx.lang == 'pt' else ('privacy', 'terms')
    words = ['namaste', 'momo', 'dal bhat', 'tandoor', 'chiya', 'Grândola'] if ctx.lang == 'pt' else ['namaste', 'momo', 'dal bhat', 'tandoor', 'chiya', 'Grândola']
    return f'''</main>
<footer class="footer">{lungta(words, 20)}
  <div class="container">
    <div class="footer-grid">
      <div>{brand(ctx)}<p class="welcome">{t['footer_welcome']}</p></div>
      <div><h4>{t['f_visit']}</h4><ul><li>{ADDR1}<br>{ADDR2}</li><li class="num">{t['hours_line']}</li><li><a class="link" href="{ctx.p(t['nav'][5][0])}">{t['f_how']}</a></li></ul></div>
      <div><h4>{t['f_talk']}</h4><ul><li><a href="tel:{TEL}" class="num">{TELF}</a></li><li><a href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{NEG['tripadvisor']['url']}" target="_blank" rel="noopener">Tripadvisor</a></li></ul></div>
      <div><h4>{t['f_pages']}</h4><ul>{pages}<li><a href="{ctx.p(priv)}">{t['privacy']}</a></li><li><a href="{ctx.p(term)}">{t['terms']}</a></li></ul></div>
    </div>
    <div class="footer-legal">
      <p><a href="https://www.livroreclamacoes.pt/inicio" target="_blank" rel="noopener">{t['livro']}</a> · <span class="tbc">{t['company']}</span></p>
      <div class="footer-bar"><span>© <span class="js-year num">2026</span> {t['copy']}</span>{lang_switch(ctx)}</div>
    </div>
  </div>
</footer>
<nav class="tabbar" aria-label="{t['quick']}">
  <a class="btn btn--wa" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span class="sr-only">WhatsApp</span></a>
  <a class="btn btn--cta" href="{ctx.p(t['nav'][1][0])}">{t['order']}</a>
  <a class="btn btn--ghost" href="{ctx.p(t['nav'][0][0])}">{t['menu']}</a>
</nav>
<script src="{ctx.u('assets/site.js')}" defer></script>
</body>
</html>
'''


def page_hero(ctx, label, h1, lead, dark=False, crumb=None, words=None):
    t = ctx.t
    return f'''<section class="page-hero{' page-hero--dark' if dark else ''}">{lungta(words or [label.lower()], 22)}
  <div class="container">
    <p class="crumbs"><a href="{ctx.p('')}">{t['home']}</a><span>/</span><span>{crumb or h1}</span></p>
    <p class="label" style="margin-top:var(--s-5)">{flags()}{label}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''


def restaurant_ld(ctx):
    return {"@context": "https://schema.org", "@type": "Restaurant", "name": "Olá Kathmandu", "url": ctx.abs('pt', ''),
            "image": DOMAIN + "/media/foto/og-inicio.jpg", "servesCuisine": ["Nepalese", "Indian"], "telephone": TEL, "email": EMAIL, "priceRange": "€",
            "address": {"@type": "PostalAddress", "streetAddress": ADDR1, "addressLocality": "Grândola", "postalCode": "7570-308", "addressRegion": "Setúbal", "addressCountry": "PT"},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "10:00", "closes": "23:00"}],
            "acceptsReservations": "True", "hasMenu": ctx.abs('pt', 'carta'), "sameAs": [FB, NEG['tripadvisor']['url']]}


# ----------------------------------------------------------------------------- INÍCIO
HOME = {
'pt': dict(title='Olá Kathmandu · Restaurante nepalês e indiano em Grândola',
  desc='Momo feitos à mão, dal bhat, caril de frango com 15 especiarias e pão do tandoor, na Rua São João de Deus, Grândola. Aberto todos os dias 10–23. Take-away por WhatsApp e delivery.',
  label='Restaurante nepalês · Grândola, Alentejo', h1=('Kathmandu,', 'na <em>Vila Morena</em>.'),
  sub='Momo fechados à mão, dal bhat como em casa, caril de frango cozinhado devagar com uma mistura de mais de 15 especiarias, pão a sair do tandoor. Uma cozinha nepalesa e indiana na Rua São João de Deus, em Grândola.',
  see_menu='Ver a carta', today='Hoje no Olá Kathmandu', today_k='Hoje', where_k='Onde', where='Rua São João de Deus 21', where_s='centro de Grândola', every='Todos os dias, 10:00–23:00', apps_k='Em casa',
  rating_s='no Tripadvisor', rating_n='3 opiniões',
  proof=[('5,0 / 5', '<span class="num">3</span> opiniões, todas 5 estrelas', 'Tripadvisor'), ('10–23', 'Aberto todos os dias, 7 dias', 'Horário'), ('45 €', 'Set Menu para 3–4 pessoas, bebida incluída', 'Para partilhar')],
  proof4=('Take-away', 'Pedido escrito no WhatsApp a partir da carta', 'Sem apps'),
  lm_label='À mesa', lm_h2='Começa com momo. Acaba com <em>chiya</em>.', lm_lead='Raviolis a vapor com achar de tomate, um thali com tudo no mesmo prato, caril e pão quente, e um chá nepalês com leite e especiarias a fechar. Doses generosas, como dizem as opiniões.',
  plates=[('nepal', 'momo.jpg', 'Momo de frango cozidos a vapor, em roda, com achar de tomate', '01 · Momo', 'Momo a vapor, fechados à mão.', 'O prato de rua de Kathmandu. De frango ou de legumes, com achar de tomate e sésamo.', None, True),
          ('nepal', 'dal-bhat-thali.jpg', 'Thali com arroz, dal, caril e acompanhamentos', '02 · Dal bhat', 'Dal bhat: o almoço nepalês.', 'Arroz, dal de lentilhas, caril, legumes, achar e iogurte. Tudo num prato, como em casa.', None, True),
          ('tandoori-caril', 'curry-frango.jpg', 'Caril de frango em karahi de cobre com coentros', '03 · Caril', 'Caril de frango com mais de 15 especiarias.', 'Cozinhado devagar até a carne desfazer. Com arroz incluído.', '9,50 €', True),
          ('tandoori-caril', 'frango-tandoori.jpg', 'Frango tandoori na tábua com molho de hortelã', '04 · Tandoor', 'Frango tandoori com um naan.', 'Marinado em iogurte e especiarias, assado no forno de barro. O naan sai ao mesmo tempo.', '10,00 €', True)],
  d_label='Delivery e take-away', d_h2='Chega a casa <em>quente</em>.', d_lead='Pede pela app que já tens no telemóvel, ou escreve-nos o pedido no WhatsApp e vem buscar: a carta inteira está aqui no site com os preços.',
  d_apps=[('Glovo', 'Pesquisa «Olá Kathmandu» na app'), ('Uber Eats', 'Pesquisa «Olá Kathmandu» na app'), ('Bolt Food', 'Pesquisa «Olá Kathmandu» na app')],
  d_tel=('Take-away por telefone', TELF), d_wa=('Take-away por WhatsApp', 'Escolhe na carta, o pedido escreve-se sozinho'),
  d_steps=[('Abre a carta', 'Toca no «+» ao lado de cada prato. O cesto aparece em baixo.'), ('Envia no WhatsApp', 'A mensagem já vai escrita com os pratos, as quantidades e o total.'), ('Vem buscar', 'Confirmamos a hora na mesma conversa. Pagas ao levantar.')],
  d_tbc='Plataformas a confirmar com o restaurante', d_cta='Encomendar na carta',
  m_label='Da carta', m_h2='Toda a carta no telemóvel, com <em>preços</em> e alergénios.', m_lead='Sem PDF. Carta completa, com os preços da carta impressa, alergénios marcados e filtro vegetariano.',
  m_open='Abrir a carta completa', m_photo_alt='Página da carta impressa do Olá Kathmandu', m_filters='Exemplo de filtros da carta',
  chips=['Vegetariano', 'Sem glúten', 'Sem lactose', 'Picante'],
  s_label='A nossa história', s_h2='De Kathmandu a Grândola, <em>a pé de especiarias</em>.',
  s_p1='Olá Kathmandu é uma cozinha nepalesa e indiana numa rua do centro de Grândola, a Rua São João de Deus. Na sala há bandeiras de oração, um Buda dourado e a bandeira do Nepal; na cozinha, um tandoor e uma mistura de especiarias feita em casa.',
  s_p2='O nome junta o «Olá» português ao nome da capital do Nepal, e é isso que a casa é: nepalesa na comida, alentejana na vizinhança. Quem entra pela primeira vez costuma sair a dizer que foi uma surpresa. <span class="tbc">história dos donos e ano de abertura · a confirmar</span>',
  s_alt='Sala do Olá Kathmandu com bandeiras de oração e Buda dourado', facts=[('5,0', 'no Tripadvisor'), ('15+', 'especiarias no caril'), ('7/7', 'dias por semana'), ('10–23', 'todos os dias')], s_more='Ler a história →',
  o_label='Do Nepal, à mesa', o_h2='O que vem de <em>lá</em>.', o_lead='Cozinha de montanha e de vale: arroz e lentilhas todos os dias, especiarias torradas em casa, pão de forno de barro.',
  ledger=[('i-steam', 'Momo', 'massa fina, recheio de frango ou legumes, vapor', 'Kathmandu'), ('i-fire', 'Tandoor', 'forno de barro a alta temperatura: naan e frango', 'Punjab · Nepal'), ('i-leaf', 'Timmur', 'pimenta nepalesa de Sichuan, no bhatmas sadeko e no aloo', 'Himalaias'),
          ('i-sun', 'Garam masala da casa', 'mais de 15 especiarias torradas e moídas', 'Cozinha'), ('i-bag', 'Chatpate e pani puri', 'petiscos de rua, picantes, doces e ácidos', 'Rua'), ('i-users', 'Dal bhat', 'o prato de todos os dias no Nepal', 'Casa')],
  r_label='Reservas', r_h2='Reservas em 30 segundos. Nós <em>confirmamos</em>.', r_lead='Envia no WhatsApp a data, a hora e o número de pessoas. Confirmamos na mesma conversa ou ligamos de volta.',
  f_title='Reserva por WhatsApp ou telemóvel', f_tel='Telemóvel', f_date='Data', f_time='Hora', f_people='Pessoas', f_name='Nome', f_name_ph='Nome e apelido', f_send='Enviar a reserva no WhatsApp',
  f_note='Diz-nos a data, a hora e quantas pessoas. Mais de 10 pessoas ou um grupo? <a class="link" href="{ev}">Pede o Set Menu</a>.',
  ways=[('Telefone', 'Todos os dias, das 10:00 às 23:00.'), ('Grupos e festas', 'Set Menu de 45 € para 3–4 pessoas, com bebida. Para grupos maiores, combinamos a travessa e a mesa.'), ('Take-away', 'Pede na carta e vem buscar; o pedido sai escrito no WhatsApp.')],
  v_label='O que dizem', v_h2='<em>5,0</em> no Tripadvisor. Três opiniões, três vezes cinco estrelas.', v_lead='Ainda são poucas, e são todas de 2026. O que repetem: primeira vez a comer nepalês, doses generosas, «uma surpresa agradável perdida em Grândola».',
  reviews=[('Primeira experiência com comida nepalesa, tudo o que escolhemos estava delicioso e muito bem servido (doses generosas).', 'mpneto2016 · agosto 2026 · Tripadvisor'),
           ('Onde menos se espera, um dos melhores restaurantes nepaleses de Portugal.', '«Uma surpresa agradável perdida em Grândola» · outubro 2026 · Tripadvisor'),
           ('Experimentei comida nepalesa pela primeira vez e este restaurante não desiludiu.', 'Me04 · agosto 2026 · Tripadvisor')],
  v_note='Citações retraduzidas da versão inglesa do Tripadvisor; o texto original em português confirma-se antes de publicar.',
  v_all='Ver todas as opiniões no Tripadvisor →',
  c_label='Como chegar', c_h2='No centro de Grândola, a dois passos da <em>Praça</em>.', c_addr='Morada', c_hours='Horário', c_tel='Telefone', c_mail='Email',
  c_hours_v='Todos os dias<br>10:00–23:00', amen=['Take-away', 'Opções vegetarianas', 'Cartão e MB Way', 'Pátio interior', 'Grupos'],
  amen_tbc='a confirmar', map_btn='Abrir no Google Maps', map_aria='Mapa esquemático: centro de Grândola', town='GRÂNDOLA'),
'en': dict(title='Olá Kathmandu · Nepali and Indian restaurant in Grândola, Alentejo',
  desc='Hand-folded momo, dal bhat, 15-spice chicken curry and tandoor bread on Rua São João de Deus, Grândola. Open every day 10–23. Take-away on WhatsApp and delivery.',
  label='Nepali restaurant · Grândola, Alentejo', h1=('Kathmandu,', 'in the <em>Vila Morena</em>.'),
  sub='Momo folded by hand, dal bhat like at home, chicken curry slow-cooked with a house blend of more than 15 spices, bread straight out of the tandoor. A Nepali and Indian kitchen on Rua São João de Deus, Grândola.',
  see_menu='See the menu', today='Today at Olá Kathmandu', today_k='Today', where_k='Where', where='Rua São João de Deus 21', where_s='centre of Grândola', every='Every day, 10:00–23:00', apps_k='At home',
  rating_s='on Tripadvisor', rating_n='3 reviews',
  proof=[('5.0 / 5', '<span class="num">3</span> reviews, all five stars', 'Tripadvisor'), ('10–23', 'Open every day, 7 days a week', 'Hours'), ('€45', 'Set Menu for 3–4 people, drink included', 'To share')],
  proof4=('Take-away', 'Order written on WhatsApp straight from the menu', 'No apps needed'),
  lm_label='At the table', lm_h2='It starts with momo. It ends with <em>chiya</em>.', lm_lead='Steamed dumplings with tomato achar, a thali with everything on one plate, curry and hot bread, and a Nepali spiced milk tea to finish. Generous portions, as the reviews say.',
  plates=[('nepal', 'momo.jpg', 'Steamed chicken momo arranged in a wheel with tomato achar', '01 · Momo', 'Steamed momo, folded by hand.', "Kathmandu's street food. Chicken or vegetable, with tomato and sesame achar.", None, True),
          ('nepal', 'dal-bhat-thali.jpg', 'Thali with rice, dal, curry and sides', '02 · Dal bhat', 'Dal bhat: the Nepali lunch.', 'Rice, lentil dal, curry, vegetables, achar and yoghurt. All on one plate, like at home.', None, True),
          ('tandoori-caril', 'curry-frango.jpg', 'Chicken curry in a copper karahi with coriander', '03 · Curry', 'Chicken curry with more than 15 spices.', 'Slow-cooked until the meat falls apart. Rice included.', '€9.50', True),
          ('tandoori-caril', 'frango-tandoori.jpg', 'Tandoori chicken on a board with mint sauce', '04 · Tandoor', 'Tandoori chicken with a naan.', 'Marinated in yoghurt and spices, roasted in the clay oven. The naan comes out at the same time.', '€10.00', True)],
  d_label='Delivery and take-away', d_h2='It arrives <em>hot</em>.', d_lead='Order on the app already on your phone, or write us the order on WhatsApp and pick it up: the whole menu is here on the site with prices.',
  d_apps=[('Glovo', 'Search "Olá Kathmandu" in the app'), ('Uber Eats', 'Search "Olá Kathmandu" in the app'), ('Bolt Food', 'Search "Olá Kathmandu" in the app')],
  d_tel=('Take-away by phone', TELF), d_wa=('Take-away on WhatsApp', 'Pick from the menu; the order writes itself'),
  d_steps=[('Open the menu', 'Tap "+" next to each dish. The basket appears at the bottom.'), ('Send on WhatsApp', 'The message is already written with dishes, quantities and total.'), ('Pick it up', 'We confirm the time in the same chat. Pay when you collect.')],
  d_tbc='Platforms to be confirmed with the restaurant', d_cta='Order from the menu',
  m_label='From the menu', m_h2='The whole menu on your phone, with <em>prices</em> and allergens.', m_lead='No PDF. The full menu with the printed-menu prices, allergens marked and a vegetarian filter.',
  m_open='Open the full menu', m_photo_alt='A page of the printed Olá Kathmandu menu', m_filters='Example of menu filters',
  chips=['Vegetarian', 'Gluten-free', 'Dairy-free', 'Spicy'],
  s_label='Our story', s_h2='From Kathmandu to Grândola, <em>on a trail of spices</em>.',
  s_p1='Olá Kathmandu is a Nepali and Indian kitchen on a street in the centre of Grândola, Rua São João de Deus. In the dining room there are prayer flags, a golden Buddha and the flag of Nepal; in the kitchen, a tandoor and a spice blend made in-house.',
  s_p2='The name joins the Portuguese "Olá" to the name of Nepal\'s capital, and that is what the place is: Nepali in the food, Alentejan in the neighbourhood. First-timers tend to leave saying it was a surprise. <span class="tbc">owners\' story and opening year · to be confirmed</span>',
  s_alt='Olá Kathmandu dining room with prayer flags and a golden Buddha', facts=[('5.0', 'on Tripadvisor'), ('15+', 'spices in the curry'), ('7/7', 'days a week'), ('10–23', 'every day')], s_more='Read the story →',
  o_label='From Nepal, to the table', o_h2='What comes from <em>there</em>.', o_lead='Mountain and valley cooking: rice and lentils every day, spices toasted in-house, bread from a clay oven.',
  ledger=[('i-steam', 'Momo', 'thin dough, chicken or vegetable filling, steam', 'Kathmandu'), ('i-fire', 'Tandoor', 'high-heat clay oven: naan and chicken', 'Punjab · Nepal'), ('i-leaf', 'Timmur', 'Nepali Sichuan pepper, in the bhatmas sadeko and the aloo', 'Himalayas'),
          ('i-sun', 'House garam masala', 'more than 15 spices, toasted and ground', 'Kitchen'), ('i-bag', 'Chatpate and pani puri', 'street snacks: hot, sweet and sour', 'Street'), ('i-users', 'Dal bhat', "Nepal's everyday plate", 'Home')],
  r_label='Reservations', r_h2='Book in 30 seconds. We <em>confirm</em>.', r_lead='Send the date, time and number of guests on WhatsApp. We confirm in the same chat or call you back.',
  f_title='Book on WhatsApp or by phone', f_tel='Phone', f_date='Date', f_time='Time', f_people='Guests', f_name='Name', f_name_ph='First and last name', f_send='Send the booking on WhatsApp',
  f_note='Tell us the date, time and number of guests. More than 10 people, or a group? <a class="link" href="{ev}">Ask for the Set Menu</a>.',
  ways=[('Phone', 'Every day, 10:00 to 23:00.'), ('Groups and parties', '€45 Set Menu for 3–4 people, drink included. For bigger groups we arrange the platter and the table.'), ('Take-away', 'Order from the menu and collect; the order goes out written on WhatsApp.')],
  v_label='What people say', v_h2='<em>5.0</em> on Tripadvisor. Three reviews, three times five stars.', v_lead='Still few, and all from 2026. What they repeat: first time eating Nepali, generous portions, "a pleasant surprise lost in Grândola".',
  reviews=[('First experience with Nepali food, everything we chose was delicious and very well served (generous portions).', 'mpneto2016 · August 2026 · Tripadvisor'),
           ('Where you least expect it, one of the best Nepalese restaurants in Portugal.', '"A pleasant surprise lost in Grândola" · October 2026 · Tripadvisor'),
           ('I tried Nepalese food for the first time and this restaurant did not disappoint.', 'Me04 · August 2026 · Tripadvisor')],
  v_note="Quotes as translated by Tripadvisor from the Portuguese originals; the originals are checked before publishing.",
  v_all='See all reviews on Tripadvisor →',
  c_label='How to get here', c_h2='In the centre of Grândola, two steps from the <em>main square</em>.', c_addr='Address', c_hours='Hours', c_tel='Phone', c_mail='Email',
  c_hours_v='Every day<br>10:00–23:00', amen=['Take-away', 'Vegetarian options', 'Card and MB Way', 'Inner patio', 'Groups'],
  amen_tbc='to be confirmed', map_btn='Open in Google Maps', map_aria='Schematic map: centre of Grândola', town='GRÂNDOLA'),
}


def apps_block(ctx, h, dark=True):
    t = ctx.t
    out = '<div class="apps">'
    for (k, name, url), (_, d) in zip(APPS, h['d_apps']):
        letter = {'glovo': 'G', 'uber': 'U', 'bolt': 'B'}[k]
        out += f'<a class="app" href="{url}" target="_blank" rel="noopener"><span class="logo {k}" aria-hidden="true">{letter}</span><span><b>{name}</b><span class="d">{d}</span></span><span class="go"><svg><use href="#i-arrow"/></svg></span></a>'
    out += f'<p style="font-size:.82rem;opacity:.7"><span class="tbc">{h["d_tbc"]}</span></p></div>'
    return out


def home(ctx):
    t, h = ctx.t, HOME[ctx.lang]
    ev = ctx.p(t['nav'][2][0]); menu = ctx.p(t['nav'][0][0]); story = ctx.p(t['nav'][3][0]); deliv = ctx.p(t['nav'][1][0])
    words = ['momo', 'dal bhat', 'caril', 'tandoor', 'chiya', 'namaste'] if ctx.lang == 'pt' else ['momo', 'dal bhat', 'curry', 'tandoor', 'chiya', 'namaste']
    rating = '5,0' if ctx.lang == 'pt' else '5.0'
    out = head(ctx, h['title'], h['desc'], restaurant_ld(ctx)) + header(ctx, True)
    out += f'''<section class="hero" id="start">
  <div class="hero-media" aria-hidden="true">
    <img class="hero-poster hero-poster--h" src="{ctx.u('media/foto/hero-poster-16x9.jpg')}" alt="" width="1920" height="1080" fetchpriority="high">
    <img class="hero-poster hero-poster--v" src="{ctx.u('media/foto/hero-poster-9x16.jpg')}" alt="" width="1080" height="1920">
    <video id="heroVideo" muted loop playsinline preload="none"
      data-src-landscape="{ctx.u('media/video/hero-16x9.mp4')}" data-webm-landscape="{ctx.u('media/video/hero-16x9.webm')}" data-poster-landscape="{ctx.u('media/foto/hero-poster-16x9.jpg')}"
      data-src-portrait="{ctx.u('media/video/hero-9x16.mp4')}" data-webm-portrait="{ctx.u('media/video/hero-9x16.webm')}" data-poster-portrait="{ctx.u('media/foto/hero-poster-9x16.jpg')}"></video>
  </div>
  <div class="hero-shade" aria-hidden="true"></div>
  {lungta(words, 24)}
  <div class="container"><div class="hero-grid">
    <div>
      <p class="label">{flags()}{h['label']}</p>
      <h1><span class="line"><span>{h['h1'][0]}</span></span><span class="line"><span>{h['h1'][1]}</span></span></h1>
      <p class="hero-sub">{h['sub']}</p>
      <div class="hero-ctas"><a class="btn btn--cta" href="{deliv}"><svg><use href="#i-scooter"/></svg>{t['order']}<svg class="arrow"><use href="#i-arrow"/></svg></a><a class="btn btn--ghost" href="{menu}">{h['see_menu']}</a></div>
    </div>
    <aside class="today" aria-label="{h['today']}">
      <div class="rating"><b class="num">{rating}</b><div><span class="stars" aria-hidden="true">★★★★★</span><small>{h['rating_n']} {h['rating_s']}</small></div></div>
      <dl>
        <dt><svg><use href="#i-clock"/></svg>{h['today_k']}</dt><dd><span class="status js-status"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_line']}</span></span><small>{h['every']}</small></dd>
        <dt><svg><use href="#i-pin"/></svg>{h['where_k']}</dt><dd>{h['where']}<small>{h['where_s']}</small></dd>
        <dt><svg><use href="#i-scooter"/></svg>{h['apps_k']}</dt><dd><div class="apps">{''.join(f'<a class="chip" href="{u}" target="_blank" rel="noopener" style="color:#FBF6EC;background:transparent;border-color:rgba(251,246,236,.35)">{n}</a>' for _, n, u in APPS)}</div></dd>
      </dl>
    </aside>
  </div></div>
</section>
<section class="proof" aria-label="{h['v_label']}"><div class="container">'''
    for i, (b, s, src) in enumerate(h['proof']):
        out += f'<div class="proof-item reveal"{f" data-delay=\"{i}\"" if i else ""}>{"<span class=\"stars\" aria-hidden=\"true\">★★★★★</span>" if i == 0 else ""}<b class="num">{b}</b><span>{s}</span><span class="src">{src}</span></div>'
    b, s, src = h['proof4']
    out += f'<div class="proof-item reveal" data-delay="3"><b>{b}</b><span>{s}</span><span class="src">{src}</span></div></div></section>\n'
    # à mesa
    out += f'<section class="section" id="a-mesa"><div class="container"><div class="section-head reveal"><p class="label">{flags()}{h["lm_label"]}</p><h2>{h["lm_h2"]}</h2><p class="lead">{h["lm_lead"]}</p></div><div class="plates">'
    for i, (anchor, file, alt, n, h3, p, price, real) in enumerate(h['plates']):
        pr = f'<span class="price num">{price}</span>' if price else f'<span class="tbc">{t["price_tbc"]}</span>'
        out += f'<a class="plate reveal"{f" data-delay=\"{i}\"" if i else ""} href="{menu}#{anchor}">{media(ctx, "4x5", file, alt)}<div><span class="n">{n}</span><h3>{h3}</h3><p>{p}</p>{pr}</div></a>'
    out += '</div></div></section>\n'
    # delivery
    steps = ''.join(f'<li><div><b>{a}</b><p>{b}</p></div></li>' for a, b in h['d_steps'])
    out += f'''<section class="section section--ink delivery" id="delivery"><div class="container">
  <div class="reveal"><p class="label" style="color:var(--gold)">{flags()}{h['d_label']}</p><h2 style="margin-top:var(--s-4);font-size:var(--fs-h2)">{h['d_h2']}</h2><p class="lead" style="margin-top:var(--s-4)">{h['d_lead']}</p>
    <ol class="steps" style="margin-top:var(--s-6)">{steps}</ol>
    <div class="hero-ctas"><a class="btn btn--gold" href="{menu}">{h['d_cta']}<svg class="arrow"><use href="#i-arrow"/></svg></a></div></div>
  <div class="reveal" data-delay="1">{apps_block(ctx, h)}</div>
</div></section>
'''
    # carta resumo
    sec = MENU['sections']
    def col(section, n=5):
        s = next(x for x in sec if x['id'] == section)
        items = ''
        for d in s['dishes'][:n]:
            pr = f'<span class="price num">{d["price"]}</span>' if d.get('price') else f'<span class="tbc">{t["price_tbc"]}</span>'
            items += f'<li><span><span class="name">{d["name"][ctx.lang]}</span><span class="desc">{d["desc"][ctx.lang]}</span></span>{pr}</li>'
        return f'<h3>{s["title"][ctx.lang]}</h3><ul class="menu-list" role="list">{items}</ul>'
    chips = h['chips']
    out += f'''<section class="section" id="carta"><div class="container">
  <div class="section-head reveal"><p class="label">{flags()}{h['m_label']}</p><h2>{h['m_h2']}</h2><p class="lead">{h['m_lead']}</p></div>
  <div class="menu-grid">
    <div class="menu-col reveal">{col('tandoori-caril', 6)}</div>
    <div class="menu-col reveal" data-delay="1">{col('aperitivos', 6)}<p style="margin-top:var(--s-5)"><a class="btn btn--ghost" href="{menu}">{h['m_open']}<svg class="arrow"><use href="#i-arrow"/></svg></a></p></div>
    <div class="menu-photo reveal" data-delay="2">{media(ctx, '4x5', 'carta-indian-fried-rice.jpg', h['m_photo_alt'], w=643, h=893)}
      <div class="menu-filters" aria-label="{h['m_filters']}"><span class="chip"><svg width="16" height="16" style="color:var(--f-verde)"><use href="#i-leaf"/></svg>{chips[0]}</span><span class="chip"><i>G</i>{chips[1]}</span><span class="chip"><i>L</i>{chips[2]}</span><span class="chip"><svg width="16" height="16" style="color:var(--f-vermelho)"><use href="#i-fire"/></svg>{chips[3]}</span></div>
    </div>
  </div>
</div></section>
'''
    facts = ''.join(f'<div><b class="num">{a}</b><span>{b}</span></div>' for a, b in h['facts'])
    out += f'''<section class="section section--alt" id="historia"><div class="container"><div class="story">
  {media(ctx, '4x5', 'sala-bandeiras.jpg', h['s_alt'], extra='reveal', w=1200, h=1500)}
  <div class="story-text reveal" data-delay="1"><p class="label">{flags()}{h['s_label']}</p><h2>{h['s_h2']}</h2><p>{h['s_p1']}</p><p>{h['s_p2']}</p>
    <div class="story-facts">{facts}</div><p><a class="link" href="{story}">{h['s_more']}</a></p></div>
</div></div></section>
'''
    ledger = ''.join(f'<li><span class="glyph"><svg><use href="#{ic}"/></svg></span><span class="what">{w}<small>{sm}</small></span><span class="where">{wh}</span></li>' for ic, w, sm, wh in h['ledger'])
    out += f'''<section class="section" id="do-nepal"><div class="container"><div class="origin">
  <div class="section-head reveal" style="margin-bottom:0"><p class="label">{flags()}{h['o_label']}</p><h2>{h['o_h2']}</h2><p class="lead">{h['o_lead']}</p></div>
  <ul class="ledger reveal" data-delay="1" role="list">{ledger}</ul>
</div></div></section>
'''
    out += booking_block(ctx, h, ev)
    revs = ''.join(f'<article class="review reveal"{f" data-delay=\"{i}\"" if i else ""}><span class="stars" aria-hidden="true">★★★★★</span><q>{q}</q><span class="who">{w}</span></article>' for i, (q, w) in enumerate(h['reviews']))
    out += f'''<section class="section section--alt" id="opinioes"><div class="container">
  <div class="section-head reveal"><p class="label">{flags()}{h['v_label']}</p><h2>{h['v_h2']}</h2><p class="lead">{h['v_lead']}</p></div>
  <div class="reviews">{revs}</div>
  <p style="margin-top:var(--s-4);font-size:.82rem;color:var(--ink-3)">{h['v_note']}</p>
  <p style="margin-top:var(--s-4)"><a class="link" href="{NEG['tripadvisor']['url']}" target="_blank" rel="noopener">{h['v_all']}</a></p>
</div></section>
'''
    out += contact_block(ctx, h)
    return out + footer(ctx)


def booking_block(ctx, h, ev, section_id='reservas'):
    t = ctx.t
    rows = [f'<a class="btn btn--ghost" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{TELF}</a>',
            f'<a class="btn btn--ghost" href="{wa_link(t["wa_group"])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a>',
            f'<a class="btn btn--ghost" href="{ctx.p(t["nav"][0][0])}">{t["menu"]}</a>']
    ways = ''.join(f'<div class="way"><span class="n num">0{i + 1}</span><div><b>{b}</b><p>{p}</p><div class="row">{row}</div></div></div>' for i, ((b, p), row) in enumerate(zip(h['ways'], rows)))
    return f'''<section class="section" id="{section_id}"><div class="container">
  <div class="section-head reveal"><p class="label">{flags()}{h['r_label']}</p><h2>{h['r_h2']}</h2><p class="lead">{h['r_lead']}</p></div>
  <div class="book">
    <div class="book-form reveal">
      <h3>{h['f_title']}</h3>
      <div class="opts">
        <a class="app" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><span class="logo wa" aria-hidden="true"><svg><use href="#i-wa"/></svg></span><span><b>WhatsApp</b><span class="d num">{TELF}</span></span><span class="go" aria-hidden="true"><svg><use href="#i-arrow"/></svg></span></a>
        <a class="app" href="tel:{TEL}"><span class="logo tel" aria-hidden="true"><svg><use href="#i-phone"/></svg></span><span><b>{h['f_tel']}</b><span class="d num">{TELF}</span></span><span class="go" aria-hidden="true"><svg><use href="#i-arrow"/></svg></span></a>
      </div>
      <p class="note">{h['f_note'].replace('{ev}', ev + '#grupos')}</p>
    </div>
    <div class="ways reveal" data-delay="1">{ways}</div>
  </div>
</div></section>
'''


def contact_block(ctx, h):
    amen = ''.join(f'<span class="chip">{a}</span>' for a in h['amen']) + f' <span class="tbc">{h["amen_tbc"]}</span>'
    return f'''<section class="section" id="contacto"><div class="container"><div class="info">
  <div class="reveal"><p class="label">{flags()}{h['c_label']}</p><h2 style="margin-top:var(--s-4);font-size:var(--fs-h2)">{h['c_h2']}</h2>
    <dl style="margin-top:var(--s-6)"><dt>{h['c_addr']}</dt><dd>{ADDR1}, {ADDR2}</dd><dt>{h['c_hours']}</dt><dd class="num">{h['c_hours_v']}</dd>
      <dt>{h['c_tel']}</dt><dd><a class="link num" href="tel:{TEL}">{TELF}</a></dd><dt>{h['c_mail']}</dt><dd><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></dd></dl>
    <div class="amen">{amen}</div></div>
  <div class="map reveal" data-delay="1" aria-label="{h['map_aria']}">
    <svg viewBox="0 0 600 400" aria-hidden="true"><defs><pattern id="mg" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0v40" fill="none" stroke="currentColor" stroke-opacity=".12"/></pattern></defs><rect width="600" height="400" fill="url(#mg)" style="color:var(--accent)"/>
      <path d="M40 60 C 150 90, 260 120, 300 190 S 420 330, 560 370" fill="none" stroke="var(--accent)" stroke-width="6" stroke-opacity=".35" stroke-linecap="round"/><path d="M0 230 C 120 210, 230 200, 300 190 S 470 150, 600 100" fill="none" stroke="var(--accent)" stroke-width="4" stroke-opacity=".25" stroke-linecap="round"/>
      <rect x="380" y="60" width="110" height="70" rx="8" fill="var(--gold)" fill-opacity=".25"/><text x="435" y="100" text-anchor="middle" font-family="Mulish, sans-serif" font-size="11" letter-spacing="1.5" fill="var(--ink-2)">PRAÇA</text>
      <text x="90" y="330" font-family="Sahitya, serif" font-weight="700" font-size="22" fill="var(--ink-2)">{h['town']}</text><text x="300" y="214" font-family="Mulish, sans-serif" font-size="10" letter-spacing="1.5" fill="var(--ink-3)">R. S. JOÃO DE DEUS</text></svg>
    <span class="pin"><svg><use href="#i-pin-fill"/></svg></span>
    <a class="btn btn--cta maplink" href="{MAPS}" target="_blank" rel="noopener">{h['map_btn']}</a>
  </div>
</div></div></section>
'''


# ----------------------------------------------------------------------------- CARTA
MENU_T = {
'pt': dict(title='Carta · Olá Kathmandu, Grândola', desc='A carta completa do Olá Kathmandu em Grândola: momo, dal bhat, caril, tandoori, biryani, naan e o Set Menu de 45 €. Preços da carta impressa, alergénios e filtro vegetariano. Pedido de take-away por WhatsApp.',
  label='Carta', h1='Momo a vapor, caril devagar, pão <em>do tandoor</em>.', lead='A carta completa, no telemóvel. Os preços são os da carta impressa; toca no «+» para montar um pedido de take-away e enviá-lo no WhatsApp.',
  filters='Filtros', legend_t='Alergénios', note='Alergénios e preços confirmam-se com a cozinha antes de publicar. Diz-nos à mesa qualquer alergia ou intolerância: adaptamos o que for possível. As secções sem preço correspondem a páginas da carta ainda não fotografadas.',
  fav='favorito', vegf='Só vegetariano', excl='Sem', basket_t='O teu pedido', send='Enviar no WhatsApp', see='Ver', hide='Esconder', add='Adicionar ao pedido'),
'en': dict(title='Menu · Olá Kathmandu, Grândola', desc='The full menu of Olá Kathmandu in Grândola: momo, dal bhat, curry, tandoori, biryani, naan and the €45 Set Menu. Printed-menu prices, allergens and a vegetarian filter. Take-away orders on WhatsApp.',
  label='Menu', h1='Steamed momo, slow curry, bread <em>from the tandoor</em>.', lead='The full menu on your phone. Prices are the ones on the printed menu; tap "+" to build a take-away order and send it on WhatsApp.',
  filters='Filters', legend_t='Allergens', note='Allergens and prices are confirmed with the kitchen before publishing. Tell us about any allergy or intolerance at the table: we adapt what we can. Sections without prices correspond to menu pages not yet photographed.',
  fav='favourite', vegf='Vegetarian only', excl='Without', basket_t='Your order', send='Send on WhatsApp', see='Show', hide='Hide', add='Add to order'),
}
ALLERGENS = {'glu': ('G', {'pt': 'Glúten', 'en': 'Gluten'}), 'lac': ('L', {'pt': 'Lactose', 'en': 'Dairy'}), 'cru': ('C', {'pt': 'Crustáceos', 'en': 'Crustaceans'}),
             'ou': ('O', {'pt': 'Ovos', 'en': 'Eggs'}), 'nuc': ('N', {'pt': 'Frutos de casca rija', 'en': 'Nuts'}), 'soj': ('S', {'pt': 'Soja', 'en': 'Soy'})}


def menu_page(ctx):
    t, m = ctx.t, MENU_T[ctx.lang]
    words = [s['title'][ctx.lang].split(' ')[0].lower() for s in MENU['sections']]
    out = head(ctx, m['title'], m['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, m['label'], m['h1'], m['lead'], crumb=m['label'], words=words)
    nav = ''.join(f'<a href="#{s["id"]}">{s["title"][ctx.lang]}</a>' for s in MENU['sections'])
    out += f'<nav class="menu-nav" aria-label="{m["label"]}"><div class="container">{nav}</div></nav>\n<div class="container">'
    chips = f'<button class="chip" type="button" aria-pressed="false" data-f="veg"><svg width="16" height="16" style="color:var(--f-verde)"><use href="#i-leaf"/></svg>{m["vegf"]}</button>'
    chips += ''.join(f'<button class="chip" type="button" aria-pressed="false" data-f="{k}"><i>{l}</i>{m["excl"]} {n[ctx.lang].lower()}</button>' for k, (l, n) in ALLERGENS.items())
    out += f'<div class="filters" role="group" aria-label="{m["filters"]}">{chips}</div>'
    legend = ''.join(f'<span><i>{l}</i>{n[ctx.lang]}</span>' for l, n in ALLERGENS.values())
    out += f'<div class="legend" aria-label="{m["legend_t"]}"><span><i style="color:var(--f-verde);border-color:var(--f-verde)">V</i>{"Vegetariano" if ctx.lang == "pt" else "Vegetarian"}</span>{legend}</div>'
    for s in MENU['sections']:
        dishes = ''
        for j, d in enumerate(s['dishes']):
            tags = d.get('tags', [])
            tg = ''.join('<i class="veg" title="Vegetarian">V</i>' if x == 'veg' else f'<i title="{ALLERGENS[x][1][ctx.lang]}">{ALLERGENS[x][0]}</i>' for x in tags)
            fav = f'<span class="fav">{m["fav"]}</span>' if d.get('fav') else ''
            price = f'<span class="price num">{d["price"]}</span>' if d.get('price') else f'<span class="price tbc">{t["price_tbc"]}</span>'
            desc = f'<span class="desc">{d["desc"][ctx.lang]}</span>' if d['desc'][ctx.lang] else ''
            tagdiv = f'<div class="tags">{tg}</div>' if tg else ''
            dishes += (f'<div class="dish" data-id="{s["id"]}-{j}" data-tags="{" ".join(tags)}"><div><span class="name">{d["name"][ctx.lang]}{fav}</span>'
                       f'{desc}{tagdiv}</div>'
                       f'<div class="side">{price}<button class="add" type="button" aria-label="{m["add"]}: {d["name"][ctx.lang]}"><svg><use href="#i-plus"/></svg></button></div></div>')
        out += f'<section class="menu-section" id="{s["id"]}"><div class="menu-section-head reveal"><p class="label">{flags()}{s["kicker"][ctx.lang]}</p><h2>{s["title"][ctx.lang]}</h2><p>{s["lead"][ctx.lang]}</p></div><div class="dishes">{dishes}</div></section>'
    out += f'<p class="menu-note">{m["note"]}</p></div>\n'
    out += f'''<aside class="basket" id="basket" aria-label="{m['basket_t']}">
  <div class="basket-bar"><div><b>{m['basket_t']} · <span class="js-count">0</span></b><small><span class="js-total">0,00 €</span> <span class="js-extra"></span></small></div>
    <div class="row"><button class="btn btn--ghost btn--sm js-toggle" type="button" style="border-color:rgba(251,246,236,.4);color:#FBF6EC">{m['see']}</button><button class="btn btn--wa btn--sm js-send" type="button"><svg><use href="#i-wa"/></svg>{m['send']}</button></div></div>
  <div class="basket-list"><ul></ul></div>
</aside>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- DELIVERY
DEL_T = {
'pt': dict(title='Delivery e take-away · Olá Kathmandu, Grândola', desc='Comida nepalesa e indiana em casa, em Grândola: pede na Glovo, Uber Eats ou Bolt Food, ou escreve o pedido de take-away no WhatsApp a partir da carta. Todos os dias 10–23.',
  label='Delivery e take-away', h1='Momo e caril <em>em casa</em>, em Grândola.', lead='Três caminhos: a app que já tens, o WhatsApp com o pedido escrito a partir da carta, ou o telefone. Em qualquer um, a comida sai da mesma cozinha.',
  faq_t='Perguntas que se repetem', faq=[('Quanto tempo demora?', 'Take-away: combinamos a hora na conversa; a maior parte dos pratos sai em 20 a 30 minutos. Nas apps, o tempo é o que a app indica. <span class="tbc">a confirmar</span>'),
        ('Posso pagar com cartão ao levantar?', 'Sim, cartão e MB Way ao levantar. <span class="tbc">a confirmar</span>'),
        ('Entregam fora de Grândola?', 'Pelas apps, a zona é a que cada app mostra. Para encomendas grandes fora da vila, liga-nos e vemos.'),
        ('Os momo viajam bem?', 'Sim. Vão a vapor em caixa fechada, com o achar à parte. Se demorares a comer, 1 minuto no micro-ondas com uma colher de água.'),
        ('E o Set Menu de 45 €?', 'Também sai para take-away: travessa fechada, para 3 a 4 pessoas. Pede com 1 hora de antecedência.')]),
'en': dict(title='Delivery and take-away · Olá Kathmandu, Grândola', desc='Nepali and Indian food at home in Grândola: order on Glovo, Uber Eats or Bolt Food, or write your take-away order on WhatsApp straight from the menu. Every day 10–23.',
  label='Delivery and take-away', h1='Momo and curry <em>at home</em>, in Grândola.', lead='Three ways: the app already on your phone, WhatsApp with the order written from the menu, or the phone. Whichever you pick, the food comes from the same kitchen.',
  faq_t='Questions that come up', faq=[('How long does it take?', 'Take-away: we agree the time in the chat; most dishes are ready in 20 to 30 minutes. On the apps, the time is the one the app shows. <span class="tbc">to be confirmed</span>'),
        ('Can I pay by card when I collect?', 'Yes, card and MB Way on collection. <span class="tbc">to be confirmed</span>'),
        ('Do you deliver outside Grândola?', 'Through the apps, the area is the one each app shows. For big orders outside town, call us and we will see.'),
        ('Do momo travel well?', 'Yes. They go steamed in a closed box, with the achar on the side. If you eat later, 1 minute in the microwave with a spoon of water.'),
        ('What about the €45 Set Menu?', 'It also goes out for take-away: a closed platter for 3 to 4 people. Order 1 hour ahead.')]),
}


def delivery_page(ctx):
    t, d, h = ctx.t, DEL_T[ctx.lang], HOME[ctx.lang]
    menu = ctx.p(t['nav'][0][0])
    out = head(ctx, d['title'], d['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, d['label'], d['h1'], d['lead'], dark=True, crumb=d['label'], words=['glovo', 'uber eats', 'bolt food', 'whatsapp', 'take-away'])
    steps = ''.join(f'<li><div><b>{a}</b><p>{b}</p></div></li>' for a, b in h['d_steps'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in d['faq'])
    out += f'''<section class="section delivery"><div class="container">
  <div class="reveal">{apps_block(ctx, h)}</div>
  <div class="reveal" data-delay="1"><p class="label">{flags()}{h['d_wa'][0]}</p><h2 style="margin-top:var(--s-4);font-size:var(--fs-h2)">{h['d_h2']}</h2>
    <ol class="steps" style="margin-top:var(--s-6)">{steps}</ol>
    <div class="hero-ctas"><a class="btn btn--cta" href="{menu}">{h['d_cta']}<svg class="arrow"><use href="#i-arrow"/></svg></a><a class="btn btn--ghost" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{TELF}</a></div></div>
</div></section>
<section class="section section--alt"><div class="container"><div class="section-head reveal"><p class="label">{flags()}{d['faq_t']}</p></div><div class="faq reveal">{faq}</div></div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- RESERVAS
RES_T = {
'pt': dict(title='Reservas · Olá Kathmandu, Grândola', desc='Reserva mesa no Olá Kathmandu, Grândola: no WhatsApp com confirmação ou por telefone. Todos os dias 10–23. Grupos com Set Menu de 45 €.',
  label='Reservas', h1='Uma mesa no Olá Kathmandu, <em>confirmada</em> na mesma conversa.', lead='Envia no WhatsApp a data, a hora e o número de pessoas. Confirmamos em poucos minutos durante o horário, ou ligamos se houver algum problema.',
  g_label='Grupos e festas', g_h2='Mesa grande, travessa grande.', g_lead='Para aniversários, equipas e famílias: o Set Menu de 45 € serve 3 a 4 pessoas com bebida; para mais gente, combinamos travessas e mesa.',
  g_people='Pessoas', g_date='Data', g_name='Nome', g_msg='Mensagem', g_msg_ph='Ocasião, horas, pedidos especiais', g_send='Pedir no WhatsApp',
  faq_t='Perguntas que se repetem', faq=[('Preciso de reservar?', 'Ao fim de semana à noite ajuda. Durante a semana costuma haver mesa, mas uma mensagem curta no WhatsApp guarda-te o lugar.'),
        ('Grupos grandes?', 'Até 10 pessoas reservas aqui. Acima disso, pede pelo formulário de grupos para combinarmos a travessa.'),
        ('Crianças?', 'Sim, e há pratos sem picante: momo, arroz frito com ovo, naan de queijo.'),
        ('Atrasos?', 'Guardamos a mesa 15 minutos. Se te atrasares mais, escreve na mesma conversa e seguramos se pudermos.')]),
'en': dict(title='Reservations · Olá Kathmandu, Grândola', desc='Book a table at Olá Kathmandu, Grândola: on WhatsApp with confirmation or by phone. Every day 10–23. Groups with the €45 Set Menu.',
  label='Reservations', h1='A table at Olá Kathmandu, <em>confirmed</em> in the same chat.', lead='Send the date, time and number of guests on WhatsApp. We confirm within minutes during opening hours, or call if there is a problem.',
  g_label='Groups and parties', g_h2='Big table, big platter.', g_lead='For birthdays, teams and families: the €45 Set Menu serves 3 to 4 with a drink; for more people we arrange platters and the table.',
  g_people='Guests', g_date='Date', g_name='Name', g_msg='Message', g_msg_ph='Occasion, time, special requests', g_send='Ask on WhatsApp',
  faq_t='Questions that come up', faq=[('Do I need to book?', 'Weekend evenings, it helps. During the week there is usually a table, but a short WhatsApp message keeps your place.'),
        ('Large groups?', 'Up to 10 people, book here. Above that, use the groups form so we can arrange the platter.'),
        ('Children?', 'Yes, and there are non-spicy dishes: momo, egg fried rice, cheese naan.'),
        ('Running late?', 'We hold the table for 15 minutes. If you are later, write in the same chat and we keep it if we can.')]),
}


def reservations_page(ctx):
    t, r, h = ctx.t, RES_T[ctx.lang], HOME[ctx.lang]
    out = head(ctx, r['title'], r['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, r['label'], r['h1'], r['lead'], crumb=r['label'], words=['reservas' if ctx.lang == 'pt' else 'bookings', 'whatsapp', TELF])
    out += booking_block(ctx, h, ctx.p(ctx.slug), section_id='reservar')
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in r['faq'])
    out += f'''<section class="section section--alt" id="grupos"><div class="container">
  <div class="section-head reveal"><p class="label">{flags()}{r['g_label']}</p><h2>{r['g_h2']}</h2><p class="lead">{r['g_lead']}</p></div>
  <div class="book">
    <form class="book-form reveal" id="groupForm" novalidate>
      <div class="fields">
        <div class="field"><label for="gPeople">{r['g_people']}</label><input id="gPeople" name="pessoas" type="number" min="4" max="60" value="8" inputmode="numeric"></div>
        <div class="field"><label for="gDate">{r['g_date']}</label><input id="gDate" name="data" type="date"></div>
        <div class="field"><label for="gName">{r['g_name']}</label><input id="gName" name="nome" type="text" autocomplete="name"></div>
        <div class="field" style="grid-column:1/-1"><label for="gMsg">{r['g_msg']}</label><textarea id="gMsg" name="mensagem" placeholder="{r['g_msg_ph']}"></textarea></div>
      </div>
      <button class="btn btn--cta js-ev-wa" type="button"><svg><use href="#i-wa"/></svg>{r['g_send']}</button>
    </form>
    {media(ctx, '1x1', 'set-menu.jpg', 'Travessa do Set Menu do Olá Kathmandu' if ctx.lang == 'pt' else 'The Olá Kathmandu Set Menu platter', extra='reveal', w=1600, h=1600)}
  </div>
</div></section>
<section class="section"><div class="container"><div class="section-head reveal"><p class="label">{flags()}{r['faq_t']}</p></div><div class="faq reveal">{faq}</div></div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- HISTÓRIA
STORY_T = {
'pt': dict(title='A nossa história · Olá Kathmandu, Grândola', desc='Olá Kathmandu: uma cozinha nepalesa e indiana na Rua São João de Deus, em Grândola. Bandeiras de oração na sala, tandoor na cozinha, momo feitos à mão.',
  label='A nossa história', h1='Um «olá» português, uma cozinha <em>de Kathmandu</em>.', lead='Esta página escreve-se com o dono. Por agora, o que se vê e se prova: a sala, o forno e a carta.',
  blocks=[('A sala', 'Bandeiras de oração penduradas do teto, um Buda dourado à entrada, a bandeira do Nepal numa parede. Mesas simples, toalhas brancas, um pátio interior. É pequeno e é de família.', 'sala-bandeiras.jpg', '3x2', 1600, 1066),
          ('A cozinha', 'Um tandoor, o forno de barro onde o naan cola à parede e o frango marinado assa a alta temperatura. Uma mistura de especiarias feita em casa, com mais de 15, que entra no caril de frango cozinhado devagar.', 'frango-tandoori.jpg', '4x5', 1200, 1500),
          ('A rua', 'Rua São João de Deus 21, no centro de Grândola. O letreiro diz «Welcome · Bem-vindo» e promete «doces nepalis, indiana e portuguesa»: há hambúrguer e wrap para quem não quer picante.', 'fachada-dia.jpg', '4x5', 1200, 1500)],
  tbc='Nomes dos donos, ano de abertura e percurso Nepal → Portugal: a recolher numa conversa com o restaurante.'),
'en': dict(title='Our story · Olá Kathmandu, Grândola', desc='Olá Kathmandu: a Nepali and Indian kitchen on Rua São João de Deus, Grândola. Prayer flags in the dining room, a tandoor in the kitchen, hand-folded momo.',
  label='Our story', h1='A Portuguese "olá", a kitchen <em>from Kathmandu</em>.', lead='This page is written with the owner. For now, what you can see and taste: the room, the oven and the menu.',
  blocks=[('The room', 'Prayer flags hanging from the ceiling, a golden Buddha by the door, the flag of Nepal on a wall. Simple tables, white cloths, an inner patio. It is small and it is family-run.', 'sala-bandeiras.jpg', '3x2', 1600, 1066),
          ('The kitchen', 'A tandoor, the clay oven where naan sticks to the wall and marinated chicken roasts at high heat. A spice blend made in-house, more than 15 of them, that goes into the slow-cooked chicken curry.', 'frango-tandoori.jpg', '4x5', 1200, 1500),
          ('The street', 'Rua São João de Deus 21, in the centre of Grândola. The sign says "Welcome · Bem-vindo" and promises Nepali, Indian and Portuguese: there is a burger and a wrap for anyone avoiding spice.', 'fachada-dia.jpg', '4x5', 1200, 1500)],
  tbc="Owners' names, opening year and the Nepal → Portugal journey: to be collected in a conversation with the restaurant."),
}


def story_page(ctx):
    s = STORY_T[ctx.lang]
    out = head(ctx, s['title'], s['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, s['label'], s['h1'], s['lead'], crumb=s['label'], words=['kathmandu', 'grândola', 'namaste', 'olá'])
    out += '<section class="section"><div class="container">'
    for i, (h2, p, file, ratio, w, hh) in enumerate(s['blocks']):
        img = media(ctx, ratio, file, h2, extra='reveal', w=w, h=hh)
        txt = f'<div class="story-text reveal" data-delay="1"><h2>{h2}</h2><p>{p}</p></div>'
        out += f'<div class="story" style="margin-bottom:var(--s-9)">{img + txt if i % 2 == 0 else txt + img}</div>'
    out += f'<p class="menu-note"><span class="tbc">{s["tbc"]}</span></p></div></section>'
    return out + footer(ctx)


# ----------------------------------------------------------------------------- GALERIA
GAL_T = {
'pt': dict(title='Galeria · Olá Kathmandu, Grândola', desc='Fotos do Olá Kathmandu em Grândola: momo, caril, tandoori, Set Menu, a sala com bandeiras de oração, a fachada.', label='Galeria', h1='A sala, a cozinha e <em>os pratos</em>.', lead='Fotos reais, da ficha pública do restaurante. Toca para ampliar.',
  tabs=[('all', 'Tudo'), ('pratos', 'Pratos'), ('sala', 'Sala e rua')], src='Fotos publicadas na ficha do restaurante no Tripadvisor (clientes e dono); autorização de uso a confirmar antes de publicar.'),
'en': dict(title='Gallery · Olá Kathmandu, Grândola', desc='Photos of Olá Kathmandu in Grândola: momo, curry, tandoori, Set Menu, the room with prayer flags, the front.', label='Gallery', h1='The room, the kitchen and <em>the plates</em>.', lead="Real photos, from the restaurant's public listing. Tap to enlarge.",
  tabs=[('all', 'All'), ('pratos', 'Dishes'), ('sala', 'Room and street')], src="Photos published on the restaurant's Tripadvisor listing (guests and owner); permission to use to be confirmed before publishing."),
}
GALLERY = [('momo.jpg', 'pratos', '1x1', {'pt': 'Momo de frango com achar', 'en': 'Chicken momo with achar'}),
           ('sala-bandeiras.jpg', 'sala', '3x2', {'pt': 'A sala, com bandeiras de oração e Buda', 'en': 'The room, with prayer flags and a Buddha'}),
           ('curry-frango.jpg', 'pratos', '3x2', {'pt': 'Caril de frango com mais de 15 especiarias', 'en': 'Chicken curry with more than 15 spices'}),
           ('dal-bhat-thali.jpg', 'pratos', '4x5', {'pt': 'Thali: arroz, dal, caril e acompanhamentos', 'en': 'Thali: rice, dal, curry and sides'}),
           ('frango-tandoori.jpg', 'pratos', '4x5', {'pt': 'Frango tandoori com molho de hortelã', 'en': 'Tandoori chicken with mint sauce'}),
           ('set-menu.jpg', 'pratos', '1x1', {'pt': 'A travessa do Set Menu (45 €)', 'en': 'The Set Menu platter (€45)'}),
           ('fachada-dia.jpg', 'sala', '4x5', {'pt': 'A fachada, Rua São João de Deus', 'en': 'The front, Rua São João de Deus'}),
           ('chowmein-arroz.jpg', 'pratos', '4x5', {'pt': 'Chowmein com arroz', 'en': 'Chowmein with rice'}),
           ('chatpate.jpg', 'pratos', '3x2', {'pt': 'Chatpate', 'en': 'Chatpate'}),
           ('patio.jpg', 'sala', '4x5', {'pt': 'O pátio interior', 'en': 'The inner patio'}),
           ('burger.jpg', 'pratos', '4x5', {'pt': 'Hambúrguer com batatas, para quem não quer picante', 'en': 'Burger and fries, for anyone avoiding spice'}),
           ('wrap.jpg', 'pratos', '4x5', {'pt': 'Wrap com salada e batatas', 'en': 'Wrap with salad and fries'}),
           ('fachada-noite.jpg', 'sala', '4x5', {'pt': 'A fachada à noite', 'en': 'The front at night'}),
           ('carta-saladas-sopas-aperitivos.jpg', 'sala', '4x5', {'pt': 'Página da carta: saladas, sopas e aperitivos', 'en': 'Menu page: salads, soups and starters'})]
SIZES = {'1x1': (1200, 1200), '3x2': (1200, 800), '4x5': (960, 1200)}


def gallery_page(ctx):
    g = GAL_T[ctx.lang]
    out = head(ctx, g['title'], g['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, g['label'], g['h1'], g['lead'], crumb=g['label'], words=['momo', 'thali', 'tandoor', 'sala' if ctx.lang == 'pt' else 'room'])
    tabs = ''.join(f'<button class="chip" type="button" aria-pressed="{"true" if k == "all" else "false"}" data-f="{k}">{v}</button>' for k, v in g['tabs'])
    items = ''
    for i, (file, cat, ratio, alt) in enumerate(GALLERY):
        w, h = SIZES[ratio]
        items += f'<div class="g{" wide" if ratio == "3x2" else ""} reveal" data-cat="{cat}"{f" data-delay=\"{i % 3}\"" if i % 3 else ""}>{media(ctx, ratio, file, alt[ctx.lang], w=w, h=h)}</div>'
    out += f'''<section class="section"><div class="container"><div class="gtabs" role="group">{tabs}</div><div class="gallery">{items}</div><p class="menu-note">{g['src']}</p></div></section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true"><button class="icon-btn close" type="button" aria-label="{ctx.t['close_menu']}"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button><img src="" alt=""><p class="cap"></p></div>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- CONTACTO
CO_T = {
'pt': dict(title='Contacto · Olá Kathmandu, Grândola', desc='Olá Kathmandu, Rua São João de Deus 21, 7570-308 Grândola. Telefone 920 220 999. Todos os dias 10:00–23:00. Mapa e como chegar.',
  label='Contacto', h1='Rua São João de Deus 21, <em>Grândola</em>.', lead='No centro da vila. Liga, escreve no WhatsApp ou aparece: estamos abertos todos os dias das 10 às 23.',
  hours_t='Horário', addr_t='Morada', talk_t='Falar connosco', amen_t='Na casa', map_t='Mapa', map_consent='O mapa do Google só carrega depois de tocares aqui (sem cookies antes).', map_load='Carregar o mapa', map_open='Abrir no Google Maps', how_t='Como chegar',
  how=[('i-pin', 'A pé', 'A rua sai do centro histórico; o restaurante fica no número 21, com o letreiro «Welcome · Bem-vindo».'), ('i-scooter', 'De carro', 'Estacionamento na rua e nas praças do centro. A 25 minutos de Alcácer do Sal e de Santiago do Cacém, 35 da Comporta.'), ('i-clock', 'De comboio', 'Estação de Grândola na linha do Sul; o centro fica a uns minutos a pé.')]),
'en': dict(title='Contact · Olá Kathmandu, Grândola', desc='Olá Kathmandu, Rua São João de Deus 21, 7570-308 Grândola, Portugal. Phone +351 920 220 999. Every day 10:00–23:00. Map and directions.',
  label='Contact', h1='Rua São João de Deus 21, <em>Grândola</em>.', lead='In the town centre. Call, message us on WhatsApp or just come in: open every day from 10 to 23.',
  hours_t='Hours', addr_t='Address', talk_t='Talk to us', amen_t='In the house', map_t='Map', map_consent='The Google map loads only after you tap here (no cookies before).', map_load='Load the map', map_open='Open in Google Maps', how_t='How to get here',
  how=[('i-pin', 'On foot', 'The street runs off the old centre; the restaurant is at number 21, under the "Welcome · Bem-vindo" sign.'), ('i-scooter', 'By car', 'Street parking and the squares in the centre. 25 minutes from Alcácer do Sal and Santiago do Cacém, 35 from Comporta.'), ('i-clock', 'By train', 'Grândola station on the southern line; the centre is a few minutes on foot.')]),
}


def contact_page(ctx):
    t, c, h = ctx.t, CO_T[ctx.lang], HOME[ctx.lang]
    out = head(ctx, c['title'], c['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, c['label'], c['h1'], c['lead'], crumb=c['label'], words=['grândola', TELF, '10–23'])
    hours = ''.join(f'<li data-day="{d}"><span>{t["days"][d]}</span><span class="num">10:00–23:00</span></li>' for d in [1, 2, 3, 4, 5, 6, 0])
    amen = ''.join(f'<span class="chip">{a}</span>' for a in h['amen']) + f' <span class="tbc">{h["amen_tbc"]}</span>'
    how = ''.join(f'<div><svg><use href="#{ic}"/></svg><div><b>{a}</b>{b}</div></div>' for ic, a, b in c['how'])
    maps_src = 'https://www.google.com/maps?q=Ol%C3%A1+Kathmandu,+Rua+S%C3%A3o+Jo%C3%A3o+de+Deus+21,+Gr%C3%A2ndola&output=embed'
    out += f'''<section class="section"><div class="container"><div class="contact-grid">
  <div class="reveal">
    <p class="label">{flags()}{c['hours_t']}</p>
    <p class="status js-status" style="margin-top:var(--s-3)"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_line']}</span></p>
    <ul class="hours">{hours}</ul>
    <p class="label" style="margin-top:var(--s-7)">{flags()}{c['addr_t']}</p>
    <p style="margin-top:var(--s-3)">{ADDR1}<br>{ADDR2}, Portugal</p>
    <p class="label" style="margin-top:var(--s-7)">{flags()}{c['talk_t']}</p>
    <div class="hero-ctas" style="margin-top:var(--s-3)"><a class="btn btn--cta" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a><a class="btn btn--ghost" href="tel:{TEL}"><svg><use href="#i-phone"/></svg>{TELF}</a></div>
    <p style="margin-top:var(--s-4)"><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p style="margin-top:var(--s-3)"><a class="link" href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a class="link" href="{NEG['tripadvisor']['url']}" target="_blank" rel="noopener">Tripadvisor</a></p>
    <p class="label" style="margin-top:var(--s-7)">{flags()}{c['amen_t']}</p>
    <div class="amen">{amen}</div>
  </div>
  <div class="reveal" data-delay="1">
    <div class="map-embed" data-src="{maps_src}" aria-label="{c['map_t']}"><div class="consent"><div><p>{c['map_consent']}</p><div class="hero-ctas" style="margin-top:var(--s-4);justify-content:center"><button class="btn btn--cta" type="button">{c['map_load']}</button><a class="btn btn--ghost" href="{MAPS}" target="_blank" rel="noopener">{c['map_open']}</a></div></div></div></div>
    <p class="label" style="margin-top:var(--s-7)">{flags()}{c['how_t']}</p>
    <div class="howto">{how}</div>
  </div>
</div></div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- LEGAL + OBRIGADO
LEGAL = {
'pt': {
 'privacidade': ('Política de privacidade · Olá Kathmandu', 'Como o Olá Kathmandu usa os dados pessoais enviados pelo site: reservas e pedidos por WhatsApp, mapa.', 'Privacidade', 'Os teus dados, <em>em resumo</em>.', 'Este site não tem cookies de rastreio e não envia nada sem uma ação tua. O que recolhemos, porquê e por quanto tempo.',
  f'''<h2>Quem somos</h2><p>Olá Kathmandu, {ADDR1}, {ADDR2}. <span class="tbc">Denominação social, NIF e sede: a completar.</span> Contacto para dados pessoais: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Que dados recolhemos e porquê</h2>
<h3>Reservas e pedidos por WhatsApp</h3><p>Os formulários de reserva, de grupo e o cesto de take-away não enviam nada para nós diretamente: compõem uma mensagem no teu telemóvel e abrem o WhatsApp. Os dados (nome, data, hora, pessoas, pratos) só chegam se carregares em «enviar» no WhatsApp. Usamo-los para guardar a mesa ou preparar o pedido e ficam no histórico da conversa, que apagamos a pedido.</p>
<h3>Plataformas de entrega</h3><p>Os botões Glovo, Uber Eats e Bolt Food levam-te para as apps dessas empresas; o que fazes lá rege-se pelas políticas delas.</p>
<h3>Mapa do Google</h3><p>O mapa da página de contacto só carrega depois de tocares em «Carregar o mapa». Só então o teu browser fala com o Google, conforme a <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">política do Google</a>.</p>
<h3>Fontes</h3><p>As fontes carregam do Google Fonts; o browser envia ao Google o endereço IP ao abrir a página. <span class="tbc">Opção: alojar as fontes no site, a decidir antes de publicar.</span></p>
<h3>Registos de servidor</h3><p>O alojamento (Netlify) guarda registos técnicos (IP, página pedida, hora) por segurança, durante pouco tempo.</p>
<h2>Cookies</h2><p>O site não usa cookies próprios nem ferramentas de análise ou publicidade. Os únicos cookies possíveis são os do Google, depois de carregares o mapa.</p>
<h2>Os teus direitos</h2><p>Podes pedir acesso, retificação, apagamento, limitação ou portabilidade dos dados e opor-te ao tratamento, escrevendo para o email acima. Podes apresentar queixa à <a href="https://www.cnpd.pt/" target="_blank" rel="noopener">CNPD</a>.</p>
<p><em>Última atualização: outubro de 2026. Texto-modelo, a rever com apoio jurídico antes de publicar.</em></p>'''),
 'termos': ('Termos e condições · Olá Kathmandu', 'Termos de utilização do site do Olá Kathmandu: reservas, take-away, propriedade intelectual, livro de reclamações.', 'Termos e condições', 'As regras <em>da casa</em>, por escrito.', 'Como funcionam as reservas e os pedidos feitos pelo site, e o que podemos prometer.',
  f'''<h2>O site</h2><p>Este site é operado pelo Olá Kathmandu, {ADDR1}, {ADDR2}. <span class="tbc">Denominação social e NIF: a completar.</span> As informações (carta, preços, horário) são indicativas e podem mudar; a carta impressa no restaurante prevalece.</p>
<h2>Reservas</h2><ul><li>Uma reserva por WhatsApp ou telefone é válida depois da nossa confirmação.</li><li>Guardamos a mesa 15 minutos depois da hora marcada; depois disso podemos dá-la a outros clientes.</li><li>Para grupos acima de 10 pessoas podemos pedir um sinal e uma ementa combinada.</li><li>Se não vieres, cancela pelo mesmo canal.</li></ul>
<h2>Take-away e delivery</h2><p>O pedido enviado por WhatsApp é uma intenção de compra; confirmamos a hora e a disponibilidade na mesma conversa. O pagamento é feito ao levantar. Nas plataformas de entrega aplicam-se as condições de cada plataforma.</p>
<h2>Alergénios</h2><p>Os alergénios marcados na carta são informativos. Diz-nos à mesa qualquer alergia; não garantimos ausência total de vestígios.</p>
<h2>Propriedade intelectual</h2><p>Textos, fotografias e grafismos do site pertencem ao Olá Kathmandu ou aos seus autores e não podem ser usados sem autorização.</p>
<h2>Reclamações e litígios</h2><p>Escreve-nos primeiro. Tens à disposição o <a href="https://www.livroreclamacoes.pt/inicio" target="_blank" rel="noopener">Livro de Reclamações eletrónico</a> e, para litígios de consumo, os centros de arbitragem (<a href="https://www.consumidor.gov.pt/" target="_blank" rel="noopener">consumidor.gov.pt</a>) e a <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">plataforma europeia RLL</a>.</p>
<p><em>Última atualização: outubro de 2026. Texto-modelo, a rever com apoio jurídico antes de publicar.</em></p>'''),
 'obrigado': ('Obrigado · Olá Kathmandu', 'O pedido foi enviado.', 'Obrigado', 'Recebemos o <em>pedido</em>.', 'Respondemos no horário de abertura, normalmente no próprio dia. Se for urgente, escreve-nos no WhatsApp.', ''),
},
'en': {
 'privacy': ('Privacy policy · Olá Kathmandu', 'How Olá Kathmandu uses personal data sent through the site: WhatsApp bookings and orders, map.', 'Privacy', 'Your data, <em>in short</em>.', 'This site has no tracking cookies and sends nothing without an action from you. What we collect, why and for how long.',
  f'''<h2>Who we are</h2><p>Olá Kathmandu, {ADDR1}, {ADDR2}, Portugal. <span class="tbc">Company name, VAT number and registered office: to be completed.</span> Contact for personal data: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>What we collect and why</h2>
<h3>Bookings and orders on WhatsApp</h3><p>The booking form, the groups form and the take-away basket send nothing to us directly: they compose a message on your phone and open WhatsApp. The details (name, date, time, guests, dishes) reach us only if you press "send" in WhatsApp. We use them to hold your table or prepare the order, and they stay in the chat history, which we delete on request.</p>
<h3>Delivery platforms</h3><p>The Glovo, Uber Eats and Bolt Food buttons take you to those companies' apps; what you do there is governed by their policies.</p>
<h3>Google map</h3><p>The map on the contact page loads only after you tap "Load the map". Only then does your browser communicate with Google, under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's policy</a>.</p>
<h3>Fonts</h3><p>Fonts load from Google Fonts; your browser sends Google your IP address when the page loads. <span class="tbc">Option: self-host the fonts, to decide before publishing.</span></p>
<h3>Server logs</h3><p>The host (Netlify) keeps short-term technical logs (IP address, page requested, time) for security.</p>
<h2>Cookies</h2><p>The site uses no cookies of its own and has no analytics or advertising tools. The only possible cookies are Google's, after you load the map.</p>
<h2>Your rights</h2><p>You can request access to your data, its rectification, erasure, restriction or portability, and object to processing, by writing to the email above. You may lodge a complaint with the Portuguese authority, <a href="https://www.cnpd.pt/" target="_blank" rel="noopener">CNPD</a>.</p>
<p><em>Last updated: October 2026. Template text, to be reviewed with legal advice before publishing.</em></p>'''),
 'terms': ('Terms & conditions · Olá Kathmandu', 'Terms of use of the Olá Kathmandu site: bookings, take-away, intellectual property, complaints book.', 'Terms & conditions', 'The <em>house</em> rules, in writing.', 'How bookings and orders made through the site work, and what we can promise.',
  f'''<h2>The site</h2><p>This site is operated by Olá Kathmandu, {ADDR1}, {ADDR2}, Portugal. <span class="tbc">Company name and VAT number: to be completed.</span> Information (menu, prices, hours) is indicative and may change; the printed menu in the restaurant prevails.</p>
<h2>Bookings</h2><ul><li>A booking on WhatsApp or by phone is valid after our confirmation.</li><li>We hold the table for 15 minutes after the booked time; after that we may give it to other guests.</li><li>For groups over 10 we may ask for a deposit and a pre-agreed menu.</li><li>If you are not coming, cancel on the same channel.</li></ul>
<h2>Take-away and delivery</h2><p>An order sent on WhatsApp is an intention to buy; we confirm time and availability in the same chat. Payment is made on collection. On delivery platforms, each platform's terms apply.</p>
<h2>Allergens</h2><p>Allergens marked on the menu are for information. Tell us about any allergy at the table; we cannot guarantee the total absence of traces.</p>
<h2>Intellectual property</h2><p>Texts, photos and graphics on the site belong to Olá Kathmandu or their authors and may not be used without permission.</p>
<h2>Complaints and disputes</h2><p>Write to us first. You can use the Portuguese <a href="https://www.livroreclamacoes.pt/inicio" target="_blank" rel="noopener">electronic Complaints Book</a> and, for consumer disputes, the arbitration centres (<a href="https://www.consumidor.gov.pt/" target="_blank" rel="noopener">consumidor.gov.pt</a>) and the <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">EU online dispute resolution platform</a>.</p>
<p><em>Last updated: October 2026. Template text, to be reviewed with legal advice before publishing.</em></p>'''),
 'thanks': ('Thank you · Olá Kathmandu', 'Your request was sent.', 'Thank you', 'We have your <em>request</em>.', 'We reply during opening hours, usually the same day. If it is urgent, message us on WhatsApp.', ''),
}}


def legal_page(ctx):
    title, desc, label, h1, lead, body = LEGAL[ctx.lang][ctx.slug]
    out = head(ctx, title, desc) + header(ctx, False)
    if not body:
        t = ctx.t
        out += f'<section class="thanks"><div class="container"><p class="label">{flags()}{label}</p><h1 style="margin-top:var(--s-4)">{h1}</h1><p class="lead">{lead}</p><div class="hero-ctas" style="justify-content:center;margin-top:var(--s-6)"><a class="btn btn--cta" href="{ctx.p("")}">{t["home"]}</a><a class="btn btn--wa" href="{wa_link(t["wa_text"])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a></div></div></section>'
        return out + footer(ctx)
    out += page_hero(ctx, label, h1, lead, crumb=label)
    out += f'<section class="section"><div class="container"><div class="prose">{body}</div></div></section>'
    return out + footer(ctx)


# ----------------------------------------------------------------------------- build
BUILDERS = {'': home, 'carta': menu_page, 'entregas': delivery_page, 'reservas': reservations_page, 'historia': story_page,
            'galeria': gallery_page, 'contacto': contact_page, 'privacidade': legal_page, 'termos': legal_page, 'obrigado': legal_page}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(HERE / 'assets', OUT / 'assets', ignore=shutil.ignore_patterns('sprite.html'))
    shutil.copy(HERE / 'assets' / 'favicon.svg', OUT / 'favicon.svg')
    if (HERE / 'media').exists(): shutil.copytree(HERE / 'media', OUT / 'media')
    n = 0
    for pt_slug, fn in BUILDERS.items():
        for lang in ('pt', 'en'):
            slug = pt_slug if lang == 'pt' else SLUGS[pt_slug]
            ctx = Ctx(lang, slug)
            write(OUT / '/'.join(ctx.rel) / 'index.html' if ctx.rel else OUT / 'index.html', fn(ctx)); n += 1
    if MODE == 'site':
        for f in (HERE / 'netlify').iterdir(): shutil.copy(f, OUT / f.name)
        urls = ''.join(f'<url><loc>{Ctx(l, s if l == "pt" else SLUGS[s]).abs()}</loc></url>' for s in BUILDERS if s != 'obrigado' for l in ('pt', 'en'))
        write(OUT / 'sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
        write(OUT / 'robots.txt', f'User-agent: *\nAllow: /\nDisallow: /obrigado/\nDisallow: /en/thanks/\nSitemap: {DOMAIN}/sitemap.xml\n')
    print(f'{n} páginas → {OUT}')


if __name__ == '__main__':
    main()
