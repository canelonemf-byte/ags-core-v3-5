"""C-MAT-001: evaluación de criterios pre-registrados (prereg sha256 efb5f872...ea90).
Aplica H-MAT-1/2/3 exactamente como están congelados. Sin aleatoriedad."""
import json, hashlib, sys, platform, subprocess, datetime, glob, os
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = "/workspace/omniscience_cmat001"; OUT = f"{ROOT}/out"
CM_PER_THZ = 1/0.0299792458
MATS = ["Si","C","GaAs","MgO","NaCl","PbTe","SnSe","SrTiO3","BaTiO3"]
EXPECT_STABLE = {m: True for m in MATS[:7]} | {"SrTiO3": False, "BaTiO3": False}
NEG_CONTROLS = ["SrTiO3","BaTiO3"]
FREQ_SET = ["Si","C","GaAs","MgO","NaCl","PbTe"]
REF_CM = {"Si":520.2,"C":1332.0,"GaAs":269.0,"MgO":396.0,"NaCl":None,"PbTe":18.0}
REF_SRC = {"Si":"Parker, Feldman, Ashkin, Phys. Rev. 155, 712 (1967), 300 K",
 "C":"Solin & Ramdas, Phys. Rev. B 1, 1687 (1970), T amb.",
 "GaAs":"Holtz, Zallen, Brafman, Phys. Rev. B 38, 6097 (1988), TO, T amb.",
 "MgO":"Komandin et al., Phys. Solid State 51 (2009) doi:10.1134/S1063783409100096, TO, 300 K",
 "NaCl":"no verificado (primaria Raunio et al. Phys. Rev. 178, 1496); 164 cm-1 compilación secundaria",
 "PbTe":"Kinch & Buss, Solid State Commun. 11 (1972) doi:10.1016/0038-1098(72)90241-4, TO, baja T"}
REF_SECONDARY_CM = {"NaCl":164.0}
CONFIGS = ["base_2x2x2_d0.01","sc_3x3x3_d0.01","disp_2x2x2_d0.03"]
sha = lambda p: hashlib.sha256(open(p,"rb").read()).hexdigest()

data = {m: json.load(open(f"{OUT}/{m}.json")) for m in MATS}
per = {}
for m in MATS:
    c = data[m]["configs"]
    verdicts = {k: bool(c[k]["stable"]) for k in CONFIGS}
    fmins = {k: c[k]["min_freq_mesh_THz"] for k in CONFIGS}
    consistent = len(set(verdicts.values())) == 1
    base = verdicts["base_2x2x2_d0.01"]
    status = ("estable" if base else "inestable") if consistent else "inconcluso"
    correct = consistent and (base == EXPECT_STABLE[m])
    row = dict(esperado="estable" if EXPECT_STABLE[m] else "inestable", veredicto=status,
               fmin_THz=fmins, veredicto_por_config=verdicts, H3_consistente=consistent,
               clasificacion_correcta=correct, a_relajada_A=data[m]["relax"]["cell_lengths_A"],
               relax_convergida=data[m]["relax"]["converged"])
    if m in FREQ_SET:
        pred = c["base_2x2x2_d0.01"]["gamma_optical_mean_THz"]
        row["omega_pred_THz"] = pred; row["omega_pred_cm"] = pred*CM_PER_THZ
        row["omega_pred_conv_THz"] = {k: c[k]["gamma_optical_mean_THz"] for k in CONFIGS}
        ref = REF_CM[m]; row["ref_fuente"] = REF_SRC[m]
        if ref is not None:
            row["omega_exp_cm"] = ref; row["omega_exp_THz"] = ref/CM_PER_THZ
            row["error_rel"] = (pred*CM_PER_THZ - ref)/ref; row["H2_pasa"] = abs(row["error_rel"]) <= 0.10
        else:
            row["omega_exp_cm"] = None; row["error_rel"] = None; row["H2_pasa"] = False
            row["H2_nota"] = "referencia no verificada: cuenta como no superado (enmienda 8)"
            s = REF_SECONDARY_CM[m]; row["analisis_secundario"] = dict(omega_exp_cm=s,
                error_rel=(pred*CM_PER_THZ - s)/s, pasaria=abs((pred*CM_PER_THZ - s)/s) <= 0.10)
    per[m] = row

n_corr = sum(per[m]["clasificacion_correcta"] for m in MATS)
neg_ok = all(per[m]["clasificacion_correcta"] for m in NEG_CONTROLS)
H1 = dict(regla="clasificación correcta >= 8/9 y ambos controles negativos correctos; inconclusos cuentan como incorrectos",
          correctos=n_corr, total=9, controles_negativos_ok=neg_ok, resultado="PASA" if (n_corr >= 8 and neg_ok) else "FALSADA")
n2 = sum(per[m]["H2_pasa"] for m in FREQ_SET)
H2 = dict(regla="|w_pred-w_exp|/w_exp <= 10% en >= 5/6 (TO sin NAC)", pasan=n2, total=6,
          resultado="PASA" if n2 >= 5 else "FALSADA")
incon = [m for m in MATS if not per[m]["H3_consistente"]]
H3 = dict(regla="veredicto invariante 2x2x2 vs 3x3x3 y 0.01 vs 0.03 A", inconclusos=incon,
          resultado="PASA" if not incon else f"PARCIAL ({len(incon)} inconclusos)")
# Sensibilidad (no pre-registrada): SnSe relajó a fase de mayor simetría
from ase.io import read; import spglib
sg = {}
for m in MATS:
    a = read(f"{OUT}/{m}_relaxed.vasp"); sg[m] = spglib.get_spacegroup((a.cell[:], a.get_scaled_positions(), a.numbers), 1e-3)
