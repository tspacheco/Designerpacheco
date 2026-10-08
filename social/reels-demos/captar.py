"""Grava a demo como num telemóvel, fotograma a fotograma, com o tempo controlado.

O relógio da página (Date, setTimeout, requestAnimationFrame) é o do Playwright e as
animações CSS são postas à mão no tempo certo, por isso a entrada do herói e as
revelações ao fazer scroll saem iguais às de um telemóvel real, sem saltos.

Uso (testes): python3 captar.py <pasta-da-demo> <saida> <segundos>; o gerar_reel.py chama captar()."""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FPS = 30
ESCALA = 2.5  # 432 px CSS × 2,5 = 1080 px

# Põe cada animação/transição CSS no tempo virtual da página (criada em t0 → currentTime = agora - t0).
ANIM = """(agora) => {
  window.__t0 = window.__t0 || new WeakMap();
  for (const a of document.getAnimations()) {
    if (!window.__t0.has(a)) window.__t0.set(a, agora);
    a.pause(); a.currentTime = agora - window.__t0.get(a);
  }
  for (const v of document.querySelectorAll('video')) {
    v.pause(); if (v.readyState > 0 && v.duration) v.currentTime = (agora / 1000) % v.duration;
  }
}"""

# Paragens do scroll: o topo de cada bloco grande da página inicial (secções e rodapé) visível.
PARAGENS = """() => {
  const vis = e => { const s = getComputedStyle(e); return s.display !== 'none' && e.offsetHeight > 120 && e.getClientRects().length };
  const bs = [...document.querySelectorAll('main section, body > section, footer')].filter(vis);
  const max = document.documentElement.scrollHeight - innerHeight;
  const ys = bs.map(b => Math.min(max, Math.round(b.getBoundingClientRect().top + scrollY - 70))).filter(y => y > 40);
  return {ys: [...new Set(ys)].sort((a, b) => a - b), max};
}"""

# Identidade da demo para o texto do reel: fonte de título, cor de destaque, fundo.
IDENTIDADE = """() => {
  const cs = e => e && getComputedStyle(e);
  const h = document.querySelector('h1 *') || document.querySelector('h1');
  const h2 = document.querySelector('h2');
  const opaco = c => c && c !== 'rgba(0, 0, 0, 0)' && c !== 'transparent';
  let acento = null;
  for (const b of document.querySelectorAll('a.btn, button.btn, .btn, a[href^="tel:"]')) {
    const s = cs(b); if (!s || b.offsetParent === null) continue;
    if (opaco(s.backgroundColor)) { acento = s.backgroundColor; break; }
  }
  return {
    titulo: cs(h2 || h).fontFamily, titulo_h1: cs(h).fontFamily,
    texto: cs(document.body).fontFamily,
    acento: acento || cs(h2 || h).color,
    fundo: cs(document.body).backgroundColor, cor: cs(document.body).color,
  };
}"""


def ease(x):  # suave nos dois lados
    return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2


def caminho(ys, ini, periodo, viagem=.7):
    """Posição do scroll no tempo t: parado no herói até `ini`, depois uma viagem por compasso
    (`periodo` s), a começar em cima do tempo forte, para as paragens caírem na música."""
    def pos(t):
        y = 0
        for k, alvo in enumerate(ys):
            a = ini + k * periodo
            if t < a: return y
            if t < a + viagem: return y + (alvo - y) * ease((t - a) / viagem)
            y = alvo
        return y
    return pos


async def captar(pasta, saida, dur, ini, periodo, n_paragens, larg=432, alt=580, hora="2026-10-06T12:30:00+03:00"):
    os.makedirs(saida, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        ctx = await b.new_context(viewport={"width": larg, "height": alt}, device_scale_factor=ESCALA,
                                  is_mobile=True, has_touch=True)
        pg = await ctx.new_page()
        await pg.clock.install(time=hora)  # terça ao meio-dia: o selo «aberto agora» das demos fica verde
        await pg.goto(f"file://{os.path.abspath(pasta)}/index.html", wait_until="load")
        await pg.evaluate("document.fonts.ready.then(()=>1)")
        await pg.add_style_tag(content="html{scroll-behavior:auto!important}::-webkit-scrollbar{display:none}")
        ident = await pg.evaluate(IDENTIDADE)
        info = await pg.evaluate(PARAGENS)
        ys = info["ys"]
        if len(ys) > n_paragens:  # escolhe paragens espalhadas pela página, a última no rodapé
            k = (len(ys) - 1) / (n_paragens - 1)
            ys = [ys[round(i * k)] for i in range(n_paragens)]
        while 0 < len(ys) < n_paragens:  # página curta: paragem extra a meio do maior salto, para o scroll não parar cedo
            pts = [0] + ys
            k = max(range(len(ys)), key=lambda i: pts[i + 1] - pts[i])
            ys.insert(k, round((pts[k] + pts[k + 1]) / 2))
        pos = caminho(ys, ini, periodo)
        n = int(dur * FPS)
        for i in range(n):
            t = i / FPS
            await pg.evaluate(f"window.scrollTo(0,{pos(t):.1f})")
            await pg.clock.run_for(1000 // FPS if i % 3 else 1000 // FPS + 1)  # 33/34 ms → 30 fps certos
            await pg.evaluate(ANIM, int(round(t * 1000)))
            await pg.screenshot(path=f"{saida}/{i:05d}.png", animations="allow")
        await b.close()
    json.dump({"identidade": ident, "paragens": ys, "fps": FPS, "n": n}, open(f"{saida}/info.json", "w"), indent=1)
    return ident


if __name__ == "__main__":
    a = sys.argv
    print(asyncio.run(captar(a[1], a[2], float(a[3]), 2.0, 2.0, 9)))
