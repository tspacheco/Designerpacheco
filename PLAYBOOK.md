# PACHECO STUDIOS — PLAYBOOK MESTRE

> Fonte de verdade da Pacheco Studios. Substitui todo o histórico de chats.
> Última atualização: 23/09/2026 (integrado no repositório + padrão NÍVEL 10K)

## 0. COMO USAR

- Este playbook vive neste repositório e é carregado automaticamente em cada sessão (via `CLAUDE.md`). Já não é preciso anexar PDF.
- Sessão nova → escreve só o que queres desta sessão. Exemplo: *"Cria sites para: Casa da Igreja (Cacela Velha) e Pizzadela (VNC). Segue o engine."*
- **Regra de ouro:** um chat = um lote (máx. 5-6 sites). Depois disso, chat novo.
- Conversas longas consomem créditos exponencialmente — o contexto inteiro é reprocessado a cada mensagem.

## 1. CONTEXTO

- **Tomás Pacheco**, fundador da Pacheco Studios — agência solo de web design + marketing digital, Algarve.
- Estudante de Economia na UAlg (campus de Gambelas).
- Responder **SEMPRE em PT-PT**, tom direto, sem enchimento. Respostas curtas (leitura em telemóvel).
- **Método:** sites de demonstração criados antes da abordagem, apresentados presencialmente no telemóvel/tablet.
- **Stack:** HTML single-file → Netlify (drag & drop do zip) ou Hostinger (zip sem `netlify.toml`, extrair em `public_html`).

## 2. MODELO DE PREÇOS

| Modalidade | Preço |
|---|---|
| Website avulso | 500 € (pagamento único) |
| Website + manutenção | 500 € + 50 €/mês |
| Desconto de grupo (2+ casas do mesmo dono) | 400 € + 40 €/mês |
| Setup sistema faturas WhatsApp | 150-300 € + 39-59 €/mês |

Incluído na mensalidade: manutenção (site sempre online), domínio pago por nós, alterações garantidas em 1 semana, suporte direto, sem custos escondidos.

Contacto nas propostas: tspacheco26@gmail.com *(falta acrescentar telefone)*

**Posicionamento de produto:** o preço de venda é o da tabela, mas a qualidade entregue é de site de 10 000 € — ver secção 3-A. É esse contraste que fecha vendas.

## 3. ENGINE DOS SITES — REGRAS OBRIGATÓRIAS

### Estrutura

- Um único ficheiro HTML, CSS e JS embutidos. Zero dependências externas exceto Google Fonts e o iframe do mapa.
- `<html lang="pt-PT">` · exatamente um `<h1>` · `<meta viewport>` com `viewport-fit=cover`.
- CSS custom properties (`:root`) para toda a paleta.
- Nav fixa que muda no scroll (`.nav.scrolled`) + burger acessível (`aria-expanded`).
- Revelação no scroll: `IntersectionObserver` sobre `.rv`, classes `.d1`/`.d2` para atraso escalonado.
- Marquee horizontal (faixa de palavras-chave) entre o herói e a primeira secção.
- JSON-LD `Restaurant` com morada, telefone, `aggregateRating` e `openingHoursSpecification` quando existirem.
- `@media (prefers-reduced-motion: reduce)` a desligar todas as animações.
- `:focus-visible` com outline visível em todos os botões e links.
- Rodapé com link para https://www.livroreclamacoes.pt/inicio (obrigatório por lei em PT).
- Banner no topo: `APRESENTAÇÃO PACHECO STUDIOS · ...` — remover na versão de produção quando o cliente compra.

### Regra HONEST-DATA (nunca quebrar)

- Nunca inventar ratings, preços, telefones, horários ou citações.
- Rating fraco (< 4,2) → omitir, não mostrar. Rating forte → destacar com o nº de avaliações.
- Dado não confirmado → escrever literalmente **"a confirmar"**.
- Citações de clientes → parafrasear ("sentido geral das avaliações públicas"), nunca copiar texto integral.
- Preços só se vierem de ementa fotografada ou do site oficial do cliente.

### IMAGENS — regra aprendida a 28/07/2026

Hotlinks externos falham (Wikimedia, TripAdvisor, agregadores bloqueiam por referrer/hotlink protection). Fazer sempre assim:

1. Fundo desenhado em **SVG inline** (cena, gradiente, ilustração) → aparece sempre, zero dependências.
2. Por cima, camada opcional `<img src="media/hero.jpg" onerror="this.parentElement.remove()">`.
3. Incluir no zip uma pasta `media/` com `LEIA-ME.txt` a explicar ao cliente que basta lá pôr `hero.jpg`.

