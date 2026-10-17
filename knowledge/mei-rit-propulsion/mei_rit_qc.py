#!/usr/bin/env python3
"""MEI-RIT v2.1-QC — MRCO + 0D I2 + PES + QUBO. Sin Qiskit.
Valores experimentales: literatura (Lafleur 2022, IOP 2025). No son medidas MEI-RIT.
"""
from __future__ import annotations
import json, math
from dataclasses import dataclass, asdict
import numpy as np

G0 = 9.80665
Q_E = 1.602176634e-19
M_U = 1.66053906660e-27
M_I = 126.90447 * M_U
M_I2 = 2 * M_I
C0 = 299792458.0

# --- literatura (E6 umbrales) ---
LIT = {
    "D_e_I2_eV": 1.542,
    "IP_I2_eV": 9.31,
    "IP_I2_dissoc_eV": 11.63,
    "IP_I_eV": 10.45,
    "D_e_I2plus_eV": 2.18,
    "EA_I_eV": 3.059,
    "omega_e_I2_cm": 214.5,
    "r_e_I2_A": 2.666,
}

@dataclass
class RfCell:
    f_hz: float = 13.56e6
    period_m: float = 8e-3
    fill: float = 0.45
    t_metal_m: float = 20e-6
    t_ald_m: float = 150e-9
    eps_r_ald: float = 7.0  # Si3N4 ~7, Al2O3 ~9.8

    def lambda0(self) -> float:
        return C0 / self.f_hz

    def electrical_size(self) -> float:
        return self.period_m / self.lambda0()

    def ok_rf_scale(self) -> bool:
        return 3e-3 <= self.period_m <= 15e-3 and self.electrical_size() < 0.15


def lorentz_eta(f: float, f0: float, gamma: float, eta_inf: float, t_ald: float, alpha: float = 8e5) -> float:
    den = (f - f0) ** 2 + (0.5 * gamma) ** 2
    return float(eta_inf * (0.5 * gamma) ** 2 / den * math.exp(-alpha * t_ald))


def f0_shift(cell: RfCell, f0_bare: float) -> float:
    # C_parasita ~ eps * fill * area / t_ald  → baja f0. Modelo de orden 1.
    c_par = cell.eps_r_ald * cell.fill * (cell.period_m ** 2) / max(cell.t_ald_m, 1e-9)
    return f0_bare / math.sqrt(1.0 + 2e-12 * c_par)


def mrco_cost(cell: RfCell, f0_bare: float = 13.56e6, gamma: float = 4e5, eta_inf: float = 0.82) -> dict:
    f0 = f0_shift(cell, f0_bare)
    eta = lorentz_eta(cell.f_hz, f0, gamma, eta_inf, cell.t_ald_m)
    size_pen = 0.0 if cell.ok_rf_scale() else 5.0 + 50.0 * abs(math.log10(max(cell.electrical_size(), 1e-12)))
    sputter = 0.0 if cell.t_ald_m >= 50e-9 else 2.0
    J = (1.0 - eta) + size_pen + sputter
    return {"eta_rf": eta, "f0": f0, "electrical_size": cell.electrical_size(), "J": J, "ok_rf_scale": cell.ok_rf_scale()}


def beam_performance(P_beam_w: float, V_b: float, f_Iplus: float, f_I2plus: float) -> dict:
    f_Iplus = max(0.0, min(1.0, f_Iplus))
    f_I2plus = max(0.0, min(1.0 - f_Iplus, f_I2plus))
    mbar = f_Iplus * M_I + f_I2plus * M_I2
    if mbar <= 0 or V_b <= 0:
        return {"T_mN": 0.0, "Isp_s": 0.0, "m_dot_kg_s": 0.0}
    vi = math.sqrt(2 * Q_E * V_b / mbar)
    I_b = P_beam_w / V_b
    m_dot = (I_b / Q_E) * mbar
    T = m_dot * vi
    return {"T_mN": T * 1e3, "Isp_s": vi / G0, "m_dot_mg_s": m_dot * 1e6, "vi_km_s": vi * 1e-3, "mbar_u": mbar / M_U}


def zerod_fractions(T_e_eV: float, n_e: float) -> dict:
    """Fracciones heurísticas (E1), no GEC. T_e alta → más I+; T_e baja → I2 y I-."""
    x = 1.0 / (1.0 + math.exp(-(T_e_eV - 4.0)))
    f_I2plus = 0.25 * (1.0 - x)
    f_Iplus = 0.55 + 0.35 * x
    s = f_Iplus + f_I2plus
    return {"f_Iplus": f_Iplus / s, "f_I2plus": f_I2plus / s, "T_e_eV": T_e_eV, "n_e": n_e}


def morse_I2(r_A: np.ndarray) -> np.ndarray:
    De = LIT["D_e_I2_eV"]
    re = LIT["r_e_I2_A"]
    # a from omega_e: a = we * 2πc * sqrt(μ/2De)  — aproximación
    a = 1.86  # 1/Å, orden I2
    return De * (1.0 - np.exp(-a * (r_A - re))) ** 2


def qubo_cell(n: int = 8, seed: int = 7) -> dict:
    """QUBO toy: metal=1 maximiza 'perímetro de matching' con fill target 0.45.
    Sustituir Q por surrogate CST en producción."""
    rng = np.random.default_rng(seed)
    N = n * n
    fill_t = 0.45
    # greedy clasico (simulador de lo que haría QAOA/annealer)
    x = (rng.random(N) < fill_t).astype(np.int8)
    def cost(z):
        fill = z.mean()
        # vecindad 4
        g = z.reshape(n, n)
        edge = np.abs(np.diff(g, axis=0)).sum() + np.abs(np.diff(g, axis=1)).sum()
        return (fill - fill_t) ** 2 * 20.0 - 0.02 * edge
    best, cb = x.copy(), cost(x)
    for _ in range(4000):
        i = int(rng.integers(0, N))
        x[i] ^= 1
        c = cost(x)
        if c <= cb:
            cb, best = c, x.copy()
        else:
            x[i] ^= 1
    return {"n": n, "fill": float(best.mean()), "C": float(cb), "pattern": best.reshape(n, n).tolist(), "nota": "E1 toy. No CST."}


def vqe_hook() -> dict:
    return {
        "backend": "NONE_IN_SANDBOX",
        "active_space": "(10e,8o) + ECP cc-pVDZ-PP",
        "qubits_jw": 16,
        "target": "De -> 1.542 eV; no Maxwell",
        "soc": "obligatorio en I; VQE sin SOC = E1 debil",
        "status": "PENDIENTE_DE_VERIFICACION",
    }


def snapshot() -> dict:
    cell = RfCell()
    z = zerod_fractions(4.5, 1e17)
    perf = beam_performance(35.0, 1200.0, z["f_Iplus"], z["f_I2plus"])
    bad = RfCell(period_m=11.78e-6)
    return {
        "lit": LIT,
        "cell_mm": {**asdict(cell), **mrco_cost(cell)},
        "cell_um_legado": {**asdict(bad), **mrco_cost(bad)},
        "zerod": z,
        "perf_proy_E2": perf,
        "qubo": qubo_cell(),
        "vqe": vqe_hook(),
        "lambda_13p56_m": C0 / 13.56e6,
        "lambda_2p45_m": C0 / 2.45e9,
    }


if __name__ == "__main__":
    s = snapshot()
    print(json.dumps(s, indent=2))
    r = np.linspace(2.0, 4.5, 6)
    print("PES Morse I2 eV", morse_I2(r).round(3).tolist())
