# PACHECO STUDIOS — PLAYBOOK MESTRE

> Fonte de verdade da Pacheco Studios. Substitui todo o histórico de chats.
> Última atualização: 06/10/2026 (lote de 10 sites em Iași — secções 5, 6 e 7)

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
- **Clientes fora de Portugal:** `lang` do país (`pt-BR`, `ro`…), fontes com o subconjunto certo (`latin-ext` para ș ț ă â î do romeno), aviso legal do país no rodapé em vez do Livro de Reclamações (Brasil: nada equivalente; Roménia: ligação ANPC SAL), banner na língua do cliente com "PACHECO STUDIOS".

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

ensō japonês · mandala · tagliatelle a cair · brasas a subir · rubrica manuscrita · ondas de açúcar + canela · folha line-art a desenhar-se · anéis de fumo + selo rotativo · bandeirolas náuticas a balançar · pincelada a pintar-se + blobs · pedra com heat-haze · pizza a girar + textura de tijolo · grelha com sardinhas + fumo · riscas de toalha + cataplana · notas musicais a flutuar · cena de praia em SVG (céu/mar/areia) · veios de marmoreio a desenharem-se + barra de pontos de cozedura + "00:00" monumental (Mr. Buffalo) · corvo a pousar no título + espinha de peixe divisora (Casa Corvo) · cardume SVG a atravessar a página (Paulo Molina) · padrão de azulejo a compor-se (Iguarias da Vila) · coral a ramificar-se em stroke-draw (O Coral) · mesa KBBQ vista de cima — grelha concêntrica + banchan a pousar (Hanam) · ecrã dividido diagonal "Forno & Mar" com mouse-follow + palavras gigantes de fundo (Catarina) · espeto 3D a girar sobre a grelha de água da ria, brasas e fagulhas em WebGL (Frango da Ria) · **"O Mostruário"** — cartões de amostra sobre blush, chips de cor reais, notas de tamanho/stock em monoespaçada como etiquetas de costureira, herói cinematográfico com a dona na loja (Toda Chic) · **"Nuvens de especiarias"** — herói-vídeo generativo em canvas determinístico (açafrão, pimentão, cardamomo, grãos de basmati), exportável em MP4 com o mesmo código (Pinhal Novo Mercado and Ria) · **carta escrita como o letreiro** — placas vermelhas em Khand que se acendem, sobre a foto real da fachada (Pinhal Novo Restaurant) · **"A conversa com a Dra."** — o site é a conversa de WhatsApp com a dentista, nas cores dela: cartão de contacto com CRO e 5,0 no Google, bolhas que respondem às perguntas dos pacientes, papel de parede com doodles de dentes, e a barra de escrever como CTA que reescreve a mensagem conforme o tema tocado (Dra. Angélica Lauermann Gomes) · **"A passagem da máquina"** — o nome da casa na didone do letreiro com a palavra de baixo em fade (máscara de riscas cada vez mais finas, cheia em cima e "skin" em baixo), uma lâmina vermelha que sobe e corta o fade ao abrir, régua dos pentes #3 → #0 em mm ao lado, e a foto da porta anotada com marcadores numerados como as placas da fachada (Society Salon, Iași) · **sombra de folhas de tília** — canvas com folhas em coração a balançar sobre a luz da manhã, porque o bistro fica em frente ao Parque Copou (teiul lui Eminescu) (Bistro Copou, Iași) · **barra que carrega anilhas** — o cliente marca produtos por objetivo, cada item põe uma anilha na barra e o pedido sai escrito no WhatsApp (Bravus Muscle Suplementos, SP) · **alcatruzes na madre** — corda com potes de barro que descem com o scroll, fachada dentro do pote (Tasquinha do Bruno) · **telhados de tesoura** com janelas que acendem quando a casa está aberta + céu de Tavira à hora real (Tasca do Tó) · **toalha de papel quadriculada** com a conta a lápis na margem (O António) · **colibri que paira** e pousa no que se toca (Restaurante Colibri) · **toalha quente** — vapor em canvas que revela o título + navalha que abre como barra de progresso (Barber's Touch) · **cartão de cliente carimbado** — 10 carimbos de tinta, um por secção (Barbearia Sr. Bonifácio) · **embrulho kraft** que abre + flores soltas que se juntam num ramo (Flor Mimosa) · **bolo em corte** — secções como camadas + construtor de bolo em SVG (Faísca & Henriques) · **painel de instrumentos** com teste de lâmpadas e luzes que levam ao orçamento (SOS CAR) · **açúcar pela peneira** sobre o stencil do nome (MB Cakes) · **Lote Iași 06/10/2026:** cúpula de cobre com boca do forno e brasa em canvas + pizza na pá (La Gioia) · caixa de bolo com tampa que levanta e fita de cetim que ata (Laurinda) · monóculo de latão que amplia + brasão que se monta (Sir John's) · cão desgrenhado tosquiado ao scroll (Sofia Pets) · relógio/roda das flores do ano (Elenor) · espelho de camarim com lâmpadas que acendem + reflexo (Beauty Zone) · borboleta com asas de unhas pintadas + frascos de verniz (Butterfly) · fita métrica como barra de progresso + giz + pesponto + fotos como moldes (Croitoria Dan) · espuma ativa limpa por rodo + gotas na laca (Auto Spa) · ficha de trabalho em matricial + ponto "la punct" (La Punct)

## 6. TRACKER DE FONTES DISPLAY (já usadas — escolher sempre uma nova)

