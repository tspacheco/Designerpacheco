#!/usr/bin/env python3
"""Vídeo 2 do Bom Paladar — "Ainda não jantou aqui?" (reel 9:16, 1080×1920, 30 fps, ~23 s).

Estratégia de conversão, por ordem:
  1. gancho local em 1 s (pergunta + ALMANCIL) para parar quem é de cá;
  2. prova: comida real a mexer (vídeo do bacalhau e do caril) e 8 pratos em cortes rápidos;
  3. atrito zero: a reserva é uma mensagem de WhatsApp, mostrada a ser escrita e enviada;
  4. o mesmo número três vezes (WhatsApp, cartão final, legenda) e a morada com horário.

Não repete o vídeo 1 (flambé e scroll do site). Tudo é foto/vídeo real da casa; a conversa
de WhatsApp mostra só a mensagem do cliente a ser enviada, sem resposta inventada.

Uso:
  python3 build.py            prepara img/, escreve video.html, renderiza frames/ e monta video.mp4
  python3 build.py --so-html  só prepara e escreve video.html (para abrir no browser com ?t=segundos)
"""
import base64, html, os, pathlib, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
FOTOS = RAIZ / "media/bom-paladar/fotos"
FONTES = RAIZ / "social/fonts"
IMG = AQUI / "img"
FRAMES = AQUI / "frames"
W, H, FPS = 1080, 1920, 30
FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"

CASA = dict(whatsapp="918 958 233", morada="R. do Comércio 367A", terra="Almancil",
            site="bompaladar.pt", jantar="Jantar seg–sáb · 19h–22h30")

# fotos reais → nome curto, foco (x, y) para o corte 9:16
FOTO = {
    "salmao":   ("WhatsApp Image 2026-07-03 at 14.56.41.jpeg", 0.5, 0.5),
    "carpaccio":("WhatsApp Image 2026-07-03 at 14.56.41 (1).jpeg", 0.5, 0.5),
    "carre":    ("WhatsApp Image 2026-07-03 at 15.06.12.jpeg", 0.5, 0.55),
    "arroz":    ("WhatsApp Image 2026-07-03 at 15.06.44.jpeg", 0.5, 0.5),
    "pops":     ("WhatsApp Image 2026-07-03 at 14.38.42 (6).jpeg", 0.5, 0.45),
    "espetada": ("WhatsApp Image 2026-07-03 at 14.56.04.jpeg", 0.55, 0.5),
    "tabua":    ("WhatsApp Image 2026-07-03 at 15.04.11 (2).jpeg", 0.5, 0.5),
    "ninho":    ("WhatsApp Image 2026-07-03 at 14.59.40.jpeg", 0.5, 0.45),
    "camarao":  ("WhatsApp Image 2026-07-03 at 15.15.31.jpeg", 0.5, 0.5),
    "tachos":   ("WhatsApp Image 2026-08-07 at 13.05.57.jpeg", 0.5, 0.75),
    "porta":    ("WhatsApp Image 2026-07-03 at 15.06.12 (1).jpeg", 0.5, 0.35),
    "fim":      ("WhatsApp Image 2026-07-03 at 14.38.42 (5).jpeg", 0.5, 0.5),
}
GRELHA = ["salmao", "carpaccio", "carre", "arroz", "pops", "espetada", "tabua", "ninho", "camarao"]


def cobrir(src, w, h, fx, fy):
    im = Image.open(src).convert("RGB")
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def preparar():
    IMG.mkdir(exist_ok=True)
    for k, (f, fx, fy) in FOTO.items():
        cobrir(FOTOS / f, W, H, fx, fy).save(IMG / f"{k}.jpg", quality=90)
        cobrir(FOTOS / f, 360, 640, fx, fy).save(IMG / f"{k}-t.jpg", quality=88)   # quadrado da grelha


def fonte(familia, estilo, peso, ficheiro):
    b64 = base64.b64encode((FONTES / ficheiro).read_bytes()).decode()
    return (f"@font-face{{font-family:'{familia}';font-style:{estilo};font-weight:{peso};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")


