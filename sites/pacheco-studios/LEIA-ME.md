# pachecost.com + ro.pachecost.com — o site da Pacheco Studios em três línguas

Um só site, um só projeto no Netlify, dois domínios:

| Endereço | Língua | Para quê |
|---|---|---|
| `pachecost.com` | Português | a página principal (mercado português) |
| `pachecost.com/en/` | Inglês | clientes estrangeiros |
| `ro.pachecost.com` | Romeno | para onde aponta o QR dos cartões (`HTTPS://RO.PACHECOST.COM/C`) |

No topo de cada página há o seletor **PT · EN · RO**. O RO leva a `ro.pachecost.com`; o PT e o EN ficam em
`pachecost.com`. Os três têm as mesmas quatro vistas e o contacto no fim.

> **Intro desligada desde 05/10 (pedido do Tomás, «por enquanto»).** Para a ligar: `INTRO_LIGADA = True` em `gerar.py`
> e gerar de novo. O que segue descreve-a quando está ligada.
>
> **Vídeo do herói com o scroll também desligado desde 05/10:** fica a imagem `media/heroi.webp` parada. Para o ligar:
> `HEROI_VIDEO = True` em `gerar.py`.

Na primeira visita de cada sessão, antes do site, corre a **intro** (4 s): um compacto entra, passa pelo portal «Diagnóstico»
(antes «Web design + marketing») e sai muscle car, passa pelo portal «Implementação de IA» e sai superdesportivo; arranca, aparece a
marca com o slogan e o ecrã sobe para mostrar o site. Um toque, o botão «Saltar» ou Esc saltam-na. Não aparece ao
recarregar, com o movimento reduzido ligado no telemóvel nem sem JavaScript; se as fotografias demorarem mais de 1,5 s,
o site abre sem ela. As fotografias (`media/intro-{1,2,3}.webp`, geradas, sem marcas registadas) só existem na intro:
nunca no corpo do site. Para as trocar: `intro-prompts.md`.

**Reposicionamento de 02/10/2026: a Pacheco Studios é uma consultoria de IA** (diagnóstico → desenho → piloto →
acompanhamento). A vista de entrada passou a ser a Consultoria; os Sites passaram a ser uma das soluções. Pesquisa e
decisões: `research/consultoria-ia-referencias.md` e PLAYBOOK, secção 17.

1. **Consultoria** (EN «Consulting», RO «Consultanță», `#consultanta`, a vista de entrada) — o herói repete a frase
   da marca: «Tens um objetivo a atingir? / A IA VAI FAZÊ-LO ACONTECER. / Só tens de dar o primeiro passo.», com o
   botão «Marcar o diagnóstico» (WhatsApp). Depois: agência vs consultoria; os cinco passos (conversa de 20 min →
   diagnóstico escrito no mesmo dia → solução desenhada → piloto de 30 dias → acompanhamento); «O que é, afinal, a
   IA por trás?» (as cinco frases de sempre, agora à vista, saíram das Automações); três números de casos reais
   (cada um leva ao caso); os compromissos; «Falas sempre com a mesma pessoa» (o Tomás).
**Atualização de 03/10, à tarde:**
- Cada caso mostra só o depoimento (`depo`) e os 3 números.
- Saíram o nome, o tipo de negócio, o problema e a solução, a caixa «próximo caso», os chips «Caso real» das Soluções e o bloco «Sites: como fazemos» (fazemos antes de pagares).
- As Soluções abrem só com uma frase.

