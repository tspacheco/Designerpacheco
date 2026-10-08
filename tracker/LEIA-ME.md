# Tracker das demos

Página (Artifact, com base de dados): https://claude.ai/artifact/NDnUhrKktvWHT2tvzMf1wT

## Como funciona

| Etapa | De onde vem |
|---|---|
| Por enviar / Enviado / Respondeu / Reunião / Sem interesse / Cliente | O Tomás toca no negócio na página e escolhe o estado (fica com a data). |
| Abriu a demo (n.º de visitas, 1.ª e última data) | Contador em cada demo (`contador-demos.patch` no gerar.py das demos) → GoatCounter → workflow `tracker-demos.yml` → `tracker/aberturas.json` → o Claude escreve na página. |

- Cada demo conta-se pelo caminho `/demo/<curto>/` (igual em pachecost.com/demo/, demo.pachecost.com e pachecost-demos.netlify.app). Só o `index.html` conta; o `pt.html` é do Tomás.
- Não contam: navegadores automáticos (ponte, testes) e quem abriu um link de demo com `#nao-contar` no fim (o Tomás faz isso uma vez em cada telemóvel e PC, ex. `https://pachecost.com/demo/fika/#nao-contar`).
- Aberturas antes do contador entrar no ar não ficam registadas.

## Rotina diária (19h de Iași)

1. `python3 tracker/sincronizar.py` (lista de negócios a partir do DEMOS do gerar.py e dos ficheiros de lote; demos novas entram como «Por enviar»).
2. Push de `.github/tracker.txt` (uma data nova) → o workflow lê o GoatCounter e faz commit de `tracker/aberturas.json`; `git pull` quando aparecer.
3. Ler a coleção `negocios` do Artifact, criar os negócios que faltam e atualizar `visitas`, `primeira`, `ultima` (sem mexer no estado nem na nota); `meta/geral` com `lido_em` e `erro`.
4. Relatório curto no thread «Tracker das demos»: funil (enviados, abriram, responderam, reuniões, sem interesse, clientes, com %), e a lista «abriram e não responderam» para o follow-up.

## Falta (Tomás)

- Token do GoatCounter: pachecost.goatcounter.com → Settings → API → New token, marcar «Read statistics».
- Guardá-lo no GitHub: repositório Designerpacheco → Settings → Secrets and variables → Actions → New repository secret, nome `GOATCOUNTER_TOKEN`.
