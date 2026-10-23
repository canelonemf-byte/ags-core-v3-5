"""lcpb: índice LCPB v2.0 del documento LOGARITHMUS BIOLOGICUS QUANTICUS v2.0 del autor, en numpy.
Lambda = log10( prod F_k^w_k / prod R_j^r_j * S ) + delta_fusion, con delta_fusion = log10(m / (1 - m)) (masa de creencia).

Hallazgo de la revisión: en el código original, gamma = Lambda_MCMC - log10(F/R*S) - delta, así que
Lambda_final = Lambda_MCMC para cualquier planeta. Los datos del planeta se cancelan y el ranking v2.0 no los refleja.
Aquí gamma = 0 por defecto, y circular_lambda() reproduce el defecto para documentarlo.
Muestreo Metropolis (Metropolis et al. 1953, doi:10.1063/1.1699114). Índice exploratorio, E0/E1: no está validado contra biosferas reales.
Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np


def delta_fusion(m):
    return float(np.log10(m / (1 - m)))


def lcpb(F, R, S=1.0, omega=None, rho=None, m=0.5, gamma=0.0):
    F = np.asarray(F, float); R = np.asarray(R, float)
    omega = np.ones_like(F) if omega is None else np.asarray(omega, float)
    rho = np.ones_like(R) if rho is None else np.asarray(rho, float)
    arg = np.prod(F ** omega) / np.prod(R ** rho) * S
    return float(np.log10(arg) + delta_fusion(m) + gamma)


def circular_lambda(F, R, S, m, lambda_mcmc):
    """Reproduce el cálculo original: siempre devuelve lambda_mcmc."""
    g = lambda_mcmc - lcpb(F, R, S, m=m)
    return lcpb(F, R, S, m=m, gamma=g)


def metropolis_gaussian(mu, sigma, n=20000, step=0.5, lo=-4, hi=3, seed=0):
    rng = np.random.default_rng(seed)
    lp = lambda x: -np.inf if (x < lo or x > hi) else -0.5 * ((x - mu) / sigma) ** 2
    x = 0.0; out = np.empty(n)
    for i in range(n):
        p = x + rng.normal(0, step)
        if np.log(rng.random()) < lp(p) - lp(x):
            x = p
        out[i] = x
    return out
