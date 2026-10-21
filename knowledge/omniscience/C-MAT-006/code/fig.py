import json,matplotlib;matplotlib.use("Agg");import matplotlib.pyplot as plt
r=json.load(open("results.json"))["run1"]
fig,ax=plt.subplots(figsize=(9,4))
for i,(mod,c) in enumerate([("mattersim","C0"),("mace","C3")]):
    d={k:v for k,v in r[mod].items() if isinstance(v,dict) and v.get("err298") is not None}
    ks=sorted(d);ax.bar([j+0.4*i for j in range(len(ks))],[100*d[k]["err298"] for k in ks],0.4,color=c,label=mod)
ax.set_xticks([j+0.2 for j in range(len(ks))]);ax.set_xticklabels(ks,rotation=90,fontsize=7)
ax.axhline(10,ls="--",c="k");ax.axhline(-10,ls="--",c="k");ax.set_ylabel("error S298 vs JANAF (%)");ax.legend()
ax.set_title("C-MAT-006: V_exp, regla R0-R4");fig.tight_layout();fig.savefig("figs/err_S298.png",dpi=130)
