"""Herramientas físicas. Cada número lleva el supuesto. No hay <σv> inventado."""
import math
import re

E_C = 1.602176634e-19
F_FAR = 96485.3321
M_I = 0.12690447
U_KG = 1.66053906660e-27
G0 = 9.80665
KWH_KG_NH3 = 50.0 * (3.0 / 17.0) + 0.7
CO2_KG_POR_KG = 1.6
D_NV = 2.87e9
GAMMA_NV = 28.024951e9
UMBRAL_DT = 3.0e21
SIGMA_CUERO = 0.33
EUR_KW = 1500.0


def _f(m):
    return float(m.group(1).replace(",", "."))


def tomar(texto: str, patron: str):
    m = re.search(patron, texto, re.I)
    return _f(m) if m else None


def _potencia_mw(texto: str):
    v = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*mw")
    if v is not None:
        return v
    v = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*kw")
    return None if v is None else v / 1000.0


def produccion_amoniaco(texto: str) -> str:
    mw = _potencia_mw(texto)
    if mw is None:
        return "falta la potencia en MW"
    kg_h = mw * 1000.0 / KWH_KG_NH3
    return (
        f"potencia {mw:g} MW\n"
        f"kg_NH3/h {kg_h:.1f}\n"
        f"CO2_evitado_kg/h {kg_h * CO2_KG_POR_KG:.1f} (1,6 kg CO2/kg NH3 de gas, supuesto)\n"
        f"kWh/kg {KWH_KG_NH3:.2f} (50 kWh/kg H2 · 3/17 kg H2 por kg NH3 · 0,7 kWh/kg de síntesis)"
    )


def energia_hb(texto: str) -> str:
    precio = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:€|eur)\s*/\s*mwh")
    linea = f"kWh/kg {KWH_KG_NH3:.2f}"
    if precio is None:
        return linea + "\nsin precio €/MWh: no hay coste"
    return linea + f"\n€/kg {KWH_KG_NH3 * precio / 1000:.3f} (electricidad, sin OPEX de planta)"


def mw_para_objetivo(texto: str) -> str:
    t = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*t\s*/\s*d")
    if t is None:
        return "falta el objetivo en t/día"
    kg_h = t * 1000.0 / 24.0
    mw = kg_h * KWH_KG_NH3 / 1000.0
    inv = mw * 1000.0 * EUR_KW
    return (
        f"objetivo {t:g} t/día\n"
        f"MW {mw:.2f}\n"
        f"inversion_eur {inv:.0f} (supuesto {EUR_KW:.0f} €/kW de electrolizador, no es una cotización)"
    )


def balance_fusion(texto: str) -> str:
    j = 18.3e6 * E_C
    lineas = [
        "reaccion D + He3 → α (3,6 MeV) + p (14,7 MeV)",
        "MeV 18.3",
        f"J/reaccion {j:.6e}",
    ]
    n = tomar(texto, r"(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)\s*(?:m-3|m\^-3|/m3)")
    sv = tomar(texto, r"(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)\s*(?:m3/s|sv)")
    if n is None or sv is None:
        lineas.append("potencia no calculada: faltan densidad (m-3) y <σv> (m3/s). No se inventa <σv>.")
        return "\n".join(lineas)
    tasa = n * n * sv
    lineas.append(f"reacciones/m3/s {tasa:.6e} (n·n·<σv>, n de cada especie)")
    lineas.append(f"W/m3 {tasa * j:.6e}")
    return "\n".join(lineas)


def producto_triple(texto: str) -> str:
    n = tomar(texto, r"(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)\s*(?:m-3|m\^-3|/m3)")
    t = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*kev")
    tau = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:s\b|tau)")
    if n is None or t is None or tau is None:
        return "faltan n (m-3), T (keV) y tau (s)"
    ntt = n * t * tau
    return (
        f"nTτ {ntt:.6e} keV·s/m3\n"
        f"vs_DT_3e21 {ntt / UMBRAL_DT:.4g} (referencia DT, no es el umbral D-He3)\n"
        "ignicion no declarada"
    )


