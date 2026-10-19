#!/usr/bin/env python3
"""Gerador do site do Andalu Gastrobar (Iași). RO em / e EN em /en/.

  python3 build.py            -> site/     (links absolutos, pronto para Netlify)
  python3 build.py preview    -> preview/  (links relativos, abre de qualquer pasta)

Conceito "Sobremesa" (design/direcao-criativa.md). Factos: notas/00-site-atual.md.
"""
import json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODE = 'preview' if len(sys.argv) > 1 and sys.argv[1] == 'preview' else 'site'
OUT = ROOT / ('preview' if MODE == 'preview' else 'site')
DOMAIN = 'https://andalugastrobar.ro'
WA = '40752803443'
TEL1, TEL2 = '+40752803443', '+40740977316'
EMAIL = 'andalu.gastrobar@gmail.com'

SPRITE = (HERE / 'assets' / 'sprite.html').read_text(encoding='utf-8')
MENU = json.loads((HERE / 'data' / 'menu.json').read_text(encoding='utf-8'))

# slug RO -> slug EN
SLUGS = {'': '', 'meniu': 'menu', 'rezervari': 'reservations', 'evenimente': 'events', 'povestea-noastra': 'our-story',
         'galerie': 'gallery', 'contact': 'contact', 'confidentialitate': 'privacy', 'termeni': 'terms', 'multumim': 'thanks'}
EN2RO = {v: k for k, v in SLUGS.items()}

# ----------------------------------------------------------------------------- textos
T = {
'ro': dict(
  lang='ro', other='en', other_label='EN', self_label='RO',
  site='Andalu Gastrobar', tag='Gastrobar · Copou',
  nav=[('meniu', 'Meniu', 'tapas · paella · sangria'), ('rezervari', 'Rezervări', 'WhatsApp · telefon'), ('evenimente', 'Evenimente & catering', 'nunți · botezuri · firme'),
       ('povestea-noastra', 'Povestea noastră', 'Madrid → Iași'), ('galerie', 'Galerie', ''), ('contact', 'Contact', 'Copou')],
  skip='Sari la conținut', book='Rezervă o masă', book_wa='Rezervă pe WhatsApp', menu='Meniu', wa='WhatsApp',
  wa_text='Bună! Aș vrea să rezerv o masă la Andalu.', wa_event='Bună! Aș vrea o ofertă pentru un eveniment la Andalu.',
  hours_short='Program: marți–sâmbătă 12–22, duminică 12–20', hours_line='Ma–Sâ 12–22 · Du 12–20 · Lu închis',
  other_version='English version →', open_menu='Deschide meniul', close_menu='Închide meniul',
  footer_welcome='Gastrobar spaniol în Copou, Iași. Masa e pusă; rămâneți cât vreți.',
  f_visit='Vizitează', f_talk='Vorbește cu noi', f_pages='Pagini', f_how='Cum ajungi', privacy='Confidențialitate', terms='Termeni și condiții',
  sal='ANPC · SAL', sol='SOL · Soluționarea online a litigiilor', company='SC LALOCA13 SRL · CUI RO40171204 · J22/2131/2018 · Strada Codrescu 6, Iași',
  copy='Andalu Gastrobar · Copou, Iași', quick='Acțiuni rapide', lang_label='Limbă / Language', main_nav='Principal',
  days=['Duminică', 'Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă'], closed='Închis',
  home='Acasă', photo_tbc='foto reală · urmează', price_tbc='preț în meniu',
),
'en': dict(
  lang='en', other='ro', other_label='RO', self_label='EN',
  site='Andalu Gastrobar', tag='Gastrobar · Copou',
  nav=[('menu', 'Menu', 'tapas · paella · sangria'), ('reservations', 'Reservations', 'WhatsApp · phone'), ('events', 'Events & catering', 'weddings · parties · corporate'),
       ('our-story', 'Our story', 'Madrid → Iași'), ('gallery', 'Gallery', ''), ('contact', 'Contact', 'Copou')],
  skip='Skip to content', book='Book a table', book_wa='Book on WhatsApp', menu='Menu', wa='WhatsApp',
  wa_text="Hello! I'd like to book a table at Andalu.", wa_event="Hello! I'd like a quote for an event at Andalu.",
  hours_short='Hours: Tuesday–Saturday 12–22, Sunday 12–20', hours_line='Tue–Sat 12–22 · Sun 12–20 · Mon closed',
  other_version='Versiunea în română →', open_menu='Open menu', close_menu='Close menu',
  footer_welcome='Spanish gastrobar in Copou, Iași. The table is set; stay as long as you like.',
  f_visit='Visit', f_talk='Talk to us', f_pages='Pages', f_how='How to get here', privacy='Privacy', terms='Terms & conditions',
  sal='ANPC · SAL', sol='ODR · Online dispute resolution', company='SC LALOCA13 SRL · VAT RO40171204 · Trade register J22/2131/2018 · Strada Codrescu 6, Iași',
  copy='Andalu Gastrobar · Copou, Iași', quick='Quick actions', lang_label='Limbă / Language', main_nav='Main',
  days=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], closed='Closed',
  home='Home', photo_tbc='real photo · coming', price_tbc='price on the menu',
)}

# ----------------------------------------------------------------------------- helpers
def wa_link(text):
    from urllib.parse import quote
    return f'https://wa.me/{WA}?text={quote(text)}'

def star():
    return '<svg class="star"><use href="#i-estrella"/></svg>'

def ph(ratio, a, b, pid):
    w, h = {'4x5': (4, 5), '3x2': (3, 2), '1x1': (1, 1), '21x9': (21, 9), '16x9': (16, 9)}[ratio]
    return (f'<svg class="ph" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="{pid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs><rect width="{w}" height="{h}" fill="url(#{pid})"/></svg>')

PALETTE = [('#C99A3B', '#A84A28'), ('#E0B45A', '#8E3C1F'), ('#8E3C1F', '#1F4E8C'), ('#F3DCD0', '#C99A3B'), ('#143563', '#8E3C1F'), ('#1F4E8C', '#C99A3B'), ('#5B6B3A', '#C99A3B')]
_pid = [0]
def media(ctx, ratio, file, alt, caption=True, w=800, h=1000, extra='', eager=False):
    _pid[0] += 1
    a, b = PALETTE[_pid[0] % len(PALETTE)]
    cap = ''   # fotos reais desde 2026-10-19; a legenda 'urmează' saiu
    load = '' if eager else ' loading="lazy"'
    return (f'<figure class="media media--{ratio} {extra}">{ph(ratio, a, b, "g" + str(_pid[0]))}'
            f'<img src="{ctx.u("media/foto/" + file)}" alt="{alt}" width="{w}" height="{h}"{load} decoding="async" onerror="this.classList.add(\'is-missing\')">{cap}</figure>')


class Ctx:
    def __init__(self, lang, slug):
        self.lang, self.slug, self.t = lang, slug, T[lang]
        self.ro_slug = slug if lang == 'ro' else EN2RO[slug]
        self.en_slug = SLUGS[self.ro_slug]
        parts = ([] if lang == 'ro' else ['en']) + ([slug] if slug else [])
        self.rel = parts
        self.depth = len(parts)
    def page_path(self, lang, slug):
        parts = ([] if lang == 'ro' else ['en']) + ([slug] if slug else [])
        if MODE == 'site':
            return '/' + ''.join(p + '/' for p in parts)
        return '../' * self.depth + ''.join(p + '/' for p in parts) + 'index.html'
    def p(self, slug):            # página na mesma língua
        return self.page_path(self.lang, slug)
    def twin(self):               # página gémea na outra língua
        other = self.t['other']
        return self.page_path(other, self.en_slug if other == 'en' else self.ro_slug)
    def u(self, asset):           # assets e media
        return ('/' if MODE == 'site' else '../' * self.depth) + asset
    def abs(self, lang=None, slug=None):
        lang = lang or self.lang; slug = self.slug if slug is None else slug
        parts = ([] if lang == 'ro' else ['en']) + ([slug] if slug else [])
        return DOMAIN + '/' + ''.join(p + '/' for p in parts)


# ----------------------------------------------------------------------------- layout
def head(ctx, title, desc, jsonld=None, theme='#F7F2E9'):
    t = ctx.t
    ld = json.dumps(jsonld, ensure_ascii=False) if jsonld else ''
    return f'''<!doctype html>
<html lang="{ctx.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{theme}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15130F" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{ctx.abs()}">
<link rel="alternate" hreflang="ro" href="{ctx.abs('ro', ctx.ro_slug)}">
<link rel="alternate" hreflang="en" href="{ctx.abs('en', ctx.en_slug)}">
<link rel="alternate" hreflang="x-default" href="{ctx.abs('ro', ctx.ro_slug)}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta property="og:url" content="{ctx.abs()}"><meta property="og:image" content="{DOMAIN}/media/foto/og-inicio.jpg"><meta property="og:locale" content="{'ro_RO' if ctx.lang == 'ro' else 'en_GB'}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
<link rel="icon" href="{ctx.u('favicon.svg')}" type="image/svg+xml">
<link rel="stylesheet" href="{ctx.u('assets/site.css')}">
{('<script type="application/ld+json">' + ld + '</script>') if ld else ''}
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<div class="grain" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .9 0"/></filter><rect width="100%" height="100%" filter="url(#g)"/></svg></div>
{SPRITE}
'''


def header(ctx, over_hero):
    t = ctx.t
    nav = ''.join(f'<a href="{ctx.p(s)}"{" aria-current=\"page\"" if s == ctx.slug else ""}>{lab}</a>' for s, lab, _ in t['nav'])
    sheet = ''.join(f'<a href="{ctx.p(s)}">{lab}{(" <small>" + sm + "</small>") if sm else ""}</a>' for s, lab, sm in t['nav'])
    book_href = '#rezervari' if ctx.slug == '' else ctx.p(t['nav'][1][0])
    return f'''<header class="header{' is-over-hero' if over_hero else ''}" id="header">
  <div class="container">
    <a class="brand" href="{ctx.p('')}" aria-label="{t['site']}, {t['home']}"><img class="logo logo--ink" src="{ctx.u('media/foto/logo-tinta.png')}" alt="Andalú GastroBar" width="1077" height="783" decoding="async"><img class="logo logo--alb" src="{ctx.u('media/foto/logo-alb.png')}" alt="" aria-hidden="true" width="1077" height="783" decoding="async"><small>{t['tag']}</small></a>
    <nav class="nav" aria-label="{t['main_nav']}">{nav}</nav>
    <div class="header-actions">
      <nav class="lang" aria-label="{t['lang_label']}">
        <a href="{ctx.p(ctx.slug) if ctx.lang == 'ro' else ctx.twin()}" hreflang="ro" lang="ro"{' aria-current="true"' if ctx.lang == 'ro' else ''}><span>RO</span></a>
        <a href="{ctx.p(ctx.slug) if ctx.lang == 'en' else ctx.twin()}" hreflang="en" lang="en"{' aria-current="true"' if ctx.lang == 'en' else ''}><span>EN</span></a>
      </nav>
      <a class="btn btn--wa" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span>{t['wa']}</span></a>
      <a class="btn btn--cta" href="{book_href}">{t['book']}</a>
      <button class="icon-btn burger" type="button" aria-controls="sheet" aria-expanded="false" aria-label="{t['open_menu']}"><svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
    </div>
  </div>
</header>
<div class="sheet" id="sheet" aria-hidden="true">
  <button class="icon-btn close" type="button" aria-label="{t['close_menu']}"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>
  <nav aria-label="{t['main_nav']} (mobile)">{sheet}</nav>
  <div class="sheet-foot">
    <p class="status js-status"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_short']}</span></p>
    <div class="row"><a class="btn btn--cta" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener">{t['book_wa']}</a><a class="btn btn--ghost" href="tel:{TEL1}">0752 803 443</a></div>
    <p><a class="link" href="{ctx.twin()}" hreflang="{t['other']}" lang="{t['other']}">{t['other_version']}</a></p>
  </div>
</div>
<main id="main">
'''


