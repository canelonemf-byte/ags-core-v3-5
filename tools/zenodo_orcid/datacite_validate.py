#!/usr/bin/env python3
"""
Valida metadatos DataCite de los DOI 10.5281/zenodo.*

  python3 datacite_validate.py
  python3 datacite_validate.py --json-out datacite_report.json
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDS = [
    20761277, 20812704, 21238123, 21321630, 21345185,
    21361772, 21401153, 21513673, 21640446, 21721963,
    21806526, 22028729, 22131030, 22131440, 22150378,
]
PERSON = "López Paz, Lázaro"
ORG_HINTS = (
    "Institute", "Institut", "Fundación", "International", "Group",
    "Sociedad", "PERSEI", "Laboratory", "Astrofísica", "Ingeniería",
    "Barcelona Institute", "Peptides", "Fractal", "Microbiology",
)


def datacite(doi: str) -> dict:
    url = f"https://api.datacite.org/dois/{doi}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.api+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json-out")
    args = p.parse_args()
    rows = []
    print(f"{'DOI':<10} {'state':<9} {'type':<14} {'orcid':<5} {'E':<2} problemas")
    print("-" * 88)
    for i in IDS:
        doi = f"10.5281/zenodo.{i}"
        payload = datacite(doi)
        attr = (payload.get("data") or {}).get("attributes") or {}
        creators = attr.get("creators") or []
        errors, warns = [], []
        if attr.get("state") != "findable":
            errors.append(f"state={attr.get('state')}")
        if len(creators) != 1:
            errors.append(f"n_creators={len(creators)}")
        for c in creators:
            name = c.get("name") or ""
            ntype = c.get("nameType")
            if ntype == "Organizational" or any(h in name for h in ORG_HINTS):
                errors.append(f"nameType={ntype} org={name[:50]}")
            if name != PERSON and ntype == "Personal":
                warns.append(f"nombre {name}")
            ids = c.get("nameIdentifiers") or []
            if any((x.get("nameIdentifierScheme") or "").upper() == "ORCID" for x in ids):
                pass
            else:
                warns.append("sin ORCID")
            if any((x.get("nameIdentifierScheme") or "").upper() in ("ROR", "ISNI") for x in ids):
                if ntype != "Personal":
                    errors.append("ROR/ISNI de institución en el autor")
        rights = attr.get("rightsList") or []
        rid = (rights[0].get("rightsIdentifier") if rights else None) or ""
        if rid and not rid.lower().startswith(("cc-by", "mit", "cc0")):
            warns.append(f"rights={rid}")
        if not rights:
            errors.append("sin rightsList")
        if not (attr.get("relatedIdentifiers") or []):
            warns.append("sin relatedIdentifiers")
        print(
            f"{i}  {str(attr.get('state')):<9} {str((creators[0] or {}).get('nameType')):<14} "
            f"{'no':<5} {len(errors):<2} {'; '.join(errors)[:55]}"
        )
        rows.append(
            {
                "doi": doi,
                "state": attr.get("state"),
                "url": attr.get("url"),
                "errors": errors,
                "warnings": warns,
                "creators": creators,
                "rights": rights,
            }
        )
    print("-" * 88)
    print(f"errores: {sum(1 for r in rows if r['errors'])}/{len(rows)}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
