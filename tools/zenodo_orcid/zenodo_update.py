#!/usr/bin/env python3
"""
Actualiza metadatos de depósitos Zenodo del portfolio Lázaro López Paz.

Uso:
  export ZENODO_TOKEN='...'          # token personal, scopes deposit:write
  python3 zenodo_update.py list
  python3 zenodo_update.py diff
  python3 zenodo_update.py apply --dry-run
  python3 zenodo_update.py apply     # escribe de verdad

Token: https://zenodo.org/account/settings/applications/tokens
No compartas el token en el chat. No subas el token a Drive.
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
META_PATH = HERE / "zenodo_metadata.json"


def load_pack() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        sys.exit(
            "Falta ZENODO_TOKEN.\n"
            "Crea uno en https://zenodo.org/account/settings/applications/tokens\n"
            "Scope mínimo: deposit:write\n"
            "Luego: export ZENODO_TOKEN='...'"
        )
    return t


def req(method: str, path: str, body: dict | None = None) -> dict | list:
    url = API + path
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {token()}",
        "Accept": "application/json",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {e.code} {method} {path}\n{err[:2000]}") from e


def related_block(pack: dict, self_doi: str) -> list[dict]:
    out = []
    for doi in pack["related_all"]:
        if doi.endswith(self_doi.split(".")[-1]) or doi == self_doi:
            continue
        out.append(
            {
                "identifier": doi,
                "relation": "isPartOf",
                "resource_type": "publication-technicalnote",
                "scheme": "doi",
            }
        )
    return out[:20]  # Zenodo admite varios; no saturar


def build_metadata(rec_id: str, spec: dict, pack: dict) -> dict:
    creator = pack["creator"]
    md = {
        "title": spec["title"],
        "upload_type": spec["upload_type"],
        "creators": [{"name": creator["name"], "affiliation": creator["affiliation"]}],
        "description": spec["description"],
        "access_right": "open",
        "license": spec.get("license", "cc-by-4.0"),
        "keywords": spec.get("keywords", []),
        "language": spec.get("language", "spa"),
        "related_identifiers": related_block(pack, f"10.5281/zenodo.{rec_id}"),
    }
    if spec.get("publication_type") and spec["upload_type"] == "publication":
        md["publication_type"] = spec["publication_type"]
    return md


def list_depositions() -> list[dict]:
    items: list[dict] = []
    page = 1
    while True:
        q = urllib.parse.urlencode({"page": page, "size": 100, "status": "published"})
        batch = req("GET", f"/deposit/depositions?{q}")
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


def cmd_list(_: argparse.Namespace) -> None:
    rows = list_depositions()
    print(f"{len(rows)} depositions published\n")
    for d in rows:
        rec = d.get("record_id") or d.get("id")
        md = d.get("metadata") or {}
        print(f"{rec}\t{md.get('title', '')[:80]}")
        creators = ", ".join(c.get("name", "") for c in md.get("creators") or [])
        print(f"         {creators[:100]}")


def cmd_diff(_: argparse.Namespace) -> None:
    pack = load_pack()
    public = {}
    for rec_id in pack["records"]:
        url = f"https://zenodo.org/api/records/{rec_id}"
        with urllib.request.urlopen(url, timeout=30) as r:
            public[rec_id] = json.loads(r.read().decode())
    for rec_id, spec in pack["records"].items():
        cur = public[rec_id]["metadata"]
        print("=" * 70)
        print(rec_id)
        print("TÍTULO ahora :", cur.get("title"))
        print("TÍTULO nuevo :", spec["title"])
        names = " | ".join(c.get("name", "") for c in cur.get("creators") or [])
        print("AUTOR  ahora :", names)
        print("AUTOR  nuevo :", pack["creator"]["name"])
        print("LIC    ahora :", cur.get("license"))
        print("LIC    nuevo :", spec.get("license"))
        print("KEYS   ahora :", cur.get("keywords"))
        print("KEYS   nuevo :", spec.get("keywords"))


def cmd_apply(args: argparse.Namespace) -> None:
    pack = load_pack()
    deps = {str(d.get("record_id") or d.get("id")): d for d in list_depositions()}
    for rec_id, spec in pack["records"].items():
        dep = deps.get(str(rec_id))
        if not dep:
            print(f"SKIP {rec_id}: no está en /deposit/depositions (¿otra cuenta?)")
            continue
        dep_id = dep["id"]
        md = build_metadata(rec_id, spec, pack)
        payload = {"metadata": md}
        print(f"{'DRY ' if args.dry_run else 'PUT '} deposition {dep_id} record {rec_id}")
        print("  ", md["title"][:90])
        if args.dry_run:
            continue
        req("PUT", f"/deposit/depositions/{dep_id}", payload)
        print("  OK")


def main() -> None:
    p = argparse.ArgumentParser(description="Zenodo metadata updater")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sub.add_parser("diff")
    ap = sub.add_parser("apply")
    ap.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "diff":
        cmd_diff(args)
    else:
        cmd_apply(args)


if __name__ == "__main__":
    main()
