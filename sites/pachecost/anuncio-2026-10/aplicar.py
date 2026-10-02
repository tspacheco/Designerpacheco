#!/usr/bin/env python3
"""pachecost.com — alterações de 01–02/10/2026 sobre o deploy exportado do Netlify (pasta cur/ → novo/).

1. Primeiro ecrã para quem chega por anúncio (PT e RO): utm_*, fbclid ou ?origem=anuncio → html.anuncio.
2. Aviso de cookies compacto no telemóvel.
3. Separadores com mais ar no computador.
4. Lema acima de cada vista principal (PT, RO, EN), escondido a quem chega por anúncio.
5. "Ponte" para as automações entre os tipos de negócio e "Mais sites que fizemos" (PT, RO, EN).
6. Foco: automações com IA por defeito (vista inicial, separadores, título, descrição, contacto);
   os sites passam a "associados" (ponte no fim das automações). Quem chega por anúncio de um site
   continua a entrar pelos sites; um anúncio de automações liga com #automatizari no fim do endereço.

Cada substituição tem de acontecer exatamente uma vez por ficheiro; se não acontecer, o script pára
(o gerador pode ter mudado o HTML).
"""
import pathlib, re, shutil, sys
from urllib.parse import quote

RAIZ = pathlib.Path(__file__).resolve().parent
CUR, NOVO = RAIZ / "cur", RAIZ / "novo"

WA = "https://wa.me/351967117357?text="
ICONE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 '
         '8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5'
         'a8.48 8.48 0 0 1 8 8v.5z"/></svg>')
SETA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

HEROI = {
    "pt": dict(
        eyebrow="Sites para restaurantes",
        titulo="Um site assim para o teu restaurante.",
        lead="Fazemos o teu site e mostramos-to antes de pagares. Sem compromisso.",
        botao="Escreve-nos no WhatsApp",
        msg="Olá Tomás! Vi o anúncio. Queria ver como ficaria o site do meu restaurante: ",
        naval_tip="Restaurante", naval_cidade="Olhão",
        toda_chic='<li class="rv dest" style="--i:2"><a class="q" href="/p/toda-chic/pt.html"',
    ),
    "ro": dict(
        eyebrow="Site-uri pentru restaurante",
        titulo="Un site ca acesta pentru restaurantul tău.",
        lead="Îți facem site-ul și ți-l arătăm înainte să plătești. Fără obligații.",
        botao="Scrie-ne pe WhatsApp",
        msg="Bună, Tomás! Am văzut anunțul. Vreau să văd cum ar arăta site-ul restaurantului meu: ",
        naval_tip="Restaurant", naval_cidade="Olhão",
        toda_chic='<li class="rv dest" style="--i:2"><a class="q" href="/p/toda-chic/"',
    ),
}

LEMA = {
    "pt": ("Tens um objetivo a atingir?", "A IA vai <span class=\"nb\">fazê-lo</span> acontecer.", "Só tens de dar o primeiro passo."),
    "ro": ("Ai un obiectiv de atins?", "AI-ul îl va face să se întâmple.", "Trebuie doar să faci primul pas."),
    "en": ("Do you have a goal to reach?", "AI will make it happen.", "You just have to take the first step."),
}

