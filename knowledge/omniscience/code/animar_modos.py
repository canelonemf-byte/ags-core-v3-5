#!/usr/bin/env python3
"""Animación de modos de cuerda + superposición (video MP4)."""
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Carpeta de salida configurable (antes fija en /home/workdir/artifacts/vibraciones/figs).
# VIBRACIONES_OUT=<dir>  (por defecto ./out/figs)
OUT = Path(os.environ.get("VIBRACIONES_OUT", "out/figs"))

L = 1.0
x = np.linspace(0, L, 400)
# coeficientes de una pulso inicial (serie de Fourier de un triángulo)
Ns = [1, 2, 3, 4, 5]
cs = [0.70, 0.00, 0.18, 0.00, 0.07]
omega1 = 2 * np.pi  # f1 = 1 Hz en unidades reducidas

def y_mode(n, t):
    return cs[n - 1] * np.sin(n * np.pi * x / L) * np.cos(n * omega1 * t)


def main(frames: int = 240, out_dir=None):
    out_dir = OUT if out_dir is None else out_dir
    fig, axes = plt.subplots(2, 1, figsize=(10.4, 6.2), gridspec_kw={"height_ratios": [1.15, 1]})
    fig.patch.set_facecolor("white")
    for ax in axes:
        ax.set_xlim(0, L)
        ax.set_ylim(-1.25, 1.25)
        ax.set_facecolor("#f7fafc")
        ax.grid(True, ls="--", alpha=0.3)

    axes[0].set_title("Modos n = 1…5 (fases independientes)", fontsize=12, color="#0b2545", fontweight="bold")
    axes[1].set_title("Superposición (pulso que viaja y se refleja)", fontsize=12, color="#0b2545", fontweight="bold")
    axes[1].set_xlabel("x / L")

    colors = ["#0d7377", "#3498db", "#c9a227", "#c0392b", "#8e44ad"]
    lines_modes = []
    for n, c in zip(Ns, colors):
        (ln,) = axes[0].plot([], [], color=c, lw=1.6, label=f"n={n}")
        lines_modes.append(ln)
    axes[0].legend(loc="upper right", ncol=5, fontsize=8)
    (line_sum,) = axes[1].plot([], [], color="#0b2545", lw=2.2)
    fill = None

    def init():
        for ln in lines_modes:
            ln.set_data([], [])
        line_sum.set_data([], [])
        return [*lines_modes, line_sum]

    def update(frame):
        t = frame / 40.0  # 40 fps → 1 s de animación = 1 s físico
        ys = []
        for i, n in enumerate(Ns):
            yn = np.sin(n * np.pi * x / L) * np.cos(n * omega1 * t)
            lines_modes[i].set_data(x, 0.85 * yn)
            ys.append(cs[n - 1] * yn)
        ytot = np.sum(ys, axis=0)
        line_sum.set_data(x, ytot)
        return [*lines_modes, line_sum]

    anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=25)
    writer = FFMpegWriter(fps=40, bitrate=2800, extra_args=["-pix_fmt", "yuv420p"])
    out = Path(out_dir) / "10_modos_cuerda_animacion.mp4"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    anim.save(str(out), writer=writer)
    plt.close()
    print("saved", out)
    return out


if __name__ == "__main__":
    main()
