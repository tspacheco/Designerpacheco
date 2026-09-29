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
- Os vídeos antigos da Pacheco Studios no Instagram só têm música (sem fala); não entram neste vídeo.

## Produção (Higgsfield)

- Imagens-chave: gpt_image_2_5 (medium), dono consistente via referência.
- Clips: Kling 3.0 std, 4 s, som off (6 créditos cada, 5 clips).
- Overlays: HTML → PNG (Playwright), Manrope, diacríticos RO.
- Montagem e som: ffmpeg + sox na sandbox; scripts em `research/video-automatizare-ro/`.
