"""Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
Neurona integrar-y-disparar con fugas (LIF), el modelo base de los chips neuromórficos.
Contexto: Mead C. (1990) Proc. IEEE 78, 1629, doi:10.1109/5.58356; Davies M. et al. (2018) IEEE Micro 38, 82, doi:10.1109/MM.2018.112130359.
tau dV/dt = -(V - V_rest) + R I.
"""
import math
import numpy as np


def simulate(I, dt=1e-4, tau=20e-3, R=1e7, v_rest=-0.065, v_th=-0.050, v_reset=-0.065, t_ref=2e-3):
    """I: array de corriente (A). Devuelve (V, tiempos_de_disparo)."""
    V = np.empty(len(I)); v = v_rest; spikes = []; ref = 0.0
    for i, Ii in enumerate(I):
        if ref > 0:
            ref -= dt; v = v_reset
        else:
            v += dt / tau * (-(v - v_rest) + R * Ii)
            if v >= v_th:
                spikes.append(i * dt); v = v_reset; ref = t_ref
        V[i] = v
    return V, spikes


def rate_theory(I, tau=20e-3, R=1e7, v_rest=-0.065, v_th=-0.050, v_reset=-0.065, t_ref=2e-3):
    """Frecuencia analítica de disparo (Hz) con corriente constante."""
    vinf = v_rest + R * I
    if vinf <= v_th:
        return 0.0
    return 1.0 / (t_ref + tau * math.log((vinf - v_reset) / (vinf - v_th)))
