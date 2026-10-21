"""Figura C-MAT-007 (original). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = json.load(open("results.json"))["run1"]["filas"]; ok = {m: r for m, r in d.items() if "S298" in r}
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
for k, a, t in (("S298", ax[0], "S(298 K)"), ("Cp298", ax[1], "Cv arm. vs Cp(298 K)")):
    for nuevo, c in ((False, "tab:blue"), (True, "tab:red")):
        x = [r[k]["ref"] for r in ok.values() if bool(r.get("nuevo")) == nuevo]; y = [r[k]["calc"] for r in ok.values() if bool(r.get("nuevo")) == nuevo]
        a.scatter(x, y, s=18, c=c, label="nuevos (13)" if nuevo else "C-MAT-006 (31)")
    lim = [0, max(r[k]["ref"] for r in ok.values()) * 1.1]; a.plot(lim, lim, "k-", lw=.8); a.plot(lim, [1.1 * v for v in lim], "k:", lw=.6); a.plot(lim, [.9 * v for v in lim], "k:", lw=.6)
    a.set_xlabel(f"NIST-JANAF {t} [J/(K·mol)]"); a.set_ylabel(f"MatterSim @V_exp {t}"); a.legend(fontsize=8)
fig.suptitle("C-MAT-007 · 44 sólidos · líneas ±10 % · L. López Paz con asistencia de IA · CC BY 4.0", fontsize=9); fig.tight_layout(); fig.savefig("figs/C-MAT-007_resumen.png", dpi=130)
