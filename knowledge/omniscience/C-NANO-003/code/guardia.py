"""Protección de memoria C-NANO-002: oom_score_adj=1000 (el OOM elige este proceso antes que CP2K) y vigilante que aborta si MemAvailable < 700 MB."""
import os, threading, time, sys
def _mem():
    for l in open("/proc/meminfo"):
        if l.startswith("MemAvailable"): return int(l.split()[1]) // 1024
def activar(umbral=700):
    try: open("/proc/self/oom_score_adj", "w").write("1000")
    except Exception as e: print("oom_score_adj no aplicado", e, flush=True)
    def vig():
        while True:
            if _mem() < umbral: print(f"GUARDIA: MemAvailable<{umbral} MB, aborto", flush=True); sys.stdout.flush(); os._exit(42)
            time.sleep(1)
    threading.Thread(target=vig, daemon=True).start()