def densidad_objetivo(texto: str) -> str:
    t = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*kev")
    tau = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:s\b|tau)")
    if t is None or tau is None or t == 0 or tau == 0:
        return "faltan T (keV) y tau (s)"
    n_dt = UMBRAL_DT / (t * tau)
    return (
        f"n_min_si_fuera_DT {n_dt:.6e} m-3 (umbral 3e21 keV·s/m3)\n"
        "n mínima D-He3 no se cierra: este nodo no tiene un umbral medido para esa reacción"
    )


def _corriente_a(texto: str):
    ma = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*ma")
    if ma is not None:
        return ma / 1000.0
    return tomar(texto, r"(\d+(?:[.,]\d+)?)\s*a\b")


def corrosion_yodo(texto: str) -> str:
    i = _corriente_a(texto)
    if i is None:
        return "falta la corriente (A o mA)"
    ug_s = i * (M_I / F_FAR) * 1e9
    return f"I {i:g} A\nconsumo_I+ {ug_s:.2f} µg/s (Faraday, n=1, M=126,904 g/mol)"


def _ve_iod(volt: float) -> float:
    m = M_I / 1e-3 * U_KG
    return math.sqrt(2.0 * E_C * volt / m)


def empuje_yodo(texto: str) -> str:
    kv = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*kv")
    volt = kv * 1000.0 if kv is not None else tomar(texto, r"(\d+(?:[.,]\d+)?)\s*v\b")
    if volt is None:
        return "falta el voltaje"
    ve = _ve_iod(volt)
    isp = ve / G0
    i = _corriente_a(texto)
    base = f"ve {ve:.0f} m/s\nIsp {isp:.0f} s (I+, ideal, sin divergencia ni dobles cargas)"
    if i is None:
        return base + "\nfalta corriente para el empuje"
    mdot = i * M_I / F_FAR
    un = mdot * ve * 1e6
    return base + f"\nempuje {un:.2f} µN\nmdot {mdot * 1e6:.4f} mg/s"


def empuje_objetivo(texto: str) -> str:
    un = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:µn|un|μn)")
    kv = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*kv")
    if un is None or kv is None:
        return "faltan empuje (µN) y voltaje (kV)"
    ve = _ve_iod(kv * 1000.0)
    mdot = (un * 1e-6) / ve
    i = mdot * F_FAR / M_I
    dia = mdot * 86400.0
    dias = 1.0 / dia if dia else float("inf")
    return (
        f"mdot {mdot * 1e6:.4f} mg/s\n"
        f"I {i * 1000:.2f} mA\n"
        f"consumo_kg/dia {dia:.6e}\n"
        f"autonomia_1kg_dias {dias:.1f} (ideal, sin pérdidas)"
    )


def _campo_t(texto: str):
    ut = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:µt|ut|μt)")
    if ut is not None:
        return ut * 1e-6
    mt = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*mt")
    if mt is not None:
        return mt * 1e-3
    return tomar(texto, r"(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)\s*t\b")


def zeeman_odmr(texto: str) -> str:
    b = _campo_t(texto)
    if b is None:
        return "falta B (µT, mT o T)"
    fp = D_NV + GAMMA_NV * b
    fm = D_NV - GAMMA_NV * b
    return (
        f"D 2.87 GHz\n"
        f"f+ {fp / 1e9:.6f} GHz\n"
        f"f- {fm / 1e9:.6f} GHz\n"
        f"split {2 * GAMMA_NV * b / 1e6:.3f} MHz (γ = 28,025 GHz/T)"
    )


def _snr(texto: str) -> str:
    c = tomar(texto, r"(?:contraste\s*)(\d+(?:[.,]\d+)?)")
    if c is None:
        c = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*%")
        if c is not None and c > 1:
            c = c / 100.0
    n = tomar(texto, r"(\d+(?:[.,]\d+)?(?:e[+-]?\d+)?)\s*fot")
    lw = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*mhz")
    if c is None or n is None or lw is None or c <= 0 or n <= 0:
        return "faltan contraste, fotones y anchura de línea (MHz)"
    bmin = (lw * 1e6) / (GAMMA_NV * c * math.sqrt(n))
    shots = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*(?:disparos|shots)")
    extra = ""
    if shots and shots > 0:
        extra = f"\nB_min_N {bmin / math.sqrt(shots) * 1e6:.4g} µT (÷√N disparos)"
    return (
        f"SNR {c * math.sqrt(n):.3g} (C·√N, ruido de disparo)\n"
        f"B_min {bmin * 1e6:.4g} µT (línea / (γ·C·√N), un disparo)"
        + extra
    )


