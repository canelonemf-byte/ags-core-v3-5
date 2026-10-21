"""Exploratorio X3: solapamiento de DOS fonónica normalizada (heurística de acoplamiento térmico en interfaces)
a partir de los resultados MACE-MP-0 de C-MAT-001. Código original."""
import json, itertools, numpy as np, phonopy
SRC="/workspace/omniscience_cmat001/out"; MATS=["Si","C","GaAs","MgO","NaCl","PbTe"]
grid=np.linspace(0,40,4001); D={}
for m in MATS:
    ph=phonopy.load(f"{SRC}/{m}_phonopy_base.yaml",produce_fc=True,log_level=0)
    ph.run_mesh([20,20,20],is_gamma_center=True); ph.run_total_dos(freq_pitch=0.01, sigma=0.1)
    d=ph.get_total_dos_dict(); g=np.interp(grid,d["frequency_points"],d["total_dos"],left=0,right=0); g=np.clip(g,0,None); D[m]=g/np.trapezoid(g,grid)
out={}
for a,b in itertools.combinations(MATS,2):
    o=float(np.trapezoid(np.minimum(D[a],D[b]),grid)); out[f"{a}|{b}"]=o
for k,v in sorted(out.items(),key=lambda x:-x[1]): print(k,round(v,3))
json.dump({"solapamiento":out,"nota":"sigma=0.1 THz, malla 20^3, DOS normalizada a 1; sin corrección de ablandamiento"},open("out/x3_dos_overlap.json","w"),indent=1)