Saira Condensed · Abril Fatface · Gilda Display · Archivo Black · Alfa Slab One · Zilla Slab · Fraunces · Playfair · Rozha One · Cinzel · Anton · Yeseva One · DM Serif Display · Bricolage Grotesque · Cormorant Garamond · Marcellus · Bitter · Bodoni Moda · Big Shoulders Display · Yatra One · Libre Caslon Display · Shippori Mincho · Eczar · Bebas Neue · Spectral · Prata · Syne · Ultra · Sora · Unbounded · Staatliches · Crete Round · Averia Serif Libre · Passion One · Gloock · Instrument Serif (→ Mr. Buffalo) · Young Serif (→ Casa Corvo; repetida no Catarina por pedido explícito do brief V2 — zonas diferentes) · Chonburi (→ Paulo Molina) · Newsreader (→ Iguarias da Vila) · Lilita One (→ O Coral) · Bungee (→ Hanam KBBQ) · Erica One (→ Frango da Ria) · Italiana (→ Toda Chic, com Jost no corpo e Courier Prime nas notas) · Martel 900 (→ Pinhal Novo Mercado and Ria, com Mukta no corpo — par devanagari-latino, a pensar na comunidade sul-asiática) · Khand 700 (→ Pinhal Novo Restaurant, com Hind no corpo — condensada de sinalética, como o letreiro) · Funnel Display 800 (→ Dra. Angélica Lauermann Gomes, com Funnel Sans no corpo e Pinyon Script só no monograma "AL") · Brygada 1918 (→ Bistro Copou, com Albert Sans no corpo) · Oranienbaum (→ Society Salon, didone estreita como o letreiro, com Hanken Grotesk no corpo, Spline Sans Mono nas medidas e Pirata One só no S vermelho) · Teko 600 (→ Bravus Muscle Suplementos, com Inter no corpo) · Caprasimo (→ Tasquinha do Bruno, com Schibsted Grotesk + Caveat) · Kufam (→ Tasca do Tó, com Public Sans + DM Mono) · Hepta Slab (→ O António, com Figtree + Reenie Beanie) · Petrona (→ Restaurante Colibri, com Karla + Caveat) · Rye (→ Barber's Touch, com Libre Franklin + Special Elite) · Holtwood One SC (→ Sr. Bonifácio, com Barlow/Barlow Condensed + Caveat) · Imbue (→ Flor Mimosa, com Figtree + Caveat) · Shrikhand (→ Faísca & Henriques, com Nunito + Pacifico) · Tilt Warp (→ SOS CAR, com Onest + Share Tech Mono) · Calistoga (→ MB Cakes, com Be Vietnam Pro + Caveat) · **Iași 06/10:** Agbalumo · Sansita Swashed · Montagu Slab · Sigmar · Bellefair · Forum · Viaoda Libre · Gelasio · Michroma · Dela Gothic One. *(Para a Roménia verificar ă ș ț com fontTools: Bagel Fat One e Amarante não os têm.)*

**Livres/planeadas:** Bevan (→ Sítio dos Presuntos).

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
- **Mogi das Cruzes – SP (Brasil):** dra-angelica-lauermann (`sites/dra-angelica-lauermann/`) — **Dra. Angélica Lauermann Gomes**, cirurgiã-dentista CRO-SP 139651, 5,0★/30 Google. Demo pt-BR "A conversa com a Dra." (WhatsApp como gramática, Funnel Display + Funnel Sans), só WhatsApp como marcação, clínica geral completa escrita por nós; nada de preços/promoções (CFO). Fotos = recortes de capturas (baixa resolução, trocar pelos originais). Primeiro site feito com o fluxo completo do impeccable (PRODUCT.md, contrato de direção, revisor final).
- **Iași (Roménia):** society-salon (`sites/society-salon/`) — **Society Salon – Barbershop**, Bd. Carol I nr. 26–28, demisol (Copou), 5,0★/69 Google, 80–120 lei, marcação no MERO (mero.ro/p/societysalon), IG @societysalon.ro. **Já tem site (societysalon.ro) → ângulo "elevar, não substituir".** Demo RO/EN "A passagem da máquina" (Oranienbaum + Hanken Grotesk), foto da porta anotada 1-2-3, rodapé ANPC (SAL) em vez do Livro de Reclamações, mapa só a pedido (sem cookies). Análise em `research/society-salon-iasi.md`. Horário, telefone, preços por serviço e fotos originais a confirmar.
- **Iași (Roménia):** bistro-copou (`sites/bistro-copou/`) — **Bistro Copou**, Strada Oastei 48 (ao lado do Parque Copou), 4,2★/677 Google, 40–60 lei, tel +40 748 631 607, bistrocopou@gmail.com, IG @bistrocopou.iasi. **Sem site próprio** (o Google aponta para iasi-delivery.ro); vende por Iasi Delivery, Wolt, Bolt Food, Glovo; reservas no Bookingham. **Demo em formato "direção"** (pedido do Tomás): 3 paletas clicáveis com pré-visualização viva (Tei și miere · Seara pe terasă · Piatră și cafea), tipografia, ideias do site e **esquema do workflow de reservas** (reserva → confirmação WhatsApp → lembrete 2 h com Vin/Anulez → visita → pedido de avaliação no dia seguinte → convite ao fim de um mês) com mensagens de exemplo em RO/EN. Site completo em rascunho (`rascunho-site.src.html`). Horário seg–sáb 09–22 (fonte: destinationiasi), domingo e preços a confirmar.
- **Lote Algarve de 05/10/2026** (10 negócios com telemóvel e sem site próprio; pesquisa em `research/algarve-10-negocios-out26.md`, briefs em `research/algarve-10-briefs.md`, fichas em `ponte/`; ramo `claude/dez-negocios-dez-websites-7gevwu`). Todos com subpáginas `#/`, fotos reais da ficha Google, CTA Ligar + WhatsApp, zips Netlify/Hostinger e `DADOS-PARA-O-DONO.md`:
  - tasquinha-do-bruno (Santa Luzia, 4,7★/651, 918 876 304, só TripAdvisor) — quadro de tapas transcrito, "a tua mesa" → WhatsApp, PT/EN.
  - tasca-do-to (Tavira, 4,5★/173, 964 610 125) — "ainda está aberto?" ao vivo, PT/EN; pratos a confirmar.
  - o-antonio (Moncarapacho, 4,6★/802, 939 163 759, só eatbu → elevar) — carta de 2023 transcrita (preços a confirmar), PT/EN.
  - restaurante-colibri (Moncarapacho, 4,5★, 968 176 680) — carta numerada com "+" para juntar à reserva.
  - barbers-touch (Loulé, 4,9★/337, 914 439 240, só IG) — marcação serviço → dia → hora → WhatsApp, PT/EN; preços a confirmar.
  - barbearia-sr-bonifacio (Olhão, 5,0★/97, 926 240 012 — confirmar vs 914 569 672) — preçário real, ordem de chegada → "Vou a caminho".
  - flor-mimosa (Faro, 4,9★/65, 912 155 977) — catálogo por ocasião + encomenda guiada, PT/EN.
  - faisca-henriques (Faro, 4,7★, 932 532 805, desde 1978) — construtor de bolo → WhatsApp.
  - sos-car (Olhão, 4,9★/13, 935 521 706) — "Que luz acendeu?" → orçamento com matrícula.
  - mb-cakes (Loulé + Almancil, 4,9★, 932 626 851, só linktree) — ementa PT/EN completa, encomenda de bolo.
- **Lote Iași de 06/10/2026** (10 negócios com telemóvel e sem site próprio; pesquisa em `research/iasi-10-negocios-out26.md`, briefs em `research/iasi-10-briefs.md`; ramo `claude/dez-negocios-dez-websites-7gevwu`). Cada um com `index.html` em RO (botão EN) e `pt.html` para o Tomás, faixa PREZENTARE, ANPC SAL + ODR, fotos e vídeos reais das fichas Google (truque `=dv`), CTA Sună + WhatsApp, zips e `DADOS-PARA-O-DONO.md`:
  - la-gioia-di-giovanni (pizzaria, 5,0★/164, 0745 451 313) — carta + comandă ridicare/livrare → WhatsApp.
  - cofetaria-laurinda (cofetărie, 4,9★/90, 0770 988 652; 2.º número 0745 092 341 a confirmar) — configurador de bolo e candy bar, 2 vídeos.
  - sir-johns-barbershop (4,8★/191, 0731 422 775) — programare serviço → dia → hora, 3 vídeos.
  - sofia-pets (coafor canin, 4,9★/129, 0742 500 111) — marcação por porte e pelo.
  - floraria-elenor (5,0★/48, 0750 105 697) — buchet la comandă por ocasião, 2 vídeos.
  - beauty-zone (5,0★, 0729 376 681) — marcação por tratamento.
  - salon-butterfly (unhas, 4,9★/24, 0748 578 709) — configurador de unhas; sem fotos reais (pedir).
  - croitoria-dan (4,6★/48, 0740 609 378) — fișa de retuș → WhatsApp.
  - auto-spa-detailing (5,0★/70, 0771 432 059) — pacotes por tipo de carro.
  - service-auto-la-punct (4,9★, 0755 537 383) — pedido de orçamento com marca/modelo/problema.
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

- [ ] **Sítio dos Presuntos** (Gambelas/Montenegro) — site por criar. Tasca beirã, donos de Viseu, R. Aquilino Ribeiro (nº 122 vs 212 a confirmar), tel 917 823 784 (TA) / 919 869 212 (booktables), Google 4,3/~1.220, até às 23:00. Pratos: presunto, leitão, tamboril, lula grelhada, sopa de feijão verde. Identidade planeada: Bevan, presuntos pendurados a balançar.
- [ ] **O Caseiro2** (ex-"O Bandeira", Montenegro) — 4,6★/438, menu de almoço ~12 €, fecha 2.ª feira. Site se houver interesse.
- [ ] **2.º lote VNC/Manta Rota:** Casa da Igreja (Cacela Velha, 289 952 126, 4,3★/329, ostras) · Pizzadela (963 350 428, 4,7★/254) · Bela Vista (4,4★/107, porco preto) · O Ligério (281 951 372) · Casa Velha (281 952 297) · Restaurante Manta Rota · O Finalmente. *(Chá com Água Salgada já tem site — excluir.)*
- [ ] **Restaurante Avenida** (Tavira) — site completo com cores, logótipo e ementa reais.
- [ ] **Instituto dos Ferroviários** — logótipo oficial, detalhes da festa, cartaz para Instagram.
- [ ] **Dra. Angélica Lauermann Gomes (dentista, Mogi das Cruzes – SP, Brasil)** — análise em `research/dra-angelica-lauermann.md`: faturação provável R$ 20–25 mil/mês; 3 focos = marcação + anti-falta por WhatsApp, Google (site pt-BR + avaliações), orçamentos + retorno. Primeiro cliente fora de Portugal: site pt-BR, LGPD, regras de publicidade do CFO. Esquema dos 3 workflows (Cal.com + Make/n8n + Notion + Brevo, sem HighLevel) em `research/dra-angelica-workflows.html`. **24/09:** demo do site feita (`sites/dra-angelica-lauermann/`); o Tomás decidiu que a agenda não será o Cal.com (volume de uma clínica); o esquema dos workflows passou a "agenda da clínica, a escolher" (requisitos: webhook ou API e link de reagendamento). **Depois:** o Tomás decidiu não usar a Clinicorp (custos em `research/agenda-clinica-odontologica-br.md`) e construir um sistema à medida: Supabase + painel PWA + WhatsApp Cloud API + n8n + IA (Claude) + Brevo, sem o prontuário (legal). Arquitetura e fases em `research/dra-angelica-sistema.md`. Checklist de execução (60 passos) em `research/dra-angelica-checklist.md`. Planos de anúncios R$ 500/1.000/1.500 com lucro estimado e preços médios dos tratamentos em `research/dra-angelica-planos.html` (artifact PPcYDCpasuT83ksvfcvKuG); preços Pacheco Studios: Essencial R$ 4.000 + R$ 500/mês, Crescimento R$ 6.000 + R$ 750/mês, Completo R$ 10.000 + R$ 1.100/mês (mensalidades "a partir de"). O Completo é o plano-âncora: existe para o Crescimento parecer a escolha sensata (marcado "Recomendado" na página). Conteúdo: Essencial = site, lembretes, Google Business Profile otimizado com resposta a todas as avaliações e pedido de avaliação pós-consulta; Crescimento = + recepcionista IA (a justificação do plano); Completo = + follow-up a quem conversou e sumiu e a orçamentos sem resposta, Google Ads, retornos/reativação, relatório. O Completo tem anúncios em bola de neve (30% do lucro reinvestido, 5 campanhas no 3.º mês); projeção de 12 meses em `research/dra-angelica-projecao-completo.pdf` (implementação paga no 3.º mês, estabiliza em ≈ R$ 3.900 de verba quando a agenda enche). Resultados por plano: página interativa `research/dra-angelica-resultados.html` (botões plano + cenário, projeção 12 meses com aprendizado dos anúncios; Essencial paga no 5.º mês, Crescimento no 4.º, Completo no 3.º) e PDF com os 3 planos. Para mostrar à Doutora: planos.pdf, resultados.pdf, projecao-completo.pdf e a demo do site.
- [ ] **Society Salon (barbearia, Iași, Roménia)** — demo feita (`sites/society-salon/`, zips Netlify/Hostinger na pasta). Antes de mostrar: abrir societysalon.ro no telemóvel e anotar 3 falhas concretas (o site deles está bloqueado nesta sessão). Pedir ao salão: horário, telefone, preços/serviços do MERO, conteúdo do Gentleman's Package, fotos originais (`media/LEIA-ME.txt`), logótipo vetorial, equipa com níveis, dados da empresa (CUI) para o rodapé. Focos de sistema: pedido de avaliação Google depois de cada marcação MERO, lembrete de novo corte aos 21–28 dias, proposta "Society Membership" (assinatura mensal).
- [ ] **Bistro Copou (Iași)** — mostrar a página de direção, escolher paleta, pedir fotos do terraço, menu com preços e horário de domingo; depois fechar o site (rascunho pronto) e o workflow de reservas (WhatsApp Business + Make/n8n + calendário).
- [ ] **Meta Ads · 125 € · 14 dias (outubro 2026)** — plano e três guiões (site, automação, marketing) em `research/meta-ads-3-videos.pdf` (HTML ao lado). Estrutura: 1 campanha de Tráfego (visualizações da página de destino), 1 conjunto, 3 anúncios, distrito de Faro "vive em", 30–65+, só interesses de dono; semana 2 retargeting para WhatsApp a quem viu ≥ 25%. Sem "2x" nem "garantia" nos anúncios. **Convenção de UTM fixa:** `utm_source=meta · utm_medium=paid-video · utm_campaign=ps-prospecao-<mês> · utm_content=<serviço>`. Frase reflexiva do vídeo de marketing: "Um produto imperdível transforma qualquer morada num destino." Antes de gravar: linha de demonstração WhatsApp a funcionar (vídeo 2), ficha Google gerida (vídeo 3), autorizações do Carlos e da Toda Chic; no pachecost.com, os separadores abrirem por `#` e o JS que troca a frase do WhatsApp quando há UTM. D1 = terça 06/10 (05/10 é feriado).
- [ ] **Meta Ads Roménia · 3 vídeos em RO** — (1) recriação Bolta Rece (só com autorização, ou «Concept neoficial»), (2) trabalho da Pacheco «Afacerea ta merită un site de acest nivel», (3) automação WhatsApp **feito**: 26,4 s, 100 % IA, na biblioteca Higgsfield (`pacheco-automatizare-whatsapp-ro.mp4` + capa). Preço no vídeo: «de la 6.000 lei + 1.000 lei/lună». Vídeo 3 vai numa campanha de Mensagens (WhatsApp). Guião, texto do anúncio e plano RO em `research/video-automatizare-ro.md`; scripts de overlays/montagem em `research/video-automatizare-ro/`. Falta: rever o vídeo, música no Instagram, linha WhatsApp a responder em RO.
- [ ] **Campanha 1 RO · web design · 75 € · 10 dias** — 2 conjuntos (A Bolta Rece «concept neoficial» / B portfólio) × 3,75 €/dia, Tráfego → visualizações da página de destino, Roménia, 28–60, interesses de dono, posicionamentos manuais sem Audience Network. Passo a passo em `research/meta-ads-ro-campanha-1.md`. Os outros 75 € ficam para a campanha de Mensagens (vídeo 3).
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
8. **WhatsApp verificado (regra de 07/10/2026).** Ter telemóvel não garante WhatsApp; no lote de Iași alguns números não o tinham. Na pesquisa, a tabela leva uma coluna «WhatsApp», com um de três valores:
   - **sim**: há prova pública, como um botão ou link wa.me na ficha Google, no Facebook ou no Instagram, um autocolante na montra numa foto, ou uma avaliação que fale do WhatsApp;
   - **?**: não há prova;
   - **não**: há prova de que não usam.
   Com «sim», a mensagem vai por WhatsApp. Com «?» ou «não», o negócio vai para a Lista A (visita) ou para uma chamada, e o ficheiro de contactos dá a morada com link do Maps em vez do botão de WhatsApp. No site, o CTA principal desses negócios é «Ligar». Daqui não se consegue testar se um número tem WhatsApp, por isso vale a prova pública ou a resposta do Tomás.

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
- **Vídeo de herói sem CDN** (aprendido a 22/09): o CDN do Higgsfield está bloqueado nesta sessão, mas `pip install imageio-ffmpeg` traz um ffmpeg com libx264. Receita: cena generativa em canvas escrita como `render(t)` determinístico (sem estado, partículas calculadas a partir de `t` e de uma seed) → corre ao vivo no site a 0 bytes → `video.js` captura os fotogramas com Playwright e codifica MP4 16:9 e 9:16 para redes sociais. Modelo em `sites/pinhal-novo-mercado/`. **Variante com fotografias** (23/09): `video-montagem.js` — lista de planos `foto:segundos:x,y,zoom→x,y,zoom` (ponto de interesse ao centro, cobre o ecrã), Ken Burns com easing, fusões de 0,7 s entre planos e do último para o primeiro (loop perfeito sem pós-processamento), graduação quente + vinheta, MP4 (libx264) e WebM (libvpx-vp9). O cliente pediu para tirar as partículas por cima de fotografia ("arco-íris com confetis") — em fotografia real, nada por cima. **Higgsfield nesta sessão:** o upload (S3 presigned) e o `upscale_image` (2 créditos/foto, 2K, bytedance) funcionam; o CDN de resultados (`*.cloudfront.net`) está bloqueado pelo proxy — os ficheiros ficam na conta Higgsfield e o Tomás descarrega-os à mão. O site usa `<video>` com as duas fontes, poster = a própria foto, vertical em ecrãs ao alto, e sem vídeo em `prefers-reduced-motion`. Atenção: o Chromium headless não descodifica H.264 — testar com o WebM. Plumas por cima de fotografia: alpha ≈ metade da versão sobre fundo escuro, senão tapam a imagem.
- **Fotos de Instagram como matéria-prima** (aprendido a 21/09): as donas de lojas pequenas têm o catálogo inteiro em stories, com faixa da marca, preço e rótulos queimados na imagem. Não pedir "fotos limpas" à cabeça — transcrever primeiro as fichas manuscritas (preço, tamanho, cor, unidades — são a única fonte de verdade) e limpar as fotos com `sites/toda-chic/ferramentas/fotos.py` (corte da faixa por transições de texto, inpainting dos rótulos com OpenCV, recorte 4:5). Só depois pedir fotos novas do que ficou fraco. Uma peça em várias cores = um produto com fotos por cor.
- **Demo de loja = ficheiro único com router por `#/`** (início, `#/c/categoria`, `#/p/peça`, favoritos, saco, páginas). Catálogo em JSON dentro do HTML, imagens em `media/` (não em base64: 80 fotos seriam 5 MB de HTML). Favoritos e saco em `localStorage` para que o cliente sinta a loja a funcionar na apresentação. Publicar como artefacto multi-ficheiro (`files`) e como zip Netlify com a pasta `media/`.

## 15. MARCA PACHECO STUDIOS (novo — 25/09/2026)

Identidade já usada no Instagram (@pachecostudiospt), agora também no cartão e em ro.pachecost.com. O site principal é **pachecost.com**. **Tudo o que é nosso usa isto; os clientes nunca.** Mercado do cartão: **Roménia** (desde 25/09/2026).

- **Cores:** carvão `#141210` · osso `#EFEAE3` · laranja `#E8622C`. Derivadas com contraste medido: `#A5A19B` (texto secundário sobre carvão, 7,3:1) · `#4D4A47` (secundário sobre osso, 7,4:1) · `#A64923` (laranja para texto sobre osso, 4,9:1) · `#D35A29` (traços sobre osso, 3,3:1). O laranja puro sobre osso dá só 2,8:1: nunca em texto sobre fundo claro.
- **Fontes:** Archivo Black (títulos em maiúsculas) · Space Mono (etiquetas, contactos, preços) · Inter (texto corrido). Os ficheiros estão em `marca/fontes/`. O Inter vem como fonte variável (um só ficheiro).
- **Voz:** o Instagram usa "tu" ("O teu negócio?"). O site (pachecost.com, PT) também usa "tu", como o site anterior; o inglês usa "you". O cartão romeno usa "tu" ("afacerea ta", "Vezi proiectele"), que é o registo normal da publicidade na Roménia. Slogan em romeno: "Unde afacerea ta **prinde viață** online." Propósito: *Web design · implementare sisteme AI* ("AI", não "IA": é o que os donos de negócio reconhecem).
- **Romeno nas fontes:** os ficheiros base (latin) não têm Ă, Ș nem Ț. Usar sempre também os `*-latin-ext.woff2` de `marca/fontes/` (`@font-face` com `unicode-range`). O gerador do cartão verifica se cada letra existe na fonte.
- **Slogan:** "Onde o trabalho **ganha vida** online." O ponto final é o ponto laranja da marca.
- **Dados de contacto num só sítio:** `marca/dados.json` alimenta o cartão e a página. Muda-se lá e corre-se `gerar.py` nos dois.
- **Regra do QR:** o QR impresso aponta **sempre para o nosso domínio** (`ro.pachecost.com/C` — subdomínio do site real; o pachecost.com usa o DNS do Netlify, por isso basta juntar o domínio ao projeto), nunca direto para o Instagram ou para outro serviço. Assim o destino muda em `destino_qr` sem reimprimir nada. Instagram vs site: o site ganha para quem lê o QR à porta (abre sem app nem login, mostra sites reais e tem o WhatsApp à mão). O Instagram fica ligado a partir da página.
- **Endereços curtos** (`enderecos_curtos`): `ro.pachecost.com/tasca-ria` → demo publicada. O cartão já não tem o espaço para escrever à mão (é igual para todos), mas continuam úteis para mandar a demo por WhatsApp.
- **Frase do verso:** a razão para apontar a câmara. As 5 opções estão em `dados.json` (`frases` + `frases_pt`) e desenhadas em `marca/cartao/frases-opcoes.png`. Recomendada: "Nu promitem. **Arătăm.**" (Não prometemos. Mostramos.)
- **Impressão:** 85 × 55 mm, papel mate 350–400 g (sem brilho: o QR não reflete).
- **QR sozinho** (`marca/qr/`): mínimo 15 mm (o cartão usa 21), margem branca de 4 módulos, escuro sobre claro, nunca logótipo no meio nem cor laranja, preto só (100 % K) na gráfica. Antes de qualquer impressão: `qr-teste-a4.pdf` a 100 % (régua de 100 mm) e ler com 2 telemóveis.
- **Netlify por arrastar o zip:** redirecionamentos em `_redirects` e cabeçalhos em `_headers` (funcionam sempre, também sem build); o `netlify.toml` fica só com `publish`. **Um projeto, dois domínios:** `ro.pachecost.com` é um alias do projeto do pachecost.com e a regra `https://ro.pachecost.com/  /ro/index.html  200!` serve-lhe a página romena; o resto dos ficheiros é partilhado. As linhas do QR (`/c`, `/C`) ficam sempre em primeiro. O gerador verifica o `_redirects` e `verificar.cjs` aplica-o num emulador dos dois domínios (o Chromium não segue um 302 vindo da interceção do Playwright: segue-se com uma página que troca o endereço, e os códigos verificam-se à parte).
- **Página do QR (ro.pachecost.com):** **só clientes reais** (decisão do Tomás, 26/09): nunca apresentações a negócios que não compraram (`demo: true` em `portfolio.json`). **Desde 29/09 a vista chama-se «Sites» e não mostra quantos trabalhos temos nem «O teu negócio?»** (decisão do Tomás: passar responsabilidade, profissionalismo e conhecimento de mercado, não procura de montra). Três `destaque: true` em «Em destaque»; os outros sites ficam dentro de 4 cartões por tipo de negócio (`setor` em `portfolio.json`), com o que o cliente pergunta e o que o site responde, ligados por pontos como numa ementa, e as automações que combinam. Por baixo, «O que fica ao nosso cuidado»: 6 compromissos verdadeiros. No fim da vista, «Mais sites que fizemos»: os restantes ativos numa grelha, só para mostrar variações, sem «O teu negócio?». Os sites de clientes sem site publicado são copiados para `/p/<slug>/` no zip (com `noindex` e o botão «Înapoi» injetados pelo gerador) — não dependem de outros Netlify. Os quadrados são só CSS: nome no tipo de letra do site (Google Fonts) sobre as cores dele; nada de capturas. As 8 automatizações estão em `conteudo/{pt,en,ro}.json` com a dor, o fluxo, o que ganha, o que precisa e com quais combina; as ligações entre elas abrem o cartão apontado sem sair da vista. O fluxo não fica no meio do texto: abre à parte, no botão «Ver o esquema» (secção 16). Os separadores funcionam sem JavaScript (`:target` + `:has()`). Fontes da marca embutidas em subconjunto latin + romeno (`marca/fontes/*-ro.woff2`, feitas com fontTools a partir do TTF do Google Fonts — pedir o CSS com um User-Agent de Android 2.2 para vir TTF). O gerador recusa-se a fazer o PDF final enquanto faltar o telefone ou o domínio, e faz só a versão com faixa "PROVA".
- **Intro de pachecost.com (29/09/2026):** na 1.ª visita de cada sessão, 4 s: compacto → portal «Web design + marketing» → muscle car → portal «Implementação de IA» → superdesportivo → arranca → marca + slogan → o ecrã sobe e mostra o site. Salta com um toque, «Saltar» ou Esc; não aparece ao recarregar, com movimento reduzido nem sem JavaScript; se as fotografias demorarem mais de 1,5 s abre o site sem ela. Fotografias geradas (Higgsfield `gpt_image_2_5`, fundo transparente, 3 créditos pelas 6 candidatas) **sem marcas registadas** (o site não pode mostrar marcas de outros como se fossem nossas): `sites/pacheco-studios/media/intro-{1,2,3}.webp`, aparadas à caixa do alfa, 1200 px, WebP q82. Prompts para as regenerar noutro sistema: `sites/pacheco-studios/intro-prompts.md`. Os carros ficam **só na intro, nunca no corpo do site** (decisão do Tomás, 29/09).
- **Trazer ficheiros para uma sessão cuja rede não chega a eles** (`.github/workflows/buscar-imagens.yml`): escrever «etiqueta url» por linha em `.github/buscar-imagens.txt` («testar url» só testa o link) e fazer push; o runner do GitHub descarrega, apara à caixa do alfa, grava WebP, uma folha de contacto e `links.txt` em `sites/pacheco-studios/media/intro-candidatos/` e faz commit no mesmo ramo (`git pull` a seguir; apagar a pasta depois de escolher). O `workflow_dispatch` não serve enquanto o ficheiro não estiver no ramo por omissão. Foi assim que as imagens do Higgsfield chegaram a 29/09 (o cloudfront deles está bloqueado nas sessões). O runner também abriu os links dos clientes a 29/09: os 8 sites ativos e o pachecost.com respondem 200; olakathmandu.com dá 503 (continua fora).
- **Capturas de sites para mostrar trabalhos:** Playwright com `reducedMotion: 'reduce'` (estado final sem animações), esconder `.pv-banner` e pedir as fontes do Google pelo lado Node (`route.fetch()`). O Chromium desta sessão não confia no proxy e sem isto as capturas saem com fontes de sistema.

## 16. DIREÇÃO DE MERCADO: MOSTRAR A MÁQUINA (novo — 26/09/2026)

Decisão do Tomás, a aplicar em tudo o que a Pacheco Studios faz daqui para a frente. Para apresentar: `research/direcao-confianca.pdf`. O raciocínio inteiro (fundamentos, riscos, Roménia, demo, métricas, plano a 90 dias, decisões pendentes): `research/mostrar-a-maquina-analise.md` (também em PDF). **Reler antes de mexer em posicionamento, propostas ou na página das automatizações.**

- **A regra-mãe: construir a prova antes de pedir o sim.** Os sites já se vendem assim (demo antes da abordagem). Para cada produto, escolher a prova mais barata que ainda convence e fazê-la antes de vender: site → a demo; automatização → o fluxo desenhado + regras + demo genérica que responde + diário; loja → a demo Toda Chic; sistema à medida → o desenho + painel de exemplo.
- **Funil:** os sites são a porta, as automatizações o segundo passo (vendem-se a quem já comprou o site, com o desenho na mão). A frio, só com a demo que responde.
- **A IA é ingrediente, não título.** «Estúdio de inteligência artificial» pede fé; «sistemas que atendem, marcam e lembram, desenhados à tua frente» descreve. Verbos do balcão (atende, marca, lembra, cobra), nunca de agência.
- **Oferta por ordem:** o Plano (20 min à mesa, PDF no mesmo dia) → o Piloto (1 automatização, 30 dias, 3 números combinados, saída com uma mensagem) → o Sistema → a Manutenção. Preço pelo desenho (caixas, contas ligadas, texto a aprovar), nunca pela palavra «IA». **Se uma proposta não tem desenho, não sai.**
- **O assistente identifica-se sempre** (não só se perguntarem): o Regulamento da IA da UE obriga a partir de agosto de 2026 e a Roménia é UE. Mensagens de retorno e postări são marketing → consentimento + «STOP»; lembretes e confirmações são transacionais.
- **Demo «Restaurantul Demo»** (WhatsApp Cloud API + n8n + Claude + Supabase): guião de 4 mensagens — olá (identifica-se) · mesa para 4 (marca) · pergunta fora da lista (passa a pessoa, o telemóvel do Tomás toca) · STOP (obedece). A passagem a pessoa é a prova, não a falha.
- **Medir por mês:** conversas · desenhos à mesa (e quantos donos corrigiram o desenho) · demos experimentadas · pilotos · pilotos que viraram manutenção.
- **Conteúdo:** um desenho por semana no Instagram («é isto que acontece quando…»), bastidores reais com autorização.

- **O obstáculo não é a dor, é a confiança.** O dono já sente a dor. O que o trava é não saber o que a IA é, não ter provas e ter de dar um «ato de fé». Vender só pela dor pede fé; vender pela transparência pede lógica.
- **Vendemos o plano, não a promessa.** Cada automatização mostra-se com o **fluxo desenhado** (como a proposta Be Legend: cada caixa um passo, gatilho, decisões, e os momentos em que entra uma pessoa), as **regras em linguagem simples** («se não responde em 24 h → toque 2»), **quem decide o quê** (o dono aprova os textos, a IA só escolhe entre respostas aprovadas, o que não sabe vai para uma pessoa) e **o que se vai medir** na primeira semana.
- **Prova sem clientes a correr:** (1) demo viva no WhatsApp — o dono escreve para um número e a recepcionista de um restaurante fictício responde; (2) propostas-desenho publicadas como exemplos; (3) diário de construção (capturas dos bastidores: n8n, tabela, mensagem real); (4) piloto de 30 dias com métricas combinadas. **Nunca** números de resultados inventados, testemunhos falsos ou «casos» que não existem.
- **A explicação da IA a um dono de negócio** (usar sempre a mesma): lê e escreve texto como uma pessoa muito rápida; não decide sozinha — as regras são nossas e do dono; corre nas contas dele (WhatsApp, agenda, Google); cada mensagem fica registada e pode ser lida; entra uma pessoa em tudo o que sai da rotina.
- **Formato-padrão das propostas:** capa · a dor nas palavras do dono · o fluxo desenhado · as regras · o que medimos · o que precisa do dono · preço. É o formato de `research/img/proposta-be-legend.jpg`.
- **Onde se aplica:** pachecost.com em PT · EN · RO (`sites/pacheco-studios/`) — **aplicado a 26/09, esquemas redesenhados a 27/09:** cada automatização abre com o botão «Ver o esquema» (EN «See the diagram», RO «Vezi schema»), que mostra num cartão no meio do ecrã o fluxo **desenhado como a proposta Be Legend**: tela pontilhada, uma caixa branca por passo com ícone e portas, gatilho a âmbar, pessoa a verde, decisão tracejada com os ramos em pílulas azul-escuras, esperas a bege e legenda. No telemóvel os ramos descem em árvore; no computador ficam lado a lado, como as situações da proposta. Depois vêm «As regras dela», «Quem decide o quê» (tu · o sistema · nós), «O que o cliente vê» e o pedido de demonstração no WhatsApp; o botão para experimentar entra quando a demo viva existir. **Link direto para mandar a um dono:** `pachecost.com/#esquema-<id>` (ou `ro.pachecost.com/#esquema-<id>`), ids em `sites/pacheco-studios/LEIA-ME.md`; pachecost.com (secção «como é feito», ver `research/pachecost-fraquezas.pdf`), cartão (a frase «Nu promitem. Arătăm.» já está nesta linha), conversas de venda (ouvir a dor → desenhar o fluxo à frente do dono → demo no telemóvel dele → piloto).

## 17. POSICIONAMENTO: CONSULTORIA DE IA (novo — 02/10/2026)

Decisão do Tomás: a Pacheco Studios deixa de se apresentar como agência que vende produtos (sites, automações) e passa a ser uma **consultoria de IA para negócios locais**. Começa pelo objetivo do dono, faz o diagnóstico, desenha, implementa e acompanha. Pesquisa: `research/consultoria-ia-referencias.md` (Viver de IA + 8 consultoras).

- **Frase da marca:** «Tens um objetivo a atingir? / A IA VAI FAZÊ-LO ACONTECER. / Só tens de dar o primeiro passo.» Mantém-se a ideologia da secção 16: explicar o que a IA é e não é, para passar confiança («Não prometemos. Mostramos.»).
- **Processo (5 passos):** conversa de diagnóstico, 20 min → diagnóstico escrito no mesmo dia → solução desenhada à frente do dono → piloto de 30 dias com o ponto de partida medido no dia 0 → acompanhamento mensal. Hoje a conversa e o diagnóstico escrito não têm custo.
- **Casos (decisão de 03/10):**
  - O site mostra resultados reais de outros negócios como **«onde podes chegar»**. O nosso trabalho é levar esses resultados para o negócio do cliente.
  - **Nenhuma ligação nem menção à Viver de IA no site** (nem nome, nem link). As fontes ficam só internas, em `conteudo/casos.json` e `research/consultoria-ia-referencias.md`, para confirmar cada número.
  - Limite que não se passa: nunca dizer que são clientes nossos ou trabalho nosso. O texto diz «já aconteceram noutros negócios / em negócios como o teu».
  - Projeções aparecem como projeções.
  - O 1.º caso nosso (piloto com dia 0 e dia 30) entra em primeiro lugar.
- **Diagnóstico em conversa (03/10):** «Conhece-nos» abre 8 perguntas no estilo chat (nome, negócio, tipo, cidade, objetivo, onde se perde, canais, contacto). No fim, a mensagem vai para o WhatsApp do Tomás; nada é guardado no site.
- **Herói (03/10):** frase da marca a dois tons sobre a imagem gerada no Higgsfield (`media/heroi.webp`), com o logótipo «P» no cabeçalho. Por baixo: «O que faz uma consultoria de IA» (caixa com 3 passos), o veredito de um caso sobre fundo 3D, o que é a IA, os números dos casos e 4 compromissos. Sem «Quem está por trás».
- **03/10 (tarde):**
  - Nos Casos só ficam o depoimento e os resultados: sem nome, sem tipo de negócio e sem a caixa «o próximo caso».
  - Saiu todo o texto «fazemos o site antes de pagares / só pagas se gostares», incluindo a página Sites.
  - As Soluções abrem só com «Estes são alguns dos sistemas mais eficazes e mais comuns para resolver a tua dor de hoje.»
- **Cookies (04/10):** saiu a faixa; nada aparece ao abrir. O rodapé diz que usar o site é aceitar a política de privacidade e a de cookies. Pixel da Meta automático em pachecost.com, desligável na página Cookies (e com Global Privacy Control). **Risco assumido pelo Tomás, avisado:** sem faixa, isto não é consentimento válido na UE (TJUE Planet49, CNPD) e a Meta exige-o aos anunciantes.
- **Herói em scroll to animation (03/10, noite):** vídeo Kling 3.0 gerado a partir da imagem do herói (push-in, os fios acendem). 18 fotogramas WebP 720 px (≈134 KB no total) em `media/heroi-seq/`, embutidos na página; o scroll avança o vídeo com fusão entre fotogramas e o texto desaparece no fim. Fica a imagem parada sem JavaScript, com movimento reduzido ou se o texto não couber no ecrã. O Seedance quase não mexia: rejeitado.
  - **04/10 — nitidez:** os primeiros fotogramas eram 720 px a q30 (esticados ~2× no ecrã) e a fusão entre fotogramas desdobrava as arestas. Agora: vídeo ampliado a 4K no Higgsfield (`upscale_video`, Topaz 2160p), 61 fotogramas em ficheiros à parte (`media/heroi-hd/d` 16:9 1920 px; `v` recorte 9:16 720×1280 para telemóvel), um fotograma de cada vez, sem fusão.
- **Diagnóstico com cara própria (não copiar o do Viver de IA):** uma pergunta por ecrã, opções A–H e a «ficha do teu negócio» a preencher-se ao lado.
  - **04/10:** «Outro» no tipo de negócio abre um campo para escrever; a pergunta do objetivo passou a **faturação mensal** em escalões curtos (PT/EN em €: até 2 500, 2 500–5 000, 5–10 mil, 10–20 mil, 20–35 mil, 35–50 mil, +50 mil, prefiro não dizer; RO em lei, ×5); cidade em RO com «Ex.: Iași». Saiu todo o «diagnóstico escrito no mesmo dia». **Logótipo só onde vai a marca, nunca em pontos/marcadores** (correção do Tomás, 04/10): o logótipo inteiro (`logo.svg`, com «PACHECO STUDIOS» em arco e «DIGITAL», função `logo_completo()` no gerador) substitui o nome «Pacheco Studios» no cabeçalho, na intro (topo e ecrã final), nas páginas legais e na placa central do fundo 3D; o nome fica só para leitores de ecrã. Os pontos laranja (regras, «Adere hoje…», ficha, veredito) continuam pontos. Saiu do rodapé a frase «Esta página é um exemplo do que fazemos».
- **PONTE em vez da sandbox (decisão do Tomás, 04/10):** tudo o que a rede da sessão não alcança (CDN do Higgsfield, sites bloqueados pelo proxy, vídeo com ffmpeg) faz-se no workflow `.github/workflows/ponte.yml`. Escrever pedidos em `.github/ponte.txt` e fazer push; o runner do GitHub responde com um commit no mesmo ramo (1–4 min) e `ponte/relatorio.txt`. Operações: `imagem` / `recorte` (WebP), `ficheiro` (tal como vem), `fotogramas` (16:9 1920 px + recorte 9:16 720×1280), `pagina` (texto, HTML e captura da página com JavaScript) e `testar`. A sandbox do Higgsfield (`sandbox_exec`) já não se usa: pedia autorização de 2 em 2 minutos e obrigava a passar ficheiros em base64 aos bocados. As ferramentas de geração do Higgsfield (imagem, vídeo, upscale) continuam a usar-se normalmente; só o transporte e o processamento passam pela ponte.
- **Site pachecost.com (PT · EN · RO)** em `sites/pacheco-studios/`, trazido do branch `cool-sagan` a 02/10. Separadores:
  - **Consultoria** (entrada);
  - **Casos**;
  - **Soluções** (as 8 automações com esquema, mais «E também»);
  - **Sites**.

  Quem vem de anúncios de sites (`utm_content=web-…`) entra direto nos Sites. Gerar e testar com `python3 gerar.py`; o zip `pacheco-studios-netlify.zip` é para arrastar para o projeto Netlify do pachecost.com.
- **A decidir:**
  - diagnóstico pago e creditado na implementação, depois do 1.º caso;
  - preços «desde»;
  - páginas por setor;
  - calculadora de horas;
  - foto do Tomás;
  - texto do cartão («Vezi proiectele» → algo sobre o diagnóstico) na próxima impressão.
