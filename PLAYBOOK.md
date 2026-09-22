# PACHECO STUDIOS — PLAYBOOK MESTRE

> Fonte de verdade da Pacheco Studios. Substitui todo o histórico de chats.
> Última atualização: 22/09/2026 (proposta Be Legend Olhão + pipeline HTML→PDF)

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

Contacto nas propostas: tspacheco26@gmail.com · **967 117 357** (já nos PDFs do Be Legend; acrescentar aos restantes)

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

ensō japonês · mandala · tagliatelle a cair · brasas a subir · rubrica manuscrita · ondas de açúcar + canela · folha line-art a desenhar-se · anéis de fumo + selo rotativo · bandeirolas náuticas a balançar · pincelada a pintar-se + blobs · pedra com heat-haze · pizza a girar + textura de tijolo · grelha com sardinhas + fumo · riscas de toalha + cataplana · notas musicais a flutuar · cena de praia em SVG (céu/mar/areia) · veios de marmoreio a desenharem-se + barra de pontos de cozedura + "00:00" monumental (Mr. Buffalo) · corvo a pousar no título + espinha de peixe divisora (Casa Corvo) · cardume SVG a atravessar a página (Paulo Molina) · padrão de azulejo a compor-se (Iguarias da Vila) · coral a ramificar-se em stroke-draw (O Coral) · mesa KBBQ vista de cima — grelha concêntrica + banchan a pousar (Hanam) · ecrã dividido diagonal "Forno & Mar" com mouse-follow + palavras gigantes de fundo (Catarina) · espeto 3D a girar sobre a grelha de água da ria, brasas e fagulhas em WebGL (Frango da Ria) · **"O Mostruário"** — cartões de amostra sobre blush, chips de cor reais, notas de tamanho/stock em monoespaçada como etiquetas de costureira, herói cinematográfico com a dona na loja (Toda Chic) · **fachada com duas portas que se abrem ao carregar** (folhas em rotateY) + secção "do prato à prateleira" que liga os dois negócios (Pinhal Novo Mercado and Ria + Restaurant) · **"a etiqueta da casinha"** — etiqueta kraft pendurada num fio que balança no herói; o tutor escreve o nome do pet e escolhe o serviço, e a etiqueta e a mensagem do WhatsApp preenchem-se ao vivo; bolhas de sabão a subir no fundo (Doris & Cia Pet Shop)

## 6. TRACKER DE FONTES DISPLAY (já usadas — escolher sempre uma nova)

Saira Condensed · Abril Fatface · Gilda Display · Archivo Black · Alfa Slab One · Zilla Slab · Fraunces · Playfair · Rozha One · Cinzel · Anton · Yeseva One · DM Serif Display · Bricolage Grotesque · Cormorant Garamond · Marcellus · Bitter · Bodoni Moda · Big Shoulders Display · Yatra One · Libre Caslon Display · Shippori Mincho · Eczar · Bebas Neue · Spectral · Prata · Syne · Ultra · Sora · Unbounded · Staatliches · Crete Round · Averia Serif Libre · Passion One · Gloock · Instrument Serif (→ Mr. Buffalo) · Young Serif (→ Casa Corvo; repetida no Catarina por pedido explícito do brief V2 — zonas diferentes) · Chonburi (→ Paulo Molina) · Newsreader (→ Iguarias da Vila) · Lilita One (→ O Coral) · Bungee (→ Hanam KBBQ) · Erica One (→ Frango da Ria) · Italiana (→ Toda Chic, com Jost no corpo e Courier Prime nas notas) · Martel 900 (→ Pinhal Novo Mercado and Ria, com Mukta no corpo — par devanagari-latino, a pensar na comunidade sul-asiática) · Fredoka (→ Doris & Cia, com Nunito no corpo e Caveat no manuscrito)