def footer(ctx):
    t = ctx.t
    pages = ''.join(f'<li><a href="{ctx.p(s)}">{lab}</a></li>' for s, lab, _ in t['nav'][:5])
    priv, term = ('confidentialitate', 'termeni') if ctx.lang == 'ro' else ('privacy', 'terms')
    book_href = '#rezervari' if ctx.slug == '' else ctx.p(t['nav'][1][0])
    return f'''</main>
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><a class="brand brand--lg" href="{ctx.p('')}" aria-label="{t['site']}, {t['home']}"><img class="logo logo--ink" src="{ctx.u('media/foto/logo-tinta.png')}" alt="Andalú GastroBar" width="1077" height="783" decoding="async"><img class="logo logo--alb" src="{ctx.u('media/foto/logo-alb.png')}" alt="" aria-hidden="true" width="1077" height="783" decoding="async"></a><p class="welcome">{t['footer_welcome']}</p></div>
      <div><h4>{t['f_visit']}</h4><ul><li>Strada Teodor Codrescu 6<br>Iași 700481</li><li class="num">{t['hours_line']}</li><li><a class="link" href="{ctx.p(t['nav'][5][0])}">{t['f_how']}</a></li></ul></div>
      <div><h4>{t['f_talk']}</h4><ul><li><a href="tel:{TEL1}" class="num">0752 803 443</a></li><li><a href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="https://www.instagram.com/andalugastrobar" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.facebook.com/andalugastrobar" target="_blank" rel="noopener">Facebook</a></li></ul></div>
      <div><h4>{t['f_pages']}</h4><ul>{pages}<li><a href="{ctx.p(priv)}">{t['privacy']}</a></li><li><a href="{ctx.p(term)}">{t['terms']}</a></li></ul></div>
    </div>
    <div class="footer-legal">
      <div class="anpc"><a href="https://anpc.ro/ce-este-sal/" target="_blank" rel="noopener">{t['sal']}</a><a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">{t['sol']}</a><a href="https://anpc.ro/" target="_blank" rel="noopener">ANPC</a></div>
      <p>{t['company']}</p>
      <div class="footer-bar"><span>© <span class="js-year num">2026</span> {t['copy']}</span>
        <nav class="lang" aria-label="{t['lang_label']}">
          <a href="{ctx.p(ctx.slug) if ctx.lang == 'ro' else ctx.twin()}" hreflang="ro" lang="ro"{' aria-current="true"' if ctx.lang == 'ro' else ''}><span>RO</span></a>
          <a href="{ctx.p(ctx.slug) if ctx.lang == 'en' else ctx.twin()}" hreflang="en" lang="en"{' aria-current="true"' if ctx.lang == 'en' else ''}><span>EN</span></a>
        </nav></div>
    </div>
  </div>
</footer>
<nav class="tabbar" aria-label="{t['quick']}">
  <a class="btn btn--wa" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg><span class="sr-only">WhatsApp</span></a>
  <a class="btn btn--cta" href="{book_href}">{t['book']}</a>
  <a class="btn btn--ghost" href="{ctx.p(t['nav'][0][0])}">{t['menu']}</a>
</nav>
<script src="{ctx.u('assets/site.js')}" defer></script>
</body>
</html>
'''


def page_hero(ctx, label, h1, lead, dark=False, crumb=None):
    t = ctx.t
    az = ('<div class="az" aria-hidden="true"><svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" viewBox="0 0 1200 400"><defs><pattern id="azp" width="120" height="120" patternUnits="userSpaceOnUse"><path d="M60 8l13 39 39 13-39 13-13 39-13-39-39-13 39-13z" fill="none" stroke="#fff" stroke-width="1"/><circle cx="60" cy="60" r="6" fill="none" stroke="#fff" stroke-width="1"/></pattern></defs><rect width="1200" height="400" fill="url(#azp)"/></svg></div>') if dark else ''
    return f'''<section class="page-hero{' page-hero--dark' if dark else ''}">{az}
  <div class="container">
    <p class="crumbs"><a href="{ctx.p('')}">{t['home']}</a><span>/</span><span>{crumb or h1}</span></p>
    <p class="label" style="margin-top:var(--s-5)">{star()}{label}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
'''


# ----------------------------------------------------------------------------- JSON-LD
def restaurant_ld(ctx):
    return {"@context": "https://schema.org", "@type": "Restaurant", "name": "Andalu Gastrobar", "url": ctx.abs('ro', ''),
            "image": DOMAIN + "/media/foto/og-inicio.jpg", "servesCuisine": ["Spanish", "Mediterranean"], "telephone": TEL1, "email": EMAIL,
            "address": {"@type": "PostalAddress", "streetAddress": "Strada Teodor Codrescu 6", "addressLocality": "Iași", "postalCode": "700481", "addressRegion": "Iași", "addressCountry": "RO"},
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "12:00", "closes": "22:00"},
                {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "12:00", "closes": "20:00"}],
            "acceptsReservations": "True", "hasMenu": ctx.abs('ro', 'meniu'),
            "sameAs": ["https://www.instagram.com/andalugastrobar", "https://www.facebook.com/andalugastrobar"],
            "founder": [{"@type": "Person", "name": "Ioana Luca"}, {"@type": "Person", "name": "Daniel Luca"}], "foundingDate": "2019", "legalName": "SC LALOCA13 SRL", "vatID": "RO40171204",
            "logo": DOMAIN + "/media/foto/logo-tinta.png", "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "1734"}}