2. **Casos** (EN «Cases», RO «Cazuri», `#cazuri`): **resultados reais de outros negócios, mostrados como «onde podes chegar»**. Decisão do Tomás de 03/10:
   - **Sem qualquer nome ou ligação à fonte no site.** As fontes ficam em `conteudo/casos.json` (interno, não vai para o zip).
   - O texto diz que os resultados já aconteceram noutros negócios. Nunca diz que são clientes nossos.
   - Cada cartão tem: o selo «Onde podes chegar», 3 números, o problema, o que fizeram e «No teu negócio, isto é» (liga à nossa solução).
   - No fim fica «Pacheco Studios · o próximo caso», com «Quero este resultado» no WhatsApp, e «Como um caso destes passa a ser teu».

   Na Consultoria (versão de 03/10):
   - **Herói:** a frase da marca a dois tons, sobre a imagem `media/heroi.webp`. Imagem gerada no Higgsfield (gpt_image_2_5, 16:9): placas escuras a flutuar com fios de luz laranja e o lado esquerdo vazio para o texto. Vai embutida na página, para abrir também fora do Netlify. Se faltar, o herói fica só escuro. Por cima corre o vídeo em scroll to animation: o vídeo Kling ampliado a 4K (Topaz) e cortado em 61 fotogramas em `media/heroi-hd/` — `d/` 16:9 a 1920 px para ecrãs deitados (2,6 MB) e `v/` recorte 9:16 a 720×1280 para telemóvel ao alto (1,7 MB). São ficheiros à parte, carregados pelo JavaScript (o primeiro logo, os outros quando o rolo arranca), desenhados um de cada vez num canvas conforme o scroll; o herói fica preso ao ecrã durante 240vh. Sem fusão entre fotogramas: num zoom desdobra as arestas e parece desfocado. Sem JavaScript, com movimento reduzido ou se o texto não couber, fica a imagem parada. Para trocar o vídeo: pôr «fotogramas sites/pacheco-studios/media/heroi-hd <passo> <url do mp4 em 4K>» em `.github/ponte.txt` e fazer push; a ponte extrai os fotogramas e faz commit no ramo; depois `git pull` e voltar a gerar.
   - **Botões:** «Conhece-nos» abre o diagnóstico; «Ver soluções» vai às Soluções. Por baixo: «Adere hoje aos sistemas que a IA te pode entregar…».
   - **Logótipo:** o «P» no anel dourado, no cabeçalho, em vez do ponto laranja.
   - **Diagnóstico:**
     - Uma pergunta por ecrã, em grande. Opções com letras (A, B, C…, também pelo teclado) e os botões Anterior e Seguinte.
     - A **ficha do teu negócio**, em papel pontilhado, preenche-se ao lado (no telemóvel, no fim).
     - No fim, «Enviar pelo WhatsApp» com a ficha inteira. Nada é guardado.
   - **Secções a seguir ao herói:**
     - «O que faz uma consultoria de IA»: uma caixa com 3 passos.
     - O veredito de um caso sobre o mosaico 3D.
     - O que é a IA.
     - Os números dos casos.
     - A responsabilidade, com 4 compromissos.
   - **Saíram:** os 5 passos, «Nunca inventamos números», «Sais quando quiseres» e «Quem está por trás».

3. **Soluções** (antes «Automações»; EN «Solutions», RO «Soluții») — segue a direção «mostrar a máquina» (PLAYBOOK, secção 16). As cinco frases «O que é, afinal, a IA
   por trás?» passaram para a Consultoria. Aqui ficam as 8 automações. Cada cartão mostra o título e a
   dor na voz do dono. Ao tocar, abre a máquina por dentro. Primeiro vem o botão **«Ver o esquema»** (EN «See the
   diagram», RO «Vezi schema»): abre um cartão no meio do ecrã com o fluxo desenhado como a proposta da Be Legend.
   Tela pontilhada, uma caixa por passo com o seu ícone, gatilho a âmbar, pessoa a verde, decisão tracejada com os
   ramos em pílulas, esperas a bege e a legenda no fim. Fecha com o X, com Esc ou tocando fora. Depois do botão: o
   que ganha, as regras, quem decide o quê, uma conversa de exemplo, o que é preciso, com quais combina e o pedido
   de demonstração no WhatsApp. No fim, três caminhos (restaurante · salão/clínica · loja).
   No fim das Soluções fica «E também» (`#servicii`, o antigo «O que mais fazemos»): 7 serviços, com «Ver um
   exemplo» quando há um cliente que o mostra. Cada automação com caso real mostra «Caso real» com ligação ao cartão.

