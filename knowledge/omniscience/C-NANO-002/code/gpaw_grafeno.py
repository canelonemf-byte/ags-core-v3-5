#!/usr/bin/env python3
"""C-NANO-002 control C1: frecuencias Γ de grafeno con GPAW PBE (onda plana 500 eV, k 18×18×1, FermiDirac 0.05 eV, vacío 20 Å) en la red relajada por MatterSim run1.
Fonones Γ por diferencias finitas en la celda primitiva (ase.vibrations, 0.01 Å): desplazar un átomo de la celda desplaza todas sus imágenes ⇒ modo q=0 exacto.
Uso: OMP_NUM_THREADS=2 python gpaw_grafeno.py   (serie, sin MPI). Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import guardia; guardia.activar(500)
import numpy as np
from ase import Atoms
from ase.vibrations import Vibrations
from gpaw import GPAW, PW, FermiDirac
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; O = f"{H}/out/gpaw"; os.makedirs(O, exist_ok=True)
a = json.load(open(f"{H}/out/run1/mattersim/grafeno.json"))["a_A"]; c = 20.0
g = Atoms("C2", cell=[[a, 0, 0], [-a / 2, a * np.sqrt(3) / 2, 0], [0, 0, c]], scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5]], pbc=True)
g.calc = GPAW(mode=PW(500), xc="PBE", kpts=(18, 18, 1), occupations=FermiDirac(0.05), convergence={"density": 1e-6, "forces": 1e-5}, symmetry="off", txt=f"{O}/gpaw.txt")
v = Vibrations(g, name=f"{O}/vib", delta=0.01, nfree=2); v.run()
vd = v.get_vibrations(); e = vd.get_energies(); M = vd.get_modes(all_atoms=True); out = []
for j in range(6):
    m = M[j].reshape(2, 3); fz = float((np.abs(m[:, 2]) ** 2).sum() / (np.abs(m) ** 2).sum())
    nu = float(np.real(e[j])) / 1.23984198e-4 if abs(np.imag(e[j])) < 1e-12 else -float(np.imag(e[j])) / 1.23984198e-4
    out.append({"nu_cm": nu, "frac_z": fz})
json.dump({"a_A": a, "modos": out, "metodo": "GPAW PBE PW500 k18x18x1 FD0.05 vac20 ase.vibrations 0.01"}, open(f"{O}/gpaw_grafeno_gamma.json", "w"), indent=1)
print("FIN_GPAW", out, flush=True)
