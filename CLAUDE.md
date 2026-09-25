# Pacheco Studios — Instruções de sessão

**Lê `PLAYBOOK.md` no início de cada sessão de trabalho.** É a fonte de verdade: contexto, preços, engine dos sites, catálogo, pendentes e método de prospeção. Não repitas contexto que já lá está.

## Regras essenciais (resumo — o detalhe está no PLAYBOOK.md)

- Responder **sempre em PT-PT**, tom direto, sem enchimento, respostas curtas (leitura em telemóvel).
- Sites: **um único ficheiro HTML** (CSS/JS embutidos), zero dependências externas exceto Google Fonts e iframe do mapa. `lang="pt-PT"`, um só `<h1>`, JSON-LD, `prefers-reduced-motion`, `:focus-visible`, link livroreclamacoes.pt no rodapé, banner "APRESENTAÇÃO PACHECO STUDIOS" nas demos.
- **HONEST-DATA:** nunca inventar ratings, preços, telefones, horários ou citações. Dado não confirmado → "a confirmar".
- **Imagens:** fundo SVG inline sempre; `<img>` opcional por cima com `onerror` de fallback; pasta `media/` com LEIA-ME.txt no zip.
- Validar e empacotar com o script bash da secção 4 do playbook (zips Netlify e Hostinger).

## Padrão de qualidade: NÍVEL 10K

Cada site entregue tem de ter qualidade percebida de 10 000 €, mesmo vendido a 500 €. Processo obrigatório por site:

1. **Usar o skill `frontend-design`** para a direção estética — brainstorm, direções alternativas, crítica antes e depois de construir. Uma assinatura visual **nova** por site (ver secção 5 do playbook — nunca repetir) e uma fonte display **nova** (secção 6).
2. **Usar o skill `ui-ux-pro-max`** para gerar o design system do tipo de negócio (paleta, par tipográfico, estilo) e adaptá-lo criticamente — nunca aceitar o output cru.
3. Motion coreografado (sequência de entrada no herói + micro-interações), copy com a voz do negócio, espaçamento e estados impecáveis, contraste AA.
4. Crítica final antes de empacotar: *"isto podia ser um template?"* Se sim, refazer a assinatura visual.

## Organização do repositório

- `PLAYBOOK.md` — playbook mestre (atualizar aqui, não em PDFs soltos).
- `sites/<nome-do-cliente>/index.html` — cada site num diretório próprio.
- `research/` — relatórios de pesquisa por zona (fazer uma vez, reutilizar).
- `prospecao/` — rotina de terreno: `checklist-diario.md`, `tracker.csv` + `stats.py` (funil e follow-ups), `qr/gerar_qr.py` (QR, cartões-demo e packs de mesa em PDF), `prospecao-10x.pdf` (versão para o telemóvel, gerada por `exportar_pdf.py` — editar os .md e voltar a gerar) e `visualizador.html` (leitor do PDF com PDF.js, publicado como artefacto).
- Atualizar o PLAYBOOK.md (catálogo, pendentes, trackers de fontes/assinaturas) sempre que um site é criado ou vendido, no mesmo commit.
