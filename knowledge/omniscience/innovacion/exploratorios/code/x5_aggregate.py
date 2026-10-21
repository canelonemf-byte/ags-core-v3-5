"""Agregación de los exploratorios X1–X4 y del exploratorio X5 (factor de escala con validación cruzada leave-one-out).
Código y figura originales."""
import json, numpy as np
from scipy.stats import spearmanr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
x1=json.load(open("out/x1_sigmaA.json"))["materiales"]; x2=json.load(open("out/x2_ferro_wells.json")); x3=json.load(open("out/x3_dos_overlap.json"))["solapamiento"]
cm=json.load(open("/workspace/omniscience_cmat001/results.json"))["por_material"]
# X1
ms=[m for m in x1 if x1[m]["error_rel_TO_CMAT001"] is not None]
r1=spearmanr([x1[m]["sigma_A_300K"] for m in ms],[abs(x1[m]["error_rel_TO_CMAT001"]) for m in ms])
# X2: Tc exp (K): PbTiO3 763, KNbO3 708, BaTiO3 393; SrTiO3 y KTaO3 no ferroeléctricos (0)
TC={"PbTiO3":763,"KNbO3":708,"BaTiO3":393,"SrTiO3":0,"KTaO3":0}; ps=list(TC)
r2=spearmanr([-x2[p]["dE_relajado_meV_fu"] for p in ps],[TC[p] for p in ps])
r2b=spearmanr([-x2[p]["dE_congelado_meV_fu"] for p in ps],[TC[p] for p in ps])
# X5: factor de escala global con LOO sobre los 4 materiales armónicos con referencia verificada
H=["Si","C","GaAs","MgO"]; ratio={m:cm[m]["omega_pred_cm"]/cm[m]["omega_exp_cm"] for m in H}
loo={}
for m in H:
    s=np.mean([ratio[k] for k in H if k!=m]); loo[m]=(cm[m]["omega_pred_cm"]/s-cm[m]["omega_exp_cm"])/cm[m]["omega_exp_cm"]
res={"X1_sigmaA":{"spearman_sigmaA_vs_abs_error_TO":{"rho":float(r1.statistic),"p":float(r1.pvalue),"n":len(ms),"materiales":ms},
      "nota":"Si DFT (Knoop et al. 2020, aiMD) = 0.15; MACE one-shot da 0.264 → sesgo alto o error del modelo armónico 2x2x2"},
     "X2_pozos":{"spearman_profundidad_relajada_vs_Tc":{"rho":float(r2.statistic),"p":float(r2.pvalue),"n":5},
      "spearman_profundidad_congelada_vs_Tc":{"rho":float(r2b.statistic),"p":float(r2b.pvalue),"n":5},"Tc_K":TC},
     "X3_dos_overlap_top5":sorted(x3.items(),key=lambda x:-x[1])[:5],
     "X5_escala_LOO":{"cociente_pred_exp":ratio,"error_LOO":loo,"n_dentro_10pct":int(sum(abs(v)<=0.10 for v in loo.values())),"max_abs_error":float(max(abs(v) for v in loo.values()))}}
json.dump(res,open("out/x5_agregado.json","w"),indent=1,ensure_ascii=False); print(json.dumps(res,indent=1,ensure_ascii=False))
fig,ax=plt.subplots(1,3,figsize=(14,4))
for m in ms: ax[0].scatter(x1[m]["sigma_A_300K"],100*abs(x1[m]["error_rel_TO_CMAT001"])); ax[0].annotate(m,(x1[m]["sigma_A_300K"],100*abs(x1[m]["error_rel_TO_CMAT001"])))
ax[0].set(xlabel="σᴬ(300 K) MACE-MP-0, one-shot",ylabel="|error TO Γ| C-MAT-001 (%)",yscale="log",title="X1 (exploratorio)")
for p in ps: ax[1].scatter(-x2[p]["dE_relajado_meV_fu"],TC[p]); ax[1].annotate(p,(-x2[p]["dE_relajado_meV_fu"],TC[p]))
ax[1].set(xscale="log",xlabel="−ΔE pozo relajado (meV/f.u.)",ylabel="Tc experimental (K); 0 = no FE",title="X2 (exploratorio)")
for p in ps: ax[2].plot(np.linspace(0,0.35,36),x2[p]["barrido_meV"],label=p)
ax[2].set(xlabel="amplitud modo blando Γ (Å, máx. por átomo)",ylabel="E − E_cúbica (meV/f.u.)",title="X2 barrido de fonón congelado"); ax[2].legend(fontsize=8)
fig.tight_layout(); fig.savefig("out/fig_exploratorios.png",dpi=120)
