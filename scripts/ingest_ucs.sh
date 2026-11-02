#!/usr/bin/env bash
# Ingesta .txt/.md/.tex de knowledge/<proyecto> con doc_chunker v1.1 (manifiesto evita duplicados).
# Usa find -print0 / read -d '' para soportar espacios en nombres de archivo.
set -uo pipefail
R=/workspace/agsgpt/ags-core-v3.6
export API_URL=http://localhost:8000 AGS_API_KEY="$(cat $R/data/api_key)" CHUNKER_MANIFEST=$R/data/ucs_chunker_manifest.json
P=("$@"); [ ${#P[@]} -eq 0 ] && P=(omniscience oraculo-mesoscopico remplast-q cero-a-amoniaco ordenador-hibrido-no-binario fusi-n-carpeta hybrix)
for p in "${P[@]}"; do
  while IFS= read -r -d '' f; do
    echo "== $p :: ${f#$R/knowledge/}"
    /workspace/agsgpt/.venv/bin/python "$R/ucs/doc_chunker.py" "$f" "$p" 2>&1 | tail -1
  done < <(find "$R/knowledge/$p" -type f \( -name '*.txt' -o -name '*.md' -o -name '*.tex' \) -print0 2>/dev/null)
done
