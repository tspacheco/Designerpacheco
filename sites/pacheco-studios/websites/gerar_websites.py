#!/usr/bin/env python3
"""Página escondida de portefólio de websites: pachecost.com/websites/ (PT) e /en/websites/ (EN).

Uso:  python3 gerar_websites.py [pasta-de-saida]      (por omissão: ./saida)
Gera: <saida>/websites/index.html, <saida>/en/websites/index.html, <saida>/websites/media/*,
      e <saida>/previa/ (mesma página com caminhos relativos, para pré-visualizar sem servidor).

Regras (Tomás, 16 nov 2026):
- A página NÃO aparece no site principal: sem link no menu/rodapé, fora do sitemap, noindex (meta + cabeçalho
  X-Robots-Tag em _headers). Não pôr «Disallow: /websites» no robots.txt: isso anunciava o endereço.
- Só entram sites feitos por nós, de negócios reais, e que estão NO AR. Cada entrada de SITES foi aberta e
  verificada a 16 nov 2026 pela ponte (capturas em media/). Antes de acrescentar um site: confirmar que abre e
  tirar captura nova com a operação «captura» da ponte. Apresentações a quem não comprou ficam de fora.
- Sem preços, sem testemunhos, sem números de resultados.
"""
import html, json, os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CALENDLY = "https://calendly.com/tspacheco26/30min"

# setor: "mesa" (restaurantes e cafés) ou "loja" (lojas e serviços)
SITES = [
    dict(id="hanam", nome="Hanam Korean Barbecue", url="https://hanamquarteira.com/", dom="hanamquarteira.com", setor="mesa",
         tipo=("Churrasco coreano", "Korean barbecue"), local="Quarteira, Portugal", linguas="PT · EN",
         nota=("Reserva de mesa ligada ao TheFork.", "Table booking connected to TheFork.")),
    dict(id="bompaladar", nome="Simona's O Bom Paladar", url="https://bompaladar.pt/", dom="bompaladar.pt", setor="mesa",
         tipo=("Cozinha portuguesa", "Portuguese cuisine"), local="Almancil, Portugal", linguas="PT · EN",
         nota=("Carta completa e reserva por WhatsApp.", "Full menu and booking over WhatsApp.")),
    dict(id="magickey", nome="Magic Key", url="https://magickeyiasi.com/", dom="magickeyiasi.com", setor="loja",
         tipo=("Chaves de automóvel", "Car keys"), local="Iași, Roménia|Iași, Romania", linguas="RO · EN",
         nota=("Serviços, loja e pedido de chave num só sítio.", "Services, shop and key requests in one place.")),
    dict(id="tavira", nome="Ginásio Clube de Tavira", url="https://ginasioclubetavira.com/", dom="ginasioclubetavira.com", setor="mesa",
         tipo=("Restaurante do clube", "Club restaurant"), local="Tavira, Portugal", linguas="PT · EN",
         nota=("Ementa, história da casa e reservas.", "Menu, house history and bookings.")),
    dict(id="kathmandu", nome="Olá Kathmandu", url="https://olakathmandu.com/", url_en="https://olakathmandu.com/en/", dom="olakathmandu.com", setor="mesa",
         tipo=("Restaurante nepalês e indiano", "Nepalese and Indian restaurant"), local="Grândola, Portugal", linguas="PT · EN",
         nota=("Carta, pedidos para casa e reservas por WhatsApp.", "Menu, delivery orders and WhatsApp bookings.")),
    dict(id="barbearia", nome="Barbearia do Cão", url="https://barbeariadocao.com/", dom="barbeariadocao.com", setor="loja",
         tipo=("Banhos e tosquias", "Dog grooming"), local="Loulé, Portugal", linguas="PT",
         nota=("Marcação de banho e tosquia, antes e depois.", "Grooming bookings, before and after gallery.")),
    dict(id="saomartinho", nome="São Martinho", url="https://sao-martinho.com/", dom="sao-martinho.com", setor="mesa",
         tipo=("Restaurante tradicional", "Traditional restaurant"), local="Guia, Portugal", linguas="PT · EN",
         nota=("Especialidades, carta e pedido de reserva.", "Specialities, menu and booking requests.")),
    dict(id="naval", nome="Grupo Naval", url="https://gruponaval.online/", dom="gruponaval.online", setor="mesa",
         tipo=("Restaurante", "Restaurant"), local="Olhão, Portugal", linguas="PT",
         nota=("O dia da casa, galeria e reservas por telefone.", "The day at the house, gallery and phone bookings.")),
    dict(id="nais", nome="NAIS Food", url="https://naisfood.ro/", url_en="https://naisfood.ro/en", dom="naisfood.ro", setor="mesa",
         tipo=("Shaorma e entregas", "Shawarma and delivery"), local="Iași, Roménia|Iași, Romania", linguas="RO · EN",
         nota=("Menu e encomenda online com entrega.", "Menu and online ordering with delivery.")),
    dict(id="jasmim2", nome="Jasmim 2 · A Marisqueira", url="https://jasmim2marisqueira.pt/", dom="jasmim2marisqueira.pt", setor="mesa",
         tipo=("Marisqueira de praia", "Beach seafood house"), local="Manta Rota, Portugal", linguas="PT · EN · ES · FR",
         nota=("Quatro línguas para quem chega de férias.", "Four languages for holiday visitors.")),
    dict(id="carnepura", nome="Carne Pura", url="https://barbeariadocaocarnes.netlify.app/", dom="barbeariadocaocarnes.netlify.app", setor="loja",
         tipo=("Loja de carne crua para cães", "Raw food shop for dogs"), local="Loulé, Portugal", linguas="PT",
         nota=("Loja com carrinho e encomenda.", "Shop with basket and ordering.")),
    dict(id="muxagata", nome="Gelataria Muxagata", url="https://gelatariamuxagata.com/", dom="gelatariamuxagata.com", setor="mesa",
         tipo=("Gelataria", "Ice cream parlour"), local="Tavira, Portugal", linguas="PT · EN",
         nota=("História, sabores e galeria.", "History, flavours and gallery.")),
]

