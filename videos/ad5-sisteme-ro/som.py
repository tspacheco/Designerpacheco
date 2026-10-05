#!/usr/bin/env python3
"""Som do reel «5 sisteme» RO, sintetizado (sem samples nem música com direitos).
Intro: o telefone toca e é cortado quando as cartas caem, sinal de ocupado em «Se pierd pe drum», relógio em tensão,
néon a acender e subida até ao drop. Depois uma batida a 100 BPM: cada sistema dura 2 compassos (4,8 s) e entra no
tempo forte com um corte; pausa sem bombo em «Un singur sistem», a batida volta no fecho e o CTA leva um toque de mensagem.
Os tempos batem com reel.html. Escreve dois ficheiros já normalizados (ffmpeg loudnorm):
  <pasta>/som-mix.wav      música + efeitos (-14 LUFS)
  <pasta>/som-efeitos.wav  só os efeitos, para pôr outra música por baixo (-16 LUFS)
Uso: python3 som.py <pasta>"""
import json, math, os, random, re, subprocess, sys, wave
from array import array

SR, DUR = 48000, 40.0
N = int(SR * DUR)
TAU = 2 * math.pi
BEAT = .6                      # 100 BPM
STEP, BAR = BEAT / 4, BEAT * 4
D = 5.2                        # drop: entra o sistema 01
CENAS = [5.2, 10.0, 14.8, 19.6, 24.4]
PAUSA, FECHO, FIM = 29.2, 34.0, 38.8
random.seed(11)


def buf():
    return array('d', bytes(8 * N))


mus, sfx, eco = [buf(), buf()], [buf(), buf()], buf()


def add(dst, t0, dur, fn, amp, pan=0.0, send=0.0):
    gl = amp * math.cos((pan + 1) * math.pi / 4) * math.sqrt(2)
    gr = amp * math.sin((pan + 1) * math.pi / 4) * math.sqrt(2)
    L, R = dst
    i0 = int(round(t0 * SR))
    for k in range(int(dur * SR)):
        i = i0 + k
        if i >= N:
            break
        if i < 0:
            continue
        v = fn(k / SR)
        L[i] += gl * v
        R[i] += gr * v
        if send:
            eco[i] += send * amp * v


def noise():
    return random.random() * 2 - 1


def agudo():  # ruído com os graves tirados (segunda diferença)
    st = [0.0, 0.0]

    def f():
        n = noise()
        v = n - 2 * st[0] + st[1]
        st[1], st[0] = st[0], n
        return v * .25
    return f


# ── instrumentos ──────────────────────────────────────────────────────────────
def kick(x):  # 160 → 48 Hz com clique; a saturação dá harmónicos que se ouvem no telemóvel
    ph = 48 * x + 112 * (1 - math.exp(-30 * x)) / 30
    knock = math.sin(TAU * 1.9 * ph) * math.exp(-28 * x) * .45 + math.sin(TAU * 3100 * x) * math.exp(-160 * x) * .25
    return math.tanh(1.8 * (math.sin(TAU * ph) * math.exp(-7 * x) + knock + noise() * math.exp(-500 * x) * .3))


def clap():
    hp = agudo()

    def f(x):
        env = sum(math.exp(-180 * (x - o)) for o in (0, .011, .023) if x >= o) * .5 + math.exp(-22 * x) * .6
        return hp() * env * 1.4 + math.sin(TAU * 190 * x) * math.exp(-35 * x) * .3
    return f


def hat(decay):
    hp = agudo()
    return lambda x: hp() * math.exp(-decay * x) * 1.6


def bass(f0, d):
    def f(x):
        env = min(1, x / .005) * math.exp(-2.2 * x) * min(1, max(0, (d - x) / .03))
        mid = sum(math.sin(TAU * f0 * n * x) / n for n in (4, 5, 6, 8)) * math.exp(-5 * x)
        return (math.tanh(3.0 * math.sin(TAU * f0 * x)) * .55 + .25 * math.sin(TAU * 2 * f0 * x) + .6 * mid) * env
    return f


