#!/usr/bin/env python3
"""Som dos reels EN, sintetizado com numpy (sem samples nem música com direitos, por isso serve também para anúncios).
Batida a 100 BPM presa à linha do tempo de reel.html: o gancho entra com tudo; cada «problema» é um compasso tenso
sem bateria, com os efeitos da interface (vibrações, toques, papéis, relógio); cada «solução» são dois compassos com
batida e arpejo, um clique por caixa do esquema, teclas na bolha e um sino quando o resultado aparece.
Uso: python3 som.py tempos.json saida.wav   (tempos.json = window.SFX de reel.html, gravado por render.cjs)"""
import json, sys, wave
import numpy as np

SR, DUR, BAR, BEAT = 48000, 30.0, 2.4, .6
S0, PAIN, OUT = [2.4, 9.6, 16.8], 2.4, 24.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
mus, sfx = np.zeros(N), np.zeros(N)


def put(bus, t0, sig, amp=1.0):
    i0 = int(t0 * SR)
    if i0 >= N:
        return
    sig = sig[:N - i0]
    bus[i0:i0 + len(sig)] += amp * sig


def tt(d):
    return np.arange(int(d * SR)) / SR


def smooth(x, w):  # passa-baixo barato (média móvel)
    return np.convolve(x, np.ones(w) / w, mode='same')


def noise(d):
    return rng.uniform(-1, 1, int(d * SR))


hz = lambda m: 440 * 2 ** ((m - 69) / 12)
# acordes por compasso: Am F C G (raiz MIDI, notas)
CH = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]


# ---------- instrumentos ----------
def kick():
    x = tt(.4); f = 45 + 85 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 7) + .3 * noise(.4) * np.exp(-x * 200)


def clap():
    x = tt(.25); n = noise(.25); n = n - smooth(n, 8)
    env = np.exp(-x * 22) * (1 + .6 * (x < .012) + .4 * ((x > .02) & (x < .03)))
    return n * env


def hat(open_=False):
    d = .18 if open_ else .05; x = tt(d); n = noise(d); n = n - smooth(n, 3)
    return n * np.exp(-x * (18 if open_ else 90))


def bass(m, d):
    x = tt(d); f = hz(m)
    s = sum(np.sin(2 * np.pi * f * k * x) / k for k in (1, 2, 3, 4))
    return np.tanh(1.6 * s) * np.minimum(1, x * 300) * np.exp(-x * 4.5)


def pluck(m, d=.35):
    x = tt(d); f = hz(m)
    return (np.sin(2 * np.pi * f * x) + .4 * np.sin(2 * np.pi * 2 * f * x) + .15 * np.sin(2 * np.pi * 3 * f * x)) * np.exp(-x * 11) * np.minimum(1, x * 500)


def pad(notes, d, att=.4, rel=.6):
    x = tt(d); env = np.minimum(1, x / att) * np.clip((d - x) / rel, 0, 1)
    return env * sum(np.sin(2 * np.pi * hz(m) * x * (1 + .002 * j) + j) for j, m in enumerate(notes)) / len(notes)


def drone(m, d):
    x = tt(d); f = hz(m)
    s = np.sin(2 * np.pi * f * x) + .5 * np.sin(2 * np.pi * f * 1.5 * x + 1) + .25 * np.sin(2 * np.pi * f * 2.01 * x)
    return s * np.minimum(1, x / .15) * np.clip((d - x) / .3, 0, 1) * (1 + .25 * np.sin(2 * np.pi * 5 * x))


# ---------- efeitos ----------
def ping(f1, f2, decay=9.0, d=.5):
    x = tt(d)
    return (np.sin(2 * np.pi * f1 * x) + .55 * np.sin(2 * np.pi * f2 * x)) * np.exp(-decay * x) * np.minimum(1, x * 400)


def buzz(d=.32):
    x = tt(d); s = np.sin(2 * np.pi * 170 * x)
    return np.sign(s) * np.abs(s) ** .35 * ((x % .16) < .11) * .55


def tick():
    x = tt(.1)
    return np.sin(2 * np.pi * 1250 * x) * np.exp(-60 * x) + noise(.1) * np.exp(-300 * x) * .4


def key():
    x = tt(.03)
    return noise(.03) * np.exp(-500 * x) * .8 + np.sin(2 * np.pi * 2400 * x) * np.exp(-200 * x) * .2


