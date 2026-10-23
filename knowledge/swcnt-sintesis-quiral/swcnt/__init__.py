"""Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
Geometría de nanotubos de carbono de pared simple a partir de los índices quirales (n, m).
Fórmulas estándar: Saito et al. (1992) Appl. Phys. Lett. 60, 2204, doi:10.1063/1.107080.
"""
import math
A_CC = 0.142  # nm, distancia C-C en grafeno
A = A_CC * math.sqrt(3)  # nm, constante de red del grafeno (~0,246)


def diameter_nm(n, m):
    return A * math.sqrt(n * n + n * m + m * m) / math.pi


def chiral_angle_deg(n, m):
    return math.degrees(math.atan(math.sqrt(3) * m / (2 * n + m)))


def is_metallic(n, m):
    """Regla de bandas en el modelo de enlace fuerte: metálico si (n - m) es múltiplo de 3."""
    return (n - m) % 3 == 0


def kind(n, m):
    if m == 0:
        return "zigzag"
    if n == m:
        return "armchair"
    return "chiral"


def candidates(d_min, d_max, semiconducting=True, n_max=30):
    """Lista (n, m) con diámetro en [d_min, d_max] nm, útil para fijar objetivos de síntesis quiral."""
    out = []
    for n in range(1, n_max + 1):
        for m in range(0, n + 1):
            d = diameter_nm(n, m)
            if d_min <= d <= d_max and (is_metallic(n, m) != semiconducting):
                out.append({"n": n, "m": m, "d_nm": round(d, 4), "angulo_deg": round(chiral_angle_deg(n, m), 2), "tipo": kind(n, m)})
    return out
