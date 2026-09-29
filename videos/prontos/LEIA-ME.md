# Vídeos prontos (anúncios)

Cortados de `videos/brutos/` a 29/09/2026. Formato 4:5 (1080x1350, feed do Facebook/Instagram), 30 fps, H.264, faixa de áudio silenciosa (o som original era só ruído de sala). Enquadrados no ecrã do portátil com o teclado por baixo, fusões de 0,3 s nos cortes, entrada e saída de 0,5 s.

| Ficheiro | Duração | O que saiu |
|---|---|---|
| `bolta-rece-ad-4x5.mp4` | 67 s (de 78) | 3,6 s de herói parado no início; 2,6 s parados na foto do salão; 2,4 s parados no widget; o fim, em que o telemóvel se afasta |
| `hanam-quarteira-ad-4x5.mp4` | 36 s (de 56) | 6,6 s do início (topo da página com a caixa branca e o telemóvel a mexer); 6,6 s a mais no herói; os 6 s finais, em que a página volta ao topo com a caixa branca |
| `jasmim-2-ad-4x5.mp4` | 27 s (de 37) | 2 s do início (fundo da página e o salto para o topo); 6 s a mais no carrossel dos pratos; 1 s do rodapé no fim |

Para voltar a gerar: `videos/brutos/*.mp4` → recorte `crop=478:598:0:Y0` (Y0 = 0 Bolta, 252 Hanam, 220 Jasmim) → `scale=1080:1350` (lanczos) → `hqdn3d` + `unsharp` → segmentos unidos com `xfade` → libx264 CRF 18 (Bolta: CRF 23 com teto de 3,6 Mb/s, para caber nos 30 MB de envio). Os segmentos (segundos no original): Bolta 3,6–54,0 · 56,6–71,0 · 73,4–76,4 · Hanam 6,6–12,0 · 18,6–49,7 · Jasmim 2,0–18,0 · 24,0–35,4.
