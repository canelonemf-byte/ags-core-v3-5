"""Tests sobre la salida REAL de simular_vibraciones.py (datos extraídos de las figuras).
Referencias: knowledge/omniscience/OMNISCIENCE_maestro.tex, líneas 549-554 (criterios de falsación H1-H6)
y 581-671 (conclusiones declaradas)."""
import hashlib, subprocess, sys, pathlib
import numpy as np
import pytest

OMEGA0 = 2 * np.pi * 0.8
ZETA = 0.08

# ---- H1 (tex:549, 581): amplitud/fase del oscilador forzado amortiguado ----
def test_h1_pico_resonancia_en_omega_r(capture):
    fig = capture("fig_shm_damped_driven")
    x, y = fig.axes[1].lines[0].get_data()
    wr = np.sqrt(1 - 2 * ZETA**2)               # pico de amplitud teórico (en ω/ω0)
    assert abs(x[np.argmax(y)] - wr) < 2 * (x[1] - x[0])

def test_h1_fase_pi_medios_en_resonancia(capture):
    fig = capture("fig_shm_damped_driven")
    x, ph = fig.axes[3].lines[0].get_data()
    assert abs(np.interp(1.0, x, ph) - np.pi / 2) < 0.02

def test_h1_amplitud_estacionaria_ode_vs_formula(capture):
    fig = capture("fig_shm_damped_driven")
    t, xt = fig.axes[2].lines[0].get_data()
    a_num = np.max(np.abs(xt[t > 20]))
    a_teo = 1.0 / (2 * ZETA * OMEGA0**2)          # F0/m=1, forzado en ω0
    assert abs(a_num - a_teo) / a_teo < 0.02

# ---- H2 (tex:550, 592): burst de 320 Hz solo tras t=2,2 s ----
def test_h2_burst_320hz_aparece_tras_2_2s(capture):
    fig = capture("fig_fft_spectrogram")
    qm = fig.axes[2].collections[0]
    C = qm.get_coordinates()                      # (nf, nt, 2)
    t = C[0, :, 0]; f = C[:, 0, 1]
    Z = np.asarray(qm.get_array()).reshape(C.shape[:2])
    i = np.argmin(np.abs(f - 320))
    antes = Z[i, (t > 0.3) & (t < 2.1)].mean(); despues = Z[i, (t > 2.25) & (t < 2.6)].mean()
    assert despues - antes > 20                   # dB

def test_h2_tono_180hz_estacionario(capture):
    fig = capture("fig_fft_spectrogram")
    qm = fig.axes[2].collections[0]; C = qm.get_coordinates()
    t = C[0, :, 0]; f = C[:, 0, 1]; Z = np.asarray(qm.get_array()).reshape(C.shape[:2])
    fila = Z[np.argmin(np.abs(f - 180)), (t > 0.3) & (t < 3.7)]
    assert fila.std() < 3                         # dB

# ---- H3 (tex:551, 624): modos de cuerda ----
@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_h3_nodos_y_vientres_modos_cuerda(capture, n):
    fig = capture("fig_modes_string")
    x, y = fig.axes[n - 1].lines[0].get_data()
    centro = np.interp(0.5, x, y)
    if n % 2 == 0:
        assert abs(centro) < 1e-2                 # nodo en L/2
    else:
        assert abs(abs(centro) - 1) < 1e-3        # vientre en L/2
    interior = y[1:-1]
    assert np.sum(np.diff(np.sign(interior)) != 0) == n - 1

# f_n = n·f_1 (H3): cubierto en la versión canónica por test_physics.py::test_string_modes_period_fn_equals_n_f1
# (animar_modos.y_mode) y por test_verificacion_frecuencias.py. Se retira el xfail de ORÁCULO.

# ---- H4 (tex:552, 647): ramas acústica/óptica ----
def test_h4_gap_diatomico_en_borde_de_zona(capture):
    fig = capture("fig_phonon_dispersion")
    ax = fig.axes[1]
    k, ac = ax.lines[0].get_data(); _, op = ax.lines[1].get_data()
    i = np.argmax(k)                              # k = π/a
    assert ac[i] < op[i]
    assert abs(ac[i] / op[i] - np.sqrt(1.0 / 2.2)) < 1e-3   # ω_ac/ω_op = sqrt(m1/m2) en π/a

def test_h4_monoatomica_omega_max_2(capture):
    fig = capture("fig_phonon_dispersion")
    _, w = fig.axes[0].lines[0].get_data()
    assert abs(w.max() - 2.0) < 1e-3

# ---- H5 (tex:553, 647): cristal fonónico 1D ----
def test_h5_bandas_de_rechazo(capture):
    fig = capture("fig_phononic_crystal_1d")
    _, T = fig.axes[0].lines[0].get_data()
    assert T.min() < 0.01 and T.max() > 0.9

def test_h5_conservacion_energia_T_le_1(capture):
    """Medio sin pérdidas: |t|^2 <= 1 en toda frecuencia."""
    fig = capture("fig_phononic_crystal_1d")
    _, T = fig.axes[0].lines[0].get_data()
    assert T.max() <= 1 + 1e-9

# ---- H6 (tex:554, 671): nodos del oscilador cuántico ----
def test_h6_nodos_qho(capture):
    fig = capture("fig_qho")
    ax = fig.axes[0]
    checked = 0
    for ln in ax.lines:
        lab = ln.get_label()
        if not lab.startswith("n="): continue
        n = int(lab.split(",")[0][2:]); E = n + 0.5
        x, y = ln.get_data(); d = (y - E) / (y - E).max()
        m = (np.abs(x) < 3.0)
        dd = d[m]
        mins = [j for j in range(1, len(dd) - 1) if dd[j] < dd[j - 1] and dd[j] <= dd[j + 1] and dd[j] < 1e-2]
        assert len(mins) == n, f"n={n}: {len(mins)} nodos"
        checked += 1
    assert checked >= 2

# ---- Q y ancho de banda (tex:577) ----
@pytest.mark.parametrize("idx,Q", [(1, 15), (2, 50), (3, 200)])
def test_ancho_banda_f0_sobre_Q(capture, idx, Q):
    fig = capture("fig_quality_and_bandwidth")
    f, P = fig.axes[0].lines[idx].get_data()
    # cruces de media potencia interpolados linealmente (la rejilla de 0,4 Hz es gruesa para Q=200)
    i = np.where(P >= 0.5)[0]; a, b = i[0], i[-1]
    f_lo = np.interp(0.5, [P[a - 1], P[a]], [f[a - 1], f[a]])
    f_hi = np.interp(0.5, [P[b + 1], P[b]], [f[b + 1], f[b]])
    assert abs((f_hi - f_lo) - 1000.0 / Q) / (1000.0 / Q) < 0.05

# ---- Determinismo (PUBLICACION v1.0.0 l.193: misma semilla ⇒ mismas figuras) ----
def test_determinismo_dos_ejecuciones(tmp_path):
    import os
    script = pathlib.Path(__file__).resolve().parents[1] / "simular_vibraciones.py"
    h = []
    for k in ("a", "b"):
        out = tmp_path / k
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True, env={"MPLBACKEND": "Agg", "PATH": "", "VIBRACIONES_OUT": str(out)})
        h.append({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob("*.png"))})
    assert len(h[0]) == 9 and h[0] == h[1]
