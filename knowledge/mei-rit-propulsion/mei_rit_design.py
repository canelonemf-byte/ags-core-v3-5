#!/usr/bin/env python3
"""MEI-RIT proto1 — diseño funcional 13.56 MHz ICP + I2.
Clase E2 (proyección de ingeniería). No es ensayo.
Uso: python3 mei_rit_design.py
"""
from __future__ import annotations
import json, math
from dataclasses import dataclass, asdict, field
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("/home/workdir/artifacts")
G0 = 9.80665
Q = 1.602176634e-19
U = 1.66053906660e-27
M_I = 126.90447 * U
M_I2 = 2.0 * M_I
EPS0 = 8.8541878128e-12
MU0 = 1.25663706212e-6
ME = 9.1093837e-31
C0 = 299792458.0
K_B = 1.380649e-23

LIT = dict(D_e=1.542, IP_I2=9.31, IP_I=10.45, IP_diss=11.63, D_I2p=2.18, EA_I=3.059)


@dataclass
class Geo:
    f_hz: float = 13.56e6
    d_ch_i_m: float = 0.032
    t_wall_m: float = 0.0015
    l_ch_m: float = 0.036
    d_grid_m: float = 0.028
    n_coil: int = 5
    d_wire_m: float = 0.0016
    pitch_m: float = 0.0045
    p_ring_m: float = 0.008
    fill_ring: float = 0.45
    t_ald_m: float = 150e-9
    t_metal_ring_m: float = 20e-6
    d_sg_m: float = 1.1e-3
    d_ag_m: float = 0.70e-3
    t_sg_m: float = 0.3e-3
    t_ag_m: float = 0.5e-3
    gap_m: float = 0.60e-3
    open_frac: float = 0.55

    @property
    def r_i(self) -> float:
        return 0.5 * self.d_ch_i_m

    @property
    def r_coil(self) -> float:
        return self.r_i + self.t_wall_m + 0.5 * self.d_wire_m

    @property
    def l_coil(self) -> float:
        return max(self.n_coil * self.pitch_m, self.d_wire_m)

    @property
    def a_grid(self) -> float:
        return math.pi * (0.5 * self.d_grid_m) ** 2


@dataclass
class Op:
    P_rf_fwd_w: float = 40.0
    eta_match: float = 0.88
    V_b_v: float = 1200.0
    V_acc_v: float = -200.0
    T_e_eV: float = 4.5
    n_e_m3: float = 1.2e17
    eta_m: float = 0.68
    f_I2plus: float = 0.12
    P_pp_other_w: float = 18.0  # PPU, heaters, cathode


def f_pe(n: float) -> float:
    return (1.0 / (2.0 * math.pi)) * math.sqrt(n * Q * Q / (EPS0 * ME))


def delta_inertial(n: float) -> float:
    return C0 / (2.0 * math.pi * f_pe(n))


def L_solenoid(geo: Geo) -> float:
    # Wheeler-ish short solenoid
    r, l, n = geo.r_coil, geo.l_coil, geo.n_coil
    return MU0 * n * n * math.pi * r * r / (l + 0.9 * r)


def C_tune(L: float, f: float) -> float:
    w = 2.0 * math.pi * f
    return 1.0 / (w * w * L)


def skin_cu(f: float) -> float:
    # Cu sigma 5.8e7
    return math.sqrt(2.0 / (MU0 * 5.8e7 * 2.0 * math.pi * f))


def fractions(op: Op) -> dict:
    f2 = max(0.0, min(0.4, op.f_I2plus))
    f1 = 1.0 - f2
    mbar = f1 * M_I + f2 * M_I2
    return dict(f_Iplus=f1, f_I2plus=f2, mbar=mbar, mbar_u=mbar / U)


