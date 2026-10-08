# Ferramenta grátis: cartaz de avaliações Google (ideia 9 dos agentes de leads)

O dono cola o link de avaliação do Google, escreve o nome do negócio e, em 1 minuto, imprime (A4/A5), descarrega
ou partilha um cartaz com QR que leva o cliente direto ao formulário de avaliação. Bónus: mensagem pronta para mandar
aos clientes pelo WhatsApp. No fim, a caixa «E agora?» abre o diagnóstico do site.

**Porquê esta e não a «nota da tua ficha Google»:** corre toda no navegador do dono, sem servidor nem leitura de
fichas (que só funciona pela PONTE, por lotes). E cada cartaz impresso fica no balcão com a linha
«Cartaz grátis em pachecost.com/cartaz»: publicidade permanente à frente dos clientes de outros negócios.

| Língua | Ficheiro em `dist/` | Endereço |
|---|---|---|
| PT | `cartaz.html` | pachecost.com/cartaz |
| RO | `ro/afis.html` | ro.pachecost.com/afis |
| EN | `en/poster.html` | pachecost.com/en/poster |

Gerar: `python3 gerar.py` (lê `src.html`, `textos.json`, `logo.svg`, `vendor/qrcode.min.js`, fontes de `marca/fontes/`).
QR: qrcode-generator 1.4.4 de Kazuhiko Arase (MIT), embutido. Testado: o QR do PNG lê-se de volta (OpenCV) com o link exato.

O link aceita: link de avaliação (`g.page/r/…/review`, `search.google.com/local/writereview?placeid=…`), link da ficha
(`maps.app.goo.gl`, `google.com/maps`, `g.co/kgs`, `g.page`), Place ID (`ChIJ…`) ou um texto com o link no meio.
Outros sites dão erro. Nada sai do telemóvel do dono; o navegador lembra o último cartaz (localStorage).

## Medição (GoatCounter, como o resto do site)

Visitas: `pachecost.com/cartaz`, `ro.pachecost.com/afis`, `pachecost.com/en/poster`. Eventos (um por visita):
`ferramenta/cartaz/link-review`, `link-maps`, `link-erro`, `ajuda`, `imprimir`, `descarregar`, `partilhar`,
`mensagem-copiar`, `mensagem-whatsapp`, `diagnostico`. O botão do diagnóstico leva
`utm_source=ferramenta&utm_content=diag-cartaz` (RO `diag-afis`, EN `diag-poster`), que abre logo o diagnóstico.

## Integração no site (thread do site, ramo kztskg)

1. Copiar `dist/cartaz.html`, `dist/ro/afis.html` e `dist/en/poster.html` para `sites/pacheco-studios/` nos mesmos
   caminhos (o gerar.py do site tem de os copiar para o zip).
2. Em `_redirects`, **antes** das regras `/ro` e `/ro/*` (secção 2):
   ```
   https://ro.pachecost.com/afis       /ro/afis.html    200!
   https://ro.pachecost.com/afis/      /ro/afis.html    200!
   ```
   `pachecost.com/cartaz` e `/en/poster` funcionam sozinhos (URLs bonitos do Netlify).
3. `sitemap.xml`: juntar os três endereços.
4. Ligações para lá (sugestão): no rodapé das três línguas, «Cartaz grátis de avaliações» / «Afiș gratuit pentru recenzii» / «Free review poster».
5. Refazer o `pachecost-com-netlify.zip` (thread das demos) e o Tomás sobe-o.
