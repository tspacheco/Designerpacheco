# Cartão de visita — Pacheco Studios (versão romena)

É o mesmo cartão para todos os negócios.

- **Frente:** o slogan em romeno ("Unde afacerea ta prinde viață online."), com o ponto final no laranja da marca, e o
  propósito: *Web design · implementare sisteme AI*.
- **Verso:** nome e função (*Fondator*), telefone com o indicativo (+351 967 117 357) e WhatsApp, email, Instagram,
  o QR para ver os trabalhos (*Vezi proiectele*) e, em baixo, a frase que dá vontade de apontar a câmara.

## Mudar a frase (ou outro texto)

Tudo o que o cartão diz está em `marca/dados.json`, no bloco `"cartao"`:

- `"frase": 1`: escolhe uma das 5 frases da lista `frases`. As palavras entre `*asteriscos*` ficam a laranja.
  O significado em português está em `frases_pt`.
- Depois de mudar: `python3 marca/cartao/gerar.py`. Isto refaz o PDF, a pré-visualização e a folha
  `frases-opcoes.png`, que mostra o verso com as 5 frases lado a lado.

Antes de imprimir, pedir a um romeno que leia o cartão.

## Antes de imprimir

1. Comprar o domínio, publicar o site e confirmar que `pachecostudios.pt/c` abre. Depois pôr
   `dominio_confirmado: true` em `marca/dados.json`. Enquanto isso não estiver feito, o gerador só faz
   `cartao-impressao-PROVA.pdf`, com uma faixa vermelha.
2. A página para onde o QR aponta ainda está em português. Tem de estar em romeno antes de os cartões chegarem
   aos negócios.
3. Imprimir 1 em casa a 100 % e ler o QR com 2 telemóveis (um deles Android antigo).

## Especificações para a gráfica

| | |
|---|---|
| Formato final | 85 × 55 mm, cantos retos |
| Ficheiro | `cartao-impressao.pdf`: 2 páginas (frente, verso), 91 × 61 mm com 3 mm de sangria, fontes incorporadas (com Ă, Â, Î, Ș, Ț), sem marcas de corte |
| Cor | PDF em RGB; a gráfica converte para CMYK. Pedir prova, sobretudo do preto da frente |
| Papel | 350–400 g, mate ou não revestido. Sem brilho: lê-se melhor ao sol e o QR não reflete |
| Acabamento | Opcional: plastificação mate *soft-touch* na frente (protege o preto) |
| Não fazer | Reduzir o cartão, mudar a cor do QR ou pôr verniz brilhante por cima do QR |

## Acessibilidade e testes (correm sempre em `gerar.py`)

- Letra mínima de 7,5 pt. O telefone está a 9 pt negrito, o nome a 11,5 pt e a frase a 13 pt.
- Contraste de cada texto: o principal a 15,6:1 e o secundário acima de 7:1. O laranja do verso foi escurecido para
  4,9:1.
- Todas as letras existem na fonte: as fontes trazem o subconjunto latin-ext, com os glifos romenos Ă, Ș e Ț.
- Nenhuma tinta a menos de 4 mm do corte e nenhum texto sobreposto. Isto é medido nos píxeis da imagem a 600 ppp,
  não em caixas.
- QR de 21 mm (versão 2-Q, módulos de 0,84 mm) com a zona de silêncio livre (3,4 mm à volta). É lido na imagem a
  600 ppp, no tamanho que uma câmara de telemóvel vê e desfocado.
- Quem não usa QR tem o endereço impresso por baixo: `pachecostudios.pt`.

## O QR

Abre `https://pachecostudios.pt/C`, um redirecionamento que controlamos. Para mudar o destino (por exemplo, para o
Instagram ou para uma versão romena da página), troca-se `destino_qr` em `marca/dados.json` e publica-se o site de
novo, **sem reimprimir cartões**.

Editar `cartao.src.html` (desenho) e `marca/dados.json` (textos e dados). O `cartao.html` é gerado.
