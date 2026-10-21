"""INN-01 (prereg congelado sha256 180ae31a…9663): σᴬ(300 K) con MACE-MP-0, muestreo armónico clásico.
Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA. Código original."""
import json, sys, numpy as np
from ase import Atoms
from ase.build import bulk
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from phonopy.phonon.random_displacements import RandomDisplacements
from mace.calculators import mace_mp
SEED, NSNAP, T, TOL = 20261018, 24, 300.0, -0.3
calc = mace_mp(model="medium", default_dtype="float64", device="cpu")
S = {"CuCl_ZB":("CuCl","zincblende",5.42),"CuBr_ZB":("CuBr","zincblende",5.69),"CuI_ZB":("CuI","zincblende",6.05),
     "AgI_ZB":("AgI","zincblende",6.50),"AgBr_ZB":("AgBr","zincblende",6.20),"AgCl_RS":("AgCl","rocksalt",5.55),
     "AgBr_RS":("AgBr","rocksalt",5.77),"AgI_RS":("AgI","rocksalt",6.07),"NaBr_RS":("NaBr","rocksalt",5.97),
     "Si_control":("Si","diamond",5.431)}
def relax(a):
    a=a.copy(); a.calc=calc; a.set_constraint(FixSymmetry(a)); BFGS(FrechetCellFilter(a),logfile=None).run(fmax=1e-3,steps=3000); a.set_constraint(); return a
def forces(sc_atoms):
    at=Atoms(sc_atoms.symbols,cell=sc_atoms.cell,scaled_positions=sc_atoms.scaled_positions,pbc=True); at.calc=calc; f=at.get_forces(); return f-f.mean(0)
def fc_model(a,n):
    ph=Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(),cell=a.cell[:],scaled_positions=a.get_scaled_positions()),supercell_matrix=np.diag([n]*3),primitive_matrix="auto")
    ph.generate_displacements(distance=0.01); ph.forces=np.array([forces(s) for s in ph.supercells_with_displacements])
    ph.produce_force_constants(); ph.symmetrize_force_constants(); ph.run_mesh([20,20,20],is_gamma_center=True)
    return ph, float(ph.get_mesh_dict()["frequencies"].min())
def sigmaA(ph, rng_boot):
    rd=RandomDisplacements(ph.supercell,ph.primitive,ph.force_constants,dist_func="classical"); rd.run(T,number_of_snapshots=NSNAP,random_seed=SEED)
    U=rd.u; fc=ph.force_constants; sc=ph.supercell; num=[];den=[];num0=[]
    for u in U:
        pos=sc.positions+u; at=Atoms(sc.symbols,cell=sc.cell,positions=pos,pbc=True); at.calc=calc; F=at.get_forces(); F-=F.mean(0)
        Fh=-np.einsum("ijab,jb->ia",fc,u); num.append(((F-Fh)**2).sum()); den.append((F**2).sum()); num0.append(((Fh-Fh)**2).sum())
    num,den=np.array(num),np.array(den); s=float(np.sqrt(num.sum()/den.sum()))
    b=[np.sqrt(num[i].sum()/den[i].sum()) for i in (rng_boot.integers(0,NSNAP,NSNAP) for _ in range(2000))]
    return s,[float(np.percentile(b,2.5)),float(np.percentile(b,97.5))],float(np.sqrt(np.sum(num0)/den.sum())),float(np.sqrt((U**2).sum(-1).mean()))
only = sys.argv[1].split(",") if len(sys.argv)>1 else list(S)
out={}
try: out=json.load(open("out/inn01_raw.json"))
except Exception: pass
for name in only:
    f,st,a0=S[name]; a=relax(bulk(f,st,a=a0,cubic=True)); rng=np.random.default_rng(SEED)
    ph3,fmin3=fc_model(a,3); ph2,fmin2=fc_model(a,2)
    r={"a_relajada_A":float(a.cell.lengths()[0]),"fmin_malla_3x3x3_THz":fmin3,"fmin_malla_2x2x2_THz":fmin2,"estable":bool(fmin3>=TOL)}
    if r["estable"]:
        s3,ci3,triv,rms=sigmaA(ph3,rng); s2,ci2,_,_=sigmaA(ph2,rng)
        r.update(sigma_a_3x3x3=s3,ic95_3x3x3=ci3,sigma_a_2x2x2=s2,ic95_2x2x2=ci2,control_trivial=triv,rms_u_A=rms)
    out[name]=r; print(name,json.dumps(r),flush=True); json.dump(out,open("out/inn01_raw.json","w"),indent=1)
    ph3.save(f"out/{name}_phonopy_3x3x3.yaml")
