# CROAE Moita — arquitetura do site (v2, 23/09/2026)

**Objetivos (do brief):** mostrar o centro · levar as pessoas até lá (ou pelo menos a ajudar) · mais apoio e notoriedade.
**Condição decisiva (v2):** o site é entregue **uma vez, sem manutenção**. Nada na página pode depender de dados que mudam: sem lista de animais, sem ocupação de boxes, sem programas inventados com valores. Os animais atuais vivem no Instagram; o site aponta para lá e para o telefone.
**Uma tarefa por página:** levar a pessoa a **um** de três gestos — *Marcar um passeio* · *Ajudar* · *Ser parceiro*.

## 1. Direção de arte — "A trela"

- **Assinatura visual:** a trela verde-água que aparece nas fotos dos passeios vira **uma linha contínua** que sai da fotografia do herói, corre pela margem esquerda da página e termina numa etiqueta **"Chegaste."** nos contactos. Desenha-se com o scroll (`stroke-dashoffset` calculado em JS a partir de dois marcadores `data-trela-inicio` / `data-trela-fim`). A metáfora é literal: a trela leva-te até ao centro. Só aparece a partir de 1220 px (abaixo disso não há margem livre); em `prefers-reduced-motion` aparece já desenhada.
- **Gesto de marca:** a bandana amarela dos cães — ícone nos botões primários.
- **Voz:** os slogans dos placares. H1 = *"Hoje é dia de fazer um novo amigo."*; Ajudar abre com *"Eles nunca te deixariam para trás."*
- **Risco justificado:** herói e rodapés em azul-escuro (dos placares) num setor onde tudo é branco-e-pastel; interior claro para leitura no telemóvel.

Paleta: `--amarelo #F2B705` · `--noite #1B2A41` · `--areia #FBF7EE` · `--areia-2 #F3EBD8` · `--terra #6B4E2E` · `--trela #1FA58A` (só linha/etiqueta, nunca texto sobre claro).
Tipografia: **Gabarito** 800/900 (display) + **Atkinson Hyperlegible** (corpo) — legibilidade para serviço público.

## 2. Páginas (cada uma um HTML auto-contido, geradas por `ferramentas/build.py` a partir de `src/`)

| Página | Conteúdo | Gesto |
|---|---|---|
| `index` | herói com foto do passeio · marquee · "Porque vale a pena ir lá" (2024 · 120 · 0 € · Sáb/Dom) · três vias · "Os animais estão no Instagram, os passeios são aqui" · equipa · **Como chegar** (contactos + mapa, fim da trela) | Marcar um passeio |
| `adotar` | 3 passos (passeio → conversa → casa) · o que é entregue (placar) · onde ver os animais (Instagram / telefone / eventos) · FAQ | Marcar uma visita |
| `ajudar` | passeios sáb/dom 10–12h · família de acolhimento temporário · doar em espécie · partilhar | Pedir a ficha / Combinar entrega |
| `parceiros` | 3 formas (em espécie · eventos · divulgação — sem valores nem nomes de programa) · logótipos por ranhuras · contrapartidas | Ser parceiro (mailto) |
| `galeria` | mosaico das Festas da Moita · "O centro por dentro" com **30 ranhuras** `media/galeria/01.jpg…30.jpg` | Vem ver ao vivo |
| `centro` | vídeo (`media/video/centro.mp4|webm`, cai para a foto) · números · cronologia · Gabinete Veterinário · contactos + horários + mapa | Ligar agora |

## 3. Mecanismo "sem manutenção"

Tudo o que o cliente pode querer acrescentar depois entra **por ficheiros com nomes fixos**, sem tocar no HTML:
- `media/galeria/01.jpg … 30.jpg` → galeria (as que faltam desaparecem; se não houver nenhuma, a secção fecha-se com uma frase).
- `media/parceiros/01.png … 12.png` → logótipos.
- `media/video/centro.mp4` (+ `.webm`) → vídeo do centro.
- Cada pasta tem `LEIA-ME.txt`. O zip entregue é o produto final.

## 4. Dados "a confirmar" que ainda aparecem

Morada exata · horário de atendimento · custos de adoção (se existirem) · link da ficha de voluntário · idade mínima/seguro · condições da FAT · lista completa de doações. Ficam com a etiqueta até o Tomás confirmar com o Gabinete Veterinário; depois é substituir texto em `src/pages/` e correr `build.py`.

## 5. Fotos

Prints do Instagram limpos com `ferramentas/limpa-instagram.py` (corte de bordas + botões). Resolução ~730 px: chega para cartões e galeria; o herói usa a foto do cão preto a 4:5 dentro de um cartão, nunca full-width.

## 6. Crítica final

"Isto podia ser um template?" — A trela só faz sentido porque está nas fotos deles e porque o site existe para levar pessoas ao centro; os slogans são deles; a estrutura "não há lista aqui, há passeios ao fim de semana" é a verdade do cliente, não uma secção de ONG genérica. O que ficou de fora ficou por uma razão: não pode ficar desatualizado.
