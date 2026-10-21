"""C-MAT-005: compara veredictos y controles entre run1 y run2 (parte de H-REP). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json
a, b = json.load(open("results.json")), json.load(open("results_replica_run2.json"))
va = {k: v["veredicto"] for k, v in a["hipotesis"].items() if k != "H-REP"}; vb = {k: v["veredicto"] for k, v in b["hipotesis"].items() if k != "H-REP"}
ca = {k: a["controles"][k]["pasa"] for k in ("C1", "C2")}; cb = {k: b["controles"][k]["pasa"] for k in ("C1", "C2")}
out = {"veredictos_run1": va, "veredictos_run2": vb, "veredictos_iguales": va == vb, "controles_iguales": ca == cb,
       "H-REP_numerico": a["hipotesis"]["H-REP"]["veredicto"], "replica": a["replica"]}
out["H-REP_final"] = "PASA" if out["H-REP_numerico"] == "PASA" and out["veredictos_iguales"] and out["controles_iguales"] else "FALSADA"
json.dump(out, open("diff_runs.json", "w"), indent=1, ensure_ascii=False); print(json.dumps({k: out[k] for k in ("veredictos_iguales", "controles_iguales", "H-REP_numerico", "H-REP_final")}))