PONTE = {
    "pt": dict(
        eyebrow="E depois do site",
        titulo="O site traz clientes. As automações mantêm-nos.",
        lead="Oito coisas que hoje fazes à mão, a andarem sozinhas no WhatsApp: marcações confirmadas, "
             "avaliações no Google, os clientes que não voltaram, faturas para o contabilista.",
        botao="Ver as automações", cliente="Cliente", assistente="Assistente",
        m1="Têm mesa para 4 hoje às 20h?",
        m2="Temos, sim. Em nome de quem fica? Confirmo já a reserva das 20:00 para 4 pessoas.",
    ),
    "ro": dict(
        eyebrow="Și după site",
        titulo="Site-ul aduce clienți. Automatizările îi păstrează.",
        lead="Opt lucruri pe care le faci acum de mână, mergând singure pe WhatsApp: programări confirmate, "
             "recenzii pe Google, clienții care nu s-au mai întors, facturi pentru contabil.",
        botao="Vezi automatizările", cliente="Client", assistente="Asistent",
        m1="Aveți masă pentru 4 diseară la 20?",
        m2="Da, avem. Pe ce nume o trec? Confirm imediat rezervarea de la 20:00 pentru 4 persoane.",
    ),
    "en": dict(
        eyebrow="And after the website",
        titulo="Your website brings customers. Automations keep them.",
        lead="Eight things you do by hand today, running on their own on WhatsApp: confirmed bookings, "
             "Google reviews, the customers who haven’t come back, invoices for your accountant.",
        botao="See the automations", cliente="Customer", assistente="Assistant",
        m1="Do you have a table for 4 tonight at 8?",
        m2="We do. What name should I put it under? I’ll confirm the booking for 4 people at 20:00 right away.",
    ),
}

# 6) foco nas automações com IA
FOCO = {
    "pt": dict(
        titulo_antes="Pacheco Studios — sites e automações com IA para negócios locais",
        titulo="Pacheco Studios — automações com IA e sites para negócios locais",
        desc_antes="Sites feitos para negócios reais e automações no WhatsApp que trazem os clientes de volta. Fazemos o teu site antes de pagares.",
        desc="Automações com IA no WhatsApp que respondem, marcam, confirmam e trazem os clientes de volta, e o site por onde eles entram. Vês uma demonstração antes de decidir.",
        og_antes="Pacheco Studios — onde o teu negócio ganha vida online",
        og="Pacheco Studios — automações com IA para o teu negócio",
        eyebrow_antes="Automações", eyebrow="Automações com IA",
        h2_antes="O site traz clientes. As automações mantêm-nos.",
        h2="A IA faz o trabalho de todos os dias. Tu aprovas.",
        contacto_antes="Fazemos o teu site e mostramos-to. Sem compromisso.",
        contacto="Mostramos-te a automação a responder ou o site já feito. Sem compromisso.",
        wa_antes="Olá Tomás! Vi os sites da Pacheco Studios e queria falar sobre o meu negócio: ",
        wa="Olá Tomás! Vi a Pacheco Studios e queria falar sobre o meu negócio: ",
        p_eyebrow="E o site?", p_titulo="O site é por onde os clientes entram.",
        p_lead="O que o cliente quer saber antes de ligar, respondido no telemóvel: o que há, se é bom, se há vaga, "
               "como chegar. Feito para o teu negócio e ligado às automações. Mostramos-to antes de pagares.",
        p_botao="Ver os sites que fizemos", p_lista="Três dos sites que fizemos",
    ),
    "ro": dict(
        titulo_antes="Pacheco Studios — site-uri și automatizări pentru afaceri locale",
        titulo="Pacheco Studios — automatizări cu AI și site-uri pentru afaceri locale",
        desc_antes="Site-uri făcute pentru afaceri reale și automatizări pe WhatsApp care aduc clienții înapoi. Îți facem site-ul înainte să plătești.",
        desc="Automatizări cu AI pe WhatsApp care răspund, programează, confirmă și aduc clienții înapoi, plus site-ul prin care ei intră. Vezi o demonstrație înainte să decizi.",
        og_antes="Pacheco Studios — unde afacerea ta prinde viață online",
        og="Pacheco Studios — automatizări cu AI pentru afacerea ta",
        eyebrow_antes="Automatizări", eyebrow="Automatizări cu AI",
        h2_antes="Site-ul aduce clienți. Automatizările îi păstrează.",
        h2="AI-ul face treaba de zi cu zi. Tu aprobi.",
        contacto_antes="Îți facem site-ul și ți-l arătăm. Fără obligații.",
        contacto="Îți arătăm automatizarea răspunzând sau site-ul gata făcut. Fără obligații.",
        wa_antes="Bună, Tomás! Am văzut site-urile Pacheco Studios și vreau să vorbim despre afacerea mea: ",
        wa="Bună, Tomás! Am văzut Pacheco Studios și vreau să vorbim despre afacerea mea: ",
        p_eyebrow="Și site-ul?", p_titulo="Site-ul e ușa prin care intră clienții.",
        p_lead="Ce vrea clientul să știe înainte să sune, răspuns pe telefon: ce ai, dacă e bun, dacă e loc, cum ajunge. "
               "Făcut pentru afacerea ta și legat de automatizări. Ți-l arătăm înainte să plătești.",
        p_botao="Vezi site-urile făcute de noi", p_lista="Trei dintre site-urile făcute de noi",
    ),
    "en": dict(
        titulo_antes="Pacheco Studios — websites and AI automations for local businesses",
        titulo="Pacheco Studios — AI automations and websites for local businesses",
        desc_antes="Websites built for real businesses and WhatsApp automations that bring customers back. We build your site before you pay.",
        desc="AI automations on WhatsApp that answer, book, confirm and bring customers back, plus the website they come in through. See a demo before you decide.",
        og_antes="Pacheco Studios — where your business comes alive online",
        og="Pacheco Studios — AI automations for your business",
        eyebrow_antes="Automations", eyebrow="AI automations",
        h2_antes="Your website brings customers. Automations keep them.",
        h2="AI does the everyday work. You approve.",
        contacto_antes="We’ll build your site and show it to you. No strings attached.",
        contacto="We’ll show you the automation answering, or your site already built. No strings attached.",
        wa_antes="Hi Tomás! I saw the Pacheco Studios websites and I’d like to talk about my business: ",
        wa="Hi Tomás! I saw Pacheco Studios and I’d like to talk about my business: ",
        p_eyebrow="And the website?", p_titulo="The website is where customers come in.",
        p_lead="What a customer wants to know before calling, answered on their phone: what you offer, whether it’s good, "
               "whether there’s room, how to get there. Built for your business and wired to the automations. We show it to you before you pay.",
        p_botao="See the sites we’ve built", p_lista="Three of the sites we’ve built",
    ),
}

