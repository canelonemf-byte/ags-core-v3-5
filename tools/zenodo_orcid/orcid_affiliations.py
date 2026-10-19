#!/usr/bin/env python3
"""
Gestiona la *política* de afiliaciones ORCID + lectura pública.

No escribe en ORCID: hace falta Member API + OAuth.
Sí lee el registro público y avisa si aparece una institución prohibida.

  python3 orcid_affiliations.py --print-template
  python3 orcid_affiliations.py --orcid 0000-0002-XXXX-XXXX
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "orcid_afiliaciones.json").read_text(encoding="utf-8"))
PUB = "https://pub.orcid.org/v3.0"


def get_public(orcid: str) -> dict:
    o = orcid.replace("https://orcid.org/", "").strip()
    req = urllib.request.Request(
        f"{PUB}/{o}/record",
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} leyendo ORCID público {o}")


def affiliations_from(record: dict) -> list[dict]:
    acts = record.get("activities-summary") or {}
    out = []
    for section in (
        "employments",
        "educations",
        "invited-positions",
        "memberships",
        "services",
        "qualifications",
        "distinctions",
    ):
        block = acts.get(section) or {}
        groups = block.get("affiliation-group") or []
        for g in groups:
            for s in g.get("summaries") or []:
                # key like employment-summary
                for k, v in s.items():
                    if k.endswith("-summary") and isinstance(v, dict):
                        org = (v.get("organization") or {}).get("name")
                        out.append(
                            {
                                "section": section,
                                "role": v.get("role-title"),
                                "org": org,
                                "city": (v.get("organization") or {}).get("address", {}).get("city")
                                if isinstance((v.get("organization") or {}).get("address"), dict)
                                else None,
                                "source": ((v.get("source") or {}).get("source-name") or {}).get("value"),
                            }
                        )
    return out


def check_forbidden(items: list[dict]) -> list[str]:
    hits = []
    banned = [b.lower() for b in CFG["forbidden_orgs"]]
    for it in items:
        org = (it.get("org") or "").lower()
        for b in banned:
            if b in org:
                hits.append(f"{it['section']}: {it.get('org')}")
    return hits


def print_template() -> None:
    emp = CFG["orcid_ui"]["employment"]
    print("=== ORCID web (Employment → Add) ===")
    print("Organization :", emp["organization"])
    print("City         :", emp["city"])
    print("Region       :", emp["region"])
    print("Country      :", emp["country"])
    print("Role         :", emp["role_title"])
    print("Start        :", emp["start_date"])
    print("URL          :", emp["url"])
    print()
    print("=== Zenodo creator.affiliation (debe coincidir en espíritu) ===")
    print(CFG["zenodo_affiliation_string"])
    print()
    print("=== No añadir ===")
    for b in CFG["forbidden_orgs"]:
        print(" -", b)
    print()
    print("Websites:")
    for w in CFG["orcid_ui"]["websites"]:
        print(f"  {w['label']}: {w['url']}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--orcid")
    p.add_argument("--print-template", action="store_true")
    args = p.parse_args()

    if args.print_template or not args.orcid:
        print_template()
        if not args.orcid:
            return

    rec = get_public(args.orcid)
    person = rec.get("person") or {}
    name = person.get("name") or {}
    print("\n=== Registro público ===")
    print("given :", (name.get("given-names") or {}).get("value"))
    print("family:", (name.get("family-name") or {}).get("value"))
    items = affiliations_from(rec)
    if not items:
        print("sin afiliaciones públicas")
    for it in items:
        print(f"  [{it['section']}] {it.get('role')} @ {it.get('org')}")
    bad = check_forbidden(items)
    if bad:
        print("ALERTA: instituciones que no deben figurar como empleo:")
        for b in bad:
            print(" -", b)
    else:
        print("sin instituciones prohibidas en el registro público")


if __name__ == "__main__":
    main()
