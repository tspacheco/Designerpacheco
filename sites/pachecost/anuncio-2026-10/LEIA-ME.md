# pachecost.com — alterações de 01/10/2026

O site da Pacheco Studios não vive neste repositório: é gerado por `gerar.py` a partir de `marca/dados.json` (no PC do Tomás) e publicado no Netlify. Esta pasta guarda as alterações feitas sobre o deploy exportado a 01/10, para as repetir ou passar para o gerador. `aplicar.py` lê `cur/` (deploy exportado) e escreve `novo/`; `pachecost-anuncio.patch` mostra as linhas exatas nos 3 ficheiros (`index.html`, `ro/index.html`, `en/index.html`).

## 1. Primeiro ecrã para quem chega por anúncio (PT e RO)

Só para quem chega com `?utm_…`, `fbclid` (a app do Facebook acrescenta-o a todos os cliques) ou `?origem=anuncio`, decidido no `<head>` antes de pintar (`html.anuncio`):

- "Sites para restaurantes" · "Um site assim para o teu restaurante." · "Fazemos o teu site e mostramos-to antes de pagares. Sem compromisso." · botão WhatsApp com a mensagem já escrita ("Vi o anúncio…"). Em romeno o mesmo. O cabeçalho de sempre e o lema ficam escondidos; o resto da página é igual.
- Em destaque: o terceiro quadrado passa a Grupo Naval (restaurante) em vez da Toda Chic.
- Sem intro (os carros).
- GoatCounter: `anuncio/chegada` ao carregar e `anuncio/whatsapp` / `anuncio/telefone` ao sair. Taxa de contacto do anúncio = `anuncio/whatsapp` ÷ `anuncio/chegada`. O pixel da Meta continua a enviar `Contact` (só em PT; a página romena não tem pixel).

## 2. Aviso de cookies compacto

Faixa colada ao fundo no telemóvel (127 px em vez de um cartão que tapava um terço do ecrã). No computador fica como estava.

## 3. Separadores com mais ar (computador)

A partir de 48rem: 2,25rem entre separadores, sublinhado só na largura do texto, barra a 3,5rem (`--tabs`, de que dependem os `scroll-margin`). No telemóvel ficam como estavam: os três têm de caber.

## 4. Lema (PT, RO, EN)

Acima de "Sites", com um traço laranja que se desenha ao carregar (respeita `prefers-reduced-motion`):

- PT: O trabalho que faz o teu negócio subir de nível.
- RO: Munca care îți duce afacerea la următorul nivel.
- EN: The work that takes your business to the next level.

Escondido a quem chega por anúncio (aí fala o herói).

## 5. Ponte para as automações (PT, RO, EN)

Entre os tipos de negócio e "Mais sites que fizemos": cartão com "E depois do site", a frase das automações ("O site traz clientes. As automações mantêm-nos."), as quatro automações mais concretas em texto, o botão "Ver as automações" (abre o separador `#automatizari`) e as duas bolhas de chat do rececionista, que entram uma a seguir à outra ao fazer scroll. Reutiliza as classes `.chat/.msg` que já existiam.

## Publicar

1. Netlify → site pachecost → Deploys → arrastar `pachecost-deploy-anuncio.zip` (entregue no chat; é a pasta `novo/`).
2. Testar no telemóvel: `https://pachecost.com/?origem=anuncio` e `https://ro.pachecost.com/?origem=anuncio`; sem parâmetros tem de aparecer a página normal, com o lema.
3. **Passar as alterações para o gerador** (`gerar.py` / `marca/dados.json`). Sem isto, o próximo `gerar.py` apaga tudo.

## Repetir noutro deploy

```bash
# cur/ = deploy exportado do Netlify (Deploys → … → Download), descomprimido
python3 aplicar.py        # escreve novo/; pára se o HTML do gerador tiver mudado
```
