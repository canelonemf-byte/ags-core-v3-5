#!/usr/bin/env python3
"""
Maestro Cuántico — módulo compartido AGs-Core.

Simulación CLÁSICA de circuitos cuánticos (statevector de Qiskit), no hardware
cuántico real. Incluye:
1. OptimizadorModular: simulated annealing para cualquier función de coste.
2. VQE parametrizable: hamiltoniano y nº de qubits arbitrarios.
3. Ejecución en paralelo (ProcessPoolExecutor).

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España,
con asistencia de inteligencia artificial.
Licencia: MIT.
"""
from __future__ import annotations

import math
import random
import time
import concurrent.futures
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

try:
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector
    from qiskit.quantum_info import Statevector, SparsePauliOp
except ImportError as e:  # pragma: no cover
    raise ImportError(
        f"falta dependencia ({e}). Instala: pip install qiskit numpy"
    ) from e

# Aviso explícito: no es un ordenador cuántico físico.
ES_SIMULACION_CLASICA = True
BACKEND = "statevector"
NOTA_HARDWARE = (
    "Simulación clásica de circuitos cuánticos (Qiskit Statevector). "
    "No usa hardware cuántico real ni garantiza ventaja cuántica."
)


# ==========================================
# 1. MOTOR DE OPTIMIZACIÓN (Simulated Annealing)
# ==========================================
class OptimizadorModular:
    """Simulated annealing genérico sobre un dict de parámetros acotados.

    Sirve para cualquier ``funcion_costo(dict) -> float``, no solo VQE.
    """

    def __init__(
        self,
        limites: Dict[str, Tuple[float, float]],
        step_sizes: Optional[Dict[str, float]] = None,
        seed: Optional[int] = None,
        patience: int = 25,
        t0: float = 0.5,
        cooling: float = 0.97,
        min_temperature: float = 1e-4,
    ):
        self.limites = limites
        self.step_sizes = dict(step_sizes) if step_sizes else {}
        for k in limites:
            self.step_sizes.setdefault(k, 0.05)
        self.rng = random.Random(seed)
        self.patience = patience
        self.t0 = t0
        self.cooling = cooling
        self.min_temperature = min_temperature
        self.posicion_actual = {
            k: self.rng.uniform(v[0], v[1]) for k, v in limites.items()
        }
        self.costo_actual = float("inf")
        self.mejor_posicion = dict(self.posicion_actual)
        self.mejor_costo = float("inf")
        self.temperature = t0
        self.stagnation = 0
        self.iteracion = 0

    def _perturbar(self, k: str) -> float:
        low, high = self.limites[k]
        span = high - low
        if span <= 0:
            return low
        sigma = self.step_sizes[k] * span * math.exp(-self.stagnation / self.patience)
        delta = self.rng.gauss(0, sigma)
        nueva = self.posicion_actual[k] + delta
        periodo = 2 * span
        nueva = (nueva - low) % periodo
        if nueva > span:
            nueva = periodo - nueva
        return nueva + low

    def paso_optimizacion(
        self, funcion_costo: Callable[[Dict[str, float]], float]
    ) -> Tuple[Dict[str, float], float]:
        self.iteracion += 1
        candidato = {k: self._perturbar(k) for k in self.limites}
        costo_candidato = funcion_costo(candidato)
        if costo_candidato < self.mejor_costo:
            self.mejor_costo = costo_candidato
            self.mejor_posicion = dict(candidato)
            self.stagnation = 0
        else:
            self.stagnation += 1
        if costo_candidato < self.costo_actual:
            self.posicion_actual = candidato
            self.costo_actual = costo_candidato
        else:
            delta = costo_candidato - self.costo_actual
            if self.temperature > self.min_temperature:
                if self.rng.random() < math.exp(-delta / self.temperature):
                    self.posicion_actual = candidato
                    self.costo_actual = costo_candidato
        self.temperature = max(self.temperature * self.cooling, self.min_temperature)
        return self.mejor_posicion, self.mejor_costo

    def optimizar(
        self,
        funcion_costo: Callable[[Dict[str, float]], float],
        max_iter: int = 1000,
    ) -> Tuple[Dict[str, float], float]:
        for _ in range(max_iter):
            self.paso_optimizacion(funcion_costo)
            if self.stagnation >= self.patience:
                break
        return self.mejor_posicion, self.mejor_costo