**Prints de carrossel do Instagram (aprendido a 23/09/2026):** trazem faixa cinzenta `#565656` à esquerda (11–16 px), linhas pretas no topo (4–19 px) e botões ‹ › a meio (≈ 36 px, translúcidos) + 3 pontos em baixo. Cortar as bordas por coluna/linha uniforme, e apagar os botões com **retalho deslocado na vertical** em texturas (calçada, relva) ou `cv2.inpaint` TELEA em zonas desfocadas/escuras — o TELEA em calçada deixa mancha. Escolher por botão, ver `media/croae-moita/`.

Exceção testada e funcional: fotos do CDN do Google (`lh3.googleusercontent.com/...=s1600`) do perfil do próprio negócio — funcionam, mas usar sempre com `onerror` de fallback.

### Hero em telemóvel

Foto/cena de fundo + `.hero-shade` com gradiente escuro reforçado abaixo dos 680px, texto alinhado em baixo. **Legibilidade acima de tudo.**

## 3-A. PADRÃO NÍVEL 10K (novo — 30/07/2026)

O que separa um site de 500 € de um de 10 000 €, e que passa a ser obrigatório em cada demo:

1. **Direção de arte por cliente, não template.** Cada site parte do mundo real do negócio (materiais, gestos, vernáculo — as brasas, a cataplana, o presunto pendurado) e assume **um risco estético justificável**. Usar o skill `frontend-design` como processo: brainstorm → explorar direções → plano → crítica → construir → crítica final.
2. **Design system consciente.** Antes de escrever CSS, correr o skill `ui-ux-pro-max` para o tipo de produto (paleta, par tipográfico, estilo) e adaptar — nunca aceitar o primeiro resultado sem crítica.
3. **Tipografia como identidade.** Par display+corpo escolhido de propósito para aquele cliente (respeitar o tracker da secção 6), escala tipográfica clara, pesos e espaçamentos intencionais.
4. **Motion coreografado, não espalhado.** Uma sequência de entrada orquestrada no herói + micro-interações discretas valem mais do que dez efeitos soltos. Menos, mas irrepreensível.
5. **Copy com voz.** Texto que soa ao dono do negócio, não a brochura genérica. Zero clichés ("paixão pela cozinha", "ingredientes frescos") sem prova concreta.
6. **Detalhe de execução.** Espaçamento consistente em toda a página, estados hover/focus/active desenhados, contraste AA, dark shade no hero móvel, 60fps nas animações (só `transform`/`opacity`).
7. **Crítica final obrigatória.** Antes de empacotar: "isto podia ser confundido com um template? O que é que só este cliente podia ter?" Se a resposta for fraca, refazer a assinatura visual.

Tudo isto **dentro** das regras do engine (single-file, HONEST-DATA, acessibilidade) — o nível 10K é execução, não complexidade técnica.

## 3-A-bis. SITES ENTREGUES SEM MANUTENÇÃO (aprendido a 23/09/2026 — CROAE Moita)

Quando o cliente compra o site avulso e ninguém vai atualizar nada, a direção de arte **não pode depender de dados que mudam** (lista de animais, stock, ocupação, "novidades"). Perguntar isto no brief antes de desenhar. Regras:
- Conteúdo vivo → apontar para onde ele já vive (Instagram, telefone), não replicar.
- O que o cliente possa querer acrescentar entra **por ficheiros de nome fixo** (`media/galeria/01…30.jpg`, `media/parceiros/01…12.png`, `media/video/x.mp4`) com `onerror` a esconder o que falta e um `LEIA-ME.txt` por pasta. Zero edição de HTML.
- Nada "a confirmar" pode ir para produção: ou se confirma ou se corta antes de entregar.
- Assinatura visual assente em algo permanente do cliente (um objeto, um gesto, um slogan), nunca num número que envelhece.
- **Capturas de carrossel do Instagram em lote** (23/09): `sites/croae-moita/ferramentas/limpa-lote.py` — corta a faixa cinzenta à esquerda, apaga os botões ‹ › por correspondência de padrão (`tpl_botao.npy`; aceitar ≥0,5 se estiver na margem a meio da altura, ≥0,85 noutro sítio) e **corta os últimos 40 px** em vez de tentar apagar os pontos (a deteção dos pontos falha em fundos claros; o corte nunca falha). Verificar sempre com a folha `verificacao_*.png` que o script gera.

## 3-B. SITES COM 3D / REACT (novo — 30/08/2026)

Quando um site precisa de React, Three.js ou outra biblioteca, a regra do ficheiro único **mantém-se** — muda só a forma:

