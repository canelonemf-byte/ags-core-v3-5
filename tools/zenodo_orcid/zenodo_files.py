#!/usr/bin/env python3
"""
Gestión programática de ficheros en Zenodo.

Regla dura de Zenodo:
  - Publicado: NO se pueden añadir/borrar/renombrar ficheros.
  - Hay que crear versión nueva → subir/borrar en el draft → publicar.
  - Metadatos de un publicado SÍ se pueden PUT sin nueva versión.

Scopes del token:
  deposit:write     listar, subir, borrar (draft)
  deposit:actions   newversion, publish, edit, discard

  export ZENODO_TOKEN='...'
  python3 zenodo_files.py list 22131030
  python3 zenodo_files.py download 22131030
  python3 zenodo_files.py newversion 22131030
  python3 zenodo_files.py upload DRAFT_ID ./archivo.pdf
  python3 zenodo_files.py delete DRAFT_ID FILE_ID
  python3 zenodo_files.py publish DRAFT_ID
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


def token() -> str:
    t = os.environ.get("ZENODO_TOKEN", "").strip()
    if not t:
        sys.exit(
            "Falta ZENODO_TOKEN\n"
            "https://zenodo.org/account/settings/applications/tokens\n"
            "Scopes: deposit:write y deposit:actions"
        )
    return t


def request(method: str, path: str, body=None, raw: bytes | None = None,
            content_type: str | None = None, auth: bool = True):
    headers = {"Accept": "application/json"}
    if auth:
        headers["Authorization"] = f"Bearer {token()}"
    data = raw
    if body is not None:
        headers["Content-Type"] = content_type or "application/json"
        data = json.dumps(body).encode("utf-8")
    elif raw is not None and content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            payload = resp.read()
            if not payload:
                return {"status": resp.status}
            try:
                return json.loads(payload.decode("utf-8"))
            except json.JSONDecodeError:
                return {"raw": payload[:200]}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        sys.exit(f"HTTP {e.code} {method} {path}\n{err[:2500]}")


def public_record(record_id: int) -> dict:
    url = f"https://zenodo.org/api/records/{record_id}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def deposition(dep_id: int) -> dict:
    return request("GET", f"/deposit/depositions/{dep_id}")


def cmd_list(args: argparse.Namespace) -> None:
    rec = public_record(args.id)
    md = rec.get("metadata") or {}
    print("DOI  :", rec.get("doi"))
    print("title:", md.get("title"))
    print("state: published (público)")
    print("files:")
    for f in rec.get("files") or []:
        key = f.get("key") or f.get("filename")
        size = f.get("size") or 0
        print(f"  {size:12}  {key}")
        if args.urls:
            links = f.get("links") or {}
            print(f"              {links.get('self') or links.get('download')}")


def cmd_download(args: argparse.Namespace) -> None:
    rec = public_record(args.id)
    out = Path(args.out or f"zenodo_{args.id}")
    out.mkdir(parents=True, exist_ok=True)
    for f in rec.get("files") or []:
        key = f.get("key") or f.get("filename") or "file.bin"
        links = f.get("links") or {}
        url = links.get("self") or links.get("download")
        if not url:
            print("SKIP sin URL", key)
            continue
        dest = out / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        print("GET", key)
        with urllib.request.urlopen(url, timeout=300) as resp, dest.open("wb") as fh:
            while True:
                chunk = resp.read(1024 * 256)
                if not chunk:
                    break
                fh.write(chunk)
        print("  ->", dest)


def cmd_files_auth(args: argparse.Namespace) -> None:
    files = request("GET", f"/deposit/depositions/{args.id}/files")
    if not isinstance(files, list):
        print(files)
        return
    for f in files:
        print(f"{f.get('id')}\t{f.get('filesize') or f.get('size')}\t{f.get('filename') or f.get('name')}")


def cmd_newversion(args: argparse.Namespace) -> None:
    dep = request("POST", f"/deposit/depositions/{args.id}/actions/newversion")
    links = dep.get("links") or {}
    draft = links.get("latest_draft")
    print("newversion OK")
    print("latest_draft:", draft)
    print("Usa el ID numérico del draft en upload/delete/publish.")
    if draft:
        draft_id = draft.rstrip("/").split("/")[-1]
        print("DRAFT_ID=", draft_id)


def cmd_upload(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.is_file():
        sys.exit(f"No existe {path}")
    dep = deposition(args.id)
    state = (dep.get("metadata") or {}).get("prereserve_doi")
    submitted = dep.get("submitted")
    if submitted and dep.get("state") == "done":
        sys.exit(
            "Este depósito está publicado. "
            "Ejecuta antes: python3 zenodo_files.py newversion ID"
        )
    bucket = (dep.get("links") or {}).get("bucket")
    if not bucket:
        sys.exit("Sin links.bucket; ¿id incorrecto?")
    name = args.name or path.name
    dest = bucket.rstrip("/") + "/" + urllib.parse.quote(name)
    data = path.read_bytes()
    headers = {
        "Authorization": f"Bearer {token()}",
        "Content-Type": "application/octet-stream",
        "Accept": "application/json",
    }
    req = urllib.request.Request(dest, data=data, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            out = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} PUT bucket\n{e.read().decode('utf-8','replace')[:2000]}")
    print("uploaded:", out.get("key") or name, "id=", out.get("id"))


def cmd_delete(args: argparse.Namespace) -> None:
    request("DELETE", f"/deposit/depositions/{args.id}/files/{args.file_id}")
    print("deleted", args.file_id)


def cmd_rename(args: argparse.Namespace) -> None:
    out = request(
        "PUT",
        f"/deposit/depositions/{args.id}/files/{args.file_id}",
        {"filename": args.name, "name": args.name},
    )
    print("renamed:", out.get("filename") or out.get("name"))


def cmd_publish(args: argparse.Namespace) -> None:
    out = request("POST", f"/deposit/depositions/{args.id}/actions/publish")
    md = out.get("metadata") or {}
    print("published:", out.get("doi") or md.get("doi"))
    print("record_id:", out.get("record_id") or out.get("id"))


def cmd_discard(args: argparse.Namespace) -> None:
    request("POST", f"/deposit/depositions/{args.id}/actions/discard")
    print("discarded draft edits")


def main() -> None:
    p = argparse.ArgumentParser(description="Zenodo file manager")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="ficheros públicos (sin token)")
    s.add_argument("id", type=int)
    s.add_argument("--urls", action="store_true")

    s = sub.add_parser("download", help="descarga pública")
    s.add_argument("id", type=int)
    s.add_argument("--out")

    s = sub.add_parser("auth-list", help="ficheros del depósito (token)")
    s.add_argument("id", type=int)

    s = sub.add_parser("newversion", help="draft a partir de un publicado")
    s.add_argument("id", type=int)

    s = sub.add_parser("upload", help="sube a un DRAFT (bucket PUT)")
    s.add_argument("id", type=int)
    s.add_argument("file")
    s.add_argument("--name")

    s = sub.add_parser("delete", help="borra fichero de un DRAFT")
    s.add_argument("id", type=int)
    s.add_argument("file_id")

    s = sub.add_parser("rename", help="renombra en un DRAFT")
    s.add_argument("id", type=int)
    s.add_argument("file_id")
    s.add_argument("name")

    s = sub.add_parser("publish", help="publica un DRAFT (DOI versión nueva)")
    s.add_argument("id", type=int)

    s = sub.add_parser("discard", help="descarta edición")
    s.add_argument("id", type=int)

    args = p.parse_args()
    {
        "list": cmd_list,
        "download": cmd_download,
        "auth-list": cmd_files_auth,
        "newversion": cmd_newversion,
        "upload": cmd_upload,
        "delete": cmd_delete,
        "rename": cmd_rename,
        "publish": cmd_publish,
        "discard": cmd_discard,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
