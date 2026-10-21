#!/usr/bin/env python3
"""C-UMF-003 parte A: energía de rutilo y anatasa (geometría experimental fija) con PBE, PBE+U o r2SCAN.
Uso: mpiexec -n N python cumf003_dft.py --met {PBE,PBEU,R2SCAN} --mat {rutilo,anatasa} --out DIR [--k reducido]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, time
from ase.spacegroup import crystal
from gpaw import GPAW, PW, FermiDirac
from gpaw.mpi import world
ap = argparse.ArgumentParser(); ap.add_argument("--met"); ap.add_argument("--mat"); ap.add_argument("--out"); ap.add_argument("--k", default="normal"); ap.add_argument("--ecut", type=float, default=600)
A = ap.parse_args()
def estructura(m):
    if m == "rutilo": return crystal(["Ti", "O"], basis=[(0, 0, 0), (0.3048, 0.3048, 0)], spacegroup=136, cellpar=[4.594, 4.594, 2.959, 90, 90, 90])
    return crystal(["Ti", "O"], basis=[(0, 0, 0), (0, 0, 0.2081)], spacegroup=141, setting=1, cellpar=[3.785, 3.785, 9.514, 90, 90, 90], primitive_cell=True)
K = {"normal": {"rutilo": (5, 5, 8), "anatasa": (6, 6, 6)}, "reducido": {"rutilo": (4, 4, 6), "anatasa": (5, 5, 5)}}[A.k][A.mat]
xc = {"PBE": "PBE", "PBEU": "PBE", "R2SCAN": "MGGA_X_R2SCAN+MGGA_C_R2SCAN"}[A.met]
setups = {"Ti": ":d,4.0"} if A.met == "PBEU" else {}
os.makedirs(A.out, exist_ok=True); tag = f"{A.met}_{A.mat}"; f = os.path.join(A.out, tag + ".json")
a = estructura(A.mat); assert len(a) == 6
a.calc = GPAW(mode=PW(A.ecut), xc=xc, setups=setups, kpts={"size": K, "gamma": True}, occupations=FermiDirac(0.01),
              maxiter=300, convergence={"energy": 1e-6}, txt=os.path.join(A.out, tag + ".txt"))
t = time.time(); e = a.get_potential_energy()
if world.rank == 0:
    json.dump({"met": A.met, "mat": A.mat, "E_eV": float(e), "E_por_atomo_eV": float(e) / 6, "kpts": K, "ecut": A.ecut, "nproc": world.size,
               "t_s": round(time.time() - t, 1)}, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f)
    print("FIN", tag, e, flush=True)
