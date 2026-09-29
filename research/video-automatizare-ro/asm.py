import subprocess as sp, os
def run(c):
    print(">>", c[:160], flush=True); sp.run(c, shell=True, check=True)
V = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"
ENC = "-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -an"
# (seg, clip, start, dur, pts, bg-filter, overlays[(png,t0,t1)])
S = [
 ("A","s1",0,3.2,1,"",[("a1",.15,1.6),("a2",1.6,9)]),
 ("B","s2",0,3.6,1,"",[("b1",.2,1.7),("b2",1.7,9)]),
 ("C","s3",0,2.8,1,"",[("c1",.5,9)]),
 ("D","s3",0,6.0,1.5,",boxblur=18:2,eq=brightness=-0.12",[("d1",0,.9),("d2",.9,1.8),("d3",1.8,3.4),("d4",3.4,4.4),("d5",4.4,9)]),
 ("E","s4",0,3.6,1,"",[("e1",.2,1.6),("e2",1.6,9)]),
 ("F","s5",0,3.2,1,"",[("f1",.2,1.0),("f2",1.0,1.8),("f3",1.8,9)]),
]
for seg,clip,ss,d,pts,bg,ovs in S:
    ins = f"-i {clip}.mp4 " + " ".join(f"-loop 1 -t {d} -i ov/{o}.png" for o,_,_ in ovs)
    f = f"[0:v]setpts={pts}*PTS,{V}{bg},tpad=stop_mode=clone:stop_duration=3,trim=0:{d},setpts=PTS-STARTPTS[b0];"
    for i,(o,t0,t1) in enumerate(ovs):
        f += f"[b{i}][{i+1}:v]overlay=0:0:enable='between(t,{t0},{t1})'[b{i+1}];"
    f = f.rstrip(";").rsplit("[",1)[0] + "[v]"
    run(f'ffmpeg -v error -y {ins} -filter_complex "{f}" -map "[v]" -t {d} {ENC} seg{seg}.mp4')
# G — fecho: último frame de s5 desfocado + cartão de preço
run(f'ffmpeg -v error -y -sseof -0.1 -i s5.mp4 -frames:v 1 last5.png')
run(f'ffmpeg -v error -y -loop 1 -t 4 -i last5.png -loop 1 -t 4 -i ov/g1.png -filter_complex "[0:v]{V},boxblur=22:2,eq=brightness=-0.15[b];[1:v]format=rgba,fade=t=in:st=0:d=0.35:alpha=1[o];[b][o]overlay=0:0[v]" -map "[v]" -t 4 {ENC} segG.mp4')
open("list.txt","w").write("".join(f"file 'seg{s}.mp4'\n" for s in "ABCDEFG"))
run("ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy video.mp4")
# SOM: ambiente + vibrações + notificações + ding
run("sox -n -r 44100 -c 2 amb.wav synth 26.4 brownnoise vol 0.06 lowpass 700")
run("sox -n -r 44100 -c 2 buzz.wav synth 0.32 sine 165 tremolo 28 95 vol 0.55 fade 0.01 0.32 0.04")
run("sox -n -r 44100 -c 2 pop.wav synth 0.09 sine 1250:760 vol 0.45 fade 0 0.09 0.06")
run("sox -n -r 44100 -c 2 ding.wav synth 0.9 pluck E5 vol 0.5 fade 0 0.9 0.6")
ev = [("buzz",.3),("buzz",1.1),("buzz",2.1),("buzz",3.8),("pop",9.6),("pop",11.4),("pop",13.0),("pop",14.0),("ding",22.5)]
ins = "-i amb.wav " + " ".join(f"-i {n}.wav" for n,_ in ev)
f = "".join(f"[{i+1}:a]adelay={int(t*1000)}|{int(t*1000)}[e{i}];" for i,(n,t) in enumerate(ev))
f += "[0:a]" + "".join(f"[e{i}]" for i in range(len(ev))) + f"amix=inputs={len(ev)+1}:normalize=0,afade=t=out:st=25.6:d=0.8[a]"
run(f'ffmpeg -v error -y {ins} -filter_complex "{f}" -map "[a]" -t 26.4 audio.wav')
run("ffmpeg -v error -y -i video.mp4 -i audio.wav -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart final.mp4")
run("ffmpeg -v error -y -ss 1.7 -i final.mp4 -frames:v 1 -q:v 3 capa.jpg")
print(sp.run("ffprobe -v error -show_entries format=duration,size -of csv=p=0 final.mp4",shell=True,capture_output=True,text=True).stdout)