# ----------------------------------------------------------------------------- INÍCIO
HOME = {
'ro': dict(title='Andalu Gastrobar · Spania, la o masă în Copou, Iași',
  desc='Gastrobar spaniol în Copou, Iași, lângă Grădina Botanică. Tapas, paella cu orez din Valencia, sangria și vinuri spaniole. Ioana și Daniel, după mai bine de zece ani la Madrid. Rezervări pe WhatsApp.',
  label='Gastrobar spaniol · Copou, Iași · din 2019', h1=('Tapas, paella', 'și o <em>sobremesa</em>', 'lungă, în Copou.'),
  sub='Ioana și Daniel s-au întors din Madrid cu bucătăria pe care au iubit-o acolo: orez din Valencia, jamón, ulei de măsline și vin din Spania. Pe Strada Teodor Codrescu 6, lângă Grădina Botanică.',
  see_menu='Vezi meniul', today='Astăzi la Andalu', reviews='de recenzii pe Google', today_k='Astăzi', where_k='Unde', where='Teodor Codrescu 6, Copou', where_s='la 5 minute de Grădina Botanică', mon='Luni închis',
  proof=[('4,8 din 5', '<span class="num">1 734</span> de recenzii', 'Google'), ('4,8 din 5', '#8 din 255 de restaurante din Iași', 'Tripadvisor'), ('98 %', 'recomandă · <span class="num">234</span> de recenzii', 'Facebook')],
  proof4=('Terasă · 150 m²', 'Până la 100 de persoane, interior și terasă', 'Copou, Iași'),
  lm_label='La masă', lm_h2='Se începe cu tapas. Se termină <em>târziu</em>.', lm_lead='Farfurii de împărțit, o paella pentru doi, o carafă de sangria cu cava și o crema catalana la final. Ca într-un restaurant de familie din Spania: Ioana și Daniel sunt în sală.',
  plates=[('tapas', 'tapas-platou-de-impartit.jpg', 'Scoici Saint-Jacques pe grătar, cu unt și salsa verde', '01 · Tapas', 'Gambas al ajillo, pulpo a la gallega, jamón ibérico tăiat la cuțit.', 'Farfurii mici, de pus în mijlocul mesei. Pâinea e pentru sosul de la creveți.'),
          ('paella', 'paella-marinera-pentru-doi.jpg', 'Paella cu fructe de mare și creveți roșii sălbatici, în tigaie', '02 · Paella', 'Paella pentru doi, cu orez din Valencia.', 'Cu fructe de mare, neagră cu creveți și calamari, sau cu pui, iepure și chorizo. Se face la comandă; merită așteptarea.'),
          ('sangria', 'sangria-alba-pahar.jpg', 'White sangria la pahar, cu zmeură și lămâie, pe terasă', '03 · Bar', 'Sangria cu cava, vinuri spaniole, gin tonic Flor de Sevilla.', 'O carafă pentru masă, un Rioja sau un Albariño la sticlă, un cocktail pe terasă.'),
          ('desert', 'cafea-cappuccino.jpg', 'Cappuccino cu o inimă în spumă', '04 · Final', 'Crema catalana, tartă San Sebastián și încă o cafea.', 'Partea de masă care nu se grăbește. Sobremesa, cum îi spun spaniolii.')],
  m_label='Din meniu', m_h2='Tot meniul, pe telefon, cu alergeni și <em>filtre</em>.', m_lead='Fără PDF. Meniul complet, cu prețuri și gramaje, alergeni marcați la fiecare preparat și filtru pentru vegetarian.',
  m_open='Deschide meniul complet', m_photo_alt='Masă plină cu tapas, văzută de sus', m_filters='Exemplu de filtre din meniu',
  chips=['Vegetarian', 'Fără gluten', 'Fără lactoză', 'Crustacee', 'Moluște'],
  s_label='Povestea noastră', s_h2='Peste zece ani la Madrid. Apoi, <em>acasă</em>, în Copou.',
  s_p1='Suntem Ioana și Daniel, un cuplu din Iași. Am trăit mai bine de zece ani la Madrid, unde Daniel a lucrat în restaurante și Ioana într-o companie din domeniul sănătății. Ideea a apărut în 2016, într-o vizită acasă. Ne-am întors la sfârșitul lui 2018 și am deschis Andalu în 2019.',
  s_p2='Numele a venit din întâmplare, de la un magazin de ceramică, în timpul lucrărilor. Andaluzia a rămas în el. Ce n-a venit din întâmplare: ingredientele din Spania, bucătarul care a gătit în Spania și Andorra, și faptul că ne găsiți în sală, la mese, ca în restaurantele de familie de acolo.',
  s_alt='Sala Andalu: scaune de catifea verde, galbenă și roz, desene pe pereți', facts=[('10+', 'ani la Madrid'), ('2019', 'deschiderea, în Copou'), ('16', 'oameni în echipă'), ('220 m²', 'interior + terasă 150 m²')], s_more='Citește povestea întreagă →',
  o_label='Din Spania, la masă', o_h2='Ce vine de <em>acolo</em>.', o_lead='Cele mai multe ingrediente le aducem din Spania. Nu pentru etichetă, ci pentru că o paella fără orez din Valencia e alt fel de mâncare.',
  ledger=[('i-rice', 'Orez pentru paella', 'bob rotund, absoarbe fondul fără să se înmoaie', 'Valencia'), ('i-jamon', 'Jamón și mezeluri', 'tăiate la comandă', 'Spania'), ('i-cheese', 'Brânzeturi', 'pe platouri, lângă vin', 'Spania'),
          ('i-oil', 'Ulei de măsline', 'pe masă, cu pâine, de la început', 'Spania'), ('i-wine', 'Vin', 'la pahar și la sticlă, în Sangria Alegria', 'Spania'), ('i-chef', 'Bucătarul', 'român, format în bucătării din Spania și Andorra', 'Spania · Andorra')],
  e_label='Evenimente &amp; catering', e_h2='O masă lungă, <em>a voastră</em>: la noi sau la voi.', e_lead='Nunți, botezuri, aniversări și evenimente de firmă, în sală, pe terasă sau cu catering la locația voastră. Până la 100 de persoane la noi.',
  kinds=[('i-rings', 'Nunți', 'Meniu spaniol de împărțit, paella pentru toată masa.'), ('i-cake', 'Botezuri și aniversări', 'Sală de 220 m², terasă de 150 m², scaune pentru copii.'), ('i-briefcase', 'Evenimente de firmă', 'Prânzuri de echipă, cine cu clienți, Wi-Fi, parcare.'), ('i-party', 'Catering', 'Tapas și paella gătite la voi, cu echipa noastră.')],
  e_cta='Cere o ofertă', e_wa='Scrie-ne pe WhatsApp',
  r_label='Rezervări', r_h2='Rezervi în 30 de secunde. Noi <em>confirmăm</em>.', r_lead='Mai ales vineri și sâmbătă seara e bine să rezervi. Trimiți pe WhatsApp, noi confirmăm masa în același chat sau te sunăm.',
  f_title='Rezervă pe WhatsApp', f_date='Data', f_time='Ora', f_people='Persoane', f_name='Numele', f_name_ph='Prenume și nume', f_send='Trimite rezervarea pe WhatsApp',
  f_note='Se deschide WhatsApp cu mesajul gata scris. Peste 12 persoane sau un eveniment? <a class="link" href="{ev}">Cere o ofertă</a>. Nu trimitem nimic fără tine; datele rămân în telefonul tău.',
  ways=[('Telefon', 'Marți–duminică, în orele de program.'), ('Pe platformele pe care le folosești deja', 'Rezervările făcute pe Poloniq și Bookingham ajung la aceeași echipă, în același caiet.'), ('Take away și livrare', 'Paella și tapas la pachet, de ridicat de la noi sau prin aplicațiile de livrare.')],
  ways_tbc='detalii de confirmat',
  v_label='Ce spun oaspeții', v_h2='<span class="num">1 734</span> de recenzii pe Google. Media: <em>4,8</em>.', v_lead='Revin cele mai des: sangria, paella, atmosfera spaniolă și faptul că Ioana și Daniel sunt la mese.',
  v_ph=['Cea mai bună mâncare din Iași. Dacă ar fi să aleg un singur loc unde să mănânc în Iași, aici ar fi, la Andalu. Favoritele mele: caracatița a la gallega, creveții cu sos de cognac, chipirones fritos.', 'Servirea a fost excelentă, terasa este răcoroasă și perfectă pentru zilele de vară, iar mâncarea a fost foarte bună. Paella cu fructe de mare pentru două persoane și patatas alioli. Le recomand cu drag!', 'Startere delicioase, porții destul de mari, gustul specific. Tot personalul foarte amabil, zâmbitor, glumeț, iar gazdele la fel de carismatice.'], v_who=['Laura A. · Local Guide · Google, 2026', 'Alexandru P. · Google, 2026', 'Alexandra F. · Local Guide · Google, 2026'],
  v_all='Vezi toate recenziile pe Google →', ig='@andalugastrobar pe Instagram →',
  c_label='Cum ajungi', c_h2='În Copou, la cinci minute de <em>Grădina Botanică</em>.', c_addr='Adresă', c_hours='Program', c_tel='Telefon', c_mail='Email',
  c_hours_v='Marți–sâmbătă 12:00–22:00<br>Duminică 12:00–20:00<br>Luni închis', amen=['Terasă', 'Parcare', 'Wi-Fi', 'Card și NFC', 'Acces cu scaun rulant', 'Scaune pentru copii', 'Opțiuni vegetariene'],
  map_btn='Deschide în Google Maps', map_aria='Hartă schematică: Copou, Iași', botanic='GRĂDINA BOTANICĂ'),
'en': dict(title='Andalu Gastrobar · Spain at a table in Copou, Iași',
  desc='Spanish gastrobar in Copou, Iași, next to the Botanical Garden. Tapas, paella with Valencian rice, sangria and Spanish wines. Ioana and Daniel, after more than ten years in Madrid. Book on WhatsApp.',
  label='Spanish gastrobar · Copou, Iași · since 2019', h1=('Tapas, paella', 'and a long', '<em>sobremesa</em> in Copou.'),
  sub='Ioana and Daniel came back from Madrid with the kitchen they loved there: Valencian rice, jamón, olive oil and Spanish wine. Strada Teodor Codrescu 6, next to the Botanical Garden.',
  see_menu='See the menu', today='Today at Andalu', reviews='Google reviews', today_k='Today', where_k='Where', where='Teodor Codrescu 6, Copou', where_s='5 minutes from the Botanical Garden', mon='Closed on Mondays',
  proof=[('4.8 / 5', '<span class="num">1,734</span> reviews', 'Google'), ('4.8 / 5', '#8 of 255 restaurants in Iași', 'Tripadvisor'), ('98 %', 'recommend · <span class="num">234</span> reviews', 'Facebook')],
  proof4=('Terrace · 150 m²', 'Up to 100 guests, indoors and on the terrace', 'Copou, Iași'),
  lm_label='At the table', lm_h2='It starts with tapas. It ends <em>late</em>.', lm_lead='Plates to share, a paella for two, a jug of cava sangria and a crema catalana to finish. Like a family-run place in Spain: Ioana and Daniel are on the floor.',
  plates=[('tapas', 'tapas-platou-de-impartit.jpg', 'Grilled scallops with butter and salsa verde', '01 · Tapas', 'Gambas al ajillo, pulpo a la gallega, hand-carved jamón ibérico.', 'Small plates for the middle of the table. The bread is for the prawn sauce.'),
          ('paella', 'paella-marinera-pentru-doi.jpg', 'Seafood paella with wild red prawns, in the pan', '02 · Paella', 'Paella for two, with rice from Valencia.', 'Seafood, black with prawns and squid, or chicken, rabbit and chorizo. Cooked to order; worth the wait.'),
          ('sangria', 'sangria-alba-pahar.jpg', 'White sangria by the glass, with raspberries and lemon, on the terrace', '03 · Bar', 'Cava sangria, Spanish wines, Flor de Sevilla gin and tonic.', 'A jug for the table, a Rioja or an Albariño by the bottle, a cocktail on the terrace.'),
          ('desert', 'cafea-cappuccino.jpg', 'Cappuccino with a heart in the foam', '04 · To finish', 'Crema catalana, San Sebastián cheesecake and one more coffee.', 'The part of the meal nobody hurries. Sobremesa, as the Spanish call it.')],
  m_label='From the menu', m_h2='The whole menu on your phone, with allergens and <em>filters</em>.', m_lead='No PDF. The full menu with prices, allergens marked on every dish and a vegetarian filter.',
  m_open='Open the full menu', m_photo_alt='A table full of tapas, seen from above', m_filters='Example of menu filters',
  chips=['Vegetarian', 'Gluten-free', 'Lactose-free', 'Crustaceans', 'Molluscs'],
  s_label='Our story', s_h2='More than ten years in Madrid. Then <em>home</em>, to Copou.',
  s_p1='We are Ioana and Daniel, a couple from Iași. We lived in Madrid for more than ten years, where Daniel worked in restaurants and Ioana for a healthcare company. The idea came in 2016, on a visit home. We moved back at the end of 2018 and opened Andalu in 2019.',
  s_p2='The name came by chance, from a ceramics shop, during the renovation. Andalusia stayed in it. What did not come by chance: the ingredients from Spain, a chef who cooked in Spain and Andorra, and the fact that you will find us on the floor, at the tables, like the family-run places over there.',
  s_alt='The Andalu dining room: green, yellow and pink velvet chairs, drawings on the walls', facts=[('10+', 'years in Madrid'), ('2019', 'opened, in Copou'), ('16', 'people on the team'), ('220 m²', 'indoors + 150 m² terrace')], s_more='Read the whole story →',
  o_label='From Spain, to the table', o_h2='What comes from <em>there</em>.', o_lead='Most of our ingredients come from Spain. Not for the label, but because a paella without Valencian rice is a different dish.',
  ledger=[('i-rice', 'Paella rice', 'round grain, soaks up the stock without going soft', 'Valencia'), ('i-jamon', 'Jamón and charcuterie', 'sliced to order', 'Spain'), ('i-cheese', 'Cheeses', 'on boards, next to the wine', 'Spain'),
          ('i-oil', 'Olive oil', 'on the table with bread, from the start', 'Spain'), ('i-wine', 'Wine', 'by the glass and bottle, in Sangria Alegria', 'Spain'), ('i-chef', 'The chef', 'Romanian, trained in kitchens in Spain and Andorra', 'Spain · Andorra')],
  e_label='Events &amp; catering', e_h2='One long table, <em>yours</em>: at ours or at yours.', e_lead='Weddings, christenings, birthdays and corporate events, in the dining room, on the terrace or catered at your venue. Up to 100 guests at ours.',
  kinds=[('i-rings', 'Weddings', 'A Spanish sharing menu, paella for the whole table.'), ('i-cake', 'Christenings and birthdays', '220 m² dining room, 150 m² terrace, high chairs.'), ('i-briefcase', 'Corporate events', 'Team lunches, client dinners, Wi-Fi, parking.'), ('i-party', 'Catering', 'Tapas and paella cooked at your place, with our team.')],
  e_cta='Request a quote', e_wa='Message us on WhatsApp',
  r_label='Reservations', r_h2='Book in 30 seconds. We <em>confirm</em>.', r_lead='Friday and Saturday evenings especially, it pays to book. Send it on WhatsApp and we confirm in the same chat or call you back.',
  f_title='Book on WhatsApp', f_date='Date', f_time='Time', f_people='Guests', f_name='Name', f_name_ph='First and last name', f_send='Send the booking on WhatsApp',
  f_note='WhatsApp opens with the message already written. More than 12 people, or an event? <a class="link" href="{ev}">Request a quote</a>. Nothing is sent without you; the details stay on your phone.',
  ways=[('Phone', 'Tuesday to Sunday, during opening hours.'), ('On the platforms you already use', 'Bookings made on Poloniq and Bookingham reach the same team, in the same book.'), ('Take away and delivery', 'Paella and tapas to go, picked up from us or through the delivery apps.')],
  ways_tbc='details to be confirmed',
  v_label='What guests say', v_h2='<span class="num">1,734</span> Google reviews. Average: <em>4.8</em>.', v_lead='What comes up most: the sangria, the paella, the Spanish atmosphere and the fact that Ioana and Daniel are at the tables.',
  v_ph=['The best food in Iași. If I had to pick a single place to eat in Iași, it would be here, at Andalu. My favourites: the octopus a la gallega, the prawns in cognac sauce, the chipirones fritos.', 'The service was excellent, the terrace is cool and perfect for summer days, and the food was very good. Seafood paella for two and patatas alioli. Warmly recommended!', 'Delicious starters, generous portions, the authentic taste. All the staff very kind, smiling, funny, and the hosts just as charismatic.'], v_who=['Laura A. · Local Guide · Google, 2026 · translated from Romanian', 'Alexandru P. · Google, 2026 · translated from Romanian', 'Alexandra F. · Local Guide · Google, 2026 · translated from Romanian'],
  v_all='See all reviews on Google →', ig='@andalugastrobar on Instagram →',
  c_label='How to get here', c_h2='In Copou, five minutes from the <em>Botanical Garden</em>.', c_addr='Address', c_hours='Hours', c_tel='Phone', c_mail='Email',
  c_hours_v='Tuesday–Saturday 12:00–22:00<br>Sunday 12:00–20:00<br>Monday closed', amen=['Terrace', 'Parking', 'Wi-Fi', 'Card and NFC', 'Wheelchair access', 'High chairs', 'Vegetarian options'],
  map_btn='Open in Google Maps', map_aria='Schematic map: Copou, Iași', botanic='BOTANICAL GARDEN'),
}