# 1) decide-se antes de pintar: chegada por anúncio (utm_*, fbclid ou ?origem=anuncio) → html.anuncio, sem intro
CABECA_ANTES = ("(function(){try{if(!sessionStorage.getItem('ps-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
                "document.documentElement.classList.add('intro-vai')}catch(e){}})();")
CABECA_DEPOIS = ("(function(){try{var a=/[?&](utm_[a-z]+=|fbclid=|origem=anuncio)/.test(location.search);"
                 "if(a)document.documentElement.classList.add('anuncio');"
                 "if(!a&&!sessionStorage.getItem('ps-intro')&&!matchMedia('(prefers-reduced-motion: reduce)').matches)"
                 "document.documentElement.classList.add('intro-vai')}catch(e){}})();")

CSS = """
/* ═══ chegada por anúncio (html.anuncio: ?utm_*, fbclid ou ?origem=anuncio, decidido no <head>) ═══
   O primeiro ecrã fala a quem viu o vídeo de um restaurante: o que fazemos, a oferta e o WhatsApp.
   Sem parâmetros, a página é a de sempre. */
.heroi-anuncio{display:none}
html.anuncio .heroi-anuncio{display:block}
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .eyebrow,
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .afirmacao,
html.anuncio #proiecte > .envolver:has(.heroi-anuncio) > .lead{display:none}
.heroi-anuncio .botao{display:flex;width:100%;margin-top:1.5rem}
/* em destaque: no anúncio, o terceiro quadrado é um restaurante e não a loja de roupa */
.so-anuncio{display:none}
html.anuncio .so-anuncio{display:block}
html.anuncio .sem-anuncio{display:none}
@media (min-width:40rem){
  .heroi-anuncio .botao{display:inline-flex;width:auto}
}
/* ═══ aviso de cookies compacto: faixa colada ao fundo no telemóvel (antes tapava um terço do ecrã) ═══ */
.rgpd{left:0;right:0;bottom:0;transform:none;width:auto;border-radius:1rem 1rem 0 0;border-bottom:0;
  gap:.55rem;padding:.7rem max(var(--gutter),env(safe-area-inset-left)) calc(.7rem + env(safe-area-inset-bottom))}
.rgpd p{font-size:.8125rem;line-height:1.4}
.rgpd .acoes{gap:.5rem}
.rgpd button{min-height:2.5rem;padding:0 .9rem}
.rgpd a{min-height:2.5rem}
@media (min-width:40rem){
  .rgpd{left:50%;right:auto;bottom:calc(1rem + env(safe-area-inset-bottom));transform:translateX(-50%);
    width:min(42rem,calc(100% - 2rem));border-radius:1rem;border-bottom:1px solid var(--linha-e);gap:.9rem;padding:1rem 1.1rem}
  .rgpd p{font-size:.875rem;line-height:1.5}
  .rgpd button{min-height:2.75rem;padding:0 1.1rem}
  .rgpd a{min-height:2.75rem}
}
/* ═══ separadores com mais ar no computador (no telemóvel ficam como estão: os três têm de caber) ═══ */
@media (min-width:48rem){
  :root{--tabs:3.5rem}
  .tabs ul{gap:2.25rem}
  .tabs a{padding-inline:.15rem}
}
/* ═══ lema: três frases no topo de cada vista principal; a do meio, em laranja e na fonte display, é o destaque.
   Escondido a quem chega por anúncio: aí fala o herói. ═══ */
.lema{display:flex;align-items:flex-start;gap:1rem;margin:0 0 clamp(2.5rem,7vw,4rem);max-width:36rem;
  font-size:clamp(1.1rem,2.2vw,1.5rem);color:var(--osso)}
.lema-traco{flex:none;width:2.25rem;height:3px;margin-top:.62em;border-radius:2px;background:var(--laranja);
  transform-origin:left center;transform:scaleX(0);animation:lema-traco .9s var(--sair) .3s forwards}
@keyframes lema-traco{to{transform:none}}
.lema-txt{display:grid;gap:.3rem}
.lema-l1,.lema-l3{font:600 1em/1.3 var(--texto);text-wrap:balance}
.lema-l2{display:block;margin:.1em 0 .15em;font:400 clamp(1.6rem,4.4vw,3rem)/1.02 var(--display);text-transform:uppercase;
  letter-spacing:.005em;color:var(--laranja);text-wrap:balance}
.lema .nb{white-space:nowrap}
html.anuncio .lema{display:none}
/* ═══ pontes: dos sites para as automações (fim dos tipos de negócio) e das automações para os sites (fim da vista) ═══ */
.ponte{margin-top:clamp(3rem,9vw,5rem);display:grid;gap:1.75rem;padding:clamp(1.4rem,4vw,2.5rem);
  border:1px solid var(--linha-e);border-radius:1.25rem;background:var(--carvao-2);
  background-image:radial-gradient(70% 90% at 100% 0%,rgba(232,98,44,.16),transparent 70%)}
.ponte .afirmacao{font-size:clamp(1.5rem,3.2vw,2.25rem);margin-top:.7rem;max-width:16ch}
.ponte .lead{font-size:1rem}
.ponte-botao{margin-top:1.4rem;border-color:var(--laranja);color:var(--laranja)}
.ponte-botao:hover,.ponte-botao:focus-visible{background:var(--laranja);color:var(--carvao)}
.ponte-botao svg{transition:transform .25s var(--sair)}
.ponte-botao:hover svg,.ponte-botao:focus-visible svg{transform:translateX(.3rem)}
.ponte .chat{max-width:none}
.ponte .grelha{margin-top:0}
/* os quadrados dentro da ponte são pequenos: crescem com o conteúdo, só nome e cidade */
.ponte .grelha{gap:.5rem}
.ponte .dest .q{aspect-ratio:auto;min-height:6rem;padding:.7rem}
.ponte .dest .q-tip,.ponte .dest .q-sep{display:none}
.ponte .grelha .dest .q-nome{font-size:calc(.95rem * var(--fs,1))}
.ponte .grelha .dest .q[style*="--f:'Space Mono'"] .q-nome{font-size:calc(.85rem * var(--fs,1))}
.ponte .dest .q-meta{min-height:0;font-size:.6875rem}
@media (min-width:40rem){
  .ponte .grelha{gap:.75rem}
  .ponte .dest .q{min-height:6.5rem;padding:.9rem}
  .ponte .grelha .dest .q-nome{font-size:calc(1.15rem * var(--fs,1))}
  .ponte .grelha .dest .q[style*="--f:'Space Mono'"] .q-nome{font-size:calc(1rem * var(--fs,1))}
  .ponte .dest .q-meta{font-size:.75rem}
}
@media (min-width:48rem){
  .ponte{grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);align-items:center;gap:clamp(2rem,5vw,4rem)}
}
@media (prefers-reduced-motion:reduce){
  .lema-traco{animation:none;transform:none}
  .ponte-botao svg{transition:none}
}
/* ═══ foco: as automações com IA são a vista inicial. Quem chega por anúncio de um site (html.anuncio) entra pelos
   sites, porque foi isso que viu no vídeo; um anúncio de automações liga com #automatizari. ═══ */
#automatizari{display:block}
#proiecte:not(:target):not(:has(:target)){display:none}
body:has(#proiecte:target,#proiecte :target,#servicii:target,#servicii :target) #automatizari{display:none}
html.anuncio:not(:has(.vista:target,.vista :target)) #automatizari{display:none}
html.anuncio:not(:has(.vista:target,.vista :target)) #proiecte{display:block}
/* separador ativo sem JavaScript, com a mesma lógica */
.tabs a[href="#proiecte"]{color:var(--osso-2);border-color:transparent}
.tabs a[href="#automatizari"]{color:var(--osso);border-color:var(--laranja)}
body:has(#proiecte:target,#proiecte :target,#servicii:target,#servicii :target) .tabs a[href="#automatizari"]{color:var(--osso-2);border-color:transparent}
body:has(#proiecte:target,#proiecte :target) .tabs a[href="#proiecte"]{color:var(--osso);border-color:var(--laranja)}
html.anuncio:not(:has(.vista:target,.vista :target)) .tabs a[href="#automatizari"]{color:var(--osso-2);border-color:transparent}
html.anuncio:not(:has(.vista:target,.vista :target)) .tabs a[href="#proiecte"]{color:var(--osso);border-color:var(--laranja)}
"""

