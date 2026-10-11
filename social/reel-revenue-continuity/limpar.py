#!/usr/bin/env python3
"""Tira a camada de texto do reel composto (cartões a ~83 % de opacidade + texto + linha de progresso + rótulos).
1) desfaz a tinta dos cartões (in = k*out + c, ajustado em 12 fotogramas) → recupera o fundo por baixo;
2) máscara: rebordos dos cartões, texto (limiar no fotograma original dentro das caixas de texto), linha e pontos, rótulos;
3) cv2.inpaint (Telea) na máscara.
Uso: python3 limpar.py in.mp4 out.mp4 [t1,t2,...]  (com tempos: grava só esses fotogramas em fr/clean_<t>.jpg)"""
import sys, subprocess, numpy as np, cv2
W, H, FPS = 1080, 1920, 30
# tinta dos cartões: varia linearmente em y (ajuste nas arestas de cima e de baixo de cada cartão, 20 fotogramas)
TINT = {0: ((183, (0.262, 0.278, 0.271), (4.7, 7.4, 12.1)), (687, (0.176, 0.187, 0.19), (12.0, 11.2, 14.7))),
        1: ((1114, (0.149, 0.151, 0.109), (14.1, 15.6, 21.1)), (1306, (0.218, 0.222, 0.222), (10.9, 13.8, 20.3)))}
CARDS = [(51, 181, 1029, 690), (51, 1112, 1029, 1309)]   # x0,y0,x1,y1 do interior
R = 30
TXT = [(70, 200, 1010, 520, 60), (70, 1140, 1010, 1228, 60), (55, 78, 290, 142, 45), (55, 1496, 620, 1544, 40), (55, 1826, 600, 1864, 40)]
DOTS = [135, 300, 470, 640, 810, 935]; DY = 841


def rrect(mask, x0, y0, x1, y1, r, val=255, th=-1):
    cv2.rectangle(mask, (x0 + r, y0), (x1 - r, y1), val, th)
    cv2.rectangle(mask, (x0, y0 + r), (x1, y1 - r), val, th)
    for cx, cy in [(x0 + r, y0 + r), (x1 - r, y0 + r), (x0 + r, y1 - r), (x1 - r, y1 - r)]:
        cv2.circle(mask, (cx, cy), r, val, th)


FILL = np.zeros((H, W), np.uint8)
KMAP = np.ones((H, 1, 3), np.float32); CMAP = np.zeros((H, 1, 3), np.float32)
for i, (x0, y0, x1, y1) in enumerate(CARDS):
    rrect(FILL, x0 + 2, y0 + 2, x1 - 2, y1 - 2, R)
    (ya, ka, ca), (yb, kb, cb) = TINT[i]
    for y in range(y0 - 2, y1 + 3):
        t = (y - ya) / (yb - ya)
        KMAP[y, 0] = np.array(ka) + t * (np.array(kb) - np.array(ka)); CMAP[y, 0] = np.array(ca) + t * (np.array(cb) - np.array(ca))
BORDER = np.zeros((H, W), np.uint8)
for x0, y0, x1, y1 in CARDS:
    outer = np.zeros((H, W), np.uint8); inner = np.zeros((H, W), np.uint8)
    rrect(outer, x0 - 7, y0 - 7, x1 + 7, y1 + 7, R + 7)
    rrect(inner, x0 + 4, y0 + 4, x1 - 4, y1 - 4, R - 4)
    BORDER |= outer & ~inner
LINE = np.zeros((H, W), np.uint8)
cv2.rectangle(LINE, (118, DY - 7), (952, DY + 7), 255, -1)
KER = np.ones((5, 5), np.uint8)


OUTSIDE = np.zeros((H, W), bool); OUTSIDE[700:1100] = True; OUTSIDE[1320:1750] = True
FEATHER = cv2.GaussianBlur(FILL.astype(np.float32) / 255, (0, 0), 6)[:, :, None]
EDGES = {0: [(183, 172), (687, 697)], 1: [(1114, 1104), (1306, 1316)]}   # (y interior, y exterior) por cartão


def fit_edge(o, yi, yo, k0, c0):
    """ajuste k,c por canal com prior (ridge) para o modelo global; pares interior/exterior na aresta"""
    I = o[yi - 1:yi + 2, 60:1020].reshape(-1, 3); O = o[yo - 1:yo + 2, 60:1020].reshape(-1, 3)
    ks = []; cs = []
    for ch in range(3):
        x = np.r_[O[:, ch], np.linspace(0, 255, 1500)]
        y = np.r_[I[:, ch], k0[ch] * np.linspace(0, 255, 1500) + c0[ch]]
        A = np.c_[x, np.ones(len(x))]
        k, c = np.linalg.lstsq(A, y, rcond=None)[0]
        ks.append(max(k, 0.15)); cs.append(c)
    return np.array(ks), np.array(cs)


