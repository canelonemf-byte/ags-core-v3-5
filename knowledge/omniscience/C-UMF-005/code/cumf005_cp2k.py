#!/usr/bin/env python3
"""C-UMF-005 parte A: energía de un punto con CP2K (GPW) sobre geometrías PBE relajadas de C-UMF-004.
Uso: python cumf005_cp2k.py --met {PBE,R2SCAN} --mat {rutilo,anatasa} --out DIR [--k normal|smoke] [--cutoff 1000] [--np 2]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, re, subprocess, time
from ase.io import read
ap = argparse.ArgumentParser()
for k in ("met", "mat", "out"): ap.add_argument("--" + k)
ap.add_argument("--k", default="normal"); ap.add_argument("--cutoff", type=float, default=1000); ap.add_argument("--np", type=int, default=2); A = ap.parse_args()
ENV = "/workspace/tools/env_cp2k"; GEO = "/workspace/omniscience_cumf004/out/a_run1/relax_%s.traj"
K = {"normal": {"rutilo": (5, 5, 8), "anatasa": (6, 6, 6)}, "smoke": {"rutilo": (2, 2, 3), "anatasa": (2, 2, 2)}}[A.k][A.mat]
FUN = {"PBE": "&XC_FUNCTIONAL PBE\n&END XC_FUNCTIONAL",
       "R2SCAN": "&XC_FUNCTIONAL\n&MGGA_X_R2SCAN\n&END MGGA_X_R2SCAN\n&MGGA_C_R2SCAN\n&END MGGA_C_R2SCAN\n&END XC_FUNCTIONAL"}[A.met]
FAM = {"PBE": "PBE", "R2SCAN": "SCAN"}[A.met]; Q = {"Ti": 12, "O": 6}
a = read(GEO % A.mat); tag = f"{A.met}_{A.mat}_{A.k}_{int(A.cutoff)}"; os.makedirs(A.out, exist_ok=True)
cell = "\n".join(f"{v} {x[0]:.10f} {x[1]:.10f} {x[2]:.10f}" for v, x in zip("ABC", a.cell))
coord = "\n".join(f"{s} {p[0]:.10f} {p[1]:.10f} {p[2]:.10f}" for s, p in zip(a.get_chemical_symbols(), a.positions))
kinds = "\n".join(f"&KIND {el}\nBASIS_SET TZV2P-MOLOPT-{FAM}-GTH-q{q}\nPOTENTIAL GTH-{FAM}-q{q}\n&END KIND" for el, q in Q.items())
inp = f"""&GLOBAL
PROJECT {tag}
RUN_TYPE ENERGY
PRINT_LEVEL LOW
&END GLOBAL
&FORCE_EVAL
METHOD QS
&DFT
BASIS_SET_FILE_NAME BASIS_MOLOPT_UZH_2026.2
POTENTIAL_FILE_NAME POTENTIAL_UZH_2026.2
&MGRID
CUTOFF {A.cutoff}
REL_CUTOFF 70
&END MGRID
&QS
EPS_DEFAULT 1.0E-12
&END QS
&KPOINTS
SCHEME MONKHORST-PACK {K[0]} {K[1]} {K[2]}
SYMMETRY F
&END KPOINTS
&SCF
EPS_SCF 1.0E-8
MAX_SCF 300
ADDED_MOS 20
&SMEAR ON
METHOD FERMI_DIRAC
ELECTRONIC_TEMPERATURE [K] 300
&END SMEAR
&MIXING
METHOD BROYDEN_MIXING
ALPHA 0.2
NBROYDEN 8
&END MIXING
&END SCF
&XC
{FUN}
&END XC
&END DFT
&SUBSYS
&CELL
{cell}
PERIODIC XYZ
&END CELL
&COORD
{coord}
&END COORD
{kinds}
&END SUBSYS
&END FORCE_EVAL
"""
wd = os.path.join(A.out, tag); os.makedirs(wd, exist_ok=True); open(os.path.join(wd, "in.inp"), "w").write(inp)
env = dict(os.environ, OMP_NUM_THREADS="1", CP2K_DATA_DIR=ENV + "/share/cp2k/data"); t = time.time()
p = subprocess.run([ENV + "/bin/mpiexec", "-n", str(A.np), ENV + "/bin/cp2k.psmp", "-i", "in.inp", "-o", "out.log"], cwd=wd, env=env)
log = open(os.path.join(wd, "out.log")).read()
m = re.findall(r"ENERGY\| Total FORCE_EVAL \( QS \) energy \[hartree\]\s+(-?\d+\.\d+)", log)
conv = "SCF run converged" in log and "SCF run NOT converged" not in log
if m and conv:
    e = float(m[-1]) * 27.211386245988
    res = {"met": A.met, "mat": A.mat, "k": A.k, "kpts": K, "cutoff_Ry": A.cutoff, "E_eV": e, "E_por_atomo_eV": e / len(a), "n": len(a), "nproc": A.np, "t_s": round(time.time() - t, 1), "rc": p.returncode}
    f = os.path.join(A.out, tag + ".json"); json.dump(res, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f); print("FIN", tag, e, flush=True)
else: print("FALLO", tag, "rc", p.returncode, "conv", conv, flush=True); raise SystemExit(1)
