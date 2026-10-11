// Mini-vídeo do carrossel: cada slide entra por partes (topo, título, texto, diagrama, cartões),
// fica o tempo de leitura e sai em fade para o seguinte. Fotograma a fotograma, sem relógio real.
// Uso: NODE_PATH=$(npm root -g) node video.js saida/carrossel-ro-video.html pasta-fotogramas [fps]
// MP4 (4:5): ffmpeg -framerate 30 -i pasta/%05d.jpg -f lavfi -i anullsrc=r=48000:cl=stereo
//   -vf "scale=1080:1350:out_color_matrix=bt709:out_range=tv,format=yuv420p" -c:v libx264 -preset slow -crf 19
//   -profile:v high -level 4.1 -colorspace bt709 -color_primaries bt709 -color_trc bt709 -g 60 -sc_threshold 0
//   -c:a aac -b:a 128k -shortest -movflags +faststart saida/video/pacheco-audit-ro.mp4
// 9:16: o mesmo com -filter_complex "[0:v]split[a][b];[a]scale=1536:1920,crop=1080:1920,boxblur=40:2,
//   eq=brightness=-0.12:saturation=0.9[bg];[bg][b]overlay=0:285,..." → saida/video/pacheco-audit-ro-9x16.mp4
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [html, pasta, fpsArg] = process.argv.slice(2);
  const FPS = Number(fpsArg || 30);
  fs.mkdirSync(pasta, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(html));
  await p.evaluate(() => document.fonts.ready);

  const total = await p.evaluate(() => {
    const css = document.createElement('style');
    css.textContent = `body{margin:0;width:1080px;height:1350px;overflow:hidden;background:#0d0e11}
      .slide{position:absolute!important;left:0;top:0;margin:0!important}
      .barra{position:absolute;left:0;bottom:0;height:6px;background:#FF6A3B;z-index:50}`;
    document.head.appendChild(css);
    const barra = document.createElement('div');
    barra.className = 'barra';
    document.body.appendChild(barra);

    const slides = [...document.querySelectorAll('.slide')];
    const ease = x => 1 - Math.pow(1 - x, 3);
    const SAIDA = 0.45;   // fade do slide anterior por cima do novo
    // Tempo de leitura: 1,6 s + 1 s por cada 18 palavras; o último fica mais 1,5 s
    const plano = slides.map((s, i) => {
      const palavras = s.innerText.split(/\s+/).filter(Boolean).length;
      const anim = [];
      let t = 0;
      const add = (el, inicio, dy = 24, dur = 0.55) => el && anim.push({ el, inicio, dy, dur });
      add(s.querySelector('.top'), 0, 0, 0.5);
      add(s.querySelector('.pag'), 0.2, 0, 0.5);
      add(s.querySelector('.rod'), 0.2, 0, 0.5);
      add(s.querySelector('.kicker'), 0.15, 16);
      add(s.querySelector('h1'), 0.25, 34, 0.7);
      add(s.querySelector('.sub'), 0.65, 22);
      t = 0.95;
      const diag = s.querySelector('.diag');
      if (diag) {
        [...diag.children].forEach((el, k) => add(el, t + k * 0.035, el.classList.contains('l') ? 0 : 10, 0.4));
        t += diag.children.length * 0.035 + 0.25;
      }
      s.querySelectorAll('.legenda, .cartao, .c4 > div, .nota, .pill, .botao, .orbita').forEach(el => {
        add(el, t, 18); t += 0.14;
      });
      const dur = 1.6 + palavras / 18 + (i === slides.length - 1 ? 1.5 : 0);
      return { s, anim, dur };
    });
    let acc = 0;
    plano.forEach(x => { x.t0 = acc; acc += x.dur; });

    window.__pinta = T => {
      let i = plano.findIndex(x => T < x.t0 + x.dur);
      if (i < 0) i = plano.length - 1;
      plano.forEach((x, k) => {
        x.s.style.display = (k === i || (k === i - 1 && T - plano[i].t0 < SAIDA)) ? '' : 'none';
        x.s.style.zIndex = k === i ? 1 : 2;
        x.s.style.opacity = 1;
        x.s.style.transform = 'none';
      });
      const atual = plano[i];
      const local = T - atual.t0;
      // O 1.º slide já está inteiro no 1.º fotograma (o gancho aparece logo na pré-visualização)
      atual.anim.forEach(a => {
        const pr = i === 0 ? 1 : ease(Math.min(1, Math.max(0, (local - a.inicio) / a.dur)));
        a.el.style.opacity = pr;
        a.el.style.translate = a.dy ? `0 ${(1 - pr) * a.dy}px` : '0 0';
      });
      if (i > 0 && local < SAIDA) {
        const ant = plano[i - 1];
        const pr = ease(local / SAIDA);
        ant.anim.forEach(a => { a.el.style.opacity = 1; a.el.style.translate = '0 0'; });
        ant.s.style.opacity = 1 - pr;
        ant.s.style.transform = `translateX(${-60 * pr}px)`;
      }
      // O ponto laranja da órbita pulsa, para haver movimento desde o 1.º segundo
      const ponto = atual.s.querySelector('.orbita em');
      if (ponto) {
        const k = (Math.sin(T * Math.PI * 1.2) + 1) / 2;
        ponto.style.boxShadow = `0 0 0 ${10 + 16 * k}px rgba(255,106,59,${0.22 - 0.12 * k})`;
      }
      barra.style.width = (1080 * Math.min(1, T / acc)) + 'px';
    };
    return acc;
  });

  const n = Math.ceil(total * FPS);
  for (let f = 0; f < n; f++) {
    await p.evaluate(T => window.__pinta(T), f / FPS);
    await p.screenshot({ path: path.join(pasta, String(f).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 93 });
  }
  console.log(n, 'fotogramas,', total.toFixed(1), 's');
  await b.close();
})();
