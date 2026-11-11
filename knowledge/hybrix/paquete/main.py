import os
import json
import logging
import secrets
import threading
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, field_validator

# Capa L5 (meta-gobernanza): bus de feromonas + GeminiMetaAgent. Si faltan los módulos, la API sigue igual.
try:
    from hybrix_phero_bus import PheromoneBus
    from gemini_meta_agent import GeminiMetaAgent
    L5_DISPONIBLE = True
except ImportError:  # pragma: no cover
    PheromoneBus = None  # type: ignore
    GeminiMetaAgent = None  # type: ignore
    L5_DISPONIBLE = False

def _default_db_path() -> Path:
    """Estado persistente FUERA del directorio de trabajo (antes: ./hybrix_api_state.json en el cwd).
    Prioridad: HYBRIX_DB_PATH > HYBRIX_DATA_DIR > $XDG_DATA_HOME/hybrix > ~/.local/share/hybrix."""
    if os.getenv("HYBRIX_DB_PATH"):
        return Path(os.environ["HYBRIX_DB_PATH"])
    base = os.getenv("HYBRIX_DATA_DIR") or os.path.join(
        os.getenv("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share"), "hybrix")
    return Path(base) / "hybrix_api_state.json"


API_KEY = os.getenv("HYBRIX_API_KEY", "")
DB_PATH = _default_db_path()
PROJECTS_PATH = Path(os.getenv("HYBRIX_PROJECTS_PATH", "projects.json"))
MAX_RECORDS = int(os.getenv("HYBRIX_MAX_RECORDS", "100000"))
MAX_PAGE_SIZE = 1000
_lock = threading.RLock()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}
logger = logging.getLogger("hybrix")
logging.basicConfig(level=logging.INFO)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_api_key(request: Request, key: Optional[str] = Security(api_key_header)) -> None:
    if not API_KEY:
        client_host = request.client.host if request.client else ""
        if client_host not in LOCAL_HOSTS:
            raise HTTPException(status_code=403, detail="Acceso restringido a localhost cuando no hay HYBRIX_API_KEY")
        return
    if not key or not secrets.compare_digest(key, API_KEY):
        raise HTTPException(status_code=401, detail="API key invalida o ausente")


def require_read_access(request: Request, key: Optional[str] = Security(api_key_header)) -> None:
    if API_KEY and (not key or not secrets.compare_digest(key, API_KEY)):
        raise HTTPException(status_code=401, detail="API key invalida o ausente para lectura")


