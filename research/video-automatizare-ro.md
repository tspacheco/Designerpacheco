# Vídeo 3 — Automação WhatsApp (Roménia, 100 % gerado)

Anúncio Meta · 9:16 · 26,4 s · RO · sem voz (lê-se sem som) · SFX (vibração, notificações, ding).
Objetivo: o dono de restaurante reconhece-se → vê o problema acontecer → vê a solução → preço → escreve-nos com a automação que quer.

## Guião

| Tempo | Imagem (Kling 3.0, i2v) | Texto no ecrã (RO) | O que faz |
|---|---|---|---|
| 0–3,2 s | Telemóvel a vibrar no balcão, notificações a acumular, cozinha em serviço ao fundo | «Clientul ți-a scris la 21:40.» → «Tu ai văzut la 23:10.» | **Gancho.** O dono reconhece-se nos primeiros 3 s |
| 3,2–6,8 s | Dono (~40, barba, avental preto) com 3 pratos, olha para o bolso a vibrar, não consegue atender | «Nu pentru că nu-ți pasă.» → «Aveai mâinile pline.» | Reconhecimento sem culpa |
| 6,8–9,6 s | Cliente no sofá, à espera, impaciente | «Între timp… a rezervat în altă parte.» | **O problema acontece** |
| 9,6–15,6 s | Chat WhatsApp (UI desenhada, texto exato) sobre fundo desfocado | Mensagem 21:40 → «scrie…» → resposta com reserva → «Andrei» → confirmação. Rótulo: «Răspuns în câteva secunde. Chiar și la 21:40.» | **A solução** |
| 15,6–19,2 s | Mesmo dono, calmo, sorri para o telemóvel, sala cheia | «Tu te ocupi de oamenii din sală.» → «Sistemul răspunde la mesaje.» | Benefício emocional |
| 19,2–22,4 s | Plano geral, sala cheia, dono recebe grupo de 4 | ✓ Răspunde în câteva secunde, zi și noapte · ✓ Face rezervarea direct în WhatsApp · ✓ Trimite reminder → mai puține mese goale | Resultados × benefício |
| 22,4–26,4 s | Fundo desfocado + cartão | «Asistent WhatsApp făcut pe măsura afacerii tale · de la 6.000 lei + 1.000 lei/lună · Preț corect. Fără costuri ascunse.» Botão: «Scrie-ne ce automatizare vrei →» · PACHECO STUDIOS | Preço + CTA |

## Anúncio (texto Meta, RO)

> Clientul ți-a scris la 21:40. Tu ai văzut la 23:10 — și masa a plecat la altcineva.
>
> Facem asistentul tău de WhatsApp: răspunde în câteva secunde, face rezervarea și trimite reminder. Tu rămâi cu oamenii din sală.
>
> Sistem făcut pe măsura afacerii tale — de la 6.000 lei + 1.000 lei/lună.
> Scrie-ne ce automatizare îți trebuie și îți spunem cum ar arăta la tine.

Título: «Nu mai pierde rezervări pe WhatsApp» · Botão: **Trimite mesaj** (objetivo Mensagens → WhatsApp).

## Notas de honestidade

- «Cele mai bune prețuri de pe piață» ficou de fora: é superlativo sem prova (lei 158/2008 e revisão da Meta podem travar). Usado: «Preț corect. Fără costuri ascunse.» — só manter se o orçamento for mesmo fechado (6.000 + 1.000/mês, sem extras).
- «Câteva secunde» e «zi și noapte» são promessas do sistema — garantir no produto (n8n + WhatsApp Cloud API).
- Sem números de resultados, sem testemunhos, sem logótipos de terceiros. O restaurante e as pessoas são gerados por IA (não é um cliente real) — não dizer «clientul nostru».
- Vídeos antigos da Pacheco Studios (biblioteca Higgsfield): o áudio é só música, sem fala; a análise visual ainda estava em fila, por isso não foram usados excertos.

## Produção (Higgsfield)

- Imagens-chave: gpt_image_2_5 (medium), dono consistente via referência.
- Clips: Kling 3.0 std, 4 s, som off (6 créditos cada, 5 clips).
- Overlays: HTML → PNG (Playwright), Manrope, diacríticos RO.
- Montagem e som: ffmpeg + sox na sandbox; scripts em `research/video-automatizare-ro/`.

## Plano dos 3 vídeos — versão Roménia

| # | Vídeo | Gancho (RO) | Destino |
|---|---|---|---|
| 1 | Recriação do site do Bolta Rece (Iași) | «Am refăcut site-ul celui mai cunoscut restaurant din Iași.» | Perfil / site |
| 2 | Trabalho da Pacheco Studios (demo real) | «Afacerea ta merită un site de acest nivel.» | Site |
| 3 | Automação WhatsApp (este) | «Clientul ți-a scris la 21:40. Tu ai văzut la 23:10.» | WhatsApp (Mensagens) |

- **Público:** Roménia inteira, «vive em»; 30–65+; interesses de donos (restauração, pequenas empresas, Facebook Page admins). Começar com as 5 cidades grandes (București, Cluj, Iași, Timișoara, Brașov) se o CPM subir.
- **Idioma:** tudo em romeno (texto no ecrã + texto do anúncio). Resposta no WhatsApp também em RO (ou EN).
- **Orçamento:** mantém-se a regra dos 14 dias — 1 campanha, 3 anúncios; o vídeo 3 vai para uma campanha de Mensagens (WhatsApp) à parte, porque o objetivo é conversa, não visita ao site.
- **Vídeo 1 — cuidado:** usar o nome e as fotos do Bolta Rece num anúncio pago precisa de autorização escrita. Sem ela: legenda fixa «Concept neoficial · Pacheco Studios», sem logótipo deles, só imagens nossas/geradas, e nunca sugerir que são clientes.
- **Frase «cele mai bune prețuri»:** trocada por «Preț corect. Fără costuri ascunse.» (superlativo sem prova).
