#!/usr/bin/env python3
"""
Automatiza la corrección de metadatos de los 15 DOI Zenodo.

Por defecto: DRY-RUN (no escribe).
  python3 zenodo_apply_all.py
  python3 zenodo_apply_all.py --authors-only
  python3 zenodo_apply_all.py --apply --authors-only
  python3 zenodo_apply_all.py --apply

Requiere: export ZENODO_TOKEN='...'  (scope deposit:write)
Token: https://zenodo.org/account/settings/applications/tokens
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = os.environ.get("ZENODO_API", "https://zenodo.org/api")
HERE = Path(__file__).resolve().parent
PACK = json.loads((HERE / "zenodo_metadata.json").read_text(encoding="utf-8"))
CREATOR = PACK["creator"]


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        die(
            "Falta ZENODO_TOKEN.\n"
            "1) https://zenodo.org/account/settings/applications/tokens\n"
            "2) scope deposit:write\n"
            "3) export ZENODO_TOKEN='...'\n"
            "No pegues el token en el chat."
        )
    return t


def api(method: str, path: str, body: dict | None = None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": f"Bearer {token()}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        die(f"HTTP {e.code} {method} {path}\n{err[:2000]}")


def depositions() -> dict[int, dict]:
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


def related(self_id: str) -> list[dict]:
    out = []
    for doi in PACK["related_all"]:
        if doi.endswith(self_id):
            continue
        out.append(
            {
                "identifier": doi,
                "relation": "isPartOf",
                "scheme": "doi",
            }
        )
    return out


def merge_metadata(current: dict, rec_id: str, authors_only: bool) -> dict:
    spec = PACK["records"][rec_id]
    md = dict(current)
    md["creators"] = [
        {"name": CREATOR["name"], "affiliation": CREATOR["affiliation"]}
    ]
    if authors_only:
        return md
    md["title"] = spec["title"]
    md["upload_type"] = spec["upload_type"]
    if spec.get("publication_type") and spec["upload_type"] == "publication":
        md["publication_type"] = spec["publication_type"]
    md["license"] = spec.get("license", "cc-by-4.0")
    md["keywords"] = spec.get("keywords", [])
    md["language"] = spec.get("language", "spa")
    md["description"] = spec["description"]
    md["access_right"] = "open"
    md["related_identifiers"] = related(rec_id)
    return md


def public_snapshot(rec_id: str) -> dict:
    url = f"https://zenodo.org/api/records/{rec_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())["metadata"]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--apply", action="store_true")
    p.add_argument("--authors-only", action="store_true")
    args = p.parse_args()

    print("Objetivo autor:", CREATOR["name"])
    print("Modo:", "APPLY" if args.apply else "DRY-RUN",
          "|", "solo autores" if args.authors_only else "metadatos completos")
    print()

    deps = depositions()
    ok = skip = 0
    for rec_id, spec in PACK["records"].items():
        live = public_snapshot(rec_id)
        live_names = " | ".join(c.get("name", "") for c in live.get("creators") or [])
        print("=" * 64)
        print(f"10.5281/zenodo.{rec_id}")
        print("  live   :", live_names[:90])
        print("  target :", CREATOR["name"])
        if not args.authors_only:
            print("  título :", spec["title"][:80])

        dep = deps.get(int(rec_id))
        if not dep:
            print("  SKIP: el token no es dueño de este record")
            skip += 1
            continue

        new_md = merge_metadata(dep.get("metadata") or {}, rec_id, args.authors_only)
        if not args.apply:
            print(f"  DRY PUT /deposit/depositions/{dep['id']}")
            ok += 1
            continue
        api("PUT", f"/deposit/depositions/{dep['id']}", {"metadata": new_md})
        print(f"  OK  deposition {dep['id']}")
        ok += 1

    print()
    print(f"Listos: {ok}  Skip: {skip}  Total pack: {len(PACK['records'])}")
    if not args.apply:
        print("Nada escrito. Repite con --apply para grabar.")


if __name__ == "__main__":
    main()
