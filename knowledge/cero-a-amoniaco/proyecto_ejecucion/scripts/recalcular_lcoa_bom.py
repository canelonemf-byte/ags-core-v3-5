#!/usr/bin/env python3
"""Recalcula LCOA indicativo del escenario PPA usando unitarios de bom.json.

Caso base 2026-11-05: organigrama B (vigilancia remota compartida),
sin alquiler de parcela propia, coste de compartir instalacion = PENDIENTE (0 hasta oferta).

No reoptimiza diseño ni series horarias.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de IA.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PE = Path(__file__).resolve().parents[1]
WACC = 0.07
PROD = 422.6
PEM_KW = 538.796
BUFFER_H = 14.134
H2_STOICH = 3 / 17
CONV = 0.98
R_H2 = 50.0 * H2_STOICH / CONV
BUF_KG = BUFFER_H * R_H2
TQ = 15.9

# Organigrama B (cerrado p6)
PERSONAL_FTE = 2.0
COSTE_FTE = 45000.0
ALQUILER_PARCELA_PROPIA_EUR_A = 0.0
# Canon / utilities / seguridad compartida con partner: sin oferta → 0 y marcado PENDIENTE
COMPARTIR_INSTALACION_EUR_A = 0.0
COMPARTIR_INSTALACION_ESTADO = "PENDIENTE_DE_VERIFICACION"


def crf(w: float, n: int) -> float:
    return w * (1 + w) ** n / ((1 + w) ** n - 1)


def main() -> None:
    bom = json.loads((PE / "bom.json").read_text(encoding="utf-8"))
    items = {i["id"]: i for i in bom["datos_clave"]["items"]}
    pem_u = items["eq_pem_01"]["precio_unitario_eur"]
    buf_u = items["eq_buf_01"]["precio_unitario_eur"]
    psa = items["eq_psa_01"]["precio_total_eur"]
    hb = items["eq_hb_01"]["precio_total_eur"]
    tq_u = items["eq_nh3_01"]["precio_unitario_eur"]
    elec = items["eq_elec_01"]["precio_total_eur"]

    a20 = crf(WACC, 20)
    capem = PEM_KW * pem_u
    capbuf = BUF_KG * buf_u
    cappsahb = psa + hb
    captq = TQ * tq_u
    capcon = elec
    cap_perm = 0.15 * (capem + capbuf + cappsahb)
    horas = 0.892 * 8760
    personal = PERSONAL_FTE * COSTE_FTE
    c = {
        "pem": capem * (a20 + 0.03) + capem * 0.35 * horas / 50000,
        "buffer_h2": capbuf * (a20 + 0.02),
        "psa_hb": cappsahb * (a20 + 0.03),
        "tanque_nh3": captq * (a20 + 0.02),
        "conexion_red": capcon * a20,
        "permisos_ingenieria": cap_perm * a20,
        "personal": personal,
        "alquiler_terreno": ALQUILER_PARCELA_PROPIA_EUR_A,
        "compartir_instalacion": COMPARTIR_INSTALACION_EUR_A,
        "ppa": 1001 * PROD,
        "venta_excedentes": -246 * PROD,
        "red_peajes_cargos": 212 * PROD,
        "agua": 3 * PROD,
    }
    total = sum(c.values())
    lcoa = total / PROD
    out = {
        "meta": {
            "proyecto": "cero_a",
            "documento": "lcoa_bom_recalc",
            "fecha": "2026-11-05",
            "zona_horaria": "Europe/Madrid",
            "autoria": "Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial",
            "nivel_evidencia": "e2",
            "escenario_opex": "organigrama_b_sin_parcela_propia",
        },
        "objetivo": "recalculo_lcoa_con_unitarios_bom_opcion_b",
        "datos_clave": {
            "lcoa_eur_t": round(lcoa),
            "desglose_eur_t": {k: round(v / PROD) for k, v in c.items()},
            "capex_eur": {
                "pem": round(capem),
                "buffer": round(capbuf),
                "psa_hb": round(cappsahb),
                "tanque": round(captq),
                "conexion": round(capcon),
                "permisos": round(cap_perm),
            },
            "opex_supuestos": {
                "personal_fte": PERSONAL_FTE,
                "coste_fte_eur_a": COSTE_FTE,
                "personal_eur_a": round(personal),
                "alquiler_parcela_propia_eur_a": ALQUILER_PARCELA_PROPIA_EUR_A,
                "compartir_instalacion_eur_a": COMPARTIR_INSTALACION_EUR_A,
                "compartir_instalacion_estado": COMPARTIR_INSTALACION_ESTADO,
            },
            "rentable_vs_gris": False,
            "gris_eur_t": [383, 562],
            "lcoa_bom_anterior_eur_t": 3145,
            "delta_vs_bom_anterior_eur_t": round(lcoa) - 3145,
        },
        "tareas": [],
        "riesgos": [
            {
                "riesgo": "no sustituye cotizaciones",
                "impacto": "alto",
                "mitigacion": "p2",
            },
            {
                "riesgo": "fee partner compartir instalacion desconocido",
                "impacto": "alto",
                "mitigacion": "marcar PENDIENTE; pedir oferta antes de FID",
            },
        ],
        "decisiones": [
            {
                "decision": "organigrama_b_vigilancia_remota",
                "estado": "hecho",
            },
            {
                "decision": "socio_planta_existente_sin_alquiler_propio",
                "estado": "hecho",
            },
        ],
        "proximo_paso": "cotizar fee de partner y equipos; reoptimizar v4",
    }
    dest = PE / "data" / "lcoa_bom_recalc.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "lcoa_eur_t": out["datos_clave"]["lcoa_eur_t"],
                "desglose_eur_t": out["datos_clave"]["desglose_eur_t"],
                "escrito": str(dest),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
