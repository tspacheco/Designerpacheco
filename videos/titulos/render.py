import asyncio, os, sys, subprocess
from playwright.async_api import async_playwright
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SP = os.path.dirname(os.path.abspath(__file__))
FPS = 30
VIDS = {  # duração, janelas animadas (s)
    "bolta": (67.27, [(0.4, 1.6), (60.6, 62.2)]),
    "hanam": (36.20, [(0.4, 1.6)]),
    "jasmim": (27.13, [(0.4, 1.6)]),
}
async def main(which):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for v in which:
            dur, wins = VIDS[v]
            ts = {0.0}
            for a, z in wins:
                n = int(round((z - a) * FPS))
                ts |= {round(a + i / FPS, 4) for i in range(n + 1)}
            ts = sorted(ts)
            d = f"{SP}/fr_{v}"; os.makedirs(d, exist_ok=True)
            await pg.goto(f"file://{SP}/tit.html?v={v}", wait_until="networkidle")
            await pg.evaluate("document.fonts.ready.then(()=>1)")
            lines = []
            for i, t in enumerate(ts):
                await pg.evaluate(f"setT({t})")
                f = f"{d}/{i:05d}.png"
                await pg.screenshot(path=f, omit_background=True)
                nxt = ts[i + 1] if i + 1 < len(ts) else dur
                lines.append(f"file '{f}'\nduration {nxt - t:.4f}\n")
            lines.append(f"file '{d}/{len(ts)-1:05d}.png'\n")
            open(f"{d}/list.txt", "w").write("".join(lines))
            print(v, len(ts), "frames", flush=True)
        await b.close()
    for v in which:
        d = f"{SP}/fr_{v}"
        cmd = [FF, "-v", "error", "-y", "-i", f"{SP}/../{v}.mp4",
               "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt",
               "-filter_complex", "[1:v]fps=30,format=rgba[o];[0:v][o]overlay=0:0:eof_action=repeat:format=auto[v]",
               "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
               "-maxrate", "6M", "-bufsize", "12M", "-pix_fmt", "yuv420p", "-c:a", "copy",
               "-movflags", "+faststart", f"{SP}/{v}-titulo-ro-4x5.mp4"]
        subprocess.run(cmd, check=True); print("ok", v, flush=True)
asyncio.run(main(sys.argv[1:] or list(VIDS)))
