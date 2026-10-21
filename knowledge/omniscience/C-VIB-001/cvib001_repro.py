#!/usr/bin/env python3
"""C-VIB-001 (v1.1: H4 compara ω² (Bloch y anillo), ARPACK con v0 fijo, H5 exige ≥2 gaps; capas de igual tiempo de tránsito cierran los gaps pares)
C-VIB-001 — reimplementación mínima reproducible (OMNISCIENCE).
Prueba H1–H6 frente a soluciones analíticas con tolerancias declaradas ANTES de ejecutar.
Uso: python cvib001_repro.py --out DIR   (semilla fija = 7)
"""
import argparse, json, hashlib, os, platform, sys
import numpy as np, scipy, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy import signal
from scipy.linalg import eigh_tridiagonal, eigh
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh

SEED = 7
# ---- Tolerancias pre-declaradas (no modificar tras ver resultados) ----
TOL = {
 "H1_amp_rel": 5e-3, "H1_phase_abs_rad": 1e-2, "H1_Q_rel": 2e-2,
 "H2_peak_bin_hz": 1.0, "H2_burst_onset_s": 0.15, "H2_burst_contrast_db": 20.0, "H2_tone_cv": 0.25,
 "H3_freq_rel": 1e-3, "H3_node_rel": 1e-6, "H3_shape_corr": 0.9999, "H3_membrane_rel": 1e-2,
 "H4_disp_rel": 1e-9, "H4_ring_rel": 1e-9,
 "H5_energy_abs": 1e-9, "H5_min_gaps": 2, "H5_gapcenter_T2_max": 0.01, "H5_pass_mean_T2_min": 0.5, "H5_flat_std_min": 0.1,
 "H6_E_rel": 1e-3,
}
FIG_META = {"Software": None}

def savefig(fig, path):
    fig.savefig(path, dpi=110, metadata=FIG_META); plt.close(fig)

