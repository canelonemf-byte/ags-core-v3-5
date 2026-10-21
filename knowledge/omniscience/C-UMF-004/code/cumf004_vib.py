#!/usr/bin/env python3
"""C-UMF-004: ZPE y U_term(298) armónicas MatterSim de rutilo y anatasa en geometría experimental (phonopy). Uso: python cumf004_vib.py --out DIR
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import argparse, json, os, warnings
warnings.filterwarnings("ignore")
import numpy as np, torch
torch.set_num_threads(2); torch.manual_seed(0)
from ase import Atoms
from ase.spacegroup import crystal
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from mattersim.forcefield import MatterSimCalculator
ap = argparse.ArgumentParser(); ap.add_argument("--out"); A = ap.parse_args(); os.makedirs(A.out, exist_ok=True)
calc = MatterSimCalculator(load_path="MatterSim-v1.0.0-5M.pth", device="cpu")
S = {"rutilo": (crystal(["Ti", "O"], basis=[(0, 0, 0), (0.3048, 0.3048, 0)], spacegroup=136, cellpar=[4.594, 4.594, 2.959, 90, 90, 90]), [3, 3, 4]),
     "anatasa": (crystal(["Ti", "O"], basis=[(0, 0, 0), (0, 0, 0.2081)], spacegroup=141, setting=1, cellpar=[3.785, 3.785, 9.514, 90, 90, 90]), [3, 3, 1])}
for m, (a, sc) in S.items():
    f = os.path.join(A.out, f"vib_{m}.json")
    if os.path.exists(f): continue
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()), supercell_matrix=np.diag(sc))
    ph.generate_displacements(distance=0.01); F = []
    for s in ph.supercells_with_displacements:
        b = Atoms(s.symbols, cell=s.cell, scaled_positions=s.scaled_positions, pbc=True); b.calc = calc; F.append(b.get_forces())
    ph.forces = np.array(F); ph.produce_force_constants(); ph.run_mesh([20, 20, 20]); fr = ph.get_mesh_dict()["frequencies"]
    ph.run_thermal_properties(temperatures=[0, 298.15]); tp = ph.get_thermal_properties_dict(); n = len(a)
    kJ = 1 / 96.485  # kJ/mol -> eV
    F0, F298, S298 = tp["free_energy"][0] * kJ, tp["free_energy"][1] * kJ, tp["entropy"][1] * kJ / 1000
    U298 = F298 + 298.15 * S298
    json.dump({"mat": m, "n_celda": n, "supercelda": sc, "n_desp": len(F), "fmin_THz": float(fr.min()),
               "ZPE_eV_at": F0 / n, "Uvib298_eV_at": U298 / n, "F298_eV_at": F298 / n}, open(f, "w"), indent=1); print(m, F0 / n, U298 / n, fr.min(), flush=True)
print("FIN", flush=True)
