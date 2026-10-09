#!/bin/bash
# Publica demos do caçador no ramo das demos: copia sites/<slug>/ e junta as linhas a DEMOS.
#   bash research/cacador/publicar.sh AAAA-MM-DD slug1 slug2 ...
set -e
R=$(git rev-parse --show-toplevel); DATA=$1; shift
DEM=claude/dez-negocios-dez-websites-7gevwu; WT=${TMPDIR:-/tmp}/wt-demos
git -C "$R" fetch -q origin $DEM
[ -d "$WT" ] || git -C "$R" worktree add -q "$WT" origin/$DEM
cd "$WT" && git checkout -q --detach origin/$DEM && git reset -q --hard origin/$DEM
for s in "$@"; do
  rm -rf "sites/$s"; mkdir -p "sites/$s"
  (cd "$R/sites/$s" && tar cf - --exclude='_fontes' --exclude='*.zip' .) | (cd "sites/$s" && tar xf -)
done
python3 - "$DATA" "$@" <<'PY'
import sys,re
data,slugs=sys.argv[1],sys.argv[2:]
p="sites/demos-pachecost/gerar.py"; s=open(p).read()
i=s.index("DEMOS = ["); j=s.index("\n]\n",i)
novos=[x for x in slugs if f'("{x}", "{x}")' not in s]
if novos:
    cab=f"    # caçador {data}\n"
    bloco=("" if cab in s[i:j] else cab)+"".join(f'    ("{x}", "{x}"),\n' for x in novos)
    if cab in s[i:j]:
        k=s.index(cab,i)+len(cab)
        while s[k:].startswith('    ("'): k=s.index("\n",k)+1
        s=s[:k]+bloco+s[k:]
    else:
        s=s[:j+1]+bloco+s[j+1:]
    open(p,"w").write(s)
print(len(novos),"linhas novas em DEMOS")
PY
git add sites/demos-pachecost/gerar.py $(printf 'sites/%s ' "$@")
git commit -qm "Caçador $DATA: demos $(echo "$@" | tr ' ' ',')" 
for i in 1 2 3 4; do git pull -q --rebase origin $DEM && git push -q origin HEAD:$DEM && break; sleep $((i*2)); done
git log --oneline -1
