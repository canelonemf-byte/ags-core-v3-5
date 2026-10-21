"""INN-01: evaluación de criterios congelados (H-A1, H-A2; H-A3 no evaluable). Código original."""
import json, os, numpy as np
from scipy.stats import spearmanr
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
r=json.load(open("out/inn01_raw.json"))
REF={"AgBr_ZB":0.68,"AgI_ZB":0.41,"CuCl_ZB":0.55,"CuBr_ZB":0.52,"CuI_ZB":0.37,"AgCl_RS":0.50,"AgBr_RS":0.48,"AgI_RS":0.52,"NaBr_RS":0.40}
ok=[m for m in REF if m in r and r[m]["estable"]]; excl=[m for m in REF if m in r and not r[m]["estable"]]
x=np.array([r[m]["sigma_a_3x3x3"] for m in ok]); y=np.array([REF[m] for m in ok]); n=len(ok)
rho=spearmanr(x,y).statistic if n>=3 else float("nan")
rng=np.random.default_rng(20261018); bs=[]
for _ in range(5000):
    i=rng.integers(0,n,n)
    if len(set(i))>2: bs.append(spearmanr(x[i],y[i]).statistic)
bs=np.array([b for b in bs if np.isfinite(b)]); ci=[float(np.percentile(bs,2.5)),float(np.percentile(bs,97.5))] if len(bs) else [None,None]
bias=float(np.mean(np.abs(x-y))) if n else None; sbias=float(np.mean(x-y)) if n else None
h1_enm="PASA" if (n>=9 and rho>=0.8 and ci[0] is not None and ci[0]>0) else ("NO EVALUABLE" if n<9 else "FALSADA")
h1_orig="NO EVALUABLE (n<10)" if n<10 else ("PASA" if (rho>=0.8 and ci[0]>0) else "FALSADA")
h2_enm=("PASA" if bias<=0.05 else "FALSADA") if n>=9 else "NO EVALUABLE"
h2_orig="NO EVALUABLE (n<10)" if n<10 else ("PASA" if bias<=0.05 else "FALSADA")
md={m:json.load(open(f"out/{m}_md.json")) for m in ["CuI_ZB","AgCl_RS"] if os.path.exists(f"out/{m}_md.json")}
res={"campana":"INN-01","n_evaluados":n,"excluidos_inestables":excl,
 "h_a1":{"rho_spearman":float(rho),"ic95_bootstrap":ci,"umbral":0.8,"resultado_criterio_enmendado_n9":h1_enm,"resultado_criterio_original_n10":h1_orig},
 "h_a2":{"sesgo_abs_medio":bias,"sesgo_firmado_medio":sbias,"umbral":0.05,"resultado_criterio_enmendado_n9":h2_enm,"resultado_criterio_original_n10":h2_orig},
 "h_a3":{"resultado":"NO EVALUABLE (enmienda A5) - cuenta como no superada"},
 "por_material":{m:dict(r[m],sigma_a_ref=REF.get(m,0.15 if m=="Si_control" else None)) for m in r},
 "controles":{"si_control":{"sigma_a_mace":r.get("Si_control",{}).get("sigma_a_3x3x3"),"ref_dft_aimd":0.15},
   "trivial_max":max(r[m].get("control_trivial",0) for m in r),
   "sensibilidad_2x2x2_vs_3x3x3_max_abs":float(max(abs(r[m]["sigma_a_2x2x2"]-r[m]["sigma_a_3x3x3"]) for m in r if r[m]["estable"])),
   "md":{m:{"sigma_a_md":md[m]["sigma_a_md"],"sigma_a_muestreo":r[m]["sigma_a_3x3x3"]} for m in md}},
 "desviaciones":[]}
json.dump(res,open("results.json","w"),indent=1,ensure_ascii=False); print(json.dumps({k:v for k,v in res.items() if k!="por_material"},indent=1,ensure_ascii=False))
for m in r: print(m, r[m]["estable"], round(r[m].get("sigma_a_3x3x3",float("nan")),3), REF.get(m), round(r[m]["fmin_malla_3x3x3_THz"],3))
fig,ax=plt.subplots(figsize=(5.5,4.5))
ax.scatter(y,x); [ax.annotate(m,(REF[m],r[m]["sigma_a_3x3x3"]),fontsize=7,xytext=(3,3),textcoords="offset points") for m in ok]
l=[0.1,0.9]; ax.plot(l,l,"k--",lw=.8); ax.fill_between(l,[v-0.05 for v in l],[v+0.05 for v in l],alpha=.15,color="g",label="±0.05 (H-A2)")
ax.set(xlabel="σᴬ DFT (Knoop et al. 2020)",ylabel="σᴬ MACE-MP-0 (muestreo clásico, FC 3×3×3)",title=f"INN-01: ρ={rho:.2f}, n={n}"); ax.legend()
fig.tight_layout(); fig.savefig("figs/inn01_sigmaA_vs_dft.png",dpi=130)
