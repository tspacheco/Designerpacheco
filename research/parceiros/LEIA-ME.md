# Parceiros que indicam (agente 6)

Pedido do Tomás (08/10/2026): encontrar quem vê negócios todos os dias (contabilistas, quem abre firmas, gráficas, reclamos luminosos, máquinas registadoras, imobiliárias de espaços comerciais, consultores de fundos, fornecedores HoReCa) em Iași e Faro, e convidá-los para o programa de parceiros. **Regras do Tomás (11/10/2026 14h38):** 3 quick wins sem custo ao parceiro; por cada negócio apresentado que comece a trabalhar connosco, 15 % do valor de implementação e 5 % do que nos pagar, a cada 3 meses. Sem valores fixos. Primeiro o incentivo, depois a proposta para assinar. Abordagem «triagem como isca»: hipótese a partir do percurso público, sem afirmar falhas internas, fecho «faça uma triagem connosco», sem minutos. Detalhe em `COMISSAO.md`. Ramo: `claude/parceiros-indicam-4kcnrc`.

**Nada se envia a parceiros até o Tomás dizer «envia»** (`ENVIAR = False` em `mensagens.py`). Até lá, a corrida de segunda só pesquisa.

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `parceiros.tsv` | Todos os parceiros, um por linha, com estado. Nunca contactar duas vezes o mesmo. |
| `PARCEIROS.md` | Lista para o Tomás, gerada: `python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md` |
| `COMISSAO.md` | As regras (3 quick wins, 15 % da implementação, 5 % por trimestre, compromissos do parceiro). |
| `comissoes.tsv` | Cada negócio indicado: parceiro, fase, comissão de 15 % e os 5 % de cada trimestre. |
| `kit/gerar.py` | Kit em duas peças, RO/EN/PT: **incentivo** (4 páginas: 3 quick wins à escolha em 9 áreas amplas, cenários de quanto pode ganhar, porquê, como apresentar; sem mensagem pronta, o parceiro fala com as suas palavras) e **proposta para assinar** (2 páginas: compromissos, comissões, regras, assinaturas). `python3 research/parceiros/kit/gerar.py "Nome"` põe o nome do parceiro. |
| `proposta/` | Caducada a 11/10 (15 % e preços de sites). Não usar. |

## Corrida semanal (segunda, 9h53 de Iași)

1. `git fetch origin claude/parceiros-indicam-4kcnrc && git checkout claude/parceiros-indicam-4kcnrc && git pull`.
2. **Escolher 4 a 6 pesquisas novas** no Maps, por tipo e bairro, que ainda não estejam em `ponte/pp-*` (ex.: `contabilitate+Tătărași+Iași`, `expert+contabil+Păcurari+Iași`, `firme+luminoase+Iași`, `tipografie+Nicolina+Iași`, `consultanta+afaceri+Iași`, `contabilidade+Olhão`, `gráfica+Loulé`). Iași primeiro; Algarve 1 pesquisa por semana enquanto o Tomás estiver na Roménia. URL `https://www.google.com/maps/search/<termo>?hl=ro`, pedido `pagina pp-AAAAMMDD-<termo> <url>`.
3. **PONTE.** Pedidos em `.github/ponte.txt`, commit, push, esperar o commit «Ponte: …» (as pesquisas do Maps levam 1 a 2 min cada). Tirar nome, nota e link de cada resultado (`.html`: `a[href*="/maps/place/"]` com `aria-label`).
4. **Fichas.** Abrir as candidatas novas (até 25 por ronda) para ler telefone, morada, site e prova de WhatsApp (`aria-label="Telefon: …"`, `Adresă: …`, `Site: …`). Preferir: nota ≥ 4,3, dezenas de avaliações ou mais, escritório independente (não cadeias nem bancos). WhatsApp «sim» só com prova pública; fixo (02…/03… em RO, 2… em PT) → «não (fixo)».
5. **Juntar 10 novos** a `parceiros.tsv` com estado «por contactar» e gerar `PARCEIROS.md`.
6. **Seguimento.** Quem está «contactado AAAA-MM-DD» há 7 dias ou mais aparece com a mensagem de lembrete (ao 2.º lembrete sem resposta, passa a «sem resposta»). Só com `ENVIAR = True`.
7. **Commit + push** e responder no thread: quantos novos, o link `https://github.com/tspacheco/Designerpacheco/blob/claude/parceiros-indicam-4kcnrc/research/parceiros/PARCEIROS.md`, quantos lembretes, e o estado de `comissoes.tsv` (indicações, implementações, comissões a pagar).

## Quando o Tomás diz alguma coisa

- «Envia» → `ENVIAR = True` em `mensagens.py` e gerar `PARCEIROS.md`.
- «X marcou reunião» → «reunião marcada» (levar o incentivo); «X aceitou» → «parceiro» (proposta com o nome dele, para assinar). «Recusou / não respondeu» → esse estado.
- «X indicou-me Y» → linha em `comissoes.tsv` (fase «indicado»); Y entra na auditoria como prioridade, pelo coordenador.
- Mudar as regras → `COMISSAO.md`, os textos de `kit/gerar.py` e as mensagens de `mensagens.py`, no mesmo commit.

## O que nunca fazer

- Inventar notas, telefones, nomes de responsáveis ou provas de WhatsApp.
- Pôr preços fixos, prometer resultados ou prazos, ou falar de sites como produto.
- Afirmar falhas internas do parceiro sem dados, ou pedir reuniões com minutos.
- Enviar a proposta para assinar antes de o parceiro ver o incentivo.
- Push noutro ramo que não este.
