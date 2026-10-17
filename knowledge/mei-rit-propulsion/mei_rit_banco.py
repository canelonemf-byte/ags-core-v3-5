#!/usr/bin/env python3
"""MEI-RIT proto1 — matching 13.56 MHz + criterios banco Ar / I2.
No enciende hardware. Genera red LC y umbrales de paso.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path("/home/workdir/artifacts")
F = 13.56e6
W = 2.0 * math.pi * F
L_H = 848.15e-9
Z0 = 50.0
WL = W * L_H


def lmatch(Rs: float) -> dict:
    if Rs >= Z0:
        raise ValueError("Rs>=Z0")
    Q = math.sqrt(Z0 / Rs - 1.0)
    Xp = Z0 / Q
    Xs = Q * Rs
    Cp = 1.0 / (W * Xp)
    Cs = 1.0 / (W * (WL - Xs))
    return dict(Rs=Rs, Q=Q, Cp_pF=Cp * 1e12, Cs_pF=Cs * 1e12, wL_ohm=WL, Xs_ohm=Xs)


def catalog_caps(Cs_pF: float, Cp_pF: float) -> dict:
    # piezas de laboratorio: doorknob + trimmer
    cs_fix = 150.0 if Cs_pF > 160 else 100.0
    cs_trim = 10.0 if Cs_pF - cs_fix <= 60 else 60.0
    # pick nearest
    cs_fix = min([100, 150, 180, 200], key=lambda x: abs(x + 25 - Cs_pF))
    return dict(
        Cs_fijo_pF=int(cs_fix),
        Cs_trimmer="10-60 pF vacuum/air cap 5 kV",
        Cp_fijo_pF=int(round(Cp_pF / 100) * 100),
        Cp_trimmer="50-500 pF o 2x500 en paralelo 3 kV",
        V_rf_est_kV=round((2 * 25 * WL) ** 0.5 / 1000, 2),  # orden, 25 W
        nota="Ceramica NP0 / vacio. No C electrolitico. Distancia >= 8 mm a tierra.",
    )


def gamma_vs_P(P=None):
    """Curva E1 de Gamma vs P_fwd en Ar tras sintonía (no medida)."""
    if P is None:
        P = np.linspace(2, 40, 20)
    # ignicion ~8-12 W en 0.3 Pa Ar; Gamma cae cuando hay plasma
    g = []
    for p in P:
        if p < 8:
            g.append(0.55 + 0.15 * np.exp(-p / 6))
        else:
            g.append(0.12 + 0.35 * np.exp(-(p - 8) / 7))
    return np.asarray(P), np.asarray(g)


def criterios() -> dict:
    return dict(
        argon=dict(
            P_base_mbar=(2e-5, 8e-5),
            P_work_Pa=(0.15, 0.6),
            gas="Ar 5.0",
            P_rf_scan_W=(5, 30),
            Gamma_ok=0.15,
            Gamma_ignicion_max=0.35,
            I_coil_max_A=12,
            T_coil_max_C=80,
            pass_si=["plasma visible o n_e Langmuir > 5e15 m-3", "Gamma<0.15 a 18-25 W", "sin arcos en caps"],
        ),
        i2_gate=dict(
            no_pasar_si=["Gamma Ar > 0.25 a 22 W", "C trimmer al tope", "puntos calientes en esmalte"],
            P_base_mbar=5e-5,
            cold_trap="ON, T<-70 C o LN2 + liner",
            T_tank_C=90,
            T_line_C=110,
            P_rf_start_W=10,
            Ib_target_mA=16,
        ),
    )


def rfq() -> list:
    return [
        dict(id="RFQ-C1", pieza="Tubo Al2O3 99.7%",
             spec="ID 32.0±0.20 mm; OD 35.0±0.20 mm; L 36.0±0.50 mm; extremos rectificados; sin vidriado interior; 2 ud + 1 spare",
             qty=3, uso="camara descarga"),
        dict(id="RFQ-C2", pieza="Capilar PTFE medical/AWG",
             spec="ID 0.20±0.02 mm (200 um); OD 1.6±0.1 mm; L stock 1.0 m (cortar 60 mm); PTFE virgen; 2 m",
             qty=2, uso="throttle I2"),
        dict(id="RFQ-C3", pieza="Rejillas grafito isostatico ISO-63 o pyrolytic",
             spec="disco 28.0±0.1 mm; SG e=0.30±0.03 mm agujero 1.10±0.05; AG e=0.50±0.05 agujero 0.70±0.05; pitch hex 1.50±0.05; 316 agujeros; gap spacer BN 0.60±0.03",
             qty=2, uso="optica ionica"),
        dict(id="RFQ-C4", pieza="Alambre Cu + PTFE",
             spec="Cu AWG14 (d=1.63 mm) 2 m + funda PTFE 2 mm ID; 5 espiras ID 35.5 mm paso 4.5 mm",
             qty=1, uso="bobina"),
        dict(id="RFQ-E1", pieza="Caps matching",
             spec="C serie: 150 pF 5 kV NP0/vacio + trimmer 10-60 pF 5 kV; C paralelo: 800 pF 3 kV + trimmer 50-500 pF",
             qty=1, uso="red L 13.56 MHz"),
        dict(id="RFQ-E2", pieza="RF 13.56 MHz",
             spec="generador 100 W 50 ohm + coupler bidireccional + cables RG-393 N",
             qty=1, uso="ICP"),
        dict(id="RFQ-F1", pieza="Tanque PTFE",
             spec="cuerpo PTFE o Al2O3 poroso; volumen 30-40 ml; heater Kapton 10 W; NTC 10k; no Al/Cu",
             qty=1, uso="sublimador"),
        dict(id="RFQ-N1", pieza="Filamento W",
             spec="alambre W 0.125 mm, 200 mm; holder grafito; fuera de linea I2",
             qty=1, uso="neutralizador proto1"),
        dict(id="RFQ-V1", pieza="Cold trap I2",
             spec="trampa -75 C o dedo LN2 + liner PTFE/Al2O3 en campana; valvula bypass turbo",
             qty=1, uso="banco halogen"),
    ]


if __name__ == "__main__":
    pts = {f"Rs_{r}ohm": lmatch(r) for r in (2.0, 4.0, 8.0)}
    nom = lmatch(4.0)
    cat = catalog_caps(nom["Cs_pF"], nom["Cp_pF"])
    P, g = gamma_vs_P()
    card = dict(
        meta=dict(id="mei-rit-banco", f_Hz=F, fecha="2026-09-22", clase="E2"),
        matching_nominal=nom,
        matching_scan=pts,
        catalogo=cat,
        criterios=criterios(),
        rfq=rfq(),
        nota="Gamma vs P es plantilla E1 para el log de banco, no una medida.",
    )
    jp = OUT / "llp/proyectos/MEI-RIT_proto1_banco.json"
    jp.write_text(json.dumps(card, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=140)
    ax.plot(P, g, color="#1f4e79", lw=2)
    ax.axhline(0.15, color="#2e7d32", ls="--", label="pass Ar")
    ax.axhline(0.25, color="#8b1e3f", ls="--", label="gate I2")
    ax.axvline(22, color="#555", ls=":", lw=1)
    ax.set_xlabel("P_RF fwd (W)")
    ax.set_ylabel("|Gamma|")
    ax.set_title("Plantilla Gamma(P) Ar — sustituir por medida")
    ax.legend()
    ax.grid(True, alpha=0.3)
    png = OUT / "MEI-RIT_proto1_gamma_plantilla.png"
    fig.tight_layout()
    fig.savefig(png, bbox_inches="tight")
    plt.close()
    print(json.dumps({
        "Cs_pF": round(nom["Cs_pF"], 1),
        "Cp_pF": round(nom["Cp_pF"], 1),
        "catalogo": cat,
        "rfq_n": len(rfq()),
        "json": str(jp),
        "plot": str(png),
    }, indent=2))
