# -*- coding: utf-8 -*-
import io, os
D = os.path.dirname(os.path.abspath(__file__))
TINTA, ROSA, ROSAE, BLUSH = '#2B1D21', '#C25C77', '#8E3A52', '#F8EFEA'

def ler(n): return io.open(os.path.join(D, n), encoding='utf-8').read()
def mono(s, cor):   return s.replace(ROSA, cor).replace(ROSAE, cor).replace(TINTA, cor)
def sem_tam(s):     # deixa o SVG escalar pelo CSS
    import re
    return re.sub(r'\swidth="[\d.]+"\sheight="[\d.]+"', '', s, count=1)

DIRS = [
 ('A', 'Pérola', 'A-perola-principal.svg', 'A-perola-monograma.svg',
  'Casa de moda. O <strong>O de TODA é um anel perfeito</strong> — lê-se como letra e como pérola. '
  'Serifa de alto contraste, muito espaço, nada a mais. É a direção mais intemporal: daqui a cinco anos não envelheceu.'),
 ('B', 'Assinatura', 'B-assinatura-principal.svg', 'B-assinatura-monograma.svg',
  'A evolução do que ela já tem. Mantém o par <strong>maiúsculas + manuscrito</strong> que ela escolheu, '
  'mas plano, sem metal nem brilhos, com o script a cruzar por baixo. É a que ela vai reconhecer como sua.'),
 ('C', 'Laço', 'C-laco-principal.svg', 'C-laco-monograma.svg',
  'O laço que já estava no logótipo, reduzido ao essencial e desenhado a régua. '
  'Serve <strong>roupa, bijuteria, cosméticos e casa</strong> — um cabide só servia roupa. '
  'É a única com um símbolo que vive sozinho: etiqueta, autocolante, saco, story.'),
]

blocos = []
for letra, nome, fp, fm, texto in DIRS:
    principal = sem_tam(ler(fp)); monograma = sem_tam(ler(fm))
    blocos.append('''
<section class="dir">
  <div class="cab">
    <span class="letra">{letra}</span>
    <div>
      <h2>{nome}</h2>
      <p class="razao">{texto}</p>
    </div>
  </div>

  <div class="palco">{principal}</div>

  <div class="provas">
    <figure>
      <div class="caixa claro">{monograma}</div>
      <figcaption>Monograma<br><span>selo, avatar, etiqueta</span></figcaption>
    </figure>
    <figure>
      <div class="caixa claro">{mono_peq}</div>
      <figcaption>Uma cor<br><span>carimbo, fatura, saco de papel</span></figcaption>
    </figure>
    <figure>
      <div class="caixa rosa">{inv}</div>
      <figcaption>Invertido<br><span>sobre a cor da marca</span></figcaption>
    </figure>
    <figure>
      <div class="caixa claro favis">
        <span class="fav f32">{monograma}</span>
        <span class="fav f16">{monograma}</span>
      </div>
      <figcaption>32px e 16px<br><span>favicon, separador do browser</span></figcaption>
    </figure>
  </div>
</section>'''.format(letra=letra, nome=nome, texto=texto, principal=principal,
                    monograma=monograma,
                    mono_peq=sem_tam(mono(ler(fp), TINTA)),
                    inv=sem_tam(mono(ler(fp), '#FFFFFF'))))