# 3) medição: chegadas por anúncio e as saídas delas, contadas à parte no GoatCounter
MED_ANTES = "  // tipos de negócio abertos, contados à parte: mostra o que interessa a quem visita\n"
MED_DEPOIS = ("  // chegadas por anúncio (html.anuncio, decidido no <head>) e as saídas delas para o WhatsApp, contadas à parte\n"
              "  var porAnuncio = document.documentElement.classList.contains('anuncio');\n"
              "  if (porAnuncio) {\n"
              "    window.addEventListener('load', function () { gc({ path: 'anuncio/chegada', title: 'chegada por anúncio', event: true }); });\n"
              "  }\n" + MED_ANTES)
SAIDA_ANTES = "    gc({ path: 'ir/' + canal, title: 'saída: ' + canal, event: true });\n"
SAIDA_DEPOIS = SAIDA_ANTES + "    if (porAnuncio) gc({ path: 'anuncio/' + canal, title: 'saída por anúncio: ' + canal, event: true });\n"

# 6) vista inicial no JavaScript (aria-current dos separadores)
VISTA_ANTES = "    var v = 'proiecte';\n"
VISTA_DEPOIS = "    var v = document.documentElement.classList.contains('anuncio') ? 'proiecte' : 'automatizari';\n"

ABRE_SITES = '<section id="proiecte" class="vista" aria-labelledby="t-proiecte">\n  <div class="envolver seccao">\n'
ABRE_AUTOS = '<section id="automatizari" class="vista" aria-labelledby="t-automatizari">\n  <div class="envolver seccao">\n'
MAIS = '<div class="mais">\n'


