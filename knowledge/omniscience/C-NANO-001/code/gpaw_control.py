#!/usr/bin/env python3
"""C-NANO-001 control C1: GPAW PBE punto único en geometrías MatterSim run1 (losa anatasa(101) y bulk anatasa). Uso: mpiexec -n 6 python3 gpaw_control.py
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import json, os, numpy as np
from ase.io import read
from gpaw import GPAW, PW, FermiDirac
from gpaw.mpi import world
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; D = f"{H}/out/run1/mattersim"; O = f"{H}/out/gpaw"; os.makedirs(O, exist_ok=True)
tj = json.load(open(f"{D}/tio2_anatasa_101.json")); s = read(f"{D}/slab_anatasa_101_t{tj['term_min']}.traj"); b = read(f"{D}/bulk_anatasa.traj")
def kp(a, slab):
    k = [max(1, int(np.ceil(1 / (0.25 * np.linalg.norm(a.cell[i]))))) for i in range(3)]
    if slab: k[2] = 1
    return tuple(k)
def E(a, slab, tag):
    f = f"{O}/{tag}.json"
    if os.path.exists(f): return json.load(open(f))["E"]
    a.calc = GPAW(mode=PW(400), xc="PBE", kpts={"size": kp(a, slab), "gamma": True}, occupations=FermiDirac(0.05), convergence={"energy": 1e-6, "density": 1e-5}, txt=f"{O}/{tag}.txt")
    e = a.get_potential_energy()
    if world.rank == 0: json.dump({"E": e, "k": kp(a, slab), "n": len(a)}, open(f, "w"))
    return e
eb = E(b, False, "bulk_anatasa"); es = E(s, True, "slab_anatasa101")
A = np.linalg.norm(np.cross(s.cell[0], s.cell[1])); g = (es - len(s) / 3 * eb / (len(b) / 3)) / (2 * A) * 16.02176634
if world.rank == 0: json.dump({"gamma_PBE_J_m2": g, "E_slab": es, "E_bulk": eb, "n_slab": len(s), "n_bulk": len(b), "area_A2": A}, open(f"{O}/gpaw_anatasa101.json", "w"), indent=1); print("FIN_GPAW", g)
