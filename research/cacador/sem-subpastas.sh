#!/bin/bash
# Passa as fotos usadas de media/g/ para media/g-NN.webp (o motor das demos não copia subpastas).
for s in "$@"; do
  d=sites/$s; grep -q 'media/g/' $d/index.html || continue
  for f in $d/media/g/*; do cp "$f" "$d/media/g-$(basename "$f")"; done
  sed -i 's#media/g/#media/g-#g' $d/index.html $d/pt.html $d/index.src.html 2>/dev/null
  echo "$s corrigido"
done
