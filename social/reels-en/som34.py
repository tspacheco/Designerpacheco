#!/usr/bin/env python3
"""Som dos reels EN 3 e 4, sintetizado com numpy (sem samples nem música com direitos, por isso também servem como anúncios).
Lê os eventos de window.SFX (gravados por render34.cjs) e escolhe o estilo pelo campo «style»:
  xray  (reel 3): 100 BPM, Mi menor, pulso grave de sonar, hats em clique, arpejo pentatónico, pads; efeitos de conversa
                  (enviado, visto, recebido lento/rápido, cronómetro), ping de sonar no raio-X, carimbos nos nós da planta.
  cafe  (reel 4): 100 BPM com swing, Dó maior 7.ª, contrabaixo, vassouras, Rhodes em contratempo, shaker; a metade «sem»
                  tem riscos de lápis e baques surdos, a metade «com» tem sinos suaves; o relógio vira com um estalo mecânico.
Uso: python3 som34.py tempos.json saida.wav"""
import json, sys, wave
import numpy as np

SR = 48000
ev = json.load(open(sys.argv[1]))
STYLE = ev.get('style', 'xray')
DUR = float(ev.get('dur', 30.0))
BAR, BEAT = 2.4, .6
N = int(SR * DUR)
rng = np.random.default_rng(11)
mus, sfx = np.zeros(N), np.zeros(N)


def put(bus, t0, sig, amp=1.0):
    i0 = int(t0 * SR)
    if i0 >= N or i0 < 0:
        return
    sig = sig[:N - i0]
    bus[i0:i0 + len(sig)] += amp * sig


def tt(d):
    return np.arange(int(d * SR)) / SR


def smooth(x, w):
    return np.convolve(x, np.ones(w) / w, mode='same')


def noise(d):
    return rng.uniform(-1, 1, int(d * SR))


hz = lambda m: 440 * 2 ** ((m - 69) / 12)


# ---------- instrumentos ----------
def kick(dec=7, lo=45):
    x = tt(.4); f = lo + 85 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * dec) + .25 * noise(.4) * np.exp(-x * 220)


def sub(m, d):
    x = tt(d)
    return np.sin(2 * np.pi * hz(m) * x) * np.minimum(1, x * 80) * np.clip((d - x) / .1, 0, 1)


def click():
    x = tt(.03); n = noise(.03); n = n - smooth(n, 2)
    return n * np.exp(-x * 400)


def hat(open_=False):
    d = .18 if open_ else .05; x = tt(d); n = noise(d); n = n - smooth(n, 3)
    return n * np.exp(-x * (18 if open_ else 90))


def pluck(m, d=.5, bright=.4):
    x = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(2 * np.pi * 2 * f * x) + .12 * np.sin(2 * np.pi * 3 * f * x)) * np.exp(-x * 7) * np.minimum(1, x * 500)


def pad(notes, d, att=.5, rel=.6):
    x = tt(d); env = np.minimum(1, x / att) * np.clip((d - x) / rel, 0, 1)
    return env * sum(np.sin(2 * np.pi * hz(m) * x * (1 + .0015 * j) + j) for j, m in enumerate(notes)) / len(notes)


def epiano(notes, d=.5):
    x = tt(d)
    s = sum(np.sin(2 * np.pi * hz(m) * x + 1.1 * np.sin(2 * np.pi * hz(m) * x) * np.exp(-x * 6)) for m in notes) / len(notes)
    return s * np.exp(-x * 3.0) * np.minimum(1, x * 200) * (1 + .15 * np.sin(2 * np.pi * 4.5 * x))


def upright(m, d=.55):
    x = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * x) + .5 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 9) + .2 * np.sin(2 * np.pi * 3 * f * x) * np.exp(-x * 14)
    return np.tanh(1.3 * s) * np.exp(-x * 3.2) * np.minimum(1, x * 300)


def brush():
    x = tt(.22); n = noise(.22); n = smooth(n, 4)
    return n * np.exp(-x * 16) * (1 + .5 * (x < .02))


def shaker():
    x = tt(.08); n = noise(.08); n = n - smooth(n, 2)
    return n * np.exp(-x * 60) * .6


# ---------- efeitos ----------
def ping(f1, f2, decay=9.0, d=.5):
    x = tt(d)
    return (np.sin(2 * np.pi * f1 * x) + .55 * np.sin(2 * np.pi * f2 * x)) * np.exp(-decay * x) * np.minimum(1, x * 400)


def tick(f=1250):
    x = tt(.1)
    return np.sin(2 * np.pi * f * x) * np.exp(-60 * x) + noise(.1) * np.exp(-300 * x) * .4