def whoosh(d=.6):
    x = tt(d); env = np.sin(np.pi * x / d) ** 2
    n = noise(d); lo, hi = smooth(n, 40), smooth(n, 6)
    mix = np.clip(x / d, 0, 1)
    return (lo * (1 - mix) + hi * mix) * env * 3


def rustle(d=.25):
    x = tt(d); n = noise(d); n = n - smooth(n, 4)
    return n * np.exp(-x * 14) * (rng.uniform(.3, 1, len(n)) > .55)


def impact():
    x = tt(1.2)
    return np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-x * 12)) / SR) * np.exp(-x * 3.5) + smooth(noise(1.2), 3) * np.exp(-x * 6) * .5


# ---------- arranjo ----------
tempos = json.load(open(sys.argv[1]))
ESTILO = sys.argv[3] if len(sys.argv) > 3 else '1'
nbars = int(DUR / BAR)
pain_bars = {int(round(s / BAR)) for s in S0}


def musica1():  # reel 1: Am F C G, bombo a cada tempo, palmas, arpejo em semicolcheias
    for b in range(nbars):
        t0 = b * BAR
        root, notes = CH[b % 4]
        if b in pain_bars:  # problema: sem bateria, drone grave e tensão
            put(mus, t0, drone(root - 12, BAR), .16)
            put(mus, t0, pad([n - 12 for n in notes], BAR, .3, .3), .07)
            put(mus, t0, kick(), .55)  # um só bombo no 1, para marcar a entrada
            continue
        last = b == nbars - 1
        for q in range(4):
            tq = t0 + q * BEAT
            if not (last and q > 1):
                put(mus, tq, kick(), .8)
            if q in (1, 3) and not (last and q == 3):
                put(mus, tq, clap(), .32)
            for e in (0, .3):
                put(mus, tq + e, hat(open_=(e == .3 and q == 3)), .09 if e else .06)
            for e in (0, .3):  # baixo em colcheias, com «pump» do bombo
                put(mus, tq + e, bass(root - 12 if e == 0 else root, .28), .2 if e else .26)
        if not last:
            arp = notes + [notes[1] + 12, notes[2] + 12, notes[1] + 12]
            for s in range(16):  # arpejo em semicolcheias
                put(mus, t0 + s * BEAT / 4, pluck(arp[s % len(arp)] + 12), .045 if s % 4 else .06)
        put(mus, t0, pad(notes, BAR + .3), .07)
    # final: acorde aberto que soa até ao fim (o reel volta ao início em loop)
    put(mus, DUR - 1.2, pad([57, 64, 69, 72, 76], 1.2, .05, .9), .14)


# reel 2: «noite → manhã», mais quente e mais lenta no sentir: Dmaj7 Bm7 Gmaj7 A6, meio-tempo, estalos de dedos,
# shaker, acordes de piano elétrico em contratempo e baixo redondo; os problemas têm o tique-taque do relógio
CH2 = [(38, [57, 61, 64, 66]), (35, [54, 57, 61, 62]), (43, [54, 57, 59, 62]), (45, [54, 57, 61, 64])]


def epiano(notes, d=.5):
    x = tt(d)
    s = sum(np.sin(2 * np.pi * hz(m) * x + 1.2 * np.sin(2 * np.pi * hz(m) * x) * np.exp(-x * 6)) for m in notes) / len(notes)
    return s * np.exp(-x * 3.2) * np.minimum(1, x * 200) * (1 + .2 * np.sin(2 * np.pi * 4.5 * x))


def snap():
    x = tt(.12); n = noise(.12); n = n - smooth(n, 2)
    return n * np.exp(-x * 45) + np.sin(2 * np.pi * 1800 * x) * np.exp(-x * 80) * .3


def sub(m, d):
    x = tt(d)
    return np.sin(2 * np.pi * hz(m) * x) * np.minimum(1, x * 80) * np.clip((d - x) / .08, 0, 1)


def musica2():
    for b in range(nbars):
        t0 = b * BAR
        root, notes = CH2[b % 4]
        if b in pain_bars:
            put(mus, t0, drone(root - 12, BAR), .12)
            for q in range(4):
                put(mus, t0 + q * BEAT, tick(), .14)  # relógio
                put(mus, t0 + q * BEAT + .3, tick()[::2], .07)
            continue
        last = b == nbars - 1
        put(mus, t0, kick(), .75)
        if not last:
            put(mus, t0 + 1.5 * BEAT, kick(), .55)
        for q in (1, 3):
            if not (last and q == 3):
                put(mus, t0 + q * BEAT, snap(), .4)
        for s16 in range(16):
            put(mus, t0 + s16 * BEAT / 4, hat() * (1 if s16 % 2 else .5), .05)
        for q in range(4):
            if not (last and q > 1):
                put(mus, t0 + q * BEAT + .3, epiano(notes, .45), .11)
        put(mus, t0, sub(root, BEAT * 1.5), .3)
        put(mus, t0 + BEAT * 2, sub(root + (7 if b % 2 else 12), BEAT * 1.9), .24)
        put(mus, t0, pad([n + 12 for n in notes], BAR + .3, .8, .8), .035)
    put(mus, DUR - 1.2, epiano([62, 66, 69, 73, 76], 1.2), .2)


