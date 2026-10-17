"""Bucle continuo del supervisor.

    python -m app.autopilot                 # sin fin (Ctrl+C o archivo STOP para parar)
    python -m app.autopilot --cycles 3      # prueba

Cada ciclo: reencola tareas atascadas, siembra las revisiones estándar que tocan (cada
--reseed segundos por proyecto y tipo), ejecuta las pendientes y escribe reports/.
Deja un latido en la cola para que GET /supervisor/status sepa si está vivo.
"""
import argparse
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
    a = ap.parse_args(argv)
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    signal.signal(signal.SIGTERM, _handle)
    signal.signal(signal.SIGINT, _handle)
    sup = Supervisor(max_workers=a.max_workers, workers_per_project=a.workers_per_project)
    log.info("autopilot iniciado: %d proyectos, max_workers=%d, sub-agentes/proyecto=%d, intervalo=%ss, reseed=%ss",
             len(sup.projects()), sup.max_workers, sup.workers_per_project, a.interval, a.reseed)
    n = 0
    while not _stop and (a.cycles == 0 or n < a.cycles):
        if Path(a.stop_file).exists():
            log.info("archivo STOP encontrado (%s): paro", a.stop_file)
            break
        n += 1
        try:
            stale = sup.queue.requeue_stale()
            seeded = sup.seed(a.reseed)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
