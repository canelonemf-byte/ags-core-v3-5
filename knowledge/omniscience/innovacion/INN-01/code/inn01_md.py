"""INN-01 control MD (enmienda A7): σᴬ desde MD Langevin 300 K con MACE-MP-0 y FC 3×3×3. Código original."""
import json, sys, numpy as np, phonopy
from ase import Atoms, units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from mace.calculators import mace_mp
SEED=20261018; calc=mace_mp(model="medium",default_dtype="float64",device="cpu")
name=sys.argv[1]; ph=phonopy.load(f"out/{name}_phonopy_3x3x3.yaml",produce_fc=True,is_compact_fc=False,log_level=0)
sc=ph.supercell; fc=ph.force_constants; at=Atoms(sc.symbols,cell=sc.cell,positions=sc.positions,pbc=True); at.calc=calc; ref=sc.positions.copy()
MaxwellBoltzmannDistribution(at,temperature_K=300,rng=np.random.default_rng(SEED))
dyn=Langevin(at,4*units.fs,temperature_K=300,friction=0.01/units.fs,rng=np.random.default_rng(SEED+1))
num=0.0;den=0.0;n=0;cellinv=np.linalg.inv(sc.cell)
def acc():
    global num,den,n
    u=at.positions-ref; fr=u@cellinv; fr-=np.round(fr); u=fr@sc.cell; u-=u.mean(0)
    F=at.get_forces(); F-=F.mean(0); Fh=-np.einsum("ijab,jb->ia",fc,u); num+=((F-Fh)**2).sum(); den+=(F**2).sum(); n+=1
for step in range(1250):
    dyn.run(1)
    if step>=250 and step%5==0: acc()
r={"sigma_a_md":float(np.sqrt(num/den)),"frames":n,"dt_fs":4,"t_total_ps":5.0,"descartado_ps":1.0}
print(name,r); json.dump(r,open(f"out/{name}_md.json","w"),indent=1)
