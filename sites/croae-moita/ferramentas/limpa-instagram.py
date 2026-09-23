# Limpa prints de carrossel do Instagram: corta bordas e apaga os botoes < > (retalho vertical em texturas, TELEA em zonas desfocadas).
# Uso: pip install opencv-python-headless numpy; por os prints em ferramentas/prints/N.webp; editar SPEC; python3 limpa-instagram.py

import cv2, numpy as np, os
SPEC = {
  2: dict(esq=0,  topo=0,  botoes=[((704,431),'telea')], nome='evento-placar-hoje-e-dia'),
  3: dict(esq=11, topo=19, botoes=[((43,452),'telea'),((717,452),'patch_down')], nome='evento-stand-festas-moita'),
  4: dict(esq=12, topo=4,  botoes=[((46,436),'patch_up'),((718,436),'patch_up')], nome='cao-preto-julius-k9'),
  5: dict(esq=13, topo=8,  botoes=[((47,439),'patch_up'),((719,439),'patch_up')], nome='cao-branco-festas'),
  6: dict(esq=16, topo=0,  botoes=[((49,425),'telea')], nome='equipa-baloico-moita'),
}
R = 23
def patch_fill(img, cx, cy, r, direcao):
    h,w = img.shape[:2]; d = 2*r+10
    dy = -d if direcao=='patch_up' else d
    if not (0 <= cy-r-4+dy and cy+r+4+dy <= h): dy = -dy
    out = img.copy()
    y0,y1 = max(cy-r-4,0), min(cy+r+4,h); x0,x1 = max(cx-r-4,0), min(cx+r+4,w)
    src = img[y0+dy:y1+dy, x0:x1]
    m = np.zeros((h,w),np.float32); cv2.circle(m,(cx,cy),r,1.0,-1)
    m = cv2.GaussianBlur(m,(0,0),3)[y0:y1,x0:x1][...,None]
    out[y0:y1,x0:x1] = (src*m + out[y0:y1,x0:x1]*(1-m)).astype(np.uint8)
    return out
DEST='../../../media/croae-moita'; os.makedirs(DEST,exist_ok=True)
for i,s in SPEC.items():
    img = cv2.imread(f'prints/{i}.webp'); h,w = img.shape[:2]
    for (cx,cy),modo in s['botoes']:
        if modo=='telea':
            mask = np.zeros((h,w),np.uint8); cv2.circle(mask,(cx,cy),R,255,-1)
            img = cv2.inpaint(img, mask, 10, cv2.INPAINT_TELEA)
        else:
            img = patch_fill(img,cx,cy,R,modo)
    out = img[s['topo']:, s['esq']:]
    cv2.imwrite(f"{DEST}/{s['nome']}.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 92])
    cv2.imwrite(f"{DEST}/{s['nome']}.webp", out, [cv2.IMWRITE_WEBP_QUALITY, 88])
    for k,((cx,cy),_) in enumerate(s['botoes']):
        cx2,cy2 = cx-s['esq'], cy-s['topo']
        cv2.imwrite(f"fin_{i}_b{k}.png", cv2.resize(out[max(cy2-45,0):cy2+45, max(cx2-45,0):cx2+45],(180,180)))
    print(i, s['nome'], out.shape[1],'x',out.shape[0])
import glob
tiles=[cv2.imread(f) for f in sorted(glob.glob('fin_*_b*.png'))]
cv2.imwrite('final_check.png', np.hstack(tiles))
# folha das 5 fotos inteiras
full=[cv2.resize(cv2.imread(f"{DEST}/{s['nome']}.jpg"),(300,350)) for s in SPEC.values()]
cv2.imwrite('final_sheet.png', np.hstack(full))
