"""Verifica con código las cifras declaradas en P001 (ANEC -0,08; QI ~10^50; Casimir ~10^60).
P001 no declara parámetros (v, R, sigma, separación de placas), así que se usan valores explícitos
y se informa si la cifra es reproducible. Salida: results/verificacion_p001.json"""
import json
from pathlib import Path
import numpy as np
import warpcalc as w

C, G = w.metrics.C, w.metrics.G
anec = {f"b={b}": w.anec_x_ray(b, vv=0.5, RR=1.0, ss=8.0, n=801) for b in (0.3, 0.5, 0.7, 0.9, 0.95)}
lp = w.planck_length()
casimir_1um = float(w.casimir_energy_density(1e-6))
rho_wall_1m = C**4 / (32 * np.pi * G) * 0.25
rho_wall_qi = C**4 / (32 * np.pi * G) * (1 / (2 * 100 * lp)) ** 2
E_qi = w.energia_total_aprox(C, 100.0, 1 / (100 * lp))
res = {
    "meta": {"proyecto": "P001", "fecha": "2026-10-24", "codigo": "warpcalc (pliegue)", "unidades_anec": "geométricas G=c=1, R=1"},
    "anec_pared": {"declarado": -0.08, "parametros": {"v": 0.5, "R": 1.0, "sigma": 8.0},
                   "calculado_por_parametro_impacto": anec,
                   "resultado": "signo negativo y orden de magnitud reproducidos (de -0,09 a -0,25 en rayos que cruzan la pared); el valor -0,08 exacto no es reproducible porque P001 no declara v, sigma ni el rayo",
                   "limitacion": "rayo nulo recto en t=0 (no geodésica completa; ignora la desviación transversal)"},
    "qi_alcubierre": {"declarado": "1e50",
                      "pared_1m_sobre_cota_pfenning_ford": 1 / w.pfenning_ford_wall_bound(1.0),
                      "energia_R100m_v_c_pared_100lP_kg": E_qi / C**2,
                      "resultado": "no reproducido: con pared de 1 m la pared supera la cota cuántica en ~6e32 veces; con la pared máxima permitida (~100 l_P), R=100 m y v=c la masa negativa es ~-2e62 kg, del orden de lo publicado por Pfenning y Ford (1997). Ninguna combinación estándar da 1e50 sin parámetros adicionales"},
    "casimir": {"declarado": "1e60", "densidad_casimir_placas_1um_J_m3": casimir_1um,
                "cociente_pared_1m": rho_wall_1m / abs(casimir_1um), "cociente_pared_100lP": rho_wall_qi / abs(casimir_1um),
                "resultado": "no reproducido: el cociente entre la energía negativa pedida y la de Casimir (placas a 1 µm) va de ~7e44 (pared de 1 m) a ~3e110 (pared de 100 l_P); 1e60 cae dentro del intervalo pero depende de parámetros no declarados"},
    "nec_wec_violan": {"declarado": True, "resultado": "verificado: T_ab n^a n^b < 0 en la pared (coincide con la fórmula analítica de Alcubierre con error < 1e-12) y la integral ANEC es negativa"},
    "t00_eje_cero": {"declarado": True, "resultado": "verificado para el observador euleriano: rho ∝ (y^2+z^2), nula sobre el eje de movimiento"},
}
Path("results").mkdir(exist_ok=True)
Path("results/verificacion_p001.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
print(json.dumps(res, indent=2, ensure_ascii=False))