def uma_vez(src, antes, depois, nome):
    n = src.count(antes)
    if n != 1:
        sys.exit(f"{nome}: esperava 1 ocorrência de «{antes[:60]}…», encontrei {n}")
    return src.replace(antes, depois)


def todas(src, antes, depois, nome, minimo):
    n = src.count(antes)
    if n < minimo:
        sys.exit(f"{nome}: esperava pelo menos {minimo} ocorrências de «{antes[:60]}…», encontrei {n}")
    return src.replace(antes, depois)


def heroi(h):
    return (f'    <div class="heroi-anuncio">\n'
            f'      <p class="eyebrow">{h["eyebrow"]}</p>\n'
            f'      <h2 class="afirmacao">{h["titulo"]}</h2>\n'
            f'      <p class="lead">{h["lead"]}</p>\n'
            f'      <a class="botao primario grande" href="{WA}{quote(h["msg"], safe="")}">{ICONE}{h["botao"]}</a>\n'
            f'    </div>\n')


def lema(t):
    return (f'    <p class="lema"><span class="lema-traco" aria-hidden="true"></span><span class="lema-txt">'
            f'<span class="lema-l1">{t[0]}</span> <strong class="lema-l2">{t[1]}</strong> <span class="lema-l3">{t[2]}</span></span></p>\n')


