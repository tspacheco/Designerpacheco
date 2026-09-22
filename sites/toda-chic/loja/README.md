# Loja Toda Chic — stock, encomendas e MB WAY

O site que já temos (`index.html`) passa a ser a loja. Não é preciso WordPress nem WooCommerce: a loja fala com uma API pequena (a mesma em teste e em produção), a dona gere tudo no `painel.html` pelo telemóvel, e o pagamento MB WAY é a Stripe.

> Sobre o WooCommerce: é um plugin gratuito que se instala num WordPress — ninguém "contacta" ninguém; o que viste foi a página comercial da Woo (alojamento pago). Não precisamos dele: obrigava a refazer o design como tema WordPress. Este caminho mantém o nosso ficheiro único.

## As peças e para que serve cada uma

| Aplicação | Papel | Quem mexe |
|---|---|---|
| **`index.html`** (o site) | A loja. Lê o catálogo e o stock da API, cria a encomenda, manda a cliente pagar. Sem API, funciona como montra (catálogo embutido). | Ninguém depois de publicado |
| **`painel.html`** | O painel da dona: encomendas (pagas → enviadas), stock por cor, peças novas com foto. Uma palavra-passe. | **A dona**, todos os dias |
| **`loja/servidor-teste.js`** | Servidor de teste no teu PC. Simula a API e o MB WAY. Serve para testar tudo hoje e para mostrar à dona. | Tu, agora |
| **Supabase** | A base de dados e a API de produção (peças, cores/stock, encomendas) + as 3 funções (`loja`, `painel`, `stripe-webhook`) + as fotos das peças novas. Plano gratuito chega. | Tu, uma vez; depois só a mensalidade |
| **Stripe** | O pagamento: Checkout alojado com **MB WAY** (e cartão). Avisa a nossa função quando o pagamento entra. Modo de teste imediato. | Tu configuras; a dona vê o dinheiro no painel Stripe |
| **Vendus / InvoiceXpress** | A fatura certificada pela AT. **Ainda não está ligado** — a Stripe não emite faturas portuguesas. Liga-se no webhook quando a dona disser que software o contabilista usa. | Contabilista + tu |

O fluxo de uma venda:

```
cliente escolhe → saco → #/pagar (nome, telemóvel, morada)
   → POST /encomendas      reserva o stock 60 min, cria a encomenda "pendente", abre o Stripe Checkout
   → cliente confirma MB WAY na app
   → Stripe → /stripe-webhook   marca "paga", desconta o stock de vez
   → site #/encomenda/<token>   "Pagamento recebido"     painel: aparece em "A tratar"
   → dona embala, marca "enviada"
   (sem pagamento em 60 min → "expirada", o stock volta sozinho)
```

## 1 · Testar já, no teu PC (5 minutos)

Precisas do Node (nodejs.org, versão 18 ou mais).

```bash
cd sites/toda-chic
node loja/servidor-teste.js
```

Abre:
- **Loja:** http://localhost:8080 — escolhe uma peça → saco → *Pagar com MB WAY* → preenche → *Pagar*. Ao fim de 6 segundos aparece "Pagamento recebido" e o stock dessa cor desceu.
- **Painel:** http://localhost:8080/painel.html — palavra-passe `123` (só no teste; em produção é o segredo `PAINEL_SENHA`). A encomenda está em "A tratar"; marca *enviada*; muda um stock; põe uma peça nova com foto e vê-a aparecer na loja.
- Para testar um pagamento **falhado**, usa um telemóvel terminado em `0` (ex.: 912345670): a encomenda fica "falhada" e o stock volta.

Os dados ficam em `loja/dados/loja.json`; apaga-o para voltar ao catálogo inicial. Isto é exatamente o comportamento que a produção vai ter — só troca a simulação pela Stripe.

## 2 · Produção: Supabase + Stripe (1 hora, uma vez)

### Supabase (base de dados + API)

1. supabase.com → *New project* (região EU, Frankfurt). Guarda a palavra-passe da base de dados.
2. *SQL Editor* → cola e corre `loja/supabase/schema.sql` (tabelas, regras de stock, cron das reservas, bucket de fotos).
3. Gera e corre o catálogo: `python3 loja/supabase/seed.py` → cola `seed.sql` no SQL Editor. (72 peças, stock das fichas.)
4. Instala a CLI: `npm i -g supabase` → `supabase login` → `supabase link --project-ref <ref>`.
5. Segredos das funções:
   ```bash
   supabase secrets set STRIPE_SECRET_KEY=sk_test_...  STRIPE_WEBHOOK_SECRET=whsec_...  PAINEL_SENHA='uma-frase-longa-que-a-dona-guarda'
   ```