- **Embutir as bibliotecas no próprio HTML**, não carregá-las por CDN. Obtêm-se pelo registo npm (`npm i react react-dom three`) e copiam-se os builds UMD (`umd/*.production.min.js`, `build/three.min.js`) para dentro de `<script>` no ficheiro. Escapar `</script>` para `<\/script>`.
- **Fontes também embutidas** em base64 (`data:font/woff2;base64,...`), extraídas do CSS do Google Fonts. Isto resolve de vez o problema de a fonte display não carregar.
- Resultado: um `index.html` de ~1 MB (≈450 KB no zip) que **abre sem rede nenhuma** — decisivo para apresentar ao telemóvel à porta do cliente, com má rede. O único pedido externo que resta é o iframe do mapa.
- **`<noscript>` obrigatório** com nome, morada, telefone, horário e link do Livro de Reclamações: o conteúdo é renderizado por JS e os motores de busca não podem ficar sem o essencial.
- Cena 3D: respeitar `prefers-reduced-motion` (renderizar um só fotograma), reduzir partículas e pixel ratio abaixo dos 820px, e `try/catch` no `WebGLRenderer` a esconder o canvas se não houver WebGL.
- Cuidado conhecido: `backdrop-filter` numa nav cria um bloco de contenção e parte qualquer menu `position:fixed` lá dentro. Usar fundo sólido.

## 4. BASH DE VALIDAÇÃO + EMPACOTAMENTO

```bash
cd /home/claude/cafes-faro
[ -f netlify.toml ] || cat > netlify.toml <<'TOML'
[build]
publish = "."
[[headers]]
for = "/*"
[headers.values]
X-Content-Type-Options = "nosniff"
Referrer-Policy = "strict-origin-when-crossorigin"
TOML
for f in NOME1 NOME2 NOME3; do
python3 -c "
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.st=[]; s.er=[]; s.v={'meta','link','img','br','hr','input','source','iframe','path','circle','svg','rect','use','line','polyline','canvas','ellipse','animate','text','template','g','defs','textPath','tr','td','stop','linearGradient','figcaption'}; s.insvg=0
    def handle_starttag(s,t,a):
        if t=='svg': s.insvg+=1
        if t not in s.v and not s.insvg: s.st.append(t)
    def handle_endtag(s,t):
        if t=='svg' and s.insvg: s.insvg-=1; return
        if s.insvg: return
        if s.st and s.st[-1]==t: s.st.pop()
        elif t in s.st:
            while s.st and s.st[-1]!=t: s.er.append('x'+s.st.pop())
            s.st.pop()
p=P(); p.feed(open('$f.html',encoding='utf-8').read())
h=open('$f.html',encoding='utf-8').read()
ok=(not p.st and not p.er)
print('$f:', 'HTML-OK' if ok else 'ERRO'+str(p.st[-4:])+str(p.er[-4:]),
      '| h1:'+str(h.count('<h1')),
      '| ptPT' if 'lang=\"pt-PT\"' in h else '| SEM-LANG',
      '| banner' if 'PACHECO' in h else '| SEM-BANNER',
      '| legal' if 'livroreclamacoes' in h else '| SEM-LEGAL',
      '| U+FFFD:'+str(h.count(chr(0xfffd))))
"
cp $f.html /mnt/user-data/outputs/$f.html
rm -rf /tmp/$f && mkdir -p /tmp/$f && cp $f.html /tmp/$f/index.html && cp netlify.toml /tmp/$f/
( cd /tmp/$f && rm -f /mnt/user-data/outputs/$f-netlify.zip && zip -q /mnt/user-data/outputs/$f-netlify.zip index.html netlify.toml )
done
```

Verificação extra depois de escrever SVG: confirmar que todos os `stop-color` e `fill` são hex ASCII válidos.

```bash
grep -o 'stop-color="[^"]*"' FICHEIRO.html | sort -u
```

**Variante Hostinger:** o mesmo zip **sem** `netlify.toml`. Instruções ao cliente: hPanel → Gestor de Ficheiros → `public_html` → Upload → Extrair → apagar `default.php`. (O `index.html` tem de ficar na raiz de `public_html`.)

## 5. ASSINATURAS VISUAIS JÁ USADAS (não repetir — inventar nova em cada site)

