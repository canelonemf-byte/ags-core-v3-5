#!/usr/bin/env python3
"""C-TIO2-HSE: energía de un punto Γ en supercelda con CP2K (GPW), PBE o HSE06+ADMM, geometrías PBE de C-UMF-004.
Uso: python hse_cp2k.py --met {PBE,HSE06} --mat {rutilo,anatasa} --sc {base,grande,smoke} --out DIR [--np 6] [--cutoff 600]
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, re, subprocess, time
import numpy as np, spglib
from ase import Atoms
from ase.io import read
ap = argparse.ArgumentParser()
for k in ("met", "mat", "out", "sc"): ap.add_argument("--" + k)
ap.add_argument("--np", type=int, default=6); ap.add_argument("--k", default=""); ap.add_argument("--cutoff", type=float, default=600); A = ap.parse_args()
ENV = "/workspace/tools/env_cp2k"; GEO = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience/C-UMF-004/out/a_run1/relax_%s.traj"
p = read(GEO % A.mat); c, s, z = spglib.standardize_cell((p.cell[:], p.get_scaled_positions(), p.numbers), to_primitive=False, symprec=1e-3)
conv = Atoms(numbers=z, cell=c, scaled_positions=s, pbc=True)
SC = {"rutilo": {"base": (2, 2, 3), "grande": (3, 3, 4), "smoke": (1, 1, 2)}, "anatasa": {"base": (2, 2, 1), "grande": (3, 3, 1), "smoke": (1, 1, 1)}}[A.mat][A.sc]
a = p if A.k else conv.repeat(SC); tag = f"{A.met}_{A.mat}_{A.sc}_{int(A.cutoff)}" + (("_k" + A.k.replace(",", "")) if A.k else "") + ("_rc3" if os.environ.get("RC_TC") == "3.0" else "")
fam = "PBE" if A.met == "PBE" else "PBE0"
HYB = A.met != "PBE"
cell = "\n".join(f"{v} {x[0]:.10f} {x[1]:.10f} {x[2]:.10f}" for v, x in zip("ABC", a.cell))
coord = "\n".join(f"{e} {q[0]:.10f} {q[1]:.10f} {q[2]:.10f}" for e, q in zip(a.get_chemical_symbols(), a.positions))
Q = {"Ti": 12, "O": 6}
aux = lambda el, q: f"BASIS_SET AUX_FIT admm-dzp-q{q}\n" if HYB else ""
kinds = "\n".join(f"&KIND {el}\nBASIS_SET DZVP-MOLOPT-{fam}-GTH-q{q}\n{aux(el,q)}POTENTIAL GTH-{fam}-q{q}\n&END KIND" for el, q in Q.items())
RC = float(os.environ.get("RC_TC", "3.5"))
rc = min(np.linalg.norm(a.cell, axis=1)) / 2 - 0.1
PBE0TC = f"""&XC_FUNCTIONAL
&PBE
SCALE_X 0.75
SCALE_C 1.0
&END PBE
&PBE_HOLE_T_C_LR
CUTOFF_RADIUS {RC}
SCALE_X 0.25
&END PBE_HOLE_T_C_LR
&END XC_FUNCTIONAL
&HF
FRACTION 0.25
&SCREENING
EPS_SCHWARZ 1.0E-6
SCREEN_ON_INITIAL_P FALSE
&END SCREENING
&INTERACTION_POTENTIAL
POTENTIAL_TYPE TRUNCATED
CUTOFF_RADIUS {RC}
T_C_G_DATA t_c_g.dat
&END INTERACTION_POTENTIAL
&MEMORY
MAX_MEMORY 1200
EPS_STORAGE_SCALING 0.1
&END MEMORY
&END HF"""
xc = "&XC_FUNCTIONAL PBE\n&END XC_FUNCTIONAL" if A.met == "PBE" else PBE0TC if A.met == "PBE0TC" else f"""&XC_FUNCTIONAL
&PBE
SCALE_X 0.0
SCALE_C 1.0
&END PBE
&XWPBE
SCALE_X -0.25
SCALE_X0 1.0
OMEGA 0.11
&END XWPBE
&END XC_FUNCTIONAL
&HF
FRACTION 0.25
{"&RI" + chr(10) + "EPS_PGF_ORB 1.0E-8" + chr(10) + "RI_METRIC TRUNCATED" + chr(10) + "CUTOFF_RADIUS 1.5" + chr(10) + "MEMORY_CUT 5" + chr(10) + "EPS_FILTER 1.0E-9" + chr(10) + "&END RI" if A.k else ""}
&SCREENING
EPS_SCHWARZ 1.0E-7
&END SCREENING
&INTERACTION_POTENTIAL
POTENTIAL_TYPE SHORTRANGE
OMEGA 0.11
&END INTERACTION_POTENTIAL
&MEMORY
MAX_MEMORY 1000
EPS_STORAGE_SCALING 0.1
&END MEMORY
&END HF"""
admm_method = 'NONE' if A.k else 'MO_DIAG'
admm = (f"&AUXILIARY_DENSITY_MATRIX_METHOD\nMETHOD BASIS_PROJECTION\nADMM_PURIFICATION_METHOD {admm_method}\n&END AUXILIARY_DENSITY_MATRIX_METHOD\n" if HYB else "")
scf = ("&SCF\nEPS_SCF 1.0E-7\nMAX_SCF 100\n&DIAGONALIZATION\nALGORITHM STANDARD\n&END DIAGONALIZATION\n&MIXING\nMETHOD BROYDEN_MIXING\nALPHA 0.3\nNBROYDEN 8\n&END MIXING\n") if A.k else "&SCF\nEPS_SCF 1.0E-7\nMAX_SCF 60\n&OT\nMINIMIZER DIIS\nPRECONDITIONER FULL_SINGLE_INVERSE\n&END OT\n&OUTER_SCF\nEPS_SCF 1.0E-7\nMAX_SCF 15\n&END OUTER_SCF\n"
kp = ("&KPOINTS\nSCHEME MONKHORST-PACK " + A.k.replace(",", " ") + "\n&END KPOINTS\n") if A.k else ""
inp = f"""&GLOBAL
PROJECT {tag}
RUN_TYPE ENERGY
PRINT_LEVEL LOW
&END GLOBAL
&FORCE_EVAL
METHOD QS
&DFT
BASIS_SET_FILE_NAME BASIS_MOLOPT_UZH
BASIS_SET_FILE_NAME BASIS_ADMM_UZH
POTENTIAL_FILE_NAME POTENTIAL_UZH
{admm}&MGRID
CUTOFF {A.cutoff}
REL_CUTOFF 60
&END MGRID
&QS
EPS_DEFAULT 1.0E-12
EPS_PGF_ORB 1.0E-8
&END QS
{kp}{scf}&END SCF
&XC
{xc}
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
pr = subprocess.run([ENV + "/bin/mpiexec", "-n", str(A.np), ENV + "/bin/cp2k.psmp", "-i", "in.inp", "-o", "out.log"], cwd=wd, env=env)
log = open(os.path.join(wd, "out.log")).read()
m = re.findall(r"ENERGY\| Total FORCE_EVAL \( QS \) energy \[hartree\]\s+(-?\d+\.\d+)", log)
ok = m and "SCF run NOT converged" not in log
if ok:
    e = float(m[-1]) * 27.211386245988
    res = {"met": A.met, "mat": A.mat, "sc": A.sc, "supercelda": SC, "cutoff_Ry": A.cutoff, "E_eV": e, "E_por_atomo_eV": e / len(a), "n": len(a), "rc_hfx_A": rc, "nproc": A.np, "t_s": round(time.time() - t, 1)}
    f = os.path.join(A.out, tag + ".json"); json.dump(res, open(f + ".tmp", "w"), indent=1); os.replace(f + ".tmp", f); print("FIN", tag, e, res["t_s"], flush=True)
else: print("FALLO", tag, "rc", pr.returncode, flush=True); raise SystemExit(1)
