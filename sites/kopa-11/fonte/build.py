#!/usr/bin/env python3
"""Gerador do site Kopa.11 (PT). Estático, pronto para Netlify.

  python3 build.py            -> site/     (formulários Netlify ativos)
  python3 build.py preview    -> preview/  (formulários simulados, para pré-visualização)

Factos: ../recolha/00-recolha-instagram.md. Nada inventado: sem preços, sem testemunhos, sem datas de drop.
Logo: assets/logo.svg é um marcador tipográfico até chegar o ficheiro real (substituir e refazer).
"""
import re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MODE = 'preview' if len(sys.argv) > 1 and sys.argv[1] == 'preview' else 'site'
OUT = ROOT / MODE
IG = 'https://www.instagram.com/kopa11_oficial/'
HERO_VIDEO = True  # media/hero.mp4 é copiado no PC (reel-01 da batalha); ver README-netlify.md
LOGO = re.sub(r'<metadata>.*?</metadata>', '', (HERE / 'assets' / 'logo.svg').read_text(encoding='utf-8'), flags=re.S)

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo:wght@400;600;700&display=swap">'

NAV = [('index', 'Início'), ('podcast', 'Podcast'), ('team-kopa', 'Team Kopa'), ('drop', 'Drop'), ('eventos', 'Eventos')]

EPISODES = [  # 2.ª temporada, verão 2026 (observado no Instagram)
    (6, 'Kasa Nostra', 'Coletivo convidado'),
    (5, 'Cody & Davy', 'Convidados'),
    (4, 'Vizzy', 'Convidado'),
    (3, 'Invasão à Batalha da Visa', 'Episódio especial, Viseu'),
    (2, 'Da Chic Thief', 'Convidado'),
]


def shell(slug, title, desc, body, extra_head=''):
    nav = ''.join(
        f'<a href="{s}.html"{" aria-current=\"page\"" if s == slug else ""}>{n}</a>' for s, n in NAV)
    form_js = '''
<script>
document.querySelectorAll('form[data-netlify]').forEach(f=>{f.addEventListener('submit',e=>{e.preventDefault();f.classList.add('sent');});});
</script>''' if MODE == 'preview' else ''
    copy_js = '''
<script>
document.querySelectorAll('[data-copy]').forEach(b=>{b.addEventListener('click',async()=>{const t=b.dataset.copy;try{await navigator.clipboard.writeText(t);b.textContent='Copiado';}catch(e){const r=document.createRange();r.selectNodeContents(b.previousElementSibling);const s=getSelection();s.removeAllRanges();s.addRange(r);}setTimeout(()=>b.textContent='Copiar',1800);});});
</script>'''
    return f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta name="theme-color" content="#0A0A0A">
<link rel="icon" href="assets/logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">Saltar para o conteúdo</a>
<header class="top"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Kopa.11, início"><img src="assets/logo.jpg" alt="Kopa.11" width="40" height="40" onerror="this.replaceWith(this.nextElementSibling);this.nextElementSibling&&this.nextElementSibling.removeAttribute('hidden')"><span hidden>{LOGO}</span></a>
  <nav class="nav" aria-label="Principal">{nav}</nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <div><div class="sig">Kopa — 1 só caminho.</div><p class="note" style="margin-top:.6rem">Streetwear e cultura hip hop, Margem Sul.</p></div>
  <div><h4>Páginas</h4><ul>{''.join(f'<li><a href="{s}.html">{n}</a></li>' for s, n in NAV)}</ul></div>
  <div><h4>Fala connosco</h4><ul>
    <li><a href="{IG}" target="_blank" rel="noopener">Instagram @kopa11_oficial</a></li>
    <li><a href="drop.html#lista">Lista do próximo drop</a></li>
  </ul></div>
  <div class="fine"><span>© Kopa.11 · Margem Sul, Portugal</span><span>Pedidos e colaborações por mensagem no Instagram</span></div>
