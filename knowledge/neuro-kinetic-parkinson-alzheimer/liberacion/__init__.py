"""Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
Modelos clásicos de liberación controlada de fármacos (cinética in vitro), para dimensionar protocolos.
- Higuchi T. (1963) J. Pharm. Sci. 52, 1145, doi:10.1002/jps.2600521210: Q(t) = k_H * sqrt(t).
- Orden cero y primer orden: modelos cinéticos estándar.
No es un modelo clínico ni sustituye ensayos; los parámetros deben salir de medidas de laboratorio.
"""
import numpy as np


def higuchi(t, k_h):
    return np.minimum(k_h * np.sqrt(np.asarray(t, float)), 1.0)


def zero_order(t, k0):
    return np.minimum(k0 * np.asarray(t, float), 1.0)


def first_order(t, k1):
    return 1 - np.exp(-k1 * np.asarray(t, float))


def fit_higuchi(t, frac):
    """Ajuste por mínimos cuadrados de k_H con datos (t, fracción liberada)."""
    s = np.sqrt(np.asarray(t, float))
    return float(np.dot(s, frac) / np.dot(s, s))


def time_to_fraction(frac, model, k):
    if model == "higuchi":
        return (frac / k) ** 2
    if model == "zero":
        return frac / k
    if model == "first":
        return -np.log(1 - frac) / k
    raise ValueError(model)