T = {
 "pt": dict(
    lang="pt-PT", outra=("EN", "/en/websites/", "English"), esta="PT",
    title="Websites profissionais · Pacheco Studios",
    desc="Websites desenhados e construídos pela Pacheco Studios para negócios reais. Todos no ar: abra qualquer um e veja-o a funcionar.",
    pill="Websites profissionais",
    h1a="Não mostramos maquetes.", h1b="Mostramos sites no ar.",
    sub="Cada site desta página foi desenhado e construído pela Pacheco Studios para um negócio real. Abra qualquer um e veja-o a funcionar.",
    cta="Fala connosco", cta2="Ver os sites",
    faixa="Capturas reais dos sites, tiradas com eles no ar",
    t_trab="Feitos por nós. Abertos ao público.",
    p_trab="Toque num site para o abrir no endereço verdadeiro do negócio.",
    f_todos="Todos", f_mesa="Restaurantes e cafés", f_loja="Lojas e serviços",
    noar="No ar", abrir="Abrir o site", cap_d="Captura do site {n} no computador", cap_m="Captura do site {n} no telemóvel",
    t_inc="O que vem em cada site.",
    inc=[("Desenho próprio", "Cada negócio recebe uma identidade só sua. Compare dois sites desta página: nenhum repete o outro."),
         ("Pensado para o telemóvel", "É no telemóvel que o cliente decide. Menu, botões e contactos ficam ao alcance do polegar."),
         ("Na língua de quem chega", "Português, inglês, romeno, espanhol ou francês, conforme os clientes que o negócio recebe."),
         ("Reservas e pedidos ligados", "WhatsApp, telefone, formulário ou a plataforma de reservas que o negócio já usa."),
         ("Legível para o Google", "Nome, morada, horário e tipo de negócio escritos para o Google os entender."),
         ("Só dados verdadeiros", "Avaliações, preços e horários vêm do negócio ou do Google. O que não está confirmado não entra.")],
    t_proc="Do primeiro contacto ao site no ar.",
    proc=[("Conversa", "Uma reunião sem compromisso para perceber o negócio, os clientes e o que o site tem de resolver."),
          ("Desenho", "Apresentamos o site já desenhado com o nome, as cores e o conteúdo do negócio, e afinamos em conjunto."),
          ("Publicação", "Pomos o site no ar no domínio do negócio e deixamos tudo a funcionar no telemóvel e no computador.")],
    fim_a="O próximo site desta página", fim_b="pode ser o do seu negócio.",
    fim_p="Marque uma reunião sem compromisso. Mostramos o que faríamos pelo seu negócio.",
    lema="Websites profissionais", priv=("Privacidade", "/privacidade.html"), cook=("Cookies", "/cookies.html"), saltar="Saltar para os sites",
 ),
 "en": dict(
    lang="en", outra=("PT", "/websites/", "Português"), esta="EN",
    title="Professional websites · Pacheco Studios",
    desc="Websites designed and built by Pacheco Studios for real businesses. All of them live: open any one and see it working.",
    pill="Professional websites",
    h1a="We don't show mockups.", h1b="We show live websites.",
    sub="Every website on this page was designed and built by Pacheco Studios for a real business. Open any one and see it working.",
    cta="Talk with us", cta2="See the websites",
    faixa="Real captures of the websites, taken while live",
    t_trab="Built by us. Open to the public.",
    p_trab="Tap a website to open it at the business's real address.",
    f_todos="All", f_mesa="Restaurants and cafés", f_loja="Shops and services",
    noar="Live", abrir="Open the website", cap_d="Capture of the {n} website on desktop", cap_m="Capture of the {n} website on a phone",
    t_inc="What comes with every website.",
    inc=[("Its own design", "Each business gets an identity of its own. Compare any two websites on this page: no two look alike."),
         ("Made for the phone", "The phone is where customers decide. Menu, buttons and contacts sit within thumb's reach."),
         ("In your customers' language", "Portuguese, English, Romanian, Spanish or French, depending on who the business welcomes."),
         ("Bookings and orders connected", "WhatsApp, phone, a form or the booking platform the business already uses."),
         ("Readable by Google", "Name, address, opening hours and business type written so Google understands them."),
         ("True data only", "Reviews, prices and opening hours come from the business or from Google. Nothing unconfirmed goes in.")],
    t_proc="From first contact to a live website.",
    proc=[("Conversation", "A meeting with no commitment to understand the business, its customers and what the website must solve."),
          ("Design", "We present the website already designed with the business's name, colours and content, and refine it together."),
          ("Launch", "We put the website live on the business's domain, working on phone and desktop.")],
    fim_a="The next website on this page", fim_b="could be your business's.",
    fim_p="Book a meeting with no commitment. We'll show what we would do for your business.",
    lema="Professional websites", priv=("Privacy", "/privacy.html"), cook=("Cookies", "/en/cookies.html"), saltar="Skip to the websites",
 ),
}