</div></footer>
{form_js}{copy_js}
</body>
</html>'''


def ep_cards(eps, live_first=False):
    out = []
    for i, (n, name, meta) in enumerate(eps):
        tag = '<span class="tag">2.ª temporada</span>'
        out.append(f'<a class="ep" href="{IG}" target="_blank" rel="noopener"><span class="n">#{n}</span><h3>{name}</h3><span class="meta">{meta}</span>{tag}</a>')
    return ''.join(out)


# ----------------------------------------------------------------------------- páginas
HERO_BG = ('<div class="hero-bg" aria-hidden="true"><video autoplay muted loop playsinline preload="metadata"'
           + (' poster="media/hero-poster.jpg"' if (HERE / 'media' / 'hero-poster.jpg').exists() else '')
           + '><source src="media/hero.mp4" type="video/mp4"></video></div>') if HERO_VIDEO else ''

HOME = f'''
<section class="hero{' has-video' if HERO_VIDEO else ''}">{HERO_BG}<div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Margem Sul · Streetwear · Hip hop</p>
    <h1><span>Veste a</span><span class="o">cena.</span></h1>
    <p class="lede">O Kopa.11 é uma marca de roupa urbana nascida dentro do hip hop da Margem Sul: um podcast em direto, uma crew de MCs e as batalhas de freestyle onde isto se decide. A roupa chega em drops limitados. Primeiro a cena, depois a peça.</p>
    <div class="cta-row">
      <a class="btn solid" href="drop.html#lista">Entrar na lista do drop</a>
      <a class="btn live" href="podcast.html">Próximo live</a>
    </div>
  </div>
  <div class="facts" aria-label="Em números">
    <div><b>2025</b><span>Margem Sul, desde julho</span></div>
    <div><b>2</b><span>temporadas de podcast</span></div>
    <div><b>2</b><span>batalhas apoiadas</span></div>
    <div><b>1</b><span>só caminho</span></div>
  </div>
</div></section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
  <span>É quase um podcast… mas</span><span>Team Kopa</span><span>Batalha da Visa</span><span>Red Bull FrancaMente</span><span>Margem Sul</span><span>1 só caminho</span>
  <span>É quase um podcast… mas</span><span>Team Kopa</span><span>Batalha da Visa</span><span>Red Bull FrancaMente</span><span>Margem Sul</span><span>1 só caminho</span>
</div></div>

