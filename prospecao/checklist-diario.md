# CHECKLIST DIÁRIO MÍNIMO — APPROACH

> Rotina de terreno da Pacheco Studios. Serve em Portugal e na Roménia (script romeno em `research/romenia.md`).
> Regra única: **nunca um dia a zero.** O "mínimo" é o chão; o "dia 10X" é o alvo (porquê em `research/metodo-10x-cardone.md`).
> Faz-se sozinho, sem Claude, com o telemóvel. O Claude entra só à noite (demos em lote) e ao domingo (métricas).

## 0. Versão de bolso (copiar para as notas do telemóvel)

| | Mínimo | Dia 10X |
|---|---|---|
| Portas abertas | 10 | 25 |
| Conversas com o dono (ou nome + hora em que está) | 4 | 10 |
| Demos mostradas no telemóvel | 2 | 6 |
| Cartões deixados | 10 | 25 |
| Packs QR entregues (vendidos ou oferecidos) | 2 | 5 |
| Follow-ups (WhatsApp / chamada / 2.ª visita) | 5 | 15 |
| Reuniões marcadas **com dia e hora** | 1 | 3 |
| Tracker preenchido antes de fechar o dia | sim | sim |
| Metas escritas de manhã **e** à noite | sim | sim |

Tempo: ~3 h/dia (2 h de rua + 30 min de follow-up + 20 min de preparação/fecho). Dia 10X = tarde inteira + manhã.

## 1. Preparação (10 min — na véspera à noite ou de manhã)

- [ ] **Uma rua, não uma cidade.** Escolher 1 rua/bairro com ≥10 negócios da Lista A (sem site, ≥4,2★, dezenas/centenas de avaliações). Marcar os 10 no mapa por ordem de percurso — zero tempo a andar.
- [ ] **Demos no telemóvel**, uma por separador, **testadas em modo avião** (são ficheiro único — têm de abrir sem rede). Brilho no máximo. Bateria > 80 % + powerbank.
- [ ] **Kit:** 30 cartões pessoais · folha de **cartões-demo do dia** (10 por A4, um por negócio — `prospecao/qr/gerar_qr.py`) · 5 packs QR de mesa "Avalie-nos no Google" · 10 autocolantes QR · caneta e bloco · MB WAY pronto para receber.
- [ ] **Janela certa por tipo de negócio:** cafés/padarias 7h30–9h ou 15h–16h30 · restaurantes 15h–18h (fora do serviço) · cabeleireiros 2.ª/3.ª feira · clínicas a meio da tarde. Não entrar em serviço — só se for para deixar cartão.
- [ ] **Escrever à mão** as metas do dia (os números da tabela de cima) e a meta grande (secção 4). É o gesto Cardone: escrever de manhã e à noite.

## 2. Na rua (2 h) — sequência de 3 minutos por porta

1. **Entrar com o telemóvel na mão, demo já aberta.** Olhar para quem manda, não para quem está mais perto.
2. **Abertura (10 s):** "Boa tarde, chamo-me Tomás, faço sites para restaurantes aqui na zona. O dono está?"
3. **Dono está (30 s):** "Vocês têm 4,6 estrelas e 300 avaliações no Google e não têm site — fora do Maps estão invisíveis. Fiz-vos uma demonstração. Posso mostrar? São 40 segundos." → mostrar → **não vender à porta**: pedir 10 minutos noutro dia (ou agora, se ele puxar). Fechar com dia e hora: "Terça às 16h?"
4. **Dono não está:** nome do dono + a que horas costuma estar → deixar o **cartão-demo** ("diga-lhe que o site dele já existe — é só ler o código") → oferecer o autocolante QR das avaliações → marcar 2.ª visita à hora dita.
5. **Pack QR (a ponte para a reunião):** "Independentemente do site: isto é um pack de mesa com QR para as avaliações do Google — o cliente lê, deixa 5 estrelas, e vocês sobem no Maps. 39 €, entrego na terça já plastificado e mostro-vos o site em 10 minutos." → vendeu = reunião marcada com data. Não vendeu = deixar o autocolante grátis e voltar na mesma.
6. **Objeção** → resposta de uma frase (secção 5) → deixar sempre algo → sair. Máximo 3 minutos, salvo se o dono prolongar.
7. **Registar no tracker antes da próxima porta** (30 s): `prospecao/tracker.csv`, uma linha por contacto.
8. **Não sair da rua antes das 10 portas.** Medo de entrar = entrar já. É o único sinal fiável de que é a porta certa.

