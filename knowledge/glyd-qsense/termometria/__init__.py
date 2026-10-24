"""termometria: termometría Raman. Incluye la temperatura absoluta por cociente anti-Stokes/Stokes, I_AS/I_S = ((ν0+ν)/(ν0−ν))^4 · exp(−hcν/kT) (Rassat y Davis 1994); la calibración lineal de un parámetro espectral frente a T; y las figuras de mérito S_r = |dX/dT|/X y δT = σ_X/|dX/dT| (Brites et al. 2012). La precisión de 0,08 °C del documento solo podrá confirmarse con los espectros reales.

Referencias (verificadas):
Brites C.D.S. et al. (2012) Thermometry at the nanoscale. Nanoscale 4, 4799. doi:10.1039/C2NR30663H
Rassat S.D., Davis E.J. (1994) Temperature Measurement of Single Levitated Microparticles Using Stokes/Anti-Stokes Raman Intensity Ratios. Applied Spectroscopy 48, 1498. doi:10.1366/0003702944027921

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia: CC BY-NC-ND 4.0 (ver LICENSE).
"""
import numpy as np
from .pendientes import cargar, dato

HC_K = 1.438776877  # hc/k en cm·K


def temp_antistokes_stokes(ratio, shift_cm, laser_cm):
    pref = ((laser_cm + shift_cm) / (laser_cm - shift_cm)) ** 4
    return HC_K * shift_cm / np.log(pref / ratio)


def calibracion_lineal(T, X):
    b, a = np.polyfit(T, X, 1)
    return a, b


def figuras_merito(T, X, sigma_X):
    a, b = calibracion_lineal(T, X)
    Xm = a + b * np.mean(T)
    return {"pendiente": b, "S_r_por_K": abs(b) / abs(Xm), "delta_T_K": sigma_X / abs(b)}


def run(cfg=None):
    cfg = cfg or cargar()
    T = np.asarray(dato(cfg, "temperaturas_calibracion_k")[0], float); X = np.asarray(dato(cfg, "parametro_espectral")[0], float)
    s = float(dato(cfg, "sigma_parametro")[0])
    if len(T) != len(X) or len(T) < 3:
        raise ValueError("se necesitan al menos 3 pares (T, X) de igual longitud")
    return figuras_merito(T, X, s)
