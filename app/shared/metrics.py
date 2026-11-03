#!/usr/bin/env python3
"""
Contador de visitas por aplicación — módulo compartido AGs-Core.

Un único fichero JSON maestro, clave por app. Cada app solo cuenta y
muestra SUS visitas y usuarios únicos; no se presenta un total global.

Privacidad: el identificador de visitante se guarda como hash con sal
(no IP en claro, no datos personales).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España,
con asistencia de inteligencia artificial.
Licencia: MIT.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

# ---------------------------------------------------------------------------
# Rutas estables (fuera del data/ gitignore del repo; compartidas en el box)
# ---------------------------------------------------------------------------
_DEFAULT_DIR = Path(os.environ.get("AGS_METRICS_DIR", "/workspace/agsgpt/data"))
MASTER_METRICS_FILE = Path(
    os.environ.get("AGS_MASTER_METRICS_FILE", str(_DEFAULT_DIR / "master_metrics.json"))
)
LOCK_FILE = Path(
    os.environ.get("AGS_METRICS_LOCK_FILE", str(_DEFAULT_DIR / "master_metrics.lock"))
)
SALT_FILE = Path(
    os.environ.get("AGS_METRICS_SALT_FILE", str(_DEFAULT_DIR / "metrics_salt"))
)

# Tope de hashes almacenados por app (evita crecimiento ilimitado).
# Al llegar al tope se siguen contando visitas; los únicos dejan de crecer
# (subconteo conservador documentado).
MAX_HASHES_PER_APP = int(os.environ.get("AGS_METRICS_MAX_HASHES", "50000"))

_EMPTY: Dict[str, Any] = {"apps": {}}


# ---------------------------------------------------------------------------
# Candado: filelock si está instalado; si no, fcntl (Linux)
# ---------------------------------------------------------------------------
@contextmanager
def _file_lock(lock_path: Path, timeout: float = 5.0) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from filelock import FileLock, Timeout  # type: ignore

        lock = FileLock(str(lock_path), timeout=timeout)
        try:
            with lock:
                yield
        except Timeout as exc:  # pragma: no cover
            raise TimeoutError(f"timeout al adquirir {lock_path}") from exc
        return
    except ImportError:
        pass

    import fcntl
    import time

    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o600)
    deadline = time.monotonic() + timeout
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    os.close(fd)
                    raise TimeoutError(f"timeout al adquirir {lock_path}")
                time.sleep(0.05)
        try:
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def _ensure_salt() -> bytes:
    """Sal persistente para hashes anónimos. Se crea una sola vez."""
    SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not SALT_FILE.exists():
        raw = secrets.token_hex(16)
        tmp = SALT_FILE.with_suffix(".tmp")
        tmp.write_text(raw, encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, SALT_FILE)
    return SALT_FILE.read_text(encoding="utf-8").strip().encode("utf-8")


def make_user_hash(raw_id: str) -> str:
    """Hash con sal de un identificador opaco (p. ej. id de sesión Streamlit).

    No acepta ni almacena IP en claro: el llamador debe pasar ya un token
    opaco o el id de sesión, nunca datos personales.
    """
    if not raw_id or not str(raw_id).strip():
        raise ValueError("raw_id vacío: no se puede hashear")
    digest = hashlib.sha256(_ensure_salt() + b"|" + str(raw_id).encode("utf-8"))
    return digest.hexdigest()[:32]


def _atomic_write(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=".metrics_", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _load_unlocked(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"apps": {}}
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {"apps": {}}
    if not isinstance(data, dict):
        return {"apps": {}}
    data.setdefault("apps", {})
    if not isinstance(data["apps"], dict):
        data["apps"] = {}
    return data


def _app_bucket(metrics: Dict[str, Any], app_name: str) -> Dict[str, Any]:
    apps = metrics.setdefault("apps", {})
    if app_name not in apps or not isinstance(apps[app_name], dict):
        apps[app_name] = {
            "total_visits": 0,
            "unique_users": 0,
            "hashes": [],
            "cities": {},
        }
    bucket = apps[app_name]
    bucket.setdefault("total_visits", 0)
    bucket.setdefault("unique_users", 0)
    bucket.setdefault("hashes", [])
    bucket.setdefault("cities", {})
    return bucket


def update_metrics(
    app_name: str,
    city: str = "desconocida",
    user_hash: str = "",
) -> int:
    """Incrementa el contador de ESTA app y devuelve sus visitas totales.

    No actualiza ni expone totales globales. ``city`` es opcional
    (por defecto ``desconocida``). ``user_hash`` debe ser ya un hash
    salado (usar ``make_user_hash``).
    """
    if not app_name or not str(app_name).strip():
        raise ValueError("app_name vacío")
    app_name = str(app_name).strip()
    city = (city or "desconocida").strip() or "desconocida"
    if not user_hash or not str(user_hash).strip():
        raise ValueError("user_hash vacío: usa make_user_hash(...)")
    user_hash = str(user_hash).strip()

    with _file_lock(LOCK_FILE):
        metrics = _load_unlocked(MASTER_METRICS_FILE)
        bucket = _app_bucket(metrics, app_name)

        bucket["total_visits"] = int(bucket["total_visits"]) + 1

        hashes = bucket.get("hashes") or []
        if not isinstance(hashes, list):
            hashes = []
        if user_hash not in hashes:
            if len(hashes) < MAX_HASHES_PER_APP:
                hashes.append(user_hash)
                bucket["hashes"] = hashes
                bucket["unique_users"] = int(bucket.get("unique_users", 0)) + 1
            # si estamos al tope: no añadimos hash ni inflamos únicos
        else:
            bucket["hashes"] = hashes

        cities = bucket.setdefault("cities", {})
        if not isinstance(cities, dict):
            cities = {}
            bucket["cities"] = cities
        cities[city] = int(cities.get(city, 0)) + 1

        # No persistir claves globales heredadas del borrador original.
        metrics.pop("total_visits_global", None)
        metrics.pop("global_hashes", None)
        metrics.pop("cities", None)

        _atomic_write(MASTER_METRICS_FILE, metrics)
        return int(bucket["total_visits"])


def get_app_metrics(app_name: str) -> Dict[str, Any]:
    """Lee solo las métricas de ``app_name`` (sin totales de otras apps)."""
    if not app_name:
        return {"total_visits": 0, "unique_users": 0, "cities": {}}
    with _file_lock(LOCK_FILE):
        metrics = _load_unlocked(MASTER_METRICS_FILE)
        bucket = metrics.get("apps", {}).get(app_name) or {}
        return {
            "total_visits": int(bucket.get("total_visits", 0) or 0),
            "unique_users": int(bucket.get("unique_users", 0) or 0),
            "cities": dict(bucket.get("cities") or {}),
        }



def _format_es(n: int) -> str:
    """Entero con separador de miles estilo español (1.234)."""
    return f"{int(n):,}".replace(",", ".")


def render_visit_badge(app_name: str) -> None:
    """Badge compacto y siempre visible con las visitas de ESTA app.

    Ejemplo visual: ``👀 1.234 visitas``. Pensado para sidebar o cabecera.
    No muestra totales globales ni otras apps.
    """
    try:
        import streamlit as st
    except ImportError as exc:  # pragma: no cover
        raise ImportError("streamlit es necesario para render_visit_badge") from exc

    data = get_app_metrics(app_name)
    total = int(data["total_visits"])
    unicos = int(data["unique_users"])
    st.markdown(
        f"""
        <div style="display:inline-block; background:#1E1E1E; color:#E8F5E9;
                    border:1px solid #4CAF50; border-radius:999px; padding:6px 14px;
                    font-size:0.95rem; font-weight:600; margin:4px 0 12px 0;">
            👀 {_format_es(total)} visitas
            <span style="color:#9E9E9E; font-weight:400; font-size:0.85rem;">
                · {_format_es(unicos)} únicos
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_app_metrics(app_name: str) -> None:
    """Muestra en Streamlit SOLO las visitas de esta app (sin total global)."""
    try:
        import streamlit as st
    except ImportError as exc:  # pragma: no cover
        raise ImportError("streamlit es necesario para render_app_metrics") from exc

    data = get_app_metrics(app_name)
    total = data["total_visits"]
    unicos = data["unique_users"]
    label = app_name.replace("_", " ").title()

    st.markdown(
        f"""
        <div style="background-color: #1E1E1E; padding: 16px; border-radius: 10px;
                    border: 1px solid #4CAF50; text-align: center; margin-bottom: 12px;">
            <h2 style="color: #4CAF50; margin: 0; font-size: 2rem;">{total:,}</h2>
            <p style="color: #FFFFFF; margin: 0; font-size: 1.05rem;">
                👀 Visitas de {label}
            </p>
            <p style="color: #AAAAAA; margin: 0; font-size: 0.9rem;">
                Usuarios únicos: {unicos:,}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def track_streamlit_visit(
    app_name: str,
    city: str = "desconocida",
) -> int:
    """Cuenta una visita por sesión Streamlit (no en cada rerun).

    Devuelve el total de visitas de esta app tras el (posible) incremento.
    No cuenta bajo pytest ni si ``AGS_METRICS_DISABLE=1`` (evita inflar el JSON
    en tests / AppTest).
    """
    if os.environ.get("AGS_METRICS_DISABLE") == "1" or os.environ.get("PYTEST_CURRENT_TEST"):
        return get_app_metrics(app_name)["total_visits"]
    try:
        import streamlit as st
    except ImportError as exc:  # pragma: no cover
        raise ImportError("streamlit es necesario para track_streamlit_visit") from exc

    flag = f"_metrics_counted_{app_name}"
    if st.session_state.get(flag):
        return get_app_metrics(app_name)["total_visits"]

    if "_metrics_visitor_id" not in st.session_state:
        st.session_state["_metrics_visitor_id"] = secrets.token_hex(16)

    user_hash = make_user_hash(st.session_state["_metrics_visitor_id"])
    total = update_metrics(app_name, city=city, user_hash=user_hash)
    st.session_state[flag] = True
    return total


# Alias de compatibilidad: el borrador original llamaba render_master_metrics
# mostrando un total global. Ahora delega al render por app y exige app_name.
def render_master_metrics(app_name: str) -> None:
    """Deprecated alias → ``render_app_metrics(app_name)`` (solo esta app)."""
    render_app_metrics(app_name)


__all__ = [
    "MASTER_METRICS_FILE",
    "LOCK_FILE",
    "SALT_FILE",
    "MAX_HASHES_PER_APP",
    "make_user_hash",
    "update_metrics",
    "get_app_metrics",
    "render_app_metrics",
    "render_visit_badge",
    "render_master_metrics",
    "track_streamlit_visit",
]