LOGO = ('<svg class="logo-m" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="50" fill="#0D0B08"/>'
        '<circle cx="50" cy="50" r="46" fill="none" stroke="#C9A256" stroke-width="3"/>'
        '<circle cx="50" cy="50" r="40" fill="none" stroke="#C8612A" stroke-width="1.6" stroke-dasharray="5 3"/>'
        '<path fill="#EDE8D8" d="M33 74v-3l5-1.2V30.2L33 29v-3h21c11 0 18 5.6 18 14.4S65 55 54 55h-6v14.8l6 1.2v3zm15-24h4.5c6 0 9.5-3.6 9.5-9.6S58.5 31 52.5 31H48z"/></svg>')
SETA = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 11L11 5M6 5h5v5"/></svg>'

CSS = r"""
:root{--bg:#0B0A09;--surface:#15120F;--surface-2:#1C1814;--ink:#F7F3EC;--ink-2:#B9B3AA;--ink-3:#8F8981;--laranja:#E8622C;--ouro:#C9A256;--ouro-2:#E6C66A;--petroleo:#14505A;--pessego:#F2B8A0;--vivo:#3DDC84;--linha:rgba(239,234,227,.12);
--display:"Inter Tight","Segoe UI",system-ui,sans-serif;--body:"Inter",system-ui,-apple-system,sans-serif;--mono:"Space Mono",ui-monospace,monospace;color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:400 1rem/1.6 var(--body);-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}
a{color:inherit}
h1,h2,h3,p{margin:0}
.in{max-width:1240px;margin:0 auto;padding-inline:clamp(16px,4vw,32px)}
.salta{position:absolute;left:-999px;top:0;background:var(--ink);color:#141210;padding:.6rem 1rem;z-index:99;border-radius:0 0 8px 0}
.salta:focus{left:0}
:focus-visible{outline:2px solid var(--ouro-2);outline-offset:3px;border-radius:4px}

/* cabeçalho */
.hd{position:fixed;inset:0 0 auto 0;height:56px;z-index:50;background:rgba(11,10,9,.78);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid var(--linha)}
.hd-in{height:100%;display:flex;align-items:center;justify-content:space-between;gap:1rem}
.logo{display:inline-flex;align-items:center;gap:.55rem;font:700 .92rem/1 var(--display);letter-spacing:-.01em;text-decoration:none;white-space:nowrap}
.logo-m{width:26px;height:26px;flex:none}
.dir{display:flex;align-items:center;gap:.6rem}
.lg{display:inline-flex;border:1px solid var(--linha);border-radius:999px;padding:2px;font:700 .68rem/1 var(--mono);letter-spacing:.08em}
.lg a,.lg span{padding:.42rem .6rem;border-radius:999px;text-decoration:none;color:var(--ink-2)}
.lg span{background:var(--ink);color:#141210}
.lg a:hover{color:var(--ink)}
.navcta{font:700 .82rem/1 var(--display);padding:.68rem 1rem;border-radius:999px;background:var(--laranja);color:#141210;text-decoration:none;white-space:nowrap}

/* herói */
.hero{position:relative;padding-top:calc(56px + clamp(3rem,9vw,6rem));overflow:hidden;isolation:isolate}
.hero::before{content:"";position:absolute;inset:0;z-index:-1;background:radial-gradient(60% 55% at 50% 0%,rgba(20,80,90,.55),transparent 70%),radial-gradient(40% 35% at 85% 30%,rgba(232,98,44,.14),transparent 70%)}
.hero-c{display:grid;justify-items:center;text-align:center;gap:1.3rem}
.pill{display:inline-flex;align-items:center;gap:.55rem;font:700 .7rem/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ouro-2);border:1px solid var(--linha);border-radius:999px;padding:.6rem .9rem;background:rgba(21,18,15,.6)}
.pill b{width:7px;height:7px;border-radius:50%;background:var(--vivo);box-shadow:0 0 0 0 rgba(61,220,132,.6);animation:pulsa 2.2s infinite}
@keyframes pulsa{70%{box-shadow:0 0 0 8px rgba(61,220,132,0)}100%{box-shadow:0 0 0 0 rgba(61,220,132,0)}}
.hero h1{font:800 clamp(2.3rem,7vw,5.2rem)/.98 var(--display);letter-spacing:-.045em;text-wrap:balance}
.hero h1 span{display:block}
.hero h1 .b{color:var(--laranja)}
.sub{max-width:44rem;color:var(--ink-2);font-size:clamp(1rem,1.6vw,1.15rem);text-wrap:pretty}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem;justify-content:center;margin-top:.3rem}
.btn{font:700 1rem/1 var(--display);padding:1.05rem 1.6rem;border-radius:999px;display:inline-flex;gap:.5rem;align-items:center;text-decoration:none;transition:transform .2s}
.btn:hover{transform:translateY(-1px)}
.b1{background:var(--laranja);color:#141210}
.b2{background:#fff;color:#111}

/* faixa de capturas (assinatura) */
.faixa{margin-top:clamp(2.6rem,6vw,4.2rem);position:relative;-webkit-mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent);mask-image:linear-gradient(90deg,transparent,#000 9%,#000 91%,transparent)}
.faixa-r{display:flex;gap:clamp(12px,1.6vw,22px);width:max-content;animation:corre 80s linear infinite}
.faixa:hover .faixa-r,.faixa:focus-within .faixa-r{animation-play-state:paused}
@keyframes corre{to{transform:translateX(-50%)}}
.fx{flex:none;width:clamp(250px,27vw,380px);border-radius:10px;overflow:hidden;border:1px solid var(--linha);background:var(--surface);text-decoration:none}
.fx img{width:100%;aspect-ratio:16/10;object-fit:cover}
.fx i{display:flex;align-items:center;gap:.45rem;font:700 .62rem/1 var(--mono);letter-spacing:.06em;font-style:normal;color:var(--ink-2);padding:.55rem .7rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.fx i::before,.dom::before{content:"";flex:none;width:6px;height:6px;border-radius:50%;background:var(--vivo)}
.faixa-l{text-align:center;font:700 .66rem/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);padding:1.1rem 1rem 0}

/* secções */
.sec{padding-block:clamp(3.6rem,9vw,6.5rem)}
.sec-h{display:grid;gap:.7rem;margin-bottom:clamp(1.6rem,4vw,2.6rem)}
.sec h2{font:800 clamp(1.8rem,4.4vw,3.1rem)/1.02 var(--display);letter-spacing:-.035em;max-width:18ch;text-wrap:balance}
.sec-h p{color:var(--ink-2);max-width:38rem}

/* filtro */
.filtro{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:clamp(1.4rem,3vw,2.2rem)}
.filtro button{font:600 .88rem/1 var(--body);color:var(--ink-2);background:none;border:1px solid var(--linha);border-radius:999px;padding:.7rem 1rem;cursor:pointer;min-height:44px}
.filtro button[aria-pressed=true]{background:var(--ink);color:#141210;border-color:var(--ink)}
.filtro button sup{font:700 .62rem/1 var(--mono);margin-left:.3rem;opacity:.7}

/* trabalhos */
.grelha{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(2rem,4vw,3.4rem) clamp(1.2rem,3vw,2.4rem)}
.tr{display:grid;gap:1.1rem;align-content:start}
.tr[hidden]{display:none}
.tr-m{position:relative;display:block;text-decoration:none;padding:0 7% 5% 0}
.jan{border-radius:12px;overflow:hidden;border:1px solid var(--linha);background:var(--surface-2);box-shadow:0 30px 60px -30px rgba(0,0,0,.8);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.jan-b{display:flex;align-items:center;gap:.5rem;padding:.5rem .7rem;border-bottom:1px solid var(--linha)}
.jan-b u{display:flex;gap:4px}.jan-b u::before,.jan-b u::after,.jan-b u b{content:"";width:7px;height:7px;border-radius:50%;background:rgba(239,234,227,.18)}
.jan-b em{flex:1;min-width:0;font:700 .62rem/1 var(--mono);font-style:normal;letter-spacing:.04em;color:var(--ink-3);background:rgba(239,234,227,.06);border-radius:6px;padding:.4rem .6rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.jan img,.jan video{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;object-position:top;background:var(--surface-2)}
.tel{position:absolute;right:0;bottom:0;width:21%;border-radius:clamp(10px,1.6vw,18px);overflow:hidden;border:3px solid #050505;outline:1px solid rgba(239,234,227,.22);background:#050505;box-shadow:0 22px 40px -14px rgba(0,0,0,.9);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.tel img,.tel video{display:block;width:100%;height:auto;aspect-ratio:420/909;object-fit:cover;object-position:top;background:#050505}
.tr-m:hover .jan{transform:translateY(-4px)}
.tr-m:hover .tel{transform:translateY(-8px)}
.tr-t{display:grid;gap:.45rem}
.tr-c{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:.3rem 1rem}
.tr h3{font:800 clamp(1.25rem,2.2vw,1.6rem)/1.1 var(--display);letter-spacing:-.025em}
.lin{font:700 .64rem/1 var(--mono);letter-spacing:.1em;color:var(--ouro-2);white-space:nowrap}
.tr-s{color:var(--ink-2);font-size:.95rem}
.tr-s b{color:var(--ink);font-weight:600}
.tr-p{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.6rem 1rem;margin-top:.35rem;padding-top:.8rem;border-top:1px solid var(--linha)}
.dom{display:inline-flex;align-items:center;gap:.5rem;font:700 .7rem/1.2 var(--mono);letter-spacing:.03em;color:var(--ink-2);min-width:0;overflow-wrap:anywhere}
.abrir{display:inline-flex;align-items:center;gap:.35rem;font:700 .88rem/1 var(--display);text-decoration:none;color:var(--ink);padding:.7rem 0;min-height:44px}
.abrir svg,.btn svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.abrir:hover{color:var(--laranja)}

/* o que vem */
.inc{background:var(--surface);border-block:1px solid var(--linha)}
.inc-g{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;border-top:1px solid var(--linha)}
.inc-g div{padding:1.5rem 1.4rem 1.6rem 0;border-bottom:1px solid var(--linha);display:grid;gap:.45rem;align-content:start}
.inc-g h3{font:700 1.08rem/1.2 var(--display);letter-spacing:-.015em}
.inc-g h3::before{content:"";display:block;width:22px;height:3px;background:var(--laranja);margin-bottom:.9rem;border-radius:2px}
.inc-g p{color:var(--ink-2);font-size:.95rem;max-width:32ch}

/* processo */
.proc{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(1.2rem,3vw,2.4rem);list-style:none;margin:0;padding:0;counter-reset:p}
.proc li{counter-increment:p;display:grid;gap:.5rem;align-content:start;padding-top:1.1rem;border-top:2px solid var(--petroleo)}
.proc li::before{content:"0" counter(p);font:700 .7rem/1 var(--mono);letter-spacing:.14em;color:var(--pessego)}
.proc h3{font:800 1.35rem/1.1 var(--display);letter-spacing:-.025em}
.proc p{color:var(--ink-2);font-size:.97rem}

/* fecho */
.fim{padding-block:clamp(4rem,10vw,7rem);text-align:center;background:radial-gradient(55% 80% at 50% 100%,rgba(20,80,90,.6),transparent 70%)}
.fim-c{display:grid;justify-items:center;gap:1.3rem}
.fim h2{font:800 clamp(2rem,5.6vw,4rem)/1 var(--display);letter-spacing:-.04em;max-width:none}
.fim h2 span{display:block}.fim h2 .b{color:var(--laranja)}
.fim p{color:var(--ink-2);max-width:34rem}
footer{border-top:1px solid var(--linha);padding-block:1.6rem calc(1.6rem + env(safe-area-inset-bottom,0px));font-size:.82rem;color:var(--ink-3)}
footer .in{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.6rem 1.5rem}
footer b{color:var(--ink-2)}
footer a{color:var(--ink-2)}

/* entrada */
.sobe{opacity:0;transform:translateY(14px);animation:sobe .7s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--i,0)*90ms + 80ms)}
@keyframes sobe{to{opacity:1;transform:none}}

@media (max-width:860px){
  .grelha{grid-template-columns:1fr}
  .inc-g{grid-template-columns:1fr 1fr}
  .proc{grid-template-columns:1fr}
}
@media (max-width:560px){
  .logo span{display:none}
  .navcta{font-size:.76rem;padding:.62rem .85rem}
  .inc-g{grid-template-columns:1fr}
  .inc-g div{padding-right:0}
  .btn{padding:1rem 1.3rem}
  .tr-m{padding:0 6% 6% 0}.tel{width:24%}
}
@media (prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  .sobe{animation:none;opacity:1;transform:none}
  .pill b{animation:none}
  .faixa{-webkit-mask-image:none;mask-image:none;overflow-x:auto}
  .faixa-r{animation:none}
  .jan,.tel,.btn{transition:none}
}
"""

