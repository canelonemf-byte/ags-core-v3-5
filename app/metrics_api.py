"""Endpoints públicos de visitas por app (badge SVG + contador HTTP).

Sin autenticación: solo incrementan/leen contadores por nombre de app.
No aceptan ni almacenan datos personales (el visitor_id se hashea con sal).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España,
con asistencia de inteligencia artificial.
Licencia: MIT.
"""
from __future__ import annotations

import re
import secrets
from typing import Any, Optional

from fastapi import APIRouter, Cookie, Header, Query, Request, Response
from fastapi.responses import JSONResponse, Response as PlainResponse

from shared.metrics import get_app_metrics, svg_badge, track_http_visit

router = APIRouter(tags=["metrics"])

_APP_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_\-]{0,63}$")
_COOKIE = "ags_vid"


def _valid_app(name: str) -> str:
    name = (name or "").strip()
    if name.endswith(".svg"):
        name = name[: -len(".svg")]
    if not _APP_RE.match(name):
        raise ValueError("app_name inválido")
    return name


def _cors_headers(origin: Optional[str]) -> dict:
    allow = (
        origin
        if origin
        and (
            origin.startswith("http://127.0.0.1")
            or origin.startswith("http://localhost")
            or origin.startswith("http://0.0.0.0")
        )
        else "*"
    )
    return {
        "Access-Control-Allow-Origin": allow,
        "Access-Control-Allow-Credentials": "true" if allow != "*" else "false",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Visitor-Id",
        "Access-Control-Max-Age": "86400",
        "Vary": "Origin",
    }


async def _read_json(request: Request) -> dict[str, Any]:
    if request.method not in ("POST", "PUT", "PATCH"):
        return {}
    ctype = (request.headers.get("content-type") or "").lower()
    if "application/json" not in ctype:
        return {}
    try:
        data = await request.json()
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


@router.options("/metrics/visit/{app_name}")
@router.options("/metrics/{app_name}")
@router.options("/metrics/badge/{app_name}")
async def metrics_options(app_name: str, request: Request):
    return Response(status_code=204, headers=_cors_headers(request.headers.get("origin")))


@router.get("/metrics/{app_name}")
async def metrics_get(app_name: str, request: Request):
    try:
        name = _valid_app(app_name)
    except ValueError:
        return JSONResponse(
            {"error": "app_name inválido"},
            status_code=400,
            headers=_cors_headers(request.headers.get("origin")),
        )
    data = get_app_metrics(name)
    return JSONResponse(
        {"app": name, **data},
        headers=_cors_headers(request.headers.get("origin")),
    )


@router.api_route("/metrics/visit/{app_name}", methods=["GET", "POST"], name="metrics_visit")
async def metrics_visit(
    app_name: str,
    request: Request,
    city: str = Query(default="desconocida", max_length=64),
    visitor_id: Optional[str] = Query(default=None, max_length=128),
    x_visitor_id: Optional[str] = Header(default=None, alias="X-Visitor-Id"),
    ags_vid: Optional[str] = Cookie(default=None),
):
    try:
        name = _valid_app(app_name)
    except ValueError:
        return JSONResponse(
            {"error": "app_name inválido"},
            status_code=400,
            headers=_cors_headers(request.headers.get("origin")),
        )

    payload = await _read_json(request)
    if isinstance(payload.get("city"), str) and payload["city"].strip():
        city = payload["city"].strip()[:64]
    body_vid = payload.get("visitor_id")
    if isinstance(body_vid, str):
        body_vid = body_vid.strip()[:128]
    else:
        body_vid = ""

    vid = (
        body_vid
        or (visitor_id or "").strip()
        or (x_visitor_id or "").strip()
        or (ags_vid or "").strip()
    )
    set_cookie = False
    if not vid:
        vid = secrets.token_hex(16)
        set_cookie = True

    result = track_http_visit(name, visitor_id=vid, city=city or "desconocida")
    resp = JSONResponse(result, headers=_cors_headers(request.headers.get("origin")))
    if set_cookie:
        resp.set_cookie(
            key=_COOKIE,
            value=vid,
            max_age=60 * 60 * 24 * 365,
            httponly=True,
            samesite="lax",
            path="/",
        )
    return resp


@router.get("/metrics/badge/{app_name}")
async def metrics_badge(
    app_name: str, request: Request, label: Optional[str] = None
):
    try:
        name = _valid_app(app_name)
    except ValueError:
        return JSONResponse(
            {"error": "app_name inválido"},
            status_code=400,
            headers=_cors_headers(request.headers.get("origin")),
        )
    svg = svg_badge(name, label=label)
    headers = {
        **_cors_headers(request.headers.get("origin")),
        "Content-Type": "image/svg+xml; charset=utf-8",
        "Cache-Control": "no-cache, max-age=0",
    }
    return PlainResponse(content=svg, media_type="image/svg+xml", headers=headers)