CSS = """
:root{--creme:#FBF1EA;--choc:#2E160E;--caramelo:#D38A3E;--verde:#25D366}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:#000}
#palco{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--choc);color:var(--creme);
  font-family:'Noto Serif Display',serif;-webkit-font-smoothing:antialiased}
.shot{position:absolute;inset:0;display:none}
.foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform-origin:50% 50%}
.grelha{position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);gap:6px;padding:6px;background:#000}
.grelha img{width:100%;height:100%;object-fit:cover;display:block;transform-origin:50% 50%}
.sombra{position:absolute;inset:0;background:linear-gradient(0deg,rgba(46,22,14,.96) 0,rgba(46,22,14,.75) 18%,rgba(46,22,14,0) 40%)}
.sombra.topo{background:linear-gradient(180deg,rgba(46,22,14,.55) 0,rgba(46,22,14,0) 14%),linear-gradient(0deg,rgba(46,22,14,.96) 0,rgba(46,22,14,.75) 18%,rgba(46,22,14,0) 40%)}
.tag{position:absolute;top:96px;left:0;right:0;text-align:center;font:600 26px/1 'Work Sans',sans-serif;letter-spacing:.34em;padding-left:.34em;text-transform:uppercase;color:var(--creme);text-shadow:0 2px 12px rgba(0,0,0,.5)}
.tag b{color:var(--caramelo);letter-spacing:0;display:inline-block;width:1.5em;margin-left:-.34em}
.txt{position:absolute;left:70px;right:70px;text-align:center;will-change:transform,opacity}
.t1{font:italic 300 132px/1.02 'Noto Serif Display',serif;letter-spacing:-.015em}
.t1 em{color:var(--caramelo)}
.t2{font:italic 400 76px/1.1 'Noto Serif Display',serif}
.t3{font:500 34px/1.4 'Work Sans',sans-serif;color:#E9D3C6}
.t3 b{color:var(--caramelo);margin:0 .45em}
.pill{display:inline-block;background:var(--creme);color:var(--choc);border-radius:999px;padding:0 44px;height:96px;font:600 34px/96px 'Work Sans',sans-serif;letter-spacing:.14em}
.num{font:600 92px/1 'Work Sans',sans-serif;letter-spacing:.02em;color:var(--creme)}
/* WhatsApp */
.wa{position:absolute;inset:0;background:#ECE5DD}
.wa .cab{position:absolute;top:0;left:0;right:0;height:210px;background:#075E54;display:flex;align-items:flex-end;padding:0 40px 30px;gap:24px;color:#fff}
.wa .cab .av{width:92px;height:92px;border-radius:50%;background:#fff;color:#075E54;font:italic 400 52px/92px 'Noto Serif Display',serif;text-align:center}
.wa .cab .nome{font:600 38px/1.15 'Work Sans',sans-serif}
.wa .cab .nome small{display:block;font:500 26px/1.3 'Work Sans',sans-serif;opacity:.85}
.wa .fundo{position:absolute;top:210px;left:0;right:0;bottom:0;background:#E5DDD5;
  background-image:radial-gradient(rgba(0,0,0,.035) 2px,transparent 2px);background-size:46px 46px}
.wa .balao{position:absolute;right:40px;top:1180px;max-width:760px;background:#DCF8C6;border-radius:26px 6px 26px 26px;padding:26px 34px 22px;font:400 40px/1.3 'Work Sans',sans-serif;color:#111;box-shadow:0 2px 4px rgba(0,0,0,.12);transform-origin:100% 0}
.wa .balao .meta{display:block;text-align:right;font:500 24px/1 'Work Sans',sans-serif;color:#7d8b80;margin-top:12px}
.wa .barra{position:absolute;left:0;right:0;bottom:0;height:150px;background:#F0F0F0;display:flex;align-items:center;gap:20px;padding:0 30px}
.wa .barra .campo{flex:1;height:96px;background:#fff;border-radius:48px;padding:0 40px;font:400 38px/96px 'Work Sans',sans-serif;color:#111;white-space:nowrap;overflow:hidden}
.wa .barra .campo .cur{display:inline-block;width:3px;height:44px;background:#111;vertical-align:-8px;margin-left:2px}
.wa .barra .env{width:96px;height:96px;border-radius:50%;background:#128C7E;display:grid;place-items:center}
.wa .barra .env svg{width:44px;height:44px;fill:#fff;transform:translateX(3px)}
.wa .topo{position:absolute;left:0;right:0;top:300px;text-align:center}
"""

