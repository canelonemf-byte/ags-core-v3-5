"""INN-03 (prereg congelado sha256 839eeaec…728a): profundidad del doble pozo con MACE-MP-0 en perovskitas ABX3.
Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA. Código original."""
import json, numpy as np, spglib
from ase import Atoms
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from mace.calculators import mace_mp
calc = mace_mp(model="medium", default_dtype="float64", device="cpu")
M = {"BiFeO3":("Bi","Fe","O",3.96),"CsGeCl3":("Cs","Ge","Cl",5.43),"CsGeBr3":("Cs","Ge","Br",5.64),"CsGeI3":("Cs","Ge","I",6.05),
     "PbZrO3":("Pb","Zr","O",4.16),"PbHfO3":("Pb","Hf","O",4.14),"CaTiO3":("Ca","Ti","O",3.84),"BaZrO3":("Ba","Zr","O",4.19),
     "SrZrO3":("Sr","Zr","O",4.10),"BaSnO3":("Ba","Sn","O",4.12)}
def perov(A,B,X,a): return Atoms([A,B,X,X,X],scaled_positions=[(0,0,0),(.5,.5,.5),(.5,.5,0),(.5,0,.5),(0,.5,.5)],cell=[a,a,a],pbc=True)
def E(a): b=a.copy(); b.calc=calc; return b.get_potential_energy()
def gamma(a,n):
    ph=Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(),cell=a.cell[:],scaled_positions=a.get_scaled_positions()),supercell_matrix=np.diag([n]*3),primitive_matrix="P")
    ph.generate_displacements(distance=0.01); F=[]
    for sc in ph.supercells_with_displacements:
        at=Atoms(sc.symbols,cell=sc.cell,scaled_positions=sc.scaled_positions,pbc=True); at.calc=calc; f=at.get_forces(); F.append(f-f.mean(0))
    ph.forces=np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants()
    ph.run_qpoints([[0,0,0]],with_eigenvectors=True); fr=ph.qpoints.frequencies[0]; ev=ph.qpoints.eigenvectors[0]
    opt=np.argsort(np.abs(fr))[3:]; k=int(opt[np.argmin(fr[opt])]); return fr,ev,k
out={}
for name,(A,B,X,a0) in M.items():
    a=perov(A,B,X,a0); a.calc=calc; a.set_constraint(FixSymmetry(a))
    BFGS(FrechetCellFilter(a),logfile=None).run(fmax=1e-4,steps=2000); a.set_constraint()
    fr,ev,k=gamma(a,2); fr3,_,k3=gamma(a,3)
    m=a.get_masses(); d=(ev[:,k].reshape(-1,3).real)/np.sqrt(m)[:,None]; d-=(m[:,None]*d).sum(0)/m.sum(); d/=np.abs(d).max()
    E0=E(a); amps=np.linspace(0,0.35,36); es=[]
    for s in amps:
        b=a.copy(); b.positions+=s*d; es.append((E(b)-E0)*1000)
    i=int(np.argmin(es))
    b=a.copy(); b.positions+=amps[i]*d+1e-3*np.random.default_rng(7).standard_normal((5,3)); b.calc=calc
    BFGS(FrechetCellFilter(b),logfile=None).run(fmax=1e-3,steps=3000); Er=(b.get_potential_energy()-E0)*1000
    sg=spglib.get_spacegroup((b.cell[:],b.get_scaled_positions(),b.numbers),1e-2)
    out[name]={"a_cubica_A":float(a.cell.lengths()[0]),"f_opt_min_gamma_2x2x2_THz":float(fr[k]),"f_opt_min_gamma_3x3x3_THz":float(fr3[k3]),
               "de_congelado_meV_fu":float(es[i]),"amp_min_A":float(amps[i]),"de_relajado_meV_fu":float(Er),"grupo_relajado":sg,"barrido_meV":[float(x) for x in es]}
    print(name,round(out[name]["a_cubica_A"],3),round(fr[k],3),round(fr3[k3],3),round(es[i],2),round(Er,2),sg,flush=True)
    json.dump(out,open("out/inn03_raw.json","w"),indent=1)
