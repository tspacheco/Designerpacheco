#!/usr/bin/env python3
"""Música dos reels das demos, sintetizada com numpy (sem samples nem direitos de terceiros).
Três estilos, escolhidos pelo tipo de negócio no reels.json; a semente (o slug) muda o tom,
a melodia e os pormenores, por isso dois reels do mesmo estilo nunca soam iguais.
  urbano : boom-bap, menor, caixa seca, baixo sub e pluck pentatónico, chiado de vinil (barbearias, tatuagens, oficinas)
  quente : lo-fi, maior 7.ª, Rhodes e escovas, ruído de sala (padarias, cafés, flores, beleza, roupa)
  energia: house, 4 no chão, baixo em contratempo, acordes cortados (auto, lavandarias, bicicletas, desporto)
No fim (campo «end») a música abre num acorde longo para o ecrã final.
Uso: python3 som-demos.py musica.json saida.wav   (json: style, bpm, dur, end, seed)"""
import json, sys, wave, zlib
import numpy as np

SR = 48000
ev = json.load(open(sys.argv[1]))
STYLE, BPM, DUR, END = ev["style"], float(ev["bpm"]), float(ev["dur"]), float(ev["end"])
SEED = zlib.crc32(ev.get("seed", "x").encode())
N = int(SR * DUR)
rng = np.random.default_rng(SEED)
mus = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(d * SR)) / SR
noise = lambda d: rng.uniform(-1, 1, int(d * SR))
smooth = lambda x, w: np.convolve(x, np.ones(w) / w, mode="same")
BEAT = 60 / BPM; BAR = 4 * BEAT
T = int(rng.integers(-3, 3))  # transposição pela semente


def put(t0, sig, amp=1.0):
    i0 = int(t0 * SR)
    if 0 <= i0 < N:
        sig = sig[:N - i0]; mus[i0:i0 + len(sig)] += amp * sig


def kick(dec=8, lo=48):
    x = tt(.4); f = lo + 90 * np.exp(-x * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * dec) + .2 * noise(.4) * np.exp(-x * 250)


def snare():
    x = tt(.25); n = noise(.25); n = n - smooth(n, 3)
    return .7 * n * np.exp(-x * 22) + .5 * np.sin(2 * np.pi * 190 * x) * np.exp(-x * 30)


def clap():
    s = np.zeros(int(.2 * SR))
    for k, o in enumerate((0, .012, .024)):
        x = tt(.2 - o); n = noise(.2 - o); n = n - smooth(n, 4)
        s[int(o * SR):] += n * np.exp(-x * (40 if k < 2 else 18))
    return s * .6


def hat(d=.05, dec=90):
    x = tt(d); n = noise(d); n = n - smooth(n, 3)
    return n * np.exp(-x * dec)


def shaker():
    x = tt(.09); n = noise(.09); n = n - smooth(n, 2)
    return n * np.sin(np.pi * x / .09) * .5


def sub(m, d):
    x = tt(d)
    return np.tanh(1.4 * np.sin(2 * np.pi * hz(m) * x)) * np.minimum(1, x * 80) * np.clip((d - x) / .08, 0, 1)


def pluck(m, d=.45, bright=.5):
    x = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(4 * np.pi * f * x) + .15 * np.sin(6 * np.pi * f * x)) * np.exp(-x * 8) * np.minimum(1, x * 500)


def epiano(notes, d=.6):
    x = tt(d)
    s = sum(np.sin(2 * np.pi * hz(m) * x + 1.0 * np.sin(2 * np.pi * hz(m) * x) * np.exp(-x * 6)) for m in notes) / len(notes)
    return s * np.exp(-x * 2.6) * np.minimum(1, x * 200) * (1 + .12 * np.sin(2 * np.pi * 4.5 * x))


def pad(notes, d, att=.6, rel=1.2):
    x = tt(d); env = np.minimum(1, x / att) * np.clip((d - x) / rel, 0, 1)
    return env * sum(np.sin(2 * np.pi * hz(m) * x * (1 + .002 * j) + j) for j, m in enumerate(notes)) / len(notes)


def riser(d):
    x = tt(d); n = noise(d); env = (x / d) ** 2
    return (n - smooth(n, 12)) * env * .8


def impact():
    x = tt(2.5)
    return np.sin(2 * np.pi * np.cumsum(40 + 70 * np.exp(-x * 12)) / SR) * np.exp(-x * 2.2) + .3 * noise(2.5) * np.exp(-x * 9)



def chords(base, kinds):
    return [(base + r + T, [base + 12 + r + T + i for i in ch]) for r, ch in kinds]


