import os
import json
import logging
import threading
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

API_KEY = os.getenv("HYBRIX_API_KEY", "")
DB_PATH = Path(os.getenv("HYBRIX_DB_PATH", "hybrix_api_state.json"))
PROJECTS_PATH = Path(os.getenv("HYBRIX_PROJECTS_PATH", "projects.json"))
MAX_RECORDS = int(os.getenv("HYBRIX_MAX_RECORDS", "100000"))
MAX_PAGE_SIZE = 1000
_lock = threading.RLock()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
LOCAL_HOSTS = {"127.0.0.1", "::1", "localhost"}
logger = logging.getLogger("hybrix")

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def require_api_key(request: Request, key: Optional[str] = Security(api_key_header)) -> None:
    if not API_KEY:
        client_host = request.client.host if request.client else ""
        if client_host in LOCAL_HOSTS:
            return
        raise HTTPException(status_code=403, detail="Acceso no autorizado")
    if not key or not time_constant_compare(key, API_KEY):
        raise HTTPException(status_code=401, detail="Clave API invalida o ausente")

def time_constant_compare(val1: str, val2: str) -> bool:
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0

class TelemetryData(BaseModel):
    trial_id: int = Field(..., ge=0)
    node_id: str = Field(..., min_length=1, max_length=64)
    timestamp: Optional[str] = None
    viability: float = Field(..., ge=0.0, le=1.0)
    active_electrodes: int = Field(..., ge=0, le=32)

class TelemetryBatch(BaseModel):
    items: List[TelemetryData]

class PredictionData(BaseModel):
    trial_id: int = Field(..., ge=0)
    node_id: str = Field(..., min_length=1, max_length=64)
    timestamp: Optional[str] = None
    label: int = Field(..., ge=0, le=1)
    prediction: int = Field(..., ge=0, le=1)
    probability: float = Field(..., ge=0.0, le=1.0)

class PredictionBatch(BaseModel):
    items: List[PredictionData]

def _guardar_estado(db: Dict[str, Any]) -> None:
    tmp = DB_PATH.with_name(f"{DB_PATH.name}.tmp")
    tmp.write_text(json.dumps({"telemetry": db["telemetry"], "predictions": db["predictions"]}), encoding="utf-8")
    tmp.replace(DB_PATH)

def _exportar_preventivo_critico(db: Dict[str, Any], trial_id: int) -> str:
    export_dir = Path("/workspace/scratch/auto_exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    filename = export_dir / f"critical_export_trial_{trial_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    lines = ["trial_id,telemetry_node_id,telemetry_timestamp,telemetry_received_at,viability,active_electrodes\n"]
    for item in db["telemetry"]:
        lines.append(f"{item['trial_id']},{item['node_id']},{item.get('timestamp','')},{item.get('received_at','')},{item['viability']},{item['active_electrodes']}\n")
    filename.write_text("".join(lines), encoding="utf-8")
    return str(filename)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = {"projects_meta": {}, "telemetry": [], "predictions": []}
    yield
    try:
        _guardar_estado(app.state.db)
    except Exception:
        pass

app = FastAPI(title="HYBRIX Orquestacion API", version="1.9.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

def _append(collection: List[Dict[str, Any]], item: Dict[str, Any]) -> None:
    collection.append(item)
    excess = len(collection) - MAX_RECORDS
    if excess > 0:
        del collection[:excess]

@app.get("/api/v1/hybrix/status")
def get_status() -> Dict[str, Any]:
    with _lock:
        return {
            "status": "online",
            "timestamp": utc_now(),
            "records_telemetry": len(app.state.db["telemetry"]),
            "records_predictions": len(app.state.db["predictions"]),
        }

@app.post("/api/v1/hybrix/telemetry", status_code=201, dependencies=[Depends(require_api_key)])
def post_telemetry(data: TelemetryData) -> Dict[str, Any]:
    record = data.model_dump()
    record["timestamp"] = record["timestamp"] or utc_now()
    record["received_at"] = utc_now()
    alert_info = {}
    with _lock:
        _append(app.state.db["telemetry"], record)
        if record["viability"] < 0.70:
            logger.warning(f"[ALERTA BIOLOGICA CRITICA] Viabilidad baja ({record['viability']}) en trial_id={record['trial_id']}")
            export_path = _exportar_preventivo_critico(app.state.db, record["trial_id"])
            alert_info = {
                "alert": "CRITICAL_LOW_VIABILITY",
                "message": f"Alerta: Viabilidad ({record['viability']}) inferior al umbral critico del 70%.",
                "auto_export_file": export_path
            }
    res = {"status": "success", "inserted": 1}
    res.update(alert_info)
    return res

@app.post("/api/v1/hybrix/telemetry/batch", status_code=201, dependencies=[Depends(require_api_key)])
def post_telemetry_batch(batch: TelemetryBatch) -> Dict[str, Any]:
    now = utc_now()
    records = []
    for item in batch.items:
        rec = item.model_dump()
        rec["timestamp"] = rec["timestamp"] or now
        rec["received_at"] = now
        records.append(rec)
    with _lock:
        for rec in records:
            _append(app.state.db["telemetry"], rec)
    return {"status": "success", "inserted": len(records)}

@app.get("/api/v1/hybrix/telemetry")
def get_telemetry(limit: int = Query(100, ge=1, le=MAX_PAGE_SIZE), offset: int = Query(0, ge=0)) -> Dict[str, Any]:
    with _lock:
        return {
            "total": len(app.state.db["telemetry"]),
            "items": app.state.db["telemetry"][offset:offset + limit],
        }

@app.post("/api/v1/hybrix/predictions", status_code=201, dependencies=[Depends(require_api_key)])
def post_prediction(data: PredictionData) -> Dict[str, Any]:
    record = data.model_dump()
    record["timestamp"] = record["timestamp"] or utc_now()
    record["received_at"] = utc_now()
    with _lock:
        _append(app.state.db["predictions"], record)
    return {"status": "success", "inserted": 1}
