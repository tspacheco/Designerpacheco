# ro.pachecost.com — a página do QR do cartão (Roménia)

Uma página só, em romeno, com três separadores e o contacto no fim:

1. **Proiecte** — um quadrado por site já feito, com a fonte e as cores do próprio site. Ao tocar, abre o site;
   lá dentro há um botão fixo «Înapoi la proiecte». No fim da grelha, o quadrado tracejado «Afacerea ta?» leva ao
   contacto. Por baixo, «Cum lucrăm»: fazemos o site antes de pagares, mostramos no telemóvel, só pagas se gostares.
2. **Automatizări** — 8 automatizações. Cada cartão mostra o título e a dor na voz do dono («Îți sună cunoscut?»);
   ao tocar abre o fluxo em 4 passos, o que ganha, o que precisa e com quais combina. No fim, «Se leagă între ele»:
   três caminhos (restaurante · salão/consultório · loja) com 3 automatizações cada, para não confundir.
3. **Ce mai facem** — 7 serviços (loja online, várias línguas, Google Maps, ementa QR, logótipo, foto/vídeo, sistemas
   à medida), com «Vezi un exemplu» quando há um site que o mostra.

Sem preços: combinam-se com cada negócio. A versão portuguesa, para rever, fica em `/pt/`.

## Editar

- Textos: `conteudo/ro.json` (romeno) e `conteudo/pt.json` (português). A estrutura é igual nos dois.
- Quadrados: `portfolio.json` — `ativo`, `nome`, `fonte`/`peso`/`bg`/`ink`/`accent` (as do site), `pasta` (site do
  repositório, copiado para `/p/<slug>/`) ou `url` (site externo). Os parceiros sem site no repositório (Simona's,
  ProBuilders, Barbearia do Cão, Gelataria Muxagata) estão desligados até haver o `url` certo.
- Contactos e domínio: `marca/dados.json` (os mesmos do cartão).
- Desenho: `index.src.html`. `index.html`, `pt/index.html` e `404.html` são gerados.

Depois de qualquer alteração: `python3 gerar.py`. Gera `dist/`, corre os testes e faz `pacheco-studios-netlify.zip`
(~18 MB, com as cópias dos 13 sites; não vai para o git).

## Publicar

1. No DNS de **pachecost.com**: registo `CNAME ro → <nome>.netlify.app` (o Netlify indica o nome exato).
2. Netlify → arrastar `pacheco-studios-netlify.zip` → *Domain management* → `ro.pachecost.com`. O HTTPS é automático.
3. Testar no telemóvel: `ro.pachecost.com/c` abre a página; um quadrado abre o site e o «Înapoi» volta;
   `ro.pachecost.com/xyz` dá a página 404 romena.
4. Só então: `dominio_confirmado: true` em `marca/dados.json` e gerar o PDF final do cartão.

Tem de ser Netlify (o `_redirects` do QR não existe no Hostinger). As cópias em `/p/` levam `noindex`: o Google
não as indexa, para não competirem com os sites dos próprios negócios.

## O que o gerador verifica

Todas as letras do conteúdo existem nas fontes embutidas (Ă, Ș, Ț incluídos); HTML válido, um só `h1`,
Livro de Reclamações, zero campos por preencher. Em 360, 390 e 1280 px, nas três vistas: sem scroll horizontal,
letra ≥ 12 px, contraste ≥ 4,5:1, alvos de toque ≥ 44 px, títulos por ordem. Separadores com e sem JavaScript,
as 8 automatizações a abrir, as ligações «Merge bine cu» a abrir a apontada, todas as ligações dos quadrados a
existir, o botão «Înapoi» dentro dos sites copiados, o `noindex`, a 404 e a barra fixa do WhatsApp.
