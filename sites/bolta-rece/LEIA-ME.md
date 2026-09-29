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

## Publicar

- **Netlify:** arrastar `dist/bolta-rece-netlify.zip` (as 6 páginas, `netlify.toml` e só as fotos que as páginas usam, com `media/LEIA-ME.txt`). Para voltar a gerá-lo: build e depois o zip com os mesmos ficheiros. O formulário de reserva funciona lá (Netlify Forms, `data-netlify`); noutro alojamento, ligar o `action` a um serviço de formulários ou deixar só o telefone.
- **Hostinger:** o mesmo, sem `netlify.toml`, em `public_html`.
- Na venda: retirar o `.banner` de `src/nav.html`, preencher os dados da firma no `src/footer.html`, voltar a correr o build.

## Vídeo "Antes vs Depois"

Gravar a página inicial: intro em vídeo → herói → scroll pelo percurso da rua até à mesa (portão, porta, arcos, descida 3D, luz final) → menu → faixa horizontal "O seară la Bolta Rece" (deixar o scroll parar em cada capítulo) → história → poesias → reservas. Para o intro aparecer em cada take, abrir numa janela anónima nova (o intro só se mostra uma vez por sessão).
