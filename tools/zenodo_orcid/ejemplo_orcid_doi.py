#!/usr/bin/env python3
"""
Integra ORCID en el creator de un DOI Zenodo.

NO inventa un ORCID. Lo lee de:
  1) argumento --orcid 0000-0000-0000-0000
  2) variable ZENODO_ORCID

  python3 ejemplo_orcid_doi.py 22131030
  ZENODO_ORCID=0000-0002-XXXX-XXXX python3 ejemplo_orcid_doi.py 22131030 --apply
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request

API = "https://zenodo.org/api"
ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


def normalize(orcid: str) -> str:
    o = orcid.strip().replace("https://orcid.org/", "").replace("http://orcid.org/", "")
    if not ORCID_RE.match(o):
        sys.exit(f"ORCID con formato inválido: {orcid}")
    return o


def get_public(record_id: int) -> dict:
    with urllib.request.urlopen(f"{API}/records/{record_id}", timeout=30) as r:
        return json.loads(r.read().decode())


def api(method: str, path: str, body=None):
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        sys.exit("Falta ZENODO_TOKEN")
    data = None if body is None else json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode()
        return json.loads(raw) if raw else {}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("record_id", type=int)
    p.add_argument("--orcid")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()

    rec = get_public(args.record_id)
    meta = rec.get("metadata") or {}
    print("DOI   :", rec.get("doi"))
    print("título:", meta.get("title"))
    for c in meta.get("creators") or []:
        print("autor :", c.get("name"), "| orcid:", c.get("orcid"))

    orcid = args.orcid or os.environ.get("ZENODO_ORCID") or ""
    if not orcid:
        print("\nNo hay ORCID. Crea uno en https://orcid.org/register")
        print("Luego: export ZENODO_ORCID=0000-0002-XXXX-XXXX")
        print("No uses el ORCID de homónimos (Sara, Iván, Miguel…).")
        return

    orcid = normalize(orcid)
    print("ORCID a escribir:", orcid)

    if not args.apply:
        print("Dry-run. Añade --apply + ZENODO_TOKEN para grabar.")
        return

    dep = api("GET", f"/deposit/depositions/{args.record_id}")
    md = dict(dep.get("metadata") or {})
    creators = md.get("creators") or []
    if not creators:
        creators = [{"name": "López Paz, Lázaro"}]
    creators[0]["orcid"] = orcid
    creators[0]["name"] = creators[0].get("name") or "López Paz, Lázaro"
    md["creators"] = creators
    api("PUT", f"/deposit/depositions/{args.record_id}", {"metadata": md})
    print("PUT orcid OK")


if __name__ == "__main__":
    main()
