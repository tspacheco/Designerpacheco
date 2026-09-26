# pachecost.com + ro.pachecost.com — o site da Pacheco Studios em três línguas

Um só site, um só projeto no Netlify, dois domínios:

| Endereço | Língua | Para quê |
|---|---|---|
| `pachecost.com` | Português | a página principal (mercado português) |
| `pachecost.com/en/` | Inglês | clientes estrangeiros |
| `ro.pachecost.com` | Romeno | para onde aponta o QR dos cartões (`HTTPS://RO.PACHECOST.COM/C`) |

No topo de cada página há o seletor **PT · EN · RO**. O RO leva a `ro.pachecost.com`; o PT e o EN ficam em
`pachecost.com`. Os três têm as mesmas três vistas e o contacto no fim:

1. **Projetos** — um quadrado por cliente real, com a fonte e as cores do próprio site: os clientes de pachecost.com,
   mais o Jasmim 2 e a Toda Chic. As apresentações a negócios que não compraram ficam de fora (decisão de 26/09).
   Primeira fila, em qualquer ecrã: **Jasmim 2, Hanam e Toda Chic**. Ao tocar, abre o site do cliente num separador
   novo. A Toda Chic ainda não tem loja publicada: abre a cópia em `/p/toda-chic/` (uma página por língua), com o
   botão fixo de voltar na língua certa. No fim da grelha, o quadrado tracejado leva ao contacto. Por baixo,
   «Como trabalhamos»: fazemos o site antes de pagares, mostramos no telemóvel, só pagas se gostares.
2. **Automações** — segue a direção «mostrar a máquina» (PLAYBOOK, secção 16). No topo, «O que é, afinal, a IA
   por trás?»: cinco frases sobre o que a IA faz e não faz. Depois, 8 automações. Cada cartão mostra o título e a
   dor na voz do dono. Ao tocar, abre a máquina por dentro: o fluxo desenhado (gatilho, automático, pessoa,
   decisão), o que ganha, as regras, quem decide o quê, uma conversa de exemplo, o que é preciso, com quais combina
   e o pedido de demonstração no WhatsApp. No fim, três caminhos (restaurante · salão/clínica · loja).
3. **O que mais fazemos** — 7 serviços, com «Ver um exemplo» quando há um cliente que o mostra.

Sem preços: combinam-se com cada negócio.

## Editar

- Textos: `conteudo/pt.json`, `conteudo/en.json` e `conteudo/ro.json`. A estrutura é igual nos três (o gerador
  recusa-se a avançar se faltar uma letra nas fontes).
- Quadrados: `portfolio.json`, pela ordem do ficheiro — `ativo`, `destaque` (os três da primeira fila), `nome`,
  `fonte`/`peso`/`bg`/`ink`/`accent` (as do site), `url` (site do cliente, abre noutro separador) ou `pasta` (site do
  repositório, copiado para `/p/<slug>/`, só para clientes sem site publicado). `demo: true` marca as apresentações:
  nunca entram. A ProBuilders está desligada até o site sair. O Jasmim 2 está em `neutro` (estilo da marca) até
  termos a fonte e as cores do site dele.
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
  cliques para o WhatsApp e o telefone como `ir/whatsapp` e `ir/telefone`.
- **Pixel da Meta** só em `pachecost.com` (PT e EN), só depois de «Aceitar» na faixa. A escolha fica guardada.
  Em `ro.pachecost.com` não há pixel nem faixa: quem lê o QR entra direto nos projetos.
- Privacidade em cada língua: `/privacidade.html`, `/privacy.html`, `/confidentialitate.html`.

O site anterior do pachecost.com (o «Estúdio de IA») está guardado em `sites/pachecost-com/`.

## O que o gerador verifica

`verificar.cjs` serve `dist/` como o Netlify serviria os dois domínios: lê o `_redirects` e aplica-o.

- O QR impresso (`ro.pachecost.com/C`) chega à página romena com um 302. Cada endereço abre na língua certa, e os
  antigos redirecionam com 301.
- Canonical, hreflang das 3 línguas, seletor com a língua atual marcada, imagem de partilha por língua. O seletor
  navega PT → RO → EN → PT entre os dois domínios.
- Em 360, 390 e 1280 px, nas 3 línguas e nas 3 vistas: sem scroll horizontal, letra ≥ 12 px, contraste ≥ 4,5:1,
  alvos de toque ≥ 44 px e títulos por ordem.
- Separadores com e sem JavaScript, as 8 automatizações e as ligações entre elas. Cada quadrado e cada exemplo tem
  de existir. A primeira fila tem de ter os três em destaque. A Toda Chic tem de voltar à página certa.
- A 404 e a privacidade em cada língua, e a barra fixa do WhatsApp.
- A faixa de cookies: aparece só em pachecost.com, «Só o essencial» nunca carrega o pixel e «Aceitar» carrega-o.
  Nos dois casos a escolha fica guardada.
