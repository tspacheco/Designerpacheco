# Patai Beach (Corralejo, Fuerteventura) — proposta de site (Pacheco Studios, 29/09/2026)

Restaurante de arroces do chef cubano Ariel Patai, na praia de La Goleta. Análise e proposta comercial em `research/patai-beach-club.md`. Esta é a demo em espanhol; EN/DE entram na venda (mesmo ficheiro, textos traduzidos).

## Ficheiros

| Ficheiro | O que é |
|---|---|
| `index.html` | página final, ficheiro único (CSS, JS e fontes embutidos) — **gerada, não editar à mão** |
| `src/index.html` | fonte da página (marcador `<!--@fontes-->`) |
| `ferramentas/build.py` | monta o `index.html`: `python3 ferramentas/build.py` |
| `ferramentas/fontes.py` → `_fontes/fontes.css` | Rufina 400/700 + Figtree 400/500/600/400i em base64 (latin + latin-ext; ñ ¿ ¡ ü ß verificados no cmap) |
| `media/` | fotos e vídeo do cliente — ver `media/LEIA-ME.txt` (nomes exatos); sem eles a web mostra arte SVG |
| `netlify.toml` | cabeçalhos para o Netlify |

## Assinatura visual: "El corte"

A web abre com **a faca a cortar a cebola** (animação procedimental em canvas, ~3,5 s, uma vez por sessão): tábua escura, luz quente, cinco cortes com rodelas a separarem-se e partículas, raios e chispas de luz ("los efectos surgen"), os anéis da cebola transformam-se nos anéis da paellera, e o ecrã **abre-se na vertical, exatamente na linha da lâmina** da foto do chef (`media/chef.jpg`: o chef de preto com a faca à frente do rosto); ao mesmo tempo as duas metades da foto deslizam e encaixam na lâmina, e um destello dourado percorre o filo. Se a foto faltar, fica uma silhueta em SVG. O mesmo corte diagonal revela as fotografias ao longo da página (`.cut`), os anéis das paelleras desenham-se ao aparecer, e o texto entra em coreografia. Se existir `media/intro.mp4`, o vídeo substitui a animação. Com movimento reduzido ou sem JS: sem intro, tudo visível. Tecla Esc ou "Saltar" fecham o intro.

Design system (ui-ux-pro-max pediu "Kinetic Brutalism" + Playfair/Karla — rejeitado: brutalismo não é um restaurante premium de praia e a Playfair já foi usada): mantido só o **preto premium + acento dourado**; paleta própria tinta `#100E0C` · hueso `#F4ECDF` · azafrán `#E3A233` · pimentón `#B8432A` · socarrat `#7A3A1B` · atlántico `#1E5F63`; tipos **Rufina** (display) + **Figtree** (texto).

## Widget de reservas por turnos (decisão do Tomás: sem Cal.com)

Dia (14 dias) → turno (almoço 13:00–15:00, jantar 19:30–21:30, **horários orientativos**) → pessoas → dados → "Solicitud recibida". Estados por turno: livre / poucas mesas / completo (lista de espera). A ocupação da demo é determinista (`hash(fecha+hora)`), para mostrar os estados.

Ligação ao motor, sem mexer na web (`window.PATAI` no fim do `<script>`):
- `endpoint`: URL que recebe `POST` JSON `{fecha, hora, turno, personas, nombre, telefono, email, idioma, notas, lista_espera, origen:"web"}`; resposta esperada `{ok, id, estado}`.
- `whatsapp`: número em formato internacional sem `+` → botão "Enviar por WhatsApp" com a mensagem pronta.
- `email`: → botão "Enviar por e-mail".
- `capacidad`: mesas por turno da demo.
- Disponibilidade real: o motor deve expor `GET /disponibilidad?fecha=AAAA-MM-DD` → `[{hora, libres, estado}]` e a função `libres()` passa a lê-lo.

## Dados reais e "por confirmar"

Reais: marca Patai Beach, Patai Beach Club S.L. (CIF B10648970), morada (Calle Arístides Hernández Morán 16, Local 2, 35660 Corralejo), redes (@patai_beach, @pataibeach, pataibeach.corralejo, YouTube), pratos citados em reseñas/Cenando con Pablo, imprensa (Cenando con Pablo, CiberCuba, COPE, El Español, Infobae, Diario de Avisos), citação de cliente do TripAdvisor (jan. 2026), o adaptar a carta a necessidades dietéticas (CiberCuba).
Por confirmar: horário, telefone/WhatsApp (4 números em circulação), e-mail, dados de inscrição no Registo Mercantil, preços (IGIC incluído), alergénios, mínimo de comensais por arroz, fotos com direitos, situação legal da esplanada na areia.

## Legal (Espanha/Canárias)

Aviso legal (LSSI art. 10), política de privacidade (RGPD + LOPDGDD) para o widget, nota de cookies (sem cookies de analítica → sem banner; só `sessionStorage` técnico do intro; mapa em link, não em iframe), hojas de reclamaciones (Decreto 90/2023). Sem preços e sem alergénios na demo.

## Publicar

Netlify: arrastar a pasta (ou zip com `index.html`, `media/`, `netlify.toml`). Hostinger: `index.html` + `media/` em `public_html`. Na venda: retirar `.banner`, preencher `window.PATAI`, horário e telefone, dados do Registo Mercantil, e-mail; colocar as fotos com os nomes de `media/LEIA-ME.txt`.

## Vídeo de apresentação

Abrir em janela anónima (o intro só aparece uma vez por sessão): corte da cebola → hoja revela o chef → scroll: corte diagonal nas fotos → paelleras a desenharem-se → widget: dia, turno com estados, pessoas, "Solicitud recibida".
