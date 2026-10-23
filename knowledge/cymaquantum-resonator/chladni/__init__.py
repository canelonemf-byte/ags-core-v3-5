"""chladni: modos de una placa rectangular delgada simplemente apoyada (Kirchhoff), f_mn = (π/2)·sqrt(D/(ρh))·((m/a)² + (n/b)²), con D = E h³/(12(1−ν²)), y sus líneas nodales. Modelo de referencia público, no los datos del autor; la geometría está pendiente. El ejemplo de material es aluminio.

Referencias (verificadas):
Gander M.J., Kwok F. (2012) Chladni Figures and the Tacoma Bridge: Motivating PDE Eigenvalue Problems via Vibrating Plates. SIAM Review 54, 573-596. doi:10.1137/10081931x

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato


def mode_frequency(m, n, a, b, h, E, nu, rho):
    D = E * h**3 / (12 * (1 - nu**2))
    return np.pi / 2 * np.sqrt(D / (rho * h)) * ((m / a) ** 2 + (n / b) ** 2)


def nodal_pattern(m, n, a, b, N=200):
    x = np.linspace(0, a, N); y = np.linspace(0, b, N)
    X, Y = np.meshgrid(x, y)
    return np.sin(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)


def nearest_modes(f, a, b, h, E, nu, rho, kmax=10, top=3):
    L = sorted(((abs(mode_frequency(m, n, a, b, h, E, nu, rho) - f), m, n) for m in range(1, kmax + 1) for n in range(1, kmax + 1)))
    return [(m, n, mode_frequency(m, n, a, b, h, E, nu, rho)) for _, m, n in L[:top]]


def run(cfg=None):
    cfg = cfg or cargar()
    g = {k: float(dato(cfg, k)[0]) for k in ("lado_a_m", "lado_b_m", "espesor_m", "frecuencia_excitacion_hz")}
    mat = {k: float(dato(cfg, k)[0]) for k in ("modulo_young_pa", "poisson", "densidad_kg_m3")}
    return {"modos_cercanos": nearest_modes(g["frecuencia_excitacion_hz"], g["lado_a_m"], g["lado_b_m"], g["espesor_m"], mat["modulo_young_pa"], mat["poisson"], mat["densidad_kg_m3"])}
