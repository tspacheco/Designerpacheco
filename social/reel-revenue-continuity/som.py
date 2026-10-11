#!/usr/bin/env python3
"""Som do reel «Revenue leaks after the yes», sintetizado em numpy (sem samples nem música com direitos).
Camadas: pad quente em Ré (drone com batimento lento), pulso suave a 100 BPM, «whoosh» + baque em cada corte do clip,
ping curto na entrada de cada bloco de texto, três pings a subir quando os nós da cadeia acendem, acorde de chegada no fecho.
Uso: python3 som.py tempos.json saida.wav   (tempos.json = window.SFX da overlay.html)"""
import json, sys, wave
import numpy as np

SR = 48000
ev = json.load(open(sys.argv[1])); OUT = sys.argv[2]
DUR = float(ev.get('dur', 35.0)); N = int(SR * DUR)
rng = np.random.default_rng(11)
mix = np.zeros(N)
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
tt = lambda d: np.arange(int(d * SR)) / SR


def put(t0, sig, amp=1.0):
    i0 = int(t0 * SR)
    if i0 < 0 or i0 >= N:
        return
    sig = sig[:N - i0]
    mix[i0:i0 + len(sig)] += amp * sig


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc = a * acc + (1 - a) * v
        y[i] = acc
    return y


def thud(f0=60, dec=8, d=.7):
    x = tt(d); f = f0 * 0.6 + f0 * 0.4 * np.exp(-x * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * dec)


def whoosh(d=.42):
    x = tt(d); n = rng.uniform(-1, 1, len(x))
    env = np.sin(np.pi * np.minimum(1, x / d)) ** 1.5
    return lowpass(n, 2200) * env - lowpass(n, 300) * env * .6


def ping(m, d=.7, bright=.3):
    x = tt(d); f = hz(m)
    env = np.exp(-x * 6) * np.minimum(1, x * 600)
    return (np.sin(2 * np.pi * f * x) + bright * np.sin(2 * np.pi * f * 2.005 * x)) * env


def pad(ms, d, att=.8, rel=1.5):
    x = tt(d); s = np.zeros_like(x)
    for m in ms:
        s += np.sin(2 * np.pi * hz(m) * x) + .35 * np.sin(2 * np.pi * hz(m) * 2.003 * x + .4) + .2 * np.sin(2 * np.pi * hz(m) * .5 * x)
    env = np.minimum(1, x / att) * np.clip((d - x) / rel, 0, 1)
    return s / len(ms) * env


x = tt(DUR)
# 1) pad: Ré grave + quinta, com batimento lento e um leve «respirar» (sobe um pouco na 2.ª metade)
drone = pad([38, 45, 50], DUR, 1.2, 1.2) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.11 * x))
put(0, drone, .16)
# 2) pulso a 100 BPM, muito baixo, com acento em cada 4 (dá o ritmo às entradas de texto)
beat = 60 / 100
k = 0
t0 = 0.0
while t0 < DUR - .2:
    put(t0, thud(48, 26, .18), .11 if k % 4 else .17); k += 1; t0 += beat
# 3) cortes do clip: whoosh + baque
for c in ev.get('cuts', []):
    put(c - .22, whoosh(), .32)
    put(c, thud(55, 9, .8), .55)
# 4) entrada de cada bloco de texto: ping curto (Lá4), e no gancho um baque de abertura
for i, b in enumerate(ev.get('blocks', [])):
    put(b + .05, ping(69 if i else 57, .5), .16)
put(0.0, thud(50, 5, 1.2), .7)
# 5) cadeias: três pings a subir (Ré5, Fá#5, Lá5) a 0,45 s, como os nós a acender
for c in ev.get('chains', []):
    for j, m in enumerate([74, 78, 81]):
        put(c + j * .45, ping(m, .6, .25), .14)
# 6) fecho: acorde Ré maior com 9.ª a crescer até ao fim + baque
t_end = float(ev.get('end', 32.5))
put(t_end, thud(45, 4, 1.4), .6)
put(t_end, pad([50, 57, 62, 64, 69], DUR - t_end + 1, .6, 1.0), .22)
# limitador simples + fade final
mix = np.tanh(mix * 1.3) * .9
mix[-int(.4 * SR):] *= np.linspace(1, 0, int(.4 * SR))
w = wave.open(OUT, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()
print('ok', OUT, f'{DUR:.1f}s pico {np.abs(mix).max():.2f}')
