# Rececionista IA — protótipo

Página: https://claude.ai/artifact/GjvzuuhAgFmnStHVKG3Snv (ficheiro: `index.html`, um só ficheiro).

## O que faz
- Telemóvel com uma conversa de atendimento. Abre com «chamada perdida» e a mensagem automática que se apresenta como assistente automático.
- 3 negócios fictícios (barbearia, restaurante, oficina, dados de exemplo em `NEGOCIOS` no topo do script) e 3 línguas (RO, PT, EN). Responde na língua em que o cliente escreve.
- Marca numa agenda fictícia (horas ocupadas geradas de forma fixa por dia), mostra o cartão da marcação e a marcação aparece em «O que o dono vê».
- O que não está na lista aprovada → passa ao dono (alerta no painel; o dono pode responder dali e a resposta entra na conversa). Grupos acima de 8, queixas e «quero falar com uma pessoa» também passam.
- STOP para tudo.
- As regras são as da automatização `receptionist` do site (`conteudo/*.json`, ramo kztskg) e da secção 16 do PLAYBOOK.

## Dois cérebros
1. **IA ao vivo**: dentro do claude.ai a página usa a capacidade `sample` (Claude, nível «quick») com 3 ferramentas da página: `ver_horas_livres`, `marcar`, `passar_a_pessoa`. As instruções estão em `instrucoes()`. Gasta a utilização de quem abre a página; a 1.ª mensagem pede autorização.
2. **Modo guião**: regras por palavras-chave, sem IA e sem custo (`responderGuiao`). Entra sozinho fora do claude.ai ou se a IA falhar. O botão do modo troca entre os dois.

## Próximos passos
- Mini telemóvel no site (Soluções → Rececionista): quem integra é o thread do site. No site não há `sample`; arranca em modo guião (grátis, sem abuso). IA a sério no site = função Netlify com a API da Claude e a chave numa variável de ambiente (nunca no repositório).
- WhatsApp, telefone e agenda reais: n8n (WhatsApp Cloud API + Google Calendar), reaproveitando as mesmas instruções e as 3 ferramentas.