def whoosh(d=.5, up=True):
    x = tt(d); env = np.sin(np.pi * x / d) ** 2
    n = noise(d); lo, hi = smooth(n, 40), smooth(n, 6)
    mix = np.clip(x / d, 0, 1)
    mix = mix if up else 1 - mix
    return (lo * (1 - mix) + hi * mix) * env * 3


def sweep(d=.45):  # linha de varrimento: ruído filtrado a descer
    x = tt(d); n = noise(d); env = np.sin(np.pi * x / d) ** 1.5
    f = 2600 * np.exp(-x * 5) + 200
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * .4 + smooth(n, 5) * .8) * env


def sonar(d=2.2):
    x = tt(d)
    return (np.sin(2 * np.pi * 740 * x) + .4 * np.sin(2 * np.pi * 1480 * x)) * np.exp(-x * 2.2) * np.minimum(1, x * 300)


def stamp():  # carimbo: baque grave + clique
    x = tt(.25); c = click()
    return np.sin(2 * np.pi * np.cumsum(90 + 120 * np.exp(-x * 40)) / SR) * np.exp(-x * 18) + np.concatenate([c, np.zeros(len(x) - len(c))]) * .8


def pencil(d=.3):
    x = tt(d); n = noise(d); n = n - smooth(n, 6)
    return n * np.exp(-x * 9) * (1 + .6 * np.sin(2 * np.pi * 23 * x))


def thud():
    x = tt(.3)
    return np.sin(2 * np.pi * np.cumsum(70 + 40 * np.exp(-x * 30)) / SR) * np.exp(-x * 14)


def flip():  # relógio de palhetas: dois estalos
    c = click(); z = np.zeros(int(.07 * SR))
    return np.concatenate([c, z, c * .7]) * 1.4


def bell(f):
    x = tt(1.1)
    return (np.sin(2 * np.pi * f * x) + .3 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 6)) * np.exp(-x * 3.5) * np.minimum(1, x * 400)


def keys(t0, d=.7):
    t = t0
    while t < t0 + d:
        x = tt(.03); put(sfx, t, noise(.03) * np.exp(-500 * x) * .8, .05); t += .05 + rng.random() * .035


# ---------- música ----------
nbars = int(np.ceil(DUR / BAR))


def musica_xray():
    # Mi menor: Em  Cmaj7  G  D/F#   (raiz MIDI, notas)
    CH = [(40, [52, 55, 59]), (36, [52, 55, 59, 60]), (43, [50, 55, 59]), (42, [50, 54, 57])]
    PENTA = [64, 67, 69, 71, 74, 76, 79]
    quiet = {1, 2, 3}  # as conversas: só pulso e pad, para se ouvirem os toques
    for b in range(nbars):
        t0 = b * BAR; root, notes = CH[b % 4]
        last = t0 + BAR >= DUR
        put(mus, t0, sub(root - 12, BEAT * 1.2), .42)          # pulso de sonar no 1
        put(mus, t0 + 2 * BEAT, sub(root - 12, BEAT * 1.2), .3)
        put(mus, t0, kick(9, 40), .5)
        if b not in quiet and not last:
            put(mus, t0 + 2 * BEAT, kick(9, 40), .35)
            for s16 in range(16):
                if s16 % 2 == 0 or rng.random() < .35:
                    put(mus, t0 + s16 * BEAT / 4, click(), .12 if s16 % 4 == 0 else .06)
            for s in range(8):  # arpejo pentatónico em colcheias
                if rng.random() < .75:
                    put(mus, t0 + s * BEAT / 2, pluck(PENTA[(b * 3 + s * 2) % len(PENTA)] + (12 if s % 3 == 0 else 0), .5, .25), .05)
        put(mus, t0, pad(notes, BAR + .4, .6, .5), .05 if b in quiet else .07)
    put(mus, DUR - 1.4, pad([52, 59, 64, 67, 71], 1.4, .05, 1.0), .14)


