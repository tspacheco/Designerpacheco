# Modelo de site romeno — como usar

Base para sites de clientes na Roménia. **Não é um site pronto**: é a camada legal e estrutural já resolvida. Cada cliente continua a precisar da sua assinatura visual e fonte display novas (PLAYBOOK secções 5 e 6) e do processo NÍVEL 10K.

## O que já vem resolvido

| Obrigação romena | Onde está no modelo |
|---|---|
| Identificação da empresa visível: denumire, **CUI**, **Nr. Reg. Com.**, sede (Lei 365/2002) | Rodapé, coluna 3 |
| Pictograma **ANPC–SAL** 250×50 com link para anpc.ro/ce-este-sal/ (Ordem ANPC 449/2022) — substitui o Livro de Reclamações | Rodapé, por baixo da identificação |
| Pictograma SOL | **Não pôr** — deixou de ser obrigatório (Ordem ANPC 270/2026) |
| Consentimento de cookies com **Accept** e **Refuz** com o mesmo peso (Lei 506/2004 + RGPD) | Caixa em baixo; o mapa do Google só carrega depois de aceitar |
| Política de confidențialitate, cookie-uri, termeni — em romeno (Lei 500/2004) | Secção "Informații legale" (acordeões) |
| Encomenda direta sem comissão de apps (argumento de venda) | Secção "Comandă direct" com telefone e WhatsApp + links Glovo/Wolt/Bolt Food |

## Trocar por cliente

1. Tudo o que está entre `{{ }}` — procurar `{{` no ficheiro até não sobrar nenhum.
2. `lang="ro"` fica. JSON-LD: `addressCountry: "RO"`, telefone `+40…`.
3. Tokens `:root` (cores e fontes) → direção de arte do cliente.
4. Preços **em lei, com IVA incluído**. Sem preço confirmado → etiqueta `de confirmat` (é o "a confirmar" romeno — regra HONEST-DATA).
5. Rating Google só se for ≥ 4,2; resumir as avaliações, nunca copiar.
6. Tirar as apps de entrega em que o cliente não está.
7. **Na versão de produção:** remover o banner "Prezentare Pacheco Studios" e todas as etiquetas `de confirmat`.

## Pasta `media/`

- `hero.jpg`, `despre.jpg` — fotos do cliente (o fundo SVG aparece sempre por baixo).
- `anpc-sal.png` — **tem de ser o pictograma oficial** descarregado de anpc.ro (secção SAL). Não desenhar uma imitação. Sem o ficheiro, aparece um botão de texto com o mesmo link.

## Validação (diferente dos sites portugueses)

```bash
f=index.html
grep -c 'lang="ro"' $f            # 1
grep -c '<h1' $f                  # 1
grep -c 'anpc.ro/ce-este-sal' $f  # ≥ 1 (não livroreclamacoes)
grep -c 'CUI' $f                  # ≥ 1
grep -c '{{' $f                   # 0 antes de mostrar ao cliente
```

## Romeno

O texto foi escrito por IA, com diacríticos corretos (ș e ț com vírgula, não cedilha). **Pedir a um nativo que reveja** antes de mostrar o primeiro site a um cliente. Tratamento: `tu` no site (é o registo habitual em restauração); `dumneavoastră` na conversa com o dono (ver guião).
