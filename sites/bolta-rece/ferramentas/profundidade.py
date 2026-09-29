#!/usr/bin/env python3
"""Gera os mapas de profundidade da descida 3D ("Sub boltă") a partir das fotografias reais.

    python3 ferramentas/profundidade.py crama-1 crama-4 pivnita-4 pivnita-1 crama-bolta

Para cada media/<nome>.jpg escreve media/profundidade-<nome>.png (360x240, 8 bits, 255 = perto).
Modelo: Depth Anything V2 Small (licença Apache-2.0, pode usar-se em trabalho comercial), em ONNX,
descarregado uma vez para ferramentas/_modelos/ (fora do git). As versões Base/Large são CC-BY-NC:
não usar em sites de clientes.

Dependências: pip install onnxruntime opencv-python-headless pillow numpy

Como funciona: o modelo aceita 518x518. Corre sobre a foto inteira (esticada) para a estrutura geral e
sobre dois quadrados (esquerda e direita) para o pormenor sem distorção; os três juntam-se (baixas
frequências da foto inteira, pormenor dos quadrados). Depois: normalização robusta, suavização que
respeita arestas e um pixel de dilatação do que está perto, para a borda de cada objeto ficar no
objeto e não na costura esticada.

Afinar no index (src/pages/index.html), em cada <figure data-tip="bolta">:
  data-vp     ponto de fuga (para onde a câmara anda), em 0–1 da foto
  data-z      "perto longe" em metros aproximados (o que está mais perto e mais longe na foto)
  data-avanco quantos metros a câmara entra na foto (mais = mais movimento, mais esticões nas paredes)
  data-luz    candeeiros visíveis na foto: "x y raio" (repetir para vários), tremeluzem
"""
import pathlib, sys, urllib.request

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MODELO = RAIZ / "ferramentas" / "_modelos" / "depth_anything_v2_vits.onnx"
URL = "https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/v2.0.0/depth_anything_v2_vits.onnx"
MEDIA = RAIZ / "media"


def sessao():
    if not MODELO.exists():
        MODELO.parent.mkdir(parents=True, exist_ok=True)
        print("a descarregar o modelo (99 MB)…")
        urllib.request.urlretrieve(URL, MODELO)
    return ort.InferenceSession(str(MODELO), providers=["CPUExecutionProvider"])


MEDIA_NET = np.array([0.485, 0.456, 0.406], np.float32)
DESVIO = np.array([0.229, 0.224, 0.225], np.float32)


def correr(s, img):
    x = np.asarray(img.resize((518, 518), Image.BICUBIC), np.float32) / 255.0
    x = ((x - MEDIA_NET) / DESVIO).transpose(2, 0, 1)[None]
    return s.run(None, {s.get_inputs()[0].name: x})[0][0]


def mapa(s, foto):
    im = Image.open(foto).convert("RGB")
    W, H = im.size
    inteira = cv2.resize(correr(s, im), (W // 4, H // 4), interpolation=cv2.INTER_CUBIC).astype(np.float32)
    h, w = inteira.shape
    lado = H // 4
    soma = np.zeros_like(inteira)
    peso = np.zeros_like(inteira)
    for x0 in (0, w - lado):
        quad = correr(s, im.crop((x0 * 4, 0, x0 * 4 + H, H)))
        quad = cv2.resize(quad, (lado, lado), interpolation=cv2.INTER_CUBIC)
        ref = inteira[:, x0:x0 + lado]
        k, b = np.linalg.lstsq(np.vstack([quad.ravel(), np.ones(quad.size)]).T, ref.ravel(), rcond=None)[0]
        rampa = np.linspace(0, 1, lado)
        p = np.clip((1 - rampa) * 3, 0, 1) if x0 == 0 else np.clip(rampa * 3, 0, 1)
        p = np.repeat(p[None, :], h, 0)
        soma[:, x0:x0 + lado] += (k * quad + b) * p
        peso[:, x0:x0 + lado] += p
    junto = np.where(peso > 0, soma / np.maximum(peso, 1e-6), inteira)
    borrar = lambda a, sg: cv2.GaussianBlur(a.astype(np.float32), (0, 0), sg)
    junto = junto - borrar(junto, 18) + borrar(inteira, 18)
    lo, hi = np.percentile(junto, 0.3), np.percentile(junto, 99.7)
    n = np.clip((junto - lo) / (hi - lo), 0, 1).astype(np.float32)
    n = cv2.resize(n, (360, 240), interpolation=cv2.INTER_AREA)
    n = cv2.bilateralFilter(n, d=7, sigmaColor=0.06, sigmaSpace=3)
    n = cv2.dilate(n, np.ones((3, 3), np.uint8))
    return (n * 255 + 0.5).astype(np.uint8)


def main():
    nomes = sys.argv[1:]
    if not nomes:
        sys.exit(__doc__)
    s = sessao()
    for nome in nomes:
        foto = MEDIA / f"{nome}.jpg"
        destino = MEDIA / f"profundidade-{nome}.png"
        Image.fromarray(mapa(s, foto), mode="L").save(destino, optimize=True)
        print(f"{destino.name}: {destino.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
