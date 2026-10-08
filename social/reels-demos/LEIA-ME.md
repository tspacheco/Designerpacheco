# Agente 4 · Um reel por demo, publicado só com o «sim» do dono

Cada demo de pachecost.com/demo/<slug>/ dá um reel 9:16 com som. O reel só é publicado depois de o dono dizer que sim, e sai como **Colaboração** no Instagram: aparece no @pachecostudiospt e no perfil do negócio ao mesmo tempo.

## Porque é que o dono aceita (o que ganha)

- **Um vídeo profissional do negócio dele, grátis**, para pôr no Instagram, Facebook ou TikTok. Barbearias, padarias e salões precisam de conteúdo todas as semanas e raramente têm quem o faça.
- **Alcance novo**: a Colaboração mostra o vídeo aos seguidores dele e aos nossos.
- **A nota Google em destaque**: o reel abre com «4,9★ pe Google · 82 de recenzii». É um elogio real, não publicidade nossa.
- **Vê o site em movimento, sem pressão**: não paga nada, não se compromete e pode pedir para tirar quando quiser.

## O que ganhamos nós

- **Um reel por demo, sem trabalho manual**: conteúdo diário para o Instagram, com um negócio real em cada um.
- **Um 2.º contacto que é um presente**, em vez de «então, viu o site?». Reciprocidade: quem recebe algo útil responde mais.
- **O «sim» é um sinal de interesse**: quem aceita passa a lead quente, com a visita de 20 minutos marcada na resposta.
- **Prova social local**: o reel entra no feed dos clientes dele e dos donos vizinhos, que veem que fazemos sites para negócios da rua deles.
- **Autorização escrita** para usar o nome, as fotos e a marca do negócio. Sem ela não se publica.

## Processo

1. **Quando enviar**: não na 1.ª mensagem (a da demo). Vai como 2.º contacto, **2 a 3 dias depois**, a quem não respondeu ou respondeu sem fechar. Se o tracker mostrar que a demo foi aberta, esses vão primeiro. Quem disse «não tenho interesse» não recebe.
2. **Gerar**: juntar uma linha ao `reels.json` (nota e avaliações só confirmadas na ficha Google; sem nota → `null`) e correr `python3 gerar_reel.py <slug>`. Sai em `saida/<slug>/`: vídeo, capa e `legenda.md` com as 3 mensagens (pedido, resposta ao «sim», legenda), na língua do dono e em PT.
3. **Enviar**: WhatsApp Business do Tomás (RO para Iași, PT para o Algarve), com a mensagem 1 e o vídeo anexado. Sem WhatsApp comprovado: mostra-se no telemóvel na visita, ou SMS com o link do vídeo.
4. **Resposta**:
   - **SIM** → mensagem 2; publicar o Reel com a legenda 3 e, antes de publicar, *Marcar pessoas → Convidar colaborador → @negócio*. O dono carrega em «Aceitar» e o vídeo aparece nos dois perfis. Se o negócio não tiver Instagram, publica-se com a localização e o nome na legenda.
   - **Pede alterações** → corrige-se a demo (thread das demos) e gera-se outra vez.
   - **NÃO ou sem resposta** → não se publica. Nunca.
   - Para usar o vídeo em **anúncios pagos** é preciso um 2.º «sim», à parte.
5. **Registo**: `estado` no `reels.json` (gerado → pedido → sim/não → publicado), que alimenta o tracker de estatísticas (aberturas, respostas, sem interesse).

## Como é o reel (10 compassos, a música manda no corte)

| Tempo | Faixa de cima | Por baixo |
|---|---|---|
| 2 compassos | **Gancho já no 1.º fotograma**: «4,9★ pe Google» → «82 de recenzii. Niciun site.» → «Așa ar arăta.» | herói da demo a fazer a entrada |
| 7 compassos | Nome do negócio, morada, «Site creat de Pacheco Studios» | o site desce uma secção por compasso, em cima do tempo forte |
| 1 compasso | «Ai o afacere? Meriți un site ca acesta.» | rodapé da demo |
| 3 s | ecrã final ro.pachecost.com / pachecost.com + «Portugal based · Acting worldwide» | |

- Abre com um resultado (a nota Google), não com uma história. Frase honesta: «Așa ar arăta» / «Seria assim», porque é uma demonstração.
- **Identidade própria por reel, automática**: a fonte de título, a cor de destaque e o fundo vêm da própria demo, e cada demo já tem assinatura e fonte únicas (PLAYBOOK §5 e §6).
- Música sintetizada (`som-demos.py`, sem direitos de terceiros): `urbano` (barbearias, tatuagens, oficinas), `quente` (padarias, cafés, flores, beleza, roupa) e `energia` (auto, lavandarias, bicicletas). O slug muda o tom e a melodia.
- Línguas: `ro`, `pt`, `en`.

## Ficheiros

- `gerar_reel.py`: tira a demo do ramo das demos (só lê, não escreve lá), grava-a, junta texto e música, faz o MP4, a capa e a `legenda.md`.
- `captar.py`: grava a demo como num telemóvel (432×580 CSS a 2,5×), com o relógio da página e as animações CSS controladas fotograma a fotograma; scroll de secção em secção.
- `titulos.html`: texto por cima (faixa de 470 px no topo).
- `som-demos.py`: música.
- `reels.json`: dados de cada reel. `textos.json`: mensagens e legendas.

Requisitos: Playwright (Chromium em /opt/pw-browsers), ffmpeg e numpy. Uma demo demora cerca de 8 minutos a gerar.
