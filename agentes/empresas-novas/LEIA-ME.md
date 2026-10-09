# Agente 7: empresas acabadas de abrir em Iași

Pedido do Tomás (08/10/2026, ideia 7 do thread «Ideias de agentes para leads»): ler os registos de empresas novas,
ficar com as da zona dele e preparar a mensagem «abriste agora, aqui está um site para ti». Ramo `claude/empresas-novas-43xm0c`.

## Fonte (testada a 08/10)

- Daqui (threads) nenhum registo se lê: ONRC, data.gov.ro, ANAF, termene, listafirme dão 403 no proxy.
- **API pública da ANAF** (`PlatitorTvaRest/v9/tva`), chamada do GitHub: grátis, sem conta. Os CUI são dados por ordem
  e o último algarismo é de controlo, por isso percorre-se a fila a partir do último CUI visto. Cada empresa traz
  nome, n.º do Registo Comercial, morada da sede, CAEN, data de registo e, em ~60 %, telefone declarado.
  A ANAF mostra a empresa no próprio dia; o CAEN chega uns dias depois (o recolher volta a perguntar até chegar).
- Volume real: ~9 000 entidades/dia no país se contarmos tudo (CUI), ~25/dia no distrito de Iași, das quais **2 a 3
  por dia** são negócio local com clientes (beleza, café, restaurante, oficina, loja, clínica…).
- Alternativas vistas: companero.ro (lista ONRC diária, lê-se pela ponte, exportação paga: 500 créditos grátis);
  data.gov.ro (dados abertos ONRC, mensais, timeout pelo runner); publicacoes.mj.pt e racius.com (Portugal, para o Algarve depois).

## Ficheiros

| Ficheiro | Para quê |
|---|---|
| `recolher.py` | Corre no GitHub (`.github/workflows/empresas-novas.yml`): lê a fila de CUI desde a última corrida, guarda Iași em `dados/iasi-AAAA-MM-DD.json`. |
| `dados/estado.json` · `dados/vistos.txt` | Último CUI lido e CUI já vistos (não repetir). |
| `lista.py` | Faz `listas/AAAA-MM-DD.md` para o Tomás: filtra Iași, últimos 14 dias, ativas, com n.º do Registo Comercial e CAEN de negócio local; mensagem em romeno + PT, demo de exemplo do mesmo ramo, WhatsApp/SMS. |
| `listas/listadas.txt` | CUI já postos numa lista (cada empresa aparece uma vez). |

## Corrida diária (rotina, seg–sex 16h47 de Iași)

Às 8h47 a ANAF ainda não tem as empresas do dia anterior (09/10: só 50 CUI novos no país, 0 em Iași); a meio da tarde já tem as do próprio dia (08/10 às 16h: registadas a 08/10 presentes).

1. `git fetch origin claude/empresas-novas-43xm0c && git checkout claude/empresas-novas-43xm0c && git pull`.
2. Mudar a linha de comentário com a data em `.github/empresas-novas.txt` (argumentos vazios = continuar do estado),
   commit, push. Esperar o commit «Empresas novas: recolha …» (3–8 min; se falhar, ver os logs do workflow
   `empresas-novas` com `mcp__github__get_job_logs`).
3. `python3 agentes/empresas-novas/lista.py`. Se der 0, não há lista nem mensagem nesse dia.
4. Rever a lista à mão (2 min): tirar o que não é negócio local apesar do CAEN (ex.: «Activ8-Cpp» com CAEN de café pode ser
   holding), e duplicados (SRL + sede secundária).
5. Commit + push de `listas/` e `dados/`. Responder no thread «Agente 7» com o número e o link
   `https://github.com/tspacheco/Designerpacheco/blob/claude/empresas-novas-43xm0c/agentes/empresas-novas/listas/AAAA-MM-DD.md`.

## Regras

- Telefone vem do registo: pode ser do contabilista; WhatsApp sempre «?» (regra do PLAYBOOK §11.8). Fixo → só chamada.
- A sede muitas vezes é casa ou escritório do advogado/contabilista: visita só se o Maps mostrar o espaço.
- PFA/II/IF têm o nome do dono: a mensagem diz «firma dumneavoastră», nunca o nome da pessoa como marca.
- Sem preço na mensagem (500 € ≈ 2.500 lei + 75 €/mês ≈ 375 lei fala-se depois). Sem números inventados.
- Não fazer push no ramo das demos. Demo própria para uma empresa nova: pedir ao coordenador (passa ao caçador).
