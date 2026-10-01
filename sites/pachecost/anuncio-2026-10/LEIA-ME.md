# pachecost.com — primeiro ecrã para quem chega por anúncio (01/10/2026)

O site da Pacheco Studios não vive neste repositório: é gerado por `gerar.py` a partir de `marca/dados.json` (no PC do Tomás) e publicado no Netlify. Esta pasta guarda a alteração feita sobre o deploy exportado a 01/10, para a repetir ou passar para o gerador.

## O que muda

Só para quem chega com `?utm_…`, `fbclid` (a app do Facebook acrescenta-o a todos os cliques) ou `?origem=anuncio`, decidido no `<head>` antes de pintar (`html.anuncio`):

- **Primeiro ecrã** (PT e RO): "Sites para restaurantes" · "Um site assim para o teu restaurante." · "Fazemos o teu site e mostramos-to antes de pagares. Sem compromisso." · botão WhatsApp com a mensagem já escrita ("Vi o anúncio…"). Em romeno o mesmo. O cabeçalho de sempre fica escondido; o resto da página é igual.
- **Em destaque:** o terceiro quadrado passa a Grupo Naval (restaurante) em vez da Toda Chic (loja de roupa).
- **Sem intro** (os carros): quem vem do anúncio vê logo a página.
- **GoatCounter:** eventos `anuncio/chegada` (ao carregar) e `anuncio/whatsapp` / `anuncio/telefone` (ao sair). Taxa de contacto do anúncio = `anuncio/whatsapp` ÷ `anuncio/chegada`. O pixel da Meta continua a enviar `Contact` nas saídas (só em PT: a página romena não tem pixel).

Para toda a gente: o **aviso de cookies** passou a faixa colada ao fundo no telemóvel (127 px em vez de um cartão que tapava um terço do ecrã). No computador fica como estava.

Sem parâmetros na ligação, a página é a de sempre (verificado com capturas). A página inglesa só ganha o aviso compacto e os contadores: não tem herói de anúncio.

## Publicar

1. Netlify → site pachecost → Deploys → arrastar `pachecost-deploy-anuncio.zip` (o zip entregue no chat; é a pasta `novo/` do script).
2. Testar no telemóvel: `https://pachecost.com/?origem=anuncio` e `https://ro.pachecost.com/?origem=anuncio`; sem parâmetros tem de aparecer a página normal.
3. **Passar a alteração para o gerador** (`gerar.py` / `marca/dados.json`): o `pachecost-anuncio.patch` mostra as linhas exatas (3 ficheiros: `index.html`, `ro/index.html`, `en/index.html`). Sem isto, o próximo `gerar.py` apaga tudo.

## Repetir noutro deploy

```bash
# cur/ = deploy exportado do Netlify (Deploys → … → Download), descomprimido
python3 aplicar.py        # escreve novo/; pára se o HTML do gerador tiver mudado
```
