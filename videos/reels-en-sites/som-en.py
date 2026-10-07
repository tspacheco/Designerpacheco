#!/usr/bin/env python3
"""Som dos reels EN do Hanam e do Jasmim 2, sintetizado com numpy (sem samples nem música com direitos).
  hanam : 96 BPM, Lá menor, kick seco e caixa com palmas, baixo sub, pluck pentatónico, chiar de grelha por baixo.
  jasmim: 92 BPM, Fá maior 7.ª, kick suave, shaker, Rhodes em contratempo, ondas ao fundo.
No fim (campo «end») a música abre num acorde longo para o fecho com pachecost.com.
Uso: python3 som-en.py tempos.json saida.wav"""
import json, sys, wave
import numpy as np

SR = 48000
ev = json.load(open(sys.argv[1]))
STYLE, DUR, END = ev["style"], float(ev["dur"]), float(ev["end"])
N = int(SR * DUR)
rng = np.random.default_rng(7)
mus = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(d * SR)) / SR
noise = lambda d: rng.uniform(-1, 1, int(d * SR))
smooth = lambda x, w: np.convolve(x, np.ones(w) / w, mode="same")


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


if STYLE == "hanam":
    BEAT = 60 / 96; BAR = 4 * BEAT
    prog = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]  # Am F C G
    penta = [69, 72, 74, 76, 79, 81]
    nb = int(END / BAR)
    for b in range(nb + 1):
        t0 = b * BAR
        root, ch = prog[b % 4]
        if t0 >= END: break
        full = b >= 1
        for k in range(4):
            tb = t0 + k * BEAT
            if tb >= END: break
            if k in (0, 2) or (full and k == 3 and b % 2): put(tb if k != 3 else tb + BEAT / 2, kick(), .9)
            if full and k in (1, 3): put(tb, snare(), .35); put(tb, clap(), .4)
            for h in (0, .5):
                if tb + h * BEAT < END: put(tb + h * BEAT, hat(), .16 if h else .22)
        put(t0, sub(root - 24, BEAT * 1.5), .45); put(t0 + BEAT * 2.5, sub(root - 24, BEAT * 1.2), .4)
        put(t0, pad(ch, BAR + .3, .3, .5), .1)
        if b >= 2:
            for k in range(8):
                if (b * 8 + k) % 3 != 1:
                    put(t0 + k * BEAT / 2, pluck(penta[(b * 5 + k * 3) % len(penta)]), .13)
    # chiar da grelha (assinatura do Hanam), baixinho por baixo de tudo
    s = noise(END); s = s - smooth(s, 3); crackle = (rng.random(len(s)) > .9993) * rng.uniform(.5, 1, len(s))
    put(0, (s * .05 + smooth(crackle, 6) * 3) * np.minimum(1, tt(END) / 1.5), .5)
    fin = [45, 57, 60, 64, 69]
else:
    BEAT = 60 / 92; BAR = 4 * BEAT
    prog = [(41, [53, 57, 60, 64]), (40, [52, 55, 59, 62]), (38, [50, 53, 57, 60]), (36, [48, 52, 55, 59])]  # Fmaj7 Em7 Dm7 Cmaj7
    nb = int(END / BAR)
    for b in range(nb + 1):
        t0 = b * BAR
        root, ch = prog[b % 4]
        if t0 >= END: break
        for k in range(4):
            tb = t0 + k * BEAT
            if tb >= END: break
            if k in (0, 2): put(tb, kick(10, 50), .6)
            if b >= 1 and k in (1, 3): put(tb, clap(), .2)
            for h in (0, .25, .5, .75):
                if tb + h * BEAT < END: put(tb + h * BEAT, shaker(), .12 if h in (.25, .75) else .07)
            if b >= 1 and tb + BEAT / 2 < END: put(tb + BEAT / 2, epiano(ch, .5), .16)
        put(t0, sub(root - 12, BEAT * 1.8), .35); put(t0 + BEAT * 2.5, sub(root - 5, BEAT * 1.2), .28)
        put(t0, pad([m + 12 for m in ch[1:]], BAR + .4), .06)
    # ondas: ruído grave que respira a cada ~6 s
    x = tt(END); w = smooth(noise(END), 60); w = smooth(w, 30)
    put(0, w * (.5 + .5 * np.sin(2 * np.pi * x / 6.4 - 1.5)) ** 2 * 3.5, .5)
    fin = [41, 53, 57, 60, 64, 67]

put(END - 1.6, riser(1.6), .35)
put(END, impact(), .55)
put(END, pad(fin, DUR - END, .05, 2.4), .3)
put(END, epiano(fin[1:], 2.8), .25)

m = mus * np.minimum(1, tt(DUR) / .03)
m = np.tanh(1.2 * m / (np.max(np.abs(m)) + 1e-9)) * .9
m /= np.max(np.abs(m)); m *= .89
pcm = (m * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("som", STYLE, f"{DUR:.2f}s")
