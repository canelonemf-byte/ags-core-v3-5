#!/usr/bin/env python3
"""
Ejemplo mínimo: leer un DOI público, validar el autor y (opcional) corregirlo.

  python3 ejemplo_validar_y_corregir.py 22131030
  ZENODO_TOKEN='...' python3 ejemplo_validar_y_corregir.py 22131030 --apply
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

API = "https://zenodo.org/api"
DOI_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 22131030
APPLY = "--apply" in sys.argv

AUTOR_OK = "López Paz, Lázaro"
AFILIACION_OK = "Investigador independiente, El Prat de Llobregat, Barcelona, España"
PROHIBIDO = (
    "Institute", "Institut", "Fundación", "PERSEI", "Sociedad",
    "Barcelona Institute", "Peptides", "Laboratory",
)


def get_publico(record_id: int) -> dict:
    url = f"{API}/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())


def api(method: str, path: str, body: dict | None = None) -> dict:
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        sys.exit("Para --apply: export ZENODO_TOKEN='...'")
    data = None if body is None else json.dumps(body).encode()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else {}


def validar(meta: dict) -> list[str]:
    errores = []
    creators = meta.get("creators") or []
    if len(creators) != 1:
        errores.append(f"número de autores = {len(creators)} (debe ser 1)")
    for c in creators:
        nombre = c.get("name") or ""
        if any(p in nombre for p in PROHIBIDO):
            errores.append(f"autor institucional: {nombre[:80]}")
        elif nombre != AUTOR_OK:
            errores.append(f"nombre no canónico: {nombre}")
        aff = c.get("affiliation") or ""
        if "El Prat de Llobregat" not in aff:
            errores.append(f"afiliación incompleta: {aff or '(vacía)'}")
    if not (meta.get("description") or "").strip():
        errores.append("descripción vacía")
    return errores


def main() -> None:
    rec = get_publico(DOI_ID)
    meta = rec.get("metadata") or {}
    print("DOI   :", rec.get("doi"))
    print("título:", meta.get("title"))
    for c in meta.get("creators") or []:
        print("autor :", c.get("name"))
        print("aff   :", c.get("affiliation"))

    errores = validar(meta)
    if not errores:
        print("VALIDACIÓN: OK")
        return
    print("VALIDACIÓN: ERRORES")
    for e in errores:
        print(" -", e)

    if not APPLY:
        print("\nSin --apply no se escribe nada.")
        return

    dep = api("GET", f"/deposit/depositions/{DOI_ID}")
    md = dict(dep.get("metadata") or {})
    md["creators"] = [{"name": AUTOR_OK, "affiliation": AFILIACION_OK}]
    api("PUT", f"/deposit/depositions/{DOI_ID}", {"metadata": md})
    print("PUT autores OK. Vuelve a ejecutar sin --apply para comprobar.")


if __name__ == "__main__":
    main()
