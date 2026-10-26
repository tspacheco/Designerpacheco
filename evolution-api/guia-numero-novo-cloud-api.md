# Número novo na WhatsApp Cloud API (oficial Meta) → n8n do Hetzner

*Pacheco Studios, 26 out 2026. Para o número novo (número C). O 723 continua na Evolution em modo sombra.*

---

## 0. Antes de começar (importante)

- **Não instales o número novo na app WhatsApp nem no WhatsApp Business.** Um número que vai para a Cloud API tem de estar livre. Se já o ativaste na app: app → Definições → Conta → **Apagar conta**, esperar uns minutos e só depois seguir.
- O cartão tem de estar no telemóvel para receber o **SMS ou a chamada** com o código.
- Custo: responder a quem escreve primeiro é **grátis** durante 24 h (72 h se a pessoa vier de um anúncio Meta→WhatsApp). Só pagam as mensagens que nós iniciamos com modelo aprovado.
- Sem verificação da empresa, a Meta deixa iniciar conversas com até 250 pessoas por dia. Responder a quem escreve não tem limite.

## 1. App na Meta (10 min)

1. **developers.facebook.com** → My Apps → **Create app** → caso de uso **«Connect with customers through WhatsApp»** (ou tipo **Business**).
2. Liga a app ao portefólio empresarial **Pacheco Studios**.
3. Na app: **WhatsApp → API Setup**. A Meta cria uma conta WhatsApp Business (WABA) e dá um número de teste. Ignora o de teste.

## 2. Juntar o número novo (10 min)

1. **API Setup → Add phone number**.
2. Nome a mostrar: **Pacheco Studios**. Categoria: Serviços profissionais. Descrição curta.
3. Introduz o número, escolhe SMS ou chamada e mete o código.
4. Se pedir, define o **PIN de 6 dígitos** (verificação em dois passos) e guarda-o no gestor de palavras-passe.
5. Aponta o **Phone number ID** e o **WhatsApp Business Account ID**, que aparecem em API Setup. Não são segredo e podes mandar-mos.

> Se o número ficar com o estado «Pending» ou «Not registered», diz-me: há um passo de registo por API (`/register` com o PIN) que fazemos juntos.

## 3. Token permanente (5 min)

O token que aparece em API Setup expira em 24 h. Para o bot usamos um que não expira:

1. **business.facebook.com → Definições → Utilizadores → Utilizadores do sistema → Adicionar**: nome `n8n-bot`, função **Admin**.
2. **Atribuir ativos**: a app (controlo total) e a conta WhatsApp (controlo total).
3. **Gerar token** → app escolhida → validade **Nunca** → permissões `whatsapp_business_messaging` e `whatsapp_business_management`.
4. Copia o token **só para o gestor de palavras-passe**. **Não mo envies.**

## 4. Credencial no n8n

n8n → **Credentials → Add → Header Auth**:
- Nome da credencial: `Meta WhatsApp`
- Name: `Authorization`
- Value: `Bearer ` + o token (com um espaço depois de Bearer)

## 5. Webhook (a Meta → o nosso n8n)

Eu preparo o fluxo n8n **«Rececionista Meta»** com o caminho `meta-whatsapp`. Quando estiver importado e publicado:

1. Na app: **WhatsApp → Configuration → Webhook → Edit**
   - Callback URL: `https://n8n.2.29.109.191.sslip.io/webhook/meta-whatsapp`
   - Verify token: uma palavra que escolhes (por exemplo `pacheco-meta-2026`), igual à que estiver no fluxo
   - **Verify and save**
2. Em **Webhook fields**, faz **Subscribe** ao campo **messages**.

## 6. Como convive com o 723 (modo sombra)

| | 723 (Evolution) | Número novo (Cloud API) |
|---|---|---|
| Ligação | Dispositivo ligado (não oficial) | API oficial da Meta |
| Risco de bloqueio | Existe; só responder | Baixo, se seguirmos as regras da Meta |
| Rascunhos | No teu PT | **No teu PT, na mesma conversa**, marcados com «📱 Meta» |
| Aprovação | Citar com OK / X / texto | Igual: o fluxo sabe por onde enviar cada um |
| Treino | Os exemplos são partilhados pelos dois números | |

- O bot continua **em sombra**: nada é enviado sem o teu OK, até ao balanço de domingo, 1 nov.
- Mais tarde podemos apontar o **anúncio Meta→WhatsApp** para o número novo. Assim as conversas do anúncio entram pela via oficial e ficam com a janela grátis de 72 h.
- A **Magic Key** seguirá este mesmo caminho oficial, na conta Meta do Jeorge (o cliente fica sempre com as contas).

## 7. O que me mandas quando acabares

- Phone number ID
- WhatsApp Business Account ID
- O verify token que escolheste

(O token permanente fica só contigo, na credencial do n8n.)
