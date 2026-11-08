# Assistente do site: Sofia

Chat flutuante «Fala connosco» com o avatar C (anel laranja/dourado/azul-petróleo e bolinha online).

- `widget.html`: estilo + botão + painel + script. Colar antes de `</body>` no site. Trocar `__IMG__` pelo caminho da foto (ex.: `/img/assistente.webp`).
- `teste-sofia.html`: página de teste (abrir no browser).
- `n8n/assistente-site-sofia.json`: fluxo para o n8n do Hetzner (`https://n8n.2.29.109.191.sslip.io`). Webhook `POST /webhook/site-chat` → Claude Haiku 5.5 → `{reply}`.
- As regras da Sofia (o que diz e não diz) estão no nó «Preparar conversa» do n8n.

## Ativar
1. n8n → Workflows → Import from File → `assistente-site-sofia.json`.
2. Nó «Claude» → Credential: escolher a mesma credencial Header Auth do rececionista (x-api-key da Anthropic).
3. Guardar e ligar o interruptor «Active».
4. Abrir `teste-sofia.html` e escrever uma mensagem.

## Segurança
O webhook está aberto a qualquer origem (`*`) para o teste. Quando o site estiver no ar, mudar «Allowed Origins» no nó Webhook e o cabeçalho no nó «Responder ao site» para `https://pachecost.com,https://ro.pachecost.com`.
