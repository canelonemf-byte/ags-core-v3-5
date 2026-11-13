"""Tests de scripts/maestro_supervision.py (simulación clásica; no escribe en knowledge/).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. MIT.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("maestro_supervision", ROOT / "scripts/maestro_supervision.py")
ms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ms)


def _sin_null(o):
    if o is None:
        return False
    if isinstance(o, dict):
        return all(_sin_null(v) for v in o.values())
    if isinstance(o, list):
        return all(_sin_null(v) for v in o)
    return True


def test_corrida_reproducible_y_llp(tmp_path):
    r1 = ms.ejecutar_agente(42, 300)
    r2 = ms.ejecutar_agente(42, 300)
    llp = ms.construir_llp("oraculo-mesoscopico", "demo", 42, 300, r1, r2, "2026-01-01T00:00:00+01:00")
    assert set(llp) == {"meta", "objetivo", "datos_clave", "tareas", "riesgos", "decisiones", "proximo_paso"}
    assert _sin_null(llp)
    dk = llp["datos_clave"]
    assert dk["reproducible_semilla"] is True
    assert llp["meta"]["evidencia"] == "E2_simulacion_propia"
    assert llp["meta"]["verificacion_software"] == "reproducible_misma_semilla"
    assert llp["meta"]["es_hardware_cuantico"] is False
    assert dk["error_abs"] == pytest.approx(abs(dk["energia_obtenida"] - dk["energia_referencia_exacta"]))
    destino = tmp_path / "out.json"
    ms.escribir_en_sitio(destino, llp)
    ms.escribir_en_sitio(destino, llp)  # reescritura en sitio, sin copias
    assert json.loads(destino.read_text(encoding="utf-8")) == llp
    assert [p.name for p in tmp_path.iterdir()] == ["out.json"]


def test_no_reproducible_marca_verificacion():
    r1 = ms.ejecutar_agente(42, 50)
    r2 = dict(r1, energia=r1["energia"] + 1e-3)
    llp = ms.construir_llp("oraculo-mesoscopico", "demo", 42, 50, r1, r2, "x")
    assert llp["meta"]["evidencia"] == "E2_simulacion_propia"
