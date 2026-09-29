# Casa Bolta Rece — novo site (proposta Pacheco Studios, 27/09/2026)

Restaurante histórico em Iași (Str. Rece nr. 10, desde 1786). O cliente tem um site WordPress (casaboltarece.ro); esta é a proposta de substituição: página inicial nova de raiz e as outras páginas no mesmo sistema.

## Estrutura

| Ficheiro | O que é |
|---|---|
| `index.html`, `istoric.html`, `meniu.html`, `galerie.html`, `contact.html`, `carmangeria.html` | páginas finais, cada uma em ficheiro único (CSS, JS e fontes embutidos) — **geradas, não editar à mão** |
| `src/pages/*.html` | conteúdo de cada página; `src/site.css`, `src/site.js`, `src/nav.html`, `src/footer.html` partilhados; `src/intro.html` (vídeo de entrada, só index); `src/bolta.js` (o percurso da rua até à mesa, só index) |
| `ferramentas/build.py` | monta as páginas finais: `python3 ferramentas/build.py` |
| `ferramentas/fontes.py` → `_fontes/fontes.css` | fontes Google (Bona Nova, Albert Sans, EB Garamond itálico) em base64, latin + latin-ext (ș ț ă) |
| `ferramentas/three.min.js` | Three.js r152 (UMD), embutido só no index |
| `ferramentas/profundidade.py` | gera `media/profundidade-*.png` (mapas de profundidade das fotos da cave) com Depth Anything V2 Small; o modelo descarrega-se para `ferramentas/_modelos/` (fora do git) |
| `media/` | 48 fotografias do site atual a 1800 px, logótipos, selo ANPC, 5 mapas de profundidade (`profundidade-*.png`, 11–15 KB cada) |

## Assinatura visual

**"Da rua até à mesa"** (29/09/2026): logo a seguir ao herói, uma só secção com o palco fixo leva o visitante por fotografias reais do cliente, pela ordem de quem chega.

1. **De porta em porta** (2D, sem WebGL): Strada Rece → poarta → terasa → prispa → salonul → spre cramă. A câmara aproxima-se de cada abertura real e a divisão seguinte aparece lá dentro, recortada com a forma dessa abertura. O portão abre-se ao meio e a porta abre-se de lado, como folhas. Os arcos do salão e da crama já estão abertos. A rua e a esplanada, que não têm abertura, aproximam-se e fundem-se na foto seguinte. A divisão do fundo cresce mais devagar do que a abertura, por isso lê-se como espaço.
2. **Sub boltă** (Three.js): crama → sub bolți → ușa pivnițelor → hrubele → masa. Cada foto da cave tem um mapa de profundidade (`media/profundidade-*.png`). A malha da foto é deslocada por ele e a câmara entra na foto com paralaxe verdadeira. A paragem seguinte nasce no ponto de fuga da anterior, enquanto o que está perto passa por nós e fica no escuro. Os candeeiros reais das fotos tremeluzem e há pó no ar. No fim, a luz do fundo da boltă enche o ecrã e dá lugar ao menu.

As legendas ficam em baixo à esquerda, com os textos do istoric do cliente. O nome do sítio e a barra de progresso ficam à direita, ou no topo no telemóvel. O botão "Coboară în pivniță" do herói salta para o início da descida.

**"O seară la Bolta Rece"**: uma faixa horizontal comandada pelo scroll vertical, em três capítulos (I masa: o prato · II vinul: as garrafas · III versul: a placă de lemn), com paragem em cada capítulo, fusão suave entre fotografias, parallax leve e barra de progresso. A lista do menu desenha as linhas pontilhadas ao aparecer e as poesias da carte de oaspeți revelam-se verso a verso.

**Fim da descida (29/09, para a gravação do vídeo):** a câmara trava devagar na mesa sob a boltă e a imagem fica no ecrã até a secção seguinte subir por cima. Já não há o clarão claro que fazia a passagem para o menu.

