# Agente 3 · Raio-X do primeiro contacto (gatilho grátis da consultoria)

Desde 11/10/2026 a Pacheco Studios é uma consultora de sistemas com IA (playbook em /mnt/project-files/playbook/). Este agente **não** faz auditorias (a Auditoria de Sistemas com IA é o produto pago) e **não** vende sites. Gera um PDF grátis de 3 páginas para negócios com site fraco: o caminho de um cliente novo do Google até à primeira mensagem, onde se parte (medido), UMA vitória rápida desenhada como System Print e 3 perguntas sobre o que não se vê de fora. O pedido é sempre o mesmo: 20 minutos de triagem curta. Sem preço.

## Como corre

1. **Candidatos** — `candidatos.csv`: negócios com site próprio tirados das fichas Google que os lotes de demos leram pela ponte. Para mais: pesquisas no Maps pela ponte (`pagina`), ler o campo «Site» e acrescentar linhas.
2. **Medir** — pela PONTE: `auditar <slug> <url>` em `.github/ponte.txt` (até ~25 por push; para mais, vários pushes seguidos). Lighthouse móvel + iPhone simulado → `auditorias/dados/<slug>.json` + `.jpg`.
3. **Ranking** — `python3 agentes/auditoria-sites/gerar.py` → `auditorias/RANKING.md` (fraqueza 0–100).
4. **Gerar** — `python3 agentes/auditoria-sites/raiox.py --top 10` (ou `raiox.py <slug> …`) → `raio-x/<slug>/radiografie-<slug>-ro.pdf` (dono) e `raio-x-<slug>-pt.pdf` (Tomás, + página de notas para os 20 minutos) e `raio-x/ENVIAR.md` (mensagens RO e links raw). Precisa de playwright (`CHROMIUM=<caminho>` se a versão não bater).
5. **Enviar** — o Tomás manda mensagem + PDF pelo WhatsApp Business RO. WhatsApp do dono: «?» nos telemóveis, «não» nos fixos (ligar).

## Regras de conteúdo

- Só números medidos no dia. A única estatística de fora é a da Google (Think with Google, 2017), com a fonte na página.
- O ponto «Quem responde e em quanto tempo?» fica sempre a cinzento: não se mede de fora e é o motivo da conversa.
- A vitória rápida é o gatilho, nunca o produto: escolhida pela primeira quebra medida (`VITORIAS` em `raiox.py`: contacto, marcação, entrada).
- Nunca chamar «auditoria» a este PDF, nunca oferecer «um site novo», nunca pôr preço.