JS = r"""
(function(){
  var bs=document.querySelectorAll('.filtro button'),cs=document.querySelectorAll('.tr');
  bs.forEach(function(b){b.addEventListener('click',function(){
    var f=b.getAttribute('data-f');
    bs.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});
    cs.forEach(function(c){c.hidden=!(f==='todos'||c.getAttribute('data-s')===f)});
  })});
  /* heros em vídeo: só carregam e tocam quando o cartão está à vista; com «reduzir movimento» fica a imagem */
  var rm=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vs=document.querySelectorAll('video[data-src]');
  if(rm||!('IntersectionObserver' in window))return;
  var io=new IntersectionObserver(function(es){es.forEach(function(en){
    var v=en.target;
    if(en.isIntersecting){if(!v.getAttribute('src'))v.setAttribute('src',v.getAttribute('data-src'));var p=v.play();if(p&&p.catch)p.catch(function(){});}
    else if(!v.paused){v.pause();}
  })},{rootMargin:'160px 0px'});
  vs.forEach(function(v){io.observe(v)});
})();
"""

def e(s):
    return html.escape(s, quote=True)

def tem(nome):
    return os.path.exists(os.path.join(AQUI, "media", nome))

def midia(s, l):
    """Ficheiros de um site para a língua l. Na página EN usa a versão inglesa do site (<id>-en-*) quando existe,
    e o vídeo do hero (<id>-en-d.mp4 / -m.mp4) quando o site abre com vídeo. A página PT fica com as imagens PT."""
    b = s["id"] + "-en" if l == "en" and tem(s["id"] + "-en-d.webp") else s["id"]
    return b, (l == "en" and tem(b + "-d.mp4") and tem(b + "-m.mp4"))