def beam(geo: Geo, op: Op) -> dict:
    fr = fractions(op)
    P_abs = op.P_rf_fwd_w * op.eta_match
    vi = math.sqrt(2.0 * Q * op.V_b_v / fr["mbar"])
    isp_ion = vi / G0
    isp_sys = op.eta_m * isp_ion
    wpa = 480.0
    I_b_max_rf = P_abs / wpa
    # punto de diseño: ~16 mA (1 mN class, grid 28 mm). No gastar todo el RF en I_b.
    I_b_des = 0.016
    I_b = min(I_b_des * (op.P_rf_fwd_w / 40.0) ** 0.55, 0.85 * I_b_max_rf, 0.028)
    mdot_ion = I_b * fr["mbar"] / Q
    mdot_tot = mdot_ion / max(op.eta_m, 0.05)
    T = mdot_ion * vi
    P_beam = I_b * op.V_b_v
    P_sys = op.P_rf_fwd_w + P_beam / 0.90 + op.P_pp_other_w
    # Child-Langmuir per open area (I+)
    d = geo.gap_m
    cl = (4.0 / 9.0) * EPS0 * math.sqrt(2.0 * Q / M_I) * (op.V_b_v ** 1.5) / (d * d)
    I_cl = cl * geo.a_grid * geo.open_frac
    j_beam = I_b / max(geo.a_grid, 1e-9)
    return dict(
        P_abs_w=P_abs,
        I_b_mA=I_b * 1e3,
        I_cl_mA=I_cl * 1e3,
        j_mA_cm2=j_beam * 1e-1,
        T_mN=T * 1e3,
        Isp_ion_s=isp_ion,
        Isp_sys_s=isp_sys,
        mdot_ion_ugs=mdot_ion * 1e9,
        mdot_tot_ugs=mdot_tot * 1e9,
        P_beam_w=P_beam,
        P_sys_w=P_sys,
        T_over_P_mN_kW=T * 1e3 / max(P_sys, 1e-6) * 1e3,
        eta_tot=0.5 * T * vi / max(P_sys, 1e-6),
        vi_km_s=vi * 1e-3,
        cl_ok=I_b < 0.7 * I_cl,
        **{k: fr[k] for k in ("f_Iplus", "f_I2plus", "mbar_u")},
    )


def coupling(geo: Geo, op: Op) -> dict:
    n = op.n_e_m3
    di = delta_inertial(n)
    ratio = di / geo.r_i
    ok_skin = 0.45 <= ratio <= 1.35
    L = L_solenoid(geo)
    Ct = C_tune(L, geo.f_hz)
    # ring electrical size
    p_l = geo.p_ring_m * geo.f_hz / C0
    rf_scale_ok = 3e-3 <= geo.p_ring_m <= 15e-3
    # Lorentz matching residual (E1)
    f0 = geo.f_hz * (1.0 - 4e-4 * (geo.t_ald_m / 150e-9 - 1.0))
    gamma = 3.5e5
    eta_rf = 0.86 * (0.5 * gamma) ** 2 / ((geo.f_hz - f0) ** 2 + (0.5 * gamma) ** 2)
    eta_rf *= math.exp(-8e5 * geo.t_ald_m)
    return dict(
        f_pe_GHz=f_pe(n) / 1e9,
        delta_in_mm=di * 1e3,
        delta_over_R=ratio,
        skin_ok=ok_skin,
        L_coil_nH=L * 1e9,
        C_tune_pF=Ct * 1e12,
        skin_cu_um=skin_cu(geo.f_hz) * 1e6,
        p_over_lambda=p_l,
        rf_scale_ok=rf_scale_ok,
        eta_rf_lorentz=eta_rf,
        lambda_m=C0 / geo.f_hz,
        B_ecr_mT=2.0 * math.pi * geo.f_hz * ME / Q * 1e3,
    )


def checks(geo: Geo, op: Op, b: dict, c: dict) -> list:
    out = []
    def add(ok, msg):
        out.append(dict(ok=bool(ok), msg=msg))
    add(abs(geo.f_hz - 13.56e6) < 1.0, "f=13.56 MHz congelada")
    add(c["skin_ok"], f"delta/R={c['delta_over_R']:.2f} en [0.45,1.35]")
    add(c["rf_scale_ok"], f"periodo anillo {geo.p_ring_m*1e3:.1f} mm")
    add(c["p_over_lambda"] < 0.01, "anillo es lumped, no FSS")
    add(4 <= geo.n_coil <= 8, f"N={geo.n_coil} vueltas")
    add(b["cl_ok"], f"I_b {b['I_b_mA']:.1f} mA < 0.7 I_CL {b['I_cl_mA']:.0f} mA")
    add(0.7 <= b["T_mN"] <= 1.35, f"T={b['T_mN']:.2f} mN en banda objetivo")
    add(2200 <= b["Isp_sys_s"] <= 2900, f"Isp_sys={b['Isp_sys_s']:.0f} s en banda")
    add(b["P_sys_w"] <= 95, f"P_sys={b['P_sys_w']:.0f} W")
    add(geo.t_ald_m >= 50e-9, "ALD >= 50 nm")
    add(op.eta_m >= 0.55, "eta_m>=0.55 (I2 molecular)")
    return out


