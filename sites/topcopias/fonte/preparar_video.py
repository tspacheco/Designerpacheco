#!/usr/bin/env python3
"""Prepara os vídeos do hero (Higgsfield) para a web.

  python3 preparar_video.py <horizontal.mp4> <vertical.mp4>

Gera assets/media/hero-h.mp4 (1600 px, sem som), hero-v.mp4 (720x1280, sem som) e os posters .jpg.
Depois corre `python3 build.py`: o hero passa a usar o vídeo em vez da animação em canvas.
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "assets", "media")


def run(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)


def preparar(src, nome, escala):
    os.makedirs(OUT, exist_ok=True)
    mp4 = os.path.join(OUT, nome + ".mp4")
    run("-i", src, "-an", "-vf", escala + ",format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "26",
        "-profile:v", "high", "-movflags", "+faststart", mp4)
    # o poster é o último fotograma (as folhas já empilhadas), para quem não reproduz vídeo
    run("-sseof", "-0.3", "-i", mp4, "-frames:v", "1", "-q:v", "4", os.path.join(OUT, nome + ".jpg"))
    print(nome, round(os.path.getsize(mp4) / 1048576, 1), "MB")


if __name__ == "__main__":
    h, v = sys.argv[1], sys.argv[2]
    preparar(h, "hero-h", "scale=1600:-2")
    preparar(v, "hero-v", "scale=720:-2")