**Livres/planeadas:** Bevan (→ Sítio dos Presuntos) · Rye · Kufam.

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
- **Pinhal Novo (Palmela):** pinhal-novo-mercado (`sites/pinhal-novo-mercado/`) — **Pinhal Novo Mercado and Ria** (mercearia, drogaria, acessórios de telemóvel; ficha Google `g/11l2h1fz7y`, 38.632305/−8.914796) + **Pinhal Novo Restaurant** (comida kebab, pizza, cozinha indiana; sem ficha no Google) do mesmo dono, lado a lado. Um site com duas portas e a ligação "do prato à prateleira". PT/EN. Martel + Mukta. Foto real da fachada do restaurante. **Tudo a confirmar:** morada, horário, telefone, carta e preços, lista de artigos (a Google bloqueada nesta sessão). Ângulo de venda: o restaurante ainda não aparece no Maps — criar a ficha e ligar os dois é parte do serviço.
- **Guarulhos · SP · Brasil (primeiro cliente brasileiro):** doris-e-cia (`sites/doris-e-cia/`) — Doris & Cia Pet Shop, banho e tosa + loja de ração, R. Alecsander Alves 162, Vila Barros, WhatsApp 11 97827-7667, 09h–19h (dias a confirmar), 5,0★/1 avaliação (omitido no site). **PT-BR, `lang="pt-BR"`**, moeda R$. Fredoka + Nunito + Caveat, fontes em base64 (`build.py` gera `index.html` a partir de `index.src.html`). Sem preços (o flyer diz "consulte"). Rodapé com consumidor.gov.br em vez de livroreclamacoes.pt (Brasil). Etiqueta interativa liga a `wa.me` com mensagem pré-preenchida. Zips Netlify e Hostinger na pasta. **Site é extra, não o produto:** a venda é trazer clientes + infraestrutura (ver `propostas/doris-e-cia/`).
- **Fuzeta** (pesquisa em `research/fuzeta.md`): casa-corvo (4,6★ RG/2.091, peixe frito, sem reservas — Young Serif, corvo + espinha) · paulo-molina (4,5★ RG/55, artigo VERSA "mestre Rui" — Chonburi, cardume; contactos a confirmar) · iguarias-da-vila (4,5★ TA nº5/32, TheFork, música ao vivo — Newsreader, azulejos; **já tem site → ângulo "elevar, não substituir"**) · o-coral (4,5★ RG/162, menu do dia — Lilita One, coral a ramificar)

### Propostas PDF