ensō japonês · mandala · tagliatelle a cair · brasas a subir · rubrica manuscrita · ondas de açúcar + canela · folha line-art a desenhar-se · anéis de fumo + selo rotativo · bandeirolas náuticas a balançar · pincelada a pintar-se + blobs · pedra com heat-haze · pizza a girar + textura de tijolo · grelha com sardinhas + fumo · riscas de toalha + cataplana · notas musicais a flutuar · cena de praia em SVG (céu/mar/areia) · veios de marmoreio a desenharem-se + barra de pontos de cozedura + "00:00" monumental (Mr. Buffalo) · corvo a pousar no título + espinha de peixe divisora (Casa Corvo) · cardume SVG a atravessar a página (Paulo Molina) · padrão de azulejo a compor-se (Iguarias da Vila) · coral a ramificar-se em stroke-draw (O Coral) · mesa KBBQ vista de cima — grelha concêntrica + banchan a pousar (Hanam) · ecrã dividido diagonal "Forno & Mar" com mouse-follow + palavras gigantes de fundo (Catarina) · espeto 3D a girar sobre a grelha de água da ria, brasas e fagulhas em WebGL (Frango da Ria) · **"O Mostruário"** — cartões de amostra sobre blush, chips de cor reais, notas de tamanho/stock em monoespaçada como etiquetas de costureira, herói cinematográfico com a dona na loja (Toda Chic) · **"Nuvens de especiarias"** — herói-vídeo generativo em canvas determinístico (açafrão, pimentão, cardamomo, grãos de basmati), exportável em MP4 com o mesmo código (Pinhal Novo Mercado and Ria) · **carta escrita como o letreiro** — placas vermelhas em Khand que se acendem, sobre a foto real da fachada (Pinhal Novo Restaurant) · **"A trela"** (→ CROAE Moita) — a trela verde das fotos dos passeios vira uma linha contínua que sai do herói, corre pela margem e se desenha com o scroll até à etiqueta "Chegaste." nos contactos; bandana amarela nos CTAs. *(A ideia "40 boxes" foi descartada: dependia de dados que mudam e o site é entregue sem manutenção.)*

## 6. TRACKER DE FONTES DISPLAY (já usadas — escolher sempre uma nova)

Saira Condensed · Abril Fatface · Gilda Display · Archivo Black · Alfa Slab One · Zilla Slab · Fraunces · Playfair · Rozha One · Cinzel · Anton · Yeseva One · DM Serif Display · Bricolage Grotesque · Cormorant Garamond · Marcellus · Bitter · Bodoni Moda · Big Shoulders Display · Yatra One · Libre Caslon Display · Shippori Mincho · Eczar · Bebas Neue · Spectral · Prata · Syne · Ultra · Sora · Unbounded · Staatliches · Crete Round · Averia Serif Libre · Passion One · Gloock · Instrument Serif (→ Mr. Buffalo) · Young Serif (→ Casa Corvo; repetida no Catarina por pedido explícito do brief V2 — zonas diferentes) · Chonburi (→ Paulo Molina) · Newsreader (→ Iguarias da Vila) · Lilita One (→ O Coral) · Bungee (→ Hanam KBBQ) · Erica One (→ Frango da Ria) · Italiana (→ Toda Chic, com Jost no corpo e Courier Prime nas notas) · Martel 900 (→ Pinhal Novo Mercado and Ria, com Mukta no corpo — par devanagari-latino, a pensar na comunidade sul-asiática) · Khand 700 (→ Pinhal Novo Restaurant, com Hind no corpo — condensada de sinalética, como o letreiro)

**Livres/planeadas:** Bevan (→ Sítio dos Presuntos) · Rye · Kufam .

Usadas a 23/09: Gabarito 800/900 (→ CROAE Moita, com Atkinson Hyperlegible no corpo — legibilidade para serviço público).

*(Caveat e Kalam são fontes de acento manuscrito — podem repetir.)*

## 7. CATÁLOGO — SITES JÁ CRIADOS

### ★ VENDIDO

| Cliente | Notas |
|---|---|
| Grupo Naval (Olhão) | **1.ª VENDA FECHADA.** 4,3★/1.041, tel 289 050 543, Av. 5 de Outubro. Banner Pacheco removido. Pendente: ementa do Carlos, canonical quando houver domínio, fotos próprias. |

### Loja online — cliente real em curso

| Cliente | Notas |
|---|---|
| Toda Chic (roupa feminina online, IG @_toda.chiic) | `sites/toda-chic/` — **mundo Mostruário escolhido** (21/09). `index.html` gerado por `ferramentas/build.py` a partir de `index.src.html` + `catalogo.json` (72 peças transcritas das fichas da dona) + fotos limpas por `ferramentas/fotos.py` → `media/`. Loja de demonstração completa com a **estrutura ditada pela dona** (5 categorias com os nomes dela + Bijuteria/Cosméticos/Casa/Promoções + estações Nova coleção/Inverno/Meia-estação/Verão): vitrine de categorias como destaque da página inicial, ficha por peça (cor → foto, tamanho, unidades, guia de tamanhos), favoritos e saco a funcionar (localStorage), páginas legais com o que falta marcado. Peças fora das categorias dela em "Por arrumar" e estações provisórias — ajustar com ela no fim. WhatsApp 933 668 148, MB WAY. Plataforma final: WooCommerce + ifthenpay. Registo da política de devoluções imposta em `REGISTO-devolucoes.md`. |

### Clientes com site próprio já entregue (edições)

| Cliente | Notas |
|---|---|
| Simona's O Bom Paladar (Loulé) | Rebrand + ementa real completa (preços das fotos) + secção Garrafeira & Bar. Zips Netlify e Hostinger entregues. Canonical aponta bompaladarloule.pt — atualizar. |
| ProBuilders (construção, Algarve) | H1 do herói removido (mantido sr-only para SEO), hero limpo para vídeo, nav móvel em 2 linhas sem burger. |

