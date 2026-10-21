"""INN-05: evaluación (criterios no evaluables por n<8 y sin DOS DFT) + figura descriptiva. Código original."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
r=json.load(open("out/inn05_raw.json")); D=np.load("out/dos_grid.npy"); g=D[0]; names=["Al","Co","Ru","TiN","Al2O3","Pb","C_control"]
res={"campana":"INN-05","n_pares_verificados":4,"n_requerido":8,
 "h_t1":{"resultado":"NO EVALUABLE (n=4<8) - cuenta como no superada"},"h_t2":{"resultado":"NO EVALUABLE (n=4<8) - cuenta como no superada"},
 "h_t3":{"resultado":"NO EVALUABLE (sin DOS DFT de PhononDB) - cuenta como no superada"},
 "controles":r["controles"],"control_identico_ok":abs(r["controles"]["Al|Al"]-1)<1e-6,"control_extremo_ok":r["controles"]["C|Pb"]<0.01,
 "descriptivo_pares":r["pares"],"materiales":r["materiales"],
 "observacion":"Con TBC experimental igual dentro del error (350 ± 60) para Al, Co y Ru sobre zafiro, O MACE vale 0.047, 0.112 y 0.013 (factor ~9): O por sí solo no explica la TBC medida. TiN|Al2O3 (TBC 700) tiene el O más alto (0.33). v_D de Ru (1044 m/s) parece anómalamente bajo frente al orden experimental: posible artefacto de MACE o de la estimación por pendientes; no verificado.",
 "desviaciones":[]}
json.dump(res,open("results.json","w"),indent=1,ensure_ascii=False); print(json.dumps(res["descriptivo_pares"],indent=1),res["controles"])
fig,ax=plt.subplots(1,2,figsize=(11,4))
for i,n in enumerate(names[:5]): ax[0].plot(g,D[i+1],label=n,lw=1)
ax[0].set(xlim=(0,30),xlabel="frecuencia (THz)",ylabel="DOS normalizada",title="INN-05: DOS fonónica MACE-MP-0"); ax[0].legend()
P=r["pares"]; ks=list(P)
ax[1].scatter([P[k]["solapamiento"] for k in ks],[P[k]["tbc_exp_MW_m2K"] for k in ks])
for k in ks: ax[1].annotate(k,(P[k]["solapamiento"],P[k]["tbc_exp_MW_m2K"]),fontsize=8,xytext=(3,3),textcoords="offset points")
ax[1].set(xlabel="solapamiento O (MACE)",ylabel="TBC experimental (MW m⁻² K⁻¹)",title="descriptivo, n=4 (no evaluable)")
fig.tight_layout(); fig.savefig("figs/inn05_dos_y_tbc.png",dpi=130)
