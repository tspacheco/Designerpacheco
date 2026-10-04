# Fotos de perfil para o Facebook (04/10/2026)

Três versões em 1024×1024 px (PNG), a partir das fontes embutidas em `social/fonts/`. O Facebook mostra a foto de perfil recortada em círculo, a 170 px no computador e 128 px no telemóvel; `pre-visualizacao-facebook.png` mostra as três já recortadas, nos dois tamanhos.

| Ficheiro | O que é |
|---|---|
| `facebook-perfil-atual.png` | Identidade atual: "P" em Archivo Black com o ponto laranja, sobre carvão. É a que bate com o site, a imagem de partilha e os anúncios. |
| `facebook-perfil-marca.png` | Ponto laranja + PACHECO STUDIOS em Space Mono. Legível só no computador; no telemóvel fica pequeno. |
| `facebook-perfil-selo.png` | O selo de `logo.svg` do site (dourado, P serifado, "DIGITAL"), com margem para o recorte. Nesta sessão não há Georgia nem Arial: o P saiu em FreeSerif e o arco em Liberation Sans. |

`perfil.html` gera as três (fontes em data URI). Para refazer: abrir num browser a 1024 px de largura e capturar cada `.quadro`, ou correr o Playwright como na sessão.
