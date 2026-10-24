"""Bucle continuo del supervisor.

    python -m app.autopilot                 # sin fin (Ctrl+C o archivo STOP para parar)
    python -m app.autopilot --cycles 3      # prueba

Cada ciclo: reencola tareas atascadas, siembra las revisiones estándar que tocan (cada
--reseed segundos por proyecto y tipo), ejecuta las pendientes y escribe reports/.
Deja un latido en la cola para que GET /supervisor/status sepa si está vivo.
"""
import argparse
import fcntl
import importlib
import logging
import os
import signal
import sys
import time
from pathlib import Path

APP = Path(__file__).resolve().parent
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from supervisor import Supervisor  # noqa: E402

# Módulos que se recargan en cada ciclo (orden de dependencias) para no usar nunca
# projects.json ni código de comprobaciones obsoletos.
RELOAD_ORDER = ["projects.manifest", "projects.knowledge", "projects",
                "supervisor.checks", "supervisor.supervisor", "supervisor"]


def reload_config():
    """Vacía la caché del manifiesto y recarga el código de comprobaciones.
    Devuelve la clase Supervisor recién cargada."""
    for name in RELOAD_ORDER:
        mod = sys.modules.get(name)
        if mod is not None:
            importlib.reload(mod)
    import supervisor as _s
    return _s.Supervisor


def acquire_lock(pid_file):
    """Bloqueo exclusivo (flock) sobre pid_file y escribe el PID real de Python.
    Devuelve el descriptor abierto, o None si ya hay otra instancia activa."""
    Path(pid_file).parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(pid_file), os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        os.close(fd)
        return None
    os.ftruncate(fd, 0)
    os.write(fd, f"{os.getpid()}\n".encode())
    os.fsync(fd)
    return fd

log = logging.getLogger("autopilot")
_stop = False


def _handle(sig, _frm):
    global _stop
    _stop = True
    log.info("señal %s recibida: paro al terminar el ciclo", sig)


def main(argv=None):
    ap = argparse.ArgumentParser(description="AGs-Core v3.6 autopilot")
    ap.add_argument("--cycles", type=int, default=0, help="0 = sin fin")
    ap.add_argument("--interval", type=float, default=float(os.getenv("AGS_AUTOPILOT_INTERVAL", 60)))
    ap.add_argument("--reseed", type=float, default=float(os.getenv("AGS_AUTOPILOT_RESEED", 6 * 3600)),
                    help="segundos entre revisiones del mismo proyecto y tipo")
    ap.add_argument("--max-workers", type=int, default=None)
    ap.add_argument("--workers-per-project", type=int, default=None)
    ap.add_argument("--stop-file", default=os.getenv("AGS_AUTOPILOT_STOP", str(APP.parent / "data" / "STOP")))
    ap.add_argument("--pid-file", default=os.getenv("AGS_AUTOPILOT_PIDFILE", str(APP.parent / "data" / "autopilot.pid")))
    ap.add_argument("--no-reload", action="store_true", help="no recargar config/código cada ciclo")
    a = ap.parse_args(argv)
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)
    lock_fd = acquire_lock(a.pid_file)
    if lock_fd is None:
        log.error("ya hay otro autopilot activo (bloqueo %s): salgo", a.pid_file)
        return 2
    sup = Supervisor(max_workers=a.max_workers, workers_per_project=a.workers_per_project)
    log.info("autopilot iniciado: %d proyectos, max_workers=%d, sub-agentes/proyecto=%d, intervalo=%ss, reseed=%ss",
             len(sup.projects()), sup.max_workers, sup.workers_per_project, a.interval, a.reseed)
    import agents  # noqa: F401  registra los agentes (incluye sub-agentes)
    _sub_state = {}
    n = 0
    while not _stop and (a.cycles == 0 or n < a.cycles):
        if Path(a.stop_file).exists():
            log.info("archivo STOP encontrado (%s): paro", a.stop_file)
            break
        n += 1
        try:
            if not a.no_reload:
                Sup = reload_config()
                sup = Sup(max_workers=a.max_workers, workers_per_project=a.workers_per_project)
            stale = sup.queue.requeue_stale()
            seeded = sup.seed(a.reseed)
            try:  # sub-agentes locales (CPU, intervalos propios, estado en data/subagentes/)
                import agents.subagents as _sa
                ran = _sa.run_due(_sub_state)
                if ran:
                    log.info("sub-agentes ejecutados: %s", ",".join(ran))
            except Exception:
                log.exception("fallo en sub-agentes")
            stats = sup.run_cycle(max_tasks=10_000)
            sup.queue.kv_set("autopilot_heartbeat", {"ts": time.time(), "pid": os.getpid(), "cycle": n, "interval": a.interval})
            lvl = logging.WARNING if stats["errors"] else logging.INFO
            log.log(lvl, "ciclo %d: sembradas=%d reencoladas=%d hechas=%d errores=%d (%.1fs) cola=%s",
                    n, seeded, stale, stats["done"], stats["errors"], stats["seconds"], sup.queue.counts())
            for e in sup.queue.events(5, "error"):
                if e["ts"] >= stats["ts"] - stats["seconds"] - 1:
                    log.error("tarea %s: %s", e["task_id"], e["message"][:300])
        except Exception:
            log.exception("fallo en el ciclo %d", n)
        if a.cycles and n >= a.cycles:
            break
        t_end = time.time() + a.interval
        while not _stop and time.time() < t_end:
            time.sleep(min(1.0, a.interval))
    hb = sup.queue.kv_get("autopilot_heartbeat") or {}
    hb.update({"ts": time.time(), "stopped": True, "pid": os.getpid()})
    sup.queue.kv_set("autopilot_heartbeat", hb)
    log.info("autopilot detenido tras %d ciclos", n)
    os.close(lock_fd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
