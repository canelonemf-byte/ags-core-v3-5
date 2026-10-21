#!/usr/bin/env python3
"""Estadística P003 (enmienda ORÁCULO 2026-10-21): McNemar exacto pareado, Holm, IC95 pareado de la diferencia,
media/dispersión entre semillas y potencia exacta de McNemar. Python puro (sin scipy).
--selftest usa DATOS SINTÉTICOS (no son resultados de ningún modelo).
Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia MIT."""
import argparse, json, math, random, statistics, sys

def _binom_pmf(k, n, p=0.5):
    return math.comb(n, k) * p**k * (1 - p)**(n - k)

def mcnemar_exacto(b, c):
    """b = LoRA acierta y base falla; c = base acierta y LoRA falla. p bilateral exacto (binomial condicional, p=0.5)."""
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(_binom_pmf(i, n) for i in range(k + 1)))

def holm(pvals, alfa=0.05):
    """pvals: dict nombre->p. Holm-Bonferroni; con 2 modelos el primer umbral es alfa/2 = 0.025."""
    orden = sorted(pvals.items(), key=lambda kv: kv[1]); m = len(orden); out = {}; prev = 0.0; parar = False
    for i, (k, p) in enumerate(orden):
        adj = min(1.0, max(prev, (m - i) * p)); prev = adj
        rech = (not parar) and p <= alfa / (m - i)
        if not rech: parar = True
        out[k] = {"p": round(p, 6), "p_ajustado_holm": round(adj, 6), "umbral": round(alfa / (m - i), 6), "rechaza_h0": rech}
    return out

def ic95_pareado(b, c, n, z=1.959963984540054):
    """IC95 de p_lora - p_base pareado, Agresti-Min (2005): +0.5 a cada celda."""
    if n <= 0: return [0.0, 0.0]
    b2, c2, n2 = b + 0.5, c + 0.5, n + 2.0
    d = (b2 - c2) / n2
    se = math.sqrt(((b2 + c2) - (b2 - c2) ** 2 / n2) / n2 ** 2)
    return [round(max(-1.0, d - z * se), 4), round(min(1.0, d + z * se), 4)]

def tabla(base, lora):
    assert len(base) == len(lora) and base
    b = sum(1 for x, y in zip(base, lora) if y and not x); c = sum(1 for x, y in zip(base, lora) if x and not y)
    return {"n": len(base), "b_lora_si_base_no": b, "c_base_si_lora_no": c, "p_base": sum(base) / len(base), "p_lora": sum(lora) / len(lora)}

def comparar(brazos, alfa=0.05, umbral_pts=10.0):
    """brazos: {modelo: {"base": [0/1], "lora": [0/1]}} sobre los mismos ítems. Primaria: McNemar exacto + Holm."""
    res, ps = {}, {}
    for mod, d in brazos.items():
        t = tabla(d["base"], d["lora"]); b, c, n = t["b_lora_si_base_no"], t["c_base_si_lora_no"], t["n"]
        ps[mod] = mcnemar_exacto(b, c); dif = 100 * (t["p_lora"] - t["p_base"])
        res[mod] = {**t, "diferencia_pts": round(dif, 2), "ic95_diferencia": ic95_pareado(b, c, n), "criterio_10pts_puntual": dif >= umbral_pts}
    h = holm(ps, alfa)
    for mod in res:
        res[mod].update(h[mod]); res[mod]["h1_enmienda"] = h[mod]["rechaza_h0"] and res[mod]["diferencia_pts"] > 0
    return res

def resumen_semillas(valores):
    v = list(valores.values())
    return {"n_semillas": len(v), "media": round(statistics.mean(v), 4), "desv_tipica": round(statistics.stdev(v), 4) if len(v) > 1 else 0.0,
            "min": min(v), "max": max(v), "semillas": sorted(valores)}

def potencia_mcnemar(n, p10, p01, alfa=0.025):
    """Potencia exacta de McNemar bilateral (cálculo bajo supuestos, no resultado). Rechazo en dirección LoRA > base."""
    pd = p10 + p01; q = p10 / pd if pd else 0.5; pot = 0.0
    for m in range(n + 1):
        pm = _binom_pmf(m, n, pd)
        if pm < 1e-12: continue
        for b in range(m + 1):
            if b * 2 > m and mcnemar_exacto(b, m - b) <= alfa: pot += pm * _binom_pmf(b, m, q)
    return pot

def n_para_potencia(delta, disc, alfa=0.025, objetivo=0.8, nmax=1000):
    p10, p01 = (disc + delta) / 2, (disc - delta) / 2
    lo, hi = 10, nmax
    if potencia_mcnemar(hi, p10, p01, alfa) < objetivo: return -1
    while hi - lo > 1:  # búsqueda binaria (potencia ~monótona; puede oscilar por discreción)
        mid = (lo + hi) // 2
        if potencia_mcnemar(mid, p10, p01, alfa) >= objetivo: hi = mid
        else: lo = mid
    return hi

def selftest():
    print("SELFTEST con DATOS SINTÉTICOS (no son resultados de modelos)")
    assert abs(mcnemar_exacto(7, 0) - 0.015625) < 1e-12
    assert mcnemar_exacto(0, 0) == 1.0 and abs(mcnemar_exacto(5, 5) - 1.0) < 1e-12
    h = holm({"a": 0.01, "b": 0.04}); assert h["a"]["rechaza_h0"] and h["b"]["rechaza_h0"]
    h = holm({"a": 0.03, "b": 0.04}); assert not h["a"]["rechaza_h0"] and not h["b"]["rechaza_h0"]
    ic = ic95_pareado(7, 0, 66); assert abs(ic[0] - 0.025) < 0.0006 and abs(ic[1] - 0.181) < 0.0006, ic  # ORÁCULO: [0.025, 0.181]
    print(json.dumps({"ic95_b7_c0_n66": ic, "referencia_oraculo": [0.025, 0.181]}))
    rng = random.Random(42)
    def sint(pb, pl, n=66):
        base = [int(rng.random() < pb) for _ in range(n)]
        return {"base": base, "lora": [1 if x else int(rng.random() < (pl - pb) / (1 - pb)) for x in base]}
    r = comparar({"sintetico_A": sint(0.4, 0.7), "sintetico_B": sint(0.4, 0.42)})
    print(json.dumps({"sintetico": True, "comparacion": r}, ensure_ascii=False, separators=(",", ":")))
    print(json.dumps({"sintetico": True, "semillas": resumen_semillas({42: 0.61, 43: 0.58, 44: 0.64})}, separators=(",", ":")))
    pw = potencia_mcnemar(66, 0.10, 0.0, alfa=0.05); assert abs(pw - 0.657) < 0.005, pw
    print(json.dumps({"potencia_n66_disc0.1_alfa0.05": round(pw, 3), "referencia_oraculo": 0.657}, separators=(",", ":")))
    print("SELFTEST OK")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--n-potencia", action="store_true", help="n para potencia 0.8, delta 0.10, alfa 0.025 (cálculo)")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.n_potencia:
        print(json.dumps({f"disc_{d:.2f}": n_para_potencia(0.10, d) for d in (0.10, 0.15, 0.20, 0.25, 0.30, 0.40)}, separators=(",", ":")))
