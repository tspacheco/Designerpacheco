# CROAE Moita — arquitetura do site (v1, 23/09/2026)

**Objetivos (do brief):** mostrar o centro · atrair mais apoio (voluntários, donativos, parceiros) · notoriedade.
**Audiência:** famílias do concelho da Moita e arredores (Barreiro, Montijo, Alcochete) a pensar adotar; pessoas com tempo ao fim de semana (voluntariado); empresas locais (parcerias).
**Uma tarefa por página:** levar a pessoa a **um** de três botões — *Quero adotar* · *Quero ajudar* · *Ser parceiro*.

## 1. Direção de arte — "As 40 boxes"

Ponto de partida no mundo real do CROAE, não num template de ONG:

- **Assinatura visual:** o centro tem **40 boxes** (facto confirmado). O herói é uma **grelha de 40 células arredondadas**, em amarelo sobre azul-escuro, que se acende célula a célula na entrada (motion coreografado ≈ 1,2 s). Algumas células abrem com a foto de um animal para adoção; ao fazer scroll a grelha desagrega-se e as fotos "saem das boxes" para a secção de adoção. A metáfora é literal: cada box vazia é um animal que foi para casa. Nunca usada no catálogo (secção 5 do playbook).
- **Gesto de marca:** a **bandana amarela** dos cães no evento. Usada como forma (triângulo com nó) nos botões primários e como divisor de secção — em SVG inline, uma só vez por página, sem virar decoração.
- **Voz:** a deles. Os slogans já existem nos placares — *"Hoje é dia de fazer um novo amigo."* é o H1. *"Eles nunca te deixariam para trás."* abre a secção de voluntariado. Sem "paixão pelos animais" nem "amigos de quatro patas".
- **Risco estético justificado:** fundo azul-escuro no herói e nos rodapés (herdado dos placares) num setor onde tudo é branco-e-pastel. Resto da página claro e arejado para contraste AA e leitura no telemóvel.

### Paleta (tokens `:root`)