Regras que não se quebram: nunca discutir · um só pedido por visita (a reunião) · nunca prometer o que o engine não faz · dados do negócio só os do Google/ementa (HONEST-DATA) · nunca falar mal do site que já têm — "elevar, não substituir".

## 3. Follow-up (30 min — ao fim do dia ou às 9h30 do dia seguinte)

- [ ] `python3 prospecao/stats.py --hoje` → lista dos próximos passos vencidos e de hoje.
- [ ] 5 mensagens WhatsApp a contactos de ontem/anteontem: nome do dono + link da demo + uma frase. Enviar **até 2 h depois** de obter o número.
- [ ] 2 chamadas/2.ªs visitas a "o dono está às X".
- [ ] Confirmar por mensagem as reuniões de amanhã (dia, hora, "levo o pack").
- [ ] Responder a tudo o que entrou hoje (WhatsApp, Instagram, e-mail).

**Cadência por contacto (o dinheiro está no follow-up — a maioria desiste ao 1.º):**

| Quando | O quê |
|---|---|
| D0 | Visita + cartão-demo (+ autocolante QR) |
| D0 + 2 h | WhatsApp com o link da demo, se houver número |
| D+2 | 2.ª visita à hora em que o dono está |
| D+4 | Mensagem curta com prova (site de outro cliente, print do Maps) |
| D+7 | Chamada |
| D+14 | Última mensagem: "fico por aqui; a demo fica guardada 30 dias" |
| D+60 | Novo contacto com uma novidade (época nova, ementa nova, pack QR) |

Mínimo **5 contactos** antes de marcar `nao` no tracker.

## 4. Fecho do dia (10 min)

- [ ] Tracker completo: portas, donos, demos, cartões, packs, reuniões. Nada fica na cabeça.
- [ ] Amanhã já decidido: rua, 10 negócios, hora de saída.
- [ ] Demos em falta → **um só pedido ao Claude, em lote** (5–6 sites por chat, secção 12 do playbook). Nunca uma a uma.
- [ ] Escrever as metas outra vez (as do dia e a grande). Uma frase: o que funcionou / o que mudo amanhã.

**Meta grande (escrever todos os dias):** *"N clientes em mensalidade até DD/MM/AAAA."* Meta normal × 10 = meta 10X. Nunca baixar a meta — subir a ação.

## 5. Objeções — uma frase cada

| Ouves | Respondes |
|---|---|
| "Já temos Facebook/Instagram." | "Ótimo, fica. O site é para quem vos procura no Google e para os turistas — e é para onde o Facebook manda quando alguém quer reservar." |
| "Não preciso, a casa está sempre cheia." | "Então a mensalidade paga-se com uma mesa por mês. E o pack de avaliações mantém-vos cheios quando a época baixar." |
| "Quanto custa?" | Preço direto (500 € · 500 € + 50 €/mês · grupo 400 € + 40 €/mês) e voltar à demo: "veja primeiro se vale isso." |
| "É caro." | "É menos do que uma mesa de 6 por mês, durante um ano. E o site fica vosso, sem custos escondidos." |
| "Manda-me por WhatsApp." | "Claro — qual é o número?" (o número é a vitória; enviar em menos de 2 h) |
| "O meu sobrinho faz isso." | "Perfeito, então já sabe que dá trabalho. Deixo a demo; se quiserem, eu faço e o sobrinho mantém." |
| "Agora não posso." | "Claro. A que horas está mais calmo? Volto às 16h, 10 minutos." |
| "Já temos site." | Ver o site à frente dele: 3 falhas concretas (telemóvel, velocidade, sem reservas/WhatsApp) → "elevar, não substituir". |
| "Não" seco. | "Obrigado pelo tempo. Deixo só o autocolante das avaliações — é grátis. Se vos trouxer estrelas, falamos." |

