# Agente 8 — Avaliações Google com queixas (Iași)

Pedido do Tomás (08/10/2026, ideia 8 do thread «Ideias de agentes para leads»): encontrar negócios cujos clientes
se queixam, nas avaliações Google, de **telefone sem resposta**, **mensagens sem resposta** ou **marcações/encomendas
que falham**, e preparar a mensagem da consultoria de IA a citar essa queixa real. São leads para a **auditoria
grátis** e a reunião de 20 minutos, não para o site. Ramo: `claude/avaliacoes-queixas-m7qdst`.

## Peças

| Ficheiro | Para quê |
|---|---|
| `.github/workflows/avaliacoes.yml` | Corre no GitHub (a rede dos threads não chega ao Maps). Dispara com push de `.github/avaliacoes.txt`, que tem o comando numa linha. Faz commit «Avaliações: recolha …» no mesmo ramo. |
| `recolher.py` | Abre as pesquisas do Maps, junta fichas novas (fora de `dados/vistos.txt`, com ≥ 15 avaliações) e lê de cada uma: nota, nº de avaliações, categoria, telefone, morada, site, prova de WhatsApp e as avaliações por 3 vias: mais recentes, piores, e pesquisa interna por «telefon», «răspuns», «mesaj», «programare». Grava `dados/AAAA-MM-DD.json`. ~50 s por ficha; 90 fichas ≈ 75 min. |
| `queixas.py` | Detetor (regex em romeno sem diacríticos) das 3 dores. Testar uma frase: `python3 queixas.py "Nu răspund la telefon"`. |
| `lista.py` | `python3 lista.py dados/AAAA-MM-DD.json` → `listas/AAAA-MM-DD.md` (mensagens RO com WhatsApp/SMS + versão PT) e `candidatos/AAAA-MM-DD.json` (frases a traduzir). |
| `traducoes/AAAA-MM-DD.json` | `{id_avaliacao: "tradução PT da frase"}`, escrito pelo Claude depois de ler os candidatos; volta a correr o `lista.py`. |
| `pesquisas/AAAA-MM-DD.txt` | As pesquisas do dia, uma por linha. |

## Corrida (segundas e quintas, 9h37 de Iași)

1. `git fetch origin claude/avaliacoes-queixas-m7qdst && git checkout claude/avaliacoes-queixas-m7qdst && git pull`.
2. Escrever `pesquisas/AAAA-MM-DD.txt` com 10 a 12 pesquisas **ainda não feitas** (ver as anteriores em `pesquisas/`): ramos onde o telefone e as mensagens são a porta de entrada (dentistas, clínicas, veterinários, salões, unhas, service auto, vulcanizare, instaladores, eletricistas, limpezas, curățătorie, pizzerias com entrega, autoescolas, fisioterapia, ginásios pequenos, fotógrafos, mudanças, reparações) e bairros/comunas (Tătărași, Nicolina, Alexandru cel Bun, Dacia, Galata, Păcurari, Copou, Canta, CUG, Valea Lupului, Miroslava, Tomești, Bucium).
3. `echo 'recolher.py --pesquisas pesquisas/AAAA-MM-DD.txt --por-pesquisa 15 --max-fichas 90' > .github/avaliacoes.txt`, commit, push. Esperar o commit «Avaliações: recolha» (até ~80 min: `until git fetch -q origin claude/avaliacoes-queixas-m7qdst && git log origin/claude/avaliacoes-queixas-m7qdst -1 --format=%s | grep -q 'Avaliações: recolha'; do sleep 30; done`, em background). Ver `dados/ultima-corrida.txt`: se as vias dizem «falhou» em todas as fichas, o Maps mudou os seletores; corrigir `recolher.py` com uma ficha de teste antes de repetir.
4. `python3 lista.py dados/AAAA-MM-DD.json`. Ler `candidatos/AAAA-MM-DD.json` e, para cada frase, **confirmar no texto completo** que a queixa é mesmo sobre o negócio (não sobre outro sítio, nem ironia, nem já resolvida pelo dono na resposta). As que não servirem: tirar a ficha do JSON do dia. Escrever `traducoes/AAAA-MM-DD.json` e correr o `lista.py` outra vez.
5. Commit + push. Responder no thread: quantas fichas lidas, quantos leads, os 3 mais fortes numa linha cada, e o link `https://github.com/tspacheco/Designerpacheco/blob/claude/avaliacoes-queixas-m7qdst/agentes/avaliacoes-queixas/listas/AAAA-MM-DD.md`.

## Regras

- Citar só frases reais, palavra por palavra, com a data relativa que o Google mostra. Nunca o nome de quem escreveu.
- Sem números inventados nem preços na mensagem (o preço fala-se na reunião: sistemas ~250 € + ~50 €/mês, site 500 € + 75 €/mês).
- WhatsApp «sim» só com link wa.me na ficha; senão «?» (link WhatsApp + SMS); fixo (02…/03…) → ligar ou visita.
- Negócios com site fraco também servem: aqui a venda é a auditoria.
- Excluir cadeias e franchisings (o dono não está em Iași).
