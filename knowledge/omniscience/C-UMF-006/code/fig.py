"""Figura C-UMF-006 (original). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = json.load(open("results.json")); k = ["ZPE_eV_at", "U_vib_eV_at", "F_vib_eV_at"]; x = range(3)
fig, ax = plt.subplots(figsize=(6, 4)); ax.bar([i - .2 for i in x], [R["dvib_ms"][c] for c in k], .4, label="MatterSim"); ax.bar([i + .2 for i in x], [R["dvib_mace"][c] for c in k], .4, label="MACE")
ax.axhline(-47.9, ls=":", c="r", label="C-UMF-004 ΔH_vib (con imaginarios)"); ax.set_xticks(list(x)); ax.set_xticklabels(["ΔZPE", "ΔU_vib(298)", "ΔF_vib(298)"]); ax.set_ylabel("anatasa − rutilo [meV/át]"); ax.legend(fontsize=8)
ax.set_title("C-UMF-006 parte B · V_exp + regla R0–R4 · L. López Paz con asistencia de IA · CC BY 4.0", fontsize=8); fig.tight_layout(); fig.savefig("figs/C-UMF-006_vib.png", dpi=130)
