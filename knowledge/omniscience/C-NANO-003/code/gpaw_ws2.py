#!/usr/bin/env python3
"""C-NANO-003 control C1: Γ de WS2 monocapa con GPAW PBE (PW 500 eV, k 12×12×1, FermiDirac 0.05 eV, vacío 20 Å) en la red a relajada por MatterSim run1 (posiciones internas relajadas en PBE).
Diferencias finitas en la celda primitiva (ase.vibrations, 0.01 Å, nfree 2) ⇒ modos q=0. Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA (ORCID 0000-0001-8601-1963)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import guardia; guardia.activar(500)
import numpy as np
from ase import Atoms
from ase.vibrations import Vibrations
from gpaw import GPAW, PW, FermiDirac
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; O = f"{H}/out/gpaw"; os.makedirs(O, exist_ok=True)
a = json.load(open(f"{H}/out/run1/mattersim/WS2.json"))["a_A"]; c = 20.0; d = 1.57 / c; g = Atoms("WS2", cell=[[a, 0, 0], [-a / 2, a * np.sqrt(3) / 2, 0], [0, 0, c]], scaled_positions=[[1/3, 2/3, .5], [2/3, 1/3, .5 + d], [2/3, 1/3, .5 - d]], pbc=True)
g.calc = GPAW(mode=PW(500), xc="PBE", kpts=(12, 12, 1), occupations=FermiDirac(0.05), convergence={"density": 1e-6, "forces": 1e-5}, symmetry="off", txt=f"{O}/gpaw.txt")
from ase.optimize import BFGS; BFGS(g, logfile=f"{O}/relax_pos.log").run(fmax=0.005, steps=60)   # solo posiciones internas (espesor S–S) en PBE
v = Vibrations(g, name=f"{O}/vib", delta=0.01, nfree=2); v.run(); vd = v.get_vibrations(); e = vd.get_energies(); M = vd.get_modes(all_atoms=True); out = []
sy = g.get_chemical_symbols()
for j in range(9):
    m = np.abs(M[j].reshape(3, 3)) ** 2; m = m / m.sum(); nu = float(np.real(e[j])) / 1.23984198e-4 if abs(np.imag(e[j])) < 1e-12 else -float(np.imag(e[j])) / 1.23984198e-4
    out.append({"nu_cm": nu, "frac_z": float(m[:, 2].sum()), "peso_Mo": float(sum(m[i].sum() for i in range(3) if sy[i] == "W"))})
json.dump({"a_A": a, "modos": out, "metodo": "GPAW PBE PW500 k12x12x1 FD0.05 vac20, posiciones relajadas PBE, ase.vibrations 0.01"}, open(f"{O}/gpaw_WS2_gamma.json", "w"), indent=1)
print("FIN_GPAW", out, flush=True)
