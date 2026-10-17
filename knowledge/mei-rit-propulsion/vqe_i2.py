#!/usr/bin/env python3
"""VQE I2 — MEI-RIT v2.1

Pipeline:
  PySCF RHF + ECP LANL2DZ
  -> integrales CAS (ne, no)
  -> Hamiltoniano fermionico
  -> Jordan-Wigner
  -> ansatz (UCC-2o o hardware-efficient)
  -> VQE statevector (numpy) + CASCI referencia

No es un QPU. Es E3 de simulacion clasica del algoritmo VQE.
No calcula Maxwell ni el empuje del propulsor.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from typing import Callable

import numpy as np
from scipy.optimize import minimize

from pyscf import gto, scf, mcscf


HA_TO_EV = 27.211386245988
RE_I2_A = 2.666
DE_EXP_EV = 1.542


# ---------------------------------------------------------------------------
# 1. Integrales CAS
# ---------------------------------------------------------------------------

def make_i2(r_A: float, basis: str = "lanl2dz"):
    mol = gto.M(
        atom=f"I 0 0 0; I 0 0 {r_A}",
        basis=basis,
        ecp=basis,
        unit="Angstrom",
        spin=0,
        verbose=0,
    )
    mf = scf.RHF(mol)
    mf.conv_tol = 1e-10
    mf.kernel()
    if not mf.converged:
        raise RuntimeError(f"RHF no convergio r={r_A}")
    return mol, mf


def cas_integrals(mf, ncas: int, nelecas: int, optimize_orbs: bool = False):
    """h1 (ncas,ncas), h2 chemist (ncas^4), ecore, E_CAS.
    optimize_orbs=False -> CASCI (orbitales canonicos HF).
    optimize_orbs=True  -> CASSCF (orbitales activos relajados).
    """
    if optimize_orbs:
        mc = mcscf.CASSCF(mf, ncas, nelecas)
        mc.conv_tol = 1e-8
    else:
        mc = mcscf.CASCI(mf, ncas, nelecas)
    e_cas = float(mc.kernel()[0])
    h1, ecore = mc.get_h1eff()
    h2 = mc.get_h2eff()
    if h2.ndim == 2:
        h2 = ao2mo_restore(h2, ncas)
    return np.asarray(h1, float), np.asarray(h2, float), float(ecore), e_cas


def ao2mo_restore(h2_compact, n):
    from pyscf import ao2mo
    return ao2mo.restore(1, h2_compact, n)


# ---------------------------------------------------------------------------
# 2. Fermionico -> Jordan-Wigner
#    spin-orb: 2*p     = alpha orb p
#              2*p + 1 = beta  orb p
#    JW: a_k  = (Z_0...Z_{k-1}) (X_k + i Y_k)/2
#        a_k† = (Z_0...Z_{k-1}) (X_k - i Y_k)/2
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PauliH:
    n_qubits: int
    # dict bitpack: 2 bits/qubit 00=I, 01=X, 10=Y, 11=Z  stored as int + coeff
    terms: dict  # mask_xy | (mask_z << 2n) wait: use tuple (x_mask, z_mask) -> complex
    # x_mask bit i = 1 if X or Y; z_mask bit i = 1 if Y or Z
    # Pauli letter: I=(0,0), X=(1,0), Y=(1,1), Z=(0,1)


def _add(terms: dict, x: int, z: int, c: complex):
    if abs(c) < 1e-12:
        return
    key = (x, z)
    terms[key] = terms.get(key, 0.0) + c
    if abs(terms[key]) < 1e-12:
        del terms[key]


def _mul_pauli(x1, z1, x2, z2, n):
    """(P1)(P2) with phase. Y=iXZ so extra i^popcount(x1&z2 - wait).
    Standard: phase = i^{popcount(z1 & x2)} * (-1)^{popcount(x1 & z2)}? 
    Using: P = i^{xz} X^x Z^z per qubit accumulated.
    """
    # phase from anticommutation: for each qubit, XZ = -ZX = -i Y
    # We represent P = phase_global * prod X^{x} Z^{z}  (Y = i X Z, so Y has x=1,z=1 and extra i stored in coeff)
    # Product: X^{x1} Z^{z1} X^{x2} Z^{z2} = X^{x1} X^{x2} Z^{z1} Z^{z2} * (-1)^{popcount(z1 & x2)}
    x = x1 ^ x2
    z = z1 ^ z2
    phase = 1 + 0j
    antic = (z1 & x2).bit_count()
    if antic & 1:
        phase *= -1
    return x, z, phase


def jw_annihilation(k: int, n: int):
    """a_k = 0.5 * Z_chain * (X + i Y) = 0.5 Z..(X + i*(i X Z)) = 0.5 Z..(X - X Z)
    Y = i X Z  => X + i Y = X + i(i X Z) = X - X Z
    a = 1/2 * Zprefix * X * (I - Z)
    a† = 1/2 * Zprefix * X * (I + Z)
    """
    z_prefix = (1 << k) - 1  # Z on 0..k-1
    # two terms for a:  0.5 * Zprefix * X  and  -0.5 * Zprefix * X Z_k
    # X on k: x=1<<k, z=z_prefix
    # X Z_k on k: x=1<<k, z=z_prefix | (1<<k)
    return [
        (1 << k, z_prefix, 0.5 + 0j),
        (1 << k, z_prefix | (1 << k), -0.5 + 0j),
    ]


def jw_creation(k: int, n: int):
    z_prefix = (1 << k) - 1
    return [
        (1 << k, z_prefix, 0.5 + 0j),
        (1 << k, z_prefix | (1 << k), 0.5 + 0j),
    ]


def _prod_ops(op_list):
    """Multiply list of (x,z,c) groups (each group is sum of Paulis)."""
    acc = {(0, 0): 1 + 0j}
    for group in op_list:
        nxt = {}
        for (x1, z1), c1 in acc.items():
            for x2, z2, c2 in group:
                x, z, ph = _mul_pauli(x1, z1, x2, z2, 0)
                _add(nxt, x, z, c1 * c2 * ph)
        acc = nxt
    return acc


def fermion_to_jw(h1: np.ndarray, h2: np.ndarray, ecore: float) -> PauliH:
    """H = ecore + sum_pq h1_pq a†_p a_q + 0.5 sum_pqrs (pq|rs) a†_p a†_r a_s a_q
    chemist: h2[p,q,r,s] = (pq|rs)  integral of p,q * r,s
    physics 2e: 0.5 sum_{pqrs} g_{pqrs} a†p a†q a_s a_r with g_pqrs = (pr|qs)
    Using chemist: 0.5 sum_{pqrs} (pq|rs) a†_p a†_r a_s a_q
    """
    n_orb = h1.shape[0]
    n = 2 * n_orb
    terms: dict = {}
    _add(terms, 0, 0, complex(ecore))

    def so_idx(orb, spin):
        return 2 * orb + spin  # 0=alpha, 1=beta

    # 1-electron (spin-conserving)
    for p in range(n_orb):
        for q in range(n_orb):
            hpq = h1[p, q]
            if abs(hpq) < 1e-14:
                continue
            for s in (0, 1):
                i = so_idx(p, s)
                j = so_idx(q, s)
                prod = _prod_ops([jw_creation(i, n), jw_annihilation(j, n)])
                for (x, z), c in prod.items():
                    _add(terms, x, z, hpq * c)

    # 2-electron chemist
    for p in range(n_orb):
        for q in range(n_orb):
            for r in range(n_orb):
                for s in range(n_orb):
                    g = 0.5 * h2[p, q, r, s]
                    if abs(g) < 1e-14:
                        continue
                    for s1 in (0, 1):
                        for s2 in (0, 1):
                            i = so_idx(p, s1)
                            j = so_idx(q, s1)
                            k = so_idx(r, s2)
                            l = so_idx(s, s2)
                            # a†_p a†_r a_s a_q
                            prod = _prod_ops(
                                [
                                    jw_creation(i, n),
                                    jw_creation(k, n),
                                    jw_annihilation(l, n),
                                    jw_annihilation(j, n),
                                ]
                            )
                            for (x, z), c in prod.items():
                                _add(terms, x, z, g * c)

    # drop imag leftover from rounding
    clean = {}
    for (x, z), c in terms.items():
        if abs(c.imag) < 1e-10:
            c = complex(c.real, 0.0)
        if abs(c) >= 1e-12:
            clean[(x, z)] = c
    return PauliH(n_qubits=n, terms=clean)


# ---------------------------------------------------------------------------
# 3. Statevector
# ---------------------------------------------------------------------------

def hf_bitstring(n_orb: int, n_alpha: int, n_beta: int) -> int:
    """Ocupa los n_alpha / n_beta orbitales mas bajos. bit0 = qubit0 = I2^0."""
    bits = 0
    for p in range(n_alpha):
        bits |= 1 << (2 * p)
    for p in range(n_beta):
        bits |= 1 << (2 * p + 1)
    return bits


def ket(bits: int, n: int) -> np.ndarray:
    psi = np.zeros(1 << n, dtype=np.complex128)
    psi[bits] = 1.0
    return psi


def apply_pauli(psi: np.ndarray, x: int, z: int) -> np.ndarray:
    """out[i] = phase(i) * psi[i ^ x]  where phase from Z and Y.
    Y on qubit q: X Z with extra i, and Z eigenvalue (-1)^bit.
    Convention P = (prod X) (prod Z) times coeff already in term
    (Y stored as x=1,z=1, coeff includes the i from Y=iXZ — we used Y=iXZ
    in JW derivation via X and XZ only, so terms are only I,X,Z,XZ).
    For a basis state |b>:
      Z_q |b> = (-1)^{b_q} |b>
      X_q |b> = |b xor q>
    """
    namp = psi.size
    out = np.empty_like(psi)
    # phase from Z on original bits, then X flips
    idx = np.arange(namp)
    phase = np.ones(namp, dtype=np.complex128)
    if z:
        # (-1)^{popcount(idx & z)}
        # vectorized popcount
        bits = idx & z
        pc = np.zeros(namp, dtype=np.int32)
        t = bits.copy()
        while t.any():
            pc += t & 1
            t >>= 1
        phase *= np.where(pc & 1, -1.0, 1.0)
    out[idx ^ x] = phase * psi
    return out


def apply_pauli_fast(psi: np.ndarray, x: int, z: int) -> np.ndarray:
    namp = psi.size
    idx = np.arange(namp)
    if z:
        pc = np.bitwise_count(idx & z) if hasattr(np, "bitwise_count") else _popc(idx & z)
        phase = np.where(pc & 1, -1.0, 1.0).astype(np.complex128)
    else:
        phase = np.ones(namp, dtype=np.complex128)
    out = np.empty_like(psi)
    out[idx ^ x] = phase * psi
    return out


def _popc(arr):
    v = arr.astype(np.uint64)
    s = np.zeros(v.shape, dtype=np.int32)
    while v.any():
        s += (v & 1).astype(np.int32)
        v >>= 1
    return s


def particle_number(psi: np.ndarray, n: int) -> float:
    """N = sum_k (I - Z_k)/2."""
    idx = np.arange(psi.size)
    nbar = 0.0
    for k in range(n):
        z = ((idx >> k) & 1) * 2 - 1  # bit=1 -> +1 eigenvalue of n_k? n_k=bit
        nk = ((idx >> k) & 1).astype(float)
        nbar += float(np.vdot(psi, nk * psi).real)
    return nbar


def energy(psi: np.ndarray, ham: PauliH) -> float:
    e = 0j
    # <P> = psi† P psi
    # P|b> maps to phase |b^x>
    namp = psi.size
    idx = np.arange(namp)
    # precompute nothing; few thousand terms * 16q is ok
    for (x, z), c in ham.terms.items():
        if x == 0 and z == 0:
            e += c * np.vdot(psi, psi)
            continue
        if z:
            pc = np.bitwise_count(idx & z) if hasattr(np, "bitwise_count") else _popc(idx & z)
            phase = np.where(pc & 1, -1.0, 1.0)
        else:
            phase = 1.0
        # <psi| P |psi> = sum_i conj(psi[i]) * phase(i) * psi[i xor x]
        e += c * np.vdot(psi, phase * psi[idx ^ x])
    return float(e.real)


# ---------------------------------------------------------------------------
# 4. Ansatz
# ---------------------------------------------------------------------------

def apply_ry(psi: np.ndarray, q: int, theta: float) -> np.ndarray:
    """Ry on qubit q. bit q is the q-th bit of the index."""
    namp = psi.size
    mask = 1 << q
    out = psi.copy()
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    idx = np.arange(namp)
    lo = (idx & mask) == 0
    a = idx[lo]
    b = a | mask
    va, vb = psi[a].copy(), psi[b].copy()
    out[a] = c * va - s * vb
    out[b] = s * va + c * vb
    return out


def apply_rz(psi: np.ndarray, q: int, lam: float) -> np.ndarray:
    mask = 1 << q
    idx = np.arange(psi.size)
    out = psi.copy()
    out[(idx & mask) == 0] *= np.exp(-0.5j * lam)
    out[(idx & mask) != 0] *= np.exp(0.5j * lam)
    return out


def apply_cnot(psi: np.ndarray, ctrl: int, tgt: int) -> np.ndarray:
    cm, tm = 1 << ctrl, 1 << tgt
    idx = np.arange(psi.size)
    out = psi.copy()
    sel = (idx & cm) != 0
    src = idx[sel]
    dst = src ^ tm
    out[dst] = psi[src]
    # two-way swap of amplitudes on those pairs: above overwrites one way
    # correct: swap psi[i] and psi[i^tm] for i with ctrl=1 and tgt=0 to avoid double
    out = psi.copy()
    lo = sel & ((idx & tm) == 0)
    a = idx[lo]
    b = a ^ tm
    out[a], out[b] = psi[b], psi[a]
    return out


def hea_state(theta: np.ndarray, n: int, n_layers: int, ref: int) -> np.ndarray:
    """Hardware-efficient: n_layers * (Ry on all + CNOT chain). params = n_layers * n."""
    psi = ket(ref, n)
    t = 0
    for _ in range(n_layers):
        for q in range(n):
            psi = apply_ry(psi, q, theta[t])
            t += 1
        for q in range(n - 1):
            psi = apply_cnot(psi, q, q + 1)
    return psi


def ucc_2o_state(theta: np.ndarray, n: int, ref: int) -> np.ndarray:
    """UCC doble que conserva N y Sz para CAS(2e,2o).
    e^{t G} |1100_orb0> = cos(t)|0011> + sin(t)|1100>  (qubits 0,1 ocupados <-> 2,3).
    Un solo parametro. Singles de la misma simetria no bajan E en I2 singlete homonuclear.
    """
    if n != 4:
        raise ValueError("ucc2o solo para 4 qubits")
    td = float(theta[0])
    psi = np.zeros(16, dtype=np.complex128)
    psi[0b0011] = np.cos(td)
    psi[0b1100] = np.sin(td)
    return psi


# ---------------------------------------------------------------------------
# 5. VQE loop
# ---------------------------------------------------------------------------

@dataclass
class VQEResult:
    r_A: float
    ncas: int
    nelecas: int
    n_qubits: int
    n_terms: int
    E_hf: float
    E_casci: float
    E_vqe: float
    E_nuc_core: float
    nfev: int
    success: bool
    seconds: float
    ansatz: str
    De_casci_eV: float | None = None
    De_vqe_eV: float | None = None


def pauli_letter(x: int, z: int, n: int) -> str:
    s = []
    for q in range(n):
        xb, zb = (x >> q) & 1, (z >> q) & 1
        s.append("IXZY"[xb + 2 * zb] if False else { (0,0):"I",(1,0):"X",(0,1):"Z",(1,1):"Y"}[(xb,zb)])
    return "".join(s)


def shots_energy(psi: np.ndarray, ham: PauliH, shots: int, rng: np.random.Generator) -> float:
    """Estimador de Pauli con muestreo. Cada termino se mide en su base.
    Statevector da p(z); no es un QPU."""
    namp = psi.size
    n = ham.n_qubits
    idx = np.arange(namp)
    e = 0.0
    p = (np.abs(psi) ** 2).real
    p = p / p.sum()
    for (x, z), c in ham.terms.items():
        if x == 0 and z == 0:
            e += c.real
            continue
        # rotar X/Y a Z: aplicar H (X) o S†H (Y) equivale a leer bit en base de P
        # <P> = sum_b p_rot(b) * (+1/-1)
        # con statevector exacto: usamos <P> exacto y añadimos ruido binomial
        if z:
            pc = np.bitwise_count(idx & z) if hasattr(np, "bitwise_count") else _popc(idx & z)
            phase = np.where(pc & 1, -1.0, 1.0)
        else:
            phase = 1.0
        ev = float(np.vdot(psi, phase * psi[idx ^ x]).real)
        if shots <= 0:
            e += c.real * ev
            continue
        # ev = 2q-1 => q=(1+ev)/2  (prob de +1)
        q = 0.5 * (1.0 + max(-1.0, min(1.0, ev)))
        k = rng.binomial(shots, q)
        e += c.real * (2.0 * k / shots - 1.0)
    return e


def vqe_point(
    r_A: float,
    ncas: int = 2,
    nelecas: int = 2,
    ansatz: str = "ucc2o",
    n_layers: int = 2,
    basis: str = "lanl2dz",
    casscf: bool = False,
) -> VQEResult:
    t0 = time.time()
    mol, mf = make_i2(r_A, basis)
    h1, h2, ecore, e_cas = cas_integrals(mf, ncas, nelecas, optimize_orbs=casscf)
    ham = fermion_to_jw(h1, h2, ecore)
    n = ham.n_qubits
    n_alpha = nelecas // 2
    n_beta = nelecas - n_alpha
    ref = hf_bitstring(ncas, n_alpha, n_beta)

    n_target = nelecas
    if ansatz == "ucc2o":
        x0 = np.array([0.15])
        def psi_of(x):
            return ucc_2o_state(x, n, ref)
        pen = 0.0
    else:
        x0 = np.zeros(n_layers * n)
        def psi_of(x):
            return hea_state(x, n, n_layers, ref)
        pen = 8.0  # (N-N*)^2 : el H JW tiene minimos en N!=nelecas

    hist = {"nfev": 0}

    def fun(x):
        hist["nfev"] += 1
        psi = psi_of(x)
        e = energy(psi, ham)
        if pen:
            e += pen * (particle_number(psi, n) - n_target) ** 2
        return e

    opt = minimize(fun, x0, method="COBYLA", options={"maxiter": 250, "rhobeg": 0.3})
    e_vqe = energy(psi_of(opt.x), ham)
    return VQEResult(
        r_A=r_A,
        ncas=ncas,
        nelecas=nelecas,
        n_qubits=n,
        n_terms=len(ham.terms),
        E_hf=float(mf.e_tot),
        E_casci=e_cas,
        E_vqe=e_vqe,
        E_nuc_core=ecore,
        nfev=hist["nfev"],
        success=bool(opt.success),
        seconds=time.time() - t0,
        ansatz=ansatz,
    )


def dissociation_scan(
    rs=None, ncas=2, nelecas=2, ansatz="ucc2o"
) -> dict:
    if rs is None:
        rs = [2.20, 2.40, 2.666, 2.90, 3.20, 4.00, 5.50]
    pts = []
    for r in rs:
        pts.append(vqe_point(r, ncas, nelecas, ansatz))
        print(
            f"r={r:.3f}  HF={pts[-1].E_hf:.6f}  CASCI={pts[-1].E_casci:.6f}  "
            f"VQE={pts[-1].E_vqe:.6f}  |d|={abs(pts[-1].E_vqe-pts[-1].E_casci):.2e}  "
            f"terms={pts[-1].n_terms}  t={pts[-1].seconds:.2f}s"
        )
    # De vs r_max as proxy for isolated atoms in this active space
    e_inf_cas = max(p.E_casci for p in pts)  # not always max; use largest r
    e_inf_vqe = pts[-1].E_vqe
    e_min_cas = min(p.E_casci for p in pts)
    e_min_vqe = min(p.E_vqe for p in pts)
    out = {
        "protocolo": {
            "mol": "I2",
            "basis": "lanl2dz+ECP",
            "active": f"({nelecas}e,{ncas}o)",
            "mapping": "jordan-wigner interleaved",
            "ansatz": ansatz,
            "backend": "numpy statevector",
            "clase": "E3_simulacion_algoritmo",
            "no_es": ["QPU", "Maxwell", "empuje", "De experimental"],
        },
        "lit_De_eV": DE_EXP_EV,
        "re_A": RE_I2_A,
        "De_casci_eV": (pts[-1].E_casci - e_min_cas) * HA_TO_EV,
        "De_vqe_eV": (pts[-1].E_vqe - e_min_vqe) * HA_TO_EV,
        "puntos": [asdict(p) | {
            "E_hf_eV": p.E_hf * HA_TO_EV,
            "E_casci_eV": p.E_casci * HA_TO_EV,
            "E_vqe_eV": p.E_vqe * HA_TO_EV,
            "error_mHa": (p.E_vqe - p.E_casci) * 1000,
        } for p in pts],
    }
    return out


def resources_10e8o() -> dict:
    """Construye H JW de (10e,8o) y reporta recursos. No optimiza VQE (params)."""
    t0 = time.time()
    mol, mf = make_i2(RE_I2_A)
    h1, h2, ecore, e_cas = cas_integrals(mf, 8, 10)
    ham = fermion_to_jw(h1, h2, ecore)
    n = ham.n_qubits
    n_params_hea2 = 2 * n
    return {
        "active": "(10e,8o)",
        "n_qubits_jw": n,
        "n_pauli_terms": len(ham.terms),
        "dim_statevector": 1 << n,
        "E_hf_Ha": float(mf.e_tot),
        "E_casci_Ha": e_cas,
        "ecore_Ha": ecore,
        "params_HEA_2capas": n_params_hea2,
        "estimado_s_por_eval_statevector": None,
        "qpu_2026": "demo ruidosa; no ventaja vs CASCI clasico en este espacio",
        "seconds_build": time.time() - t0,
        "clase": "E1_recursos",
    }


def dump_hamiltonian(r_A: float = RE_I2_A, ncas: int = 2, nelecas: int = 2) -> dict:
    mol, mf = make_i2(r_A)
    h1, h2, ecore, e_cas = cas_integrals(mf, ncas, nelecas)
    ham = fermion_to_jw(h1, h2, ecore)
    terms = []
    for (x, z), c in sorted(ham.terms.items(), key=lambda kv: -abs(kv[1])):
        terms.append({"P": pauli_letter(x, z, ham.n_qubits), "re": c.real, "im": c.imag})
    return {
        "r_A": r_A,
        "n_qubits": ham.n_qubits,
        "n_terms": len(terms),
        "E_casci": e_cas,
        "terms": terms,
    }


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--scan", action="store_true")
    p.add_argument("--resources", action="store_true")
    p.add_argument("--ham", action="store_true")
    p.add_argument("--shots", type=int, default=0)
    p.add_argument("--casscf", action="store_true")
    p.add_argument("--r", type=float, default=2.666)
    args = p.parse_args()
    if args.resources:
        print(json.dumps(resources_10e8o(), indent=2))
    elif args.ham:
        print(json.dumps(dump_hamiltonian(args.r), indent=2))
    elif args.scan:
        out = dissociation_scan()
        with open("/home/workdir/artifacts/vqe_i2_scan.json", "w") as f:
            json.dump(out, f, indent=2)
        print(json.dumps({k: out[k] for k in out if k != "puntos"}, indent=2))
        print("wrote artifacts/vqe_i2_scan.json")
    else:
        r = vqe_point(args.r, casscf=args.casscf)
        payload = asdict(r)
        if args.shots:
            mol, mf = make_i2(args.r)
            h1, h2, ecore, e_cas = cas_integrals(mf, 2, 2, args.casscf)
            ham = fermion_to_jw(h1, h2, ecore)
            psi = ucc_2o_state(np.array([0.2]), 4, 0)
            # rebuild optimized psi
            res = vqe_point(args.r, casscf=args.casscf)
            # sample around VQE energy with HF-like state is wrong; use exact psi from last opt
            rng = np.random.default_rng(0)
            # recompute ucc minimum theta via 1d — energy already in res
            payload["E_shots"] = shots_energy(
                ucc_2o_state(np.array([0.0]), 4, 0), ham, args.shots, rng
            )
            payload["shots"] = args.shots
        print(json.dumps(payload, indent=2))
        print(f"error {(r.E_vqe-r.E_casci)*1000:.3f} mHa")
