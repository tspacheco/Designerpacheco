#!/usr/bin/env python3
"""Som do reel «5 things under one AI question», sintetizado com numpy (sem samples nem música com direitos).
Camadas: drone grave que desce de tom durante a queda, vento que cresce com a profundidade, impacto no gancho,
um baque + ping de sonar (cada vez mais grave) em cada uma das 5 camadas, acorde de chegada no fecho.
Se o clip base tiver áudio (Kling gera ambiente), mistura-o em fundo a −12 dB.
Uso: python3 som.py tempos.json base.mp4 saida.wav"""
import json, subprocess, sys, wave
import numpy as np

SR = 48000
ev = json.load(open(sys.argv[1]))
BASE, OUT = sys.argv[2], sys.argv[3]
DUR = float(ev.get('dur', 15.0))
N = int(SR * DUR)
rng = np.random.default_rng(7)
mix = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(d * SR)) / SR


def put(t0, sig, amp=1.0):
    i0 = int(t0 * SR)
    if i0 >= N or i0 < 0:
        return
    sig = sig[:N - i0]
    mix[i0:i0 + len(sig)] += amp * sig


def lowpass(x, cutoff):
    # filtro de 1.º ordem (RC) — chega para vento e drones
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc = a * acc + (1 - a) * v
        y[i] = acc
    return y


def lowpass_sweep(x, c0, c1):
    # cutoff a subir de c0 a c1 ao longo do sinal (vento que abre com a queda)
    n = len(x); y = np.empty_like(x); acc = 0.0
    cut = np.geomspace(c0, c1, n); a = np.exp(-2 * np.pi * cut / SR)
    for i in range(n):
        acc = a[i] * acc + (1 - a[i]) * x[i]
        y[i] = acc
    return y


def thud(f0=70, dec=9, d=.6):
    x = tt(d); f = f0 * 0.55 + f0 * 0.45 * np.exp(-x * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * dec) + .3 * lowpass(rng.uniform(-1, 1, len(x)), 900) * np.exp(-x * 60)


def ping(m, d=.9):
    x = tt(d); f = hz(m)
    env = np.exp(-x * 5) * np.minimum(1, x * 400)
    return (np.sin(2 * np.pi * f * x) + .35 * np.sin(2 * np.pi * f * 2.01 * x)) * env


def pad(ms, d, att=.6):
    x = tt(d); s = np.zeros_like(x)
    for m in ms:
        s += np.sin(2 * np.pi * hz(m) * x) + .4 * np.sin(2 * np.pi * hz(m) * 2 * x + .3)
    env = np.minimum(1, x / att) * np.clip((d - x) / 1.2, 0, 1)
    return s / len(ms) * env


# 1) drone: Mi grave a descer uma oitava durante o reel, com pulsação lenta
x = tt(DUR)
f = hz(40) * 2 ** (-x / DUR * 1.0)           # E2 → E1
drone = np.sin(2 * np.pi * np.cumsum(f) / SR) + .5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
drone *= (0.75 + 0.25 * np.sin(2 * np.pi * 0.5 * x)) * np.minimum(1, x * 2) * np.clip((DUR - x) / 1.0, 0, 1)
put(0, drone, .22)

# 2) vento: ruído filtrado que abre e cresce com a profundidade
wind = lowpass_sweep(rng.uniform(-1, 1, N), 120, 2600)
wind *= np.minimum(1, (x / 1.2) ** 1.6) * np.clip((DUR - .4 - x) / 1.0, 0, 1)
put(0, wind, .18)

# 3) gancho: impacto no 1.º fotograma e na 2.ª linha
put(0.0, thud(60, 6, .9), .9)
put(float(ev.get('hook2', 1.2)), thud(80, 10, .5), .55)

# 4) camadas: baque + ping de sonar cada vez mais grave
for i, t0 in enumerate(ev.get('facts', [3, 5, 7, 9, 11])):
    put(t0, thud(75 - i * 6, 8, .7), .8)
    put(t0 + .05, ping(88 - i * 3), .28)

# 5) fecho: acorde de chegada (Mi menor com 9.ª) e um ping final
t_end = float(ev.get('end', 13.0))
put(t_end, thud(55, 5, 1.2), .9)
put(t_end + .02, pad([40, 47, 52, 55, 66], DUR - t_end, .35), .35)
put(t_end + .3, ping(76, 1.6), .22)

# 6) ambiente do clip base (se tiver áudio)
try:
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', BASE, '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    amb = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    amb = amb[:N]
    if len(amb):
        amb = lowpass(amb, 4000) * np.clip((DUR - .5 - x[:len(amb)]) / .5, 0, 1)
        put(0, amb, .25)
except Exception as ex:
    print('sem ambiente do clip:', ex)

# limitador simples + fade final
mix = np.tanh(mix * 1.4) * .95
mix[-int(.3 * SR):] *= np.linspace(1, 0, int(.3 * SR))
w = wave.open(OUT, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print('ok', OUT, f'{DUR:.1f}s pico {np.abs(mix).max():.2f}')
