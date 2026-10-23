"""Sub-agentes especializados ligeros (CPU, sin LLM, sin red externa) — AGs-Core v3.6.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT.
Evidencia: E3 software (comprobaciones reales con tests unitarios). No entrenan, no publican, no hacen push,
no descargan pesos. Cada uno escribe su estado JSON (snake_case, sin null) en data/subagentes/<nombre>.json.
"""
import asyncio, hashlib, importlib.util, json, os, re, shutil, time
from pathlib import Path

from base_agent import BaseAgent
from registry import register

ROOT = Path(__file__).resolve().parents[2]
KN = ROOT / "knowledge"
DATA = KN / "fusi-n-carpeta" / "data"
STATUS_DIR = ROOT / "data" / "subagentes"
TEST_SHA = "0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5"
AUTOR = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
LLP_KEYS = {"meta", "objetivo", "datos_clave", "tareas", "riesgos", "decisiones", "proximo_paso"}
SNAKE = re.compile(r"^[a-z0-9_áéíóúñü]+$")


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else ""


def _clean(x):
    """Sin null: None → ''."""
    if isinstance(x, dict):
        return {k: _clean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_clean(v) for v in x]
    return "" if x is None else x


class WorkerAgent(BaseAgent):
    domain = "subagentes"
    preferred_model = "local_check"
    fallback_models: list = []
    interval = 900  # segundos entre ejecuciones desde el autopilot

    @property
    def system_prompt(self):
        return f"Sub-agente local '{self.name}': {self.description}. Comprobaciones reales, no inventa."

    def check(self) -> dict:  # pragma: no cover - abstracto
        raise NotImplementedError

    def execute(self, write: bool = True) -> dict:
        t0 = time.time()
        try:
            res = self.check(); estado = "ok" if not res.get("problemas") else "aviso"
        except Exception as exc:  # el bucle nunca se cae por un worker
            res = {"problemas": [f"{type(exc).__name__}: {str(exc)[:200]}"]}; estado = "error"
        out = _clean({"sub_agente": self.name, "estado": estado, "ts": round(t0, 1),
                      "duracion_s": round(time.time() - t0, 3), "evidencia": "E3_software",
                      "autor": AUTOR, **res})
        if write:
            STATUS_DIR.mkdir(parents=True, exist_ok=True)
            (STATUS_DIR / f"{self.name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        return out

    async def run(self, task, context=None):
        out = await asyncio.to_thread(self.execute)
        return {"agent": self.name, "domain": self.domain, "model_used": "local_check", "output": out,
                "evidencia": "E3_software", "es_evidencia": False}


@register
class VerificadorLicencias(WorkerAgent):
    name = "verificador_licencias"; description = "LICENSE/NOTICE por proyecto y licencias pendientes"
    interval = 3600
    def check(self):
        sin = [p.name for p in sorted(KN.iterdir()) if p.is_dir() and not any((p / f).exists() for f in ("LICENSE", "LICENSE.md", "NOTICE", "NOTICE.md"))]
        pend = []
        lj = KN / "fusi-n-carpeta" / "licencias.json"
        if lj.exists():
            for m in json.loads(lj.read_text(encoding="utf-8")).get("modelos", []):
                if "PENDIENTE" in json.dumps(m, ensure_ascii=False).upper():
                    pend.append(m.get("id", ""))
        return {"proyectos_sin_licencia": sin, "licencias_pendientes": pend,
                "problemas": ([f"{len(sin)} proyectos sin LICENSE/NOTICE"] if sin else []) + ([f"{len(pend)} licencias PENDIENTE DE VERIFICACIÓN"] if pend else [])}


@register
class DetectorDuplicados(WorkerAgent):
    name = "detector_duplicados"; description = "duplicados exactos y casi-duplicados; filtraciones a test"
    interval = 3600
    def check(self):
        spec = importlib.util.spec_from_file_location("near_dup", ROOT / "scripts" / "near_dup.py")
        nd = importlib.util.module_from_spec(spec); spec.loader.exec_module(nd)
        items = nd.load_pairs(); exact, near = nd.analyse_pairs(items, 0.85); lk = nd.leaks(exact, near, items)
        return {"pares": len(items), "grupos_exactos": len(exact), "casi": len(near), "filtraciones_a_test": len(lk),
                "problemas": [f"{len(lk)} filtraciones a test"] if lk else []}


@register
class RevisorEvidencia(WorkerAgent):
    name = "revisor_evidencia_e0_e6"; description = "afirmaciones E4–E6 sin marca de verificación en docs"
    interval = 3600
    PAT = re.compile(r"\bE[456]\b")
    def check(self):
        hits = []
        for p in sorted(KN.rglob("*.md")):
            for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if self.PAT.search(line) and not re.search(r"E0\s*[–-]\s*E6|PENDIENTE|no es|sin |ningún|objetivo|requiere|futuro|hasta", line, re.I):
                    hits.append({"archivo": str(p.relative_to(ROOT)), "linea": i, "texto": line.strip()[:160]})
        return {"afirmaciones_e4_e6_revisar": len(hits), "ejemplos": hits[:20],
                "problemas": [f"{len(hits)} líneas con E4–E6 a revisar"] if hits else []}


@register
class ValidadorEsquemaLLP(WorkerAgent):
    name = "validador_esquema_llp"; description = "respuestas LLP JSON: claves, snake_case, sin null"
    interval = 1800
    @staticmethod
    def validate(obj) -> list[str]:
        errs = []
        def walk(x, path=""):
            if x is None:
                errs.append(f"null en {path or '/'}")
            elif isinstance(x, dict):
                for k, v in x.items():
                    if not SNAKE.match(k):
                        errs.append(f"clave no snake_case: {path}/{k}")
                    walk(v, f"{path}/{k}")
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    walk(v, f"{path}[{i}]")
        walk(obj)
        if isinstance(obj, dict) and LLP_KEYS & set(obj) and not LLP_KEYS <= set(obj):
            errs.append(f"faltan claves LLP: {sorted(LLP_KEYS - set(obj))}")
        return errs
    def check(self):
        tot = llp = 0; bad = []
        for split in ("train", "val", "test"):
            for i, line in enumerate((DATA / f"{split}.jsonl").read_text(encoding="utf-8").splitlines(), 1):
                tot += 1
                try:
                    obj = json.loads(json.loads(line)["response"])
                except Exception:
                    continue
                if not isinstance(obj, dict):
                    continue
                llp += 1
                e = self.validate(obj)
                if e:
                    bad.append({"split": split, "linea": i, "errores": e[:3]})
        return {"pares": tot, "respuestas_json": llp, "invalidas": len(bad), "ejemplos": bad[:20],
                "problemas": [f"{len(bad)} respuestas LLP inválidas"] if bad else []}


@register
class MonitorServicios(WorkerAgent):
    name = "monitor_servicios"; description = "estado HTTP de API, UIs, NNC y LiteLLM (solo localhost)"
    interval = 300
    URLS = {"api_8000": "http://127.0.0.1:8000/health", "ui_8501": "http://127.0.0.1:8501/",
            "ucs_8502": "http://127.0.0.1:8502/", "nnc_8080": "http://127.0.0.1:8080/", "nnc_8010": "http://127.0.0.1:8010/",
            "litellm": os.getenv("LITELLM_BASE_URL", "http://localhost:4000") + "/health/liveliness"}
    def check(self):
        import httpx
        st = {}
        for k, u in self.URLS.items():
            try:
                st[k] = f"http_{httpx.get(u, timeout=3).status_code}"
            except Exception:
                st[k] = "caido"
        down = [k for k, v in st.items() if v != "http_200"]
        return {"servicios": st, "problemas": [f"no responden 200: {down}"] if down else []}


@register
class Preflight7B(WorkerAgent):
    name = "preflight_7b"; description = "chequeo previo al entrenamiento 7B (no entrena, no descarga pesos)"
    interval = 3600
    def check(self):
        prob = []
        man = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
        splits = {}
        for s in ("train", "val", "test"):
            p = DATA / f"{s}.jsonl"; h = _sha_file(p)
            exp = man.get("splits", {}).get(s, {}).get("sha256", "")
            n = sum(1 for _ in p.open(encoding="utf-8"))
            schema_ok = all({"instruction", "response"} <= set(json.loads(l)) for l in p.read_text(encoding="utf-8").splitlines() if l.strip())
            splits[s] = {"pares": n, "sha256_ok": h == exp, "esquema_ok": schema_ok}
            if h != exp: prob.append(f"sha256 {s} no coincide con manifest")
            if not schema_ok: prob.append(f"esquema {s} inválido")
        test_ok = _sha_file(DATA / "test.jsonl") == TEST_SHA
        if not test_ok: prob.append("test congelado modificado")
        cfg = KN / "fusi-n-carpeta" / "configs" / "lora.yaml"
        cfg_txt = cfg.read_text(encoding="utf-8") if cfg.exists() else ""
        if not cfg_txt: prob.append("falta configs/lora.yaml")
        gpu = bool(shutil.which("nvidia-smi"))
        try:
            import torch; gpu = gpu or bool(torch.cuda.is_available())
        except Exception:
            pass
        if not gpu: prob.append("sin GPU: entrenamiento 7B bloqueado")
        mem = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo") if l.split(":")[0] in ("MemTotal", "MemAvailable")}
        disk = shutil.disk_usage(ROOT)
        lic = json.loads((KN / "fusi-n-carpeta" / "licencias.json").read_text(encoding="utf-8")) if (KN / "fusi-n-carpeta" / "licencias.json").exists() else {}
        n_train = splits["train"]["pares"]
        return {"splits": splits, "test_congelado_ok": test_ok, "lora_yaml": bool(cfg_txt),
                "licencias_modelos": [{"id": m.get("id", ""), "licencia": m.get("licencia", "")} for m in lic.get("modelos", [])],
                "gpu": gpu, "ram_total_gb": round(mem.get("MemTotal", 0) / 2**20, 1), "ram_libre_gb": round(mem.get("MemAvailable", 0) / 2**20, 1),
                "disco_libre_gb": round(disk.free / 2**30, 1),
                "estimacion": {"evidencia": "E0_estimacion_orden_magnitud", "metodo": "QLoRA 4-bit 7B: pesos ~3.5 GB + activaciones/optimizador",
                               "vram_gb_min": 10, "vram_gb_recomendada": 16, "pesos_descarga_gb": 14.5,
                               "tiempo_h_3_epocas_gpu_24gb": round(3 * n_train * 0.5 / 3600, 2)},
                "aprobacion_usuario": "requerida", "entrena": False, "descarga_pesos": False, "problemas": prob}


@register
class GeneradorParesLora(WorkerAgent):
    name = "generador_pares_lora"; description = "recoge y valida pares nuevos de agentes en staging (no toca test)"
    interval = 1800
    SOURCES = [Path("/workspace/p003/pares_lora.jsonl")]
    def check(self):
        def key(r): return hashlib.sha256(re.sub(r"\s+", " ", f"{r.get('instruction','')} {r.get('response','')}".lower()).strip().encode()).hexdigest()
        seen = set()
        for s in ("train", "val", "test"):
            for l in (DATA / f"{s}.jsonl").read_text(encoding="utf-8").splitlines():
                if l.strip(): seen.add(key(json.loads(l)))
        files = [p for p in sorted(KN.rglob("*.jsonl")) if DATA not in p.parents] + [p for p in self.SOURCES if p.exists()]
        nuevos, simulados, invalidos, ya = [], [], 0, 0
        for p in files:
            for l in p.read_text(encoding="utf-8").splitlines():
                try: r = json.loads(l)
                except Exception: invalidos += 1; continue
                if isinstance(r, dict):  # alias aceptados por knowledge/fusi-n-carpeta/docs/esquema_lora_pares.md
                    if "instruction" not in r and "instruccion" in r: r = {**{k: v for k, v in r.items() if k != "instruccion"}, "instruction": r["instruccion"]}
                    if "response" not in r and "respuesta" in r: r = {**{k: v for k, v in r.items() if k != "respuesta"}, "response": r["respuesta"]}
                if not isinstance(r, dict) or not str(r.get("instruction", "")).strip() or not str(r.get("response", "")).strip():
                    invalidos += 1; continue
                k = key(r)
                if k in seen: ya += 1; continue
                seen.add(k)
                row = _clean({**r, "origen": str(p), "sha256": k, "autor": r.get("autor") or AUTOR})
                (simulados if r.get("simulado") is True or "simulad" in str(r.get("evidencia", "")).lower() else nuevos).append(row)
        out = ROOT / "data" / "staging"; out.mkdir(parents=True, exist_ok=True)
        for fn, rows in (("pares_staging.jsonl", nuevos), ("pares_simulados_fuera_train.jsonl", simulados)):
            (out / fn).write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows), encoding="utf-8")
        return {"archivos": len(files), "nuevos_staging": len(nuevos), "simulados_fuera": len(simulados),
                "ya_en_dataset": ya, "invalidos": invalidos, "toca_test": False,
                "problemas": [f"{invalidos} líneas inválidas"] if invalidos else []}


WORKERS = [VerificadorLicencias, DetectorDuplicados, RevisorEvidencia, ValidadorEsquemaLLP, MonitorServicios, Preflight7B, GeneradorParesLora]


def run_due(state: dict, now: float | None = None) -> list[str]:
    """Ejecuta los workers cuyo intervalo ha vencido. state: {nombre: ts_ultima}."""
    from registry import get_agent
    now = now or time.time(); ran = []
    for cls in WORKERS:
        w = get_agent(cls.name)
        if now - state.get(w.name, 0) >= w.interval:
            w.execute(); state[w.name] = now; ran.append(w.name)
    return ran
