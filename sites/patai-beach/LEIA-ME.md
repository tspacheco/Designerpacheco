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

Tudo o que se revela no site revela-se **por um corte vertical, como a lâmina da faca**:

1. **Abertura (uma vez por sessão, ~7,7 s, "Saltar"/Esc):** ecrã escuro com a marca → uma linha dourada corta o ecrã e **abre o vídeo do cliente** num painel vertical, com o fundo desfocado da mesma cena (o chef a servir a paella → langosta em grande plano) e o título "Entre fogones, arroz y buena compañía" → no fim, o ecrã abre-se **na linha da lâmina da foto do chef** e o herói aparece com as duas metades da cara a encaixar. Se o vídeo não estiver pronto aos 2,6 s (rede lenta, ficheiro em falta, reprodução automática bloqueada), entra direto o herói. A animação da faca a cortar a cebola foi retirada a 29/09 a pedido do Tomás (está no histórico do git, commit `e8d1f62`, se for para voltar).
2. **Herói:** foto do chef de preto com a faca à frente do rosto (`media/chef.jpg`), partida na lâmina; vídeo `media/hero.mp4` opcional por cima.
3. **"Entre fogones, arroz y buena compañía" (secção 3D comandada pelo scroll):** painéis verticais empilhados em profundidade; cada scroll **corta o painel da frente ao meio** — as duas metades abrem-se como portas para trás, com um brilho no fio — e o seguinte avança. Os painéis de vídeo tocam só quando estão à frente e o fotograma fica congelado nas metades durante o corte. Termina no retrato do chef, com a lâmina exatamente no centro. Painéis de foto opcionais (`arroz-bogavante.jpg`, `tapas.jpg`, `terraza.jpg`) entram sozinhos quando o ficheiro existe.
4. Mesa giratória 3D das paelleras (langosta e langostinos já com foto real), cortes diagonais nas fotografias, paelleras SVG que se desenham.

**Fotos do cliente (29/09):** a secção "El chef" mostra o chef de jaleca na praia. "Entre fogones" tem 6 painéis: mesa, langosta, tapas, jamón, a servir e o chef. A foto da esplanada na areia está preparada em `media/terraza.jpg` mas fica fora do site até o título legal estar confirmado; ver `media/LEIA-ME.txt`.

Com movimento reduzido ou sem JS: sem abertura, a secção 3D vira uma grelha estática com legendas, tudo visível.

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

## Qualidade e desempenho do vídeo

- `intro.mp4` e `fogones-mesa.mp4`: **corte sem recompressão** do original (720×1280, H.264, ~1,2 Mbit/s). `fogones-langosta` e `fogones-jamon` começam fora de um keyframe, por isso foram recomprimidos a CRF 19 (SSIM 0,991 face ao original — visualmente igual). Todos sem som, com `faststart`; WebM VP9 como reserva.
- O vídeo da abertura só é descarregado na primeira visita da sessão (`preload="none"` + `load()` no JS); os vídeos da secção 3D só quando a secção está a menos de ~1 ecrã; só toca o painel da frente.
- Nada de leituras de layout durante o scroll (posições em cache, recalculadas em resize/ResizeObserver); fundo desfocado da abertura = duas imagens de 3 KB já desfocadas (sem filtros ao vivo).
- Testado (Chromium, 29/09): fluxo normal, Saltar, Esc, vídeo pendurado, vídeo em falta, autoplay bloqueado, segunda visita, telemóvel, movimento reduzido, percurso completo sem erros na consola, sem scroll horizontal a 360/768/1024/1440.

## Publicar

Netlify: arrastar a pasta (ou zip com `index.html`, `media/`, `netlify.toml`). Hostinger: `index.html` + `media/` em `public_html`. Na venda: retirar `.banner`, preencher `window.PATAI`, horário e telefone, dados do Registo Mercantil, e-mail; colocar as fotos com os nomes de `media/LEIA-ME.txt`.

## Vídeo de apresentação

Abrir em janela anónima (o intro só aparece uma vez por sessão): corte da cebola → hoja revela o chef → scroll: corte diagonal nas fotos → paelleras a desenharem-se → widget: dia, turno com estados, pessoas, "Solicitud recibida".
