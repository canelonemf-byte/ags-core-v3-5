#!/usr/bin/env python3
"""
Paginación automática para la API REST de Zenodo.

Reglas (2025-11+):
  /api/deposit/depositions     size máx. 100
  /api/records  anónimo        size máx. 25
  /api/records  autenticado    size máx. 100
  búsqueda / OAI               30 req/min

Uso:
  from zenodo_paginate import paginate, fetch_all_depositions
  for dep in fetch_all_depositions(token):
      ...
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator
from typing import Any

DEFAULT_API = "https://zenodo.org/api"

SIZE_DEPOSIT = 100
SIZE_RECORDS_ANON = 25
SIZE_RECORDS_AUTH = 100


class ZenodoHTTPError(RuntimeError):
    def __init__(self, status: int, path: str, body: str):
        super().__init__(f"HTTP {status} {path}\n{body[:2000]}")
        self.status = status
        self.path = path
        self.body = body


def _parse_retry_after(headers: Any) -> float:
    raw = headers.get("Retry-After")
    if raw:
        try:
            return max(1.0, float(raw))
        except ValueError:
            pass
    reset = headers.get("X-RateLimit-Reset")
    if reset:
        try:
            wait = float(reset) - time.time()
            if wait > 0:
                return min(wait, 60.0)
        except ValueError:
            pass
    return 2.0


def request_json(
    method: str,
    url: str,
    token: str | None = None,
    body: dict | None = None,
    timeout: int = 60,
    retries: int = 4,
) -> tuple[Any, dict[str, str]]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    last_err: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8")
                hdrs = {k: v for k, v in resp.headers.items()}
                payload = json.loads(raw) if raw else None
                return payload, hdrs
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 503) and attempt < retries - 1:
                time.sleep(_parse_retry_after(e.headers) * (attempt + 1))
                last_err = e
                continue
            raise ZenodoHTTPError(e.code, url, err_body) from e
        except TimeoutError as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"falló {method} {url}: {last_err}")


def _next_from_link(headers: dict[str, str]) -> str | None:
    link = headers.get("Link") or headers.get("link")
    if not link:
        return None
    for part in link.split(","):
        if 'rel="next"' in part or "rel='next'" in part:
            start = part.find("<")
            end = part.find(">")
            if start >= 0 and end > start:
                return part[start + 1 : end].strip()
    return None


def paginate(
    path: str,
    *,
    api: str = DEFAULT_API,
    token: str | None = None,
    params: dict | None = None,
    size: int | None = None,
    max_pages: int = 200,
    sleep_s: float = 0.0,
) -> Iterator[Any]:
    """
    Recorre page=1..N hasta que una página venga corta o no haya Link: next.

    path: '/deposit/depositions' o '/records'
    Yields cada elemento de la lista (o hits si el cuerpo es {hits: {hits: [...]}}).
    """
    if size is None:
        if path.rstrip("/").endswith("records") and not token:
            size = SIZE_RECORDS_ANON
        elif path.rstrip("/").endswith("records"):
            size = SIZE_RECORDS_AUTH
        else:
            size = SIZE_DEPOSIT

    query = dict(params or {})
    query.setdefault("page", 1)
    query["size"] = size
    url = api.rstrip("/") + path
    if "?" not in url:
        url = url + "?" + urllib.parse.urlencode(query)

    pages = 0
    while url and pages < max_pages:
        payload, headers = request_json("GET", url, token=token)
        pages += 1
        items, page_len, requested = _unwrap_page(payload, size)
        for item in items:
            yield item
        next_url = _next_from_link(headers)
        if next_url:
            url = next_url
        elif page_len < requested:
            break
        else:
            query["page"] = int(query.get("page", 1)) + 1
            url = api.rstrip("/") + path + "?" + urllib.parse.urlencode(query)
        if sleep_s:
            time.sleep(sleep_s)
        remaining = headers.get("X-RateLimit-Remaining")
        if remaining is not None:
            try:
                if int(remaining) <= 2:
                    time.sleep(max(sleep_s, 2.0))
            except ValueError:
                pass


def _unwrap_page(payload: Any, requested: int) -> tuple[list, int, int]:
    if payload is None:
        return [], 0, requested
    if isinstance(payload, list):
        return payload, len(payload), requested
    if isinstance(payload, dict):
        hits = payload.get("hits")
        if isinstance(hits, dict) and isinstance(hits.get("hits"), list):
            inner = hits["hits"]
            return inner, len(inner), requested
        if isinstance(payload.get("results"), list):
            inner = payload["results"]
            return inner, len(inner), requested
        return [payload], 1, requested
    return [], 0, requested


def fetch_all_depositions(
    token: str,
    *,
    api: str = DEFAULT_API,
    status: str | None = None,
) -> list[dict]:
    params = {}
    if status:
        params["status"] = status
    return list(
        paginate(
            "/deposit/depositions",
            api=api,
            token=token,
            params=params,
            size=SIZE_DEPOSIT,
        )
    )


def fetch_records(
    query: str,
    *,
    token: str | None = None,
    api: str = DEFAULT_API,
    all_versions: bool = False,
) -> list[dict]:
    params = {"q": query}
    if all_versions:
        params["all_versions"] = "true"
    return list(
        paginate(
            "/records",
            api=api,
            token=token,
            params=params,
        )
    )


if __name__ == "__main__":
    import os
    import sys

    q = sys.argv[1] if len(sys.argv) > 1 else 'creators.name:"López Paz"'
    print("GET /api/records q=", q, "anónimo size=25")
    n = 0
    for rec in paginate("/records", params={"q": q}):
        n += 1
        md = rec.get("metadata") or rec
        title = (md.get("title") if isinstance(md, dict) else "") or rec.get("id")
        print(f"  {rec.get('id')}\t{str(title)[:70]}")
        if n >= 15:
            break
    print("páginas recorridas vía paginate(); cortado a 15 hits de muestra")
