# Agente 3 · auditoria grátis a sites fracos

Negócios que **já pagam por um site** mas têm um site fraco recebem uma auditoria grátis: «o teu site hoje vs. o que podia ser», com notas reais, 3 vitórias rápidas e o que isso quer dizer em clientes. Zona por omissão: Iași (PDF em romeno para o dono, versão PT com notas para o Tomás).

## Como corre

1. **Candidatos** — `candidatos.csv`: negócios com site próprio tirados das fichas Google que os lotes de demos já leram pela ponte (os que foram excluídos «por já terem site»). Para mais: novas pesquisas no Maps pela ponte (`pagina`), ler o campo «Site» e acrescentar linhas.
2. **Medir** — pela PONTE, uma linha por site em `.github/ponte.txt`: `auditar <slug> <url>` (até ~25 por push; para mais, vários pushes seguidos). O runner corre o Lighthouse móvel (o mesmo motor do PageSpeed) e abre o site num iPhone simulado. Resultado: `auditorias/dados/<slug>.json` + `<slug>.jpg`. As demos nossas medem-se da mesma forma (`auditar demo-<slug> https://pachecost-demos.netlify.app/<slug>/`) e servem de «o que podia ser».
3. **Escolher** — `python3 agentes/auditoria-sites/gerar.py ranking` escreve `auditorias/RANKING.md` (fraqueza 0–100).
4. **Gerar** — `python3 agentes/auditoria-sites/gerar.py --top 10` (ou `gerar.py <slug> …`): `auditorias/<slug>/auditie-<slug>-ro.pdf` (dono, 3 páginas) e `auditoria-<slug>-pt.pdf` (Tomás, + página de notas com a mensagem RO pronta). Precisa de playwright (`CHROMIUM=<caminho do chrome>` se a versão não bater).
5. **Enviar** — o Tomás manda a mensagem + PDF pelo WhatsApp Business RO. WhatsApp do dono fica «?» (sem prova pública): se falhar, ligar ou visitar.

## Regras de conteúdo

- Só números medidos no próprio dia. A única estatística de fora é a da Google (Think with Google, 2017: abandono vs. tempo de carregamento), com a fonte na página.
- Sem preço no PDF. O dinheiro conta-se na reunião com os dois números do dono (visitas/mês e valor de um cliente).
- A demo de comparação é escolhida pelo tipo de negócio (`DEMO_POR_TIPO` no gerador).