class TelemetryData(BaseModel):
    trial_id: int = Field(..., ge=0)
    node_id: str = Field(..., min_length=1, max_length=64)
    timestamp: Optional[str] = None
    viability: float = Field(..., ge=0.0, le=1.0)
    active_electrodes: int = Field(..., ge=0, le=32)

    @field_validator("timestamp")
    @classmethod
    def check_iso(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp debe estar en formato ISO 8601")
        return v


class TelemetryBatch(BaseModel):
    items: List[TelemetryData] = Field(..., min_length=1, max_length=500)


class PredictionData(BaseModel):
    trial_id: int = Field(..., ge=0)
    node_id: str = Field(..., min_length=1, max_length=64)
    timestamp: Optional[str] = None
    label: int = Field(..., ge=0, le=1)
    prediction: int = Field(..., ge=0, le=1)
    probability: float = Field(..., ge=0.0, le=1.0)

    @field_validator("timestamp")
    @classmethod
    def check_iso(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("timestamp debe estar en formato ISO 8601")
        return v


class PredictionBatch(BaseModel):
    items: List[PredictionData] = Field(..., min_length=1, max_length=500)


def _guardar_estado(db: Dict[str, Any]) -> None:
    tmp = DB_PATH.with_suffix(".tmp")
    try:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps({"telemetry": db["telemetry"], "predictions": db["predictions"]}), encoding="utf-8")
        tmp.replace(DB_PATH)
    except OSError:
        logger.exception("Error al guardar estado en %s", DB_PATH)


L5_ENABLED = os.getenv("HYBRIX_L5_ENABLED", "1") not in ("0", "false", "no")
L5_INTERVAL = int(os.getenv("HYBRIX_L5_INTERVAL", "50"))


def _init_l5(app: FastAPI) -> None:
    """Crea el bus de feromonas y el GeminiMetaAgent (modelo: GEMINI_MODEL o gemini-3.5-flash).
    Sin GEMINI_API_KEY el agente queda en estado 'pending' y no llama a la red."""
    app.state.phero = None
    app.state.l5 = None
    if not (L5_ENABLED and L5_DISPONIBLE):
        return
    app.state.phero = PheromoneBus()
    app.state.l5 = GeminiMetaAgent(app.state.phero, None, analysis_interval=L5_INTERVAL)


def _l5_feed(records: List[Dict[str, Any]]) -> None:
    """Deposita cada predicción como feromona 'prediccion_final' y avanza un ciclo del agente L5.
    Se ejecuta en segundo plano (BackgroundTasks) para no retrasar la respuesta HTTP."""
    agent = getattr(app.state, "l5", None)
    bus = getattr(app.state, "phero", None)
    if agent is None or bus is None:
        return
    for r in records:
        try:
            bus.deposit("prediccion_final", r, ttl_s=300)
            agent.step()
        except Exception:  # el L5 nunca debe tumbar la API
            logger.exception("[L5] fallo al procesar la predicción trial_id=%s", r.get("trial_id"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = {"projects_meta": {}, "telemetry": [], "predictions": []}
    _init_l5(app)
    if PROJECTS_PATH.exists():
        try:
            app.state.db["projects_meta"] = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            app.state.db["projects_meta"] = {}
    if DB_PATH.exists():
        try:
            persisted = json.loads(DB_PATH.read_text(encoding="utf-8"))
            if not isinstance(persisted, dict):
                raise ValueError("estructura inesperada")
            app.state.db["telemetry"] = persisted.get("telemetry", [])
            app.state.db["predictions"] = persisted.get("predictions", [])
        except (OSError, ValueError):
            corrupto = DB_PATH.with_name(f"{DB_PATH.name}.corrupto-{int(time.time())}")
            DB_PATH.rename(corrupto)
            logger.error("Estado ilegible movido a %s; se arranca con base vacia", corrupto)
    yield
    try:
        _guardar_estado(app.state.db)
    except OSError:
        logger.exception("No se pudo guardar el estado en %s", DB_PATH)


app = FastAPI(title="HYBRIX Orquestacion API", version="1.9.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("HYBRIX_CORS_ORIGINS", "http://127.0.0.1:5500,http://localhost:5500").split(","),
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)


def _trigger_auto_export(trial_id: int, viability: float):
    auto_dir = Path("/workspace/scratch/auto_exports")
    auto_dir.mkdir(parents=True, exist_ok=True)
    filename = f"critical_export_trial_{trial_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    target_path = auto_dir / filename
    lines = ["trial_id,telemetry_node_id,telemetry_timestamp,telemetry_received_at,viability,active_electrodes,prediction_node_id,prediction_timestamp,prediction_received_at,label,prediction,probability"]
    for item in app.state.db["telemetry"]:
        lines.append(f"{item['trial_id']},{item['node_id']},{item.get('timestamp','')},{item.get('received_at','')},{item['viability']},{item['active_electrodes']},,,,,,")
    target_path.write_text("\n".join(lines), encoding="utf-8")
    logger.warning("[AUTO-EXPORT] Exportacion preventiva generada en %s tras alerta de viabilidad (%f)", target_path, viability)
    return str(target_path)


def _append(collection: List[Dict[str, Any]], item: Dict[str, Any]) -> None:
    collection.append(item)
    excess = len(collection) - MAX_RECORDS
    if excess > 0:
        del collection[:excess]
        logger.warning("Límite MAX_RECORDS (%d) alcanzado. Se han purgado los %d registros más antiguos.", MAX_RECORDS, excess)


@app.get("/api/v1/hybrix/status")
def get_status() -> Dict[str, Any]:
    with _lock:
        return {
            "status": "online",
            "timestamp": utc_now(),
            "metadata": app.state.db["projects_meta"],
            "records_telemetry": len(app.state.db["telemetry"]),
            "records_predictions": len(app.state.db["predictions"]),
        }


@app.post("/api/v1/hybrix/telemetry", status_code=201, dependencies=[Depends(require_api_key)])
def post_telemetry(data: TelemetryData) -> Dict[str, Any]:
    record = data.model_dump()
    record["timestamp"] = record["timestamp"] or utc_now()
    record["received_at"] = utc_now()
    alert_info = None
    with _lock:
        _append(app.state.db["telemetry"], record)
        _guardar_estado(app.state.db)
        if record["viability"] < 0.70:
            logger.error("[ALERTA BIOLOGICA CRITICA] Viabilidad baja (%.2f) detectada en ensayo trial_id=%d. Umbral seguro >= 0.70", record["viability"], record["trial_id"])
            exported_file = _trigger_auto_export(record["trial_id"], record["viability"])
            alert_info = {
                "alert": "CRITICAL_LOW_VIABILITY",
                "message": f"Alerta: Viabilidad ({record['viability']:.2f}) inferior al umbral critico del 70%.",
                "auto_export_file": exported_file
            }
    res = {"status": "success", "inserted": 1}
    if alert_info:
        res.update(alert_info)
    return res


@app.post("/api/v1/hybrix/telemetry/batch", status_code=201, dependencies=[Depends(require_api_key)])
def post_telemetry_batch(batch: TelemetryBatch) -> Dict[str, Any]:
    now = utc_now()
    records = []
    for item in batch.items:
        record = item.model_dump()
        record["timestamp"] = record["timestamp"] or now
        record["received_at"] = now
        records.append(record)
    with _lock:
        for record in records:
            _append(app.state.db["telemetry"], record)
        _guardar_estado(app.state.db)
    return {"status": "success", "inserted": len(records)}


@app.post("/api/v1/hybrix/predictions", status_code=201, dependencies=[Depends(require_api_key)])
def post_prediction(data: PredictionData, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    record = data.model_dump()
    record["timestamp"] = record["timestamp"] or utc_now()
    record["received_at"] = utc_now()
    with _lock:
        _append(app.state.db["predictions"], record)
        _guardar_estado(app.state.db)
    background_tasks.add_task(_l5_feed, [dict(record)])
    return {"status": "success", "inserted": 1}


@app.post("/api/v1/hybrix/predictions/batch", status_code=201, dependencies=[Depends(require_api_key)])
def post_prediction_batch(batch: PredictionBatch, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    now = utc_now()
    records = []
    for item in batch.items:
        record = item.model_dump()
        record["timestamp"] = record["timestamp"] or now
        record["received_at"] = now
        records.append(record)
    with _lock:
        for record in records:
            _append(app.state.db["predictions"], record)
        _guardar_estado(app.state.db)
    background_tasks.add_task(_l5_feed, [dict(r) for r in records])
    return {"status": "success", "inserted": len(records)}


@app.get("/api/v1/hybrix/l5/status", dependencies=[Depends(require_read_access)])
def get_l5_status() -> Dict[str, Any]:
    """Estado de la capa L5 (GeminiMetaAgent). No expone claves."""
    agent = getattr(app.state, "l5", None)
    bus = getattr(app.state, "phero", None)
    if agent is None:
        return {"enabled": False, "status": "disabled" if not L5_ENABLED else "unavailable"}
    return {
        "enabled": True,
        "status": agent.status,
        "model": agent.model_name,
        "cycle_count": agent.cycle_count,
        "analysis_interval": agent.analysis_interval,
        "buffer": len(agent.history_buffer),
        "buffer_max": agent.history_buffer.maxlen,
        "last_error": agent.last_error,
        "ultima_directriz": bus.sniff("gemini_hyperparameters_update") if bus else None,
    }


@app.get("/api/v1/hybrix/telemetry", dependencies=[Depends(require_read_access)])
def get_telemetry(limit: int = Query(100, ge=1, le=MAX_PAGE_SIZE), offset: int = Query(0, ge=0)) -> Dict[str, Any]:
    with _lock:
        items = app.state.db["telemetry"][offset:offset + limit]
        return {
            "total": len(app.state.db["telemetry"]),
            "limit": limit,
            "offset": offset,
            "items": items
        }


@app.get("/api/v1/hybrix/predictions", dependencies=[Depends(require_read_access)])
def get_predictions(limit: int = Query(100, ge=1, le=MAX_PAGE_SIZE), offset: int = Query(0, ge=0)) -> Dict[str, Any]:
    with _lock:
        items = app.state.db["predictions"][offset:offset + limit]
        return {
            "total": len(app.state.db["predictions"]),
            "limit": limit,
            "offset": offset,
            "items": items
        }


@app.delete("/api/v1/hybrix/admin/records", dependencies=[Depends(require_api_key)])
def delete_records(confirm: bool = Query(False)) -> Dict[str, Any]:
    if not confirm:
        raise HTTPException(status_code=400, detail="Debe enviar confirm=true")
    with _lock:
        deleted = len(app.state.db["telemetry"]) + len(app.state.db["predictions"])
        app.state.db["telemetry"].clear()
        app.state.db["predictions"].clear()
        _guardar_estado(app.state.db)
    return {"status": "success", "deleted": deleted}