- Layout navy `#142238` + dourado `#C59A3E`. Script-tipo antigo (reportlab): `/home/claude/proposta_shalom.py` (dicionário T com pt/en).
- **Pipeline novo (22/09/2026): HTML → PDF com Playwright/Chromium**, em `propostas/<cliente>/` — `build.py` gera `proposta.html` (fontes Google embutidas em base64, diagrama SVG desenhado em código) e `render.js` imprime o PDF A4. Muito mais controlo de design do que o reportlab. Fontes do documento: Barlow Condensed + Inter + JetBrains Mono.
- **Be Legend Olhão (ginásio, belegend.pt)** — `propostas/be-legend-olhao/Be-Legend-Olhao-Follow-up-e-Recuperacao.pdf`, 9 páginas: sistema de *follow-up e recuperação de clientes* (motor de fluxo n8n, **nunca nomeado nos PDFs** — regra do Tomás: "é trabalho nosso", aparece só como "motor de fluxo") + WhatsApp Business API. Contexto dado pelo Tomás: a receção faz 100+ chamadas/dia e quase ninguém atende. Princípio do sistema: "ligar só a quem responde" (3 toques WhatsApp em 7 dias → lista diária para a receção; quem não responde fica em **pausa 3 semanas e recebe depois um novo toque com uma oferta pessoal**, ex.: desconto na mensalidade — regra pedida pelo Tomás para tirar ao dono o medo de "perder o contacto para sempre"; está na FAQ do documento completo). 5 fluxos: lead novo, aula experimental, inativo 14 dias, pagamento em atraso, renovação. Preço definido pelo Tomás: **2700 € montagem (IVA incluído) + 400 €/mês + IVA (492 €)**, mensalidade a cobrir **todos os ginásios Be Legend em Portugal** (Olhão, Faro, Lisboa) com servidores a funcionar e reparação prioritária; assistência presencial por um subdiretor da Pacheco Studios (dito no fim dos dois PDFs). Mensalidade média de sócio: 40 € (base dos cálculos de ganho). **Regra pedida pelo Tomás: não expor no documento o relato da receção de que "quase ninguém atende"** — o problema é descrito de forma neutra. **Segundo PDF, curto:** `Be-Legend-Olhao-O-que-vai-mudar.pdf` (6 páginas, `build_resumo.py`) — antes/depois em 5 linhas; os 6 passos do fluxo com o que o dono decide em cada um; **duas variantes à escolha** (A: chamada primeiro, o sistema recupera por WhatsApp quem não atende; B: mensagem primeiro, a receção liga só a quem respondeu), com vantagem/desvantagem; **página de ofertas rotativas** (3 ativas, renovadas a cada 3 meses; ingredientes que o ginásio já tem: batido de proteína, água, massagista, 1 h de personal trainer para fechar mensalidade — só opções, sem pacotes fechados); **projeção** para 100 chamadas/dia num só ginásio com pressupostos explícitos (20 % atendem chamada fria, 35 % respondem ao WhatsApp, 70 % atendem chamada quente, 25/35 % conversão, 2/5 min) — hoje 5/dia em 5 h; A 12/dia em 7,6 h; B 9/dia em 3,2 h — e **ganhos a 40 €/mensalidade** no fim da tabela (ganho líquido/mês num ginásio: A +5 545 €, B +2 654 €, já descontados os 492 €); página de escolha com checkboxes (Variante A / B / "Aplicável em todos os Be Legend Portugal") e assinatura. Pressupostos não medidos: o piloto substitui-os. **Terceiro PDF:** `Be-Legend-Programa-de-Parceiros.pdf` (2 páginas, `build_parceiros.py`) — recompensa por recomendação **em desconto, não em dinheiro**: por cada negócio fechado por recomendação do Be Legend, um mês de mensalidade grátis, com dois meses de intervalo (fecho em setembro → dezembro grátis; dois fechos → dezembro e janeiro; nunca se perdem, empurram para o mês seguinte). Conta a partir do pagamento da montagem pelo cliente apresentado; sem limite; não convertível em dinheiro; inclui **10 % de desconto na montagem para quem chega pela recomendação do Be Legend** e uma mensagem de exemplo (a recomendação pode ser numa conversa de café; a pessoa contacta o Tomás depois). Decisão do Tomás depois da minha recomendação (sem obrigações ao cliente, sem comissão sobre mensalidades). Nota discreta nos dois documentos principais: "mais tarde, o mesmo motor pode receber um segundo fluxo: aquisição de novos clientes" (pedido do Tomás: sem ruído). Enviar os três PDFs juntos.
- **Doris & Cia Pet Shop (Guarulhos, Brasil)** — `propostas/doris-e-cia/Doris-e-Cia-Plano-de-Impulso.pdf` (6 páginas, PT-BR, `build_checklist.py`, reutiliza o CSS do Be Legend): diagnóstico da ficha Google e Instagram (**categoria errada "Loja de répteis"**, sem descrição, 1 avaliação, capa com ração, dois Instagrams, sem preços públicos, sem agendamento online, sem site), checklist em 4 fases (arrumar de graça → oferta e infraestrutura → anúncios → fidelização), 3 níveis de Meta Ads (R$ 400 / 800 / 1.500 com premissas explícitas: R$ 8/conversa, 40 % agendam, ticket R$ 55, 40 % recorrem), perguntas para a dona e próximos passos. **Regra do Tomás: o site é extra; a venda é clientes + infraestrutura.** Reunião marcada para 23/09/2026. Links do Google Maps e Instagram estão bloqueados nesta sessão: os dados vieram de prints enviados pelo Tomás.
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

- [ ] **Doris & Cia (Guarulhos)** — reunião 23/09. Confirmar na reunião: dias/folga, preços por porte, gatos, leva e traz, qual Instagram fica principal, software/planilha de clientes, nível de ads. Preços da Pacheco em R$ ainda por definir (tabela do playbook é em €). Depois: arrumar categoria + descrição + fotos no Google, pedir avaliações, WhatsApp Business, agendamento, site no ar (extra).