| Token | Hex | Uso |
|---|---|---|
| `--amarelo` | `#F2B705` | bandana, CTA primário, células da grelha |
| `--amarelo-escuro` | `#B8860B` | texto amarelo sobre claro (AA), hover |
| `--noite` | `#1B2A41` | herói, rodapé, texto principal |
| `--areia` | `#FBF7EE` | fundo das secções claras (não é o creme-padrão #F4F1EA: mais quente, puxa ao amarelo) |
| `--terra` | `#6B4E2E` | legendas, patas do padrão, texto secundário |
| `--branco` | `#FFFFFF` | cartões |

Contraste verificado: `--noite` sobre `--areia` 13,5:1 · branco sobre `--noite` 14:1 · `--noite` sobre `--amarelo` 8,9:1 · `--amarelo-escuro` sobre `--areia` 4,6:1.

### Tipografia (novas no tracker)

- **Display:** `Gabarito` 800/900 — geométrica, calorosa, próxima do lettering dos placares sem o copiar. Só em H1/H2 e nos números.
- **Corpo:** `Atkinson Hyperlegible` 400/700 — desenhada para legibilidade (serviço público, leitura por pessoas mais velhas no telemóvel). Justifica-se por si.
- **Utilitária:** `Atkinson Hyperlegible` 700 em maiúsculas pequenas para eyebrows e etiquetas (uma família a menos a carregar).

Rejeitado do `ui-ux-pro-max` (output cru: roxo de comunidade + Fredoka/Nunito + "vibrante e block-based") — é a resposta genérica para "comunidade"; a cor do cliente é amarelo/azul-escuro e a fonte redonda infantil não serve um serviço municipal. Mantido do output: secções largas (≥ 48 px), tipo grande, hover com mudança de cor, 200–300 ms.

## 2. Estrutura da página (single-file, `#/` sem router — âncoras)

```
┌──────────────────────────────────────────────────────┐
│ banner APRESENTAÇÃO PACHECO STUDIOS (remover na venda) │
│ nav: Adotar · Ajudar · Parceiros · O centro · Contactos│
├──────────────────────────────────────────────────────┤
│ HERÓI (--noite)                                        │
│  grelha 40 boxes ●●●●●●●●●●  H1 "Hoje é dia de fazer   │
│  (acende-se em seq.)         um novo amigo."           │
│                              [Quero adotar] [Ajudar]   │
│  faixa de factos: 40 boxes · até 120 animais · GVM     │
├──────────────────────────────────────────────────────┤
│ marquee: ADOTA · PASSEIA · APADRINHA · DOA · PARTILHA  │
├──────────────────────────────────────────────────────┤
│ ADOTAR (--areia)                                       │
│  cartões por animal (foto, nome, idade, porte, tempo   │
│  no centro) — dados vêm do cliente; sem dados → "a     │
│  confirmar". "Entregue com: vacinas, desparasitação,   │
│  microchip, esterilização, ração" (placar, confirmado) │
│  passos: 1 visita · 2 conversa · 3 vai para casa       │
├──────────────────────────────────────────────────────┤
│ AJUDAR (branco)                                        │
│  "Eles nunca te deixariam para trás."                  │
│  3 vias: Voluntariado (sáb/dom 10–12h, marcação) ·     │
│  FAT · Doar (lista do que precisam — a confirmar)      │
│  CTA: e-mail gab.vetmun@cm-moita.pt / tel              │
├──────────────────────────────────────────────────────┤
│ PARCEIROS (--noite) — secção pedida no brief           │
│  "O CROAE saiu à rua nas Festas da Moita. Quem esteve  │
│  connosco:" mural de logótipos (a confirmar) + galeria │
│  do evento (5 fotos limpas) + "A sua empresa aqui":    │
│  3 formatos de parceria (ração/material · patrocínio   │
│  de evento · apadrinhamento de box) + CTA "Ser parceiro"│
├──────────────────────────────────────────────────────┤
│ O CENTRO (--areia)                                     │
│  inaugurado 12/03/2024 · 5 edifícios · recreio comum · │
│  gerido pelo Gabinete Veterinário Municipal · cheque-  │
│  veterinário · fotos do espaço (por obter)             │
├──────────────────────────────────────────────────────┤
│ CONTACTOS + mapa (morada a confirmar) · horário a conf.│
│ rodapé: Moita Município · Livro de Reclamações · IG/FB │
└──────────────────────────────────────────────────────┘
```

**Móvel:** herói com a grelha reduzida a 4×10 atrás do texto, `.hero-shade` reforçado; CTAs em coluna; secções em 1 coluna; nav com burger acessível.

## 3. Secção "Parcerias" — porquê e como

O stand nas Festas já expunha logótipos de negócios locais: a relação existe, só não está formalizada. O site dá-lhe forma:

1. **Prova:** "Estivemos nas Festas da Moita com X parceiros" (número a confirmar) + galeria do evento.
2. **Oferta clara, três níveis** (nomes a validar com o cliente): *Amigo* (ração/material em espécie) · *Padrinho de box* (apoio mensal a uma das 40 boxes — liga-se à assinatura visual: a box "apadrinhada" fica marcada na grelha) · *Parceiro de evento* (presença em ações de adoção).
3. **Contrapartida:** logótipo no site e nos placares, menção nas redes do CROAE.
4. **Um só CTA:** "Ser parceiro" → mailto com assunto pré-preenchido (sem formulário — sem backend).

## 4. Motion

- Entrada do herói: grelha acende em varrimento diagonal (transform/opacity, 40 × 25 ms), depois H1 e CTAs (fade-up 400 ms). Total < 1,5 s.
- Scroll: `.rv` com `IntersectionObserver`, `.d1/.d2`.
- Micro: cartão de animal levanta 4 px e a bandana do botão "roda" 6° no hover.
- `prefers-reduced-motion`: grelha já acesa, zero transições.

## 5. Conteúdo que falta (bloqueia a construção final, não a demo)

Ver lista "A confirmar" em `research/croae-moita.md`. Para a **demo** avança-se com o que está confirmado e "a confirmar" no resto. Fotos de animais e placares (a enviar pelo Tomás) entram em `media/croae-moita/`, limpas de UI do Instagram com o método desta sessão (corte de bordas + inpainting dos botões).

## 6. Crítica final prevista

"Isto podia ser um template?" — A grelha das 40 boxes só faz sentido neste centro; a bandana só faz sentido porque os cães a usam; os slogans são deles. Se a demo for apresentada sem fotos reais dos animais, a grelha tem de aguentar sozinha — por isso é a assinatura, não decoração.