def home(ctx):
    t, h = ctx.t, HOME[ctx.lang]
    ev = ctx.p(t['nav'][2][0]); menu = ctx.p(t['nav'][0][0]); story = ctx.p(t['nav'][3][0])
    out = head(ctx, h['title'], h['desc'], restaurant_ld(ctx)) + header(ctx, True)
    out += f'''<section class="hero" id="start">
  <div class="hero-media" aria-hidden="true">
    <div class="hero-ph"><span class="blob b1"></span><span class="blob b2"></span><span class="blob b3"></span>
      <svg class="azulejo" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" viewBox="0 0 1200 800"><defs><pattern id="az" width="120" height="120" patternUnits="userSpaceOnUse"><path d="M60 8l13 39 39 13-39 13-13 39-13-39-39-13 39-13z" fill="none" stroke="#fff" stroke-width="1"/><circle cx="60" cy="60" r="6" fill="none" stroke="#fff" stroke-width="1"/><path d="M0 0h120v120" fill="none" stroke="#fff" stroke-width=".6" stroke-opacity=".5"/></pattern></defs><rect width="1200" height="800" fill="url(#az)"/></svg>
    </div>
    <picture class="hero-poster"><source media="(orientation: portrait)" srcset="{ctx.u('media/foto/hero-poster-9x16.jpg')}"><img src="{ctx.u('media/foto/hero-poster-16x9.jpg')}" alt="" width="1920" height="1080" fetchpriority="high" decoding="async"></picture>
    <video id="heroVideo" muted loop playsinline preload="none"
      data-src-landscape="{ctx.u('media/video/hero-16x9.mp4')}" data-webm-landscape="{ctx.u('media/video/hero-16x9.webm')}" data-poster-landscape="{ctx.u('media/foto/hero-poster-16x9.jpg')}"
      data-src-portrait="{ctx.u('media/video/hero-9x16.mp4')}" data-webm-portrait="{ctx.u('media/video/hero-9x16.webm')}" data-poster-portrait="{ctx.u('media/foto/hero-poster-9x16.jpg')}"></video>
  </div>
  <div class="curtain" aria-hidden="true"></div>
  <div class="container"><div class="hero-grid">
    <div>
      <p class="label">{star()}{h['label']}</p>
      <h1><span class="line">{h['h1'][0]}</span><span class="line">{h['h1'][1]}</span><span class="line">{h['h1'][2]}</span></h1>
      <p class="hero-sub">{h['sub']}</p>
      <div class="hero-ctas"><a class="btn btn--cta" href="#rezervari">{t['book']}<svg class="arrow"><use href="#i-arrow"/></svg></a><a class="btn btn--ghost" href="{menu}">{h['see_menu']}</a></div>
    </div>
    <aside class="today" aria-label="{h['today']}">
      <div class="rating"><b class="num">{'4,8' if ctx.lang == 'ro' else '4.8'}</b><div><span class="stars" aria-hidden="true">★★★★★</span><small><span class="num">{'1 734' if ctx.lang == 'ro' else '1,734'}</span> {h['reviews']}</small></div></div>
      <dl>
        <dt><svg><use href="#i-clock"/></svg>{h['today_k']}</dt><dd><span class="status js-status"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_line']}</span></span><small>{h['mon']}</small></dd>
        <dt><svg><use href="#i-pin"/></svg>{h['where_k']}</dt><dd>{h['where']}<small>{h['where_s']}</small></dd>
      </dl>
    </aside>
  </div></div>
</section>
<section class="proof" aria-label="{h['v_label']}"><div class="container">'''
    for i, (b, s, src) in enumerate(h['proof']):
        out += f'<div class="proof-item reveal"{f" data-delay=\"{i}\"" if i else ""}><span class="stars" aria-hidden="true">★★★★★</span><b class="num">{b}</b><span>{s}</span><span class="src">{src}</span></div>'
    b, s, src = h['proof4']
    out += f'<div class="proof-item reveal" data-delay="3"><b>{b}</b><span>{s}</span><span class="src">{src}</span></div></div></section>\n'
    # la masă
    out += f'<section class="section" id="la-masa"><div class="container"><div class="section-head reveal"><p class="label">{star()}{h["lm_label"]}</p><h2>{h["lm_h2"]}</h2><p class="lead">{h["lm_lead"]}</p></div><div class="plates">'
    for i, (anchor, file, alt, n, h3, p) in enumerate(h['plates']):
        out += f'<a class="plate reveal"{f" data-delay=\"{i}\"" if i else ""} href="{menu}#{anchor}">{media(ctx, "4x5", file, alt)}<div><span class="n">{n}</span><h3>{h3}</h3><p>{p}</p></div></a>'
    out += '</div></div></section>\n<div class="container"><div class="tiles-row" aria-hidden="true"></div></div>\n'
    # menu resumo
    sec = MENU['sections']
    def col(section, n=5):
        s = next(x for x in sec if x['id'] == section)
        items = ''.join(f'<li><span><span class="name">{d["name"][ctx.lang]}</span><span class="desc">{d["desc"][ctx.lang]}</span></span><span class="price num">{d["price"]}</span></li>' for d in s['dishes'][:n])
        return f'<h3>{s["title"][ctx.lang]}</h3><ul class="menu-list" role="list">{items}</ul>'
    chips = h['chips']
    out += f'''<section class="section" id="meniu"><div class="container">
  <div class="section-head reveal"><p class="label">{star()}{h['m_label']}</p><h2>{h['m_h2']}</h2><p class="lead">{h['m_lead']}</p></div>
  <div class="menu-grid">
    <div class="menu-col reveal">{col('tapas')}</div>
    <div class="menu-col reveal" data-delay="1">{col('principale')}<p style="margin-top:var(--s-5)"><a class="btn btn--ghost" href="{menu}">{h['m_open']}<svg class="arrow"><use href="#i-arrow"/></svg></a></p></div>
    <div class="menu-photo reveal" data-delay="2">{media(ctx, '3x2', 'masa-plina-tapas-de-sus.jpg', h['m_photo_alt'], w=1200, h=800)}
      <div class="menu-filters" aria-label="{h['m_filters']}"><span class="chip"><svg width="16" height="16" style="color:var(--olive)"><use href="#i-leaf"/></svg>{chips[0]}</span><span class="chip"><i>G</i>{chips[1]}</span><span class="chip"><i>L</i>{chips[2]}</span><span class="chip"><i>C</i>{chips[3]}</span><span class="chip"><i>M</i>{chips[4]}</span></div>
    </div>
  </div>
</div></section>
'''
    facts = ''.join(f'<div><b class="num">{a}</b><span>{b}</span></div>' for a, b in h['facts'])
    out += f'''<section class="section section--alt" id="povestea"><div class="container"><div class="story">
  {media(ctx, '4x5', 'sala-scaune-catifea.jpg', h['s_alt'], extra='reveal')}
  <div class="story-text reveal" data-delay="1"><p class="label">{star()}{h['s_label']}</p><h2>{h['s_h2']}</h2><p>{h['s_p1']}</p><p>{h['s_p2']}</p>
    <div class="story-facts">{facts}</div><p><a class="link" href="{story}">{h['s_more']}</a></p></div>
</div></div></section>
'''
    ledger = ''.join(f'<li><span class="glyph"><svg><use href="#{ic}"/></svg></span><span class="what">{w}<small>{sm}</small></span><span class="where">{wh}</span></li>' for ic, w, sm, wh in h['ledger'])
    out += f'''<section class="section" id="din-spania"><div class="container"><div class="origin">
  <div class="section-head reveal" style="margin-bottom:0"><p class="label">{star()}{h['o_label']}</p><h2>{h['o_h2']}</h2><p class="lead">{h['o_lead']}</p></div>
  <ul class="ledger reveal" data-delay="1" role="list">{ledger}</ul>
</div></div></section>
'''
    kinds = ''.join(f'<div class="kind"><svg><use href="#{ic}"/></svg><div><b>{b}</b>{p}</div></div>' for ic, b, p in h['kinds'])
    out += f'''<section class="events" id="evenimente">
  <figure class="media" aria-hidden="true"><svg class="ph" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" viewBox="0 0 1200 600"><defs><linearGradient id="pe" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#143563"/><stop offset=".6" stop-color="#1F4E8C"/><stop offset="1" stop-color="#8E3C1F"/></linearGradient></defs><rect width="1200" height="600" fill="url(#pe)"/><rect width="1200" height="600" fill="url(#az)" opacity=".12"/></svg><img src="{ctx.u('media/foto/masa-lunga-eveniment-terasa.jpg')}" alt="" width="2400" height="1200" loading="lazy" decoding="async" onerror="this.classList.add('is-missing')"></figure>
  <div class="container">
    <div class="reveal"><p class="label">{star()}{h['e_label']}</p><h2 style="margin-top:var(--s-4)">{h['e_h2']}</h2><p class="lead" style="margin-top:var(--s-4)">{h['e_lead']}</p></div>
    <div class="kinds reveal" data-delay="1">{kinds}</div>
    <div class="hero-ctas reveal" data-delay="2" style="margin-top:0"><a class="btn btn--cta" href="{ev}">{h['e_cta']}<svg class="arrow"><use href="#i-arrow"/></svg></a><a class="btn btn--ghost" href="{wa_link(t['wa_event'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>{h['e_wa']}</a></div>
  </div>
</section>
'''
    out += booking_block(ctx, h, ev)
    # reviews + instagram
    revs = ''.join(f'<article class="review reveal"{f" data-delay=\"{i}\"" if i else ""}><span class="stars" aria-hidden="true">★★★★★</span><q>{q}</q><span class="who">{w}</span></article>' for i, (q, w) in enumerate(zip(h['v_ph'], h['v_who'])))
    igs = ''
    cols = ['#C99A3B', '#1F4E8C', '#A84A28', '#5B6B3A', '#143563', '#8E3C1F']
    for i, c in enumerate(cols):
        igs += f'<a class="reveal"{f" data-delay=\"{i % 3}\"" if i % 3 else ""} href="https://www.instagram.com/andalugastrobar" target="_blank" rel="noopener"><figure class="media media--1x1"><svg class="ph" viewBox="0 0 1 1" aria-hidden="true"><rect width="1" height="1" fill="{c}"/></svg><img src="{ctx.u(f"media/foto/ig-0{i + 1}.jpg")}" alt="" width="600" height="600" loading="lazy" decoding="async" onerror="this.classList.add(\'is-missing\')"></figure></a>'
    out += f'''<section class="section section--alt" id="recenzii"><div class="container">
  <div class="section-head reveal"><p class="label">{star()}{h['v_label']}</p><h2>{h['v_h2']}</h2><p class="lead">{h['v_lead']}</p></div>
  <div class="reviews">{revs}</div>
  <p style="margin-top:var(--s-5)"><a class="link" href="https://www.google.com/maps/search/Andalu+Gastrobar+Ia%C8%99i" target="_blank" rel="noopener">{h['v_all']}</a></p>
  <div class="insta" aria-label="Instagram @andalugastrobar">{igs}</div>
  <p style="margin-top:var(--s-4)"><a class="link" href="https://www.instagram.com/andalugastrobar" target="_blank" rel="noopener">{h['ig']}</a></p>
</div></section>
'''
    out += contact_block(ctx, h)
    return out + footer(ctx)


def booking_block(ctx, h, ev, section_id='rezervari'):
    t = ctx.t
    times = ''.join(f'<option value="{x}:00"{" selected" if x == 19 else ""}>{x}:00</option>' for x in range(12, 22))
    ways = ''
    rows = [f'<a class="btn btn--ghost" href="tel:{TEL1}"><svg><use href="#i-phone"/></svg>0752 803 443</a><a class="btn btn--ghost" href="tel:{TEL2}"><svg><use href="#i-phone"/></svg>0740 977 316</a>',
            '<a class="btn btn--ghost" href="https://andalu.poloniq.ro/" target="_blank" rel="noopener">Poloniq</a><a class="btn btn--ghost" href="https://bookingham.ro/iasi/restaurante/andalu-gastrobar/1562" target="_blank" rel="noopener">Bookingham</a>', None]
    for i, ((b, p), row) in enumerate(zip(h['ways'], rows)):
        extra = f' <span class="tbc">{h["ways_tbc"]}</span>' if row is None else ''
        ways += f'<div class="way"><span class="n num">0{i + 1}</span><div><b>{b}</b><p>{p}{extra}</p>{f"<div class=\"row\">{row}</div>" if row else ""}</div></div>'
    return f'''<section class="section" id="{section_id}"><div class="container">
  <div class="section-head reveal"><p class="label">{star()}{h['r_label']}</p><h2>{h['r_h2']}</h2><p class="lead">{h['r_lead']}</p></div>
  <div class="book">
    <form class="book-form reveal" id="bookForm" novalidate>
      <h3>{h['f_title']}</h3>
      <div class="fields">
        <div class="field"><label for="bDate">{h['f_date']}</label><input id="bDate" name="data" type="date" required></div>
        <div class="field"><label for="bTime">{h['f_time']}</label><select id="bTime" name="ora" required>{times}</select></div>
        <div class="field"><label for="bPeople">{h['f_people']}</label><input id="bPeople" name="persoane" type="number" min="1" max="12" value="2" inputmode="numeric" required></div>
        <div class="field"><label for="bName">{h['f_name']}</label><input id="bName" name="nume" type="text" autocomplete="name" placeholder="{h['f_name_ph']}" required></div>
      </div>
      <button class="btn btn--cta" type="submit"><svg><use href="#i-wa"/></svg>{h['f_send']}</button>
      <p class="note">{h['f_note'].replace('{ev}', ev)}</p>
    </form>
    <div class="ways reveal" data-delay="1">{ways}</div>
  </div>
</div></section>
'''