musica1() if ESTILO == "1" else musica2()

if ESTILO == '1':
    put(sfx, 0, impact(), .55)                 # gancho: entra com tudo
else:                                          # gancho do reel 2: o relógio rola das 00:30 para as 07:00 com um despertador suave
    put(sfx, 0, kick(), .5)
    for j, f in enumerate((1318.5, 1760, 2217.5, 2637)):
        put(sfx, .9 + j * .09, ping(f, f * 1.5, 5, .9), .08)
for t in [S0[0], S0[1], S0[2], OUT, 27.0]:
    put(sfx, t - .35, whoosh(.55), .1)
for i, s in enumerate(S0):
    put(sfx, s + PAIN - .3, whoosh(.5), .09)    # problema → solução
    ui = tempos[i]['pain']
    if ui == 'ring':  # chamada a tocar (dois tons) que fica perdida; o contador sobe até 12
        for j in range(2):
            x = tt(.4); put(sfx, s + .1 + j * .45, (np.sin(2 * np.pi * 440 * x) + np.sin(2 * np.pi * 480 * x)) * .5 * np.minimum(1, x * 80) * np.clip((.4 - x) / .05, 0, 1), .14)
        put(sfx, s + .95, ping(330, 311, 5, .7), .15)
        for j in range(11):
            put(sfx, s + 1.0 + j * .073, tick(), .07)
    elif ui == 'calls':
        for j, tp in enumerate(['ch', 'wa', 'ch', 'ch', 'wa']):
            put(sfx, s + .1 + j * .16, buzz(.2) if tp == 'ch' else ping(1568, 2349, d=.4), .2 if tp == 'ch' else .14)
    elif ui == 'lapsed':  # clientes que se afastam: toques a descer de tom
        for j, f in enumerate((660, 523, 392)):
            put(sfx, s + .1 + j * .18, ping(f, f * 1.5, 7, .5), .11)
    elif ui == 'diary':
        for j in range(4):
            put(sfx, s + .1 + j * .18, tick(), .12)
        put(sfx, s + .5, ping(330, 311, 5, .7), .16)  # nota «errada» no no-show
    elif ui == 'reviews':
        put(sfx, s + .15, ping(1047, 1568, d=.5), .12); put(sfx, s + .5, ping(523, 494, 6, .6), .13)
    elif ui == 'receipts':
        for j in range(5):
            put(sfx, s + .08 + j * .12, rustle(), .35)
    elif ui == 'night':
        for j in range(5):
            put(sfx, s + .1 + j * .45, tick(), .1)
    elif ui == 'insta':
        put(sfx, s + .1, ping(880, 1320, d=.4), .1)
    for ts in tempos[i]['steps']:
        put(sfx, ts, tick(), .13)
    for tb in tempos[i]['bolhas']:
        t = tb
        while t < tb + .75:
            put(sfx, t, key(), .06); t += .05 + rng.random() * .035
    r = s + PAIN + 3.6                          # o resultado troca o título
    for f, d in ((784, 0), (1175, .08), (1568, .16)):
        put(sfx, r + d, ping(f, f * 2, 3, 1.4), .09)
# fecho: «Comment 1, 2 or 3» e o botão do site
for j in range(3):
    put(sfx, OUT + .75 + j * .25, tick(), .12)
put(sfx, OUT + 1.6, ping(1047, 1568, 4, .8), .12)
put(sfx, 27.0 + .8, ping(1318.5, 1975.5, 3, 1.2), .1)

mix = np.tanh(1.1 * (mus + sfx))
mix *= .89 / (np.abs(mix).max() or 1)
fade = np.ones(N); fade[-int(.25 * SR):] = np.linspace(1, 0, int(.25 * SR))
pcm = (mix * fade * 32767).astype('<i2')
with wave.open(sys.argv[2] if len(sys.argv) > 2 else 'som.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(np.repeat(pcm, 2).tobytes())
