# Prospeção por e-mail (ligada ao n8n)

Estado: à espera do plano do Tomás (11/10/2026).

## Já preparado
- Ramo: `claude/pesquisa-emails-n8n-s29643`.
- Pasta: `research/emails/` — uma lista por dia em `AAAA-MM-DD.csv`.
- Fontes de negócios: listas do caçador (`research/cacador/` no ramo `claude/cacador-diario-nkiz36`) e lotes 1–4 de Iași.
- Sites de clientes lêem-se pela PONTE (`.github/ponte.txt` → `ponte/relatorio.txt`).

## Formato das listas (o n8n lê o CSV pelo link raw do GitHub)
`negocio,cidade,nicho,site,email,fonte_email,lingua,demo,estado`

- `email`: só endereços publicados pelo próprio negócio (site, Google, página pública). Sem prova → vazio.
- `fonte_email`: URL onde o e-mail aparece.
- `estado`: `por-enviar` | `enviado` | `respondeu` | `nao-enviar`.

## Regras
- Nada de credenciais no repositório: SMTP/Gmail e URL do n8n ficam só no n8n (ou em Secrets do GitHub, colados pelo Tomás).
- Envio com intervalo e saudação a variar, como no WhatsApp.
- Cada e-mail tem forma de sair da lista (RGPD).
