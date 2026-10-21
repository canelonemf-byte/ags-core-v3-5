"""Exploratorio X2: profundidad del doble pozo ferroeléctrico (fonón congelado del modo Γ más blando y relajación
libre) con MACE-MP-0 en perovskitas cúbicas. Código original."""
import json, numpy as np
from ase import Atoms
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from mace.calculators import mace_mp
calc = mace_mp(model="medium", default_dtype="float64", device="cpu")
# a0 iniciales aproximados (fase cúbica); la relajación fija el valor del modelo
P = {"PbTiO3": ("Pb","Ti",3.97), "KNbO3": ("K","Nb",4.02), "BaTiO3": ("Ba","Ti",4.006), "SrTiO3": ("Sr","Ti",3.905), "KTaO3": ("K","Ta",3.989)}
def perov(A,B,a): return Atoms([A,B,"O","O","O"], scaled_positions=[(0,0,0),(.5,.5,.5),(.5,.5,0),(.5,0,.5),(0,.5,.5)], cell=[a,a,a], pbc=True)
def E(a): b=a.copy(); b.calc=calc; return b.get_potential_energy()
out = {}
for name,(A,B,a0) in P.items():
    a = perov(A,B,a0); a.calc = calc; a.set_constraint(FixSymmetry(a))
    BFGS(FrechetCellFilter(a), logfile=None).run(fmax=1e-4, steps=2000); a.set_constraint()
    ph = Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(), cell=a.cell[:], scaled_positions=a.get_scaled_positions()), supercell_matrix=np.diag([2,2,2]), primitive_matrix="P")
    ph.generate_displacements(distance=0.01); F=[]
    for sc in ph.supercells_with_displacements:
        at=Atoms(sc.symbols,cell=sc.cell,scaled_positions=sc.scaled_positions,pbc=True); at.calc=calc; f=at.get_forces(); F.append(f-f.mean(0))
    ph.forces=np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_qpoints([[0,0,0]], with_eigenvectors=True); fr=ph.qpoints.frequencies[0]; ev=ph.qpoints.eigenvectors[0]
    k=int(np.argmin(fr)); m=a.get_masses(); d=(ev[:,k].reshape(-1,3).real)/np.sqrt(m)[:,None]; d-= (m[:,None]*d).sum(0)/m.sum(); d/=np.abs(d).max()
    E0=E(a); amps=np.linspace(0,0.35,36); es=[]
    for s in amps:
        b=a.copy(); b.positions+=s*d; es.append((E(b)-E0)*1000)
    i=int(np.argmin(es))
    # relajación libre (sin simetría) desde el mínimo del barrido, incluida la celda
    b=a.copy(); b.positions+=amps[i]*d+1e-3*np.random.default_rng(7).standard_normal((5,3)); b.calc=calc
    BFGS(FrechetCellFilter(b), logfile=None).run(fmax=1e-3, steps=3000); Er=(b.get_potential_energy()-E0)*1000
    import spglib; sg=spglib.get_spacegroup((b.cell[:],b.get_scaled_positions(),b.numbers),1e-2)
    out[name]={"a_cubica_A":float(a.cell.lengths()[0]),"f_min_Gamma_THz":float(fr[k]),"dE_congelado_meV_fu":float(es[i]),"amp_min_A":float(amps[i]),
               "dE_relajado_meV_fu":float(Er),"grupo_relajado":sg,"barrido_meV":[float(x) for x in es]}
    print(name, out[name]["a_cubica_A"].__round__(3), round(fr[k],3), round(es[i],2), amps[i], round(Er,2), sg, flush=True)
json.dump(out, open("out/x2_ferro_wells.json","w"), indent=1)