def contact_block(ctx, h):
    t = ctx.t
    amen = ''.join(f'<span class="chip">{a}</span>' for a in h['amen'])
    return f'''<section class="section" id="contact"><div class="container"><div class="info">
  <div class="reveal"><p class="label">{star()}{h['c_label']}</p><h2 style="margin-top:var(--s-4);font-size:var(--fs-h2);line-height:1.02">{h['c_h2']}</h2>
    <dl style="margin-top:var(--s-6)"><dt>{h['c_addr']}</dt><dd>Strada Teodor Codrescu 6, Iași 700481</dd><dt>{h['c_hours']}</dt><dd class="num">{h['c_hours_v']}</dd>
      <dt>{h['c_tel']}</dt><dd><a class="link num" href="tel:{TEL1}">0752 803 443</a> · <a class="link num" href="tel:{TEL2}">0740 977 316</a></dd><dt>{h['c_mail']}</dt><dd><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></dd></dl>
    <div class="amen" aria-label="Facilities">{amen}</div></div>
  <div class="map reveal" data-delay="1" aria-label="{h['map_aria']}">
    <svg viewBox="0 0 600 400" aria-hidden="true"><defs><pattern id="mg" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0v40" fill="none" stroke="currentColor" stroke-opacity=".12"/></pattern></defs><rect width="600" height="400" fill="url(#mg)" style="color:var(--accent)"/>
      <path d="M60 380 C 160 300, 220 240, 330 200 S 520 90, 580 40" fill="none" stroke="var(--accent)" stroke-width="6" stroke-opacity=".35" stroke-linecap="round"/><path d="M0 150 C 120 170, 230 160, 336 200 S 470 300, 600 320" fill="none" stroke="var(--accent)" stroke-width="4" stroke-opacity=".25" stroke-linecap="round"/>
      <ellipse cx="470" cy="120" rx="80" ry="55" fill="var(--olive)" fill-opacity=".22"/><text x="470" y="124" text-anchor="middle" font-family="Instrument Sans, sans-serif" font-size="12" letter-spacing="1.5" fill="var(--ink-2)">{h['botanic']}</text>
      <text x="110" y="330" font-family="Instrument Serif, serif" font-style="italic" font-size="22" fill="var(--ink-2)">Copou</text><text x="330" y="236" font-family="Instrument Sans, sans-serif" font-size="11" letter-spacing="1.5" fill="var(--ink-3)">STR. TEODOR CODRESCU</text></svg>
    <span class="pin"><svg><use href="#i-pin-fill"/></svg></span>
    <a class="btn btn--cta maplink" href="https://www.google.com/maps/search/?api=1&query=Andalu+Gastrobar+Strada+Teodor+Codrescu+6+Ia%C8%99i" target="_blank" rel="noopener">{h['map_btn']}</a>
  </div>
</div></div></section>
'''


# ----------------------------------------------------------------------------- MENIU
MENU_T = {
'ro': dict(title='Meniu · Andalu Gastrobar, Iași', desc='Meniul complet al Andalu Gastrobar din Copou, Iași: tapas, paella cu orez din Valencia, carne și pește la grătar, deserturi spaniole, sangria și vinuri. Alergeni marcați, filtru vegetarian.',
  label='Meniu', h1='Tapas de împărțit, paella pentru doi, <em>sangria</em> pentru masă.', lead='Meniul complet, pe telefon, cu prețuri și gramaje. Alergenii sunt marcați la fiecare preparat; apasă un filtru ca să vezi doar ce poți mânca.',
  filters='Filtre', legend_t='Alergeni', note='Prețuri în lei, din meniul digital al restaurantului (octombrie 2026); meniul de la masă are prioritate. Alergenii sunt marcați după descrierea fiecărui preparat, nu sunt lista legală completă: spuneți-ne la masă orice alergie sau intoleranță, adaptăm ce se poate.',
  fav='favorit', tbc='preț în meniu', vegf='Doar vegetarian', excl='Fără'),
'en': dict(title='Menu · Andalu Gastrobar, Iași', desc='The full menu of Andalu Gastrobar in Copou, Iași: tapas, paella with Valencian rice, grilled meat and fish, Spanish desserts, sangria and wines. Allergens marked, vegetarian filter.',
  label='Menu', h1='Tapas to share, paella for two, <em>sangria</em> for the table.', lead='The full menu on your phone, with prices and portion sizes. Allergens are marked on every dish; tap a filter to see only what you can eat.',
  filters='Filters', legend_t='Allergens', note='Prices in lei, from the restaurant\'s digital menu (October 2026); the menu at the table prevails. Allergens follow each dish\'s description and are not the full legal list: tell us about any allergy or intolerance at the table, we adapt what we can.',
  fav='favourite', tbc='price on the menu', vegf='Vegetarian only', excl='Without'),
}
ALLERGENS = {'glu': ('G', {'ro': 'Gluten', 'en': 'Gluten'}), 'lac': ('L', {'ro': 'Lactoză', 'en': 'Dairy'}), 'cru': ('C', {'ro': 'Crustacee', 'en': 'Crustaceans'}),
             'mol': ('M', {'ro': 'Moluște', 'en': 'Molluscs'}), 'pes': ('P', {'ro': 'Pește', 'en': 'Fish'}), 'ou': ('O', {'ro': 'Ouă', 'en': 'Eggs'}),
             'nuc': ('N', {'ro': 'Nuci', 'en': 'Nuts'}), 'sul': ('S', {'ro': 'Sulfiți', 'en': 'Sulphites'})}


def menu_page(ctx):
    t, m = ctx.t, MENU_T[ctx.lang]
    out = head(ctx, m['title'], m['desc'], restaurant_ld(ctx) | {"@type": "Restaurant"}) + header(ctx, False)
    out += page_hero(ctx, m['label'], m['h1'], m['lead'], crumb=m['label'])
    nav = ''.join(f'<a href="#{s["id"]}">{s["title"][ctx.lang]}</a>' for s in MENU['sections'])
    out += f'<nav class="menu-nav" aria-label="{m["label"]}"><div class="container">{nav}</div></nav>\n<div class="container">'
    chips = f'<button class="chip" type="button" aria-pressed="false" data-f="veg"><svg width="16" height="16" style="color:var(--olive)"><use href="#i-leaf"/></svg>{m["vegf"]}</button>'
    chips += ''.join(f'<button class="chip" type="button" aria-pressed="false" data-f="{k}"><i>{l}</i>{m["excl"]} {n[ctx.lang].lower()}</button>' for k, (l, n) in ALLERGENS.items())
    out += f'<div class="filters" role="group" aria-label="{m["filters"]}">{chips}</div>'
    legend = ''.join(f'<span><i>{l}</i>{n[ctx.lang]}</span>' for l, n in ALLERGENS.values())
    out += f'<div class="legend" aria-label="{m["legend_t"]}"><span><i style="color:var(--olive);border-color:var(--olive)">V</i>{"Vegetarian"}</span>{legend}</div>'
    for s in MENU['sections']:
        dishes = ''
        for d in s['dishes']:
            tags = d.get('tags', [])
            tg = ''.join(f'<i class="veg" title="Vegetarian">V</i>' if x == 'veg' else f'<i title="{ALLERGENS[x][1][ctx.lang]}">{ALLERGENS[x][0]}</i>' for x in tags)
            fav = f'<span class="fav">{m["fav"]}</span>' if d.get('fav') else ''
            price = f'<span class="price">{d["price"]}</span>' if d.get('price') else f'<span class="price tbc">{m["tbc"]}</span>'
            wt = f'<span class="wt num">{d["w"]}</span>' if d.get('w') else ''
            dishes += f'<div class="dish" data-tags="{" ".join(tags)}"><div><span class="name">{d["name"][ctx.lang]}{wt}{fav}</span><span class="desc">{d["desc"][ctx.lang]}</span>{f"<div class=\"tags\">{tg}</div>" if tg else ""}</div>{price}</div>'
        out += f'<section class="menu-section" id="{s["id"]}"><div class="menu-section-head reveal"><p class="label">{star()}{s["kicker"][ctx.lang]}</p><h2>{s["title"][ctx.lang]}</h2><p>{s["lead"][ctx.lang]}</p></div><div class="dishes">{dishes}</div></section>'
    out += f'<p class="menu-note">{m["note"]}</p></div>\n'
    return out + footer(ctx)


# ----------------------------------------------------------------------------- REZERVĂRI
RES_T = {
'ro': dict(title='Rezervări · Andalu Gastrobar, Iași', desc='Rezervă o masă la Andalu Gastrobar, Copou, Iași: pe WhatsApp cu confirmare, la telefon sau pe Poloniq și Bookingham. Marți–sâmbătă 12–22, duminică 12–20.',
  label='Rezervări', h1='O masă la Andalu, <em>confirmată</em> în același chat.', lead='Trimiți pe WhatsApp data, ora și numărul de persoane. Noi confirmăm masa în câteva minute, în orele de program, sau te sunăm dacă e vreo problemă.',
  faq_t='Întrebări care revin', faq=[('Trebuie să rezerv?', 'Vineri și sâmbătă seara, da: sala se umple. În restul săptămânii, de obicei găsim loc, dar o rezervare scurtă pe WhatsApp ne ajută să vă ținem masa.'),
        ('Grupuri mari?', 'Până la 12 persoane rezervați direct aici. Peste 12, sau dacă vreți un meniu fix, cereți o ofertă pe pagina de evenimente.'),
        ('Terasa?', 'Terasa are 150 m² și se rezervă la fel. Spuneți în mesaj „terasă” și o notăm, în funcție de vreme.'),
        ('Copii?', 'Avem scaune pentru copii. Spuneți câți copii vin, ca să pregătim masa.'),
        ('Întârzieri?', 'Ținem masa 15 minute după ora rezervată. Dacă întârziați mai mult, scrieți-ne pe același chat și o reținem dacă putem.')]),
'en': dict(title='Reservations · Andalu Gastrobar, Iași', desc='Book a table at Andalu Gastrobar, Copou, Iași: on WhatsApp with confirmation, by phone or on Poloniq and Bookingham. Tuesday–Saturday 12–22, Sunday 12–20.',
  label='Reservations', h1='A table at Andalu, <em>confirmed</em> in the same chat.', lead='Send the date, time and number of guests on WhatsApp. We confirm the table within minutes during opening hours, or call you if there is a problem.',
  faq_t='Questions that come up', faq=[('Do I need to book?', 'Friday and Saturday evenings, yes: the room fills up. The rest of the week we usually find space, but a quick WhatsApp booking lets us hold your table.'),
        ('Large groups?', 'Up to 12 people, book right here. Over 12, or if you want a set menu, request a quote on the events page.'),
        ('The terrace?', 'The terrace is 150 m² and is booked the same way. Write "terrace" in the message and we note it, weather permitting.'),
        ('Children?', 'We have high chairs. Tell us how many children are coming so we can set the table.'),
        ('Running late?', 'We hold the table for 15 minutes after the booked time. If you are later than that, message us on the same chat and we keep it if we can.')]),
}


