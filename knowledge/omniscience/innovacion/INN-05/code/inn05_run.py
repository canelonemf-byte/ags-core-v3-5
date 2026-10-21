"""INN-05 (prereg congelado sha256 4d8f3ba1…e4d2): solapamiento de DOS fonónica MACE-MP-0 y línea base AMM (descriptivo, n=4).
Autoría: Lázaro López Paz (ORCID 0000-0001-8601-1963), con asistencia de IA. Código original."""
import json, itertools, numpy as np, spglib, phonopy
from ase import Atoms
from ase.build import bulk
from ase.spacegroup import crystal
from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS
from phonopy import Phonopy
from phonopy.structure.atoms import PhonopyAtoms
from mace.calculators import mace_mp
calc=mace_mp(model="medium",default_dtype="float64",device="cpu")
def prim(a):
    c,p,n=spglib.find_primitive((a.cell[:],a.get_scaled_positions(),a.numbers),symprec=1e-3); return Atoms(numbers=n,cell=c,scaled_positions=p,pbc=True)
S={"Al":bulk("Al","fcc",a=4.05),"Pb":bulk("Pb","fcc",a=4.95),"Co":bulk("Co","hcp",a=2.507,c=4.07),"Ru":bulk("Ru","hcp",a=2.706,c=4.282),
   "TiN":bulk("TiN","rocksalt",a=4.24),
   "Al2O3":prim(crystal(["Al","O"],basis=[(0,0,0.3522),(0.3064,0,0.25)],spacegroup=167,cellpar=[4.759,4.759,12.991,90,90,120]))}
grid=np.linspace(0,40,4001); D={}; info={}
dirs=np.array([d for d in itertools.product([-1,0,1],repeat=3) if any(d)],float); dirs/=np.linalg.norm(dirs,axis=1)[:,None]
for name,a in S.items():
    a=a.copy(); a.calc=calc; a.set_constraint(FixSymmetry(a)); BFGS(FrechetCellFilter(a),logfile=None).run(fmax=1e-3,steps=3000); a.set_constraint()
    ph=Phonopy(PhonopyAtoms(symbols=a.get_chemical_symbols(),cell=a.cell[:],scaled_positions=a.get_scaled_positions()),supercell_matrix=np.diag([2,2,2]),primitive_matrix="P")
    ph.generate_displacements(distance=0.01); F=[]
    for sc in ph.supercells_with_displacements:
        at=Atoms(sc.symbols,cell=sc.cell,scaled_positions=sc.scaled_positions,pbc=True); at.calc=calc; f=at.get_forces(); F.append(f-f.mean(0))
    ph.forces=np.array(F); ph.produce_force_constants(); ph.symmetrize_force_constants(); ph.save(f"out/{name}_phonopy.yaml")
    ph.run_mesh([20,20,20],is_gamma_center=True); fmin=float(ph.get_mesh_dict()["frequencies"].min())
    ph.run_total_dos(freq_pitch=0.01,sigma=0.1); d=ph.get_total_dos_dict()
    g=np.clip(np.interp(grid,d["frequency_points"],d["total_dos"],left=0,right=0),0,None); D[name]=g/np.trapezoid(g,grid)
    # velocidad de Debye: q cartesiano |q| = 0.02 Å^-1 (sin 2π), v = f/|q| en THz·Å (=100 m/s)
    rec=np.linalg.inv(a.cell[:]).T  # vectores recíprocos sin 2π (filas)
    qred=[(0.02*u)@np.linalg.inv(rec) for u in dirs]; ph.run_qpoints(qred); fr=np.sort(ph.qpoints.frequencies,axis=1)[:,:3]
    v=fr/0.02*100.0; vD=float((np.mean(1/v**3)/1)**(-1/3))
    rho=float(a.get_masses().sum()*1.66053906660e-27/(a.get_volume()*1e-30))
    info[name]={"cell_lengths_A":a.cell.lengths().tolist(),"fmin_THz":fmin,"v_debye_m_s":vD,"densidad_kg_m3":rho,"Z":rho*vD}
    print(name,json.dumps(info[name]),flush=True)
pC=phonopy.load("/workspace/omniscience_cmat001/out/C_phonopy_base.yaml",produce_fc=True,log_level=0); pC.run_mesh([20,20,20],is_gamma_center=True); pC.run_total_dos(freq_pitch=0.01,sigma=0.1)
d=pC.get_total_dos_dict(); g=np.clip(np.interp(grid,d["frequency_points"],d["total_dos"],left=0,right=0),0,None); D["C_control"]=g/np.trapezoid(g,grid)
O=lambda x,y: float(np.trapezoid(np.minimum(D[x],D[y]),grid))
TBC={"Al|Al2O3":350.0,"Co|Al2O3":350.0,"Ru|Al2O3":350.0,"TiN|Al2O3":700.0}
pairs={}
for p,tb in TBC.items():
    m,s=p.split("|"); Z1,Z2=info[m]["Z"],info[s]["Z"]; pairs[p]={"tbc_exp_MW_m2K":tb,"solapamiento":O(m,s),"t_amm":4*Z1*Z2/(Z1+Z2)**2}
res={"materiales":info,"pares":pairs,"controles":{"Al|Al":O("Al","Al"),"C|Pb":O("C_control","Pb")},"nota":"descriptivo; H-T1/H-T2/H-T3 no evaluables (enmiendas C2, C3)"}
json.dump(res,open("out/inn05_raw.json","w"),indent=1); print(json.dumps(res["pares"],indent=1),res["controles"])
np.save("out/dos_grid.npy",np.vstack([grid]+[D[k] for k in ["Al","Co","Ru","TiN","Al2O3","Pb","C_control"]]))