<section class="band"><div class="wrap">
  <p class="eyebrow">O podcast</p>
  <h2>É quase um podcast… <span class="gold">mas</span></h2>
  <p class="lede" style="margin-top:1rem">Kota Phill e Concept recebem no Bunker quem está a fazer o rap acontecer. Em direto no Instagram. Os últimos episódios:</p>
  <div class="grid" style="margin-top:2rem">{ep_cards(EPISODES[:3])}</div>
  <div class="cta-row"><a class="btn" href="podcast.html">Todos os episódios</a></div>
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <p class="eyebrow">A roupa</p>
    <h2>Drops limitados. Sem reposição.</h2>
    <p class="lede" style="margin-top:1rem">Cada peça sai numa janela curta e só se produz o que foi pedido. Quem está na lista sabe primeiro a data, o desenho e os tamanhos. A primeira peça é a que a Team Kopa já veste: a t-shirt preta TEAM KOPA.</p>
    <div class="cta-row"><a class="btn solid" href="drop.html#lista">Quero saber primeiro</a></div>
  </div>
  <div class="poster" aria-hidden="true">
    <span class="pill">Drop 01 · em preparação</span>
    <div class="big">Team<br><em>Kopa</em><br>Tee</div>
    <div class="foot"><span>Preto · algodão pesado</span><span>Edição limitada</span></div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">Onde estamos</p>
  <h2>Nas batalhas, não na bancada.</h2>
  <ul class="list" style="margin-top:1.5rem">
    <li><span class="k">Viseu</span><div><b>Batalha da Visa</b><small>Roda de improviso no centro histórico, desde 2023. O Kopa.11 apoia e já levou lá o podcast (episódio #3).</small></div></li>
    <li><span class="k">Porto</span><div><b>Red Bull FrancaMente</b><small>Final nacional de freestyle. O Kopa.11 entregou um prémio extra ao campeão.</small></div></li>
    <li><span class="k">2800</span><div><b>Margem Sul</b><small>Onde o hip hop português começou, nos anos 80, entre Almada e o Miratejo. É daqui que falamos.</small></div></li>
  </ul>
  <div class="cta-row"><a class="btn" href="eventos.html">Ver eventos</a></div>
</div></section>
'''

PODCAST = f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Em direto no Instagram</p>
    <h1><span>É quase um</span><span class="o">podcast…</span><span>mas</span></h1>
    <p class="lede">Conversa, rimas e pouca cerimónia. Kota Phill e Concept recebem no Bunker MCs, coletivos e quem organiza a cena. Em direto em @kopa11_oficial; o que se diz ali não se repete.</p>
    <div class="cta-row"><a class="btn live" href="{IG}" target="_blank" rel="noopener">Seguir para apanhar o live</a></div>
  </div>
  <div class="poster" aria-hidden="true">
    <span class="pill">Live · kopa11_oficial</span>
    <div class="big">É quase<br>um <em>podcast</em><br>mas..</div>
    <div class="foot"><span>Kota Phill · Concept</span><span>Bunker</span></div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">2.ª temporada · verão 2026</p>
  <h2>Episódios</h2>
  <div class="grid" style="margin-top:2rem">{ep_cards(EPISODES)}</div>
  <p class="note" style="margin-top:1.5rem">A 1.ª temporada começou com o EP.1 com Joker. Os episódios entram aqui em formato gravado assim que forem publicados.</p>
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <p class="eyebrow">Queres vir ao Bunker?</p>
    <h2>Convidados e coletivos</h2>
    <p class="lede" style="margin-top:1rem">MCs, produtores, organizadores de batalhas, marcas da cena. Diz-nos quem és e o que estás a fazer.</p>
  </div>
  <div>
    <form name="convidado" method="POST" data-netlify="true" netlify-honeypot="site" action="obrigado.html">
      <input type="hidden" name="form-name" value="convidado">
      <p hidden><label>Site <input name="site" id="hp1"></label></p>
      <div class="field"><label for="c-nome">Nome ou nome artístico</label><input id="c-nome" name="nome" required autocomplete="name"></div>
      <div class="field"><label for="c-ig">Instagram</label><input id="c-ig" name="instagram" placeholder="@" required></div>
      <div class="field"><label for="c-oque">O que fazes</label><input id="c-oque" name="o_que" placeholder="MC, produtor, coletivo, batalha…"></div>
      <button class="btn solid" type="submit">Enviar</button>
    </form>
    <div class="ok">Recebido. Respondemos pelo Instagram.</div>
  </div>
</div></section>
'''

TEAM = f'''
<section class="hero"><div class="wrap">
  <p class="eyebrow">A crew</p>
  <h1><span>Team</span><span class="o">Kopa</span></h1>
  <p class="lede">Os MCs que vestem a marca e a levam às batalhas. A Team Kopa não é patrocínio: é a razão de a roupa existir. A primeira t-shirt da marca foi feita para eles.</p>
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <p class="eyebrow">Como funciona</p>
    <h2>Um só caminho</h2>
    <ul class="list" style="margin-top:1.5rem">
      <li><span class="k">01</span><div><b>Batalhar</b><small>A crew compete nas rodas e finais que importam. A marca vai com eles.</small></div></li>
      <li><span class="k">02</span><div><b>Gravar</b><small>Os episódios do podcast nascem das pessoas que a crew conhece.</small></div></li>
      <li><span class="k">03</span><div><b>Vestir</b><small>Cada peça aparece primeiro na crew. Depois, em drop limitado, em quem está na lista.</small></div></li>
    </ul>
  </div>
  <div class="poster" aria-hidden="true">
    <span class="pill">Team Kopa</span>
    <div class="big">Rimas<br>não se<br><em>compram</em></div>
    <div class="foot"><span>Freestyle</span><span>Margem Sul</span></div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">Membros</p>
  <h2>Quem é a Team Kopa</h2>
  <ul class="list" style="margin-top:1.5rem">
    <li><span class="k">KP</span><div><b>Kota Phill</b><small>Fundador do Kopa.11 e host do podcast. Organiza a Klandestina MS e faz as premiações à mão.</small></div></li>
    <li><span class="k">CC</span><div><b>Concept</b><small>Co-host do «É quase um podcast… mas».</small></div></li>
    <li><span class="k">CD</span><div><b>Cody</b><small>Gere as presenças no Bunker.</small></div></li>
    <li><span class="k">NS</span><div><b>Negativo Sul</b><small>Vídeo e imagem da crew.</small></div></li>
  </ul>
  <p class="note" style="margin-top:1rem">Fotos dos MCs da crew entram aqui com a autorização de cada um.</p>
  <div class="cta-row"><a class="btn" href="{IG}" target="_blank" rel="noopener">Ver no Instagram</a></div>
</div></section>
'''

DROP = f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <p class="eyebrow">Drop 01 · em preparação</p>
    <h1><span>Team Kopa</span><span class="o">Tee</span></h1>
    <p class="lede">A t-shirt preta que a crew veste nas batalhas, em algodão pesado, com o KOPA em dourado. Sai numa janela curta e só se produz o que for encomendado. Quem está na lista recebe a data e o acesso antecipado.</p>
    <div class="cta-row"><a class="btn solid" href="#lista">Entrar na lista</a></div>
  </div>
  <div class="poster" aria-hidden="true">
    <span class="pill">Edição limitada</span>
    <div class="big">Team<br><em>Kopa</em><br>Tee</div>
    <div class="foot"><span>Preto · dourado</span><span>XS – XXL</span></div>
  </div>
</div></section>

<section class="band" id="lista"><div class="wrap split">
  <div>
    <p class="eyebrow">Lista do drop</p>
    <h2>Sabe primeiro.</h2>
    <p class="lede" style="margin-top:1rem">Dizes-nos o tamanho e por onde queres ser avisado. Quando o drop abrir, tens 24 horas antes de toda a gente. Sem spam: só drops e lives.</p>
    <ul class="list" style="margin-top:1.5rem">
      <li><span class="k">01</span><div><b>Entras na lista</b><small>Nome, tamanho e contacto.</small></div></li>
      <li><span class="k">02</span><div><b>Recebes a data</b><small>Com o desenho final e o preço.</small></div></li>
      <li><span class="k">03</span><div><b>Encomendas na janela</b><small>Produzimos só o que foi pedido. Sem reposição.</small></div></li>
    </ul>
  </div>
  <div>
    <form name="lista-drop" method="POST" data-netlify="true" netlify-honeypot="site" action="obrigado.html">
      <input type="hidden" name="form-name" value="lista-drop">
      <p hidden><label>Site <input name="site" id="hp2"></label></p>
      <div class="field"><label for="d-nome">Nome</label><input id="d-nome" name="nome" required autocomplete="name"></div>
      <div class="field"><label for="d-contacto">Email ou WhatsApp</label><input id="d-contacto" name="contacto" required autocomplete="email" placeholder="email ou +351"></div>
      <div class="field"><label for="d-ig">Instagram (opcional)</label><input id="d-ig" name="instagram" placeholder="@"></div>
      <div class="field"><span class="eyebrow" style="color:var(--bone-2)">Tamanho</span>
        <div class="sizes">{''.join(f'<label><input type="radio" name="tamanho" value="{s}" id="t-{s.lower()}"{" checked" if s == "M" else ""}><span>{s}</span></label>' for s in ['XS','S','M','L','XL','XXL'])}</div>
      </div>
      <button class="btn solid" type="submit">Entrar na lista</button>
      <p class="note">Usamos o contacto só para avisar de drops e lives do Kopa.11. Sais quando quiseres.</p>
    </form>
    <div class="ok">Estás na lista. Avisamos antes de abrir.</div>
  </div>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">O que já saiu do Bunker</p>
  <h2>Feito à mão, feito aqui</h2>
  <ul class="list" style="margin-top:1.5rem">
    <li><span class="k">Tees</span><div><b>T-shirts estampadas</b><small>Sobretudo pretas, com frases de rua. A base da marca desde julho de 2025.</small></div></li>
    <li><span class="k">×</span><div><b>Collabs com artistas</b><small>South Flavour × Johny Malibz, Rapboy. Peças a dois nomes, em quantidade fechada.</small></div></li>
    <li><span class="k">Cap</span><div><b>Boné «Anti-Hype»</b><small>O acessório da casa.</small></div></li>
    <li><span class="k">1/1</span><div><b>Personalizadas por encomenda</b><small>Uma frase, um nome, um DJ, uma crew. Feita para ti.</small></div></li>
    <li><span class="k">Prémio</span><div><b>Premiações para batalhas</b><small>T-shirts pintadas à mão e troféus em impressão 3D para quem organiza rodas de freestyle.</small></div></li>
    <li><span class="k">3D</span><div><b>Quadros 3D</b><small>2Pac, Snoop, Biggie. Para a parede do Bunker ou da tua sala.</small></div></li>
  </ul>
  <p class="lede" style="margin-top:1.5rem">Batalhas, coletivos e lives com público podem ter a sua peça própria. Fala connosco pelo Instagram.</p>
  <div class="cta-row"><a class="btn" href="{IG}" target="_blank" rel="noopener">Falar pelo Instagram</a></div>
</div></section>
'''

EVENTOS = f'''
<section class="hero"><div class="wrap">
  <p class="eyebrow">Batalhas · lives · colaborações</p>
  <h1><span>Onde a cena</span><span class="o">acontece</span></h1>
  <p class="lede">O Kopa.11 está nas rodas de freestyle que estão a crescer em Portugal e leva o podcast até elas. Esta é a agenda que se vai enchendo.</p>
</div></section>

<section class="band"><div class="wrap">
  <p class="eyebrow">Já aconteceu</p>
  <h2>Por onde passámos</h2>
  <ul class="list" style="margin-top:1.5rem">
    <li><span class="k">Viseu</span><div><b>Batalha da Visa × Kopa.11</b><small>Colaboração com a roda de improviso de Viseu, ativa desde outubro de 2023, e gravação do episódio #3, «Invasão à Batalha da Visa».</small></div></li>
    <li><span class="k">Porto</span><div><b>Red Bull FrancaMente · final nacional</b><small>O Kopa.11 entregou um prémio extra ao vencedor da final de freestyle.</small></div></li>
    <li><span class="k">Bunker</span><div><b>É quase um podcast… mas · 2.ª temporada</b><small>Cinco episódios em direto no Instagram, de julho a setembro de 2026.</small></div></li>
    <li><span class="k">1 ano</span><div><b>1st B.Day</b><small>Primeiro aniversário da marca.</small></div></li>
  </ul>
</div></section>

<section class="band"><div class="wrap split">
  <div>
    <p class="eyebrow">Organizas uma batalha?</p>
    <h2>Leva o Kopa.11 para a tua roda</h2>
    <p class="lede" style="margin-top:1rem">Prémio para o vencedor, peça exclusiva do evento ou um episódio do podcast gravado no sítio. Diz-nos o que é e quando é.</p>
  </div>
  <div>
    <form name="evento" method="POST" data-netlify="true" netlify-honeypot="site" action="obrigado.html">
      <input type="hidden" name="form-name" value="evento">
      <p hidden><label>Site <input name="site" id="hp3"></label></p>
      <div class="field"><label for="e-nome">Evento</label><input id="e-nome" name="evento" required></div>
      <div class="field"><label for="e-local">Cidade e data</label><input id="e-local" name="local_data" required></div>
      <div class="field"><label for="e-contacto">Contacto (Instagram, email ou WhatsApp)</label><input id="e-contacto" name="contacto" required></div>
      <button class="btn solid" type="submit">Propor</button>
    </form>
    <div class="ok">Recebido. Falamos em breve.</div>
  </div>
</div></section>
'''

OBRIGADO = f'''
<section class="hero"><div class="wrap">
  <p class="eyebrow">Recebido</p>
  <h1><span>Estás</span><span class="o">dentro.</span></h1>
  <p class="lede">Avisamos antes de abrir. Até lá, o live continua em @kopa11_oficial.</p>
  <div class="cta-row"><a class="btn solid" href="index.html">Voltar ao início</a><a class="btn" href="{IG}" target="_blank" rel="noopener">Instagram</a></div>
</div></section>
'''

PAGES = {
    'index': ('Kopa.11', 'Streetwear e cultura hip hop da Margem Sul: podcast em direto, Team Kopa, batalhas de freestyle e drops limitados.', HOME),
    'podcast': ('É quase um podcast… mas · Kopa.11', 'O podcast em direto do Kopa.11, com Kota Phill e Concept no Bunker. Episódios da 2.ª temporada.', PODCAST),
    'team-kopa': ('Team Kopa · Kopa.11', 'A crew de MCs que veste o Kopa.11 e a leva às batalhas de freestyle.', TEAM),
    'drop': ('Drop · Kopa.11', 'Drops limitados do Kopa.11. Entra na lista para saber primeiro a data e ter acesso antecipado.', DROP),
    'eventos': ('Eventos · Kopa.11', 'Batalhas de freestyle, lives e colaborações do Kopa.11.', EVENTOS),
    'obrigado': ('Recebido · Kopa.11', 'Inscrição recebida.', OBRIGADO),
}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'assets').mkdir(parents=True)
    shutil.copy(HERE / 'assets' / 'site.css', OUT / 'assets' / 'site.css')
    shutil.copy(HERE / 'assets' / 'logo.svg', OUT / 'assets' / 'logo.svg')
    if (HERE / 'media').exists() and any((HERE / 'media').iterdir()):
        shutil.copytree(HERE / 'media', OUT / 'media')
    for slug, (title, desc, body) in PAGES.items():
        (OUT / f'{slug}.html').write_text(shell(slug, title, desc, body), encoding='utf-8')
    if MODE == 'site':
        for f in (HERE / 'netlify').iterdir():
            shutil.copy(f, OUT / f.name)
    print(f'{MODE}: {len(PAGES)} páginas em {OUT}')


if __name__ == '__main__':
    main()
