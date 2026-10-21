#!/bin/bash
# Adaptación operativa (posterior a la congelación, declarada): enlaza las salidas anidadas out/<run>/<mod>/<mod>/X.json a la ruta que espera cmat005_eval.py. No cambia datos ni criterios.
cd /workspace/omniscience_cmat005/C-MAT-005
for run in run1 run2; do for mod in mattersim mace; do
  for f in out/$run/$mod/$mod/*.json; do [ -e "$f" ] && ln -sf "$mod/$(basename $f)" "out/$run/$mod/$(basename $f)"; done
  for f in out/$run/artefacto/$mod/artefacto/$mod/*.json; do [ -e "$f" ] && ln -sf "artefacto/$mod/$(basename $f)" "out/$run/artefacto/$mod/$(basename $f)"; done
done; done