def contraste_odmr(texto: str) -> str:
    return _snr(texto)


def sensibilidad_magnetica(texto: str) -> str:
    return _snr(texto)


def densidad_corriente(texto: str) -> str:
    i = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*ma")
    a = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*cm")
    if i is None or a is None or a == 0:
        return "faltan corriente (mA) y área (cm2)"
    j = i / a
    e = (j * 10.0) / SIGMA_CUERO
    return (
        f"J {j:.3f} mA/cm2\n"
        f"E {e:.2f} V/m (σ = {SIGMA_CUERO} S/m, supuesto de cuero cabelludo, no del cerebro)"
    )


def protocolo_objetivo(texto: str) -> str:
    j = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*ma\s*/\s*cm")
    a = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*cm")
    minutos = tomar(texto, r"(\d+(?:[.,]\d+)?)\s*min")
    if j is None or a is None:
        return "faltan J (mA/cm2) y área (cm2)"
    i = j * a
    linea = f"I {i:.2f} mA\nelectrodo {a:g} cm2 para J {j:g} mA/cm2"
    if minutos is None:
        return linea + "\nsin minutos: no hay dosis en culombios"
    return linea + f"\ndosis {(i / 1000.0) * minutos * 60.0:.3f} C"


def balance_ecosistema(texto: str) -> str:
    mw = _potencia_mw(texto)
    if mw is None:
        return "falta la potencia en MW"
    kg_h = mw * 1000.0 / KWH_KG_NH3
    h2 = kg_h * (3.0 / 17.0)
    agua = h2 * 9.0
    o2 = h2 * 8.0
    return (
        f"MW {mw:g}\n"
        f"NH3_kg/h {kg_h:.1f}\n"
        f"agua_kg/h {agua:.1f} (9 kg agua por kg H2)\n"
        f"O2_kg/h {o2:.1f} (8 kg O2 por kg H2)\n"
        "He3 no calculado: falta la fracción D-D y <σv>. No se afirma autoprovisión."
    )


CATALOGO = [
    ("zero_a", "mw_para_objetivo", ("t/dia", "t/día", "tonelada", "objetivo"), mw_para_objetivo),
    ("zero_a", "energia_hb", ("kwh/kg", "coste", "€/mwh", "precio"), energia_hb),
    ("zero_a", "produccion_amoniaco", ("amoniaco", "nh3", "mw", "haber"), produccion_amoniaco),
    ("d3he_tokamak", "densidad_objetivo", ("densidad objetivo", "n mínima", "n minima", "ignicion"), densidad_objetivo),
    ("d3he_tokamak", "producto_triple", ("triple", "ntτ", "ntt", "lawson", "tau"), producto_triple),
    ("d3he_tokamak", "balance_fusion", ("fusion", "fusión", "hev", "kev", "he3", "helio"), balance_fusion),
    ("mei_rit", "empuje_objetivo", ("objetivo", "autonomia", "autonomía"), empuje_objetivo),
    ("mei_rit", "corrosion_yodo", ("corrosion", "corrosión", "faraday"), corrosion_yodo),
    ("mei_rit", "empuje_yodo", ("empuje", "isp", "kv", "yodo"), empuje_yodo),
    ("q_matrix", "sensibilidad_magnetica", ("sensibilidad", "b_min", "bmin"), sensibilidad_magnetica),
    ("q_matrix", "contraste_odmr", ("contraste", "snr", "fotones"), contraste_odmr),
    ("q_matrix", "zeeman_odmr", ("zeeman", "odmr", "split", "nv"), zeeman_odmr),
    ("neuroglyq", "protocolo_objetivo", ("protocolo", "objetivo", "dosis"), protocolo_objetivo),
    ("neuroglyq", "densidad_corriente", ("densidad", "ma/cm", "electrodo", "tdcs"), densidad_corriente),
    ("ecosistema", "balance_ecosistema", ("ecosistema", "sinergia", "balance"), balance_ecosistema),
]
