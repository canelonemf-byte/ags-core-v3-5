#!/usr/bin/env python3
"""
Validador configurable de metadatos Zenodo.

  python3 zenodo_validate.py
  python3 zenodo_validate.py --config zenodo_validate_config.json
  python3 zenodo_validate.py --json-out report.json
  python3 zenodo_validate.py --fail-on error     # exit 1 si hay errores
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def public_record(record_id: int) -> dict:
    url = f"https://zenodo.org/api/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def license_id(meta: dict) -> str | None:
    lic = meta.get("license")
    if isinstance(lic, dict):
        return lic.get("id")
    return str(lic) if lic else None


def check_record(record_id: int, cfg: dict, pack: dict | None) -> dict:
    rec = public_record(record_id)
    meta = rec.get("metadata") or {}
    files = rec.get("files") or []
    errors: list[str] = []
    warns: list[str] = []

    creators = meta.get("creators") or []
    names = [c.get("name") or "" for c in creators]
    affs = [c.get("affiliation") or "" for c in creators]
    acfg = cfg.get("author") or {}

    if len(creators) == 0:
        errors.append("sin creators")
    if len(creators) > int(acfg.get("max_creators", 1)):
        errors.append(f"demasiados creators ({len(creators)})")

    accepted = set(acfg.get("name_accepted") or [acfg.get("name")])
    forbidden = acfg.get("name_forbidden_substrings") or []
    for n in names:
        if any(s and s in n for s in forbidden):
            errors.append(f"creator institucional: {n[:80]}")
        elif n not in accepted and n != acfg.get("name"):
            warns.append(f"nombre no canónico: {n}")

    must = acfg.get("affiliation_must_contain") or []
    ban = acfg.get("affiliation_forbidden") or []
    for a in affs:
        if must and not any(m in a for m in must):
            warns.append(f"afiliación sin El Prat: {a[:80] or '(vacía)'}")
        for b in ban:
            if b and b in a:
                errors.append(f"afiliación prohibida: {a[:80]}")

    title = meta.get("title") or ""
    spec = (pack or {}).get("records", {}).get(str(record_id))
    if cfg.get("compare_titles_with_pack") and spec:
        if title != spec.get("title"):
            warns.append(f"título ≠ ficha: {title[:70]}")

    lic = license_id(meta)
    allowed = cfg.get("license_by_record", {}).get(str(record_id)) or cfg.get("license_allowed") or []
    if lic not in allowed:
        errors.append(f"licencia no permitida: {lic}")

    desc = meta.get("description") or ""
    vmin = int(cfg.get("description_min_chars") or 0)
    if len(desc.strip()) < vmin:
        errors.append(f"descripción corta ({len(desc)} < {vmin})")

    if cfg.get("require_related_identifiers") and not (meta.get("related_identifiers") or []):
        warns.append("related_identifiers vacío")

    lang = meta.get("language")
    want_lang = cfg.get("require_language")
    if want_lang and lang != want_lang:
        warns.append(f"idioma {lang!r} ≠ {want_lang!r}")

    if cfg.get("require_open_access") and meta.get("access_right") not in (None, "open"):
        errors.append(f"access_right={meta.get('access_right')}")

    forbidden_fn = set(cfg.get("forbidden_filenames") or [])
    sizes: list[int] = []
    total = 0
    for f in files:
        key = f.get("key") or ""
        size = int(f.get("size") or 0)
        sizes.append(size)
        total += size
        if key in forbidden_fn:
            warns.append(f"fichero a versionar: {key}")
    if cfg.get("warn_duplicate_file_sizes"):
        for sz, n in Counter(sizes).items():
            if sz > 10_000 and n > 1:
                warns.append(f"posible duplicado ({n} ficheros de {sz} bytes)")
    max_mb = float(cfg.get("max_file_mb_warn") or 0)
    if max_mb:
        for f in files:
            mb = (f.get("size") or 0) / 1e6
            if mb > max_mb:
                warns.append(f"fichero grande {mb:.1f} MB: {f.get('key')}")

    return {
        "id": record_id,
        "doi": rec.get("doi") or f"10.5281/zenodo.{record_id}",
        "title": title,
        "creators": names,
        "license": lic,
        "files": len(files),
        "mb": round(total / 1e6, 2),
        "errors": errors,
        "warnings": warns,
        "ok": not errors,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default=str(HERE / "zenodo_validate_config.json"))
    p.add_argument("--json-out")
    p.add_argument("--fail-on", choices=["never", "error", "warning"], default="never")
    args = p.parse_args()

    cfg = load_json(Path(args.config))
    pack = None
    pack_path = HERE / cfg.get("pack_path", "zenodo_metadata.json")
    if pack_path.exists():
        pack = load_json(pack_path)

    results = [check_record(int(i), cfg, pack) for i in cfg["records"]]
    n_err = sum(1 for r in results if r["errors"])
    n_warn = sum(1 for r in results if r["warnings"])

    print(f"{'DOI':<10} {'E':<3} {'W':<3} {'OK':<4} problemas")
    print("-" * 78)
    for r in results:
        problems = "; ".join(r["errors"] + [f"warn:{w}" for w in r["warnings"]])
        print(f"{r['id']}  {len(r['errors']):<3} {len(r['warnings']):<3} {'YES' if r['ok'] else 'NO':<4} {problems[:90]}")
    print("-" * 78)
    print(f"records {len(results)} | con errores {n_err} | con avisos {n_warn} | limpios {sum(1 for r in results if r['ok'] and not r['warnings'])}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print("escrito", args.json_out)

    if args.fail_on == "error" and n_err:
        return 1
    if args.fail_on == "warning" and (n_err or n_warn):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
