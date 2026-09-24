# Bom Paladar — carrossel de outono (outubro 2026)

Série dos azulejos, 2.º capítulo. Setembro foi azul e branco ("Obrigado, Almancil."); outubro fica azul e ocre, com o itálico da cor do barro dos tachos.

**Sugestão de publicação:** quinta, 1 de outubro, entre as 17h e as 18h (antes do jantar).

## Ordem

| # | Ficheiro | Texto |
|---|---|---|
| 1 | `01-capa.png` | OUTONO · ALMANCIL — **Tempo de tacho.** |
| 2 | `02-o-lume.png` | O LUME — **As noites arrefecem.** *A grelha, não.* |
| 3 | `03-outubro.png` | *O verão pediu branco.* **Outubro pede tinto.** Três tintos da nossa carta |
| 4 | `04-a-tabua.png` | PARA PARTILHAR — **E o tinto pede tábua.** *Queijos e enchidos, para dois.* |
| 5 | `05-reservar.png` | **Venha pelo tacho.** *Fique pelo tinto.* Reserve a sua mesa · WhatsApp · horário · morada |

## Legenda

> Chegou o tempo do tacho.
> As noites arrefecem, a grelha não, e o tinto volta à mesa.
>
> Jantar de segunda a sábado, das 19h às 22h30.
> Reservas pelo WhatsApp 918 958 233.
> R. do Comércio 367A, Almancil · bompaladar.pt
>
> #almancil #algarve #loule #cozinhaportuguesa #azulejos #outono #vinhotinto #jantaremalmancil

## Texto alternativo (Instagram → Definições avançadas → Acessibilidade)

1. Vários tachos de barro com arroz, camarão e ervas frescas. Texto: Tempo de tacho.
2. Bifes na grelha entre chamas. Texto: As noites arrefecem. A grelha, não.
3. Bife do lombo grelhado sobre espinafres, com o texto por cima. Texto: O verão pediu branco. Outubro pede tinto. Três tintos da nossa carta: Piano Reserva Touriga Nacional, Douro; Monte do Álamo Reserva, Alentejo; Barranco Longo Private Selection, Algarve.
4. Tábua de queijos e enchidos com queijo frito e nozes. Texto: E o tinto pede tábua. Queijos e enchidos, para dois.
5. Caril de camarão em cesto de pappadum, com malagueta e flor. Texto: Venha pelo tacho. Fique pelo tinto. Reserve a sua mesa. WhatsApp 918 958 233.

## Confirmar com a Simona antes de publicar

- Os três tintos continuam na carta (a lista é a da carta fotografada a 13/07).
- A tábua de queijos e enchidos continua a ser para dois.

## Imagens

- 02, 03 e 05 são fotos reais, sem edição (grelha, bife do lombo, caril de camarão). O 03 e o 05 têm estrutura própria para não repetirem setembro: no 03 o texto fica em cima e a foto em baixo; o 05 deixa a porta da casa e mostra um prato.
- 01 e 04: versão final com o prato real sobre mesa de azulejo azul e ocre, gerada no Higgsfield (GPT Image 2.5, 24/09). Sem essas imagens em `img/`, o `build.py` usa as fotos originais (é o rascunho atual).
- 03: a tira de azulejo no topo vem do painel azul e ocre gerado no Higgsfield; no rascunho usa o azulejo de setembro.
- Para gerar as finais: `python3 build.py --baixar` (precisa do domínio `d8j0ntlcm91z4.cloudfront.net` autorizado no ambiente), ou pôr as 3 imagens em `img/` com os nomes `ia-tachos.png`, `ia-tabua.png` e `ia-painel.png` e correr `python3 build.py`.
