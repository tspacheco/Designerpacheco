# Reel EN 5 · «You ask AI one question. This is what's underneath.» (08/10/2026)

Reel orgânico em inglês para @pachecostudiospt, pedido do Tomás (08/10): 5 curiosidades sobre a infraestrutura de uma empresa com IA, plano 3D feito no Higgsfield, gancho nos 3 primeiros segundos com uma figura humana figurativa em 3D, fundo em abismo que desce cada vez mais fundo, ritmo rápido, no máximo 15 s. Pensado com o Fable.

- `reel-en-5-under-one-question-9x16.mp4`: 15 s, 1080×1920, H.264/AAC, moov no início (MP4 normal, não fragmentado: a Meta carrega).
- `reel-en-5-under-one-question-capa.jpg`: capa para escolher no Instagram.
- Língua: inglês, como os reels anteriores da série (trocar para PT ou RO é só mudar o objeto `FACTS` e o gancho em `overlay.html`).

## Ângulo e identidade

Ângulo novo na série: **a vertical**. Em vez de 3 sistemas em coluna, conclusão + raio-X ou antes/depois, este abre com um resultado («You ask AI one question. This is what's underneath.») e **desce** por 5 camadas, cada uma mais funda e mais estranha: a pergunta → a máquina → a energia → o planeta → o fundo do mar. A ordem é a própria descida.

- Vídeo de fundo: clip 3D do Higgsfield (Kling 3.0 pro, 9:16, prompt em `prompts.md`): figura humana lisa, sem rosto, branca-barro, à beira de um poço circular com um telemóvel na mão; a câmara passa-lhe pelo ombro e mergulha pelas camadas (racks de servidores, cabos, torres de arrefecimento, grelha de cidade, fundo do oceano).
- Texto: Dela Gothic One (números monumentais, nova na série) + JetBrains Mono (etiquetas e fontes). Osso `#EFEAE3` e laranja Pacheco `#E8622C` sobre o abismo. Tudo entra a cair de cima e sai a cair para baixo, com um contador de profundidade a acelerar à direita e uma régua de ticks a subir à esquerda.
- Som: sintetizado em numpy (`som.py`, sem direitos de terceiros): drone grave que desce uma oitava ao longo da queda, vento que abre com a profundidade, impacto no gancho, baque + ping de sonar cada vez mais grave em cada camada, acorde de chegada no fecho. O ambiente gerado pelo Kling vai misturado em fundo.
- Linha do tempo (15 s): gancho 0–3 · camadas a 3, 5, 7, 9 e 11 (2 s cada) · fecho 13–15 com pachecost.com + «Portugal based · Acting worldwide».

## As 5 curiosidades e as fontes (factos reais, verificados a 08/10/2026)

| # | No ecrã | Facto | Fonte |
|---|---|---|---|
| 1 | **0.34 Wh** · One ChatGPT question. A light bulb for ~2 min. | Sam Altman escreveu que uma pergunta média ao ChatGPT gasta cerca de 0,34 Wh («o que um forno usa em pouco mais de um segundo, ou uma lâmpada eficiente em dois minutos») e cerca de 0,000085 galões de água (≈ 0,32 ml). É um número da própria empresa, sem metodologia publicada; por isso o ecrã diz «company figure». | Sam Altman, «The Gentle Singularity», blog.samaltman.com, 10/06/2025 |
| 2 | **100,000 GPUs** · One training cluster. Built in 122 days. | O cluster Colossus da xAI em Memphis entrou em funcionamento com 100 000 GPUs Nvidia H100 refrigeradas a líquido, montado em 122 dias (anúncio da xAI/Elon Musk em 02/09/2024, confirmado pela Nvidia como o maior supercomputador de GPUs do mundo). Depois duplicou para 200 000. | Publicação de Elon Musk em X (02/09/2024); Nvidia Data Center em X; cobertura em techstartups.com e tomshardware.com |
| 3 | **A nuclear plant** · Three Mile Island, restarting. 20-year deal to feed data centres. | A Constellation vai reabrir a Unidade 1 de Three Mile Island (≈ 835 MW, fechada em 2019 por razões económicas) com um contrato de compra de energia de 20 anos com a Microsoft para alimentar os seus centros de dados; investimento de 1,6 mil milhões de dólares, arranque previsto para 2027–2028, sujeito à NRC. | Comunicado da Constellation Energy, 20/09/2024; World Nuclear News, «Constellation to restart Three Mile Island unit, powering Microsoft» |
| 4 | **1.5%** · of the world's electricity went to data centres in 2024. Doubling by 2030. | A Agência Internacional de Energia estima que os centros de dados consumiram cerca de 415 TWh em 2024 (≈ 1,5 % da eletricidade mundial) e projeta cerca de 945 TWh em 2030 (mais do dobro, mais do que o Japão inteiro consome hoje). | IEA, relatório «Energy and AI», abril de 2025 (iea.org/reports/energy-and-ai) |
| 5 | **864 servers** · 2 years under the sea, 36 m down. 1/8 the failures of land. | Project Natick da Microsoft: um cilindro com 12 racks e 864 servidores ficou 2 anos (2018–2020) no fundo do mar ao largo das Órcades, a 117 pés (≈ 36 m) de profundidade, e teve uma taxa de avarias de 1/8 da do grupo de controlo em terra (atmosfera de azoto seco, sem pessoas). | Microsoft, «Microsoft finds underwater datacenters are reliable, practical and use energy sustainably», news.microsoft.com, 14/09/2020 |

Nada é resultado nosso; são factos públicos de terceiros, cada um com a fonte no ecrã em letra pequena e aqui.

## Gerar de novo

`node render.cjs /tmp/reel-abyss base.mp4` (Playwright, ffmpeg, numpy). `base.mp4` é o clip do Higgsfield (ver `prompts.md`; a transferência faz-se pela PONTE, `.github/ponte.txt`). Textos e tempos em `overlay.html`; som em `som.py` (lê `window.SFX` da página).

## Legenda com foco em alcance (versão final, 08/10/2026 19:50)

Decisão (pedido do Tomás: alcance): **legenda curta, com 4 hashtags**. Razões, verificadas a 08/10/2026:
- O alcance de um reel vem do tempo de visualização e, sobretudo, dos **envios por DM** (sends per reach): é o sinal que leva o reel a quem não nos segue (Mosseri, jan. 2025; cobertura em socialmediatoday.com, eclincher.com). A legenda deve pedir o envio, não o comentário.
- As hashtags **não aumentam o alcance** («don't increase your reach», Mosseri, maio 2025) e o Instagram limita a **5 por publicação** desde dez. 2025; servem só para catalogar. Usar 3 a 4 específicas não prejudica e ajuda a pesquisa; mais do que isso é ruído.
- A pesquisa do Instagram lê a legenda e o texto no ecrã: as **palavras-chave vão na 1.ª linha** (os primeiros ~125 caracteres aparecem antes do «mais»).
- Comprida ou curta: a 1.ª linha decide; o resto só é lido por quem já parou. Fica curta, com as fontes em 5 linhas porque o ecrã final diz «Sources in the caption».

**Legenda (copiar):**

Inside the AI infrastructure behind one ChatGPT question: 5 facts, 15 seconds. ⬇️

Send this to the friend who thinks AI lives in the cloud.

−1 One question ≈ 0.34 Wh (OpenAI's own figure, 2025)
−2 100,000 GPUs in one cluster, built in 122 days (xAI, 2024)
−3 A nuclear plant restarted to feed data centres (Constellation + Microsoft, 2024)
−4 1.5% of the world's electricity, doubling by 2030 (IEA, 2025)
−5 864 servers, 2 years on the seabed, 1/8 the failures (Microsoft, 2020)

Your business doesn't need any of this to use AI well. It needs the right system. pachecost.com

#AIinfrastructure #datacenter #artificialintelligence #techfacts

**Palavras de atração (3 a 4, para a 1.ª linha, o texto no ecrã ou o Instagram sem hashtags):** AI infrastructure · data centre · ChatGPT · nuclear

Versão ultracurta (se quiseres testar sem fontes na legenda; nesse caso tira «Sources in the caption» do ecrã final em `overlay.html`):
«What's under one ChatGPT question? 5 facts, 15 s. Send it to someone who uses AI every day. pachecost.com #AIinfrastructure #datacenter #techfacts»

## Legenda anterior (primeira versão, para registo)


You ask AI one question. Here's what's underneath it. 👇

−1 One ChatGPT question ≈ 0.34 Wh. A light bulb for two minutes. (OpenAI's own figure, June 2025)
−2 One training cluster: 100,000 GPUs. Built in 122 days. (xAI Colossus, Memphis, Sept 2024)
−3 A nuclear plant is being restarted to feed data centres. Three Mile Island, 20-year deal with Microsoft. (Constellation, Sept 2024)
−4 Data centres took 1.5% of the world's electricity in 2024. Set to double by 2030. (IEA, Energy and AI, 2025)
−5 Microsoft kept 864 servers on the seabed for 2 years. One eighth of the failures of land. (Project Natick, 2020)

None of this is magic. It's infrastructure. And a small business doesn't need any of it to use AI well: it needs the right system, drawn in front of you.

Free diagnosis: pachecost.com
Portugal based · Acting worldwide

#AIforbusiness #datacenter #smallbusiness #artificialintelligence #techfacts