def clean(f):
    f = np.ascontiguousarray(f).copy()
    o = f.astype(np.float32)
    orig = o
    # 1) texto, rebordos, linha e pontos: inpaint ainda sobre o fotograma composto (antes de desfazer a tinta)
    mask = BORDER | LINE
    for x0, y0, x1, y1, th in TXT:
        box = o[y0:y1, x0:x1].max(axis=2) > th
        mask[y0:y1, x0:x1] |= box.astype(np.uint8) * 255
    for x in DOTS:
        r, g, b = o[DY, x]
        active = r > 150 and g < 150
        cv2.circle(mask, (x, DY), 46 if active else 28, 255, -1)
    mask = cv2.dilate(mask, KER)
    o = cv2.inpaint(f, mask, 6, cv2.INPAINT_TELEA).astype(np.float32)
    # 2) desfazer a tinta dos cartões (ajuste por fotograma nas arestas, interpolado em y)
    kmap = KMAP.copy(); cmap = CMAP.copy()
    for i, (x0, y0, x1, y1) in enumerate(CARDS):
        (ya, ka, ca), (yb, kb, cb) = TINT[i]
        (yi1, yo1), (yi2, yo2) = EDGES[i]
        k1, c1 = fit_edge(orig, yi1, yo1, ka, ca); k2, c2 = fit_edge(orig, yi2, yo2, kb, cb)
        for y in range(y0 - 2, y1 + 3):
            t = (y - yi1) / (yi2 - yi1)
            kmap[y, 0] = k1 + t * (k2 - k1); cmap[y, 0] = c1 + t * (c2 - c1)
    v = np.clip((o - cmap) / kmap, 0, 255)
    # a croma recuperada é ruído (o cartão era ~90 % opaco): a cor vem de uma tabela luma→croma aprendida no resto do
    # fotograma (escuro = neutro, claro = laranja), como numa colorização; a luma fica com desfoque leve
    yuv = cv2.cvtColor(v.astype(np.uint8), cv2.COLOR_RGB2YUV).astype(np.float32)
    ref = cv2.cvtColor(o.astype(np.uint8), cv2.COLOR_RGB2YUV).astype(np.float32)
    outs = ref[OUTSIDE][::3]
    bins = np.minimum((outs[:, 0] // 16).astype(int), 15)
    lut = np.zeros((16, 2), np.float32); have = np.zeros(16, bool)
    for b in range(16):
        sel = bins == b
        if sel.sum() > 40:
            lut[b] = np.median(outs[sel, 1:], axis=0); have[b] = True
    idx = np.where(have)[0]
    for b in range(16):
        if not have[b]:
            lut[b] = lut[idx[np.argmin(np.abs(idx - b))]]
    Y = cv2.GaussianBlur(yuv[:, :, 0], (0, 0), 1.6)
    yb = np.minimum((Y // 16).astype(int), 15)
    yuv[:, :, 0] = Y
    yuv[:, :, 1] = cv2.GaussianBlur(lut[yb, 0], (0, 0), 4)
    yuv[:, :, 2] = cv2.GaussianBlur(lut[yb, 1], (0, 0), 4)
    v = cv2.cvtColor(np.clip(yuv, 0, 255).astype(np.uint8), cv2.COLOR_YUV2RGB).astype(np.float32)
    u = o * (1 - FEATHER) + v * FEATHER
    return np.clip(u, 0, 255).astype(np.uint8)


src, dst = sys.argv[1], sys.argv[2]
if len(sys.argv) > 3:
    for t in sys.argv[3].split(','):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', t, '-i', src, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
        f = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
        cv2.imwrite(f'fr/clean_{t}.jpg', cv2.cvtColor(clean(f), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 92])
    sys.exit()
# troço opcional (segundos) para correr em paralelo: SEG=inicio,duracao
import os
seg = []
if os.environ.get('SEG'):
    a, d = os.environ['SEG'].split(','); seg = ['-ss', a, '-t', d]
dec = subprocess.Popen(['ffmpeg', '-v', 'error'] + seg + ['-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', dst], stdin=subprocess.PIPE)
n = 0
while True:
    raw = dec.stdout.read(W * H * 3)
    if len(raw) < W * H * 3:
        break
    f = np.frombuffer(raw, np.uint8).reshape(H, W, 3)
    enc.stdin.write(clean(f).tobytes()); n += 1
    if n % 150 == 0:
        print(n, flush=True)
enc.stdin.close(); enc.wait(); dec.wait()
print('ok', n)
