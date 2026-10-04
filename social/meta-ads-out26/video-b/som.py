#!/usr/bin/env python3
"""Som do vídeo B, sintetizado (sem samples nem música com direitos): vibrações e toques das notificações,
cliques do esquema, sopros nas transições e um acorde final. Os tempos batem com a linha do tempo de video.html.
Uso: python3 som.py som.wav"""
import math, random, struct, sys, wave

SR, DUR = 48000, 19.5
N = int(SR * DUR)
buf = [0.0] * N
random.seed(7)


def add(t0, dur, fn, amp):
    i0 = int(t0 * SR)
    for k in range(int(dur * SR)):
        i = i0 + k
        if 0 <= i < N:
            buf[i] += amp * fn(k / SR)


def ping(f1, f2, decay=9.0):  # toque de mensagem: duas parciais com decaimento rápido
    return lambda x: (math.sin(2 * math.pi * f1 * x) + .55 * math.sin(2 * math.pi * f2 * x)) * math.exp(-decay * x) * min(1, x * 400)


def buzz(x):  # vibração do telemóvel: 170 Hz quase quadrado, em duas pulsações
    gate = 1.0 if (x % .16) < .11 else 0.0
    s = math.sin(2 * math.pi * 170 * x)
    return math.copysign(abs(s) ** .35, s) * gate * .55


def tick(x):  # clique do esquema
    return (math.sin(2 * math.pi * 1250 * x) * math.exp(-60 * x) + (random.random() * 2 - 1) * math.exp(-300 * x) * .4)


def key(x):  # tecla na bolha a escrever
    return (random.random() * 2 - 1) * math.exp(-500 * x) * .8 + math.sin(2 * math.pi * 2400 * x) * math.exp(-200 * x) * .2


def whoosh(d):  # ruído filtrado com subida e descida
    st = {'y': 0.0}

    def f(x):
        env = math.sin(math.pi * min(1, x / d)) ** 2
        a = .04 + .5 * env  # o filtro abre a meio
        st['y'] += a * ((random.random() * 2 - 1) - st['y'])
        return st['y'] * env
    return f


def pad(freqs, d, att=1.2, rel=1.5):
    def f(x):
        env = min(1, x / att) * min(1, max(0, (d - x) / rel))
        return env * sum(math.sin(2 * math.pi * fr * x + j) * (1 + .003 * math.sin(2 * math.pi * .3 * x)) for j, fr in enumerate(freqs)) / len(freqs)
    return f


# cena 1 · chamadas perdidas (tipos pela ordem de video.html)
tipos = ['ch', 'wa', 'ch', 'ch', 'wa', 'ch', 'ch', 'wa']
for i, tp in enumerate(tipos):
    t = .25 + i * .27
    if tp == 'ch':
        add(t, .32, buzz, .22)
    else:
        add(t, .45, ping(1568, 2349), .16)
add(0, 5.4, pad([55, 82.4], 5.4, att=.6, rel=1.0), .10)          # tensão grave por baixo
add(3.0, .9, lambda x: math.sin(2 * math.pi * 65 * x) * math.exp(-5 * x), .28)  # pancada surda na citação
# transições
add(5.15, .7, whoosh(.7), .30)
add(12.0, .7, whoosh(.7), .30)
# cena 2 · o esquema
for t in (6.05, 6.65, 8.45, 9.0, 9.12, 9.24, 9.25, 9.4, 9.55):
    add(t, .12, tick, .10)
t = 7.05
while t < 8.2:
    add(t, .03, key, .05)
    t += .055 + random.random() * .04
add(10.15, .9, ping(784, 1175, 4), .14)
add(10.32, 1.0, ping(1047, 1568, 4), .12)
add(5.4, 14.1, pad([220, 277.2, 329.6, 440], 14.1, att=1.5, rel=2.0), .055)  # acorde quente quando o sistema entra
# cenas 3 e 4 · regras e diagnóstico
for t in (13.25, 13.67, 14.09, 16.75):
    add(t, .12, tick, .10)
for f, t in ((659.3, 17.7), (987.8, 17.8), (1318.5, 17.9)):
    add(t, 1.9, ping(f, f * 2, 2.2), .11)

peak = max(abs(v) for v in buf) or 1
g = .7 / peak
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'som.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<hh', s, s) for s in (int(max(-1, min(1, v * g)) * 32767) for v in buf)))