def pagina(l, m):
    """l = 'pt' | 'en'; m = prefixo dos ficheiros de media (ex.: '/websites/media/')."""
    t = T[l]; k = 0 if l == "pt" else 1
    def url(s):
        return s.get("url_en", s["url"]) if l == "en" else s["url"]
    def janela(s):
        b, v = midia(s, l); a = e(t["cap_d"].format(n=s["nome"]))
        if v:
            return (f'<video muted loop playsinline preload="none" poster="{m}{b}-d.webp" data-src="{m}{b}-d.mp4" '
                    f'width="1120" height="700" aria-label="{a}"></video>')
        return f'<img src="{m}{b}-d.webp" width="1120" height="700" alt="{a}" loading="lazy" decoding="async">'
    def telemovel(s):
        b, v = midia(s, l); a = e(t["cap_m"].format(n=s["nome"]))
        if v:
            return (f'<video muted loop playsinline preload="none" poster="{m}{b}-m.webp" data-src="{m}{b}-m.mp4" '
                    f'width="420" height="909" aria-label="{a}"></video>')
        return f'<img src="{m}{b}-m.webp" width="420" height="909" alt="{a}" loading="lazy" decoding="async">'

    def local(s):
        p = s["local"].split("|"); return p[k] if len(p) > 1 else p[0]
    faixa = "".join(
        f'<a class="fx" href="{url(s)}" target="_blank" rel="noopener" tabindex="{"0" if rep == 0 else "-1"}"{" aria-hidden=\"true\"" if rep else ""}>'
        f'<img src="{m}{midia(s, l)[0]}-d.webp" width="1120" height="700" alt="{e(t["cap_d"].format(n=s["nome"])) if rep == 0 else ""}" loading="{"eager" if rep == 0 and i < 4 else "lazy"}" decoding="async"><i>{s["dom"]}</i></a>'
        for rep in (0, 1) for i, s in enumerate(SITES))
    cartoes = "".join(f'''
<article class="tr" data-s="{s["setor"]}">
  <a class="tr-m" href="{url(s)}" target="_blank" rel="noopener" aria-label="{e(t["abrir"])}: {e(s["nome"])}">
    <div class="jan"><div class="jan-b"><u><b></b></u><em>{s["dom"]}</em></div>
      {janela(s)}</div>
    <div class="tel">{telemovel(s)}</div>
  </a>
  <div class="tr-t">
    <div class="tr-c"><h3>{e(s["nome"])}</h3><span class="lin">{s["linguas"]}</span></div>
    <p class="tr-s"><b>{e(s["tipo"][k])} · {e(local(s))}.</b> {e(s["nota"][k])}</p>
    <div class="tr-p"><span class="dom">{s["dom"]} · {e(t["noar"])}</span><a class="abrir" href="{url(s)}" target="_blank" rel="noopener">{e(t["abrir"])}<span class="sr"> {e(s["nome"])}</span>{SETA}</a></div>
  </div>
</article>''' for s in SITES)
    n_mesa = sum(1 for s in SITES if s["setor"] == "mesa"); n_loja = len(SITES) - n_mesa
    inc = "".join(f"<div><h3>{e(a)}</h3><p>{e(b)}</p></div>" for a, b in t["inc"])
    proc = "".join(f"<li><h3>{e(a)}</h3><p>{e(b)}</p></li>" for a, b in t["proc"])
    og = f"https://pachecost.com/websites/media/og-{l}.jpg"
    return f'''<!doctype html>
<html lang="{t["lang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="theme-color" content="#0B0A09">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Pacheco Studios">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800&family=Space+Mono:wght@700&display=swap">
<style>{CSS}.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}</style>
</head>
<body>
<a class="salta" href="#sites">{e(t["saltar"])}</a>
<header class="hd"><div class="in hd-in">
  <a class="logo" href="#topo" aria-label="Pacheco Studios">{LOGO}<span>Pacheco Studios</span></a>
  <div class="dir">
    <div class="lg" aria-label="Língua / Language"><span aria-current="true">{t["esta"]}</span><a href="{t["outra"][1]}" hreflang="{"en" if l == "pt" else "pt-PT"}" aria-label="{t["outra"][2]}">{t["outra"][0]}</a></div>
    <a class="navcta" href="{CALENDLY}" target="_blank" rel="noopener">{e(t["cta"])}</a>
  </div>
</div></header>

<main id="topo">
<section class="hero">
  <div class="in hero-c">
    <span class="pill sobe" style="--i:0"><b></b>{e(t["pill"])}</span>
    <h1 class="sobe" style="--i:1"><span>{e(t["h1a"])}</span><span class="b">{e(t["h1b"])}</span></h1>
    <p class="sub sobe" style="--i:2">{e(t["sub"])}</p>
    <div class="ctas sobe" style="--i:3"><a class="btn b1" href="{CALENDLY}" target="_blank" rel="noopener">{e(t["cta"])}</a><a class="btn b2" href="#sites">{e(t["cta2"])}</a></div>
  </div>
  <div class="faixa sobe" style="--i:5"><div class="faixa-r">{faixa}</div></div>
  <p class="faixa-l">{e(t["faixa"])}</p>
</section>

<section class="sec" id="sites"><div class="in">
  <div class="sec-h"><h2>{e(t["t_trab"])}</h2><p>{e(t["p_trab"])}</p></div>
  <div class="filtro" role="group" aria-label="{e(t["f_todos"])}">
    <button type="button" data-f="todos" aria-pressed="true">{e(t["f_todos"])}<sup>{len(SITES)}</sup></button>
    <button type="button" data-f="mesa" aria-pressed="false">{e(t["f_mesa"])}<sup>{n_mesa}</sup></button>
    <button type="button" data-f="loja" aria-pressed="false">{e(t["f_loja"])}<sup>{n_loja}</sup></button>
  </div>
  <div class="grelha">{cartoes}
  </div>
</div></section>

<section class="sec inc"><div class="in">
  <div class="sec-h"><h2>{e(t["t_inc"])}</h2></div>
  <div class="inc-g">{inc}</div>
</div></section>

<section class="sec"><div class="in">
  <div class="sec-h"><h2>{e(t["t_proc"])}</h2></div>
  <ol class="proc">{proc}</ol>
</div></section>

<section class="fim"><div class="in fim-c">
  <h2><span>{e(t["fim_a"])}</span><span class="b">{e(t["fim_b"])}</span></h2>
  <p>{e(t["fim_p"])}</p>
  <a class="btn b1" href="{CALENDLY}" target="_blank" rel="noopener">{e(t["cta"])}</a>
</div></section>
</main>

<footer><div class="in"><span><b>Pacheco Studios</b> · {e(t["lema"])}</span><span>+351 967 117 357 · +40 723 098 556 · <a href="{t["priv"][1]}">{t["priv"][0]}</a> · <a href="{t["cook"][1]}">{t["cook"][0]}</a></span></div></footer>
<script>{JS}</script>
</body>
</html>
'''

