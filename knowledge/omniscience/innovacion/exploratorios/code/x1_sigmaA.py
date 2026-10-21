"""Exploratorio X1 (no pre-registrado como confirmatorio): medida de anarmonicidad sigma^A (muestreo
armónico 'one-shot' a 300 K) con MACE-MP-0 sobre las constantes de fuerza de C-MAT-001. Código original."""
import json, numpy as np, phonopy
from ase import Atoms
from mace.calculators import mace_mp
SRC = "/workspace/omniscience_cmat001/out"; MATS = ["Si","C","GaAs","MgO","NaCl","PbTe"]
SEED, NSNAP, T = 20261018, 24, 300.0
calc = mace_mp(model="medium", default_dtype="float64", device="cpu")
res = {"semilla": SEED, "n_snapshots": NSNAP, "T_K": T, "materiales": {}}
rng = np.random.default_rng(SEED)
for m in MATS:
    ph = phonopy.load(f"{SRC}/{m}_phonopy_base.yaml", produce_fc=True, is_compact_fc=False, log_level=0)
    fc = ph.force_constants  # (N,N,3,3)
    ph.generate_displacements(number_of_snapshots=NSNAP, random_seed=SEED, temperature=T)
    U = ph.displacements; num = []; den = []
    for sc, u in zip(ph.supercells_with_displacements, U):
        at = Atoms(sc.symbols, cell=sc.cell, scaled_positions=sc.scaled_positions, pbc=True); at.calc = calc
        F = at.get_forces(); F -= F.mean(0)
        Fh = -np.einsum("ijab,jb->ia", fc, u)
        num.append(((F - Fh)**2).sum()); den.append((F**2).sum())
    num, den = np.array(num), np.array(den)
    s = float(np.sqrt(num.sum()/den.sum()))
    boot = [np.sqrt(num[i].sum()/den[i].sum()) for i in (rng.integers(0, NSNAP, NSNAP) for _ in range(2000))]
    rms_u = float(np.sqrt((U**2).sum(-1).mean()))
    res["materiales"][m] = {"sigma_A_300K": s, "IC95": [float(np.percentile(boot,2.5)), float(np.percentile(boot,97.5))], "rms_desplazamiento_A": rms_u}
    print(m, round(s,3), np.round(res["materiales"][m]["IC95"],3), round(rms_u,3), flush=True)
cm = json.load(open("/workspace/omniscience_cmat001/results.json"))["por_material"]
for m in MATS: res["materiales"][m]["error_rel_TO_CMAT001"] = cm[m].get("error_rel")
json.dump(res, open("out/x1_sigmaA.json","w"), indent=1)