PONTO = "<b>·</b>"


def e(t):
    return html.escape(t, quote=False)


def pagina():
    fontes = (fonte("Noto Serif Display", "italic", "300 400", "noto-serif-display-italic-variable.woff2")
              + fonte("Work Sans", "normal", "300 700", "work-sans-variable.woff2"))
    grelha = "".join(f'<img src="img/{k}-t.jpg">' for k in GRELHA)
    c = CASA
    n1 = len(list((IMG / "v1").glob("*.jpg"))); n2 = len(list((IMG / "v2").glob("*.jpg")))
    return f'''<!doctype html><html lang="pt-PT"><head><meta charset="utf-8"><title>Bom Paladar — vídeo 2</title>
<style>{fontes}{CSS}</style></head><body><div id="palco">

<section class="shot" id="s-gancho">
  <div class="grelha">{grelha}</div>
  <div class="sombra" style="background:linear-gradient(0deg,rgba(46,22,14,.96) 0,rgba(46,22,14,.85) 16%,rgba(46,22,14,.35) 27%,rgba(46,22,14,0) 36%)"></div>
  <p class="tag">Almancil{PONTO}Algarve</p>
  <p class="txt t1" style="top:1500px">Ainda não<br>jantou <em>aqui?</em></p>
</section>

<section class="shot" id="s-bacalhau"><img class="foto" id="v1"><div class="sombra"></div>
  <p class="txt t2" style="top:1560px">Bacalhau Bom Paladar</p>
  <p class="txt t3" style="top:1670px">assinatura da casa</p>
</section>

<section class="shot" id="s-mar"><img class="foto" src="img/arroz.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Do mar.</p></section>
<section class="shot" id="s-salmao"><img class="foto" src="img/salmao.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Do mar.</p></section>
<section class="shot" id="s-caril"><img class="foto" id="v2"><div class="sombra"></div><p class="txt t1" style="top:1520px">Do mar.</p></section>
<section class="shot" id="s-carre"><img class="foto" src="img/carre.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Da terra.</p></section>
<section class="shot" id="s-pops"><img class="foto" src="img/pops.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Da terra.</p></section>
<section class="shot" id="s-tabua"><img class="foto" src="img/tabua.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Para partilhar.</p></section>
<section class="shot" id="s-espetada"><img class="foto" src="img/espetada.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Para partilhar.</p></section>
<section class="shot" id="s-ninho"><img class="foto" src="img/ninho.jpg"><div class="sombra"></div><p class="txt t1" style="top:1520px">Para acabar.</p></section>

<section class="shot" id="s-porta"><img class="foto" src="img/porta.jpg"><div class="sombra topo"></div>
  <p class="tag">Simona’s{PONTO}O Bom Paladar</p>
  <p class="txt t1" style="top:1330px">Chegue.</p>
  <p class="txt t3" style="top:1520px;font-size:40px">{e(c["morada"])}{PONTO}{e(c["terra"])}<br>{e(c["jantar"])}</p>
</section>

<section class="shot" id="s-wa"><div class="wa">
  <div class="cab"><div class="av">S</div><div class="nome">Simona’s O Bom Paladar<small>WhatsApp {e(c["whatsapp"])}</small></div></div>
  <div class="fundo"></div>
  <p class="topo t1" style="color:var(--choc);font-size:118px">Reserve.<br><span style="font-size:60px;color:#6b4535">É uma mensagem.</span></p>
  <div class="balao" id="balao">Olá! Mesa para 2, sexta às 20h?<span class="meta">20:14 ✓✓</span></div>
  <div class="barra"><div class="campo"><span id="digita"></span><span class="cur" id="cur"></span></div>
    <div class="env"><svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg></div></div>
</div></section>

<section class="shot" id="s-fim"><img class="foto" src="img/tachos.jpg"><div class="sombra topo"></div>
  <p class="tag">Simona’s{PONTO}O Bom Paladar</p>
  <p class="txt t1" style="top:1150px">Sente-se.</p>
  <p class="txt" style="top:1370px"><span class="pill">RESERVE PELO WHATSAPP</span></p>
  <p class="txt num" style="top:1520px">{e(c["whatsapp"])}</p>
  <p class="txt t3" style="top:1660px;font-size:36px">{e(c["morada"])}{PONTO}{e(c["terra"])}{PONTO}{e(c["site"])}<br>{e(c["jantar"])}</p>
</section>

</div>
<script>
const FPS={FPS}, N1={n1}, N2={n2};
const $=id=>document.getElementById(id);
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const ease=x=>1-Math.pow(1-x,3);
const MSG="Olá! Mesa para 2, sexta às 20h?";
// timeline (segundos)
const T=[
 ["s-gancho",0,2.2],["s-bacalhau",2.2,5.0],
 ["s-mar",5.0,6.0],["s-salmao",6.0,6.9],["s-caril",6.9,8.2],["s-carre",8.2,9.1],["s-pops",9.1,10.1],
 ["s-tabua",10.1,11.1],["s-espetada",11.1,12.0],["s-ninho",12.0,13.2],
 ["s-porta",13.2,17.0],["s-wa",17.0,21.0],["s-fim",21.0,24.5]];
const DUR=24.5;
function kb(el,tl,dur,from,to,ox,oy){{const p=ease(clamp(tl/dur,0,1));const s=from+(to-from)*p;el.style.transformOrigin=ox+"% "+oy+"%";el.style.transform="scale("+s.toFixed(4)+")";}}
function rise(el,tl,t0,d=.35,dy=40){{const p=ease(clamp((tl-t0)/d,0,1));el.style.opacity=p;el.style.transform="translateY("+((1-p)*dy).toFixed(1)+"px)";}}
function render(t){{
  for(const [id,a,b] of T){{const el=$(id);const on=t>=a&&t<b;el.style.display=on?"block":"none";if(!on)continue;const tl=t-a,dur=b-a;
    const foto=el.querySelector(".foto"),txts=el.querySelectorAll(".txt");
    switch(id){{
      case "s-gancho":{{const imgs=el.querySelectorAll(".grelha img");imgs.forEach((im,i)=>{{const p=ease(clamp((tl-i*.09)/.22,0,1));im.style.opacity=p;im.style.transform="scale("+(0.72+0.28*p).toFixed(3)+")";}});
        rise(txts[0],tl,1.0,.4,60);el.querySelector(".tag").style.opacity=clamp((tl-.5)/.3,0,1);
        const z=ease(clamp((tl-1.9)/.3,0,1));el.querySelector(".grelha").style.transform="scale("+(1+z*2.2).toFixed(3)+")";el.querySelector(".grelha").style.transformOrigin="50% 50%";break;}}
      case "s-bacalhau":{{const i=clamp(Math.round(tl*FPS)+1,1,N1);foto.src="img/v1/"+String(i).padStart(3,"0")+".jpg";foto.style.transform="scale(1.06)";rise(txts[0],tl,.25);rise(txts[1],tl,.45);break;}}
      case "s-caril":{{const i=clamp(Math.round(tl*FPS)+1,1,N2);foto.src="img/v2/"+String(i).padStart(3,"0")+".jpg";foto.style.transform="scale(1.06)";rise(txts[0],tl,0,.2,20);break;}}
      case "s-porta":{{kb(foto,tl,dur,1.0,1.18,50,42);rise(txts[0],tl,.3,.5,50);rise(txts[1],tl,.9,.5,30);break;}}
      case "s-wa":{{const n=clamp(Math.floor((tl-.5)/1.6*MSG.length),0,MSG.length);$("digita").textContent=MSG.slice(0,n);$("cur").style.opacity=(tl<2.2&&Math.floor(tl*3)%2===0)?1:0;
        const sent=tl>=2.35;$("digita").textContent=sent?"":MSG.slice(0,n);const p=ease(clamp((tl-2.35)/.3,0,1));const bal=$("balao");bal.style.opacity=sent?1:0;bal.style.transform="scale("+(0.6+0.4*p).toFixed(3)+")";
        const tp=el.querySelector(".topo");tp.style.opacity=ease(clamp((tl-.15)/.35,0,1));break;}}
      case "s-fim":{{kb(foto,tl,dur,1.02,1.12,50,80);rise(txts[0],tl,.2,.45,50);rise(txts[1],tl,.6,.4,30);rise(txts[2],tl,.8,.4,30);rise(txts[3],tl,1.0,.4,20);
        const p=$("s-fim").querySelector(".pill");p.style.transform="scale("+(1+0.03*Math.sin(tl*4)).toFixed(3)+")";break;}}
      default:{{const [ox,oy]=[[40,50],[60,45],[50,60],[45,50],[55,55],[50,40]][Math.abs(id.length*7)%6];kb(foto,tl,dur,1.0,1.10,ox,oy);rise(txts[0],tl,0,.25,30);}}
    }}
  }}
}}
window.render=render;window.DUR=DUR;
const q=new URLSearchParams(location.search);if(q.get("t"))render(parseFloat(q.get("t")));
</script></body></html>'''


