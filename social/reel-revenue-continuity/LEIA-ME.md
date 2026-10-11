# Reel EN · «Revenue leaks after the yes» (11/10/2026)

Reformulação do reel «Revenue Continuity» que o Tomás montou (fundo 3D do Higgsfield: personagem escura com a esfera laranja do cliente e ícones em órbita). Pedido (11/10): aproveitar só o vídeo de fundo e tornar o texto coerente e útil, com o texto a acertar com o movimento de cada plano.

- `reel-en-revenue-leaks-9x16.mp4`: 35 s, 1080×1920, H.264/AAC, moov no início. Som sintetizado (publicar com som).
- `reel-en-revenue-leaks-capa.jpg`: capa para escolher no Instagram.
- `Pacheco-Studios-Revenue-Continuity-Reel.mp4`: o vídeo original composto (upload do Tomás). O clip limpo não estava em nenhuma conta do Higgsfield ligada ao projeto; o fundo limpo foi recuperado deste ficheiro com `limpar.py`.

## O que mudou e porquê

O vídeo original tinha 8 cartões de texto que mudavam a meio dos planos, tapavam a cara da personagem (cartões a ~90 % de opacidade sobre y 180–690 e 1110–1310) e falavam de coisas que não se viam («context must travel»). O clip tem **7 planos de 5 s** (cortes a 5,1 · 9,9 · 15,0 · 20,1 · 24,9 · 30,0), em ritmo de 3: esfera em grande plano com recuo de câmara (0, 15, 30) · personagem aberta (5, 20) · personagem média/grande (10, 25). A versão nova segue esse ritmo:

| Plano | O que se vê | Texto |
|---|---|---|
| 0–5 | mão com a esfera do cliente, câmara recua | **Revenue leaks after the yes.** Five leaks. One owner and one rule for each. (o título «assenta» com o recuo da câmara) |
| 5–10 | personagem de corpo inteiro com a esfera ao peito, ícones em órbita | Leak 01 · the no-show — **No reminder, no show.** Rule: every booking gets a reminder and a named owner. Cadeia: Booking → Reminder → Confirmed |
| 10–15 | plano médio, aponta aos ícones | Leak 02 · feedback — **Praise and complaints need different doors.** Rule: praise goes public, complaints go to a person. Today. Review → Route → Reply |
| 15–20 | esfera outra vez (o cliente), recuo de câmara | Leak 03 · the quiet customer — **Silence is a signal.** Rule: 60 days without a visit triggers one message with one offer. |
| 20–25 | personagem apresenta a esfera na palma | Leak 04 · the day — **See the day before it runs you.** Rule: one screen, every morning, before the first client. Bookings · Exceptions · Unanswered |
| 25–30 | grande plano, cabeça ocupa o topo | Leak 05 · the paperwork — **Receipts at midnight.** (bloco centrado sobre o peito, o único sítio livre) Rule: capture, check and send. Same day. Receipt → Check → Accountant |
| 30–32,5 | esfera, recuo de câmara | The method — **One event. One owner. One next action.** Trigger · Owner · Rule · Handoff |
| 32,5–35 | a mão entrega a esfera | **DM “audit”** — We map where your leads, decisions and delivery break. Before you buy another tool. pachecost.com · Portugal based · Acting worldwide |

Cada bloco entra no corte (sobe + aparece em 0,3 s) e sai 0,25 s antes do corte seguinte; os nós das cadeias acendem um a um (0,45 s) com um ping no som. Zona segura do Instagram respeitada (texto entre y 250 e ~1580). Sem números inventados: «60 days» é a regra, não uma estatística. Segue o playbook de consultoria (11/10): fuga operacional, dono + regra + handoff para uma pessoa, CTA «DM audit»; nada de venda de sites nem «automatizamos o teu negócio».

Identidade (nova na série): Chakra Petch Bold (título, quadrada e técnica como os ícones 3D) + IBM Plex Mono (etiquetas e cadeias), osso `#F1ECE4` e laranja `#F07A3A`, gradiente escuro no topo para legibilidade. Som (`som.py`, numpy, sem direitos de terceiros): pad em Ré, pulso a 100 BPM, whoosh + baque em cada corte, ping em cada bloco, três pings a subir nas cadeias, acorde de chegada no fecho.

## Gerar de novo

1. `python3 limpar.py Pacheco-Studios-Revenue-Continuity-Reel.mp4 clean.mp4` (OpenCV; ~15 min): desfaz a tinta dos dois cartões (ajuste por fotograma nas arestas), apaga texto, rebordos, linha de progresso e rótulos com inpainting, e recolore a zona recuperada com uma tabela luma→croma aprendida no resto do fotograma.
2. `node render.cjs /tmp/reel-rc clean.mp4` (Playwright + ffmpeg + numpy, ~5 min). Textos e tempos em `overlay.html`; som em `som.py`. Pré-visualizar fotogramas: `node render.cjs /tmp/reel-rc clean.mp4 frames 0.4,5.6,10.6`.

Limitação: a zona dos cartões antigos foi recuperada de ~10 % de sinal; nas zonas claras (esfera, mão) nota-se uma faixa mais suave e menos saturada. O gradiente do topo e o bloco centrado do plano 25–30 tapam a maior parte. Se o clip limpo do Higgsfield aparecer, basta substituir `clean.mp4` e correr o passo 2.

## Legenda (Instagram, EN)

Revenue leaks after the yes: 5 leaks in a service business and the rule that closes each one.

No-shows, feedback with no route, quiet customers, a day that runs you, receipts at midnight. One event, one owner, one next action.

DM “audit” and we map where your leads, decisions and delivery break, before you buy another tool. pachecost.com

#aiconsulting #smallbusinessowner #salonowner #restaurantowner #operations
