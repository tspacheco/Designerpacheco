# Brief dos construtores do caçador

Cada construtor recebe 3 a 4 negócios (linha do `AAAA-MM-DD.tsv` + brief em `briefs-AAAA-MM-DD.md`) e constrói a demo de cada um em `sites/<slug>/`, no repositório `/home/user/Designerpacheco` (ramo `claude/cacador-diario-nkiz36`). Não fazer commit, push nem usar ferramentas `mcp__hearthbot__`; o coordenador da corrida faz isso.

## Antes de começar

1. Ler `CLAUDE.md`, `PLAYBOOK.md` §3, §3-A e §11, e um site de referência do lote 4 inteiro: `sites/star-service-auto/` (estrutura de pastas, `index.src.html`, `ferramentas/build.py`, `ferramentas/fontes.py`, `DADOS-PARA-O-DONO.md`, `media/LEIA-ME.txt`). Copiar `ferramentas/` e `netlify.toml` de lá e adaptar.
2. Usar os skills `frontend-design` e `ui-ux-pro-max` para a direção de cada site (o CLAUDE.md obriga), mas a fonte display e a assinatura visual são as do brief: não trocar sem razão (ver ponto 4).
3. Dados do negócio: a ficha está em `ponte/cc-AAAAMMDD-f-<slug>.txt` (texto visível) e `.html`; fotos em `sites/<slug>/media/g/*.webp` quando existirem. Ler as avaliações visíveis no `.txt` para a voz do negócio e os serviços.

## Regras de cada site

- Romeno por omissão com botão EN; `pt.html` é a mesma página em PT (o `build.py` gera as duas a partir de `{{ro|en|pt}}`).
- Um só ficheiro HTML com CSS/JS embutidos e fontes em base64 (`ferramentas/fontes.py`, subconjuntos latin + latin-ext). Zero dependências externas exceto o iframe do mapa.
- Um só `<h1>`, JSON-LD do negócio, `prefers-reduced-motion`, `:focus-visible`, contraste AA, banner «PREZENTARE PACHECO STUDIOS» (como nas outras demos), rodapé com ANPC SAL + ODR (como o site de referência).
- **HONEST-DATA:** só o que está na ficha (nome, nota, nº de avaliações, telefone, morada, horário, categoria, avaliações). O que falta fica «de confirmat»; preços nunca inventados. Nada de notas sobre a origem dos dados; no máximo um selo «de confirmat».
- **CTA:** WhatsApp «?» → botão principal **Sună** (tel:) e o pedido do formulário sai por WhatsApp ou SMS; WhatsApp «sim» → WhatsApp; fixo → só **Sună**.
- Fotos: usar só ficheiros diretamente em `media/` (o motor das demos não copia subpastas: copiar de `media/g/` para `media/<nome>.webp`). Fundo SVG inline sempre, `<img>` por cima com `onerror`. Sem fotos → site ilustrado, nunca fotos falsas.
- Assinatura visual do brief, coreografada: sequência de entrada no herói, micro-interações, estados impecáveis. A funcionalidade que vende (marcação, pedido, montador, etc.) tem de funcionar de ponta a ponta.

## Verificar antes de entregar

1. A fonte display tem ă â î ș ț: `python3 -c "from fontTools.ttLib import TTFont; ..."` sobre o ficheiro descarregado; se faltar, escolher outra que não esteja em `/tmp/claude-0/fontes-usadas.txt` nem no PLAYBOOK §6 e dizê-lo na entrega.
2. `python3 ferramentas/build.py` sem erros; script do PLAYBOOK §4 (HTML-OK, um h1, banner; o `lang` é `ro` e não `pt-PT` nestas demos: ignorar esse aviso) e os zips `<slug>-netlify.zip` e `<slug>-hostinger.zip` como no site de referência.
3. Abrir `index.html` e `pt.html` no Chromium do Playwright (`executablePath: '/opt/pw-browsers/chromium'`) a 390 px e 1280 px: sem erros de consola, sem scroll horizontal; olhar para as capturas e corrigir o que estiver mal.
4. Crítica final: «isto podia ser um template?» Se sim, refazer a assinatura.

## Entrega (texto final, curto)

Por site: slug, fonte display usada, assinatura, funcionalidade, tamanho do `index.html`, e qualquer desvio do brief ou dado em falta.
