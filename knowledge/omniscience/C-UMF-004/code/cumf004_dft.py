#!/usr/bin/env python3
"""C-UMF-004 parte A: relajación PBE (celda+posiciones) y energías PBE/r2SCAN/HSE06 en la geometría relajada.
Uso: mpiexec -n N python cumf004_dft.py --etapa {relax,sp} --met {PBE,R2SCAN,HSE06} --mat {rutilo,anatasa} --out DIR [--k normal|reducido] [--ecut 600]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, sys, time
from ase.io import read, write
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from gpaw import GPAW, PW, FermiDirac
from gpaw.mpi import world
ap = argparse.ArgumentParser()
for k in ("etapa", "met", "mat", "out"): ap.add_argument("--" + k)
ap.add_argument("--k", default="normal"); ap.add_argument("--ecut", type=float, default=600); A = ap.parse_args()
def estructura(m):
    from ase.spacegroup import crystal
    if m == "rutilo": return crystal(["Ti", "O"], basis=[(0, 0, 0), (0.3048, 0.3048, 0)], spacegroup=136, cellpar=[4.594, 4.594, 2.959, 90, 90, 90])
    return crystal(["Ti", "O"], basis=[(0, 0, 0), (0, 0, 0.2081)], spacegroup=141, setting=1, cellpar=[3.785, 3.785, 9.514, 90, 90, 90], primitive_cell=True)
K = {"normal": {"rutilo": (5, 5, 8), "anatasa": (6, 6, 6)}, "reducido": {"rutilo": (3, 3, 4), "anatasa": (3, 3, 3)}}[A.k][A.mat]
os.makedirs(A.out, exist_ok=True); geo = os.path.join(A.out, f"relax_{A.mat}.traj")
def calc(xc, tag):
    kw = dict(mode=PW(A.ecut), kpts={"size": K, "gamma": True}, maxiter=300, convergence={"energy": 1e-6}, txt=os.path.join(A.out, tag + ".txt"))
    if xc == "HSE06": return GPAW(xc={"name": "HSE06", "backend": "pw"}, symmetry="off", **kw)
    return GPAW(xc={"PBE": "PBE", "R2SCAN": "MGGA_X_R2SCAN+MGGA_C_R2SCAN"}[xc], occupations=FermiDirac(0.01), **kw)
t = time.time()
if A.etapa == "relax":
    a = estructura(A.mat); a.calc = calc("PBE", f"relax_{A.mat}")
    opt = BFGS(FrechetCellFilter(a), logfile=os.path.join(A.out, f"relax_{A.mat}.log")); cv = opt.run(fmax=0.01, steps=60)
    e = a.get_potential_energy(); write(geo, a)
    res = {"met": "PBE_relax", "convergio": bool(cv), "cell": a.cell.cellpar().tolist(), "V_A3": a.get_volume()}
else:
    a = read(geo); tag = f"{A.met}_{A.mat}_{A.k}"; a.calc = calc(A.met, tag); e = a.get_potential_energy(); res = {"met": A.met}
if world.rank == 0:
    tag = f"relax_{A.mat}" if A.etapa == "relax" else f"{A.met}_{A.mat}_{A.k}"; f = os.path.join(A.out, tag + ".json")
    res.update({"mat": A.mat, "E_eV": float(e), "E_por_atomo_eV": float(e) / len(a), "n": len(a), "kpts": K, "ecut": A.ecut, "nproc": world.size, "t_s": round(time.time() - t, 1)})
    json.dump(res, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f); print("FIN", tag, e, flush=True)
