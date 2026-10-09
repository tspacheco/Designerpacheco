#!/usr/bin/env bash
# Espera pelo commit «Ponte: …» depois do último push, numa só chamada (modo economia), e imprime só o resumo.
#   bash research/cacador/esperar.sh [minutos, 9 por omissão]
R=claude/cacador-diario-nkiz36
base=$(git rev-parse HEAD)
fim=$(( $(date +%s) + ${1:-9} * 60 ))
while [ "$(date +%s)" -lt "$fim" ]; do
  sleep 30
  git fetch -q origin "$R" 2>/dev/null || continue
  if git log --format=%s "$base..origin/$R" | grep -q '^Ponte:'; then
    git pull -q --rebase origin "$R"
    echo "ponte: $(grep -c '^ok' ponte/relatorio.txt) ok, $(grep -c '^ERRO' ponte/relatorio.txt) erros"
    grep '^ERRO' ponte/relatorio.txt | cut -c1-140 | head -5
    exit 0
  fi
done
echo "ponte ainda sem resposta; correr outra vez"
