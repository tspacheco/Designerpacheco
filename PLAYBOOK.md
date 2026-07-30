# PACHECO STUDIOS — PLAYBOOK MESTRE

> Fonte de verdade da Pacheco Studios. Substitui todo o histórico de chats.
> Última atualização: 30/07/2026 (integrado no repositório + padrão NÍVEL 10K)

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

ensō japonês · mandala · tagliatelle a cair · brasas a subir · rubrica manuscrita · ondas de açúcar + canela · folha line-art a desenhar-se · anéis de fumo + selo rotativo · bandeirolas náuticas a balançar · pincelada a pintar-se + blobs · pedra com heat-haze · pizza a girar + textura de tijolo · grelha com sardinhas + fumo · riscas de toalha + cataplana · notas musicais a flutuar · cena de praia em SVG (céu/mar/areia) · veios de marmoreio a desenharem-se + barra de pontos de cozedura + "00:00" monumental (Mr. Buffalo) · corvo a pousar no título + espinha de peixe divisora (Casa Corvo) · cardume SVG a atravessar a página (Paulo Molina) · padrão de azulejo a compor-se (Iguarias da Vila) · coral a ramificar-se em stroke-draw (O Coral)

## 6. TRACKER DE FONTES DISPLAY (já usadas — escolher sempre uma nova)

Saira Condensed · Abril Fatface · Gilda Display · Archivo Black · Alfa Slab One · Zilla Slab · Fraunces · Playfair · Rozha One · Cinzel · Anton · Yeseva One · DM Serif Display · Bricolage Grotesque · Cormorant Garamond · Marcellus · Bitter · Bodoni Moda · Big Shoulders Display · Yatra One · Libre Caslon Display · Shippori Mincho · Eczar · Bebas Neue · Spectral · Prata · Syne · Ultra · Sora · Unbounded · Staatliches · Crete Round · Averia Serif Libre · Passion One · Gloock · Instrument Serif (→ Mr. Buffalo) · Young Serif (→ Casa Corvo) · Chonburi (→ Paulo Molina) · Newsreader (→ Iguarias da Vila) · Lilita One (→ O Coral)

**Livres/planeadas:** Bevan (→ Sítio dos Presuntos) · Rye · Kufam · Erica One · Bungee.

*(Caveat e Kalam são fontes de acento manuscrito — podem repetir.)*

## 7. CATÁLOGO — SITES JÁ CRIADOS

### ★ VENDIDO

| Cliente | Notas |
|---|---|
| Grupo Naval (Olhão) | **1.ª VENDA FECHADA.** 4,3★/1.041, tel 289 050 543, Av. 5 de Outubro. Banner Pacheco removido. Pendente: ementa do Carlos, canonical quando houver domínio, fotos próprias. |

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
- [ ] Acrescentar telefone do Tomás às propostas PDF.
- [ ] Registar taxas de fecho por tipo de negócio (Albufeira, Gambelas, VNC).

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
