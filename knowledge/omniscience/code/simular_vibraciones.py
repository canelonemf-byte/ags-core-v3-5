#!/usr/bin/env python3
"""
Simulaciones reproducibles de vibraciones científicas.
Autor conceptual: análisis Grok para Lázaro López Paz
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch
from scipy.fft import rfft, rfftfreq
from scipy.signal import spectrogram, windows
from scipy.integrate import solve_ivp

# Carpeta de salida configurable (antes fija en /home/workdir/artifacts/vibraciones/figs).
# VIBRACIONES_OUT=<dir>  (por defecto ./out/figs, relativo al directorio de trabajo)
OUT = Path(os.environ.get("VIBRACIONES_OUT", "out/figs"))

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#fbfcfe",
    "axes.edgecolor": "#2c3e50",
    "axes.labelcolor": "#1a2332",
    "text.color": "#1a2332",
    "xtick.color": "#1a2332",
    "ytick.color": "#1a2332",
    "axes.grid": True,
    "grid.alpha": 0.28,
    "grid.linestyle": "--",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 160,
    "savefig.dpi": 180,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "font.family": "DejaVu Sans",
})

NAVY = "#0b2545"
TEAL = "#0d7377"
GOLD = "#c9a227"
CRIMSON = "#c0392b"
SLATE = "#34495e"
SKY = "#3498db"


def save(fig, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    fig.savefig(path, pad_inches=0.18)
    plt.close(fig)
    print(f"saved {path}")


def fig_shm_damped_driven():
    t = np.linspace(0, 20, 4000)
    omega0 = 2.0 * np.pi * 0.8
    zeta_list = [0.0, 0.08, 0.25, 1.0]
    labels = ["no amortiguado", "subamortiguado", "amortiguado medio", "crítico"]

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 7.4))
    fig.suptitle("Oscilador armónico: libre, amortiguado y forzado", fontweight="bold", color=NAVY)

    ax = axes[0, 0]
    x0, v0 = 1.0, 0.0
    for zeta, lab, c in zip(zeta_list, labels, [NAVY, TEAL, SKY, CRIMSON]):
        wn = omega0
        wd = wn * np.sqrt(max(1 - zeta**2, 0))
        if zeta < 1:
            x = np.exp(-zeta * wn * t) * (x0 * np.cos(wd * t) + ((v0 + zeta * wn * x0) / max(wd, 1e-9)) * np.sin(wd * t))
        else:
            x = (x0 + (v0 + wn * x0) * t) * np.exp(-wn * t)
        ax.plot(t, x, label=lab, color=c, lw=1.6)
    ax.set_title("Respuesta libre (condiciones iniciales fijas)")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("x(t)")
    ax.legend(loc="upper right", framealpha=0.92)

    ax = axes[0, 1]
    zeta = 0.08
    F0, m = 1.0, 1.0
    omegas = np.linspace(0.2 * omega0, 2.2 * omega0, 600)
    amp = (F0 / m) / np.sqrt((omega0**2 - omegas**2) ** 2 + (2 * zeta * omega0 * omegas) ** 2)
    phase = np.arctan2(2 * zeta * omega0 * omegas, omega0**2 - omegas**2)
    ax.plot(omegas / omega0, amp / amp.max(), color=TEAL, lw=2.2, label="amplitud normalizada")
    ax.axvline(1.0, color=GOLD, ls=":", lw=1.4, label="ω = ω₀")
    ax.set_title("Curva de resonancia (ζ = 0.08)")
    ax.set_xlabel("ω / ω₀")
    ax.set_ylabel("A(ω) / A_max")
    ax.legend()

    ax = axes[1, 0]
    omega_drive = omega0
    def rhs(tt, y):
        x, v = y
        return [v, -2 * zeta * omega0 * v - omega0**2 * x + np.cos(omega_drive * tt)]
    sol = solve_ivp(rhs, (0, 25), [0.0, 0.0], t_eval=np.linspace(0, 25, 5000), rtol=1e-7)
    ax.plot(sol.t, sol.y[0], color=NAVY, lw=1.4)
    ax.set_title("Transitorio + régimen permanente (forzado en resonancia)")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("x(t)")

    ax = axes[1, 1]
    ax.plot(omegas / omega0, phase, color=CRIMSON, lw=2.0)
    ax.axhline(np.pi / 2, color=GOLD, ls=":", lw=1.2)
    ax.set_title("Retraso de fase φ(ω)")
    ax.set_xlabel("ω / ω₀")
    ax.set_ylabel("φ (rad)")

    fig.tight_layout()
    save(fig, "01_oscilador_armonico.png")


def fig_fft_spectrogram():
    fs = 2000.0
    t = np.arange(0, 4.0, 1 / fs)
    # chirp + tono + burst
    sig = (
        0.7 * np.sin(2 * np.pi * (40 + 60 * t) * t)
        + 0.45 * np.sin(2 * np.pi * 180 * t)
        + 0.9 * np.sin(2 * np.pi * 320 * t) * (t > 2.2) * np.exp(-(t - 2.2) * 3)
        + 0.08 * np.random.default_rng(7).normal(size=t.size)
    )
    win = windows.hann(t.size)
    spec = np.abs(rfft(sig * win))
    freqs = rfftfreq(t.size, 1 / fs)

    fig, axes = plt.subplots(3, 1, figsize=(11.0, 8.2), gridspec_kw={"height_ratios": [1.1, 1.2, 1.6]})
    fig.suptitle("Análisis espectral: de la serie temporal a la huella vibratoria", fontweight="bold", color=NAVY)

    axes[0].plot(t, sig, color=NAVY, lw=0.7)
    axes[0].set_ylabel("amplitud")
    axes[0].set_title("Señal: chirp + tono 180 Hz + burst 320 Hz + ruido")
    axes[0].set_xlim(0, 4)

    axes[1].semilogy(freqs, spec / spec.max(), color=TEAL, lw=1.3)
    axes[1].set_xlim(0, 500)
    axes[1].set_ylabel("FFT (norm.)")
    axes[1].set_title("Transformada de Fourier (ventana de Hann)")

    f_s, t_s, Sxx = spectrogram(sig, fs=fs, nperseg=256, noverlap=200, window="hann")
    im = axes[2].pcolormesh(t_s, f_s, 10 * np.log10(Sxx + 1e-16), shading="gouraud", cmap="magma")
    axes[2].set_ylim(0, 500)
    axes[2].set_xlabel("t (s)")
    axes[2].set_ylabel("f (Hz)")
    axes[2].set_title("Espectrograma (dB) — evolución temporal de las frecuencias")
    fig.colorbar(im, ax=axes[2], pad=0.02, label="dB")

    fig.tight_layout()
    save(fig, "02_fft_espectrograma.png")


def fig_modes_string():
    L = 1.0
    x = np.linspace(0, L, 400)
    fig, axes = plt.subplots(2, 2, figsize=(11.0, 7.0))
    fig.suptitle("Modos normales de una cuerda fija (condiciones de Dirichlet)", fontweight="bold", color=NAVY)
    for n, ax in enumerate(axes.ravel(), start=1):
        y = np.sin(n * np.pi * x / L)
        ax.fill_between(x, 0, y, color=TEAL, alpha=0.22)
        ax.plot(x, y, color=NAVY, lw=2.0)
        ax.plot(x, -y, color=NAVY, lw=1.0, ls="--", alpha=0.5)
        ax.set_title(f"n = {n}   ·   fₙ = n·f₁")
        ax.set_xlabel("x / L")
        ax.set_ylabel("amplitud")
        ax.set_xlim(0, 1)
        ax.axhline(0, color=SLATE, lw=0.6)
    fig.tight_layout()
    save(fig, "03_modos_cuerda.png")


def fig_phonon_dispersion():
    # Cadena 1D monoatómica y diatómica
    ka = np.linspace(-np.pi, np.pi, 500)
    omega_mono = 2 * np.abs(np.sin(ka / 2))

    # diatómica
    m1, m2 = 1.0, 2.2
    K = 1.0
    mu = 1 / m1 + 1 / m2
    disc = np.sqrt(mu**2 - (4 / (m1 * m2)) * np.sin(ka / 2) ** 2)
    w_ac = np.sqrt(K * (mu - disc))
    w_op = np.sqrt(K * (mu + disc))

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8))
    fig.suptitle("Dispersión fonónica: cadena 1D (modelo de Born–von Karman)", fontweight="bold", color=NAVY)

    ax = axes[0]
    ax.plot(ka / np.pi, omega_mono, color=TEAL, lw=2.4)
    ax.set_title("Red monoatómica  ω(k) = 2√(K/m) |sin(ka/2)|")
    ax.set_xlabel("k a / π")
    ax.set_ylabel("ω / ω_max")
    ax.set_xlim(-1, 1)
    ax.axvline(0, color=SLATE, lw=0.5)

    ax = axes[1]
    ax.plot(ka / np.pi, w_ac / w_op.max(), color=TEAL, lw=2.2, label="rama acústica")
    ax.plot(ka / np.pi, w_op / w_op.max(), color=CRIMSON, lw=2.2, label="rama óptica")
    ax.fill_between(ka / np.pi, w_ac.max() / w_op.max() * np.ones_like(ka),
                    w_op.min() / w_op.max() * np.ones_like(ka), color=GOLD, alpha=0.18, label="gap")
    ax.set_title("Red diatómica: gap entre ramas acústica y óptica")
    ax.set_xlabel("k a / π")
    ax.set_ylabel("ω / ω_max")
    ax.set_xlim(-1, 1)
    ax.legend()

    fig.tight_layout()
    save(fig, "04_dispersion_fononica.png")


def fig_phononic_crystal_1d():
    """Modelo simple de cristal fonónico 1D: transmisión vs frecuencia (método de transferencia)."""
    # N celdas A-B con impedancias distintas
    n_cells = 12
    z1, z2 = 1.0, 4.0
    d1, d2 = 0.5, 0.5
    c1, c2 = 1.0, 0.7
    freqs = np.linspace(0.02, 3.2, 1400)
    T = []
    for f in freqs:
        omega = 2 * np.pi * f
        k1 = omega / c1
        k2 = omega / c2
        # matriz de una interfaz + propagación (simplificado: T-matrix acústica 1D)
        def layer(z, k, d):
            # transfer of pressure/velocity
            return np.array([
                [np.cos(k * d), 1j * z * np.sin(k * d)],
                [1j * np.sin(k * d) / z, np.cos(k * d)],
            ], dtype=complex)
        M = np.eye(2, dtype=complex)
        for _ in range(n_cells):
            M = layer(z2, k2, d2) @ layer(z1, k1, d1) @ M
        # transmisión con carga z0 = z1
        z0 = z1
        A, B = M[0, 0], M[0, 1]
        C, D = M[1, 0], M[1, 1]
        denom = A + B / z0 + C * z0 + D
        t = 2.0 / denom
        T.append(np.abs(t) ** 2)
    T = np.clip(np.array(T).real, 0, 4)

    fig, ax = plt.subplots(figsize=(11.0, 4.6))
    ax.plot(freqs, T, color=NAVY, lw=1.5)
    ax.fill_between(freqs, 0, T, color=TEAL, alpha=0.18)
    ax.set_ylim(0, min(2.2, T.max() * 1.05))
    ax.set_xlim(freqs.min(), freqs.max())
    ax.set_xlabel("frecuencia (u.a.)")
    ax.set_ylabel("|T|²")
    ax.set_title("Cristal fonónico 1D (12 celdas A–B): bandas prohibidas de transmisión", fontweight="bold", color=NAVY)
    fig.tight_layout()
    save(fig, "05_cristal_fononico_T.png")


def fig_2d_membrane_modes():
    """Modos (m,n) de membrana rectangular simplemente apoyada."""
    a, b = 1.0, 0.72
    xs = np.linspace(0, a, 220)
    ys = np.linspace(0, b, 160)
    X, Y = np.meshgrid(xs, ys)
    modes = [(1, 1), (2, 1), (1, 2), (2, 2), (3, 1), (3, 2)]
    fig, axes = plt.subplots(2, 3, figsize=(11.4, 6.8))
    fig.suptitle("Modos de membrana rectangular  ψₘₙ ∝ sin(mπx/a) sin(nπy/b)", fontweight="bold", color=NAVY)
    for ax, (m, n) in zip(axes.ravel(), modes):
        Z = np.sin(m * np.pi * X / a) * np.sin(n * np.pi * Y / b)
        im = ax.imshow(Z, origin="lower", extent=[0, a, 0, b], cmap="RdBu_r", aspect="auto")
        ax.set_title(f"({m},{n})")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, "06_modos_membrana.png")


def fig_qho():
    """Oscilador armónico cuántico: niveles y densidades |ψ_n|²."""
    x = np.linspace(-4.5, 4.5, 800)
    # Hermite via recurrence
    def hermite_psi(n, x):
        # ψ_n = 1/sqrt(2^n n! sqrt(π)) e^{-x^2/2} H_n(x)
        Hnm2 = np.ones_like(x)
        Hnm1 = 2 * x
        if n == 0:
            H = Hnm2
        elif n == 1:
            H = Hnm1
        else:
            H = Hnm1
            for k in range(2, n + 1):
                Hn = 2 * x * Hnm1 - 2 * (k - 1) * Hnm2
                Hnm2, Hnm1 = Hnm1, Hn
            H = Hn
        norm = 1.0 / np.sqrt((2**n) * math.factorial(n) * np.sqrt(np.pi))
        return norm * np.exp(-x**2 / 2) * H

    fig, ax = plt.subplots(figsize=(10.8, 6.4))
    V = 0.5 * x**2
    ax.plot(x, V, color=SLATE, lw=1.6, label="V(x) = ½ mω²x²  (u.a.)")
    colors = ["#0d7377", "#3498db", "#c9a227", "#c0392b", "#8e44ad", "#16a085"]
    for n, c in enumerate(colors):
        psi = hermite_psi(n, x)
        E = n + 0.5
        dens = psi**2
        scale = 0.85 / dens.max()
        ax.fill_between(x, E, E + dens * scale, color=c, alpha=0.35)
        ax.plot(x, E + dens * scale, color=c, lw=1.4, label=fr"n={n}, E=(n+½)ħω")
        ax.axhline(E, color=c, lw=0.5, ls=":")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-0.1, 6.4)
    ax.set_xlabel("x (u.a. del QHO)")
    ax.set_ylabel("energía / ħω")
    ax.set_title("Oscilador armónico cuántico: niveles y densidades de probabilidad", fontweight="bold", color=NAVY)
    ax.legend(loc="upper right", ncol=1, fontsize=8)
    fig.tight_layout()
    save(fig, "07_oscilador_cuantico.png")


def fig_quality_and_bandwidth():
    f0 = 1000.0
    Qs = [5, 15, 50, 200]
    f = np.linspace(600, 1400, 2000)
    fig, ax = plt.subplots(figsize=(10.8, 4.8))
    for Q, c in zip(Qs, [CRIMSON, GOLD, TEAL, NAVY]):
        # Lorentziana de potencia
        P = 1.0 / (1 + Q**2 * ((f / f0) - (f0 / f)) ** 2)
        ax.plot(f, P, lw=2.0, color=c, label=f"Q = {Q}")
    ax.set_xlabel("f (Hz)")
    ax.set_ylabel("potencia normalizada")
    ax.set_title("Factor de calidad Q y ancho de banda: Δf ≈ f₀ / Q", fontweight="bold", color=NAVY)
    ax.legend()
    fig.tight_layout()
    save(fig, "08_factor_calidad.png")


def fig_coupled_oscillators():
    t = np.linspace(0, 30, 4000)
    # dos masas iguales, k y kc
    omega_s = 1.0  # simétrico
    omega_a = 1.35  # antisimétrico
    x1 = np.cos(omega_s * t) + np.cos(omega_a * t)
    x2 = np.cos(omega_s * t) - np.cos(omega_a * t)
    fig, axes = plt.subplots(3, 1, figsize=(11.0, 7.2), sharex=True)
    fig.suptitle("Dos osciladores acoplados: batido y modos simétrico / antisimétrico", fontweight="bold", color=NAVY)
    axes[0].plot(t, x1, color=TEAL, lw=1.3)
    axes[0].set_ylabel("x₁")
    axes[0].set_title("Masa 1")
    axes[1].plot(t, x2, color=CRIMSON, lw=1.3)
    axes[1].set_ylabel("x₂")
    axes[1].set_title("Masa 2")
    axes[2].plot(t, x1 + x2, color=NAVY, lw=1.2, label="x₁+x₂ (modo simétrico)")
    axes[2].plot(t, x1 - x2, color=GOLD, lw=1.2, label="x₁−x₂ (modo antisimétrico)")
    axes[2].legend(loc="upper right")
    axes[2].set_xlabel("t (u.a.)")
    axes[2].set_ylabel("combinaciones")
    fig.tight_layout()
    save(fig, "09_osciladores_acoplados.png")


if __name__ == "__main__":
    np.random.seed(7)
    fig_shm_damped_driven()
    fig_fft_spectrogram()
    fig_modes_string()
    fig_phonon_dispersion()
    fig_phononic_crystal_1d()
    fig_2d_membrane_modes()
    fig_qho()
    fig_quality_and_bandwidth()
    fig_coupled_oscillators()
    print("ALL FIGURES OK")