def ponte(p):
    return (f'      <aside class="ponte rv" aria-labelledby="t-ponte">\n'
            f'        <div class="ponte-texto">\n'
            f'          <p class="eyebrow">{p["eyebrow"]}</p>\n'
            f'          <h3 id="t-ponte" class="afirmacao">{p["titulo"]}</h3>\n'
            f'          <p class="lead">{p["lead"]}</p>\n'
            f'          <a class="botao ponte-botao" href="#automatizari">{p["botao"]}{SETA}</a>\n'
            f'        </div>\n'
            f'        <div class="chat" aria-hidden="true">\n'
            f'          <div class="msg client rv" style="--i:3"><small>{p["cliente"]}</small>{p["m1"]}</div>\n'
            f'          <div class="msg asistent rv" style="--i:14"><small>{p["assistente"]}</small>{p["m2"]}</div>\n'
            f'        </div>\n'
            f'      </aside>\n    ')


def ponte_site(f, cartoes):
    return (f'    <aside class="ponte ponte-site rv" aria-labelledby="t-ponte-site">\n'
            f'      <div class="ponte-texto">\n'
            f'        <p class="eyebrow">{f["p_eyebrow"]}</p>\n'
            f'        <h3 id="t-ponte-site" class="afirmacao">{f["p_titulo"]}</h3>\n'
            f'        <p class="lead">{f["p_lead"]}</p>\n'
            f'        <a class="botao ponte-botao" href="#proiecte">{f["p_botao"]}{SETA}</a>\n'
            f'      </div>\n'
            f'      <ul class="grelha" aria-label="{f["p_lista"]}">\n{cartoes}      </ul>\n'
            f'    </aside>\n')


def naval(h):
    return ('<li class="rv dest so-anuncio" style="--i:2"><a class="q" href="https://gruponaval.online" '
            'style="--bg:#0A1C2E;--ink:#F2EDE2;--ac:#C9A227;--f:\'Sora\';--w:800;--fs:1" target="_blank" rel="noopener">'
            '<span class="q-nome">Grupo Naval</span><span class="q-meta"><span class="q-tip">' + h["naval_tip"] +
            '</span><span class="q-sep">&nbsp;· </span><span class="q-oras">' + h["naval_cidade"] + '</span></span></a></li>\n')


def reordenar_tabs(src, nome):
    m = re.search(r'(<nav class="tabs"[^>]*>\s*<ul>\n)(.*?)(\s*</ul>)', src, re.S)
    if not m:
        sys.exit(f"{nome}: não encontro os separadores")
    lis = {x.group(1): x.group(0) for x in re.finditer(r'[ \t]*<li><a href="#([a-z]+)" data-vista="[a-z]+"[^>]*>[^<]*</a></li>', m.group(2))}
    if set(lis) != {"proiecte", "automatizari", "servicii"}:
        sys.exit(f"{nome}: separadores inesperados {sorted(lis)}")
    lis["proiecte"] = lis["proiecte"].replace(' aria-current="page"', "")
    lis["automatizari"] = lis["automatizari"].replace('data-vista="automatizari"', 'data-vista="automatizari" aria-current="page"')
    novo = m.group(1) + lis["automatizari"] + "\n" + lis["proiecte"] + "\n" + lis["servicii"] + m.group(3)
    return src[:m.start()] + novo + src[m.end():]