RENDER_JS = r"""
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, html, outdir, fps] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);
  // pré-carregar as sequências de vídeo e as fotos
  await p.evaluate(async () => {
    const urls = [...document.querySelectorAll('img')].map(i => i.getAttribute('src')).filter(Boolean);
    for (let k = 1; k <= 76; k++) urls.push('img/v1/' + String(k).padStart(3, '0') + '.jpg');
    for (let k = 1; k <= 40; k++) urls.push('img/v2/' + String(k).padStart(3, '0') + '.jpg');
    await Promise.all(urls.map(u => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = u; })));
  });
  const dur = await p.evaluate(() => window.DUR);
  const n = Math.round(dur * fps);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => window.render(t), f / fps);
    await p.screenshot({ path: path.join(outdir, String(f).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 93 });
    if (f % 60 === 0) console.log('frame', f, '/', n);
  }
  await b.close();
})();
"""


def folha():
    """Folha de revisão: 8 frames-chave lado a lado."""
    ts = [0.6, 1.6, 3.5, 6.5, 10.5, 15.0, 19.6, 23.0]
    th = 640; tw = 360
    f = Image.new("RGB", (len(ts) * (tw + 12) + 12, th + 70), (27, 27, 27))
    d = ImageDraw.Draw(f); fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    for i, t in enumerate(ts):
        im = Image.open(FRAMES / f"{round(t * FPS):04d}.jpg").resize((tw, th), Image.LANCZOS)
        f.paste(im, (12 + i * (tw + 12), 12)); d.text((12 + i * (tw + 12), th + 30), f"{t:.1f} s", fill=(214, 178, 94), font=fnt)
    f.save(AQUI / "folha-revisao.png")


def main():
    preparar()
    (AQUI / "video.html").write_text(pagina(), encoding="utf-8")
    (AQUI / "render.js").write_text(RENDER_JS)
    if "--so-html" in sys.argv:
        return
    FRAMES.mkdir(exist_ok=True)
    for f in FRAMES.glob("*.jpg"):
        f.unlink()
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    subprocess.run(["node", str(AQUI / "render.js"), str(AQUI / "video.html"), str(FRAMES), str(FPS)],
                   check=True, cwd=AQUI, env={**os.environ, "NODE_PATH": npm})
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-framerate", str(FPS),
                    "-i", str(FRAMES / "%04d.jpg"), "-c:v", "libx264", "-preset", "slow", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(AQUI / "Bom-Paladar-video-2.mp4")], check=True)
    folha()


if __name__ == "__main__":
    main()