# ==========================================
# 2. LÓGICA CUÁNTICA (VQE — simulación clásica)
# ==========================================
PauliTerm = Tuple[str, float]
HamiltonianoLike = Union[SparsePauliOp, Sequence[PauliTerm]]


def crear_ansatz(n_qubits: int, reps: int = 1):
    """Ansatz Ry + CNOT lineal. n_qubits arbitrario."""
    if n_qubits < 1:
        raise ValueError("n_qubits debe ser >= 1")
    theta = ParameterVector("t", n_qubits * (reps + 1))
    qc = QuantumCircuit(n_qubits)
    idx = 0
    for r in range(reps + 1):
        for q in range(n_qubits):
            qc.ry(theta[idx], q)
            idx += 1
        if r < reps:
            for q in range(n_qubits - 1):
                qc.cx(q, q + 1)
    return qc, theta


def crear_hamiltoniano_demo() -> SparsePauliOp:
    """Hamiltoniano de demostración 2 qubits: 0.5 ZI + 0.5 IZ + 0.3 XX.

    Energía exacta del estado fundamental: -sqrt(1.09).
    """
    return SparsePauliOp.from_list([("ZI", 0.5), ("IZ", 0.5), ("XX", 0.3)])


# Alias retrocompatible con el script original
crear_hamiltoniano = crear_hamiltoniano_demo


def _como_sparse(hamiltoniano: HamiltonianoLike) -> SparsePauliOp:
    if isinstance(hamiltoniano, SparsePauliOp):
        return hamiltoniano
    return SparsePauliOp.from_list(list(hamiltoniano))


def hacer_funcion_costo(ansatz, theta, hamiltoniano: HamiltonianoLike):
    """Devuelve f(params_dict) = <ψ(θ)|H|ψ(θ)> con Statevector (clásico)."""
    H = _como_sparse(hamiltoniano)
    param_names = [p.name for p in theta]

    def costo(params_dict: Dict[str, float]) -> float:
        values = [params_dict[n] for n in param_names]
        bound = ansatz.assign_parameters({p: v for p, v in zip(theta, values)})
        state = Statevector.from_instruction(bound)
        return float(state.expectation_value(H).real)

    return costo


def energia_exacta(hamiltoniano: HamiltonianoLike) -> float:
    """Menor autovalor de H (diagonalización clásica densa)."""
    H = _como_sparse(hamiltoniano)
    return float(np.linalg.eigvalsh(H.to_matrix())[0])


def optimizar_vqe(
    seed: int = 42,
    max_iter: int = 800,
    n_qubits: Optional[int] = None,
    hamiltoniano: Optional[HamiltonianoLike] = None,
    reps: int = 1,
    patience: int = 60,
    t0: float = 0.3,
    cooling: float = 0.98,
) -> Tuple[Dict[str, float], float, OptimizadorModular, SparsePauliOp]:
    """VQE con annealing. Si no se pasa H, usa el demo de 2 qubits."""
    H = _como_sparse(hamiltoniano) if hamiltoniano is not None else crear_hamiltoniano_demo()
    if n_qubits is None:
        n_qubits = H.num_qubits
    if H.num_qubits != n_qubits:
        raise ValueError(
            f"n_qubits={n_qubits} no coincide con hamiltoniano ({H.num_qubits} qubits)"
        )
    ansatz, theta = crear_ansatz(n_qubits, reps)
    costo_fn = hacer_funcion_costo(ansatz, theta, H)
    limites = {p.name: (0.0, 2 * math.pi) for p in theta}
    step_sizes = {p.name: 0.15 for p in theta}
    opt = OptimizadorModular(
        limites,
        step_sizes=step_sizes,
        seed=seed,
        patience=patience,
        t0=t0,
        cooling=cooling,
    )
    pos, E = opt.optimizar(costo_fn, max_iter=max_iter)
    return pos, E, opt, H


