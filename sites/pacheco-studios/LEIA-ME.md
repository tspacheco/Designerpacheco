# ro.pachecost.com — a página do QR do cartão (Roménia)

Uma página só, em romeno, com três separadores e o contacto no fim:

1. **Proiecte** — um quadrado por site já feito, com a fonte e as cores do próprio site. Ao tocar, abre o site;
   lá dentro há um botão fixo «Înapoi la proiecte». No fim da grelha, o quadrado tracejado «Afacerea ta?» leva ao
   contacto. Por baixo, «Cum lucrăm»: fazemos o site antes de pagares, mostramos no telemóvel, só pagas se gostares.
2. **Automatizări** — segue a direção «mostrar a máquina» (PLAYBOOK, secção 16). No topo, «Ce e, de fapt, AI-ul din
   spate?»: cinco frases sobre o que a AI faz e não faz. Depois, 8 automatizações. Cada cartão mostra o título e a
   dor na voz do dono («Îți sună cunoscut?»). Ao tocar, abre a máquina por dentro: o fluxo desenhado (declanșator,
   automat, persoană, decizie), o que ganha, as regras, quem decide o quê (tu · sistemul · noi), uma conversa de
   exemplo, o que é preciso, com quais combina e «Cere o demonstrație pe WhatsApp». No fim, «Se leagă între ele»:
   três caminhos (restaurante · salão/consultório · loja) com 3 automatizações cada, para não confundir.
3. **Ce mai facem** — 7 serviços (loja online, várias línguas, Google Maps, ementa QR, logótipo, foto/vídeo, sistemas
   à medida), com «Vezi un exemplu» quando há um site que o mostra.

Sem preços: combinam-se com cada negócio. A versão portuguesa, para rever, fica em `/pt/`.

## Editar

- Textos: `conteudo/ro.json` (romeno) e `conteudo/pt.json` (português). A estrutura é igual nos dois.
- Quadrados: `portfolio.json` — `ativo`, `nome`, `fonte`/`peso`/`bg`/`ink`/`accent` (as do site), `pasta` (site do
  repositório, copiado para `/p/<slug>/`) ou `url` (site externo, abre noutro separador). Só a ProBuilders está
  desligada, até haver o `url` certo.
- Contactos e domínio: `marca/dados.json` (os mesmos do cartão).
- Desenho: `index.src.html`. `index.html`, `pt/index.html`, `404.html`, `_redirects`, `_headers` e `netlify.toml`
  são gerados: não editar à mão.

Depois de qualquer alteração: `python3 gerar.py`. Gera `dist/`, corre os testes e faz `pacheco-studios-netlify.zip`
(~18 MB, com as cópias dos 11 sites do repositório; não vai para o git).

## Publicar (uma vez; depois, só arrastar o zip novo)

O `pachecost.com` usa o DNS do Netlify (servidores `nsone.net`). Por isso não é preciso mexer no DNS à mão.

1. `python3 gerar.py` → sai `pacheco-studios-netlify.zip`.
2. Netlify, na mesma conta do `pachecost.com` → *Add new project* (ou *site*) → *Deploy manually* → arrastar o zip.
3. No projeto novo → *Domain management* → *Add a domain* → `ro.pachecost.com` → confirmar. O Netlify cria o registo
   sozinho e liga o HTTPS em minutos (às vezes até uma hora).
   - Se o `pachecost.com` estiver noutra conta: nessa conta, *Domains* → `pachecost.com` → *Add new record* →
     `CNAME`, nome `ro`, valor `<nome-do-projeto>.netlify.app`.
4. Testar no telemóvel: `ro.pachecost.com/c` abre a página em romeno; um quadrado abre o site e o «Înapoi» volta;
   `ro.pachecost.com/xyz` dá a página 404 romena.
5. Imprimir `marca/qr/qr-teste-a4.pdf` e ler os QR. Só depois mandar o cartão para a gráfica.

Para atualizar: `python3 gerar.py` → no projeto do Netlify, *Deploys* → arrastar o zip novo. O QR não muda.

Tem de ser Netlify: o `_redirects` do QR (`/c` e `/C`) e o `_headers` não existem no Hostinger. As cópias em `/p/`
levam `noindex` (na página e no cabeçalho): o Google não as indexa, para não competirem com os sites dos próprios
negócios.

## O que o gerador verifica

Todas as letras do conteúdo existem nas fontes embutidas (Ă, Ș, Ț incluídos); HTML válido, um só `h1`, Livro de
Reclamações, zero campos por preencher; o `_redirects` com `/c` e `/C` para o destino do QR. Em 360, 390 e 1280 px,
nas três vistas: sem scroll horizontal, letra ≥ 12 px, contraste ≥ 4,5:1, alvos de toque ≥ 44 px, títulos por ordem.
Separadores com e sem JavaScript, as 8 automatizações a abrir, as ligações «Merge bine cu» a abrir a apontada, todas
as ligações dos quadrados a existir, o botão «Înapoi» dentro dos sites copiados, o `noindex`, a 404 e a barra fixa do
WhatsApp.
