#!/bin/bash
# Deploy do pachecost-demos: correr SÓ quando o Tomás disser «publica» (ordem de 09/10: nenhum deploy automático).
# O Netlify só publica quando sites/demos-pachecost/PUBLICAR.txt muda; os outros pushes acumulam.
#   bash research/cacador/deploy.sh AAAA-MM-DD
set -e
R=$(git rev-parse --show-toplevel); DATA=$1
DEM=claude/dez-negocios-dez-websites-7gevwu; WT=${TMPDIR:-/tmp}/wt-demos
git -C "$R" fetch -q origin $DEM
[ -d "$WT" ] || git -C "$R" worktree add -q "$WT" origin/$DEM
cd "$WT" && git checkout -q --detach origin/$DEM && git reset -q --hard origin/$DEM
echo "$DATA $(TZ=Europe/Bucharest date +%H:%M) — caçador corrida B" >> sites/demos-pachecost/PUBLICAR.txt
git add sites/demos-pachecost/PUBLICAR.txt
git commit -qm "Caçador $DATA: deploy do dia (corrida B)"
for i in 1 2 3 4; do git pull -q --rebase origin $DEM && git push -q origin HEAD:$DEM && break; sleep $((i*2)); done
git log --oneline -1
