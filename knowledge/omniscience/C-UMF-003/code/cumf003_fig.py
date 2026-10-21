"""Figura original C-UMF-003. Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = json.load(open("/workspace/omniscience_cumf003/results.json")); f, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
d = R["dE_AR_meV_at"]["run1"]; ms = list(d); a1.bar(ms, [d[m] for m in ms], color="tab:blue"); a1.axhspan(-1, 19, color="tab:green", alpha=.2, label="exp ±10")
a1.axhline(9.0, color="k", ls="--", label="exp +9.0"); a1.axhline(0, color="gray"); a1.set_ylabel("E(anatasa)−E(rutilo) [meV/átomo]"); a1.legend(); a1.set_title("A: orden de polimorfos TiO2")
b = R["dV_rel"]["run1"]; mats = list(b["ms"]); x = range(len(mats))
a2.bar([i - .2 for i in x], [100 * b["ms"][m] for m in mats], .4, label="MatterSim"); a2.bar([i + .2 for i in x], [100 * b["ms_d3"][m] for m in mats], .4, label="MatterSim+D3(BJ)")
a2.axhspan(-5, 5, color="tab:green", alpha=.15); a2.set_xticks(list(x)); a2.set_xticklabels(mats, rotation=45); a2.set_ylabel("ΔV/V_exp [%]"); a2.legend(); a2.set_title("B: volúmenes")
f.tight_layout(); [f.savefig(f"/workspace/omniscience_cumf003/figs/fig_cumf003.{e}", dpi=150) for e in ("png", "svg")]
