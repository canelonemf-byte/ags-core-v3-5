"""liberacion: cinética de liberación (Korsmeyer-Peppas, Higuchi) y estabilidad (Arrhenius), con las ecuaciones que usan los documentos del autor.
Fuentes: Korsmeyer R.W. et al. (1983) Int. J. Pharm. 15, 25, doi:10.1016/0378-5173(83)90064-9; Ritger P.L., Peppas N.A. (1987) J. Control. Release 5, 23, doi:10.1016/0168-3659(87)90034-4; Higuchi T. (1963) J. Pharm. Sci. 52, 1145, doi:10.1002/jps.2600521210.
Modelo in vitro; no es un modelo clínico. Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np

R_GAS = 8.314462618


def korsmeyer_peppas(t, k, n):
    """Mt/Minf = k t^n (válido para Mt/Minf <= 0,6)."""
    return k * np.asarray(t, float) ** n


def fit_korsmeyer_peppas(t, frac):
    """Ajuste lineal en log-log; usa solo puntos con 0 < frac <= 0,6. Devuelve (k, n)."""
    t = np.asarray(t, float); frac = np.asarray(frac, float)
    m = (t > 0) & (frac > 0) & (frac <= 0.6)
    n, lk = np.polyfit(np.log(t[m]), np.log(frac[m]), 1)
    return float(np.exp(lk)), float(n)


def mechanism(n, geometry="slab"):
    """Clasificación de Ritger y Peppas (1987): lámina 0,5 / 1,0; cilindro 0,45 / 0,89; esfera 0,43 / 0,85."""
    lo, hi = {"slab": (0.5, 1.0), "cylinder": (0.45, 0.89), "sphere": (0.43, 0.85)}[geometry]
    if n <= lo + 1e-9:
        return "fickiana"
    if n < hi - 1e-9:
        return "anómala (no fickiana)"
    return "caso II (orden cero)"


def higuchi_q(D, Cs, A, t):
    """Ecuación de Higuchi (1963): Q = sqrt(D Cs (2A - Cs) t), con A > Cs."""
    return np.sqrt(D * Cs * (2 * A - Cs) * np.asarray(t, float))


def arrhenius(A, Ea, T):
    """k = A exp(-Ea / (R T)), Ea en J/mol, T en K."""
    return A * np.exp(-Ea / (R_GAS * np.asarray(T, float)))
