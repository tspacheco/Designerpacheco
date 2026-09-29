# Intro de pachecost.com — os três carros

As fotografias da intro estão em `media/intro-1.webp` (compacto), `media/intro-2.webp` (muscle car descapotável)
e `media/intro-3.webp` (superdesportivo). Foram geradas no Higgsfield (gpt_image_2_5, fundo transparente) a partir das
fotos do Tomás, sem logótipos nem marcas: o site não pode mostrar marcas registadas como se fossem nossas.

Para trocar um carro: gerar com um dos prompts abaixo, aparar à caixa do alfa, reduzir a 1200 px de largura, gravar em
WebP com transparência (qualidade 82) com o mesmo nome, e correr `python3 gerar.py`. O JavaScript mede cada fotografia
ao carregar; só o comprimento no palco está fixo (`CARROS` em `index.src.html`: 246 · 300 · 287 unidades, à escala real).

## Prompts (em inglês: é a língua em que os geradores acertam mais)

O bloco comum vai no fim de cada um. Pedir sempre os três na mesma sessão, com o mesmo bloco comum, para a luz e a
câmara baterem certo entre eles.

**1 · Compacto (o ponto de partida)**
> Studio photograph of a light metallic sky-blue early-2000s European five-door compact hatchback, plain steel-look alloy wheels, black bumper trim. <bloco comum>

**2 · Muscle car (depois do web design + marketing)**
> Studio photograph of a bright orange American muscle-car convertible with the black soft top up, two wide matte-black racing stripes running over the hood, low front splitter and black multi-spoke alloy wheels. <bloco comum>

**3 · Superdesportivo (depois da implementação de IA)**
> Studio photograph of a dark graphite-grey mid-engine hypercar with a large fixed rear wing, deep front splitter, orange brake calipers and dark forged wheels. <bloco comum>

**Bloco comum**
> Exact side profile facing right, camera at wheel-hub height with a long telephoto lens (no perspective distortion), the whole car inside the frame with generous empty margin on every side, tyres resting on an invisible floor, no shadow, no reflection, isolated on a fully transparent background (if not available: pure white background), no logos, no badges, no text, no license plates, soft neutral daylight, photorealistic, sharp, 4k.

Se o sistema não fizer fundo transparente: pedir fundo branco puro e tirar o fundo depois (o Higgsfield tem
`remove_background`; o remove.bg também serve). Verificar sempre que nenhuma roda nem para-choques fica cortado pela
margem: a caixa do alfa não pode tocar nas bordas da imagem.
