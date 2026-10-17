#!/usr/bin/env python3
"""MEI-RIT proto1 realizable — feed I2, óptica, térmica, secuencia.
E2 de ingeniería. No ensayo.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("/home/workdir/artifacts")
Q = 1.602176634e-19
U = 1.66053906660e-27
R_U = 8.314462618
M_I2 = 0.25380894  # kg/mol
GAMA = 1.30
G0 = 9.80665

def p_vap_I2(T_C: float) -> float:
    """Antoine-like (Pa). Check: 100 C ~ 6 kPa."""
    T = T_C + 273.15
    A, B, C = 3.36, 1039.0, -146.59
    return 1e5 * 10 ** (A - B / (T + C))

def sonic_mdot(P_Pa: float, T_K: float, d_m: float, Cd: float = 0.65) -> float:
    """kg/s, I2 choked orifice."""
    R = R_U / M_I2
    g = GAMA
    coef = math.sqrt(g / R) * (2.0 / (g + 1.0)) ** ((g + 1.0) / (2.0 * (g - 1.0)))
    A = Cd * math.pi * (0.5 * d_m) ** 2
    return A * P_Pa * coef / math.sqrt(T_K)

def size_orifice(mdot_kgs: float, T_C: float = 90.0, Cd: float = 0.65) -> dict:
    P = p_vap_I2(T_C)
    T = T_C + 273.15
    # invert d
    R = R_U / M_I2
    g = GAMA
    coef = math.sqrt(g / R) * (2.0 / (g + 1.0)) ** ((g + 1.0) / (2.0 * (g - 1.0)))
    A_eff = mdot_kgs * math.sqrt(T) / (P * coef)
    A = A_eff / Cd
    d = 2.0 * math.sqrt(A / math.pi)
    # capilar viscoso realizable (no joya 50 um que se tapa)
    mu = 1.8e-5
    L = 0.060
    rho = P * M_I2 / (R_U * T)
    # Hagen: m = pi r^4 rho dP / (8 mu L)
    r4 = mdot_kgs * 8.0 * mu * L / (math.pi * rho * max(P, 1.0))
    d_cap = 2.0 * r4 ** 0.25
    return dict(
        T_C=T_C, P_kPa=P / 1e3, d_sonic_um=d * 1e6, cap_d_um=d_cap * 1e6,
        cap_L_mm=L * 1e3, Cd=Cd, mdot_ugs=mdot_kgs * 1e9,
        arquitectura="capilar PTFE 60 mm + T_tank, no orificio 50 um",
    )

def grid_layout(d_grid=0.028, d_sg=0.0011, pitch=0.00150, hex_pack=True) -> dict:
    A = math.pi * (0.5 * d_grid) ** 2
    a_cell = (math.sqrt(3) / 2.0) * pitch * pitch if hex_pack else pitch * pitch
    n = int(A / a_cell)
    a_h = math.pi * (0.5 * d_sg) ** 2
    tau = n * a_h / A
    return dict(n_holes=n, pitch_mm=pitch * 1e3, tau=tau, A_grid_cm2=A * 1e4)

def perveance(I_b, V_b, d_gap=6e-4, n_holes=300, d_sg=1.1e-3):
    """Normalized perveance vs Child-Langmuir single aperture."""
    # CL one hole
    Jcl = (4.0 / 9.0) * 8.854e-12 * math.sqrt(2 * Q / (126.90447 * U)) * (V_b ** 1.5) / (d_gap ** 2)
    Icl_h = Jcl * math.pi * (0.5 * d_sg) ** 2
    return dict(Icl_hole_uA=Icl_h * 1e6, I_per_hole_uA=I_b / n_holes * 1e6, np_ratio=(I_b / n_holes) / Icl_h)

def thermal_budget() -> dict:
    # órdenes de magnitud proto lab
    return dict(
        tank_W=(3.0, 8.0),
        lines_W=(2.0, 5.0),
        coil_loss_W=(3.0, 8.0),
        chamber_rad_W=(2.0, 6.0),
        cathode_fil_W=(6.0, 12.0),
        electronics_W=(4.0, 8.0),
        T_tank_C=(80, 100),
        T_line_C=(105, 120),  # > tank, anti-condensa
        T_melt_I2_C=113.7,
        nota="Lineas siempre mas calientes que el tanque. Nunca fundir I2 en tanque proto1.",
    )

def sequence() -> list:
    return [
        "1 VACIO: P<5e-5 mbar, trampas I2 ON, no ventear a turbo sin cold trap",
        "2 LINEAS: heaters 110 C, verificar no puentes termicos al tanque",
        "3 TANQUE: rampa 2 K/min hasta 90 C, Pvap~3.6 kPa",
        "4 CATOD0: filamento W 7-10 W, emision >1.2*Ib antes de extraer",
        "5 RF: 10 W fwd, matching C, buscar Gamma<0.3, luego 18-25 W",
        "6 IGNICION: si no hay plasma en 3 s, pulse 30 W 200 ms y volver",
        "7 GRIDS: V_acc -150 V, luego V_b 400->1200 V en 10 s",
        "8 PUNTO: Ib 16 mA, Gamma<0.15, T_tank lock 90 C",
        "9 APAGADO: HV off, RF off, tanque 40 C, lineas 110 C hasta Pvap baja, entonces lineas off",
        "10 VENTING: N2 seco, nunca aire humedo sobre I2 residual",
    ]

def bom() -> list:
    return [
        dict(id="C1", item="Tubo Al2O3 32 mm ID x 36 mm, pared 1.5 mm", qty=2, eur=(80, 250), mat="Al2O3", i2="OK"),
        dict(id="C2", item="Bobina Cu esmaltado AWG14 5 espiras / recubrimiento teflon", qty=2, eur=(20, 60), mat="Cu+PTFE", i2="Cu NO expuesto"),
        dict(id="C3", item="Rejillas grafito pirolitico SG/AG Ø28 mm", qty=2, eur=(1200, 4000), mat="C", i2="OK"),
        dict(id="C4", item="Aisladores BN o Al2O3 de grid", qty=8, eur=(40, 120), mat="BN/Al2O3", i2="OK"),
        dict(id="C5", item="Anillo matching Cu 8 mm pitch + ALD Si3N4 150 nm", qty=2, eur=(200, 800), mat="Cu+Si3N4", i2="OK si ALD intacto"),
        dict(id="F1", item="Tanque PTFE / Al2O3 poroso 50-80 g I2", qty=1, eur=(80, 300), mat="PTFE/Al2O3", i2="OK"),
        dict(id="F2", item="Capilar PTFE 180-220 um ID x 60 mm (throttle)", qty=4, eur=(20, 80), mat="PTFE", i2="OK"),
        dict(id="F3", item="Valvula NC PTFE/FFKM 1/8", qty=1, eur=(150, 500), mat="PTFE", i2="OK"),
        dict(id="F4", item="Heaters kapton + NTC tanque y lineas", qty=4, eur=(40, 120), mat="polyimide", i2="fuera de vapor"),
        dict(id="F5", item="I2 resublimado 100 g", qty=1, eur=(30, 80), mat="I2", i2="propelente"),
        dict(id="E1", item="RF 13.56 MHz 100 W lab + tuner pi", qty=1, eur=(800, 2500), mat="elec", i2="-"),
        dict(id="E2", item="Fuente HV 0-1500 V / 50 mA flotante", qty=1, eur=(600, 1800), mat="elec", i2="-"),
        dict(id="E3", item="Fuente ACC 0-400 V", qty=1, eur=(200, 600), mat="elec", i2="-"),
        dict(id="E4", item="Fuente filamento 0-8 V / 5 A", qty=1, eur=(80, 250), mat="elec", i2="-"),
        dict(id="N1", item="Filamento W 0.125 mm (proto1) / holder grafito", qty=10, eur=(20, 80), mat="W", i2="fuera del vapor I2"),
        dict(id="D1", item="Sonda Langmuir W + feedthrough Al2O3", qty=1, eur=(150, 400), mat="W/Al2O3", i2="limitado"),
        dict(id="D2", item="RPA 4 rejas grafito", qty=1, eur=(400, 1200), mat="C", i2="OK"),
        dict(id="D3", item="Directional coupler + medidor Gamma 13.56", qty=1, eur=(200, 700), mat="elec", i2="-"),
        dict(id="V1", item="Cold trap I2 / liner Al2O3 o PTFE camara", qty=1, eur=(300, 1500), mat="trap", i2="instalacion"),
    ]

def checks(feed, grid, pv) -> list:
    out = []
    def add(ok, msg):
        out.append(dict(ok=bool(ok), msg=msg))
    add(80 <= feed["T_C"] <= 100, "T_tank 80-100 C (NPT30)")
    add(2.0 <= feed["P_kPa"] <= 6.5, "Pvap 2-6 kPa")
    add(feed.get("cap_d_um", 0) >= 150, f"capilar {feed.get('cap_d_um',0):.0f} um (no joya 50 um)")
    add(150 <= grid["n_holes"] <= 400, f"N agujeros={grid['n_holes']}")
    add(0.35 <= grid["tau"] <= 0.60, f"tau={grid['tau']:.2f}")
    add(0.08 <= pv["np_ratio"] <= 0.55, f"perveance rel {pv['np_ratio']:.2f}")
    return out


if __name__ == "__main__":
    mdot = 34.66e-9  # kg/s card
    feed = size_orifice(mdot, 90.0)
    # table T
    Ts = list(range(70, 111, 5))
    vap = [{"T_C": t, "P_kPa": p_vap_I2(t) / 1e3, "mdot_ugs_180um": sonic_mdot(p_vap_I2(t), t + 273.15, 180e-6) * 1e9} for t in Ts]
    grid = grid_layout()
    pv = perveance(0.016, 1200.0, n_holes=grid["n_holes"], d_sg=0.0011)
    th = thermal_budget()
    ck = checks(feed, grid, pv)
    card = dict(
        meta=dict(id="mei-rit-proto1-realizable", fecha="2026-09-22", clase="E2"),
        feed=feed,
        vapor_curve=vap,
        grid=grid,
        perveance=pv,
        thermal=th,
        sequence=sequence(),
        bom=bom(),
        checks=ck,
        pass_n=sum(1 for x in ck if x["ok"]),
        fail_n=sum(1 for x in ck if not x["ok"]),
        punto_lab=dict(
            P_rf_fwd_w=22,
            I_b_mA=16,
            V_b_v=1200,
            T_tank_C=90,
            eta_e_est=0.31,
            nota="RF lean: no gastar 40 W. Filamento W, no RF-cathode en proto1.",
        ),
        no_hacer=[
            "Tanque Al o Cu desnudo",
            "Lineas mas frias que tanque",
            "Mo grids sin evidencia de lifetime I2",
            "Dual 2.45 GHz",
            "VQE como hito de banco",
            "Masa sistema 220 g",
        ],
    )
    p = OUT / "llp/proyectos/MEI-RIT_proto1_realizable.json"
    p.write_text(json.dumps(card, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(1, 2, figsize=(8.8, 3.2), dpi=140)
    ax[0].plot([v["T_C"] for v in vap], [v["P_kPa"] for v in vap], color="#1f4e79", lw=2)
    ax[0].axhspan(2, 6, color="#1f4e79", alpha=0.08)
    ax[0].axvline(90, color="#8b1e3f", ls="--", lw=1)
    ax[0].set_xlabel("T tanque (C)")
    ax[0].set_ylabel("P_vap I2 (kPa)")
    ax[0].set_title("Sublimacion (Antoine)")
    ax[0].grid(True, alpha=0.3)
    ax[1].plot([v["T_C"] for v in vap], [v["mdot_ugs_180um"] for v in vap], color="#2e7d32", lw=2)
    ax[1].axhline(34.7, color="#8b1e3f", ls="--", lw=1, label="mdot card")
    ax[1].set_xlabel("T tanque (C)")
    ax[1].set_ylabel("mdot orificio 180 um (ug/s)")
    ax[1].set_title("Caudal choked Cd=0.65")
    ax[1].grid(True, alpha=0.3)
    fig.tight_layout()
    png = OUT / "MEI-RIT_proto1_feed.png"
    fig.savefig(png, bbox_inches="tight")
    plt.close()
    print(json.dumps({
        "pass": card["pass_n"], "fail": card["fail_n"],
        "d_sonic_um": round(feed["d_sonic_um"], 1),
        "cap_d_um": round(feed["cap_d_um"], 1),
        "P_kPa_90C": round(feed["P_kPa"], 2),
        "n_holes": grid["n_holes"],
        "tau": round(grid["tau"], 3),
        "np_ratio": round(pv["np_ratio"], 3),
        "bom_n": len(card["bom"]),
        "json": str(p),
        "plot": str(png),
        "fails": [x["msg"] for x in ck if not x["ok"]],
    }, indent=2))
