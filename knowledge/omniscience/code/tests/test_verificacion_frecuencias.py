"""Tests de la ADICIÓN NUEVA verificacion_frecuencias.py (no del código original). H3, maestro.tex:551/624."""
import numpy as np
from verificacion_frecuencias import frecuencias_cuerda

def test_fn_igual_n_f1_numerico():
    f, f1 = frecuencias_cuerda(n_modos=6)
    n = np.arange(1, 7)
    assert np.all(np.abs(f - n * f1) / (n * f1) < 1e-4)
