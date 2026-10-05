# Facebook da Pacheco Studios

**Logótipo oficial: o selo** (decisão do Tomás, 04/10/2026). É o `logo.svg` do pachecost.com: fundo #0D0B08, anel duplo dourado #C9A256, anel tracejado laranja, "P" serifado creme #EDE8D8, "PACHECO STUDIOS" em arco e "DIGITAL". Não propor outros logótipos.

## Foto de perfil

`facebook-perfil-selo.png` (1024×1024): o selo com margem para o recorte redondo. Nesta máquina não há Georgia nem Arial, por isso o "P" saiu em FreeSerif e o arco em Liberation Sans; a foto que já está na página foi feita com as fontes originais e pode ficar. `perfil.html` gera-a.

## Capa (`capa/`)

Feita em 1640×924 (16:9). O computador mostra a faixa do meio, 1640×624 (820×312 a 2×); o telemóvel mostra a imagem inteira (640×360). Tudo o que importa está dentro dessa faixa e fora do canto inferior esquerdo, onde a foto de perfil se sobrepõe. Texto: o lema do site (02/10) + "Automações com IA · Sites" + 967 117 357 · pachecost.com.

| Ficheiro | Direção |
|---|---|
| `capa-facebook-selo-aberto-1640x924.png` | **Recomendada.** O anel do selo em ponto grande, com a frase no lugar do "P"; o ponto laranja da marca no anel tracejado. |
| `capa-facebook-ondas-1640x924.png` | Os anéis do selo a sair do canto da foto de perfil, como ondas, com o texto à direita. |
| `capa-facebook-selo-aberto-en-1640x924.png` | **Em inglês (04/10), a usar agora.** Selo aberto com "AI audit · Automations · Solutions", o lema em inglês, +351 967 117 357 · pachecost.com e "HQ Portugal · Working worldwide". |
| `capa-facebook-ondas-en-1640x924.png` | Ondas, em inglês, com o mesmo texto. |

`previa-*` (com `-en` para as inglesas) mostram cada uma com a foto de perfil por cima, no computador e no telemóvel (posições aproximadas).

Carregar: Página → foto de capa → Carregar foto. No computador, se o Facebook pedir para arrastar, centrar a frase e guardar. PNG porque tem texto: o Facebook comprime menos.

Refazer: `python3 gerar.py` (escreve `capa.html` com as quatro capas, PT e EN; textos em `TEXTOS`; fontes do site em `fontes/`) e `python3 exportar.py` (PNG + pré-visualizações; precisa do Playwright com o Chromium em `/opt/pw-browsers/chromium`).
