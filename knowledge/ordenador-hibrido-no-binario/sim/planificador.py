"""Planificador E2: HEFT vs consciente de error/coste de conversión (ADC/DAC).

Usa tablas de sim_mvm (salidas/resultados.csv) como modelo de coste sobre un DAG
sintético. NO es experimento. Semilla fija. Supuestos documentados en la salida.
"""
from __future__ import annotations
import csv, json, pathlib
from collections import defaultdict

D = pathlib.Path(__file__).parent
OUT = D / "salidas"
SEMILLA = 20261030  # distinta de MVM; fija para reproducibilidad del planificador
# Factores de latencia supuestos (ciclos relativos); no vienen de literatura verificada
LATENCIA_REL = {
    "cmos_digital": 1.0,
    "cim_memristivo": 0.4,  # supuesto: MVM analógico más rápido en este modelo
}
COM_COST = 0.05  # supuesto: coste de comunicación entre tareas (unidades de latencia)


def load_mvm_table(path: pathlib.Path):
    rows = list(csv.DictReader(open(path)))
    procs = []
    for r in rows:
        key = r["config"]
        if key == "cmos_digital":
            name = "cmos"
        else:
            name = f"cim_L{r['niveles']}_adc{r['bits_adc']}"
        procs.append({
            "name": name,
            "config": key,
            "niveles": int(float(r["niveles"])),
            "bits_adc": int(float(r["bits_adc"])),
            "error_rel": float(r["error_rel"]),
            "energia_por_mac_pj": float(r["energia_por_mac_pj"]),
            "frac_adc_dac": float(r["frac_adc_dac"]),
            "latencia_rel": LATENCIA_REL.get(key, 0.4),
        })
    return procs


def synthetic_dag():
    """DAG sintético: 8 tareas con precedencias. macs y error_max son supuestos."""
    # id -> {macs, error_max, preds}
    tasks = {
        "T0": {"macs": 5.0e6, "error_max": 0.50, "preds": []},
        "T1": {"macs": 8.0e6, "error_max": 0.20, "preds": ["T0"]},
        "T2": {"macs": 3.0e6, "error_max": 0.05, "preds": ["T0"]},  # pide alta precisión
        "T3": {"macs": 1.2e7, "error_max": 0.40, "preds": ["T1"]},
        "T4": {"macs": 4.0e6, "error_max": 0.02, "preds": ["T1", "T2"]},  # muy estricta → CMOS
        "T5": {"macs": 6.0e6, "error_max": 0.30, "preds": ["T3"]},
        "T6": {"macs": 2.0e6, "error_max": 0.15, "preds": ["T4"]},
        "T7": {"macs": 7.0e6, "error_max": 0.25, "preds": ["T5", "T6"]},
    }
    return tasks


def upward_rank(tasks, procs, cost_fn):
    """Rango ascendente HEFT con coste medio sobre procesadores factibles."""
    succs = defaultdict(list)
    for t, info in tasks.items():
        for p in info["preds"]:
            succs[p].append(t)
    rank = {}

    def _rank(t):
        if t in rank:
            return rank[t]
        costs = [cost_fn(t, p) for p in procs if cost_fn(t, p) is not None]
        w = sum(costs) / len(costs) if costs else 1e9
        if succs[t]:
            rank[t] = w + max(_rank(s) + COM_COST for s in succs[t])
        else:
            rank[t] = w
        return rank[t]

    for t in tasks:
        _rank(t)
    return rank


def schedule(tasks, procs, cost_fn, rank):
    """List-scheduling: orden por rango; asignar al proc con EFT mínimo factible."""
    order = sorted(tasks, key=lambda t: rank[t], reverse=True)
    ready_time_proc = {p["name"]: 0.0 for p in procs}
    finish = {}
    assign = {}
    energy = {}
    for t in order:
        best = None
        for p in procs:
            c = cost_fn(t, p)
            if c is None:
                continue
            est = max(
                [finish[pr] + COM_COST for pr in tasks[t]["preds"]] + [ready_time_proc[p["name"]]]
            )
            eft = est + c
            e = p["energia_por_mac_pj"] * tasks[t]["macs"]
            cand = (eft, e, p["name"], est, c, p)
            if best is None or cand[0] < best[0] or (cand[0] == best[0] and cand[1] < best[1]):
                best = cand
        if best is None:
            raise RuntimeError(f"sin procesador factible para {t}")
        eft, e, pname, est, dur, p = best
        assign[t] = {
            "procesador": pname,
            "inicio": est,
            "fin": eft,
            "duracion": dur,
            "energia_pj": e,
            "error_rel_modelo": p["error_rel"],
            "frac_adc_dac": p["frac_adc_dac"],
            "error_max_tarea": tasks[t]["error_max"],
        }
        finish[t] = eft
        ready_time_proc[pname] = eft
        energy[t] = e
    makespan = max(finish.values())
    return {
        "asignacion": assign,
        "makespan": makespan,
        "energia_total_pj": sum(energy.values()),
        "orden": order,
    }


