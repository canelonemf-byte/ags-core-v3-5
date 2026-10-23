"""oraculo: conductancia mesoscópica de Landauer, G = (2e²/h)·Σ T_n, con propagación Monte Carlo de la incertidumbre. Cada salida da media, intervalo del 95 %, supuestos y límites, que es lo que pide el alcance declarado.

Referencias (verificadas):
van Wees B.J. et al. (1988) Quantized conductance of point contacts in a two-dimensional electron gas. Phys. Rev. Lett. 60, 848. doi:10.1103/PhysRevLett.60.848

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato

G0 = 2 * (1.602176634e-19) ** 2 / 6.62607015e-34


def landauer(T):
    T = np.asarray(T, float)
    if np.any((T < 0) | (T > 1)):
        raise ValueError("cada transmisión debe estar en [0, 1]")
    return G0 * T.sum(axis=-1)


def predecir(T_media, T_sigma, n=20000, seed=0):
    rng = np.random.default_rng(seed)
    S = np.clip(rng.normal(T_media, T_sigma, size=(n, len(T_media))), 0, 1)
    g = landauer(S)
    return {"G_media_S": float(g.mean()), "ic95_S": [float(x) for x in np.percentile(g, [2.5, 97.5])],
            "supuestos": "transporte coherente, canales independientes, T_n gaussianas truncadas", "limites": "no incluye interacción ni temperatura"}


def run(cfg=None):
    cfg = cfg or cargar()
    return predecir(dato(cfg, "transmisiones_media")[0], dato(cfg, "transmisiones_sigma")[0])
