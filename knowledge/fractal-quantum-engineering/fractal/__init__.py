"""fractal: dimensión fractal por conteo de cajas (modelo de referencia público, no los datos del autor). Sustituye el ejemplo de Sierpinski por el patrón real en datos_pendientes.yaml.

Referencias (verificadas):
Mandelbrot B. (1967) How Long Is the Coast of Britain? Statistical Self-Similarity and Fractional Dimension. Science 156, 636. doi:10.1126/science.156.3775.636

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import numpy as np
from .pendientes import cargar, dato, DatoPendiente


def box_counting_dimension(mask, sizes=None):
    """Dimensión fractal por conteo de cajas de una matriz booleana 2D (Mandelbrot 1967)."""
    m = np.asarray(mask, bool)
    n = min(m.shape)
    if sizes is None:
        sizes = [s for s in (2 ** np.arange(0, int(np.log2(n)))) if s < n]
    counts = []
    for s in sizes:
        h, w = (m.shape[0] // s) * s, (m.shape[1] // s) * s
        b = m[:h, :w].reshape(h // s, s, w // s, s).any(axis=(1, 3))
        counts.append(b.sum())
    slope = np.polyfit(np.log(1 / np.asarray(sizes, float)), np.log(counts), 1)[0]
    return float(slope)


def sierpinski_carpet(level):
    c = np.ones((1, 1), bool)
    for _ in range(level):
        z = np.zeros_like(c)
        c = np.block([[c, c, c], [c, z, c], [c, c, c]])
    return c


def cargar_patron(ruta):
    if ruta.endswith(".npy"):
        return np.load(ruta) > 0
    return np.loadtxt(ruta, delimiter=",") > 0


def run(cfg=None):
    cfg = cfg or cargar()
    ruta, origen = dato(cfg, "ruta_patron")
    if ruta == "ejemplo:sierpinski":
        m = sierpinski_carpet(5)
    else:
        m = cargar_patron(ruta)
    D = box_counting_dimension(m, sizes=[1, 3, 9, 27, 81] if ruta == "ejemplo:sierpinski" else None)
    return {"dimension_fractal": D, "origen": origen}
