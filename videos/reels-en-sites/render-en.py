"""Reels EN do Hanam e do Jasmim 2 (9:16, com som).
Uso: python3 render-en.py [hanam] [jasmim]   (precisa de Playwright, ffmpeg e numpy)
Base: videos/prontos/<nome>-ad-4x5.mp4 (ramo claude/awesome-knuth-8hnx4j). Títulos em tit-en.html, som em som-en.py."""
import asyncio, os, sys, subprocess, json
from playwright.async_api import async_playwright
SP = os.path.dirname(os.path.abspath(__file__))
PRONTOS = os.path.join(SP, "..", "prontos")
FPS, FECHO = 30, 3.0
INICIO = .55  # os vídeos de base abrem e fecham com 0,5 s de fade a preto: corta-se para o 1.º fotograma já mostrar o site
VIDS = {  # vídeo de base, duração útil (sem os fades), deslocamento vertical (igual a V.y em tit-en.html)
    "hanam": ("hanam-quarteira-ad-4x5.mp4", 35.15, 170, "reel-en-hanam-9x16.mp4"),
    "jasmim": ("jasmim-2-ad-4x5.mp4", 26.08, 330, "reel-en-jasmim-9x16.mp4"),
}


async def frames(which):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for v in which:
            _, dur, _, _ = VIDS[v]
            total = dur + FECHO
            ts = set()
            for a, z in [(0, 2.1), (dur - .2, dur + 1.1)]:
                n = int(round((z - a) * FPS))
                ts |= {round(a + i / FPS, 4) for i in range(n + 1)}
            ts = sorted(ts)
            d = f"{SP}/fr_{v}"; os.makedirs(d, exist_ok=True)
            await pg.goto(f"file://{SP}/tit-en.html?v={v}&d={dur}", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready.then(()=>1)")
            lines = []
            for i, t in enumerate(ts):
                await pg.evaluate(f"setT({t})")
                f = f"{d}/{i:05d}.png"
                await pg.screenshot(path=f, omit_background=True)
                nxt = ts[i + 1] if i + 1 < len(ts) else total
                lines.append(f"file '{f}'\nduration {nxt - t:.4f}\n")
            lines.append(f"file '{d}/{len(ts)-1:05d}.png'\n")
            open(f"{d}/list.txt", "w").write("".join(lines))
            print(v, len(ts), "frames", flush=True)
        await b.close()


def build(v):
    src, dur, y, out = VIDS[v]
    total = dur + FECHO
    d = f"{SP}/fr_{v}"
    json.dump({"style": v, "dur": total, "end": dur}, open(f"{d}/som.json", "w"))
    subprocess.run(["python3", f"{SP}/som-en.py", f"{d}/som.json", f"{d}/som.wav"], check=True)
    # fundo preto com a duração total; o vídeo fica parado no último fotograma por baixo do fecho
    fc = (f"color=black:s=1080x1920:r=30:d={total:.3f}[c];[0:v]trim=start={INICIO}:duration={dur},setpts=PTS-STARTPTS,fps=30[b];"
          f"[c][b]overlay=0:{y}:eof_action=repeat[bg];"
          "[1:v]fps=30,format=rgba[o];[bg][o]overlay=0:0:eof_action=repeat:format=auto,format=yuv420p[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", f"{PRONTOS}/{src}", "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt",
           "-i", f"{d}/som.wav", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "7M", "-bufsize", "14M",
           "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{SP}/{out}"]
    subprocess.run(cmd, check=True)
    # capa: fotograma com o título completo
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2.5", "-i", f"{SP}/{out}", "-frames:v", "1", "-q:v", "3",
                    f"{SP}/{out.replace('-9x16.mp4', '-capa.jpg')}"], check=True)
    print("ok", out, flush=True)


which = sys.argv[1:] or list(VIDS)
asyncio.run(frames(which))
for v in which:
    build(v)
