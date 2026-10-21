"""INN-01: análisis suplementario NO pre-registrado (informativo). Código original."""
import json, numpy as np
from scipy.stats import spearmanr
r=json.load(open("out/inn01_raw.json"))
OS={"AgBr_ZB":0.68,"AgI_ZB":0.41,"CuCl_ZB":0.55,"CuBr_ZB":0.52,"CuI_ZB":0.37,"AgCl_RS":0.50,"AgBr_RS":0.48,"AgI_RS":0.52,"NaBr_RS":0.40}
MD={"AgBr_ZB":2.64,"AgI_ZB":0.80,"CuCl_ZB":1.90,"CuBr_ZB":2.78,"CuI_ZB":0.41,"AgCl_RS":0.85,"AgBr_RS":0.75,"AgI_RS":0.62}
ok=[m for m in OS if r[m]["estable"]]
def rho(ref,ms): ms=[m for m in ms if m in ref]; return {"n":len(ms),"rho":float(spearmanr([r[m]["sigma_a_3x3x3"] for m in ms],[ref[m] for m in ms]).statistic)}
x=np.array([r[m]["sigma_a_3x3x3"] for m in ok]); y=np.array([OS[m] for m in ok])
out={"nota":"no pre-registrado; solo informativo",
 "rho_vs_one_shot_n8":rho(OS,ok),"rho_vs_aimd_texto_original_H-A1":rho(MD,ok),
 "rho_vs_one_shot_2x2x2":{"rho":float(spearmanr([r[m]["sigma_a_2x2x2"] for m in ok],y).statistic)},
 "sesgo_abs_medio_n8":float(np.mean(np.abs(x-y))),"sesgo_firmado_medio_n8":float(np.mean(x-y)),
 "frac_dentro_0.05":float(np.mean(np.abs(x-y)<=0.05)),
 "compuerta_0.30_todos_marcados":bool(all(r[m]["sigma_a_3x3x3"]>=0.30 for m in ok)),
 "si_control":{"mace":r["Si_control"]["sigma_a_3x3x3"],"ref":0.15}}
json.dump(out,open("out/inn01_suplementario.json","w"),indent=1,ensure_ascii=False); print(json.dumps(out,indent=1))