4. **Sites** (EN «Websites», RO «Site-uri») — não mostra quantos trabalhos temos nem pede «o teu negócio»
   (decisão do Tomás, 29/09): passa responsabilidade e conhecimento de mercado, como as automações.
   - **Em destaque:** Jasmim 2, HANAM e Toda Chic, com a fonte e as cores de cada site.
   - **Por tipo de negócio:** quatro cartões que abrem como os das automações: restaurantes e marisqueiras; cafés,
     pastelarias e gelatarias; lojas online; serviços com marcação. Fechado, mostra como o cliente escolhe. Aberto,
     mostra as perguntas do cliente e o que o site responde, ligadas por pontos como numa ementa. Mostra também os
     sites que já fizemos para esse tipo, as automações que combinam e o pedido no WhatsApp.
   - **O que fica ao nosso cuidado:** seis compromissos que já cumprimos em todos os sites: dados verdadeiros, abre
     depressa, Google, leitura para toda a gente, a lei e a manutenção.
   - **Como trabalhamos:** fazemos o site antes de pagares, mostramos no telemóvel, só pagas se gostares.
   - **Mais sites que fizemos:** no fim, os outros sites ativos numa grelha simples, só para mostrar mais variações;
     sem quadrado «O teu negócio?».

   Os sites dos clientes abrem num separador novo. A Toda Chic ainda não tem loja publicada: abre a cópia em
   `/p/toda-chic/` (uma página por língua), com o botão fixo de voltar na língua certa. As apresentações a negócios
   que não compraram nunca entram (decisão de 26/09).

Sem preços: combinam-se com cada negócio.

**Anúncios de sites:** quem chega com `utm_content=web-…` (as campanhas Meta de web design) entra direto nos Sites, que é o que o anúncio mostrou.

## Editar

- Casos: `conteudo/casos.json` (empresa, ligação para a fonte, a que soluções nossas se aplica, quais aparecem na
  Consultoria) + os textos de cada língua em `cazuri.itens` dos três JSON, com o mesmo id. O gerador trava se faltar
  um caso numa língua, se um caso não tiver 3 números ou se apontar para uma solução que não existe.
- Textos: `conteudo/pt.json`, `conteudo/en.json` e `conteudo/ro.json`. A estrutura é igual nos três (o gerador
  recusa-se a avançar se faltar uma letra nas fontes).
- Sites: `portfolio.json`, pela ordem do ficheiro — `ativo`, `destaque` (os três «Em destaque»), `setor` (o cartão
  do tipo de negócio: `restauracao`, `cafes`, `lojas` ou `marcacoes`), `nome`,
  `fonte`/`peso`/`bg`/`ink`/`accent` (as do site), `url` (site do cliente, abre noutro separador) ou `pasta` (site do
  repositório, copiado para `/p/<slug>/`, só para clientes sem site publicado). `demo: true` marca as apresentações:
  nunca entram. A ProBuilders está desligada até o site sair. O Ola Kathmandu está desligado desde 29/09: o
  `olakathmandu.com` não abre. O Jasmim 2 está em `neutro` (estilo da marca) até termos a fonte e as cores
  do site dele.
- Tipos de negócio: `proiecte.setores` nos três JSON. Cada um tem `tipos`, `decide` (como o cliente escolhe), `qa`
  (pergunta do cliente e resposta do site) e `combina` (ids das automações). Só se escreve o que os nossos sites
  fazem mesmo.
- Esquemas: os passos são o `fluxo` de cada automação nos três JSON (`tip`, `t`, `d`; `espera` junta uma caixa de
  espera antes do passo; `ramuri` faz a decisão e os ramos). Os ícones estão em `conteudo/esquemas.json`, um por
  passo e um por ramo, iguais nas três línguas. Os desenhos dos ícones estão em `ICONES_ESQUEMA`, no `gerar.py`. Se
  faltar um ícone, o gerador para e diz qual.
- Intro: os textos estão em `intro` nos três JSON (rótulos dos portais, as três legendas, «Saltar» e a descrição para
  leitores de ecrã); o slogan do fim é o de `og`. As fotografias são `media/intro-{1,2,3}.webp` (o JavaScript mede cada
  uma ao carregar; só o comprimento no palco está fixo em `CARROS`, no `index.src.html`, com os tempos em `T`). Como
  gerar outras: `intro-prompts.md`.