def foco(src, lingua, nome):
    f = FOCO[lingua]
    src = uma_vez(src, f"<title>{f['titulo_antes']}</title>", f"<title>{f['titulo']}</title>", nome)
    src = todas(src, f["desc_antes"], f["desc"], nome, 3)          # meta description, og:description, JSON-LD
    src = uma_vez(src, f'property="og:title" content="{f["og_antes"]}"', f'property="og:title" content="{f["og"]}"', nome)
    src = uma_vez(src, f'<p class="eyebrow">{f["eyebrow_antes"]}</p>\n        <h2 id="t-automatizari" class="afirmacao">{f["h2_antes"]}</h2>',
                  f'<p class="eyebrow">{f["eyebrow"]}</p>\n        <h2 id="t-automatizari" class="afirmacao">{f["h2"]}</h2>', nome)
    src = uma_vez(src, f'<p class="lead">{f["contacto_antes"]}</p>', f'<p class="lead">{f["contacto"]}</p>', nome)
    src = todas(src, quote(f["wa_antes"], safe=""), quote(f["wa"], safe=""), nome, 2)
    src = uma_vez(src, VISTA_ANTES, VISTA_DEPOIS, nome)
    src = reordenar_tabs(src, nome)
    # ponte das automações para os sites, no fim da vista das automações, com os quadrados em destaque
    i = src.find('<section id="proiecte"'); g0 = src.find('<ul class="grelha">', i); g1 = src.find("</ul>", g0)
    cartoes = src[src.find("\n", g0) + 1:g1]
    a = src.find('<section id="automatizari"'); j = src.find("</section>", a); k = src.rfind("  </div>\n", 0, j)
    if not (0 < a < k < j) or src[k - 9:k] != "    </div>\n"[-9:]:
        sys.exit(f"{nome}: não encontro o fim da vista das automações")
    return src[:k] + ponte_site(f, cartoes) + src[k:]


def tratar(rel, lingua):
    src = (CUR / rel).read_text(encoding="utf-8")
    src = uma_vez(src, CABECA_ANTES, CABECA_DEPOIS, rel)
    i = src.rfind("</style>", 0, src.find("</head>"))
    assert i > 0, rel
    src = src[:i] + CSS + src[i:]
    src = uma_vez(src, MED_ANTES, MED_DEPOIS, rel)
    src = uma_vez(src, SAIDA_ANTES, SAIDA_DEPOIS, rel)
    topo = heroi(HEROI[lingua]) if lingua in HEROI else ""
    src = uma_vez(src, ABRE_SITES, ABRE_SITES + topo + lema(LEMA[lingua]), rel)
    src = uma_vez(src, ABRE_AUTOS, ABRE_AUTOS + lema(LEMA[lingua]), rel)
    if lingua in HEROI:
        tc = HEROI[lingua]["toda_chic"]
        src = uma_vez(src, tc, tc.replace('class="rv dest"', 'class="rv dest sem-anuncio"'), rel)
        j = src.find('class="rv dest sem-anuncio"'); k = src.find("</li>\n", j) + len("</li>\n")
        src = src[:k] + naval(HEROI[lingua]) + src[k:]
    src = uma_vez(src, MAIS, ponte(PONTE[lingua]) + MAIS, rel)
    src = foco(src, lingua, rel)
    (NOVO / rel).parent.mkdir(parents=True, exist_ok=True)
    (NOVO / rel).write_text(src, encoding="utf-8")
    print(f"{rel}: {len((CUR / rel).read_text(encoding='utf-8'))} → {len(src)} bytes")


if NOVO.exists():
    shutil.rmtree(NOVO)
shutil.copytree(CUR, NOVO)
tratar("index.html", "pt")
tratar("ro/index.html", "ro")
tratar("en/index.html", "en")