def reservations_page(ctx):
    t, r = ctx.t, RES_T[ctx.lang]
    h = HOME[ctx.lang]
    ev = ctx.p(t['nav'][2][0])
    out = head(ctx, r['title'], r['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, r['label'], r['h1'], r['lead'], crumb=r['label'])
    out += booking_block(ctx, h, ev, section_id='rezervari')
    faq = ''.join(f'<div class="step reveal"><h3>{q}</h3><p>{a}</p></div>' for q, a in r['faq'])
    out += f'<section class="section section--alt"><div class="container"><div class="section-head reveal"><p class="label">{star()}{r["faq_t"]}</p></div><div class="steps" style="margin-top:0">{faq}</div></div></section>\n'
    return out + footer(ctx)


# ----------------------------------------------------------------------------- EVENIMENTE
EV_T = {
'ro': dict(title='Evenimente & catering · Andalu Gastrobar, Iași', desc='Nunți, botezuri, aniversări și evenimente de firmă la Andalu Gastrobar, Copou, Iași: sală de 220 m², terasă de 150 m², până la 100 de persoane, catering cu tapas și paella la locația voastră.',
  label='Evenimente &amp; catering', h1='O masă lungă, a voastră: <em>la noi</em> sau la voi.', lead='Sala de 220 m², terasa de 150 m², până la 100 de persoane. Sau echipa noastră gătește paella și tapas la locația voastră. Ne scrieți ce sărbătoriți, noi răspundem cu o propunere.',
  packs_t='Trei feluri de a o face', packs=[('Tapas', 'Masa de împărțit', ['Platouri de tapas în mijlocul mesei', 'Jamón, brânzeturi, pimientos, bravas', 'Sangria Alegria la carafă', 'Pentru aniversări și evenimente de firmă'], 'preț de persoană la ofertă'),
        ('Paella', 'Paella pentru toată masa', ['Tapas de început', 'Paella gătită în tigăi mari, la vedere', 'Crema catalana la final', 'Pentru botezuri, nunți mici, prânzuri de echipă'], 'preț de persoană la ofertă'),
        ('Catering', 'La locația voastră', ['Echipa noastră vine cu tigăile', 'Tapas reci și calde, paella la fața locului', 'Veselă și personal la cerere', 'Pentru nunți, petreceri în grădină, birouri'], 'ofertă după vizită')],
  feat=1, steps_t='Cum decurge', steps=[('Ne scrieți', 'Ce sărbătoriți, câți sunteți, când. Pe formular sau pe WhatsApp.'), ('Răspundem', 'În orele de program, cu o propunere de meniu și un preț de persoană.'), ('Degustați', 'Dacă vreți, veniți la o masă să încercați meniul înainte.'), ('Confirmăm', 'Cu un avans și numărul final de persoane, cu câteva zile înainte.')],
  form_t='Cereți o ofertă', f_type='Tipul evenimentului', types=['Nuntă', 'Botez', 'Aniversare', 'Eveniment de firmă', 'Catering la locația noastră', 'Altceva'], f_people='Persoane', f_date='Data (aproximativă)', f_name='Numele', f_phone='Telefon', f_msg='Ce ar trebui să știm', f_msg_ph='Meniu, alergii, program, locație…',
  f_consent='Sunt de acord ca datele din formular să fie folosite doar pentru a răspunde la această cerere. <a href="{priv}">Confidențialitate</a>.', f_send='Trimite cererea', f_wa='Sau trimite pe WhatsApp',
  f_note='Formularul ajunge pe emailul restaurantului. Răspundem în orele de program.',
  side_t='Ce aveți la dispoziție', side=[('220 m² interior', 'Sală renovată, mese care se unesc pentru grupuri.'), ('150 m² terasă', 'Pentru lunile calde: aperitiv afară, masa înăuntru sau totul pe terasă.'), ('Până la 100 de persoane', 'Interior și terasă, la mese sau cocktail în picioare.'), ('Parcare, Wi-Fi, scaune pentru copii', 'Și acces cu scaun rulant.')]),
'en': dict(title='Events & catering · Andalu Gastrobar, Iași', desc='Weddings, christenings, birthdays and corporate events at Andalu Gastrobar, Copou, Iași: 220 m² dining room, 150 m² terrace, up to 100 guests, tapas and paella catering at your venue.',
  label='Events &amp; catering', h1='One long table, yours: <em>at ours</em> or at yours.', lead='A 220 m² dining room, a 150 m² terrace, up to 100 guests. Or our team cooks paella and tapas at your venue. Tell us what you are celebrating and we reply with a proposal.',
  packs_t='Three ways to do it', packs=[('Tapas', 'The sharing table', ['Tapas platters in the middle of the table', 'Jamón, cheeses, pimientos, bravas', 'Sangria Alegria by the jug', 'For birthdays and corporate events'], 'price per person on request'),
        ('Paella', 'Paella for the whole table', ['Tapas to start', 'Paella cooked in big pans, in view', 'Crema catalana to finish', 'For christenings, small weddings, team lunches'], 'price per person on request'),
        ('Catering', 'At your venue', ['Our team comes with the pans', 'Cold and hot tapas, paella on site', 'Tableware and staff on request', 'For weddings, garden parties, offices'], 'quote after a visit')],
  feat=1, steps_t='How it goes', steps=[('You write to us', 'What you are celebrating, how many, when. On the form or on WhatsApp.'), ('We reply', 'During opening hours, with a menu proposal and a price per person.'), ('You taste', 'If you like, come for a meal and try the menu first.'), ('We confirm', 'With a deposit and the final headcount, a few days before.')],
  form_t='Request a quote', f_type='Type of event', types=['Wedding', 'Christening', 'Birthday', 'Corporate event', 'Catering at our venue', 'Something else'], f_people='Guests', f_date='Date (approximate)', f_name='Name', f_phone='Phone', f_msg='What we should know', f_msg_ph='Menu, allergies, timing, venue…',
  f_consent='I agree that the details in this form are used only to answer this request. <a href="{priv}">Privacy</a>.', f_send='Send the request', f_wa='Or send on WhatsApp',
  f_note='The form goes to the restaurant\'s email. We reply during opening hours.',
  side_t='What you have', side=[('220 m² indoors', 'A renovated dining room, tables that join up for groups.'), ('150 m² terrace', 'For the warm months: aperitif outside, dinner inside, or everything on the terrace.'), ('Up to 100 guests', 'Indoors and terrace, seated or standing cocktail.'), ('Parking, Wi-Fi, high chairs', 'And wheelchair access.')]),
}


def events_page(ctx):
    t, e = ctx.t, EV_T[ctx.lang]
    priv = ctx.p('confidentialitate' if ctx.lang == 'ro' else 'privacy')
    thanks = ctx.p('multumim' if ctx.lang == 'ro' else 'thanks')
    out = head(ctx, e['title'], e['desc'], restaurant_ld(ctx) | {"@type": "Restaurant"}, theme='#15130F') + header(ctx, False)
    out += page_hero(ctx, e['label'], e['h1'], e['lead'], dark=True, crumb=e['label'].replace('&amp;', '&'))
    packs = ''
    for i, (k, h3, items, pp) in enumerate(e['packs']):
        li = ''.join(f'<li>{x}</li>' for x in items)
        packs += f'<div class="pack reveal{" is-featured" if i == e["feat"] else ""}"{f" data-delay=\"{i}\"" if i else ""}><span class="k">0{i + 1} · {k}</span><h3>{h3}</h3><ul>{li}</ul><p class="pp"><small>{pp}</small></p></div>'
    out += f'<section class="section"><div class="container"><div class="section-head reveal"><p class="label">{star()}{e["packs_t"]}</p></div><div class="packs" style="margin-top:0">{packs}</div></div></section>\n'
    steps = ''.join(f'<div class="step reveal"{f" data-delay=\"{i}\"" if i else ""}><b class="num">0{i + 1}</b><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(e['steps']))
    out += f'<section class="section section--alt"><div class="container"><div class="section-head reveal"><p class="label">{star()}{e["steps_t"]}</p></div><div class="steps" style="margin-top:0">{steps}</div></div></section>\n'
    types = ''.join(f'<option>{x}</option>' for x in e['types'])
    side = ''.join(f'<div class="way"><span class="n num">0{i + 1}</span><div><b>{a}</b><p>{b}</p></div></div>' for i, (a, b) in enumerate(e['side']))
    form_name = 'eveniment' if ctx.lang == 'ro' else 'event'
    out += f'''<section class="section" id="oferta"><div class="container"><div class="split">
  <form class="form reveal" id="eventForm" name="{form_name}" method="POST" action="{thanks}" data-netlify="true" netlify-honeypot="website">
    <input type="hidden" name="form-name" value="{form_name}"><p class="sr-only"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></p>
    <h3>{e['form_t']}</h3>
    <div class="fields">
      <div class="field"><label for="eType">{e['f_type']}</label><select id="eType" name="tip">{types}</select></div>
      <div class="field"><label for="ePeople">{e['f_people']}</label><input id="ePeople" name="persoane" type="number" min="1" max="300" inputmode="numeric" required></div>
      <div class="field"><label for="eDate">{e['f_date']}</label><input id="eDate" name="data" type="date"></div>
      <div class="field"><label for="ePhone">{e['f_phone']}</label><input id="ePhone" name="telefon" type="tel" autocomplete="tel" required></div>
      <div class="field field--full"><label for="eName">{e['f_name']}</label><input id="eName" name="nume" type="text" autocomplete="name" required></div>
      <div class="field field--full"><label for="eMsg">{e['f_msg']}</label><textarea id="eMsg" name="mesaj" placeholder="{e['f_msg_ph']}"></textarea></div>
    </div>
    <label class="check"><input type="checkbox" name="consimtamant" required><span>{e['f_consent'].replace('{priv}', priv)}</span></label>
    <div class="hero-ctas" style="margin-top:0"><button class="btn btn--cta" type="submit">{e['f_send']}<svg class="arrow"><use href="#i-arrow"/></svg></button><button class="btn btn--wa js-ev-wa" type="button"><svg><use href="#i-wa"/></svg>{e['f_wa']}</button></div>
    <p class="note" style="font-size:var(--fs-small);color:var(--ink-2)">{e['f_note']}</p>
  </form>
  <div class="reveal" data-delay="1"><p class="label">{star()}{e['side_t']}</p><div class="ways" style="margin-top:var(--s-5)">{side}</div>
    {media(ctx, '3x2', 'masa-lunga-eveniment-terasa.jpg', 'Masă lungă pe terasă' if ctx.lang == 'ro' else 'Long table on the terrace', w=1200, h=800, extra='reveal')}</div>
</div></div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- POVESTEA
ST_T = {
'ro': dict(title='Povestea noastră · Andalu Gastrobar, Iași', desc='Ioana și Daniel Luca, un cuplu din Iași, au trăit peste zece ani la Madrid și au deschis Andalu Gastrobar în Copou în 2019: ingrediente din Spania, bucătar format în Spania și Andorra, gazde în sală.',
  label='Povestea noastră', h1='Am plecat din Iași. Ne-am întors cu <em>Spania</em> în bagaje.',
  lead='Ioana și Daniel Luca. Peste zece ani la Madrid, o idee venită într-o vacanță acasă, un restaurant deschis în 2019 pe Strada Teodor Codrescu.',
  chapters=[('2016', 'Ideea, într-o vizită acasă', 'Locuiam la Madrid de ani buni. Daniel lucra în restaurante, Ioana într-o companie din domeniul sănătății. Într-o vacanță la Iași ne-am dat seama ce ne lipsea aici: o masă ca acolo, lungă, cu farfurii de împărțit și fără grabă. Ideea a rămas.'),
            ('2018', 'Întoarcerea', 'La sfârșitul lui 2018 ne-am mutat înapoi. Am găsit spațiul din Copou, lângă Grădina Botanică, și am început lucrările. Numele a venit din întâmplare, de la un magazin de ceramică, în timpul renovării. Andaluzia a rămas în el.'),
            ('2019', 'Deschiderea', 'Am deschis Andalu în 2019, cu o parte din investiție prin programul pentru diaspora. Orezul pentru paella vine din Valencia, jamónul, brânzeturile, uleiul și vinul din Spania. Bucătarul e român, format în bucătării din Spania și Andorra.'),
            ('Azi', 'Gazde în sală', 'Suntem 16 oameni în echipă. Ne găsiți în sală, la mese, ca în restaurantele de familie de acolo. Am renovat sala; urmează bucătăria. Oaspeții noștri sunt oameni pasionați de mâncare, și asta ne ține.')],
  quote='„Spaniolii știu să își trăiască viața.”', quote_who='Ioana Luca', values_t='Ce nu negociem', values=[('Ingredientele', 'Cele mai multe vin din Spania. O paella fără orezul potrivit e alt fel de mâncare.'), ('Timpul la masă', 'Nu grăbim pe nimeni. Sobremesa face parte din masă.'), ('Gazdele', 'Suntem în sală. Dacă ceva nu e bine, ne spuneți nouă, direct.')],
  cta='Rezervă o masă', cta2='Vezi meniul', src='Faptele din această pagină vin din interviurile acordate de Ioana și Daniel Luca publicațiilor Ziarul Financiar și BZI.'),
'en': dict(title='Our story · Andalu Gastrobar, Iași', desc='Ioana and Daniel Luca, a couple from Iași, lived in Madrid for over ten years and opened Andalu Gastrobar in Copou in 2019: ingredients from Spain, a chef trained in Spain and Andorra, hosts on the floor.',
  label='Our story', h1='We left Iași. We came back with <em>Spain</em> in our luggage.',
  lead='Ioana and Daniel Luca. More than ten years in Madrid, an idea that came on a holiday home, a restaurant opened in 2019 on Strada Teodor Codrescu.',
  chapters=[('2016', 'The idea, on a visit home', 'We had lived in Madrid for years. Daniel worked in restaurants, Ioana for a healthcare company. On a holiday in Iași we realised what we missed here: a table like over there, long, with plates to share and no hurry. The idea stayed.'),
            ('2018', 'Coming back', 'At the end of 2018 we moved back. We found the space in Copou, next to the Botanical Garden, and started the works. The name came by chance, from a ceramics shop, during the renovation. Andalusia stayed in it.'),
            ('2019', 'Opening', 'We opened Andalu in 2019, part of the investment through the diaspora start-up programme. The paella rice comes from Valencia; the jamón, cheeses, oil and wine from Spain. The chef is Romanian, trained in kitchens in Spain and Andorra.'),
            ('Today', 'Hosts on the floor', 'We are a team of 16. You will find us on the floor, at the tables, like the family-run places over there. We renovated the dining room; the kitchen is next. Our guests are people who love food, and that keeps us going.')],
  quote='"The Spanish know how to live their lives."', quote_who='Ioana Luca', values_t='What we do not negotiate', values=[('The ingredients', 'Most come from Spain. A paella without the right rice is a different dish.'), ('Time at the table', 'We hurry no one. The sobremesa is part of the meal.'), ('The hosts', 'We are on the floor. If something is not right, tell us, directly.')],
  cta='Book a table', cta2='See the menu', src='The facts on this page come from interviews Ioana and Daniel Luca gave to Ziarul Financiar and BZI.'),
}


def story_page(ctx):
    t, s = ctx.t, ST_T[ctx.lang]
    out = head(ctx, s['title'], s['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, s['label'], s['h1'], s['lead'], crumb=s['label'])
    out += f'<section class="section"><div class="container"><div class="split split--rev">{media(ctx, "4x5", "sala-scaune-catifea.jpg", HOME[ctx.lang]["s_alt"], extra="reveal")}<div class="ways reveal" data-delay="1" style="gap:0">'
    for i, (y, h3, p) in enumerate(s['chapters']):
        out += f'<div class="way"><span class="n num">{y}</span><div><b>{h3}</b><p style="font-size:var(--fs-body)">{p}</p></div></div>'
    out += '</div></div></div></section>\n'
    vals = ''.join(f'<div class="step reveal"{f" data-delay=\"{i}\"" if i else ""}><b class="num">0{i + 1}</b><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(s['values']))
    out += f'''<section class="section section--alt"><div class="container">
  <blockquote class="reveal" style="margin:0 0 var(--s-8);max-width:30ch"><p style="font-family:var(--font-display);font-size:var(--fs-h2);line-height:1.05;font-style:italic">{s['quote']}</p><footer class="label" style="margin-top:var(--s-4)">{s['quote_who']}</footer></blockquote>
  <div class="section-head reveal"><p class="label">{star()}{s['values_t']}</p></div>
  <div class="steps" style="margin-top:0;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">{vals}</div>
  <div class="hero-ctas reveal" style="margin-top:var(--s-8)"><a class="btn btn--cta" href="{ctx.p(t['nav'][1][0])}">{s['cta']}<svg class="arrow"><use href="#i-arrow"/></svg></a><a class="btn btn--ghost" href="{ctx.p(t['nav'][0][0])}">{s['cta2']}</a></div>
  <p style="margin-top:var(--s-7);font-size:var(--fs-small);color:var(--ink-3);max-width:60ch">{s['src']}</p>
</div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- GALERIE
GA_T = {
'ro': dict(title='Galerie · Andalu Gastrobar, Iași', desc='Fotografii de la Andalu Gastrobar, Copou, Iași: paella, tapas, sangria, sala și terasa.', label='Galerie', h1='Sala, terasa, <em>farfuriile</em>.', lead='Sala cu scaune de catifea, terasa cu iederă și farfuriile. Fotografii de pe Instagram și Facebook-ul restaurantului.',
  tabs=[('all', 'Toate'), ('food', 'Farfurii'), ('room', 'Sala'), ('terrace', 'Terasa')], close='Închide'),
'en': dict(title='Gallery · Andalu Gastrobar, Iași', desc='Photos from Andalu Gastrobar, Copou, Iași: paella, tapas, sangria, the dining room and the terrace.', label='Gallery', h1='The room, the terrace, <em>the plates</em>.', lead='The velvet-chair dining room, the ivy terrace and the plates. Photos from the restaurant\'s Instagram and Facebook.',
  tabs=[('all', 'All'), ('food', 'Plates'), ('room', 'The room'), ('terrace', 'Terrace')], close='Close'),
}
GALLERY = [('food', 'paella-fructe-de-mare.jpg', 'Paella cu fructe de mare / Seafood paella', 'is-wide', '3x2', 1600, 1067), ('food', 'vieiras-1x1.jpg', 'Scoici Saint-Jacques / Scallops', '', '1x1', 1000, 1000), ('room', 'sala-intrare.jpg', 'Intrarea și desenele de pe perete / The entrance and the wall drawings', 'is-tall', '4x5', 1200, 1500),
           ('food', 'sangria-alba-1x1.jpg', 'White sangria', '', '1x1', 600, 600), ('terrace', 'terasa-vara.jpg', 'Terasa, vara / The terrace in summer', 'is-wide', '3x2', 1600, 1067), ('room', 'sala-scaune-1x1.jpg', 'Scaunele de catifea / The velvet chairs', '', '1x1', 1000, 1000),
           ('food', 'secreto-iberico.jpg', 'Secreto ibérico', '', '1x1', 600, 600), ('food', 'crochete.jpg', 'Crochete / Croquettes', '', '1x1', 1000, 1000), ('room', 'bar-andalu.jpg', 'Jamónul, la bar / The jamón at the bar', 'is-wide', '3x2', 1440, 960),
           ('food', 'caracatita-la-gratar.jpg', 'Caracatiță pe jar / Charcoal-grilled octopus', '', '1x1', 1200, 1200), ('terrace', 'terasa-acoperita.jpg', 'Terasa acoperită / The covered terrace', 'is-tall', '4x5', 1200, 1500), ('room', 'sala-lunga.jpg', 'Masa lungă din sală / The long table', 'is-wide', '3x2', 1440, 960)]


def gallery_page(ctx):
    t, g = ctx.t, GA_T[ctx.lang]
    out = head(ctx, g['title'], g['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, g['label'], g['h1'], g['lead'], crumb=g['label'])
    tabs = ''.join(f'<button class="chip" type="button" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in g['tabs'])
    items = ''.join(f'<figure class="g {cls} reveal" data-cat="{cat}">{media(ctx, ratio, f, alt, w=w, h=h).replace("<figure class=", "<div class=").replace("</figure>", "</div>")}</figure>' for cat, f, alt, cls, ratio, w, h in GALLERY)
    out += f'''<section class="section"><div class="container"><div class="gtabs" role="group">{tabs}</div><div class="gallery">{items}</div></div></section>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="{g['label']}"><button class="icon-btn close" type="button" aria-label="{g['close']}"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button><img src="" alt=""><p class="cap"></p></div>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- CONTACT
CO_T = {
'ro': dict(title='Contact și cum ajungi · Andalu Gastrobar, Iași', desc='Andalu Gastrobar, Strada Teodor Codrescu 6, Copou, Iași, lângă Grădina Botanică. Telefon +40 752 803 443, WhatsApp, email. Program marți–sâmbătă 12–22, duminică 12–20.',
  label='Contact', h1='În Copou, la cinci minute de <em>Grădina Botanică</em>.', lead='Strada Teodor Codrescu 6. Parcare pe stradă, terasă vara, Wi-Fi tot anul. Cel mai rapid răspuns: WhatsApp.',
  hours_t='Program', addr_t='Adresă', talk_t='Vorbește cu noi', map_t='Harta', map_consent='Harta Google se încarcă doar după ce apeși. Până atunci nu se trimite nimic către Google.', map_load='Încarcă harta', map_open='Deschide în Google Maps',
  how_t='Cum ajungi', how=[('i-pin', 'Pe jos', 'Din centru, pe Bulevardul Carol I spre Copou, 15–20 de minute. De la Grădina Botanică, 5 minute.'), ('i-clock', 'Cu mașina', 'Parcare pe stradă în zonă, gratuită. Pe Teodor Codrescu se intră din Bulevardul Carol I.'), ('i-arrow', 'Transport public', 'Autobuzele și tramvaiele spre Copou opresc pe Carol I; de acolo, câteva minute pe jos.')],
  amen_t='Facilități'),
'en': dict(title='Contact and how to get here · Andalu Gastrobar, Iași', desc='Andalu Gastrobar, Strada Teodor Codrescu 6, Copou, Iași, next to the Botanical Garden. Phone +40 752 803 443, WhatsApp, email. Open Tuesday–Saturday 12–22, Sunday 12–20.',
  label='Contact', h1='In Copou, five minutes from the <em>Botanical Garden</em>.', lead='Strada Teodor Codrescu 6. Street parking, terrace in summer, Wi-Fi all year. Fastest reply: WhatsApp.',
  hours_t='Opening hours', addr_t='Address', talk_t='Talk to us', map_t='Map', map_consent='The Google map loads only after you tap. Until then nothing is sent to Google.', map_load='Load the map', map_open='Open in Google Maps',
  how_t='How to get here', how=[('i-pin', 'On foot', 'From the centre, up Bulevardul Carol I towards Copou, 15–20 minutes. From the Botanical Garden, 5 minutes.'), ('i-clock', 'By car', 'Free street parking in the area. Teodor Codrescu is entered from Bulevardul Carol I.'), ('i-arrow', 'Public transport', 'Buses and trams to Copou stop on Carol I; from there, a few minutes on foot.')],
  amen_t='Facilities'),
}
HOURS = {0: (12, 20), 1: None, 2: (12, 22), 3: (12, 22), 4: (12, 22), 5: (12, 22), 6: (12, 22)}


def contact_page(ctx):
    t, c = ctx.t, CO_T[ctx.lang]
    h = HOME[ctx.lang]
    out = head(ctx, c['title'], c['desc'], restaurant_ld(ctx)) + header(ctx, False)
    out += page_hero(ctx, c['label'], c['h1'], c['lead'], crumb=c['label'])
    hours = ''
    for d in [1, 2, 3, 4, 5, 6, 0]:
        v = HOURS[d]
        hours += f'<li data-day="{d}"><span>{t["days"][d]}</span><span class="num{" closed" if not v else ""}">{f"{v[0]}:00–{v[1]}:00" if v else t["closed"]}</span></li>'
    amen = ''.join(f'<span class="chip">{a}</span>' for a in h['amen'])
    how = ''.join(f'<div><svg><use href="#{ic}"/></svg><div><b>{a}</b>{b}</div></div>' for ic, a, b in c['how'])
    maps_src = 'https://www.google.com/maps?q=Andalu+Gastrobar,+Strada+Teodor+Codrescu+6,+Iasi&output=embed'
    out += f'''<section class="section"><div class="container"><div class="contact-grid">
  <div class="reveal">
    <p class="label">{star()}{c['hours_t']}</p>
    <p class="status js-status" style="margin-top:var(--s-3);font-weight:600"><i aria-hidden="true"></i><span class="js-status-text">{t['hours_line']}</span></p>
    <ul class="hours">{hours}</ul>
    <p class="label" style="margin-top:var(--s-7)">{star()}{c['addr_t']}</p>
    <p style="margin-top:var(--s-3)">Strada Teodor Codrescu 6<br>Iași 700481, România</p>
    <p class="label" style="margin-top:var(--s-7)">{star()}{c['talk_t']}</p>
    <div class="hero-ctas" style="margin-top:var(--s-3)"><a class="btn btn--cta" href="{wa_link(t['wa_text'])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a><a class="btn btn--ghost" href="tel:{TEL1}"><svg><use href="#i-phone"/></svg>0752 803 443</a><a class="btn btn--ghost" href="tel:{TEL2}"><svg><use href="#i-phone"/></svg>0740 977 316</a></div>
    <p style="margin-top:var(--s-4)"><a class="link" href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p style="margin-top:var(--s-3)"><a class="link" href="https://www.instagram.com/andalugastrobar" target="_blank" rel="noopener">Instagram</a> · <a class="link" href="https://www.facebook.com/andalugastrobar" target="_blank" rel="noopener">Facebook</a></p>
    <p class="label" style="margin-top:var(--s-7)">{star()}{c['amen_t']}</p>
    <div class="amen">{amen}</div>
  </div>
  <div class="reveal" data-delay="1">
    <div class="map-embed" data-src="{maps_src}" aria-label="{c['map_t']}"><div class="consent"><div><p>{c['map_consent']}</p><div class="hero-ctas" style="margin-top:var(--s-4);justify-content:center"><button class="btn btn--cta" type="button">{c['map_load']}</button><a class="btn btn--ghost" href="https://www.google.com/maps/search/?api=1&query=Andalu+Gastrobar+Strada+Teodor+Codrescu+6+Ia%C8%99i" target="_blank" rel="noopener">{c['map_open']}</a></div></div></div></div>
    <p class="label" style="margin-top:var(--s-7)">{star()}{c['how_t']}</p>
    <div class="howto">{how}</div>
  </div>
</div></div></section>
'''
    return out + footer(ctx)


# ----------------------------------------------------------------------------- LEGAL + OBRIGADO
LEGAL = {
'ro': {
 'confidentialitate': ('Politica de confidențialitate · Andalu Gastrobar', 'Cum folosește Andalu Gastrobar datele personale trimise prin site: rezervări pe WhatsApp, cereri de ofertă, hartă.', 'Confidențialitate', 'Datele voastre, <em>pe scurt</em>.', 'Site-ul acesta nu are cookie-uri de urmărire și nu trimite nimic fără o acțiune a voastră. Ce colectăm, de ce și cât timp.',
  '''<h2>Cine suntem</h2><p>Andalu Gastrobar, Strada Teodor Codrescu 6, Iași 700481. Societatea: SC LALOCA13 SRL, CUI RO40171204, J22/2131/2018, cu sediul la aceeași adresă. Contact pentru date personale: <a href="mailto:andalu.gastrobar@gmail.com">andalu.gastrobar@gmail.com</a>.</p>
<h2>Ce date colectăm și de ce</h2>
<h3>Rezervarea pe WhatsApp</h3><p>Formularul de rezervare nu trimite nimic către noi direct: compune un mesaj în telefonul vostru și deschide WhatsApp. Datele (nume, dată, oră, număr de persoane) ajung la noi doar dacă apăsați „trimite” în WhatsApp. Le folosim ca să vă ținem masa și le păstrăm în istoricul conversației, pe care îl putem șterge la cerere.</p>
<h3>Cererea de ofertă pentru evenimente</h3><p>Formularul trimite numele, telefonul, tipul evenimentului, numărul de persoane, data și mesajul vostru pe emailul restaurantului, printr-un serviciu de formulare al găzduirii (Netlify). Temei: pașii premergători unui contract, la cererea voastră (art. 6 alin. 1 lit. b GDPR). Păstrăm cererea cât durează discuția și, dacă nu se încheie un contract, maximum 12 luni.</p>
<h3>Harta Google</h3><p>Harta de pe pagina de contact se încarcă doar după ce apăsați „Încarcă harta”. Abia atunci browserul vostru comunică cu Google, conform <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">politicii Google</a>.</p>
<h3>Fonturi</h3><p>Fonturile se încarcă de la Google Fonts; browserul trimite către Google adresa IP la încărcarea paginii. <span class="tbc">Opțiune: găzduirea fonturilor pe site, de decis înainte de publicare.</span></p>
<h3>Jurnale de server</h3><p>Găzduirea (Netlify) păstrează jurnale tehnice (adresa IP, pagina cerută, ora) pentru securitate, pe termen scurt.</p>
<h2>Cookie-uri</h2><p>Site-ul nu folosește cookie-uri proprii și nu are instrumente de analiză sau de publicitate. Singurele cookie-uri posibile sunt cele ale Google, după ce încărcați harta.</p>
<h2>Drepturile voastre</h2><p>Puteți cere accesul la date, rectificarea, ștergerea, restricționarea sau portabilitatea lor și vă puteți opune prelucrării, scriind la adresa de mai sus. Aveți dreptul de a depune o plângere la <a href="https://www.dataprotection.ro/" target="_blank" rel="noopener">ANSPDCP</a>.</p>
<p><em>Ultima actualizare: octombrie 2026. Textul este un model și se verifică cu un consultant juridic înainte de publicare.</em></p>'''),
 'termeni': ('Termeni și condiții · Andalu Gastrobar', 'Termenii de utilizare a site-ului Andalu Gastrobar: rezervări, evenimente, proprietate intelectuală, ANPC.', 'Termeni și condiții', 'Regulile <em>casei</em>, în scris.', 'Cum funcționează rezervările și cererile de ofertă făcute prin site, și ce vă putem promite.',
  '''<h2>Site-ul</h2><p>Site-ul andalugastrobar.ro este operat de Andalu Gastrobar, Strada Teodor Codrescu 6, Iași. Societatea: SC LALOCA13 SRL, CUI RO40171204, J22/2131/2018. Informațiile de pe site (meniu, prețuri, program) sunt orientative și se pot schimba; meniul de la masă are prioritate.</p>
<h2>Rezervări</h2><ul><li>O rezervare trimisă pe WhatsApp, telefon sau platforme este valabilă după confirmarea noastră.</li><li>Ținem masa 15 minute după ora rezervată; după aceea o putem oferi altor oaspeți.</li><li>Pentru grupuri de peste 12 persoane putem cere un avans și un meniu stabilit în prealabil.</li><li>Vă rugăm să anulați pe același canal dacă nu mai veniți.</li></ul>
<h2>Evenimente și catering</h2><p>Cererea de ofertă nu obligă la nimic. Un eveniment se confirmă printr-o ofertă acceptată în scris, un avans și numărul final de persoane comunicat cu <span class="tbc">X zile</span> înainte. <span class="tbc">Condițiile de avans și de anulare se completează de restaurant.</span></p>
<h2>Alergeni</h2><p>Alergenii marcați în meniu sunt informativi. Spuneți-ne la masă orice alergie; nu putem garanta absența totală a urmelor.</p>
<h2>Proprietate intelectuală</h2><p>Textele, fotografiile și elementele grafice de pe site aparțin Andalu Gastrobar sau autorilor lor și nu pot fi folosite fără acord.</p>
<h2>Soluționarea litigiilor</h2><p>Pentru reclamații, scrieți-ne întâi nouă. Consumatorii pot apela la <a href="https://anpc.ro/ce-este-sal/" target="_blank" rel="noopener">ANPC – SAL</a> și la <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">platforma europeană SOL</a>.</p>
<p><em>Ultima actualizare: octombrie 2026. Textul este un model și se verifică cu un consultant juridic înainte de publicare.</em></p>'''),
 'multumim': ('Mulțumim · Andalu Gastrobar', 'Cererea a fost trimisă.', 'Mulțumim', 'Am primit <em>cererea</em>.', 'Răspundem în orele de program, de obicei în aceeași zi. Dacă e urgent, scrieți-ne pe WhatsApp.', ''),
},
'en': {
 'privacy': ('Privacy policy · Andalu Gastrobar', 'How Andalu Gastrobar uses personal data sent through the site: WhatsApp bookings, quote requests, map.', 'Privacy', 'Your data, <em>in short</em>.', 'This site has no tracking cookies and sends nothing without an action from you. What we collect, why and for how long.',
  '''<h2>Who we are</h2><p>Andalu Gastrobar, Strada Teodor Codrescu 6, Iași 700481, Romania. Company: SC LALOCA13 SRL, VAT RO40171204, trade register J22/2131/2018, registered at the same address. Contact for personal data: <a href="mailto:andalu.gastrobar@gmail.com">andalu.gastrobar@gmail.com</a>.</p>
<h2>What we collect and why</h2>
<h3>Booking on WhatsApp</h3><p>The booking form sends nothing to us directly: it composes a message on your phone and opens WhatsApp. The details (name, date, time, number of guests) reach us only if you press "send" in WhatsApp. We use them to hold your table and keep them in the chat history, which we can delete on request.</p>
<h3>Event quote request</h3><p>The form sends your name, phone, event type, number of guests, date and message to the restaurant's email through our host's form service (Netlify). Basis: steps prior to a contract, at your request (art. 6(1)(b) GDPR). We keep the request for the length of the discussion and, if no contract follows, for at most 12 months.</p>
<h3>Google map</h3><p>The map on the contact page loads only after you tap "Load the map". Only then does your browser communicate with Google, under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google's policy</a>.</p>
<h3>Fonts</h3><p>Fonts load from Google Fonts; your browser sends Google your IP address when the page loads. <span class="tbc">Option: self-host the fonts, to decide before publishing.</span></p>
<h3>Server logs</h3><p>The host (Netlify) keeps short-term technical logs (IP address, page requested, time) for security.</p>
<h2>Cookies</h2><p>The site uses no cookies of its own and has no analytics or advertising tools. The only possible cookies are Google's, after you load the map.</p>
<h2>Your rights</h2><p>You can request access to your data, its rectification, erasure, restriction or portability, and object to processing, by writing to the address above. You have the right to lodge a complaint with the Romanian authority, <a href="https://www.dataprotection.ro/" target="_blank" rel="noopener">ANSPDCP</a>.</p>
<p><em>Last updated: October 2026. This text is a template and is checked with a legal adviser before publishing.</em></p>'''),
 'terms': ('Terms & conditions · Andalu Gastrobar', 'Terms of use of the Andalu Gastrobar site: bookings, events, intellectual property, ANPC.', 'Terms & conditions', 'The <em>house</em> rules, in writing.', 'How bookings and quote requests made through the site work, and what we can promise.',
  '''<h2>The site</h2><p>andalugastrobar.ro is operated by Andalu Gastrobar, Strada Teodor Codrescu 6, Iași, Romania. Company: SC LALOCA13 SRL, VAT RO40171204, trade register J22/2131/2018. Information on the site (menu, prices, hours) is indicative and may change; the printed menu at the table prevails.</p>
<h2>Bookings</h2><ul><li>A booking sent on WhatsApp, by phone or on a platform is valid after our confirmation.</li><li>We hold the table for 15 minutes after the booked time; after that we may offer it to other guests.</li><li>For groups over 12 we may ask for a deposit and a pre-agreed menu.</li><li>Please cancel on the same channel if you are no longer coming.</li></ul>
<h2>Events and catering</h2><p>A quote request commits you to nothing. An event is confirmed by a written acceptance of the quote, a deposit and the final headcount sent <span class="tbc">X days</span> before. <span class="tbc">Deposit and cancellation terms to be completed by the restaurant.</span></p>
<h2>Allergens</h2><p>Allergens marked on the menu are for information. Tell us about any allergy at the table; we cannot guarantee the total absence of traces.</p>
<h2>Intellectual property</h2><p>Texts, photos and graphics on the site belong to Andalu Gastrobar or their authors and may not be used without consent.</p>
<h2>Disputes</h2><p>For complaints, write to us first. Consumers may use <a href="https://anpc.ro/ce-este-sal/" target="_blank" rel="noopener">ANPC – SAL</a> and the <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener">EU online dispute resolution platform</a>.</p>
<p><em>Last updated: October 2026. This text is a template and is checked with a legal adviser before publishing.</em></p>'''),
 'thanks': ('Thank you · Andalu Gastrobar', 'Your request was sent.', 'Thank you', 'We have your <em>request</em>.', 'We reply during opening hours, usually the same day. If it is urgent, message us on WhatsApp.', ''),
}}


def legal_page(ctx):
    title, desc, label, h1, lead, body = LEGAL[ctx.lang][ctx.slug]
    out = head(ctx, title, desc) + header(ctx, False)
    if not body:   # obrigado
        t = ctx.t
        out += f'<section class="thanks"><div class="container"><p class="label">{star()}{label}</p><h1 style="margin-top:var(--s-4)">{h1}</h1><p>{lead}</p><div class="hero-ctas" style="justify-content:center;margin-top:var(--s-6)"><a class="btn btn--cta" href="{ctx.p("")}">{t["home"]}</a><a class="btn btn--wa" href="{wa_link(t["wa_text"])}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>WhatsApp</a></div></div></section>'
        return out + footer(ctx)
    out += page_hero(ctx, label, h1, lead, crumb=label)
    out += f'<section class="section"><div class="container"><div class="prose">{body}</div></div></section>'
    return out + footer(ctx)


# ----------------------------------------------------------------------------- build
BUILDERS = {'': home, 'meniu': menu_page, 'rezervari': reservations_page, 'evenimente': events_page, 'povestea-noastra': story_page,
            'galerie': gallery_page, 'contact': contact_page, 'confidentialitate': legal_page, 'termeni': legal_page, 'multumim': legal_page}


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    shutil.copytree(HERE / 'assets', OUT / 'assets', ignore=shutil.ignore_patterns('sprite.html'))
    shutil.copy(HERE / 'assets' / 'favicon.svg', OUT / 'favicon.svg')
    if (HERE / 'media').exists():
        shutil.copytree(HERE / 'media', OUT / 'media')
    urls = []
    for ro_slug, fn in BUILDERS.items():
        for lang in ('ro', 'en'):
            slug = ro_slug if lang == 'ro' else SLUGS[ro_slug]
            ctx = Ctx(lang, slug)
            html = fn(ctx)
            if MODE == 'preview':
                html = html.replace('<main id="main">', '<div class="demo-bar">Pre-vizualizare · Pacheco Studios · site în lucru</div>\n<main id="main">', 1)
            rel = Path(*ctx.rel) / 'index.html' if ctx.rel else Path('index.html')
            write(OUT / rel, html)
            if ro_slug != 'multumim':
                urls.append(ctx.abs())
    if MODE == 'site':
        for f in (HERE / 'netlify').glob('*'):
            shutil.copy(f, OUT / f.name)
        write(OUT / 'robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
        write(OUT / 'sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    n = sum(1 for _ in OUT.rglob('index.html'))
    print(f'{MODE}: {n} páginas em {OUT}')


if __name__ == '__main__':
    main()