- [ ] **Be Legend Olhão** — enviar o PDF por e-mail ao dono; se houver interesse: reunião de 30 min (confirmar o software de gestão do ginásio e o que exporta; número de WhatsApp Business; voz das mensagens), piloto de 30 dias só com o fluxo de inativos. Preço fechado pelo Tomás (2700 € IVA incl. + 400 €/mês + IVA, todos os Legends); falta a aceitação do dono e a escolha da variante A/B.

- [ ] **Sítio dos Presuntos** (Gambelas/Montenegro) — site por criar. Tasca beirã, donos de Viseu, R. Aquilino Ribeiro (nº 122 vs 212 a confirmar), tel 917 823 784 (TA) / 919 869 212 (booktables), Google 4,3/~1.220, até às 23:00. Pratos: presunto, leitão, tamboril, lula grelhada, sopa de feijão verde. Identidade planeada: Bevan, presuntos pendurados a balançar.
- [ ] **O Caseiro2** (ex-"O Bandeira", Montenegro) — 4,6★/438, menu de almoço ~12 €, fecha 2.ª feira. Site se houver interesse.
- [ ] **2.º lote VNC/Manta Rota:** Casa da Igreja (Cacela Velha, 289 952 126, 4,3★/329, ostras) · Pizzadela (963 350 428, 4,7★/254) · Bela Vista (4,4★/107, porco preto) · O Ligério (281 951 372) · Casa Velha (281 952 297) · Restaurante Manta Rota · O Finalmente. *(Chá com Água Salgada já tem site — excluir.)*
- [ ] **Restaurante Avenida** (Tavira) — site completo com cores, logótipo e ementa reais.
- [ ] **Instituto dos Ferroviários** — logótipo oficial, detalhes da festa, cartaz para Instagram.
- [x] Telefone do Tomás (967 117 357) nas propostas PDF — feito nos PDFs do Be Legend, replicar nos outros.
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
- **Montagem de WooCommerce em PT:** passo a passo completo em `research/woocommerce-pt-passo-a-passo.md` (alojamento → WooCommerce → legais → **ifthenpay/MB WAY** → faturação AT → envios → stock → catálogo → conta *Gestor da loja* para o cliente). Dois erros que custam caro: **esquecer o callback da ifthenpay** (o dinheiro entra mas a encomenda fica "a aguardar") e **dar Administrador ao cliente** em vez de Gestor da loja. Entregar sempre o manual do cliente (modelo: `sites/toda-chic/MANUAL-DONA.md`) — faz parte do produto, não é extra.
- Fluxo do impeccable para cliente novo: `impeccable context` → `reference/init.md` → **PRODUCT.md por cliente** (`sites/<cliente>/PRODUCT.md`, não na raiz) → `new-work` para o mundo visual → `detect` antes de entregar.
- **Fotos de Instagram como matéria-prima** (aprendido a 21/09): as donas de lojas pequenas têm o catálogo inteiro em stories, com faixa da marca, preço e rótulos queimados na imagem. Não pedir "fotos limpas" à cabeça — transcrever primeiro as fichas manuscritas (preço, tamanho, cor, unidades — são a única fonte de verdade) e limpar as fotos com `sites/toda-chic/ferramentas/fotos.py` (corte da faixa por transições de texto, inpainting dos rótulos com OpenCV, recorte 4:5). Só depois pedir fotos novas do que ficou fraco. Uma peça em várias cores = um produto com fotos por cor.
- **Demo de loja = ficheiro único com router por `#/`** (início, `#/c/categoria`, `#/p/peça`, favoritos, saco, páginas). Catálogo em JSON dentro do HTML, imagens em `media/` (não em base64: 80 fotos seriam 5 MB de HTML). Favoritos e saco em `localStorage` para que o cliente sinta a loja a funcionar na apresentação. Publicar como artefacto multi-ficheiro (`files`) e como zip Netlify com a pasta `media/`.
