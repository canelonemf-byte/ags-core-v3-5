"""SIMULACIÓN (E1–E2) de orquestación con N sub-agentes simulados. NO son agentes reales.

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT.
Modelo: cola de eventos discretos; N workers simulados con tiempo de servicio exponencial, K coordinadores,
tasa de fallo p con reintento. Mide throughput, latencia p50/p95 y utilización. Sin red, sin LLM.
    python scripts/sim_subagentes.py --n 50000 --tareas 200000
"""
import argparse, heapq, json, random, sys


def simular(n=50000, tareas=200000, coord=100, servicio_s=30.0, llegada_hz=1000.0, p_fallo=0.02, seed=42):
    rnd = random.Random(seed)
    libres = n; cola = []; ev = []; t = 0.0; lat = []; fallos = 0; ocupado = 0.0
    for i in range(tareas):
        t += rnd.expovariate(llegada_hz); heapq.heappush(ev, (t, 0, i, t))
    coord_cap = coord * 50.0  # despachos/s por coordinador (supuesto)
    ultimo_desp = 0.0
    while ev:
        t, tipo, i, t0 = heapq.heappop(ev)
        if tipo == 0:
            cola.append((i, t0))
        else:
            libres += 1
            if rnd.random() < p_fallo:
                fallos += 1; cola.append((i, t0))
            else:
                lat.append(t - t0)
        while libres and cola:
            ultimo_desp = max(ultimo_desp + 1.0 / coord_cap, t)
            j, s0 = cola.pop(0) if len(cola) < 1000 else cola.pop()
            d = rnd.expovariate(1.0 / servicio_s); ocupado += d
            libres -= 1; heapq.heappush(ev, (ultimo_desp + d, 1, j, s0))
    lat.sort(); dur = t
    return {"simulacion": True, "evidencia": "E2_simulacion_computacional", "aviso": "workers simulados, no agentes reales",
            "parametros": {"n_workers": n, "tareas": tareas, "coordinadores": coord, "servicio_medio_s": servicio_s,
                           "llegada_hz": llegada_hz, "p_fallo": p_fallo, "seed": seed},
            "resultado": {"completadas": len(lat), "reintentos": fallos, "duracion_sim_s": round(dur, 1),
                          "throughput_hz": round(len(lat) / dur, 2) if dur else 0,
                          "latencia_p50_s": round(lat[len(lat) // 2], 2), "latencia_p95_s": round(lat[int(len(lat) * .95)], 2),
                          "utilizacion": round(ocupado / (n * dur), 4) if dur else 0}}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for k, v in (("n", 50000), ("tareas", 200000), ("coord", 100), ("seed", 42)):
        ap.add_argument(f"--{k}", type=int, default=v)
    a = ap.parse_args()
    print(json.dumps(simular(a.n, a.tareas, a.coord, seed=a.seed), ensure_ascii=False))
