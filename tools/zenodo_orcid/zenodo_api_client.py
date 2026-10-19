#!/usr/bin/env python3
"""
Cliente mínimo de la API REST de Zenodo (Invenio).

Endpoints usados:
  GET  /api/deposit/depositions
  GET  /api/deposit/depositions/{id}
  PUT  /api/deposit/depositions/{id}     {"metadata": {...}}
  GET  /api/records/{id}                 (público, sin token)

Auth:  Authorization: Bearer $ZENODO_TOKEN
Token: https://zenodo.org/account/settings/applications/tokens
Scope: deposit:write

Ejemplos:
  export ZENODO_TOKEN='...'
  python3 zenodo_api_client.py list
  python3 zenodo_api_client.py get 22131030
  python3 zenodo_api_client.py set-author 22131030
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

CREATOR = {
    "name": "López Paz, Lázaro",
    "affiliation": "Investigador independiente, El Prat de Llobregat, Barcelona, España",
}


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        sys.exit("Falta ZENODO_TOKEN (scope deposit:write)")
    return t


def request(method: str, path: str, body: dict | None = None, auth: bool = True):
    headers = {"Accept": "application/json"}
    if auth:
        headers["Authorization"] = f"Bearer {token()}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {method} {path}\n{e.read().decode('utf-8', 'replace')[:2000]}")


def list_depositions() -> list[dict]:
    out, page = [], 1
    while True:
        q = urllib.parse.urlencode({"page": page, "size": 100})
        batch = request("GET", f"/deposit/depositions?{q}")
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def get_public(record_id: int) -> dict:
    url = f"https://zenodo.org/api/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def set_single_author(deposition_id: int, creator: dict = CREATOR) -> dict:
    dep = request("GET", f"/deposit/depositions/{deposition_id}")
    md = dict(dep.get("metadata") or {})
    md["creators"] = [creator]
    return request("PUT", f"/deposit/depositions/{deposition_id}", {"metadata": md})


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    g = sub.add_parser("get")
    g.add_argument("record_id", type=int)
    s = sub.add_parser("set-author")
    s.add_argument("record_id", type=int)
    args = p.parse_args()

    if args.cmd == "list":
        for d in list_depositions():
            rid = d.get("record_id") or d.get("id")
            title = (d.get("metadata") or {}).get("title", "")
            print(f"{rid}\t{title[:80]}")
        return

    if args.cmd == "get":
        rec = get_public(args.record_id)
        md = rec.get("metadata") or {}
        print("title:", md.get("title"))
        print("doi  :", rec.get("doi"))
        for c in md.get("creators") or []:
            print("author:", c.get("name"), "|", c.get("affiliation"))
        print("license:", md.get("license"))
        return

    # set-author: record_id público ≈ deposition id en estos 15
    out = set_single_author(args.record_id)
    names = [c.get("name") for c in (out.get("metadata") or {}).get("creators") or []]
    print("updated creators:", names)


if __name__ == "__main__":
    main()
