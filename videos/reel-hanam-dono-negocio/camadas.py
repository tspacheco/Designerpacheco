from PIL import Image, ImageDraw, ImageFont
import sys
S=sys.argv[1]
W,H=1080,1920
BUN=S+'/bungee.ttf'
INTB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
INTX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'
INTS='/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
ACC=(255,122,61,255)
def canvas(): return Image.new('RGBA',(W,H),(0,0,0,0))
def center(d,y,txt,font,fill):
    w=d.textlength(txt,font=font); d.text(((W-w)/2,y),txt,font=font,fill=fill); return w
# L1
im=canvas(); d=ImageDraw.Draw(im); f=ImageFont.truetype(BUN,104)
center(d,170,'ÉS DONO DE',f,(255,255,255,255)); center(d,290,'UM NEGÓCIO?',f,(255,255,255,255))
im.save(S+'/l1.png')
# L2
im=canvas(); d=ImageDraw.Draw(im); f=ImageFont.truetype(INTB,50)
y=440
for ln in ['O teu negócio pode começar com','um website destes e ir até uma','infraestrutura de IA.']:
    center(d,y,ln,f,(236,236,236,255)); y+=64
im.save(S+'/l2.png')
# Insight
im=canvas(); d=ImageDraw.Draw(im)
x0,y0,x1,y1=70,1440,W-70,1640
d.rounded_rectangle((x0,y0,x1,y1),radius=22,fill=(14,12,10,225),outline=(255,122,61,140),width=2)
d.rounded_rectangle((x0,y0,x0+12,y1),radius=6,fill=ACC)
fl=ImageFont.truetype(INTX,26)
d.text((x0+44,y0+28),'I N S I G H T',font=fl,fill=ACC)
fa=ImageFont.truetype(INTX,52); fb=ImageFont.truetype(INTS,40)
d.text((x0+44,y0+70),'Reduz até 40% os custos',font=fa,fill=ACC)
d.text((x0+44,y0+134),'sem contratar mais ninguém.',font=fb,fill=(255,255,255,255))
im.save(S+'/ins.png')
