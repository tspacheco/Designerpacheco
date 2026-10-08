# Parceiros que indicam (agente 6)

Pedido do Tomás (08/10/2026): encontrar quem vê negócios novos todos os dias (contabilistas, quem abre firmas, gráficas, reclamos luminosos, máquinas registadoras, imobiliárias de espaços comerciais, consultores de fundos, fornecedores HoReCa) em Iași e Faro, e propor-lhes uma comissão por cliente indicado, com uma demo como exemplo. Ramo: `claude/parceiros-indicam-4kcnrc`.

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `parceiros.tsv` | Todos os parceiros, um por linha, com estado. Nunca contactar duas vezes o mesmo. |
| `PARCEIROS.md` | Lista para o Tomás, gerada: `python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md` |
| `COMISSAO.md` | A regra da comissão e a conta (proposta por omissão; decisão do Tomás). |
| `comissoes.tsv` | Cada cliente indicado: parceiro, estado, comissão devida e paga. |
| `proposta/gerar.py` | Proposta A4 (RO, PT Iași, PT Algarve) em HTML e PDF. Valores em `VALORES`. |

## Corrida semanal (segunda, 9h53 de Iași)

1. `git fetch origin claude/parceiros-indicam-4kcnrc && git checkout claude/parceiros-indicam-4kcnrc && git pull`.
2. **Escolher 4 a 6 pesquisas novas** no Maps, por tipo e bairro, que ainda não estejam em `ponte/pp-*` (ex.: `contabilitate+Tătărași+Iași`, `expert+contabil+Păcurari+Iași`, `firme+luminoase+Iași`, `tipografie+Nicolina+Iași`, `consultanta+afaceri+Iași`, `contabilidade+Olhão`, `gráfica+Loulé`). Iași primeiro; Algarve 1 pesquisa por semana enquanto o Tomás estiver na Roménia. URL `https://www.google.com/maps/search/<termo>?hl=ro`, pedido `pagina pp-AAAAMMDD-<termo> <url>`.
3. **PONTE.** Pedidos em `.github/ponte.txt`, commit, push, esperar o commit «Ponte: …» (as pesquisas do Maps levam 1 a 2 min cada). Tirar nome, nota e link de cada resultado (`.html`: `a[href*="/maps/place/"]` com `aria-label`).
4. **Fichas.** Abrir as candidatas novas (até 25 por ronda) para ler telefone, morada, site e prova de WhatsApp (`aria-label="Telefon: …"`, `Adresă: …`, `Site: …`). Preferir: nota ≥ 4,3, dezenas de avaliações ou mais, escritório independente (não cadeias nem bancos). WhatsApp «sim» só com prova pública; fixo (02…/03… em RO, 2… em PT) → «não (fixo)».
5. **Juntar 10 novos** a `parceiros.tsv` com estado «por contactar» e gerar `PARCEIROS.md`.
6. **Seguimento.** Quem está «contactado AAAA-MM-DD» há 7 dias ou mais aparece com a mensagem de lembrete. Ao 2.º lembrete sem resposta, passa a «sem resposta».
7. **Commit + push** e responder no thread: quantos novos, o link `https://github.com/tspacheco/Designerpacheco/blob/claude/parceiros-indicam-4kcnrc/research/parceiros/PARCEIROS.md`, quantos lembretes, e o estado de `comissoes.tsv` (indicações, clientes que pagaram, comissões a pagar).

## Quando o Tomás diz alguma coisa

- «X aceitou / recusou / não respondeu» → atualizar `estado` em `parceiros.tsv` e gerar `PARCEIROS.md`.
- «X indicou-me Y» → linha em `comissoes.tsv` (estado «indicado»); o cliente indicado entra no caçador como prioridade (demo própria no ramo das demos, pelo coordenador).
- Mudar a comissão → `VALORES` em `proposta/gerar.py`, correr o gerador, atualizar `COMISSAO.md` e as frases de `mensagens.py`.

## O que nunca fazer

- Inventar notas, telefones, nomes de responsáveis ou provas de WhatsApp.
- Prometer prazos de entrega ou resultados na proposta.
- Push noutro ramo que não este.