# ---------------- H1: oscilador amortiguado forzado ----------------
def H1(out):
    m, w0, zeta, F0 = 1.0, 2*np.pi, 0.05, 1.0
    k, c = m*w0**2, 2*zeta*m*w0
    def amp_phase(w):
        A = F0/np.sqrt((k-m*w**2)**2 + (c*w)**2); phi = np.arctan2(c*w, k-m*w**2); return A, phi
    res = {}; ratios = [0.5, 0.9, 1.0, 1.1, 2.0]; rows = []
    for r in ratios:
        w = r*w0; T = 2*np.pi/w; tend = 60/(zeta*w0) // T * T  # >> tiempo de relajación
        sol = solve_ivp(lambda t, y: [y[1], (F0*np.cos(w*t) - c*y[1] - k*y[0])/m], (0, tend), [0, 0],
                        method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
        t = np.linspace(tend-10*T, tend, 4001); x = sol.sol(t)[0]
        # x = a cos wt + b sin wt  -> A=sqrt(a²+b²), retraso phi = atan2(b,a)
        G = np.vstack([np.cos(w*t), np.sin(w*t)]).T; a, b = np.linalg.lstsq(G, x, rcond=None)[0]
        An, phn = np.hypot(a, b), np.arctan2(b, a); Aa, pha = amp_phase(w)
        rows.append({"w_over_w0": r, "A_num": An, "A_ana": Aa, "rel_err": abs(An-Aa)/Aa, "phase_num": phn, "phase_ana": pha, "phase_err": abs(phn-pha)})
    # Q y ancho de banda de potencia (analítico vs muestreo fino)
    ws = np.linspace(0.8*w0, 1.2*w0, 200001); P = amp_phase(ws)[0]**2
    half = ws[P >= P.max()/2]; Q_num = w0/(half[-1]-half[0]); Q_ana = 1/(2*zeta)
    worst_amp = max(r["rel_err"] for r in rows); worst_ph = max(r["phase_err"] for r in rows)
    res = {"params": {"m": m, "w0": w0, "zeta": zeta, "F0": F0}, "rows": rows,
           "Q_num_halfpower": Q_num, "Q_ana_1_over_2zeta": Q_ana, "Q_rel_err": abs(Q_num-Q_ana)/Q_ana,
           "phase_at_resonance": rows[2]["phase_num"],
           "pass": bool(worst_amp < TOL["H1_amp_rel"] and worst_ph < TOL["H1_phase_abs_rad"] and abs(Q_num-Q_ana)/Q_ana < TOL["H1_Q_rel"]),
           "metric": f"max err rel amplitud={worst_amp:.2e}; max err fase={worst_ph:.2e} rad; Q={Q_num:.4f} vs {Q_ana:.4f}"}
    # figura
    w = w0; tend = 15
    sol = solve_ivp(lambda t, y: [y[1], (F0*np.cos(w*t) - c*y[1] - k*y[0])/m], (0, tend), [0, 0], method="DOP853", rtol=1e-10, atol=1e-12, dense_output=True)
    t = np.linspace(0, tend, 6000); fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(t, sol.sol(t)[0], lw=0.8); ax[0].axhline(amp_phase(w0)[0], ls="--", c="r"); ax[0].axhline(-amp_phase(w0)[0], ls="--", c="r")
    ax[0].set(title="H1: transitorio forzado en ω=ω0 (ζ=0.05)", xlabel="t [s]", ylabel="x")
    wr = np.linspace(0.2, 2.5, 800)*w0; ax[1].plot(wr/w0, amp_phase(wr)[0], label="analítica")
    ax[1].plot([r["w_over_w0"] for r in rows], [r["A_num"] for r in rows], "o", label="ODE (régimen permanente)")
    ax[1].set(title="Curva de resonancia", xlabel="ω/ω0", ylabel="A"); ax[1].legend()
    savefig(fig, os.path.join(out, "H1_oscilador.png")); return res

# ---------------- H2: FFT vs espectrograma ----------------
def H2(out):
    rng = np.random.default_rng(SEED); fs, T = 2000.0, 4.0; t = np.arange(0, T, 1/fs)
    chirp = signal.chirp(t, f0=40, t1=T, f1=120, method="linear")
    tone = 0.8*np.sin(2*np.pi*180*t)
    burst = np.where((t >= 2.2) & (t < 3.2), 1.0, 0.0)*np.sin(2*np.pi*320*t)
    x = chirp + tone + burst + 0.3*rng.standard_normal(t.size); x -= x.mean()
    X = np.abs(np.fft.rfft(x*np.hanning(x.size))); f = np.fft.rfftfreq(x.size, 1/fs)
    def peak(lo, hi): s = (f >= lo) & (f <= hi); return float(f[s][np.argmax(X[s])])
    p180, p320 = peak(170, 190), peak(310, 330)
    band_chirp = X[(f >= 40) & (f <= 120)].mean(); band_noise = X[(f >= 500) & (f <= 900)].mean()
    fS, tS, S = signal.spectrogram(x, fs=fs, window="hann", nperseg=256, noverlap=192, mode="psd")
    b320 = S[(fS >= 310) & (fS <= 330)].sum(0); b180 = S[(fS >= 170) & (fS <= 190)].sum(0)
    before = b320[tS < 2.1].mean(); after = b320[(tS > 2.3) & (tS < 3.1)].mean()
    contrast_db = 10*np.log10(after/before)
    thr = np.sqrt(before*after); onset = float(tS[np.argmax(b320 > thr)])
    cv180 = float(b180.std()/b180.mean())
    ok = (abs(p180-180) <= TOL["H2_peak_bin_hz"] and abs(p320-320) <= TOL["H2_peak_bin_hz"] and band_chirp > 3*band_noise
          and abs(onset-2.2) <= TOL["H2_burst_onset_s"] and contrast_db >= TOL["H2_burst_contrast_db"] and cv180 <= TOL["H2_tone_cv"])
    fig, ax = plt.subplots(3, 1, figsize=(10, 8))
    ax[0].plot(t, x, lw=0.4); ax[0].set(title="H2: señal sintética (semilla 7)", xlabel="t [s]")
    ax[1].semilogy(f, X); ax[1].set(xlim=(0, 500), title="FFT (Hann)", xlabel="f [Hz]")
    ax[2].pcolormesh(tS, fS, 10*np.log10(S+1e-12), shading="auto"); ax[2].set(ylim=(0, 500), title="Espectrograma (nperseg=256, solape 75 %)", xlabel="t [s]", ylabel="f [Hz]")
    fig.tight_layout(); savefig(fig, os.path.join(out, "H2_fft_espectrograma.png"))
    return {"peak180_hz": p180, "peak320_hz": p320, "chirp_band_over_noise": float(band_chirp/band_noise),
            "burst_onset_s": onset, "burst_contrast_db": float(contrast_db), "tone180_cv": cv180, "pass": bool(ok),
            "metric": f"picos {p180:.2f}/{p320:.2f} Hz; onset burst {onset:.3f} s (esperado 2.2); contraste {contrast_db:.1f} dB; CV tono {cv180:.3f}"}

# ---------------- H3: cuerda de Dirichlet (+ membrana) ----------------
def H3(out):
    L, N = 1.0, 401; h = L/(N+1); x = np.arange(1, N+1)*h
    w2, V = eigh_tridiagonal(np.full(N, 2/h**2), np.full(N-1, -1/h**2), select="i", select_range=(0, 5))
    fn = np.sqrt(w2)/(2*np.pi); ratios = fn/fn[0]; n = np.arange(1, 7)
    f_ana = n/(2*L)  # c=1
    rel = np.abs(fn-f_ana)/f_ana; rel_ratio = np.abs(ratios-n)/n
    psi2 = V[:, 1]; mid = N//2; node = abs(psi2[mid])/np.abs(psi2).max()
    corr = [abs(np.dot(V[:, i], np.sin((i+1)*np.pi*x/L)))/np.linalg.norm(np.sin((i+1)*np.pi*x/L)) for i in range(6)]
    # membrana rectangular a×b (c=1): f_mn = 0.5*sqrt((m/a)²+(n/b)²)
    a, b, Nx, Ny = 1.0, 1.5, 59, 89; hx, hy = a/(Nx+1), b/(Ny+1)
    Dx = diags([np.full(Nx-1, -1.0), np.full(Nx, 2.0), np.full(Nx-1, -1.0)], [-1, 0, 1])/hx**2
    Dy = diags([np.full(Ny-1, -1.0), np.full(Ny, 2.0), np.full(Ny-1, -1.0)], [-1, 0, 1])/hy**2
    Lap = kron(identity(Ny), Dx) + kron(Dy, identity(Nx))
    ev = np.sort(eigsh(Lap.tocsc(), k=6, sigma=0, which="LM", v0=np.ones(Nx*Ny))[0]); fm = np.sqrt(ev)/(2*np.pi)  # [v1.1] v0 fijo: determinista
    fa = np.sort([0.5*np.hypot(mm/a, nn/b) for mm in range(1, 6) for nn in range(1, 6)])[:6]
    relm = np.abs(fm-fa)/fa
    ok = rel.max() < TOL["H3_freq_rel"] and node < TOL["H3_node_rel"] and min(corr) > TOL["H3_shape_corr"] and relm.max() < TOL["H3_membrane_rel"]
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for i in range(4): ax[0].plot(np.r_[0, x, L], np.r_[0, V[:, i]/np.abs(V[:, i]).max(), 0] + 2.2*i, label=f"n={i+1}")
    ax[0].set(title="H3: modos de cuerda (FD) ", xlabel="x/L"); ax[0].legend(fontsize=7)
    ax[1].plot(n, fn, "o", label="FD"); ax[1].plot(n, f_ana, "-", label="n·f1 analítico"); ax[1].set(title="Espectro armónico", xlabel="n", ylabel="f_n"); ax[1].legend()
    savefig(fig, os.path.join(out, "H3_cuerda.png"))
    return {"f_num": fn.tolist(), "f_ana": f_ana.tolist(), "max_rel_err_f": float(rel.max()), "max_rel_err_ratio": float(rel_ratio.max()),
            "node_n2_at_L_over_2": float(node), "min_shape_corr": float(min(corr)), "membrane_f_num": fm.tolist(), "membrane_f_ana": fa.tolist(),
            "membrane_max_rel_err": float(relm.max()), "pass": bool(ok),
            "metric": f"err rel f_n≤{rel.max():.2e}; |ψ2(L/2)|/max={node:.1e}; corr forma≥{min(corr):.6f}; membrana err≤{relm.max():.2e}"}

# ---------------- H4: cadena diatómica 1D ----------------
def H4(out):
    K, m1, m2, a = 1.0, 1.0, 2.2, 1.0; ks = np.linspace(-np.pi/a, np.pi/a, 401)
    def D(k): return np.array([[2*K/m1, -K*(1+np.exp(-1j*k*a))/np.sqrt(m1*m2)], [-K*(1+np.exp(1j*k*a))/np.sqrt(m1*m2), 2*K/m2]])
    num = np.array([np.sqrt(np.clip(np.linalg.eigvalsh(D(k)), 0, None)) for k in ks])
    s = 1/m1 + 1/m2; disc = np.sqrt(s**2 - 4*np.sin(ks*a/2)**2/(m1*m2))
    ana2 = np.c_[K*(s-disc), K*(s+disc)]; ana = np.sqrt(ana2)
    num2 = np.array([np.linalg.eigvalsh(D(k)) for k in ks])
    # [v1.1] comparar ω² (la raíz cerca de ω=0 amplifica el redondeo ~1e-16 a ~1e-8)
    rel = np.abs(num2-ana2).max()/ana2.max()
    w_ac, w_op = np.sqrt(2*K/m2), np.sqrt(2*K/m1)
    # anillo finito de 2N átomos (ruta independiente: diagonalización en espacio real)
    Nc = 100; M = np.tile([m1, m2], Nc); n = 2*Nc; Phi = np.zeros((n, n))
    for i in range(n): Phi[i, i] = 2*K; Phi[i, (i+1) % n] = Phi[(i+1) % n, i] = -K
    w_ring = np.sqrt(np.clip(eigh(Phi/np.sqrt(np.outer(M, M)), eigvals_only=True), 0, None))
    in_gap = int(((w_ring > w_ac*(1+1e-9)) & (w_ring < w_op*(1-1e-9))).sum())
    ring_ac_max = w_ring[:Nc].max(); ring_op_min = w_ring[Nc:].min()
    # monoatómica
    mono_num = np.array([2*np.sqrt(K/m1)*abs(np.sin(k*a/2)) for k in ks])
    Phim = np.zeros((Nc, Nc))
    for i in range(Nc): Phim[i, i] = 2*K; Phim[i, (i+1) % Nc] = Phim[(i+1) % Nc, i] = -K
    wm2 = np.sort(eigh(Phim/m1, eigvals_only=True))  # [v1.1] comparar ω²
    wm2_ana = np.sort(4*(K/m1)*np.sin(np.pi*np.arange(Nc)/Nc)**2)
    mono_rel = np.abs(wm2-wm2_ana).max()/wm2_ana.max()
    ok = (rel < TOL["H4_disp_rel"] and w_op > w_ac and in_gap == 0 and abs(ring_ac_max-w_ac)/w_ac < TOL["H4_ring_rel"]
          and abs(ring_op_min-w_op)/w_op < TOL["H4_ring_rel"] and mono_rel < TOL["H4_ring_rel"])
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(ks, mono_num); ax[0].set(title="Monoatómica ω=2√(K/m)|sin(ka/2)|", xlabel="k")
    ax[1].plot(ks, num[:, 0], label="acústica"); ax[1].plot(ks, num[:, 1], label="óptica"); ax[1].axhspan(w_ac, w_op, color="grey", alpha=0.3, label="gap")
    ax[1].set(title=f"H4: diatómica m2/m1={m2/m1}", xlabel="k"); ax[1].legend()
    savefig(fig, os.path.join(out, "H4_dispersion.png"))
    return {"max_rel_err_bloch_vs_analytic_omega2": float(rel), "w_ac_pi": w_ac, "w_op_pi": w_op, "gap": w_op-w_ac,
            "ring_ac_max": float(ring_ac_max), "ring_op_min": float(ring_op_min), "ring_modes_in_gap": in_gap,
            "mono_ring_rel_err": float(mono_rel), "pass": bool(ok),
            "metric": f"gap ω_op(π)-ω_ac(π)={w_op-w_ac:.4f} (ω_ac={w_ac:.4f}, ω_op={w_op:.4f}); err Bloch={rel:.1e}; modos del anillo en el gap={in_gap}"}

# ---------------- H5: cristal fonónico 1D (matriz de transferencia) ----------------
def H5(out):
    rhoA, cA, dA = 1.0, 1.0, 0.5; rhoB, cB, dB = 4.0, 1.0, 0.5; ZA, ZB = rhoA*cA, rhoB*cB; Ncell = 12; a = dA+dB
    w = np.linspace(1e-3, 4*np.pi, 20001)
    def layer(Z, c, d, w):
        kd = w*d/c; return np.array([[np.cos(kd), 1j*Z*np.sin(kd)], [1j*np.sin(kd)/Z, np.cos(kd)]])
    T2 = np.empty_like(w); R2 = np.empty_like(w)
    for i, wi in enumerate(w):
        cell = layer(ZA, cA, dA, wi) @ layer(ZB, cB, dB, wi); M = np.linalg.matrix_power(cell, Ncell)
        den = M[0, 0] + M[0, 1]/ZA + ZA*M[1, 0] + M[1, 1]
        T2[i] = abs(2/den)**2; R2[i] = abs((M[0, 0] + M[0, 1]/ZA - ZA*M[1, 0] - M[1, 1])/den)**2
    # Bloch analítico: cos(qa) = cos kA dA cos kB dB − ½(ZA/ZB+ZB/ZA) sin kA dA sin kB dB
    rhs = np.cos(w*dA/cA)*np.cos(w*dB/cB) - 0.5*(ZA/ZB+ZB/ZA)*np.sin(w*dA/cA)*np.sin(w*dB/cB)
    gap = np.abs(rhs) > 1
    # centros de gap: máximos locales de |rhs| dentro de cada gap
    edges = np.flatnonzero(np.diff(gap.astype(int))); segs = []
    starts = np.r_[0, edges+1] if gap[0] else edges[::2]+1
    lab = np.cumsum(np.r_[0, np.abs(np.diff(gap.astype(int)))])
    centers = []
    for L_ in np.unique(lab[gap]):
        idx = np.flatnonzero(lab == L_); centers.append(idx[np.argmax(np.abs(rhs[idx]))])
    T2_centers = T2[centers]; deep = np.abs(rhs) > 1.05; passband = np.abs(rhs) < 0.95
    energy_err = np.abs(T2+R2-1).max()
    ok = (energy_err < TOL["H5_energy_abs"] and len(centers) >= TOL["H5_min_gaps"] and T2_centers.max() < TOL["H5_gapcenter_T2_max"]
          and T2[passband].mean() > TOL["H5_pass_mean_T2_min"] and T2.std() > TOL["H5_flat_std_min"])
    fig, ax = plt.subplots(figsize=(10, 4)); ax.plot(w*a/np.pi, T2, lw=0.8, label="|T|² (TMM, N=12)")
    ax.fill_between(w*a/np.pi, 0, 1, where=gap, color="grey", alpha=0.3, label="gap de Bloch (analítico)")
    ax.set(title="H5: cristal fonónico 1D A–B, Z2/Z1=4", xlabel="ωa/(πc)", ylabel="|T|²"); ax.legend()
    savefig(fig, os.path.join(out, "H5_cristal_fononico_T.png"))
    return {"Z_ratio": ZB/ZA, "N": Ncell, "n_gaps_found": len(centers), "gap_center_freqs_wa_over_pi": (w[centers]*a/np.pi).tolist(),
            "T2_at_gap_centers": T2_centers.tolist(), "T2_mean_passband": float(T2[passband].mean()), "T2_mean_deep_gap": float(T2[deep].mean()),
            "T2_std": float(T2.std()), "max_energy_error": float(energy_err), "pass": bool(ok),
            "metric": f"{len(centers)} gaps; |T|² máx en centros={T2_centers.max():.2e}; |T|² medio en bandas={T2[passband].mean():.3f}; |R|²+|T|²−1≤{energy_err:.1e}"}

# ---------------- H6: oscilador armónico cuántico ----------------
def H6(out):
    N, xmax = 4001, 12.0; x = np.linspace(-xmax, xmax, N); h = x[1]-x[0]
    E, V = eigh_tridiagonal(1/h**2 + 0.5*x**2, np.full(N-1, -0.5/h**2), select="i", select_range=(0, 9))
    n = np.arange(10); Ea = n+0.5; rel = np.abs(E-Ea)/Ea
    nodes = []
    for i in range(10):
        psi = V[:, i]; mask = np.abs(psi) > 1e-4*np.abs(psi).max(); p = psi[mask]
        nodes.append(int(np.sum(np.sign(p[1:]) != np.sign(p[:-1]))))
    ok = rel.max() < TOL["H6_E_rel"] and nodes == list(n)
    fig, ax = plt.subplots(figsize=(7, 6)); ax.plot(x, 0.5*x**2, "k", lw=0.8)
    for i in range(6): ax.plot(x, E[i] + 0.8*V[:, i]**2/np.max(V[:, i]**2), label=f"n={i}, E={E[i]:.4f}")
    ax.set(xlim=(-5, 5), ylim=(0, 7), title="H6: QHO, |ψ_n|² desplazadas a E_n (ħ=m=ω=1)", xlabel="x"); ax.legend(fontsize=7)
    savefig(fig, os.path.join(out, "H6_qho.png"))
    return {"E_num": E.tolist(), "E_ana": Ea.tolist(), "max_rel_err_E": float(rel.max()), "nodes": nodes, "pass": bool(ok),
            "metric": f"err rel E_n≤{rel.max():.2e} (n=0..9); nodos={nodes}"}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True); np.random.seed(SEED)
    results = {"campaign": "C-VIB-001", "implementation": "cvib001_repro.py (reimplementación mínima; código original no recuperado)",
               "seed": SEED, "tolerances": TOL}
    for name, fn in [("H1", H1), ("H2", H2), ("H3", H3), ("H4", H4), ("H5", H5), ("H6", H6)]:
        results[name] = fn(args.out)
    results["all_pass"] = all(results[h]["pass"] for h in ["H1", "H2", "H3", "H4", "H5", "H6"])
    with open(os.path.join(args.out, "results.json"), "w") as f: json.dump(results, f, indent=1, ensure_ascii=False, default=float)
    for h in ["H1", "H2", "H3", "H4", "H5", "H6"]: print(h, "PASS" if results[h]["pass"] else "FAIL", "|", results[h]["metric"])
    print("ALL_PASS", results["all_pass"])

if __name__ == "__main__": main()