nb = int(END / BAR) + 1
if STYLE == "urbano":
    prog = chords(45, [(0, [0, 3, 7]), (-4, [0, 4, 7]), (-9, [0, 3, 7, 10]), (-5, [0, 4, 7])])  # i VI iv v
    penta = [69 + T + i for i in (0, 3, 5, 7, 10, 12)]
    pat = rng.permutation(8)
    for b in range(nb):
        t0 = b * BAR; root, ch = prog[b % 4]
        for k in range(4):
            tb = t0 + k * BEAT
            if tb >= END: break
            if k in (0, 2): put(tb + (BEAT / 2 if k == 2 and b % 2 else 0), kick(), .9)  # bombo atrasado nos compassos ímpares
            if b >= 1 and k in (1, 3): put(tb, snare(), .45); put(tb + .01, clap(), .25)
            for h in (0, .5):
                if tb + h * BEAT < END: put(tb + h * BEAT + (.03 if h else 0), hat(), .14 if h else .2)  # swing ligeiro
        put(t0, sub(root - 12, BEAT * 1.6), .5); put(t0 + BEAT * 2.75, sub(root - 12, BEAT * .9), .4)
        put(t0, pad(ch, BAR + .3, .3, .5), .09)
        if b >= 2:
            for k in range(8):
                if pat[k] % 3 != 1 and t0 + k * BEAT / 2 < END:
                    put(t0 + k * BEAT / 2, pluck(penta[(pat[k] + b * 2) % 6], .4, .35), .12)
    s = noise(END); crackle = (rng.random(len(s)) > .9994) * rng.uniform(.4, 1, len(s))
    put(0, (smooth(s, 40) * .4 + smooth(crackle, 5) * 2.5), .35)  # vinil
    fin = [prog[0][0], *prog[0][1], prog[0][1][0] + 12]
elif STYLE == "quente":
    prog = chords(41, [(0, [0, 4, 7, 11]), (-1, [0, 3, 7, 10]), (-3, [0, 3, 7, 10]), (-5, [0, 4, 7, 11])])  # IΔ VIIm7 VIm7 VΔ
    for b in range(nb):
        t0 = b * BAR; root, ch = prog[b % 4]
        for k in range(4):
            tb = t0 + k * BEAT
            if tb >= END: break
            if k in (0, 2) or (k == 3 and b % 2): put(tb + (BEAT / 2 if k == 3 else 0), kick(10, 50), .6)
            if b >= 1 and k in (1, 3): put(tb, snare(), .18)
            for h in (0, .5):
                if tb + h * BEAT < END: put(tb + h * BEAT + (.05 if h else 0), shaker(), .1)
            if b >= 1 and k in (0, 2) and tb + BEAT * .5 < END: put(tb + BEAT * (.5 if k else 0), epiano(ch, .9), .17)
        put(t0, sub(root - 12, BEAT * 1.8), .32); put(t0 + BEAT * 2.5, sub(root - 5, BEAT * 1.2), .25)
        put(t0, pad([m + 12 for m in ch[1:]], BAR + .4), .05)
    x = tt(END); room = smooth(smooth(noise(END), 50), 30)
    put(0, room * 2.2 * (.7 + .3 * np.sin(2 * np.pi * x / 5)), .4)  # sala
    fin = [prog[0][0], *prog[0][1], prog[0][1][1] + 12]
else:  # energia
    prog = chords(43, [(0, [0, 3, 7, 10]), (-2, [0, 4, 7]), (-4, [0, 4, 7, 11]), (-7, [0, 3, 7])])
    for b in range(nb):
        t0 = b * BAR; root, ch = prog[b % 4]
        for k in range(4):
            tb = t0 + k * BEAT
            if tb >= END: break
            put(tb, kick(9, 46), .85)
            if b >= 1 and k in (1, 3): put(tb, clap(), .35)
            if tb + BEAT / 2 < END:
                put(tb + BEAT / 2, hat(.08, 40), .2)  # aberto no contratempo
                put(tb + BEAT / 2, sub(root - 12, BEAT * .4), .42)
            for h in (.25, .75):
                if tb + h * BEAT < END: put(tb + h * BEAT, hat(), .09)
            if b >= 1:
                for h in (.5, .75) if (b + k) % 2 else (.5,):
                    if tb + h * BEAT < END: put(tb + h * BEAT, pad(ch, .16, .005, .05), .14)  # acorde cortado
        put(t0, pad([m + 12 for m in ch], BAR + .2, .8, .4), .04)
    fin = [prog[0][0], *prog[0][1], prog[0][1][0] + 12]

put(END - 1.6, riser(1.6), .3)
put(END, impact(), .5)
put(END, pad(fin, DUR - END, .05, 2.4), .3)
put(END, epiano(fin[1:], 2.8), .25)

m = mus * np.minimum(1, tt(DUR) / .03)
m = np.tanh(1.2 * m / (np.max(np.abs(m)) + 1e-9)) * .9
m /= np.max(np.abs(m)); m *= .89
pcm = (m * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("som", STYLE, f"{BPM:g} BPM", f"{DUR:.2f}s")