**Site escuro (29/09):** o site inteiro passou a fundo `--noapte`, sem secções claras, para a gravação de ecrã e a campanha de Facebook não terem flashes de luz. Os tokens `--text`/`--text-2` são agora claros, os painéis usam `--panou` (branco a 4,5 %), as linhas `--linie`, e há `--verde-2`/`--rosu-2` para texto sobre escuro. O widget, o formulário simples, a lista do menu, a galeria e o mapa (invertido) seguem o mesmo tom. A fotografia do salão no istoric leva sombra. Para voltar ao fundo claro: repor os tokens antigos (`--text:#2B1A12; --text-2:#5A4536`, `body{background:var(--var)}`) e os fundos `#fff9f0`/`#fff` dos painéis; está tudo no histórico do git (commit anterior a 29/09, "versão final sem marca").

**Estados:** sem WebGL, a descida faz-se com as mesmas fotografias em 2D (zoom para o fundo e fusão). O `<html>` nasce com `class="no-js"` e um script no head troca para `js` (e junta `rm` com movimento reduzido). Sem JavaScript ou com movimento reduzido, o percurso e a faixa ficam empilhados na vertical, fotografia a fotografia, com todas as legendas. Fontes: Bona Nova (títulos), Albert Sans (corpo), EB Garamond itálico (citações e versos).

**Afinar o percurso** (em `src/pages/index.html`, em cada `<figure class="cadru">`):
- tour (`data-tip="prag"`): `data-op` é a abertura em coordenadas 0–1 da foto (`r x0 y0 x1 y1` retângulo, `a x0 x1 topo nascença base` arco, `z x y` sem abertura); `data-abre="centro|esq|dir"` faz a abertura abrir-se como porta; `data-foco` é o `object-position` da foto.
- descida (`data-tip="bolta"`): `data-vp` ponto de fuga, `data-z` "perto longe" em metros, `data-avanco` metros que a câmara entra (mais = mais movimento e mais esticões nas paredes), `data-luz` candeeiros "x y raio", `data-rel` mapa de profundidade. Para outra foto: `python3 ferramentas/profundidade.py <nome>`.

**Desempenho:** o JavaScript gasta 0,1–0,4 ms por quadro, e até 5 ms no percentil 95 com o CPU 4x mais lento. Os mapas constroem-se aos bocados e as texturas descodificam-se fora da thread principal. O shader compila antes de a pessoa chegar à cave. Só há duas fotos no ecrã de cada vez e o ciclo pára quando a secção sai de vista. No telemóvel, a câmara anda menos e a malha é mais leve.

**Ideia 2, em espera:** "a casa em corte", desenho a traço da casa cortada ao meio. Existe só como vídeo de proposta em `prototipos/` e só entra no site se o Tomás a escolher.

## Intro em vídeo (só na primeira entrada)

`src/intro.html` mostra `media/intro.mp4` (+ `media/intro.webm`) em ecrã inteiro **uma vez por sessão**, só no index, e funde para o herói — que é a mesma fotografia em que o vídeo acaba. Sem o ficheiro, o build deixa o intro de fora e o site abre direto no herói, sem pedidos em falta. Para o ativar: pôr `media/intro.mp4` (+ `intro.webm`) e voltar a correr o build. O vídeo tem `preload="none"` e só começa a descarregar na primeira entrada. Os ficheiros vêm do Higgsfield (ver `sites/carmangeria-boierilor/intro/LEIA-ME.md` para os comandos ffmpeg). Não usar em transições entre páginas.

## Dados reais (do site atual) e o que está "de confirmat"

Reais: nome, morada, telefones (+40 752 589 881 · +40 232 212 255), e-mail, horário (Luni–Duminică 08:00–22:00), Facebook/Instagram, textos do istoric e da página inicial, nomes dos pratos, poesias, a ligação ao magazin Carmangeria Boierilor (Dacia).
De confirmat: denumire firmă/CUI/Reg. Com. (rodapé), preços (não há nenhum no site), PDF do menu, alergénios, link de encomenda online da Carmangeria, morada/horário do magazin.

