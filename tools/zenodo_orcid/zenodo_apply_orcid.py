#!/usr/bin/env python3
"""
Añade ORCID al creator de los 15 DOI Zenodo.

NO inventa un iD. Fuentes, en este orden:
  --orcid 0000-0002-XXXX-XXXX
  $ZENODO_ORCID
  zenodo_metadata.json → creator.orcid

También normaliza el nombre a «López Paz, Lázaro» para que
DataCite deje de marcar Organizational.

  python3 zenodo_apply_orcid.py
  python3 zenodo_apply_orcid.py --orcid 0000-0002-XXXX-XXXX
  python3 zenodo_apply_orcid.py --orcid 0000-0002-XXXX-XXXX --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = os.environ.get("ZENODO_API", "https://zenodo.org/api")
HERE = Path(__file__).resolve().parent
PACK = json.loads((HERE / "zenodo_metadata.json").read_text(encoding="utf-8"))
ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
NAME = PACK["creator"]["name"]
AFF = PACK["creator"]["affiliation"]


def normalize_orcid(raw: str) -> str:
    o = (raw or "").strip().replace("https://orcid.org/", "").replace("http://orcid.org/", "")
    if not ORCID_RE.match(o):
        sys.exit(
            "ORCID inválido o ausente.\n"
            "Crea el tuyo en https://orcid.org/register\n"
            "Luego: --orcid 0000-0002-XXXX-XXXX  o  export ZENODO_ORCID=...\n"
            "No uses iD de Sara / Iván / Miguel López Paz."
        )
    return o


def resolve_orcid(cli: str | None) -> str:
    for candidate in (cli, os.environ.get("ZENODO_ORCID"), PACK.get("creator", {}).get("orcid")):
        if candidate:
            return normalize_orcid(str(candidate))
    return normalize_orcid("")  # dispara el mensaje de ayuda


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        sys.exit("Falta ZENODO_TOKEN (scope deposit:write)")
    return t


def api(method: str, path: str, body=None):
    data = None if body is None else json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {token()}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else {}


def depositions() -> dict[int, dict]:
    try:
        from zenodo_paginate import fetch_all_depositions
        batch = fetch_all_depositions(token(), api=API)
    except Exception:
        batch, page = [], 1
        while True:
            q = urllib.parse.urlencode({"page": page, "size": 100})
            chunk = api("GET", f"/deposit/depositions?{q}")
            if not isinstance(chunk, list) or not chunk:
                break
            batch.extend(chunk)
            if len(chunk) < 100:
                break
            page += 1
    out = {}
    for dep in batch:
        rid = dep.get("record_id") or dep.get("id")
        if rid is not None:
            out[int(rid)] = dep
    return out


def public_orcid(record_id: int) -> tuple[str, str | None]:
    url = f"https://zenodo.org/api/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as r:
        meta = json.loads(r.read().decode())["metadata"]
    cs = meta.get("creators") or []
    name = cs[0].get("name") if cs else ""
    orcid = cs[0].get("orcid") if cs else None
    return name, orcid


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--orcid")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--keep-name", action="store_true",
                   help="no tocar name/affiliation; solo añadir orcid")
    args = p.parse_args()

    orcid = resolve_orcid(args.orcid)
    print("ORCID objetivo:", orcid)
    print("Nombre objetivo:", NAME if not args.keep_name else "(se conserva)")
    print("Modo:", "APPLY" if args.apply else "DRY-RUN")
    print()

    deps = depositions() if args.apply or os.environ.get("ZENODO_TOKEN") else {}
    if not deps and args.apply:
        sys.exit("El token no listó depositions.")

    ok = skip = 0
    for rec_id in PACK["records"]:
        live_name, live_orcid = public_orcid(int(rec_id))
        print("=" * 60)
        print(f"10.5281/zenodo.{rec_id}")
        print("  name  live:", live_name[:70])
        print("  orcid live:", live_orcid)
        print("  orcid new :", orcid)

        dep = deps.get(int(rec_id))
        if not dep:
            print("  SKIP: no está en la cuenta del token" if args.apply else "  DRY (sin deposition)")
            skip += 1
            continue
        md = dict(dep.get("metadata") or {})
        creators = list(md.get("creators") or [{}])
        c0 = dict(creators[0])
        if not args.keep_name:
            c0["name"] = NAME
            c0["affiliation"] = AFF
        c0["orcid"] = orcid
        md["creators"] = [c0]
        if not args.apply:
            print(f"  DRY PUT /deposit/depositions/{dep['id']}")
            ok += 1
            continue
        api("PUT", f"/deposit/depositions/{dep['id']}", {"metadata": md})
        print("  OK")
        ok += 1

    print(f"\nlistos {ok}  skip {skip}")
    print("DataCite tardará minutos–horas en mostrar nameIdentifiers ORCID.")


if __name__ == "__main__":
    main()
