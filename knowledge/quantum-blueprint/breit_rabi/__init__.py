"""breit_rabi: niveles hiperfinos con J = 1/2 en un campo B (fórmula de Breit-Rabi). Completa las fórmulas de Zeeman parciales del documento. Los parámetros del material están pendientes.

Referencias (verificadas):
Breit G., Rabi I.I. (1931) Measurement of Nuclear Spin. Phys. Rev. 38, 2082. doi:10.1103/PhysRev.38.2082.2

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato

MU_B = 9.2740100783e-24; H = 6.62607015e-34


def breit_rabi(B, dE_hz, I, gJ=2.00231930436, gI=0.0):
    """Niveles (F, m_F, E en Hz) para J = 1/2 (Breit-Rabi). gI usa el convenio de Steck: H_I = gI muB I·B."""
    x = (gJ - gI) * MU_B * B / (H * dE_hz)
    c0 = -dE_hz / (4 * I + 2)
    out = []
    for m2 in range(-int(2 * I + 1), int(2 * I + 1) + 1, 2):
        m = m2 / 2
        lin = gI * MU_B * m * B / H
        if abs(abs(m) - (I + 0.5)) < 1e-9:
            out.append((I + 0.5, m, dE_hz * I / (2 * I + 1) + np.sign(m) * (gJ / 2 + gI * I) * MU_B * B / H))
            continue
        r = np.sqrt(1 + 4 * m * x / (2 * I + 1) + x * x)
        out.append((I + 0.5, m, c0 + lin + dE_hz / 2 * r))
        out.append((I - 0.5, m, c0 + lin - dE_hz / 2 * r))
    return out


def run(cfg=None):
    cfg = cfg or cargar()
    B = float(dato(cfg, "campo_b_t")[0]); dE = float(dato(cfg, "desdoblamiento_hiperfino_hz")[0]); I = float(dato(cfg, "espin_nuclear_i")[0])
    return {"niveles": breit_rabi(B, dE, I)}
