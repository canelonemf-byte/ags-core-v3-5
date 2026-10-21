"""Re-chequeo ADJ-02: ¿puede un flagelo bacteriano resonar en agua? Estimación de orden de magnitud original.
Varilla de Euler-Bernoulli (modo fundamental en voladizo) frente a arrastre de Stokes (teoría de fuerza resistiva)."""
import json, numpy as np
eta, rho_w = 1e-3, 1000.0           # agua, Pa s, kg/m3
L, a = 10e-6, 10e-9                 # longitud y radio del filamento
EI = 3.5e-22                        # rigidez a flexión del flagelo, N m^2 (orden de magnitud de la literatura; ver fuentes)
rho = 1350.0                        # densidad proteína
mu = rho*np.pi*a**2 + rho_w*np.pi*a**2   # masa por longitud + masa añadida
zeta = 4*np.pi*eta/(np.log(L/a)+0.5)     # coeficiente de arrastre normal por unidad de longitud (RFT)
w0 = (1.875**2)*np.sqrt(EI/(mu*L**4))     # frecuencia natural sin amortiguamiento (voladizo)
Q = mu*w0/zeta; tau_relax = zeta*L**4/(1.875**4*EI)
Re = rho_w*(w0*a)*a/eta
r = {"omega0_rad_s":w0,"f0_Hz":w0/2/np.pi,"Q":Q,"tau_relajacion_s":tau_relax,"Re_aprox":Re,
     "conclusion":"Q<<1: el filamento está sobreamortiguado; no existe resonancia mecánica aguda que explotar"}
print(json.dumps(r,indent=1)); json.dump(r,open("out/x4_recheck_flagelo.json","w"),indent=1)