html = '''<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Toda Chic — três propostas de logótipo</title>
<style>
:root{{--tinta:{TINTA};--rosa:{ROSA};--rosae:{ROSAE};--blush:{BLUSH};--linha:rgba(43,29,33,.14)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--blush);color:var(--tinta);font:400 17px/1.65 ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
.folha{{max-width:1080px;margin:0 auto;padding:clamp(2rem,5vw,4.5rem) clamp(1.25rem,4vw,3rem) 5rem}}
header.topo{{border-bottom:1.5px solid var(--linha);padding-bottom:2rem;margin-bottom:3.5rem}}
header.topo h1{{font-size:clamp(1.9rem,4.5vw,2.9rem);font-weight:400;letter-spacing:-.01em;line-height:1.1}}
header.topo p{{margin-top:.9rem;color:var(--rosae);max-width:62ch}}
header.topo .quem{{margin-top:1.4rem;font-size:15px;color:rgba(43,29,33,.6)}}
.dir{{padding:3.5rem 0;border-bottom:1.5px solid var(--linha)}}
.cab{{display:flex;gap:1.6rem;align-items:flex-start;margin-bottom:2.6rem}}
.letra{{flex:none;width:52px;height:52px;border:1.5px solid var(--rosa);border-radius:50%;
  display:grid;place-items:center;color:var(--rosa);font-size:20px}}
.dir h2{{font-size:clamp(1.5rem,3.4vw,2.1rem);font-weight:400;letter-spacing:-.01em}}
.razao{{margin-top:.7rem;color:rgba(43,29,33,.74);max-width:68ch}}
.razao strong{{color:var(--tinta);font-weight:600}}
.palco{{background:#fff;border-radius:14px;padding:clamp(2rem,6vw,4rem);display:grid;place-items:center;min-height:230px}}
.palco svg{{height:clamp(110px,16vw,178px);width:auto;max-width:100%}}
.provas{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.1rem;margin-top:1.1rem}}
.caixa{{border-radius:12px;display:grid;place-items:center;padding:1.4rem;min-height:130px}}
.caixa.claro{{background:#fff}}
.caixa.rosa{{background:var(--rosa)}}
.caixa svg{{width:100%;max-width:190px;height:auto;max-height:74px}}
.caixa.claro > svg[viewBox="0 0 100 100"]{{max-width:70px;max-height:70px}}
.favis{{gap:1.4rem;grid-auto-flow:column}}
.fav{{display:inline-grid;place-items:center}}
.fav svg{{height:auto}}
.f32 svg{{width:32px;max-width:32px}}
.f16 svg{{width:16px;max-width:16px}}
figcaption{{margin-top:.7rem;font-size:14px;color:rgba(43,29,33,.62);text-align:center;line-height:1.35}}
figcaption span{{font-size:13px;color:rgba(43,29,33,.45)}}
.paleta{{padding-top:3.5rem}}
.paleta h2{{font-size:1.5rem;font-weight:400;margin-bottom:1.4rem}}
.cores{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.1rem}}
.cor{{border-radius:12px;overflow:hidden;background:#fff}}
.cor .amostra{{height:84px}}
.cor .nome{{padding:.8rem 1rem;font-size:14px}}
.cor code{{display:block;color:rgba(43,29,33,.55);font-size:13px;margin-top:.15rem}}
.nota{{margin-top:3rem;padding:1.6rem 1.8rem;background:#fff;border-radius:12px;font-size:16px;color:rgba(43,29,33,.78)}}
.nota strong{{color:var(--tinta)}}
@media(max-width:780px){{
  .provas,.cores{{grid-template-columns:repeat(2,1fr)}}
  .cab{{gap:1rem}}
}}
</style>
</head>
<body>
<div class="folha">
<header class="topo">
  <h1>Toda Chic — três propostas de logótipo</h1>
  <p>Todas vetoriais, todas com o nome e a assinatura <em>“Embeleza-te connosco”</em>, todas em tons de rosa.
     Cada uma é mostrada como vai mesmo aparecer: sozinha, a uma cor, invertida e ao tamanho de um favicon.</p>
  <p class="quem">Pacheco Studios · 20 de setembro de 2026</p>
</header>
{blocos}
<section class="paleta">
  <h2>Paleta</h2>
  <div class="cores">
    <div class="cor"><div class="amostra" style="background:{TINTA}"></div><div class="nome">Tinta<code>{TINTA}</code></div></div>
    <div class="cor"><div class="amostra" style="background:{ROSA}"></div><div class="nome">Rosa da marca<code>{ROSA}</code></div></div>
    <div class="cor"><div class="amostra" style="background:{ROSAE}"></div><div class="nome">Rosa escuro<code>{ROSAE}</code></div></div>
    <div class="cor"><div class="amostra" style="background:{BLUSH};box-shadow:inset 0 0 0 1px rgba(43,29,33,.1)"></div><div class="nome">Blush<code>{BLUSH}</code></div></div>
  </div>
  <div class="nota">
    <strong>Porquê estes rosas.</strong> O rosa do logótipo atual é um efeito metálico: só existe em ecrã e desaparece
    quando se imprime a uma cor ou se borda numa etiqueta. Estes são rosas verdadeiros, com contraste suficiente
    para texto, e o blush mantém o ambiente quente que ela já tinha escolhido.
  </div>
</section>
</div>
</body>
</html>'''.format(TINTA=TINTA, ROSA=ROSA, ROSAE=ROSAE, BLUSH=BLUSH, blocos=''.join(blocos))

io.open(os.path.join(D,'propostas-logo.html'),'w',encoding='utf-8').write(html)
print('prancha escrita: %d KB' % (len(html)/1024))