def cost_heft(tasks, procs):
    """Coste = latencia_rel * escala por macs (media de procs; sin filtro de error)."""
    ref = max(tasks[t]["macs"] for t in tasks)

    def fn(t, p):
        return p["latencia_rel"] * (tasks[t]["macs"] / ref)

    return fn


def cost_error_aware(tasks, procs):
    """Descarta destinos con error_rel > error_max; coste = latencia + α·energía_norm + β·frac_adc_dac."""
    ref_macs = max(tasks[t]["macs"] for t in tasks)
    e_max = max(p["energia_por_mac_pj"] for p in procs) or 1.0
    alpha, beta = 0.3, 0.2  # supuestos de ponderación

    def fn(t, p):
        if p["error_rel"] > tasks[t]["error_max"]:
            return None  # no factible
        lat = p["latencia_rel"] * (tasks[t]["macs"] / ref_macs)
        en = alpha * (p["energia_por_mac_pj"] / e_max)
        conv = beta * p["frac_adc_dac"]
        return lat + en + conv

    return fn


def main():
    table = OUT / "resultados.csv"
    if not table.exists():
        raise SystemExit("falta salidas/resultados.csv; ejecuta sim_mvm.py antes")
    procs = load_mvm_table(table)
    # restringir a un subconjunto representativo para el DAG (menos ruido en salida)
    keep = {"cmos", "cim_L4_adc4", "cim_L8_adc6", "cim_L16_adc8"}
    procs = [p for p in procs if p["name"] in keep]
    tasks = synthetic_dag()

    resultados = {}
    for nombre, cost_builder in (
        ("HEFT", cost_heft),
        ("error_coste_aware", cost_error_aware),
    ):
        fn = cost_builder(tasks, procs)
        rank = upward_rank(tasks, procs, fn)
        resultados[nombre] = schedule(tasks, procs, fn, rank)
        resultados[nombre]["ranks"] = {k: round(v, 6) for k, v in rank.items()}

    heft_e = resultados["HEFT"]["energia_total_pj"]
    aw_e = resultados["error_coste_aware"]["energia_total_pj"]
    resumen = {
        "nivel_evidencia": "E2",
        "tipo": "simulacion",
        "nota": "prototipo mínimo; no es experimento ni validación de hardware",
        "semilla": SEMILLA,
        "propuesta_diseno_nivel": "E0",
        "supuestos": [
            "DAG sintético de 8 tareas con macs y error_max inventados para la demo",
            "latencias relativas CMOS=1.0, CIM=0.4 (supuesto)",
            "COM_COST=0.05 entre tareas (supuesto)",
            "ponderación α=0.3 (energía) β=0.2 (frac ADC/DAC) en el planificador consciente (supuesto)",
            "modelo de coste = tablas sim_mvm con parámetros supuestos (E2)",
            "sin fotónica ni QPU en esta corrida (solo CMOS y configs CIM de la tabla)",
        ],
        "procesadores": [{"name": p["name"], "error_rel": p["error_rel"],
                          "energia_por_mac_pj": p["energia_por_mac_pj"],
                          "frac_adc_dac": p["frac_adc_dac"]} for p in procs],
        "comparacion": {
            "HEFT_makespan": resultados["HEFT"]["makespan"],
            "HEFT_energia_pj": heft_e,
            "aware_makespan": resultados["error_coste_aware"]["makespan"],
            "aware_energia_pj": aw_e,
            "ahorro_energia_aware_vs_heft": (1 - aw_e / heft_e) if heft_e else None,
        },
        "resultados": resultados,
    }
    OUT.mkdir(exist_ok=True)
    json.dump(resumen, open(OUT / "planificador_resultados.json", "w"), indent=1, ensure_ascii=False)
    # CSV plano de asignaciones
    with open(OUT / "planificador_asignaciones.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "tarea", "procesador", "inicio", "fin", "energia_pj",
                    "error_rel_modelo", "error_max_tarea", "frac_adc_dac"])
        for alg, res in resultados.items():
            for t, a in res["asignacion"].items():
                w.writerow([alg, t, a["procesador"], a["inicio"], a["fin"], a["energia_pj"],
                            a["error_rel_modelo"], a["error_max_tarea"], a["frac_adc_dac"]])
    print(json.dumps(resumen["comparacion"], indent=1, ensure_ascii=False))
    # conteo de destinos CIM vs CMOS
    for alg, res in resultados.items():
        dest = defaultdict(int)
        for a in res["asignacion"].values():
            dest[a["procesador"]] += 1
        print(alg, dict(dest))


if __name__ == "__main__":
    main()
