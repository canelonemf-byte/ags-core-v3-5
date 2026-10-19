#!/usr/bin/env bash
# Automatiza la corrección. El token NO va en este archivo.
set -euo pipefail
cd "$(dirname "$0")"

if [[ -z "${ZENODO_TOKEN:-}" ]]; then
  echo "export ZENODO_TOKEN='...'  # https://zenodo.org/account/settings/applications/tokens"
  exit 1
fi

echo "== 1/3 dry-run solo autores =="
python3 zenodo_apply_all.py --authors-only

echo "== 2/3 apply solo autores =="
python3 zenodo_apply_all.py --apply --authors-only

echo "== 3/3 apply metadatos completos =="
python3 zenodo_apply_all.py --apply

echo "Hecho. Comprueba un DOI: https://zenodo.org/records/22131030"
