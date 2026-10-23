"""Ejemplo: energía negativa necesaria para una burbuja de Alcubierre y para la de Natário.
Uso: python examples/energia_burbuja.py [v_m_s] [R_m] [sigma_1_m]"""
import sys
import json
import warpcalc as w

v = float(sys.argv[1]) if len(sys.argv) > 1 else 3e7     # 0,1 c
R = float(sys.argv[2]) if len(sys.argv) > 2 else 100.0
s = float(sys.argv[3]) if len(sys.argv) > 3 else 0.08
x, y, z, h = w.grid(2.5 * R, 81)
ea = w.total_energy(w.alcubierre_rho_analytic(x, y, z, v, R, s), h)
en = w.total_energy(w.eulerian_energy_density(w.natario_shift(x, y, z, v, R, s, h), h), h)
print(json.dumps({
    "parametros": {"v_m_s": v, "radio_m": R, "sigma_1_m": s},
    "energia_alcubierre_J": ea, "masa_equivalente_alcubierre_kg": ea / w.metrics.C**2,
    "energia_natario_J": en,
    "grosor_pared_m": 1 / s,
    "cota_pfenning_ford_m": w.pfenning_ford_wall_bound(v / w.metrics.C),
    "conclusion": "energía negativa de orden astronómico y pared muy por encima de la cota cuántica: no realizable hoy",
}, indent=2, ensure_ascii=False))