### Demos criadas (por zona)

- **Albufeira:** prime-sushi · delhi-6-bistro · ita-trattoria (já tem site — ângulo redesign) · nabrasa-bbq · clara-barriga-advogada · ondas-dacucar · cbweed-albufeira · shalom-ribs
- **Olhão:** grupo-naval-olhao ★
- **Gambelas/Faro:** uarte-gambelas (tel 967 597 927 vs 289 047 001 — CONFIRMAR à porta)
- **Vila Nova de Cacela / Manta Rota:** sabinos · urban-oven · a-camponesa · cacela-mar · tavont
- **Monte Gordo / Altura:** mr-buffalo (`sites/mr-buffalo/`) — steakhouse 4,8★/80 TA, Travelers' Choice, trilingue PT/EN/ES, direção "Brasa e Mármore", Instrument Serif + Figtree, CTA WhatsApp +351 913 619 433. Morada/carta/preços a confirmar.
- **Quarteira:** hanam-kbbq (`sites/hanam-kbbq/`) — Hanam Korean Barbecue "The Original", R. Vasco da Gama 70. 4,9★/497 Google, TheFork 9,5 (CTA de reserva real), TA 5,0, 15–35 €, fecha 23:00, IG @hanam_korean_barbecue. Bilingue PT/EN, Bungee, assinatura "mesa KBBQ vista de cima". Tel/horário abertura/carta a confirmar; fotos do cliente por obter (slots media/ prontos).
- **Altura:** pizzaria-catarina (`sites/pizzaria-catarina/`) — "Forno & Mar" V2 vibrante, TA 3,9★/238 nº5/37, trilingue PT/EN/ES, Young Serif + Schibsted Grotesk, proposta dupla site + sessão fotográfica (shot list no HTML), tel 281 957 492, todos os dias 12–15/19–23. Validado com `impeccable detect`.
- **Quarteira:** hanam-kbbq (`sites/hanam-kbbq/`) — ver acima.
- **Moncarapacho / Olhão:** frango-da-ria (`sites/frango-da-ria/`) — churrasqueira, 4,3★/1.586 (Restaurant Guru), EN125 Alfândega-Bias do Sul, fecha à terça. Direção "Entre a brasa e a ria": **React + Three.js**, espeto 3D a girar sobre brasas e sobre a ria. Erica One + Manrope, PT/EN. Passa `impeccable detect` sem findings. Telefone e Tripadvisor a confirmar (fontes divergem).
- **Pinhal Novo (Palmela) — dois sites, mesmo dono:** pinhal-novo-mercado (`sites/pinhal-novo-mercado/`) — **Pinhal Novo Mercado and Ria** (ficha Google `g/11l2h1fz7y`, 38.632305/−8.914796): herói em vídeo-montagem das fotografias reais da loja (entrada → corredores → telemóveis; MP4+WebM 16:9 e 9:16 em `media/video/`, gerados por `video-montagem.js`), uma secção por família (Mercearia, Peixe, Drogaria, Telemóvel, Bebidas e snacks, Ao balcão) cada uma com cor e animação próprias, Peixe e Drogaria com fotografia animada (revelação, varrimento de luz, etiquetas); Martel + Mukta. · pinhal-novo-restaurant (`sites/pinhal-novo-restaurant/`) — **Pinhal Novo Restaurant** (kebab, pizza, cozinha indiana; sem ficha no Google): abertura com a foto real da fachada, carta em placas vermelhas; Khand + Hind. PT/EN nos dois; cada um aponta para o outro. **Tudo a confirmar:** morada, horário, telefone, carta e preços, lista de artigos (a Google bloqueada nesta sessão). Ângulo de venda: o restaurante ainda não aparece no Maps — criar a ficha e ligar os dois é parte do serviço.
- **Moita (Setúbal) — cliente institucional/ONG:** croae-moita (`sites/croae-moita/`) — Centro de Recolha Oficial de Animais Errantes, gerido pelo Gabinete Veterinário Municipal. Pesquisa em `research/croae-moita.md`; arquitetura em `sites/croae-moita/ARQUITETURA.md` (direção "As 40 boxes", secção de parcerias pedida no brief). Fotos do Instagram limpas em `media/croae-moita/` (pasta de entrada dos uploads do Tomás). **Site multi-página construído (23/09, v2):** `index` · `adotar` · `ajudar` · `parceiros` · `galeria` · `centro`, cada página um HTML auto-contido gerado por `ferramentas/build.py` a partir de `src/` (base.css/js, nav, footer, `pages/*.html` com blocos META/CSS/JS). Direção "A trela" (ver secção 5), JSON-LD `AnimalShelter`, Gabarito + Atkinson Hyperlegible. **Entregue sem manutenção:** zero conteúdo que mude (sem lista de animais — aponta para o Instagram e o telefone); o cliente acrescenta conteúdo por ficheiros de nome fixo — `media/galeria/01…30.jpg`, `media/parceiros/01…12.png`, `media/video/centro.mp4` — cada pasta com LEIA-ME. Tel 212 806 816 / 962 049 674, gab.vetmun@cm-moita.pt. Morada, horário, fichas dos animais, parceiros e níveis de parceria a confirmar. Exceção assumida à regra single-file: o cliente pediu multi-página; cada página continua auto-contida.
- **Fuzeta** (pesquisa em `research/fuzeta.md`): casa-corvo (4,6★ RG/2.091, peixe frito, sem reservas — Young Serif, corvo + espinha) · paulo-molina (4,5★ RG/55, artigo VERSA "mestre Rui" — Chonburi, cardume; contactos a confirmar) · iguarias-da-vila (4,5★ TA nº5/32, TheFork, música ao vivo — Newsreader, azulejos; **já tem site → ângulo "elevar, não substituir"**) · o-coral (4,5★ RG/162, menu do dia — Lilita One, coral a ramificar)