def escreve(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, "w", encoding="utf-8").write(texto)

def main():
    saida = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "saida"))
    for s in SITES:
        for suf in ("d", "m"):
            assert os.path.exists(os.path.join(AQUI, "media", f'{s["id"]}-{suf}.webp')), f'falta a captura {s["id"]}-{suf}.webp'
    escreve(os.path.join(saida, "websites", "index.html"), pagina("pt", "/websites/media/"))
    escreve(os.path.join(saida, "en", "websites", "index.html"), pagina("en", "/websites/media/"))
    md = os.path.join(saida, "websites", "media")
    shutil.rmtree(md, ignore_errors=True); shutil.copytree(os.path.join(AQUI, "media"), md)
    # pré-visualização sem servidor (caminhos relativos)
    pv = os.path.join(saida, "previa")
    escreve(os.path.join(pv, "index.html"), pagina("pt", "media/").replace('href="/en/websites/"', 'href="en.html"'))
    escreve(os.path.join(pv, "en.html"), pagina("en", "media/").replace('href="/websites/"', 'href="index.html"'))
    shutil.rmtree(os.path.join(pv, "media"), ignore_errors=True); shutil.copytree(os.path.join(AQUI, "media"), os.path.join(pv, "media"))
    print(f"ok: {len(SITES)} sites → {saida}")

if __name__ == "__main__":
    main()