sens = dict(descripcion="SnSe: la relajación con FixSymmetry(Pnma) convergió a una estructura Fm-3m (tipo NaCl); el veredicto 'estable' no corresponde a la fase Pnma experimental. Si SnSe se contase como incorrecto:",
            correctos=n_corr - (1 if per["SnSe"]["clasificacion_correcta"] else 0),
            resultado_H1="PASA" if (n_corr-1 >= 8 and neg_ok) else "FALSADA")
harm = [per[m]["error_rel"] for m in ["Si","C","GaAs","MgO"]]
explor = dict(nota="exploratorio, NO pre-registrado", error_medio_firmado_Si_C_GaAs_MgO=float(np.mean(harm)),
              interpretacion="ablandamiento sistemático de MACE-MP-0 (cf. Deng et al., npj Comput. Mater. 2025, doi:10.1038/s41524-024-01500-6)")
res = dict(campana="C-MAT-001", prereg_sha256=sha(f"{ROOT}/prereg_C-MAT-001.FROZEN.md"),
           modelo="MACE-MP-0 medium (2023-12-03, 128L1 epoch199), float64, CPU", tolerancia_THz=-0.3,
           por_material=per, grupos_espaciales_relajados=sg, H_MAT_1=H1, H_MAT_2=H2, H_MAT_3=H3,
           sensibilidad_no_prereg=sens, exploratorio=explor,
           desviaciones=["Ninguna desviación de criterios. Observación: SnSe relajó a Fm-3m (ver sensibilidad).",
                         "NAC no aplicado (sin cargas de Born), según protocolo: se compara TO."],
           generado=datetime.datetime.now().astimezone().isoformat(timespec="seconds"))
json.dump(res, open(f"{ROOT}/results.json","w"), indent=1, ensure_ascii=False, default=float)

# figura
fig, ax = plt.subplots(1,2, figsize=(11,4.2))
ms = [m for m in FREQ_SET]
pred = [per[m]["omega_pred_cm"] for m in ms]
exp = [per[m]["omega_exp_cm"] or REF_SECONDARY_CM.get(m) for m in ms]
ax[0].loglog(exp, pred, "o"); lim=[10,2000]; ax[0].plot(lim,lim,"k--",lw=.8)
ax[0].fill_between(lim,[0.9*l for l in lim],[1.1*l for l in lim],color="g",alpha=.15,label="±10%")
for m,x,y in zip(ms,exp,pred): ax[0].annotate(m+("*" if m=="NaCl" else ""),(x,y),xytext=(4,-10),textcoords="offset points")
ax[0].set_xlabel("ω_exp TO Γ (cm⁻¹)"); ax[0].set_ylabel("ω_pred MACE-MP-0 (cm⁻¹)"); ax[0].legend(); ax[0].set_title("H-MAT-2 (*NaCl: ref. secundaria, no evaluada)")
fm = [per[m]["fmin_THz"]["base_2x2x2_d0.01"] for m in MATS]
ax[1].bar(MATS, fm, color=["tab:blue" if EXPECT_STABLE[m] else "tab:red" for m in MATS]); ax[1].axhline(-0.3,color="k",ls="--",lw=.8)
ax[1].set_ylabel("f_min malla 20³ (THz)"); ax[1].set_title("H-MAT-1 (rojo = control negativo)"); ax[1].tick_params(axis="x",rotation=45)
fig.tight_layout(); fig.savefig(f"{ROOT}/fig_resumen_HMAT.png", dpi=130)

# provenance
pf = subprocess.run([f"{ROOT}/.venv/bin/pip","freeze"],capture_output=True,text=True).stdout
open(f"{ROOT}/requirements.lock","w").write(pf)
import torch, ase, phonopy, mace
ck = "/home/box/.cache/mace/20231203mace128L1_epoch199model"
prov = dict(campana="C-MAT-001", fecha=res["generado"], python=sys.version, plataforma=platform.platform(),
            versiones=dict(torch=torch.__version__, ase=ase.__version__, phonopy=phonopy.__version__, mace_torch=getattr(mace,"__version__","0.3.16"), spglib=spglib.__version__, numpy=np.__version__),
            checkpoint=dict(ruta=ck, sha256=sha(ck), nombre="MACE-MP-0 medium 2023-12-03"),
            fallback_CHGNet_usado=False, semillas="no aplica: relajación BFGS y desplazamientos Phonopy deterministas; estructuras iniciales con parámetros experimentales",
            prereg=dict(ruta="prereg_C-MAT-001.FROZEN.md", sha256=res["prereg_sha256"], congelado="2026-10-18 21:16 UTC+2"),
            scripts={os.path.basename(p): sha(p) for p in glob.glob(f"{ROOT}/code/*.py")},
            requirements_lock_sha256=sha(f"{ROOT}/requirements.lock"),
            salidas={os.path.relpath(p,ROOT): sha(p) for p in sorted(glob.glob(f"{OUT}/*"))+[f"{ROOT}/results.json", f"{ROOT}/fig_resumen_HMAT.png", f"{ROOT}/run.log"]})
json.dump(prov, open(f"{ROOT}/provenance_C-MAT-001.json","w"), indent=1, ensure_ascii=False)
print(json.dumps(dict(H1=H1,H2=H2,H3=H3,sens=sens,explor=explor,sg=sg),indent=1,ensure_ascii=False))
for m in MATS:
    r=per[m]; print(m, r["veredicto"], r["clasificacion_correcta"], round(r["fmin_THz"]["base_2x2x2_d0.01"],3),
      round(r.get("omega_pred_cm",0),1), r.get("omega_exp_cm"), None if r.get("error_rel") is None else round(100*r["error_rel"],1), r.get("analisis_secundario"))