## 6. Os QR como produto de entrada

O QR não é o negócio — é a **razão para voltar com hora marcada**. Ordem de venda:

| Produto | O que é | Preço PT (sugestão) | Serve para |
|---|---|---|---|
| **Autocolante "Avalie-nos no Google"** | 1 autocolante de porta/balcão com QR direto para o formulário de avaliação | Grátis | Ficar na porta do negócio. Razão para a 2.ª visita ("subiram as avaliações?"). |
| **Pack de mesa "5 estrelas"** | 5 cavaletes A6 plastificados + 1 autocolante + 1 cartão de balcão | 39 € (custo ~6–8 € de impressão) | Primeiro "sim" pago. A entrega **é** a reunião. |
| **Pack mesa completo** | Avaliações + Wi-Fi (liga sozinho) + WhatsApp reservas + Instagram | 59 € | Negócios com esplanada/turistas. |
| **QR Ementa / Reservas** | Aponta para a secção da ementa e para o WhatsApp do site | Incluído no site | Argumento de venda do site: "a ementa em QR vem incluída". |
| **Cartão-demo** | Cartão 85×55 com o nome do negócio e QR para a demo dele | Custo nosso | Deixar quando o dono não está. |

Todos gerados por `prospecao/qr/gerar_qr.py` (SVG + PDF A4 pronto para a copiadora). Link das avaliações: `https://search.google.com/local/writereview?placeid=<PLACE_ID>` (Place ID Finder da Google — funciona sem ser dono). Testar cada QR com 2 telemóveis antes de imprimir. QR com ≥ 3 cm nos cavaletes, ≥ 2 cm nos cartões, correção de erro H.

Preços em lei para a Roménia: `research/romenia.md`, secção 4 (a confirmar no terreno).

## 7. Revisão semanal (domingo, 1 h)

- [ ] `python3 prospecao/stats.py` → totais, funil e taxas (portas → donos → demos → reuniões → propostas → vendas). Registar as taxas no playbook, secção 11 (pendente antigo: "taxas de fecho por tipo de negócio").
- [ ] Onde caiu o funil? Poucos donos → mudar a hora. Poucas demos → demos mais fortes ou abertura mais curta. Poucas reuniões → pedir a reunião mais cedo e com hora. Poucas vendas → rever a proposta, não o preço.
- [ ] Zona da próxima semana escolhida + 30 negócios pesquisados (Lista A / Lista B).
- [ ] Demos da semana pedidas em lote. Cartões-demo impressos. Packs QR repostos (5).
- [ ] Metas 10X da semana escritas. Uma coisa a mudar no script.

## 8. Como fazer 10X sem 10X horas

- **Densidade:** uma rua por dia; a porta seguinte é a do lado. Andar é tempo morto.
- **Lote:** demos 5–6 por chat, cartões-demo 10 por folha, packs feitos ao domingo, follow-ups todos em 30 min.
- **Script decorado:** zero improviso na abertura; a energia vai para ouvir o dono.
- **Sem pausa entre portas:** decidir "entro" é uma decisão que se toma uma vez por dia, não 10.
- **Deixar sempre algo:** cada porta rende pelo menos um cartão na caixa — a rua começa a conhecer o nome.
- **Follow-up custa quase zero:** é aqui que se multiplica por 10 sem tempo de rua.
- **Um dia 10X por semana:** tarde e manhã inteiras na mesma zona — até a rua inteira saber quem és.