def pluck(f0, dec=5.0):
    return lambda x: min(1, x / .004) * sum(math.sin(TAU * f0 * n * x) / n * math.exp(-dec * (.4 + .6 * n) * x) for n in range(1, 6)) * .7


def pad(freqs, d, att=.8, rel=1.0):
    def f(x):
        env = min(1, x / att) * min(1, max(0, (d - x) / rel))
        return env * sum(math.sin(TAU * fr * x) + math.sin(TAU * fr * 1.004 * x + 1) for fr in freqs) / (2 * len(freqs))
    return f


def ping(f1, f2, decay=9.0):  # toque de mensagem
    return lambda x: (math.sin(TAU * f1 * x) + .55 * math.sin(TAU * f2 * x)) * math.exp(-decay * x) * min(1, x * 400)


def subida(d, top=.55):  # ruído que abre e cresce até ao fim
    st = [0.0]

    def f(x):
        p = min(1, x / d)
        st[0] += (.015 + top * p * p) * (noise() - st[0])
        return st[0] * p ** 1.5 * 2
    return f


def crash():
    hp = agudo()
    return lambda x: hp() * math.exp(-2.8 * x) * 1.2 + noise() * math.exp(-9 * x) * .2


def sub_queda(x):  # pancada grave 60 → 38 Hz
    ph = 38 * x + 22 * (1 - math.exp(-4 * x)) / 4
    return math.tanh(1.5 * math.sin(TAU * ph)) * math.exp(-2.5 * x)


def toque(d):  # campainha de telefone: duas campainhas batidas à vez, 25 vezes por segundo
    def f(x):
        ph = x * 25
        s = int(ph)
        fr = ph - s
        b1 = math.sin(TAU * 1180 * x) + .5 * math.sin(TAU * 2950 * x)
        b2 = math.sin(TAU * 1330 * x) + .5 * math.sin(TAU * 3320 * x)
        a, b = (b1, b2) if s % 2 == 0 else (b2, b1)
        env = min(1, x / .01) * min(1, max(0, (d - x) / .006))
        return env * (math.exp(-fr * 3) * a + math.exp(-(fr + 1) * 3) * b) / 1.6
    return f


def carta(x):  # carta de vidro a cair na mesa
    return (math.sin(TAU * 2650 * x) * math.exp(-45 * x) + .6 * math.sin(TAU * 4180 * x) * math.exp(-70 * x)
            + noise() * math.exp(-400 * x) * .5 + math.sin(TAU * 140 * x) * math.exp(-40 * x) * .5)


def ocupado(d):  # sinal de ocupado (425 Hz)
    def f(x):
        env = min(1, x / .006) * min(1, max(0, (d - x) / .01))
        return env * (math.sin(TAU * 425 * x) + .3 * math.sin(TAU * 850 * x) + .15 * math.sin(TAU * 1275 * x))
    return f


def relogio(f0):
    return lambda x: math.sin(TAU * f0 * x) * math.exp(-60 * x) + noise() * math.exp(-300 * x) * .4


def neon(x):  # zumbido curto de um tubo a acender
    s = math.sin(TAU * 100 * x)
    return (math.copysign(abs(s) ** .3, s) * .6 + noise() * .3) * math.exp(-18 * x) * (1 if (x * 50) % 1 < .7 else .3)


def glide(f0, f1, d):  # tom que sobe
    def f(x):
        p = min(1, x / d)
        ph = f0 * d * ((f1 / f0) ** p - 1) / math.log(f1 / f0)
        return math.sin(TAU * ph) * p * p
    return f


def pop(f0):  # bolha das pílulas
    return lambda x: math.sin(TAU * (f0 * x + f0 * .5 * x * x / .06 if x < .06 else f0 * .09 + 2 * f0 * (x - .06))) * math.exp(-30 * x)


