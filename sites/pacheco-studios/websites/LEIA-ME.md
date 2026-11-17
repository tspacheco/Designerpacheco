# Página escondida de portefólio de websites (16 nov 2026)

- Endereços depois de publicar: pachecost.com/websites/ (PT) e pachecost.com/en/websites/ (EN).
- ZIP para o Netlify: pacheco-studios-netlify-2026-11-17-v29-websites.zip = v27 (9 nov) + a página (substitui o v28). Nada mais mudou no site.
- 17 nov (pedido do Tomás): a página EN mostra cada site na versão inglesa (9 sites) e os 6 sites com hero em vídeo aparecem a correr (Jasmim 2, Hanam, Bom Paladar, Ginásio Clube de Tavira, São Martinho, Olá Kathmandu). Ficheiros media/<id>-en-d/-m (.webp e .mp4, laço de 7 s sem salto). Grupo Naval, Barbearia do Cão e Carne Pura só têm PT. A página PT ficou igual.
- Escondida: sem link no site, fora do sitemap e do robots.txt, noindex na página e no _headers. O montar_zip.py recusa-se a fazer o ZIP se alguma página do site apontar para /websites.
- Fonte: GitHub tspacheco/Designerpacheco, ramo claude/websites-portefolio, sites/pacheco-studios/websites/ (gerar_websites.py + montar_zip.py + media/).
- Sem preços, sem testemunhos, sem números.

## Os 12 sites (todos abertos a 16 nov 2026, HTTP 200, com captura real)
Prova de autoria: crédito «Site por Pacheco Studios» no próprio site (C), lista de clientes reais do portfolio.json confirmada pelo Tomás em set. 2026 (L) ou memória do projeto (M).
hanamquarteira.com (C, L) · bompaladar.pt (C, L) · magickeyiasi.com (C, M) · ginasioclubetavira.com (L) · olakathmandu.com (L, M) · barbeariadocao.com (C, L) · sao-martinho.com (C, L) · gruponaval.online (L, 1.ª venda) · naisfood.ro (M) · jasmim2marisqueira.pt (L) · barbeariadocaocarnes.netlify.app (M) · gelatariamuxagata.com (C, L)

## Ficaram de fora (não estão publicados como site do cliente)
Andalu Gastrobar, Kopa 11, WashUp, Tshirts do Sul, TopCopias, Borda d'Água, Toda Chic (sem endereço público), ProBuilders (sem endereço), as demos /p/ e todas as apresentações a quem não comprou.

## Acrescentar um site
1. Pedir captura na ponte: `captura <id> <url> pt-PT` em .github/ponte.txt (ramo com o ponte.yml novo). Versão inglesa e vídeo do hero: `gravar <id>-en <url> locale=en-US seg=8 [ls=chave=en] ['clique=<css>']` (grava no Chrome, que toca H.264); fazer o laço com o xfade descrito no commit de 17 nov.
2. Converter para media/<id>-d.webp (1120×700) e <id>-m.webp (420×909), acrescentar a entrada em SITES.
3. `python3 montar_zip.py <zip-atual> <zip-novo>`.
