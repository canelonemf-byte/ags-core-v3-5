"""Tests del Maestro Cuántico compartido (simulación clásica statevector)."""
from __future__ import annotations

import math

import pytest

from shared.maestro_cuantico import (
    OptimizadorModular,
    crear_ansatz,
    crear_hamiltoniano_demo,
    energia_exacta,
    optimizar_vqe,
    ejecutar_paralelo,
    hacer_funcion_costo,
)
import agents  # noqa: F401 — registra maestro_cuantico
from registry import get_agent, agents_by_domain

pytestmark = pytest.mark.unit


def test_energia_exacta_demo():
    H = crear_hamiltoniano_demo()
    esperado = -math.sqrt(1.09)
    e0 = energia_exacta(H)
    assert e0 == pytest.approx(esperado, abs=1e-5)


def test_vqe_encuentra_ground_state():
    _, E, _, H = optimizar_vqe(seed=42, max_iter=1000)
    assert abs(E - energia_exacta(H)) < 0.05


def test_optimizador_modular_esfera():
    """Optimizador reutilizable fuera de VQE."""
    def esfera(p):
        return p["x"] ** 2 + p["y"] ** 2

    opt = OptimizadorModular(
        {"x": (-3.0, 3.0), "y": (-3.0, 3.0)},
        seed=1,
        patience=50,
        t0=0.5,
        cooling=0.95,
    )
    pos, costo = opt.optimizar(esfera, max_iter=500)
    assert costo < 0.05
    assert abs(pos["x"]) < 0.4
    assert abs(pos["y"]) < 0.4


def test_vqe_hamiltoniano_arbitrario_1q():
    H = [("Z", 1.0)]
    _, E, _, H_obj = optimizar_vqe(
        seed=0, max_iter=400, n_qubits=1, hamiltoniano=H, reps=1, patience=80
    )
    assert H_obj.num_qubits == 1
    assert abs(E - energia_exacta(H_obj)) < 0.08


def test_ansatz_n_qubits():
    qc, theta = crear_ansatz(3, reps=1)
    assert qc.num_qubits == 3
    assert len(theta) == 3 * 2


def test_ejecutar_paralelo_default_no_mutable():
    """Default de semillas no mutable; bajo pytest corre en serie (sin pool)."""
    out1 = ejecutar_paralelo(semillas=[42, 123], max_iter=120, usar_procesos=False)
    out2 = ejecutar_paralelo(semillas=[42, 123], max_iter=120, usar_procesos=False)
    assert len(out1["resultados"]) == 2
    assert len(out2["resultados"]) == 2
    assert out1["es_simulacion_clasica"] is True
    assert out1["modo_pool"] == "serie"
    assert out1["mejor"]["energia"] <= max(r["energia"] for r in out1["resultados"])


def test_agente_registrado():
    names = {a.name for a in agents_by_domain("compute")}
    assert "maestro_cuantico" in names
    a = get_agent("maestro_cuantico")
    assert "simulación" in a.description.lower() or "statevector" in a.description.lower()


@pytest.mark.asyncio
async def test_agente_vqe_ok():
    out = await get_agent("maestro_cuantico").run(
        "vqe demo", context={"seed": 42, "max_iter": 500, "modo": "vqe"}
    )
    assert out["status"] == "ok"
    assert out["es_simulacion_clasica"] is True
    assert out["data"]["error_abs"] < 0.05
    assert "statevector" in out["output"].lower() or "clásica" in out["output"].lower()
