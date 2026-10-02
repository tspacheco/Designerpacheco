# pachecost.com — alterações de 01–02/10/2026

O site da Pacheco Studios não vive neste repositório: é gerado por `gerar.py` a partir de `marca/dados.json` (no PC do Tomás) e publicado no Netlify. Esta pasta guarda as alterações feitas sobre o deploy exportado a 01/10, para as repetir ou passar para o gerador. `aplicar.py` lê `cur/` (deploy exportado) e escreve `novo/`; `pachecost-anuncio.patch` mostra as linhas exatas nos 3 ficheiros (`index.html`, `ro/index.html`, `en/index.html`). Capturas: `captura-*.png`.

## 6. Foco: automações com IA (02/10)

- **Vista inicial = Automações.** Separadores por ordem: Automações · Sites · O que mais fazemos. A lógica vive em CSS (`:has`, como o resto da página) e no `vista()` do JavaScript, por isso funciona sem JavaScript e com os endereços `#…` partilhados.
- **Cabeçalho das automações:** "Automações com IA" · "A IA faz o trabalho de todos os dias. Tu aprovas." (RO: "Automatizări cu AI" · "AI-ul face treaba de zi cu zi. Tu aprobi." · EN: "AI automations" · "AI does the everyday work. You approve."). Os leads ficam como estavam.
- **Título, descrição, og:title e JSON-LD** reescritos nas três línguas com as automações à frente (ex.: "Automações com IA no WhatsApp que respondem, marcam, confirmam e trazem os clientes de volta, e o site por onde eles entram. Vês uma demonstração antes de decidir."). As imagens `og-*.png` não foram tocadas.
- **Contacto:** "Mostramos-te a automação a responder ou o site já feito. Sem compromisso." A mensagem pré-escrita do WhatsApp deixa de dizer "Vi os sites da Pacheco Studios" e passa a "Vi a Pacheco Studios…" (3 ligações por página).
- **Ponte das automações para os sites** no fim da vista das automações: "E o site?" · "O site é por onde os clientes entram." · botão "Ver os sites que fizemos" (`#proiecte`) · os três quadrados em destaque, em versão pequena.
- A ponte dos sites para as automações (secção 5) e o lema (secção 4, agora em ambas as vistas) ficam.

### Para onde vai cada ligação

| Ligação | Onde cai |
|---|---|
| `pachecost.com`, `ro.pachecost.com`, cartão `/C` (→ `/?origem=cartao`) | Automações, com o lema |
| Anúncio de um site (`?utm_…`, `fbclid`, `?origem=anuncio`, **sem** `#`) | Sites, com o herói "Um site assim para o teu restaurante" (foi isso que o vídeo mostrou) |
| Anúncio de automações: `pachecost.com/?utm_source=facebook#automatizari` | Automações, sem herói (o `#automatizari` manda) |
| Qualquer endereço com `#proiecte` | Sites |

Os dois anúncios a correr (até ~06/10) apontam para `/?utm_source…` sem `#`: continuam a cair nos sites. Os anúncios seguintes, sobre automações, levam `#automatizari` no fim.

## 1. Primeiro ecrã para quem chega por anúncio (PT e RO)

Só para quem chega com `?utm_…`, `fbclid` (a app do Facebook acrescenta-o a todos os cliques) ou `?origem=anuncio`, decidido no `<head>` antes de pintar (`html.anuncio`):

- "Sites para restaurantes" · "Um site assim para o teu restaurante." · "Fazemos o teu site e mostramos-to antes de pagares. Sem compromisso." · botão WhatsApp com a mensagem já escrita ("Vi o anúncio…"). Em romeno o mesmo. O cabeçalho de sempre e o lema ficam escondidos; o resto da página é igual.
- Em destaque: o terceiro quadrado passa a Grupo Naval (restaurante) em vez da Toda Chic.
- Sem intro (os carros).
- GoatCounter: `anuncio/chegada` ao carregar e `anuncio/whatsapp` / `anuncio/telefone` ao sair. Taxa de contacto do anúncio = `anuncio/whatsapp` ÷ `anuncio/chegada`. O pixel da Meta continua a enviar `Contact` (só em PT; a página romena não tem pixel).

## 2. Aviso de cookies compacto

Faixa colada ao fundo no telemóvel (127 px em vez de um cartão que tapava um terço do ecrã). No computador fica como estava.

## 3. Separadores com mais ar (computador)

A partir de 48rem: 2,25rem entre separadores, sublinhado só na largura do texto, barra a 3,5rem (`--tabs`, de que dependem os `scroll-margin`). No telemóvel ficam como estavam: os três têm de caber.

## 4. Lema (PT, RO, EN)

No topo das vistas Automações e Sites: três frases, com a do meio em laranja e na fonte display (o destaque), e um traço laranja que se desenha ao carregar (respeita `prefers-reduced-motion`):

- PT: Tens um objetivo a atingir? / **A IA vai fazê-lo acontecer.** / Só tens de dar o primeiro passo.
- RO: Ai un obiectiv de atins? / **AI-ul îl va face să se întâmple.** / Trebuie doar să faci primul pas.
- EN: Do you have a goal to reach? / **AI will make it happen.** / You just have to take the first step.

Em português, "fazê-lo" não se parte no hífen (`span.nb`). Escondido a quem chega por anúncio (aí fala o herói).

## 5. Ponte para as automações (PT, RO, EN)

Entre os tipos de negócio e "Mais sites que fizemos": cartão com "E depois do site", a frase "O site traz clientes. As automações mantêm-nos.", as quatro automações mais concretas em texto, o botão "Ver as automações" (abre `#automatizari`) e as duas bolhas de chat do rececionista, que entram uma a seguir à outra ao fazer scroll. Reutiliza as classes `.chat/.msg` que já existiam.

## Publicar

1. Netlify → site pachecost → Deploys → arrastar `pachecost-deploy-foco-ia.zip` (entregue no chat; é a pasta `novo/`).
2. Testar no telemóvel: `pachecost.com` (automações), `pachecost.com/?origem=anuncio` (herói dos sites), `pachecost.com/?origem=anuncio#automatizari` (automações), `ro.pachecost.com` e `ro.pachecost.com/C`.
3. **Passar as alterações para o gerador** (`gerar.py` / `marca/dados.json`). Sem isto, o próximo `gerar.py` apaga tudo.

## Repetir noutro deploy

```bash
# cur/ = deploy exportado do Netlify (Deploys → … → Download), descomprimido
python3 aplicar.py        # escreve novo/; pára se o HTML do gerador tiver mudado
```