- Contactos, domínios e medição: `marca/dados.json` (os mesmos do cartão). `medicao` tem o GoatCounter e o pixel da
  Meta do site anterior; o pixel só existe nas línguas de `pixel_linguas` (PT e EN).
- Desenho: `index.src.html`. As páginas (`index.html`, `en/`, `ro/`, 404, privacidade) e os ficheiros do Netlify
  (`_redirects`, `_headers`, `netlify.toml`, `robots.txt`, `sitemap.xml`) são gerados: não editar à mão.

Depois de qualquer alteração: `python3 gerar.py`. Gera `dist/`, corre os testes e faz `pacheco-studios-netlify.zip`
(~7 MB; não vai para o git).

## Publicar

É o **mesmo projeto do Netlify que já tem o pachecost.com**. O `pachecost.com` usa o DNS do Netlify (servidores
`nsone.net`), por isso não é preciso mexer no DNS à mão.

1. `python3 gerar.py` → sai `pacheco-studios-netlify.zip`.
2. Netlify → o projeto do pachecost.com → *Deploys* → arrastar o zip para a caixa de publicação manual.
   A partir daqui, `pachecost.com` abre em português.
3. Só na primeira vez: no mesmo projeto → *Domain management* → *Add a domain* (ou *Add domain alias*) →
   `ro.pachecost.com` → confirmar. O Netlify cria o registo sozinho e liga o HTTPS em minutos (às vezes até uma
   hora).
   - Se o DNS do `pachecost.com` estiver noutra conta: nessa conta, *Domains* → `pachecost.com` → *Add new record* →
     `CNAME`, nome `ro`, valor `<nome-do-projeto>.netlify.app`.
4. Testar no telemóvel: ler o QR de um cartão → abre em romeno; `pachecost.com` → português; o seletor muda de língua;
   um quadrado da Toda Chic abre e o botão de voltar regressa à mesma língua.

Para atualizar: `python3 gerar.py` → *Deploys* → arrastar o zip novo. O QR não muda.

**Mandar um esquema a alguém** (no WhatsApp, depois de uma conversa): `pachecost.com/#esquema-programari` abre o
desenho direto; ao fechar, fica-se na automação dele. Em romeno: `ro.pachecost.com/#esquema-programari`. Os oito:
`receptionist` · `programari` · `recenzii` · `lead` · `documente` · `revenire` · `raport` · `social`.

### Como os dois domínios funcionam (o `_redirects`)

1. `/c` e `/C` → `/?origem=cartao` (302). Ficam **sempre em primeiro lugar**: é o QR impresso.
2. `https://ro.pachecost.com/` é servido pela página romena (`/ro/index.html`, reescrita 200). Todos os outros
   ficheiros (`/p/`, `/media/`, privacidade) são partilhados pelos dois domínios.
3. `pachecost.com/ro/` → `ro.pachecost.com`; `ro.pachecost.com/en/` → `pachecost.com/en/`; o antigo `/pt/` →
   `pachecost.com` (301).
4. Uma página 404 em cada língua.

Tem de ser Netlify: estas regras não existem no Hostinger. As cópias em `/p/` levam `noindex` (na página e no
cabeçalho), para não competirem no Google com os sites dos próprios negócios.

### Medição (igual ao site anterior)

- **GoatCounter**, sem cookies e sem pedir autorização, nos dois domínios. O domínio entra no caminho
  (`pachecost.com/`, `ro.pachecost.com/`). As leituras do QR contam à parte, como o evento `qr/cartao`, e os
  cliques para o WhatsApp e o telefone como `ir/whatsapp` e `ir/telefone`. Cada esquema aberto conta como
  `esquema/<id>` (`esquema/programari`, por exemplo): dá para ver quais automações interessam mais.
- **Link direto ao diagnóstico (anúncios):** `pachecost.com/#diagnostico` ou qualquer link com `utm_content=diag-…`
  abre o diagnóstico logo ao chegar, sem a intro. Fechar volta à página inicial. Os links com `utm_content=web-…` não mudam.
