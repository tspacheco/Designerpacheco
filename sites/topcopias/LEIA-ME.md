# TopCopias · estado do site novo (18 out 2026)

Copistería TopCopias, Zaragoza. TOPCOPIAS S.L., CIF B10964534. Duas lojas: P.º de Fernando el Católico, 30 (ficha Google 4,5★, 365 avaliações, tel. 693 36 15 12, trabajostc@gmail.com) e Calle Arzobispo Apaolaza, 3 (domicílio fiscal, tel. 876 950 183, imprimetop@gmail.com). Pedidos: pedidos@topcopias.com. WhatsApp no site atual: 747 452 495 (o link deles está partido: wa.me/3747452495, falta o 4).

## Site atual (topcopias.com, WordPress + Elementor + WooCommerce)
- Vende impressão online com envio para a península (3,95 € + IVA, grátis desde 39 €), "desde 0,019 €", +30.000 clientes, 20 anos, entrega 24–48 h.
- O configurador de preços é JavaScript e não se lê da cloud; o único produto WooCommerce é "Impresión" a 1,00 €. Não há horários, nem preços públicos, nem recolha em loja clara.

## O que o site novo faz
- Hero com zona de upload: o cliente larga o PDF, a página conta as páginas e deteta no próprio telemóvel quais têm cor (pdf.js), e o preço aparece linha a linha.
- Opções: cor automática / tudo P&B / tudo cor, frente e verso, 2 páginas por face, A4/A3, papel 80/100/160 g, agrafado, furação, espiral, térmica; recolha numa das duas lojas ou envio.
- Formulário Netlify Forms "pedido" com até 5 ficheiros (limite Netlify 8 MB por envio; acima disso o pedido segue sem ficheiros e o cliente manda-os por WhatsApp/email com o código TC-DDMM-XXXX). Sem pagamentos: paga ao levantar.
- Páginas: Inicio, Imprimir online, Servicios, Precios, Tiendas, Aviso legal, Privacidad, Cookies, 404. Redirects 301 das URLs antigas.

## Ficheiros
- fonte/build.py (`python3 build.py` → site/, `python3 build.py preview` → preview/); preços em fonte/data/precios.json; dados em fonte/data/negocio.json.
- topcopias-site.zip = pasta site/ para arrastar no Netlify.
- Pré-visualização: https://claude.ai/artifact/NocDXY4GzNfHsEmdCZZtqN (republicar a partir de uma cópia de preview/ no scratchpad).
- Fotos: só a fachada e o interior recortados da captura da ficha Google (baixa resolução).

## Falta do cliente
1. Tabela de preços real (os valores em precios.json são de referência; "confirmado": false mostra aviso na página Precios).
2. Horário completo das duas lojas (só se sabe que abre às 9:00 de segunda a sexta).
3. Qual o número de WhatsApp oficial (747 452 495 ou 693 36 15 12).
4. Que serviços fazem de facto: encadernação térmica, flyers, cartões de visita, A3, cartolina.
5. Fotos boas da loja e trabalhos (Instagram/Google) e o logótipo em alta (pedido à sessão no PC).
6. Se o envio para a península continua e se querem pagamento online mais tarde.
7. Email de destino das notificações do formulário Netlify e domínio (topcopias.com aponta hoje para o WordPress).

## 18 out, 2.ª versão (inspiração copyfly.es)
- Barra promo preta no topo, hero imersivo em ecrã inteiro com o upload numa "pílula" e preços desde, cinta amarela de serviços a correr.
- Fundo do hero: animação em canvas de folhas a voar e a empilhar (assets/hero.js), já a funcionar. Quando existirem assets/media/hero-h.mp4 e hero-v.mp4, o build usa o vídeo (horizontal em ecrãs largos, vertical no telemóvel).
- Vídeos Higgsfield (Seedance 2.5, 8 s, 1080p, sem som), jobs 4b09b270-db53-42aa-bd28-59a2c17802ec (16:9) e c0382412-0a1d-411b-9565-517b1717d092 (9:16). A cloud não os descarrega; quando chegarem: `python3 preparar_video.py horizontal.mp4 vertical.mp4 && python3 build.py`, depois refazer o ZIP.