# ── intro 0–5,2 (cartas a cair ~1,2 s · mão na cara ~2,5 s · néon ~3 s · laço à volta das cartas ~3,8 s) ──
add(sfx, .05, .80, toque(.80), .28)
add(sfx, 1.02, .20, toque(.20), .28)                     # segundo toque cortado quando as cartas caem
for t, p in ((1.25, -.3), (1.33, .3), (1.40, 0)):
    add(sfx, t, .25, carta, .14, p)
add(sfx, 1.58, 1.2, sub_queda, .30)                      # «Se pierd pe drum»
for t in (1.58, 1.93, 2.28):
    add(sfx, t, .17, ocupado(.17), .16)
for i, t in enumerate((2.2, 2.8, 3.4, 4.0, 4.6)):         # relógio já no tempo da batida
    add(sfx, t, .12, relogio(1700 if i % 2 == 0 else 1300), .09 + .015 * i)
add(mus, 2.0, 3.0, pad([55, 82.4, 110, 164.8], 3.0, att=1.2, rel=.4), .14)
for t, p in ((3.0, -.5), (3.14, .5), (3.27, 0)):
    add(sfx, t, .2, neon, .08, p)
add(sfx, 3.2, 1.8, subida(1.8), .16)
add(sfx, 3.4, 1.6, glide(110, 880, 1.6), .035)
for _ in range(12):
    add(sfx, 3.7 + random.random() * .4, .2, ping(2500 + random.random() * 2500, 6000, 25), .025, random.random() * 1.6 - .8, .3)
for f, t in ((659.3, 4.05), (880.0, 4.10), (987.8, 4.15)):
    add(sfx, t, 1.0, ping(f, f * 2, 3.5), .06, 0, .4)


# ── batida ────────────────────────────────────────────────────────────────────
ACORDES = {'Am': ([220, 261.63, 329.63], 55.0), 'F': ([220, 261.63, 349.23], 43.65),
           'C': ([196, 261.63, 329.63], 65.41), 'G': ([196, 246.94, 293.66], 49.0)}
PROG = ['Am', 'F', 'C', 'G']


def impacto(t, forte=1.0):
    add(sfx, t, 1.6, crash(), .14 * forte)
    add(sfx, t, 1.2, sub_queda, .22 * forte)


def transicao(t):
    add(sfx, t - .6, .6, subida(.6, .7), .13)
    impacto(t, .8)


for b in range(14):
    t0 = D + b * BAR
    sec = b // 2                       # 0–4 sistemas · 5 pausa · 6 fecho
    nome = PROG[b % 4]
    notas, raiz = ACORDES[nome]
    if sec == 5:                       # «Un singur sistem»: sem bombo, só acorde e toques suaves
        add(mus, t0, BAR + .3, pad([raiz * 2] + notas, BAR + .3, att=.3, rel=.4), .22)
        for q in range(4):
            for j, f in enumerate(notas):
                add(mus, t0 + q * BEAT + j * .012, .7, pluck(f * 2, 7), .07, (-.3, 0, .3)[j], .5)
        continue
    for s in (0, 7, 10):
        add(mus, t0 + s * STEP, .45, kick, .24)
    for s, d in ((0, .9), (7, .45), (10, .75)):
        add(mus, t0 + s * STEP, d, bass(raiz, d), .13)
    for s in (4, 12):
        add(mus, t0 + s * STEP, .3, clap(), .34)
    for s in range(16):
        if s % 2 == 0:
            add(mus, t0 + s * STEP, .08, hat(80), .09 if s % 4 else .065, .25)
        elif sec >= 2:
            add(mus, t0 + s * STEP, .06, hat(110), .045, -.25)
    if sec >= 1 and b % 2 == 1:
        add(mus, t0 + 14 * STEP, .3, hat(12), .07, .3)
    for s, v in ((0, 1), (3, .6), (6, .8), (10, .65)):
        for j, f in enumerate(notas):
            add(mus, t0 + s * STEP + j * .008, .8, pluck(f, 3.5), .24 * v, (-.35, 0, .35)[j], .25)
    if sec in (3, 4, 6):               # arpejo agudo a partir do sistema 04
        for s in range(16):
            f = notas[s % 3] * 2
            add(mus, t0 + s * STEP, .25, pluck(f, 9), .06, .4 if s % 2 else -.4, .4)
    if b == 9:                         # rufo antes da pausa
        for k, s in enumerate((12, 13, 14, 15)):
            add(mus, t0 + s * STEP, .2, clap(), .08 + .03 * k)

