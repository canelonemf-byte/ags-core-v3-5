import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "/workspace/skill_scripts/data-craft")
import house
from house import theme, color as C

def generate_qmatrix_chart():
    theme.apply("report")
    
    # Datos simulados de 32 sensores NV de Q-MATRIX
    np.random.seed(42)
    channels = np.arange(1, 33)
    spike_rates_hz = np.random.uniform(2.0, 18.0, 32)
    spike_rates_hz[3] = 28.5  # Canal 4 pico
    spike_rates_hz[12] = 24.1 # Canal 13 pico
    spike_rates_hz[21] = 22.0 # Canal 22 pico

    magnetic_fields_nT = spike_rates_hz * 1.8 + np.random.normal(0, 0.2, 32)
    pl_fluorescence = 1.0 - (0.15 * (spike_rates_hz / (spike_rates_hz + 10.0)))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7.5), sharex=True)

    accent_color = "#d55e00"  # Vermillion Okabe-Ito

    # Gráfico 1: Campo Magnético Local (nT) por Canal NV
    bars = ax1.bar(channels, magnetic_fields_nT, color=C.OKABE_ITO[0], alpha=0.85, width=0.6, label="Campo Magnético (nT)")
    ax1.axhline(np.mean(magnetic_fields_nT), color=accent_color, linestyle="--", linewidth=1.5, label=f"Media: {np.mean(magnetic_fields_nT):.1f} nT")
    ax1.set_ylabel("Campo (nT)", fontsize=11, fontweight="bold")
    ax1.set_ylim(0, 68)
    ax1.legend(loc="upper right", frameon=False)
    theme.declutter(ax1)

    # Destacar picos
    for idx in [3, 12, 21]:
        bars[idx].set_color(accent_color)
        ax1.annotate(f"{magnetic_fields_nT[idx]:.1f} nT",
                     xy=(channels[idx], magnetic_fields_nT[idx]),
                     xytext=(channels[idx], magnetic_fields_nT[idx] + 5),
                     ha="center", fontsize=9, fontweight="bold", color=accent_color,
                     arrowprops=dict(arrowstyle="->", color=accent_color, lw=1))

    # Gráfico 2: Contraste de Fotoluminiscencia ODMR (PL)
    ax2.plot(channels, pl_fluorescence, marker="o", color=C.OKABE_ITO[2], linewidth=2, label="Fotoluminiscencia (PL)")
    ax2.set_ylabel("PL Relativa", fontsize=11, fontweight="bold")
    ax2.set_xlabel("Canal / Centro NV Nanodiamante (1 - 32)", fontsize=11, fontweight="bold")
    ax2.set_ylim(0.80, 1.02)
    ax2.legend(loc="lower right", frameon=False)
    theme.declutter(ax2)

    theme.title(ax1, "Lectura Cuántica Q-MATRIX: Campos Magnéticos en Nanodiamantes NV",
                "Sensado no invasivo de potenciales de acción neuronales mediante espectroscopía ODMR (32 canales)")
    theme.source(ax2, "Fuente: Arquitectura HYBRIX Capa L3 — Q-MATRIX NV Center Sensing Protocol")

    output_path = "/workspace/scratch/qmatrix_odmr_spectrum.png"
    house.save(fig, output_path)
    print(f"Grafico Q-MATRIX guardado en {output_path}")

if __name__ == "__main__":
    generate_qmatrix_chart()
