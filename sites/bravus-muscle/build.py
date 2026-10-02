# Embute fontes (fontes.css gerado com ferramentas Google Fonts) e fotos de media/ em index.html
import re,base64,sys,os
d=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(d,'index.src.html'),encoding='utf-8').read()
f=open(sys.argv[1],encoding='utf-8').read() if len(sys.argv)>1 else ''
s=s.replace('/*__FONTES__*/',f)
def emb(m):
    path=os.path.join(d,m.group(1))
    if not os.path.exists(path): return m.group(0)
    return 'src="data:image/jpeg;base64,'+base64.b64encode(open(path,'rb').read()).decode()+'"'
s=re.sub(r'src="(media/[^"]+\.jpg)"',emb,s)
open(os.path.join(d,'index.html'),'w',encoding='utf-8').write(s)
print('ok',len(s))