### Propostas PDF (reportlab)

- Layout navy `#142238` + dourado `#C59A3E`. Script-tipo: `/home/claude/proposta_shalom.py` (dicionário T com pt/en).
- Royal Food — 600 € tudo incluído, âncora 500 € riscada.
- Grupo Shalom / Ido — 500 € + 50 €/mês, caixa dourada "PARA O GRUPO −20%" → 400 € + 40 €/mês. Nunca dizer "família Shalom" nem o número de restaurantes — usar "o seu grupo de restaurantes". Versões PT + EN.

## 8. VÍDEO (prompts — modelo recomendado: Kling 3.0 standard)

- Escrever prompts em inglês, com números explícitos ("1 pair of tongs", "4 blurred hands").
- Sequências com 3+ etapas → dividir em 2 clips de 5s e colar no CapCut.
- Slogans e texto entram em pós-produção, nunca no prompt.
- Negative padrão: `static camera, still pose, standing still, text, watermark, logos, real human faces, distorted hands, extra limbs, blurry, style change` (+ `raw meat, burnt black meat, plastic-looking food` para comida; + `building deformation, façade changing shape` para arquitetura/time-lapse).
- Prompts já entregues: Shalom Ribs (brasa → queda → time-lapse de ossos) · Restaurante Avenida (time-lapse da fachada, "Várias gerações por aqui passaram").

## 9. SISTEMA DE FATURAS WHATSAPP (blueprint entregue)

Twilio (nunca Evolution/Baileys — banimento Meta) → n8n → ler QR Code da AT (Portaria 195/2020, campos A-S) → fallback Claude Vision → Supabase região UE (`restaurants` / `invoices` / `raw_messages`, RLS) → confirmação por WhatsApp → relatório mensal CSV+ZIP ao contabilista.

- **Legal:** DL 28/2019 — arquivo digital válido, papel destruível após dedução do IVA, conservar 10 anos.
- Custo ~1-3 €/restaurante/mês (3-6 € após 01/10/2026, quando a Meta passa a cobrar mensagens de serviço).
- Concorrente direto: Robot de Arquivo do TOConline. **Diferenciador: zero app, só WhatsApp.**

## 10. PENDENTES

- [ ] **CROAE Moita** — demo multi-página v2 feita ("A trela", sem manutenção). Fotos (19 capturas do Instagram limpas em lote com `ferramentas/limpa-lote.py` → `media/galeria/01–22.jpg`) e 2 vídeos (`media/video/akira.mp4`, `gatinhos.mp4`, recodificados 720p faststart) já no site. Falta: logótipos de parceiros; ficha de voluntário (link/idade) e condições da FAT ainda "a confirmar" na página Ajudar; saber se o site é da Câmara ou de voluntários. Quando houver fotos novas: `limpa-lote.py PASTA media/galeria 23`, correr `build.py`.
- [ ] **Sítio dos Presuntos** (Gambelas/Montenegro) — site por criar. Tasca beirã, donos de Viseu, R. Aquilino Ribeiro (nº 122 vs 212 a confirmar), tel 917 823 784 (TA) / 919 869 212 (booktables), Google 4,3/~1.220, até às 23:00. Pratos: presunto, leitão, tamboril, lula grelhada, sopa de feijão verde. Identidade planeada: Bevan, presuntos pendurados a balançar.
- [ ] **O Caseiro2** (ex-"O Bandeira", Montenegro) — 4,6★/438, menu de almoço ~12 €, fecha 2.ª feira. Site se houver interesse.
- [ ] **2.º lote VNC/Manta Rota:** Casa da Igreja (Cacela Velha, 289 952 126, 4,3★/329, ostras) · Pizzadela (963 350 428, 4,7★/254) · Bela Vista (4,4★/107, porco preto) · O Ligério (281 951 372) · Casa Velha (281 952 297) · Restaurante Manta Rota · O Finalmente. *(Chá com Água Salgada já tem site — excluir.)*
- [ ] **Restaurante Avenida** (Tavira) — site completo com cores, logótipo e ementa reais.
- [ ] **Instituto dos Ferroviários** — logótipo oficial, detalhes da festa, cartaz para Instagram.
- [ ] Acrescentar telefone do Tomás às propostas PDF.
- [ ] Registar taxas de fecho por tipo de negócio (Albufeira, Gambelas, VNC).
- [ ] **Toda Chic** — pedir à dona: (1) fotos individuais sem preço nem faixa das 6 peças que só existem em fichas (calções de linho, saia, blusas sem alça, vestido preto/branco, pantalona, conjunto vermelho); (2) preço das calças clássicas em 4 cores e das sandálias com laços; (3) tamanhos das ~20 peças sem indicação; (4) identificação da empresa (nome, NIF, morada), e-mail, portes/transportadora, software de faturação. Depois: mostrar a demo, fechar orçamento por referências, montar WooCommerce + ifthenpay.