## Rezervări (widget, 29/09/2026)

No início (`#rezervari`) e no contacto (`contact.html#rezervare`) há um widget com o mesmo percurso do do Patai Beach, em romeno: 1 ziua (21 dias, com "azi" e "mâine") · 2 ora (prânz 12:00–15:30, seara 18:00–21:00, de meia em meia hora) · 3 persoane · 4 locul (oriunde, cramă, salon, sala rustică, terasă, como preferência) · os dados · a confirmação. Todos os botões "Rezervă o masă" levam ao widget; o telefone continua ao lado.

- **Hora de Iași:** o "hoje" e as horas já passadas contam-se em Europe/Bucharest, seja qual for o fuso de quem reserva. Hoje só aceita horas com pelo menos uma hora de antecedência; se já não houver, pede para ligar.
- **Sem ocupação inventada:** ao contrário da demo do Patai, o widget não mostra "liber / puține mese / complet" enquanto não houver um sistema a dizê-lo. As horas são pedidos; o texto diz que o restaurante confirma.
- **Para onde vai o pedido:**
  1. se `window.BOLTA.endpoint` estiver preenchido: `POST` JSON `{data, ora, interval, persoane, zona, nume, telefon, email, observatii, lista_asteptare, limba, sursa}`; resposta 2xx = recebido;
  2. senão, no Netlify: vai para o painel **Forms → rezervare** (sem configurar nada). Para receber cada pedido por e-mail: Netlify → Site configuration → Forms → Form notifications → Email notification → casaboltareceiasi@gmail.com;
  3. se não houver nenhum dos dois, ou o envio falhar, o ecrã final diz isso e oferece "Trimiteți pe e-mail" (já preenchido), "Sunați" e "Copiați cererea".
- **Ligar a um sistema de reservas** (em `src/rezervare.html`, depois build): `window.BOLTA = { endpoint: "https://…/rezervari", disponibilitate: "https://…/disponibilitate", whatsapp: "" }`. A disponibilidade é `GET …?data=AAAA-LL-ZZ` → `{"19:30": 0, "20:00": 2}` (mesas livres por hora); com ela aparecem os estados e a lista de espera. Também se podem mudar `pranz`, `seara`, `zile`, `telefon`, `email`; `netlify: false` para alojamentos sem Netlify Forms.
- **Sem JavaScript:** aparece um formulário simples com os mesmos campos (é também a definição que o Netlify Forms regista).

## Publicar

- **Netlify:** arrastar `dist/bolta-rece-netlify.zip` (as 6 páginas, `netlify.toml` e só as fotos que as páginas usam, com `media/LEIA-ME.txt`). Para voltar a gerá-lo: build e depois o zip com os mesmos ficheiros.
- **Hostinger:** o mesmo, sem `netlify.toml`, em `public_html`, e com `netlify: false` em `window.BOLTA` (os pedidos passam a sair por e-mail ou telefone).
- **Sem marca:** `python3 ferramentas/build.py` gera a versão final, sem a faixa nem o crédito da Pacheco Studios. `python3 ferramentas/build.py --demo` gera a versão de apresentação, com a faixa "Prezentare Pacheco Studios"; é essa que vai para a demo no claude.ai.
- **Antes de entregar ao cliente:** preencher denumire firmă, CUI e Nr. Reg. Com. no `src/footer.html` (ainda "de confirmat") e voltar a correr o build.

## Vídeo "Antes vs Depois"

Gravar a página inicial: intro em vídeo → herói → scroll pelo percurso da rua até à mesa (portão, porta, arcos, descida 3D, luz final) → menu → faixa horizontal "O seară la Bolta Rece" (deixar o scroll parar em cada capítulo) → história → poesias → reservas. Para o intro aparecer em cada take, abrir numa janela anónima nova (o intro só se mostra uma vez por sessão).