- **Medir o diagnóstico** (painel em https://pachecost.goatcounter.com; eventos em «diagnostico/…»): `aberto` (tocou
  em «Conhece-nos») → `comecou` → `pergunta-01-nome` … `pergunta-08-contacto` (a 1.ª vez que chega a cada uma; a
  diferença entre duas seguidas é quem desistiu ali) → `fim` → `enviado` (tocou em «Enviar pelo WhatsApp»; é o número
  que conta). No pixel da Meta, `enviado` vai como `Lead`. `ir/whatsapp` conta só os outros botões de WhatsApp.
- **Sem faixa de cookies (decisão do Tomás, 04/10):** nada aparece ao abrir o site. O rodapé diz «Ao usares este site
  aceitas os nossos termos: a política de privacidade e a política de cookies», com as duas ligações.
- **Pixel da Meta** só em `pachecost.com` (PT e EN) e carrega sozinho. Desliga-se na página Cookies (`cookies.html`,
  `en/cookies.html`), que guarda `ps-consentimento = nao` neste navegador; com o sinal Global Privacy Control também não
  carrega. Em `ro.pachecost.com` não há pixel; a página é `cookie-uri.html`.
  **Risco assumido:** na UE, «continuar a navegar» não conta como consentimento para cookies de publicidade (TJUE
  Planet49, CNPD, diretrizes EDPB 05/2020), e a Meta exige consentimento aos anunciantes. O Tomás foi avisado a 04/10 e
  escolheu assim. Para voltar a pedir autorização, a faixa antiga está no histórico do git (antes de 04/10).
- Privacidade em cada língua: `/privacidade.html`, `/privacy.html`, `/confidentialitate.html`.

O site anterior do pachecost.com (o «Estúdio de IA») está guardado em `sites/pachecost-com/`.

## O que o gerador verifica

Antes de gerar, o `gerar.py` confirma no DNS que o domínio de cada quadrado existe. Um link morto trava a publicação e
diz qual é: experimentar o mesmo nome em .pt e .online e, se também não existirem, pôr `ativo: false`. Sem rede, só
avisa.

`verificar.cjs` serve `dist/` como o Netlify serviria os dois domínios: lê o `_redirects` e aplica-o.

- O QR impresso (`ro.pachecost.com/C`) chega à página romena com um 302. Cada endereço abre na língua certa, e os
  antigos redirecionam com 301.
- Canonical, hreflang das 3 línguas, seletor com a língua atual marcada, imagem de partilha por língua. O seletor
  navega PT → RO → EN → PT entre os dois domínios.
- Em 360, 390 e 1280 px, nas 3 línguas e nas 3 vistas: sem scroll horizontal, letra ≥ 12 px, contraste ≥ 4,5:1,
  alvos de toque ≥ 44 px e títulos por ordem.
- Os 8 esquemas nas 3 línguas, a 360 e a 1280 px: cada um abre num cartão no meio do ecrã, com o foco lá dentro, e
  nenhuma caixa sai da tela. Letra, contraste e títulos também dentro do cartão. Esc, o X e tocar fora fecham; pelo
  teclado, o foco volta ao botão. O endereço `#esquema-…` abre-o direto e, sem JavaScript, mostra-o na mesma.
- Separadores com e sem JavaScript, as 8 automatizações e as ligações entre elas. Três sites em destaque e mais
  nenhum na grelha. Os 4 tipos de negócio, cada site ativo dentro de um deles, e cada ligação tem de existir. O
  «Combina com» abre a automação. A Toda Chic tem de voltar à página certa. Os testes de leitura abrem todos os
  cartões antes de medir.
- A 404 e a privacidade em cada língua, e a barra fixa do WhatsApp.
- A intro, nas 3 línguas: na 1.ª visita da sessão aparece com as três fotografias e os textos certos, a página por
  baixo fica inerte, sobe no fim (≈ 4 s) e não volta ao recarregar; «Saltar» e Esc saltam-na; com movimento reduzido ou
  sem JavaScript não aparece. Letra, contraste e alvos de toque também dentro dela.
- Cookies: nada aparece ao abrir; o pixel carrega sozinho em pachecost.com, nunca em ro.pachecost.com; o botão da página Cookies desliga-o e volta a ligá-lo; com Global Privacy Control não carrega.
  Nos dois casos a escolha fica guardada.
