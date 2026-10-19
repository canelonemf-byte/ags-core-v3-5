#!/usr/bin/env python3
"""
Corrige SOLO el autor de los 15 DOI de Lázaro López Paz en Zenodo.

Deja un único creator:
  name:        López Paz, Lázaro
  affiliation: Investigador independiente, El Prat de Llobregat, Barcelona, España

No toca título, ficheros, keywords ni licencia.
El DOI no cambia.

Uso:
  export ZENODO_TOKEN='...'     # scope deposit:write
  python3 zenodo_fix_authors.py              # ensayo en seco
  python3 zenodo_fix_authors.py --apply      # escribe
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = os.environ.get("ZENODO_API", "https://zenodo.org/api")

RECORD_IDS = [
    20761277,
    20812704,
    21238123,
    21321630,
    21345185,
    21361772,
    21401153,
    21513673,
    21640446,
    21721963,
    21806526,
    22028729,
    22131030,
    22131440,
    22150378,
]

CREATOR = {
    "name": "López Paz, Lázaro",
    "affiliation": (
        "Investigador independiente, El Prat de Llobregat, Barcelona, España"
    ),
}


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        sys.exit(
            "Falta ZENODO_TOKEN.\n"
            "https://zenodo.org/account/settings/applications/tokens\n"
            "Scope: deposit:write\n"
            "export ZENODO_TOKEN='...'"
        )
    return t


def api(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token()}",
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        API + path, data=data, headers=headers, method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} {method} {path}\n{err[:2000]}") from e


def list_published() -> dict[int, dict]:
    found: dict[int, dict] = {}
    page = 1
    while True:
        q = urllib.parse.urlencode({"page": page, "size": 100})
        batch = api("GET", f"/deposit/depositions?{q}")
        if not isinstance(batch, list) or not batch:
            break
        for dep in batch:
            rid = dep.get("record_id") or dep.get("id")
            if rid is not None:
                found[int(rid)] = dep
        if len(batch) < 100:
            break
        page += 1
    return found


def public_creators(record_id: int) -> list[str]:
    url = f"https://zenodo.org/api/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        meta = json.loads(resp.read().decode())["metadata"]
    return [c.get("name", "") for c in (meta.get("creators") or [])]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true", help="escribir en Zenodo")
    args = p.parse_args()

    print("Creator objetivo:")
    print(f"  {CREATOR['name']}")
    print(f"  {CREATOR['affiliation']}")
    print("Modo:", "APPLY" if args.apply else "DRY-RUN")
    print()

    if not os.environ.get("ZENODO_TOKEN", "").strip() and not args.apply:
        deps = {}
        print("(sin token: comparación pública; PUT omitido)\n")
    else:
        deps = list_published()

    for rid in RECORD_IDS:
        live = public_creators(rid)
        print("=" * 64)
        print(f"10.5281/zenodo.{rid}")
        print("  ahora :", " | ".join(live) or "(vacío)")
        print("  nuevo :", CREATOR["name"])

        dep = deps.get(rid)
        if not dep:
            print("  SKIP: no está en /deposit/depositions de este token")
            continue

        dep_id = dep["id"]
        current_md = dep.get("metadata") or {}
        new_md = dict(current_md)
        new_md["creators"] = [CREATOR]
        # Evitar dejar autores duplicados tipo PERSEI ×2
        payload = {"metadata": new_md}

        if not args.apply:
            print(f"  DRY  PUT /deposit/depositions/{dep_id}")
            continue

        api("PUT", f"/deposit/depositions/{dep_id}", payload)
        print(f"  OK   deposition {dep_id}")


if __name__ == "__main__":
    main()
