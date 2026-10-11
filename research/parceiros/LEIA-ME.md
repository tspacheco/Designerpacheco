# Parceiros que indicam (agente 6)

Pedido do Tomás (08/10/2026): encontrar quem vê negócios novos todos os dias (contabilistas, quem abre firmas, gráficas, reclamos luminosos, máquinas registadoras, imobiliárias de espaços comerciais, consultores de fundos, fornecedores HoReCa) em Iași e Faro, e propor-lhes uma parceria, com uma demo como exemplo. **Acordo decidido pelo Tomás a 11/10/2026:** damos primeiro 3 quick wins sem custo; o parceiro mostra o nosso nome (post/story @pachecostudiospt + linha no site); cada trabalho que vier da recomendação dele dá-lhe 15 % do valor da implementação (mensalidades fora), pago até 7 dias depois de o cliente pagar. Texto mestre: `/mnt/project-files/prospecao-instagram/COMISSAO-PARCEIROS.md` (não reescrever; alinhar com ele). Ramo: `claude/parceiros-indicam-4kcnrc`.

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `parceiros.tsv` | Todos os parceiros, um por linha, com estado. Nunca contactar duas vezes o mesmo. |
| `PARCEIROS.md` | Lista para o Tomás, gerada: `python3 research/parceiros/mensagens.py > research/parceiros/PARCEIROS.md` |
| `COMISSAO.md` | O acordo (3 quick wins + nome + 15 %), as contas em lei e o menu de quick wins. |
| `comissoes.tsv` | Cada cliente indicado: parceiro, estado, comissão devida e paga. |
| `proposta/gerar.py` | Proposta A4 (RO, PT Iași, PT Algarve) em HTML e PDF, para mostrar depois dos quick wins. Valores em `VALORES`. |

## Corrida semanal (segunda, 9h53 de Iași)

1. `git fetch origin claude/parceiros-indicam-4kcnrc && git checkout claude/parceiros-indicam-4kcnrc && git pull`.
2. **Escolher 4 a 6 pesquisas novas** no Maps, por tipo e bairro, que ainda não estejam em `ponte/pp-*` (ex.: `contabilitate+Tătărași+Iași`, `expert+contabil+Păcurari+Iași`, `firme+luminoase+Iași`, `tipografie+Nicolina+Iași`, `consultanta+afaceri+Iași`, `contabilidade+Olhão`, `gráfica+Loulé`). Iași primeiro; Algarve 1 pesquisa por semana enquanto o Tomás estiver na Roménia. URL `https://www.google.com/maps/search/<termo>?hl=ro`, pedido `pagina pp-AAAAMMDD-<termo> <url>`.
3. **PONTE.** Pedidos em `.github/ponte.txt`, commit, push, esperar o commit «Ponte: …» (as pesquisas do Maps levam 1 a 2 min cada). Tirar nome, nota e link de cada resultado (`.html`: `a[href*="/maps/place/"]` com `aria-label`).
4. **Fichas.** Abrir as candidatas novas (até 25 por ronda) para ler telefone, morada, site e prova de WhatsApp (`aria-label="Telefon: …"`, `Adresă: …`, `Site: …`). Preferir: nota ≥ 4,3, dezenas de avaliações ou mais, escritório independente (não cadeias nem bancos). WhatsApp «sim» só com prova pública; fixo (02…/03… em RO, 2… em PT) → «não (fixo)».
5. **Juntar 10 novos** a `parceiros.tsv` com estado «por contactar» e gerar `PARCEIROS.md`.
6. **Seguimento.** Quem está «contactado AAAA-MM-DD» há 7 dias ou mais aparece com a mensagem de lembrete (ao 2.º lembrete sem resposta, passa a «sem resposta»). Quem está «quick wins entregues» aparece com a mensagem da parceria (nome + 15 %, com o PDF). A 1.ª mensagem nunca fala de comissão.
7. **Commit + push** e responder no thread: quantos novos, que quick wins estão por entregar, o link `https://github.com/tspacheco/Designerpacheco/blob/claude/parceiros-indicam-4kcnrc/research/parceiros/PARCEIROS.md`, quantos lembretes, e o estado de `comissoes.tsv` (indicações, clientes que pagaram, comissões a pagar).

## Quando o Tomás diz alguma coisa

- «X aceitou» → estado «quick wins em curso» e anotar em `notas` as 3 soluções escolhidas; «entreguei a X» → «quick wins entregues»; depois de ele mostrar o nome → «parceiro». «Recusou / não respondeu» → esse estado. Gerar `PARCEIROS.md` a seguir.
- «X indicou-me Y» → linha em `comissoes.tsv` (estado «indicado»); o cliente indicado entra no caçador como prioridade (demo própria no ramo das demos, pelo coordenador).
- Mudar o acordo → primeiro confirmar o texto mestre em `/mnt/project-files/prospecao-instagram/COMISSAO-PARCEIROS.md`; depois `VALORES` e textos em `proposta/gerar.py`, `COMISSAO.md` e as mensagens de `mensagens.py`.

## O que nunca fazer

- Inventar notas, telefones, nomes de responsáveis ou provas de WhatsApp.
- Prometer prazos de entrega ou resultados na proposta.
- Falar de comissão antes de os 3 quick wins estarem entregues.
- Push noutro ramo que não este.