def sweep_power(geo: Geo, op: Op) -> tuple:
    Ps = np.linspace(20.0, 70.0, 26)
    T, Isp, eta = [], [], []
    for p in Ps:
        o = Op(**{**op.__dict__, "P_rf_fwd_w": float(p)})
        b = beam(geo, o)
        T.append(b["T_mN"])
        Isp.append(b["Isp_sys_s"])
        eta.append(b["eta_tot"])
    return Ps, np.array(T), np.array(Isp), np.array(eta)


def plots(geo: Geo, op: Op, path: Path) -> str:
    Ps, T, Isp, eta = sweep_power(geo, op)
    fig, ax = plt.subplots(1, 3, figsize=(10.2, 3.2), dpi=140)
    ax[0].plot(Ps, T, color="#1f4e79", lw=2)
    ax[0].axhspan(0.7, 1.3, color="#1f4e79", alpha=0.08)
    ax[0].set_xlabel("P_RF fwd (W)")
    ax[0].set_ylabel("T (mN)")
    ax[0].set_title("Empuje (E2)")
    ax[0].grid(True, alpha=0.3)
    ax[1].plot(Ps, Isp, color="#8b1e3f", lw=2)
    ax[1].axhspan(2300, 2800, color="#8b1e3f", alpha=0.08)
    ax[1].set_xlabel("P_RF fwd (W)")
    ax[1].set_ylabel("Isp sistema (s)")
    ax[1].set_title("Isp con eta_m e I2+")
    ax[1].grid(True, alpha=0.3)
    ax[2].plot(Ps, 100 * eta, color="#2e7d32", lw=2)
    ax[2].set_xlabel("P_RF fwd (W)")
    ax[2].set_ylabel("eta_tot (%)")
    ax[2].set_title("eta = T v / (2 P_sys)")
    ax[2].grid(True, alpha=0.3)
    fig.suptitle("MEI-RIT proto1 13.56 MHz — proyección, no medida", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close()
    return str(path)


def card(geo: Geo, op: Op) -> dict:
    c = coupling(geo, op)
    b = beam(geo, op)
    ck = checks(geo, op, b, c)
    return dict(
        meta=dict(id="mei-rit-proto1", f_hz=geo.f_hz, fecha="2026-09-22", clase="E2"),
        geo=asdict(geo),
        op=asdict(op),
        coupling=c,
        beam=b,
        lit_eV=LIT,
        checks=ck,
        pass_n=sum(1 for x in ck if x["ok"]),
        fail_n=sum(1 for x in ck if not x["ok"]),
        nota="P_beam sale de PPU HV, no de la bobina. I_b limitado por pérdida de descarga 480 W/A.",
    )


if __name__ == "__main__":
    geo, op = Geo(), Op()
    d = card(geo, op)
    jp = OUT / "llp/proyectos/MEI-RIT_proto1_card.json"
    jp.parent.mkdir(parents=True, exist_ok=True)
    jp.write_text(json.dumps(d, indent=2), encoding="utf-8")
    png = OUT / "MEI-RIT_proto1_map.png"
    plots(geo, op, png)
    print(json.dumps({
        "pass": d["pass_n"], "fail": d["fail_n"],
        "T_mN": round(d["beam"]["T_mN"], 3),
        "Isp_sys_s": round(d["beam"]["Isp_sys_s"], 1),
        "I_b_mA": round(d["beam"]["I_b_mA"], 2),
        "P_sys_w": round(d["beam"]["P_sys_w"], 1),
        "L_nH": round(d["coupling"]["L_coil_nH"], 1),
        "C_pF": round(d["coupling"]["C_tune_pF"], 1),
        "delta_over_R": round(d["coupling"]["delta_over_R"], 3),
        "card": str(jp),
        "plot": str(png),
        "fails": [x["msg"] for x in d["checks"] if not x["ok"]],
    }, indent=2))