## 11. PROSPEÇÃO — MÉTODO QUE FUNCIONA

1. Pesquisa prévia da zona → lista de negócios sem site com rating ≥4,2 e dezenas/centenas de avaliações.
2. Dividir em **Lista A (visitar)** — montra aberta, porta-a-porta — e **Lista B (ligar)** — negócios de marcação.
3. Criar as demos antes de ir. Apresentar no telemóvel.
4. Horários: cafés/padarias 7h30-9h ou 15h-16h30 · restaurantes 15h-18h (fora do serviço) · cabeleireiros 2.ª/3.ª feira · clínicas a meio da tarde.
5. Evitar cadeias e franchisings (decisão não é local). Verificar sempre se já têm site antes de investir tempo.
6. Ângulo que fecha: **"tem 4,5 estrelas e centenas de avaliações — e está invisível fora do Google Maps."**
7. Quem já tem site (Tavont, Ita Trattoria): **"elevar, não substituir"** — mostrar 3 falhas concretas do site atual.

## 12. ECONOMIA DE CRÉDITOS

- Um lote por chat. Ao 5.º/6.º site, chat novo (o playbook carrega automaticamente deste repo).
- Pedir tudo de uma vez ("cria estes 4 sites") em vez de um a um.
- Pesquisa profunda (research) só uma vez por zona — guardar o relatório neste repo (`research/`) e reutilizá-lo.
- Não repetir contexto que já está neste ficheiro.
- Evitar "continua" e ajustes em cadeia: juntar os ajustes num só pedido.

## 14. SISTEMAS INTERNOS (novo — 21/09/2026)

Investigação em `research/sistemas-pacheco-studios.md` — ler antes de pagar qualquer ferramenta.

- **Regra:** só entra ferramenta que suporte "secção por cliente". HighLevel (sub-conta + snapshot) e Notion (página por cliente + convidados) passam; Make passa com prefixo `[CLIENTE]` nos cenários; **Brevo só tem sub-contas no Enterprise** (~449 $/mês) → uma conta por cliente ou e-mail no HighLevel; **Slack** só interno e só com equipa (Free não partilha canais com clientes).
- **Caminho:** Notion + Make Core já; trial de 14 dias do HighLevel com um só objetivo — o snapshot "Restaurante PT" (pipeline, reservas, formulário, review 2 h depois, template WhatsApp). Starter (97 $) quando 3 clientes pagarem mensalidade; Unlimited (297 $) a partir do 4.º.
- **O que o HighLevel não faz em PT:** fatura certificada AT (Make → Vendus/InvoiceXpress), MB WAY (Stripe diz ter MB WAY em 2026 — **a confirmar** em contas PT; se sim, rever a secção 13), WhatsApp a custo fixo (add-on por conversa, orçamentar 20–150 $/mês).

## 13. CLIENTES DE E-COMMERCE (novo — 20/09/2026)

Primeiro cliente de loja online: **Toda Chic** (`sites/toda-chic/`). Regras aprendidas:

- Investigação de base reutilizável em `research/loja-online-pt.md` — legal, pagamentos, plataformas e impacto no preço. **Ler antes de orçamentar qualquer loja.**
- **MB WAY decide a plataforma.** Sem ele perdem-se vendas em Portugal. Elimina o "estático + Stripe" e obriga a app de parceiro no Shopify. Por defeito: **WooCommerce + ifthenpay**.
- **Faturação certificada pela AT** (ATCUD + QR Code) não é opcional e a loja não a faz sozinha: tem de ligar ao software que o contabilista do cliente usa. **Perguntar na primeira reunião.**
- Uma loja **não é um site de 500 €** nem de 50 €/mês. Orçamentar à parte: carregamento do catálogo (por nº de referências), integração de pagamentos e faturação, páginas legais, formação do cliente. A mensalidade cobre alojamento, segurança, backups e suporte de encomendas.
- **Quando o cliente exige algo ilegal** (ex.: "não aceito trocas nem devoluções", que é nulo em venda à distância): avisar por escrito, propor a alternativa legal, e se insistir — construir, mas deixar **registo assinado** do aviso e da decisão. Modelo em `sites/toda-chic/REGISTO-devolucoes.md`, com anexo pronto a reencaminhar ao cliente. Protege a Pacheco Studios.
- **Loja sem WordPress (novo — 22/09):** o site de ficheiro único passa a loja com uma API pequena: **Supabase** (tabelas peças/cores/encomendas, RPCs de reserva de stock, cron de expiração, 3 Edge Functions) + **Stripe Checkout com MB WAY** + `painel.html` para o cliente (encomendas, stock, peças novas). Modelo completo em `sites/toda-chic/loja/` com **servidor de teste local** (`node loja/servidor-teste.js`) que simula a API e o MB WAY — testado ponta-a-ponta. Vantagem: o design fica intacto e o cliente gere tudo no telemóvel. Reutilizar para qualquer loja: mudar `catalogo.json`, correr `seed.py`.
- **Montagem de WooCommerce em PT (alternativa):** passo a passo completo em `research/woocommerce-pt-passo-a-passo.md` (alojamento → WooCommerce → legais → **ifthenpay/MB WAY** → faturação AT → envios → stock → catálogo → conta *Gestor da loja* para o cliente). Dois erros que custam caro: **esquecer o callback da ifthenpay** (o dinheiro entra mas a encomenda fica "a aguardar") e **dar Administrador ao cliente** em vez de Gestor da loja. Entregar sempre o manual do cliente (modelo: `sites/toda-chic/MANUAL-DONA.md`) — faz parte do produto, não é extra.
- Fluxo do impeccable para cliente novo: `impeccable context` → `reference/init.md` → **PRODUCT.md por cliente** (`sites/<cliente>/PRODUCT.md`, não na raiz) → `new-work` para o mundo visual → `detect` antes de entregar.
- **Vídeo de herói sem CDN** (aprendido a 22/09): o CDN do Higgsfield está bloqueado nesta sessão, mas `pip install imageio-ffmpeg` traz um ffmpeg com libx264. Receita: cena generativa em canvas escrita como `render(t)` determinístico (sem estado, partículas calculadas a partir de `t` e de uma seed) → corre ao vivo no site a 0 bytes → `video.js` captura os fotogramas com Playwright e codifica MP4 16:9 e 9:16 para redes sociais. Modelo em `sites/pinhal-novo-mercado/`. **Variante com fotografias** (23/09): `video-montagem.js` — lista de planos `foto:segundos:x,y,zoom→x,y,zoom` (ponto de interesse ao centro, cobre o ecrã), Ken Burns com easing, fusões de 0,7 s entre planos e do último para o primeiro (loop perfeito sem pós-processamento), graduação quente + vinheta, MP4 (libx264) e WebM (libvpx-vp9). O cliente pediu para tirar as partículas por cima de fotografia ("arco-íris com confetis") — em fotografia real, nada por cima. O site usa `<video>` com as duas fontes, poster = a própria foto, vertical em ecrãs ao alto, e sem vídeo em `prefers-reduced-motion`. Atenção: o Chromium headless não descodifica H.264 — testar com o WebM. Plumas por cima de fotografia: alpha ≈ metade da versão sobre fundo escuro, senão tapam a imagem.
- **Fotos de Instagram como matéria-prima** (aprendido a 21/09): as donas de lojas pequenas têm o catálogo inteiro em stories, com faixa da marca, preço e rótulos queimados na imagem. Não pedir "fotos limpas" à cabeça — transcrever primeiro as fichas manuscritas (preço, tamanho, cor, unidades — são a única fonte de verdade) e limpar as fotos com `sites/toda-chic/ferramentas/fotos.py` (corte da faixa por transições de texto, inpainting dos rótulos com OpenCV, recorte 4:5). Só depois pedir fotos novas do que ficou fraco. Uma peça em várias cores = um produto com fotos por cor.
- **Demo de loja = ficheiro único com router por `#/`** (início, `#/c/categoria`, `#/p/peça`, favoritos, saco, páginas). Catálogo em JSON dentro do HTML, imagens em `media/` (não em base64: 80 fotos seriam 5 MB de HTML). Favoritos e saco em `localStorage` para que o cliente sinta a loja a funcionar na apresentação. Publicar como artefacto multi-ficheiro (`files`) e como zip Netlify com a pasta `media/`.