def musica_cafe():
    # Dó maior: Cmaj7  Am7  Dm7  G13 ; swing nas colcheias (a 2.ª colcheia atrasa 1/3 de tempo)
    CH = [(36, [60, 64, 67, 71]), (33, [60, 64, 67, 69]), (38, [60, 62, 65, 69]), (31, [59, 62, 65, 69])]
    sw = BEAT * .33
    for b in range(nbars):
        t0 = b * BAR; root, notes = CH[b % 4]
        last = t0 + BAR >= DUR
        for q in range(4):  # contrabaixo a andar
            m = [root, root + 7, root + 4, root + 9][q] if q != 3 or b % 2 else root + 5
            put(mus, t0 + q * BEAT, upright(m + 12, .6), .32 if q % 2 == 0 else .25)
            put(mus, t0 + q * BEAT, hat(), .035)
            put(mus, t0 + q * BEAT + sw, hat(), .05)
            if q in (1, 3):
                put(mus, t0 + q * BEAT, brush(), .22)
            put(mus, t0 + q * BEAT + BEAT / 2, shaker(), .12)
        if not last:
            put(mus, t0 + BEAT + sw, epiano(notes, .5), .11)
            put(mus, t0 + 3 * BEAT + sw, epiano([n + (0 if b % 2 else 12) for n in notes], .5), .09)
        else:
            put(mus, t0, epiano(notes, 1.5), .14)
        put(mus, t0, kick(10, 50), .3)
        put(mus, t0 + 2 * BEAT + sw, kick(10, 50), .22)
    put(mus, DUR - 1.4, epiano([60, 64, 67, 71, 74], 1.4), .22)


# ---------- eventos ----------
def each(name):
    return ev.get(name, []) or []


if STYLE == 'xray':
    musica_xray()
    for t in each('scan'):
        put(sfx, t - .05, sweep(.5), .16)
    for t in each('send'):
        put(sfx, t, whoosh(.3, True), .1); put(sfx, t + .05, ping(1760, 2637, 12, .25), .05)
    for t in each('seen'):
        put(sfx, t, tick(1800), .07)
    for t in each('noreply'):
        put(sfx, t, thud(), .35); put(sfx, t, pad([40, 47], 1.2, .05, .8), .12)
    for t in each('recv_slow'):
        put(sfx, t, ping(523, 494, 5, .9), .16)  # toque baço, meio desafinado
    for t in each('recv_fast'):
        put(sfx, t, ping(1319, 1760, 6, .6), .14); put(sfx, t + .12, ping(1760, 2637, 7, .5), .1)
    for t in each('tick'):
        put(sfx, t, tick(1500), .08)
    for t in each('booked'):
        for f, d in ((784, 0), (1175, .08), (1568, .16)):
            put(sfx, t + d, ping(f, f * 2, 3, 1.2), .08)
    for t in each('xray'):
        put(sfx, t, sonar(), .22); put(sfx, t + .9, sonar(1.6), .12)
    for t in each('node'):
        put(sfx, t, stamp(), .5); put(sfx, t + .02, sweep(.25), .05)
    for t in each('result'):
        put(sfx, t, pad([52, 59, 64, 71], 1.6, .1, 1.0), .16)
        for f, d in ((659, 0), (988, .1), (1319, .2)):
            put(sfx, t + d, ping(f, f * 2, 3, 1.3), .07)
    for t in each('rule'):
        put(sfx, t, kick(5, 38), .7)
    for t in each('abc'):
        put(sfx, t, tick(), .12)
    for t in each('btn'):
        put(sfx, t, ping(1047, 1568, 4, .8), .12)
else:
    musica_cafe()
    for t in each('flip'):
        put(sfx, t, flip(), .5)
    for t in each('top_in'):
        put(sfx, t, whoosh(.3, False), .08)
    for t in each('top_bad'):
        put(sfx, t, pencil(.35), .3); put(sfx, t + .05, thud(), .3)
    for t in each('node'):
        put(sfx, t, bell(1319 if int(t * 10) % 2 else 1568), .06); put(sfx, t, tick(1100), .06)
    for t in each('ok'):
        for f, d in ((1047, 0), (1319, .09), (1568, .18)):
            put(sfx, t + d, bell(f), .07)
    for t in each('typing'):
        keys(t, .7)
    for t in each('morning'):
        put(sfx, t, ping(1760, 2217, 6, .5), .1); put(sfx, t + .1, ping(2217, 2637, 7, .4), .08)
    for t in each('zzz'):
        put(sfx, t, pad([48, 55], 1.0, .2, .6), .05)
    for t in each('result'):
        put(sfx, t, epiano([60, 64, 67, 71, 76], 1.6), .25)
    for t in each('abc'):
        put(sfx, t, tick(), .12)
    for t in each('btn'):
        put(sfx, t, ping(1047, 1568, 4, .8), .12)

mix = np.tanh(1.1 * (mus + sfx))
mix *= .89 / (np.abs(mix).max() or 1)
fade = np.ones(N); fade[-int(.25 * SR):] = np.linspace(1, 0, int(.25 * SR))
pcm = (mix * fade * 32767).astype('<i2')
with wave.open(sys.argv[2] if len(sys.argv) > 2 else 'som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(np.repeat(pcm, 2).tobytes())
