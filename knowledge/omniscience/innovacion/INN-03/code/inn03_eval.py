"""INN-03: evaluación de criterios congelados (H-F1, H-F2, controles). Código original."""
import json, numpy as np
from scipy.stats import spearmanr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
r=json.load(open("out/inn03_raw.json"))
TC={"BiFeO3":1098,"CsGeCl3":428,"CsGeBr3":511,"CsGeI3":550,"PbZrO3":0,"PbHfO3":0,"CaTiO3":0,"BaZrO3":0,"SrZrO3":0,"BaSnO3":0}
ms=list(TC); n=len([m for m in ms if m in r])
rho=spearmanr([-r[m]["de_relajado_meV_fu"] for m in ms],[TC[m] for m in ms])
pred={m:abs(r[m]["de_relajado_meV_fu"])>=10 for m in ms}; true={m:TC[m]>0 for m in ms}
acc=sum(pred[m]==true[m] for m in ms)/len(ms)
ctrl={m:not pred[m] for m in ["BaZrO3","CaTiO3"]}
h1="PASA" if (n>=8 and rho.statistic>=0.7) else "FALSADA"
h2="PASA" if acc>=0.8 else "FALSADA"
glob="FALSADA" if (h1=="FALSADA" or h2=="FALSADA" or not all(ctrl.values())) else "PASA"
tabla={m:{"tc_exp_K":TC[m],"de_relajado_meV_fu":r[m]["de_relajado_meV_fu"],"de_congelado_meV_fu":r[m]["de_congelado_meV_fu"],
          "pred_fe":pred[m],"fe_real":true[m],"acierto":pred[m]==true[m],"grupo_relajado":r[m]["grupo_relajado"],
          "f_opt_min_gamma_2x2x2_THz":r[m]["f_opt_min_gamma_2x2x2_THz"],"f_opt_min_gamma_3x3x3_THz":r[m]["f_opt_min_gamma_3x3x3_THz"],"a_cubica_A":r[m]["a_cubica_A"]} for m in ms}
# sensibilidad no pre-registrada: profundidad congelada en lugar de relajada
rho_c=spearmanr([-r[m]["de_congelado_meV_fu"] for m in ms],[TC[m] for m in ms])
res={"campana":"INN-03","n":n,"h_f1":{"rho_spearman":float(rho.statistic),"p":float(rho.pvalue),"umbral":0.7,"resultado":h1},
     "h_f2":{"aciertos":int(sum(pred[m]==true[m] for m in ms)),"total":len(ms),"exactitud":acc,"umbral":0.8,"resultado":h2},
     "controles_negativos":{"BaZrO3_bajo_umbral":ctrl["BaZrO3"],"CaTiO3_bajo_umbral":ctrl["CaTiO3"]},"veredicto_global":glob,
     "por_material":tabla,"sensibilidad_no_prereg":{"rho_profundidad_congelada":float(rho_c.statistic)},"desviaciones":[]}
json.dump(res,open("results.json","w"),indent=1,ensure_ascii=False); print(json.dumps({k:v for k,v in res.items() if k!="por_material"},indent=1,ensure_ascii=False))
for m in ms: t=tabla[m]; print(m,t["tc_exp_K"],round(t["de_relajado_meV_fu"],2),t["pred_fe"],t["acierto"],t["grupo_relajado"],round(t["f_opt_min_gamma_2x2x2_THz"],3),round(t["f_opt_min_gamma_3x3x3_THz"],3))
fig,ax=plt.subplots(figsize=(6,4.3))
for m in ms:
    x=max(abs(r[m]["de_relajado_meV_fu"]),1e-3); ax.scatter(x,TC[m],c="tab:red" if TC[m]>0 else "tab:blue"); ax.annotate(m,(x,TC[m]),fontsize=7,xytext=(3,3),textcoords="offset points")
ax.axvline(10,ls="--",c="k",lw=.8); ax.set(xscale="log",xlabel="|ΔE pozo relajado| MACE-MP-0 (meV/f.u.)",ylabel="Tc experimental (K); 0 = sin fase FE",title=f"INN-03: ρ={rho.statistic:.2f}, exactitud={acc:.0%}")
fig.tight_layout(); fig.savefig("figs/inn03_pozos_vs_tc.png",dpi=130)
