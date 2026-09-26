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

## Antes de imprimir

1. Publicar a página no Netlify com o domínio `ro.pachecost.com` (passos em `sites/pacheco-studios/LEIA-ME.md`) e
   confirmar no telemóvel que `ro.pachecost.com/c` abre. **Sem isto, o QR lê-se mas não abre nada.**
2. Pedir a um romeno que leia o cartão e a página.
3. Imprimir `marca/qr/qr-teste-a4.pdf` em casa, a 100 %, e ler os QR com 2 telemóveis (um iPhone e um Android).
   O de 21 mm é o do cartão.
4. Mandar `cartao-impressao.pdf` à gráfica.

`dominio_confirmado` já está a `true` em `marca/dados.json`, por isso o gerador faz o PDF final. Se o domínio mudar,
voltar a pô-lo a `false` até o novo endereço abrir: o gerador passa a fazer só `cartao-impressao-PROVA.pdf`, com uma
faixa vermelha.

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
- Quem não usa QR tem o endereço impresso por baixo: `ro.pachecost.com`.

## O QR

Abre `https://ro.pachecost.com/C`, um redirecionamento que controlamos (ficheiro `_redirects` do Netlify). Para mudar
o destino (por exemplo, para o Instagram), troca-se `destino_qr` em `marca/dados.json` e publica-se o site de novo,
**sem reimprimir cartões**. O mesmo QR, sozinho e noutros tamanhos (autocolante, gráfica, folha de teste), está em
`marca/qr/`.

Editar `cartao.src.html` (desenho) e `marca/dados.json` (textos e dados). O `cartao.html` é gerado.
