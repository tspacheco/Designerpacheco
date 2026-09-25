# Cartão de visita — Pacheco Studios

Frente escura com o slogan do Instagram. Verso claro com os contactos, um QR para ver os trabalhos e o
**espaço tracejado "O SEU SITE: pachecostudios.pt/____"**. Nesse espaço escreve-se à mão o endereço curto da demo que
fizemos para o negócio. É a assinatura do cartão: o cartão só fica completo quando tem lá o negócio da pessoa.

## Antes de imprimir

1. Em `marca/dados.json`: preencher `telefone` e pôr `dominio_confirmado: true` (só depois de comprar o
   `pachecostudios.pt` e publicar o site: o QR tem de abrir alguma coisa).
2. `python3 marca/cartao/gerar.py`. Enquanto faltar o telefone ou o domínio, o gerador só faz
   `cartao-impressao-PROVA.pdf`, com uma faixa vermelha, para não se imprimir por engano.
3. Imprimir 1 em casa a 100 % e ler o QR com 2 telemóveis (um deles Android antigo).

## Especificações para a gráfica

| | |
|---|---|
| Formato final | 85 × 55 mm, cantos retos |
| Ficheiro | `cartao-impressao.pdf`: 2 páginas (frente, verso), 91 × 61 mm com 3 mm de sangria, fontes incorporadas, sem marcas de corte |
| Cor | PDF em RGB; a gráfica converte para CMYK. Pedir prova, sobretudo do preto da frente |
| Papel | 350–400 g, mate ou não revestido. Sem brilho: lê-se melhor ao sol, o QR não reflete e o verso deixa escrever à caneta |
| Acabamento | Opcional: plastificação mate *soft-touch* **só na frente** (protege o preto). Verso sem plastificação nem verniz |
| Não fazer | Reduzir o cartão, mudar a cor do QR ou pôr verniz brilhante por cima do QR |

## Acessibilidade (medida pelo gerador, em `acessibilidade.json`)

- Letra mínima de 7,5 pt; o telefone está a 10 pt e o nome a 11,5 pt.
- Contraste: texto principal a 15,6:1; texto secundário acima de 7:1. O laranja pequeno do verso foi escurecido
  para 4,9:1, e o laranja da frente está a 5,5:1 em letra grande.
- QR com 21 mm, versão 2 com correção Q (aguenta ~25 % de dano) e módulos de 0,84 mm. Está em maiúsculas para usar
  o modo alfanumérico (menos módulos, mais fáceis de ler). É lido na imagem a 600 ppp, reduzido ao tamanho que uma
  câmara de telemóvel vê e desfocado.
- Quem não usa QR tem alternativas: o endereço vem impresso no espaço tracejado e há a instrução "aponte a câmara".
- Os números estão em Space Mono (0/O e 1/l não se confundem). Os ícones têm sempre texto ao lado. Nenhuma
  informação depende só da cor.

## O QR e os endereços escritos à mão

- O QR abre `https://pachecostudios.pt/C`, um redirecionamento que controlamos. Hoje leva à página da Pacheco Studios.
  Para levar ao Instagram, troca-se `destino_qr` em `marca/dados.json` e publica-se o site de novo. **Não é preciso
  reimprimir os cartões.**
- Espaço tracejado: publica-se a demo no Netlify e acrescenta-se em `enderecos_curtos`, por exemplo
  `"tasca-ria": "https://tasca-ria.netlify.app"`. Depois `python3 sites/pacheco-studios/gerar.py` e volta a
  publicar-se o zip. Quem escrever `pachecostudios.pt/tasca-ria`, ou escrever `tasca-ria` no campo da página, vai
  parar à demo.

Editar `cartao.src.html` (desenho) e `marca/dados.json` (dados). O `cartao.html` é gerado.