6. Publica as funções (a partir de `sites/toda-chic/loja`):
   ```bash
   supabase functions deploy loja --no-verify-jwt
   supabase functions deploy painel --no-verify-jwt
   supabase functions deploy stripe-webhook --no-verify-jwt
   ```
   A API fica em `https://<ref>.supabase.co/functions/v1`.

### Stripe (MB WAY)

1. Conta Stripe da **dona** (é ela que recebe o dinheiro; precisa de NIF/atividade e IBAN). Começa em modo de teste.
2. *Settings → Payment methods* → ativar **MB WAY** (disponível para contas em Portugal) e cartão. O Checkout escolhe sozinho o que mostrar.
3. *Developers → API keys* → a chave secreta vai para o `STRIPE_SECRET_KEY` acima.
4. *Developers → Webhooks → Add endpoint*: URL `https://<ref>.supabase.co/functions/v1/stripe-webhook`, eventos `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `checkout.session.expired`. O *signing secret* vai para `STRIPE_WEBHOOK_SECRET`.
5. Testar: em modo de teste, o Checkout mostra MB WAY com um número de teste e confirma sem app. Faz uma compra, vê a encomenda passar a "paga" no painel e o stock descer.
6. Quando o contabilista confirmar a faturação, trocar para as chaves *live* e repetir o webhook em modo live.

### Ligar o site e o painel à API

Antes de `</head>` no `index.html` e no `painel.html` (ou no `netlify.toml` via inject), uma linha:

```html
<script>window.LOJA_API="https://<ref>.supabase.co/functions/v1"</script>
```

Sem esta linha o site continua a funcionar como montra (catálogo embutido, botão de pagar em pré-visualização). Publicar os dois ficheiros + `media/` no Netlify/Hostinger como até aqui. O painel fica em `/painel.html` — não está ligado de lado nenhum e está marcado `noindex`; a proteção é a palavra-passe.

## 3 · O que ainda falta para vender a sério

- **Fatura certificada (AT):** ligar Vendus/InvoiceXpress no `stripe-webhook` depois de `marcar_paga`. Depende do software do contabilista.
- **Portes:** hoje é "a confirmar" e 0 € no total. Quando a dona decidir (valor fixo / grátis acima de X €), é uma linha no `criar_encomenda` e um `line_item` extra na Stripe.
- **E-mail à cliente:** a Stripe já manda o recibo do pagamento; o e-mail "encomenda enviada" pode sair do painel (Resend, 5 min) — para já a dona avisa pelo botão WhatsApp do painel.
- **Palavra-passe do painel:** é uma só, longa, guardada no telemóvel da dona. Chega para uma loja de uma pessoa; se um dia houver mais gente, passa-se para Supabase Auth.
- Isto foi **testado ponta-a-ponta no servidor local** (compra, falha, expiração, painel, peça nova). As funções Supabase e a Stripe seguem o mesmo contrato mas **não puderam ser executadas nesta sessão** (rede bloqueada) — o primeiro deploy pode pedir um ajuste pequeno; testa em modo de teste antes de passar a live.

## Contrato da API (igual no teste e na produção)

| Método | Rota | Corpo → resposta |
|---|---|---|
| GET | `/catalogo` | → `{categorias, estacoes, pecas[]}` com `cores[].stock` já sem reservas |
| POST | `/encomendas` | `{linhas:[{peca,cor,tam,qt}], cliente:{nome,telemovel,email,morada,cp,localidade,nif}, retorno}` → `{token,id,total,estado,checkoutUrl}` |
| GET | `/encomendas/:token` | → `{id,estado,total,linhas,motivo}` |
| POST | `/stripe-webhook` | (Stripe) |
| GET | `/painel/encomendas` | cabeçalho `X-Painel` → lista |
| PATCH | `/painel/encomendas/:id` | `{estado:'enviada'|'cancelada'}` |
| GET | `/painel/pecas` | → peças com `cores[].stock/reservado` |
| PATCH | `/painel/stock` | `{peca,cor,stock}` → `{stock,disponivel}` |
| POST | `/painel/pecas` | `{nome,preco,precoAntigo,cat,estacao,tam,tamanhos,desc,cores:[{nome,hex,stock,fotoBase64}]}` |
| PATCH | `/painel/pecas/:id` | campos a mudar (`ativo:false` retira a peça) |

Estados de uma encomenda: `pendente → paga → enviada`, ou `pendente → falhada | expirada | cancelada`.
