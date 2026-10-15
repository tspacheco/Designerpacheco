import cv2, numpy as np, subprocess, sys
SRC='/tmp/claude-0/w/stab60.mp4'; OUT='/tmp/claude-0/w/ext_clean.mp4'
T1=float(sys.argv[1]) if len(sys.argv)>1 else 2.35
cap=cv2.VideoCapture(SRC)
ok,f0=cap.read(); H,W=f0.shape[:2]
# vidro da porta no fotograma 0 (coordenadas 1080x1920)
glass=np.array([[150,915],[490,925],[486,1700],[140,1695]],np.float32)
transom=np.array([[165,745],[530,752],[530,850],[160,846]],np.float32)
window=np.array([[715,780],[1080,790],[1080,1700],[715,1700]],np.float32)
handle=np.array([[130,1225],[205,1225],[205,1300],[130,1300]],np.int32)
def poly_mask(pts,shape):
    m=np.zeros(shape[:2],np.uint8); cv2.fillPoly(m,[pts.astype(np.int32)],255); return m
# placa limpa: apagar a pessoa refletida no fotograma 0
plate=f0.copy()
pm=np.zeros((H,W),np.uint8); cv2.ellipse(pm,(228,1265),(70,215),0,0,360,255,-1)
pm=cv2.dilate(pm,np.ones((15,15),np.uint8))
plate=cv2.inpaint(plate,pm,9,cv2.INPAINT_TELEA)
plate=cv2.GaussianBlur(plate,(0,0),1.2)
plate=(plate.astype(np.float32)*0.82).astype(np.uint8)  # vidro fumado
gmask0=poly_mask(glass,f0.shape); gmask0[handle[0][1]:handle[2][1],handle[0][0]:handle[1][0]]=0
sift=cv2.SIFT_create(3000)
def feats(img,H_):
    ex=np.full(img.shape[:2],255,np.uint8)
    for p in (glass,transom,window):
        q=cv2.perspectiveTransform(p.reshape(-1,1,2),H_).reshape(-1,2)
        cv2.fillPoly(ex,[q.astype(np.int32)],0)
    g=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return sift.detectAndCompute(g,ex)
Hc=np.eye(3); prev=f0; kp_p,de_p=feats(f0,Hc)
ff=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','60','-i','-','-c:v','libx264','-crf','12','-preset','fast','-pix_fmt','yuv420p',OUT],stdin=subprocess.PIPE)
bf=cv2.BFMatcher()
n=0; frame=f0
while True:
    if n>0:
        ok,frame=cap.read()
        if not ok or n/60>T1: break
        kp,de=feats(frame,Hc)
        m=[a for a,b in bf.knnMatch(de_p,de,k=2) if a.distance<0.7*b.distance]
        A=np.float32([kp_p[x.queryIdx].pt for x in m]); B=np.float32([kp[x.trainIdx].pt for x in m])
        Hs,inl=cv2.findHomography(A,B,cv2.RANSAC,3.0)
        Hc=Hs@Hc; kp_p,de_p=kp,de
        # recalcular features com a máscara já atualizada
        kp_p,de_p=feats(frame,Hc)
    wp=cv2.warpPerspective(plate,Hc,(W,H),flags=cv2.INTER_LINEAR)
    wm=cv2.warpPerspective(gmask0,Hc,(W,H))
    wm=cv2.erode(wm,np.ones((5,5),np.uint8))
    a=cv2.GaussianBlur(wm,(0,0),3).astype(np.float32)[...,None]/255
    out=(frame*(1-a)+wp*a).astype(np.uint8)
    ff.stdin.write(out.tobytes()); n+=1
    if n%30==0: print(n, len(m) if n>1 else 0, flush=True)
ff.stdin.close(); ff.wait(); print('frames',n)
