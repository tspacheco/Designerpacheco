#!/bin/bash
cd /tmp/claude-0/w
G="scale=1920:1080:flags=lanczos,eq=contrast=1.07:saturation=1.12:gamma=1.04,unsharp=5:5:0.5:5:5:0.0,fps=30,format=yuv420p"
seg(){ ffmpeg -v error -y -i $6 -vf "trim=$2:$3,crop=1080:608:0:'$5',setpts=(PTS-STARTPTS)/$4,$G" -an -c:v libx264 -crf 14 -preset fast v3$1.mp4; }
seg A 0.0 1.3 0.45 "20+t*385" ext_clean.mp4
seg P 0.5 2.3 0.5 "${PY:-820+(t-0.9)*60}" ext_clean.mp4
seg I 6.9 14.2 0.6 "${IY:-760+220*clip((t-8.8)/0.8\,0\,1)-280*clip((t-11.6)/0.8\,0\,1)}" stab60.mp4
for s in A P I; do ffprobe -v error -show_entries format=duration -of csv=p=0 v3$s.mp4; done
ffmpeg -v error -y -i v3P.mp4 -vf "fps=1.5,scale=480:-1,tile=5x1" -frames:v 1 cP.jpg
ffmpeg -v error -y -i v3I.mp4 -vf "fps=0.75,scale=480:-1,tile=5x2" -frames:v 1 cI.jpg