impacto(D, 1.2)
for t in CENAS[1:]:
    transicao(t)

# pausa: pílulas e texto a entrar no tempo
for t, f in ((30.4, 600), (31.0, 680), (31.6, 760)):
    add(sfx, t, .25, pop(f), .18)
add(sfx, 32.2, .12, relogio(1500), .07)
add(sfx, 32.8, 1.2, subida(1.2, .7), .18)
for k in range(6):
    add(mus, 33.1 + k * STEP, .2, clap(), .05 + .03 * k)
impacto(FECHO, 1.1)

# fecho: toque de mensagem no CTA e acorde final
add(sfx, 35.2, .6, ping(1568, 2349), .15, 0, .3)
add(sfx, 35.34, .6, ping(1976, 2960), .11, 0, .3)
impacto(FIM, .7)
add(mus, FIM, DUR - FIM, pad([65.41, 130.81, 196, 329.63, 493.88, 587.33], DUR - FIM, att=.05, rel=1.0), .10)
for j, f in enumerate((261.63, 329.63, 392.0, 587.33)):
    add(mus, FIM + j * .03, DUR - FIM, pluck(f, 1.6), .05, (-.4, -.15, .15, .4)[j], .4)


# ── eco em pingue-pongue (0,45 s à esquerda, 0,30 s à direita) ───────────────
dl, dr = int(.45 * SR), int(.30 * SR)
yl, yr = buf(), buf()
lpl = lpr = 0.0
for i in range(N):
    lpl += .35 * ((yl[i - dl] if i >= dl else 0.0) - lpl)
    lpr += .35 * ((yr[i - dr] if i >= dr else 0.0) - lpr)
    yl[i] = eco[i] + .34 * lpl
    yr[i] = eco[i] + .34 * lpr
    mus[0][i] += .35 * lpl
    mus[1][i] += .35 * lpr


# ── saída ─────────────────────────────────────────────────────────────────────
def escreve(path, L, R):
    peak = max(max(abs(v) for v in L), max(abs(v) for v in R)) or 1
    k = math.tanh(1.3)
    out = array('h', bytes(4 * N))
    for i in range(N):
        out[2 * i] = int(math.tanh(1.3 * L[i] / peak) / k * 32000)
        out[2 * i + 1] = int(math.tanh(1.3 * R[i] / peak) / k * 32000)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(out.tobytes())


def normaliza(src, dst, lufs):  # graves um pouco abaixo: a maioria ouve na coluna do telemóvel
    f = f'highpass=f=30,lowshelf=f=110:g=-4,loudnorm=I={lufs}:TP=-1.5:LRA=11'
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', f + ':print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = json.loads(re.findall(r'\{[^{}]*\}', r.stderr)[-1])
    f += (f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-af', f, '-ar', str(SR), dst], check=True)


pasta = sys.argv[1] if len(sys.argv) > 1 else '.'
os.makedirs(pasta, exist_ok=True)
mix = [array('d', (a + b for a, b in zip(mus[c], sfx[c]))) for c in (0, 1)]
escreve(os.path.join(pasta, 'mix-bruto.wav'), *mix)
escreve(os.path.join(pasta, 'efeitos-bruto.wav'), *sfx)
normaliza(os.path.join(pasta, 'mix-bruto.wav'), os.path.join(pasta, 'som-mix.wav'), -14)
normaliza(os.path.join(pasta, 'efeitos-bruto.wav'), os.path.join(pasta, 'som-efeitos.wav'), -16)
