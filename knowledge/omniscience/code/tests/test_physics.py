"""Comprobaciones derivables del propio código. NO validan el modelo frente a experimento:
solo verifican que lo que el código dibuja cumple las relaciones que el propio código declara."""
import numpy as np
import pytest

pytestmark = pytest.mark.physics


def lines(fig, ax_index=0):
    return fig.axes[ax_index].get_lines()


def test_string_modes_period_fn_equals_n_f1():
    import animar_modos as am
    t = np.linspace(0, 1, 7)
    for n in am.Ns:
        if am.cs[n - 1] == 0:
            continue
        # f1 = omega1 / 2π = 1 Hz → el modo n repite con periodo 1/n  (fn = n·f1)
        for tt in t:
            np.testing.assert_allclose(am.y_mode(n, tt + 1.0 / n), am.y_mode(n, tt), atol=1e-9)
        # extremos fijos (Dirichlet)
        y = am.y_mode(n, 0.0)
        assert abs(y[0]) < 1e-12 and abs(y[-1]) < 1e-9


def test_string_mode_figure_has_n_minus_1_interior_nodes(captured):
    sv, figs = captured
    sv.fig_modes_string()
    fig = figs["03_modos_cuerda.png"]
    for n, ax in enumerate(fig.axes, start=1):
        y = ax.get_lines()[0].get_ydata()[1:-1]
        crossings = np.sum(np.sign(y[:-1]) != np.sign(y[1:]))
        assert crossings == n - 1


def test_phonon_dispersion_limits(captured):
    sv, figs = captured
    sv.fig_phonon_dispersion()
    fig = figs["04_dispersion_fononica.png"]
    ka = lines(fig, 0)[0].get_xdata()
    mono = lines(fig, 0)[0].get_ydata()
    assert mono.max() == pytest.approx(2.0, rel=1e-4)       # ω_max = 2√(K/m) con K=m=1
    assert mono[np.argmin(np.abs(ka))] < 0.02                # ω(k→0) → 0
    ac, op = (l.get_ydata() for l in lines(fig, 1)[:2])
    assert np.all(op >= ac)                                  # rama óptica por encima de la acústica
    m1, m2 = 1.0, 2.2                                        # valores del propio código
    edge = np.argmax(np.abs(ka))
    # en el borde de zona: ω_ac = √(2K/m2), ω_op = √(2K/m1)  (normalizado por ω_op,max = √(2K(1/m1+1/m2)))
    wmax = np.sqrt(2 * (1 / m1 + 1 / m2))
    assert ac[edge] == pytest.approx(np.sqrt(2 / m2) / wmax, rel=1e-3)
    assert op[edge] == pytest.approx(np.sqrt(2 / m1) / wmax, rel=1e-3)


def test_phononic_crystal_transmission_is_bounded(captured):
    sv, figs = captured
    sv.fig_phononic_crystal_1d()
    T = lines(figs["05_cristal_fononico_T.png"])[0].get_ydata()
    assert T.min() >= 0
    assert T.max() <= 1 + 1e-6                               # medio sin pérdidas: |T|² ≤ 1
    assert T.min() < 0.1                                     # existen bandas prohibidas


def test_quality_factor_bandwidth(captured):
    sv, figs = captured
    sv.fig_quality_and_bandwidth()
    fig = figs["08_factor_calidad.png"]
    f0 = 1000.0
    for ln, Q in zip(lines(fig), [5, 15, 50, 200]):
        f, P = ln.get_xdata(), ln.get_ydata()
        # pico en f0 (P=1); la rejilla (paso 0.4 Hz) no contiene f0 exacto → máximo muestreado algo < 1
        df = f[1] - f[0]
        assert abs(f[np.argmax(P)] - f0) <= df
        assert 0.99 < P.max() <= 1.0
        if Q >= 50:                                          # Δf ≈ f0/Q (aprox. válida para Q alto)
            above = f[P >= 0.5]
            assert above.max() - above.min() == pytest.approx(f0 / Q, rel=0.12)


def test_coupled_oscillators_normal_modes(captured):
    sv, figs = captured
    sv.fig_coupled_oscillators()
    fig = figs["09_osciladores_acoplados.png"]
    t = lines(fig, 0)[0].get_xdata()
    s, a = (l.get_ydata() for l in lines(fig, 2)[:2])
    np.testing.assert_allclose(s, 2 * np.cos(1.0 * t), atol=1e-12)
    np.testing.assert_allclose(a, 2 * np.cos(1.35 * t), atol=1e-12)


def test_qho_levels_equally_spaced(captured):
    sv, figs = captured
    sv.fig_qho()
    fig = figs["07_oscilador_cuantico.png"]
    E = sorted({round(float(l.get_ydata()[0]), 9) for l in lines(fig)
                if np.ptp(l.get_ydata()) == 0})
    assert E[:6] == pytest.approx([n + 0.5 for n in range(6)])   # E_n = (n+½)ħω


def test_mv1_dft_fallback_on_anomalous_force(monkeypatch):
    import omniscience_mv1 as mv1
    s = mv1.CrystalStructure("Si2", np.eye(3) * 5.4, np.zeros((2, 3)), ["Si", "Si"])
    w = mv1.OmniscienceMV1Workflow("TEST")
    monkeypatch.setattr(w.matter_engine, "calculate_supercell_forces_mlip",
                        lambda sc: np.full((8, 3), 50.0))
    res = w.run_campaign(s)
    assert any("Fallback Adversarial a DFT" in x and "REVISION" in x for x in res["provenance_trace"])
    # NOTA: en MV1 las fuerzas y frecuencias son un surrogate aleatorio; 'verified_prediction'
    # aquí no es un resultado físico.