# ==========================================
# 3. PARALELISMO
# ==========================================
def worker_vqe(semilla: int, max_iter: int = 400) -> Dict[str, Any]:
    """Tarea aislada para ProcessPoolExecutor (demo 2 qubits)."""
    t0 = time.time()
    _, E, opt, H = optimizar_vqe(seed=semilla, max_iter=max_iter)
    e_exact = energia_exacta(H)
    return {
        "semilla": semilla,
        "energia": E,
        "energia_exacta": e_exact,
        "error": abs(E - e_exact),
        "iter": opt.iteracion,
        "tiempo_s": time.time() - t0,
        "backend": BACKEND,
        "es_simulacion_clasica": ES_SIMULACION_CLASICA,
    }


def ejecutar_paralelo(
    semillas: Optional[Sequence[int]] = None,
    max_iter: int = 400,
    max_workers: Optional[int] = None,
    usar_procesos: bool = True,
) -> Dict[str, Any]:
    """Lanza varias semillas en paralelo. Devuelve dict con resultados reales.

    Por defecto usa ProcessPoolExecutor con contexto spawn (evita deadlocks
    con pytest/hilos). Si ``usar_procesos=False``, ejecuta en serie.
    """
    if semillas is None:
        semillas = [42, 123, 777, 999, 1024]
    semillas = list(semillas)
    inicio = time.time()
    resultados: List[Dict[str, Any]]
    if not usar_procesos or len(semillas) == 1:
        resultados = [worker_vqe(s, max_iter) for s in semillas]
        modo_pool = "serie"
    else:
        import multiprocessing as mp

        ctx = mp.get_context("spawn")
        try:
            with concurrent.futures.ProcessPoolExecutor(
                max_workers=max_workers, mp_context=ctx
            ) as ex:
                futures = [ex.submit(worker_vqe, s, max_iter) for s in semillas]
                resultados = [f.result() for f in futures]
            modo_pool = "procesos_spawn"
        except Exception:
            # p. ej. ejecución desde stdin / entornos sin spawn fiable
            resultados = [worker_vqe(s, max_iter) for s in semillas]
            modo_pool = "serie_fallback"
    mejor = min(resultados, key=lambda x: x["energia"])
    return {
        "resultados": resultados,
        "mejor": mejor,
        "tiempo_total_s": time.time() - inicio,
        "n_workers": len(semillas),
        "modo_pool": modo_pool,
        "backend": BACKEND,
        "es_simulacion_clasica": ES_SIMULACION_CLASICA,
        "nota": NOTA_HARDWARE,
    }


def main_cli(argv: Optional[List[str]] = None) -> int:
    """CLI mínima: --test / --paralelo (para uso manual)."""
    import sys
    import unittest

    argv = list(sys.argv[1:] if argv is None else argv)
    if "--test" in argv:
        # Los tests viven en tests/test_maestro_cuantico.py; aquí smoke rápido.
        H = crear_hamiltoniano_demo()
        e0 = energia_exacta(H)
        esperado = -math.sqrt(1.09)
        assert abs(e0 - esperado) < 1e-5, (e0, esperado)
        print(f"OK energia_exacta={e0:.8f} (esperado {esperado:.8f})")
        return 0
    if "--paralelo" in argv:
        out = ejecutar_paralelo()
        for r in out["resultados"]:
            print(
                f"  semilla={r['semilla']:4d} | E={r['energia']:+.6f} | "
                f"error={r['error']:.6f} | t={r['tiempo_s']:.2f}s"
            )
        m = out["mejor"]
        print(
            f"mejor semilla={m['semilla']} E={m['energia']:+.6f} "
            f"exacta={m['energia_exacta']:+.6f} total={out['tiempo_total_s']:.2f}s"
        )
        print(NOTA_HARDWARE)
        return 0
    print("Uso: python -m shared.maestro_cuantico --test | --paralelo")
    print(NOTA_HARDWARE)
    return 1


if __name__ == "__main__":
    raise SystemExit(main_cli())
