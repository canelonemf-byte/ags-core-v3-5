#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

# Configuración de estilo
sns.set_theme(style='whitegrid', palette='colorblind', font='DejaVu Sans')

def generate_sample_logs(log_path):
    events = []
    base_time = datetime(2026, 11, 1, 10, 0, 0)
    
    # 25 eventos secuenciales
    for i in range(25):
        current_time = base_time + timedelta(seconds=i * 15)
        ts = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Simular comportamiento: entre evento 8 y 15 hay caída de red
        if 8 <= i <= 14:
            evt = "L5_GENAI_FALLBACK"
            st = "WARNING" if i != 12 else "CRITICAL"
            mode = "heuristic_local"
            viability = 0.88 - (0.03 * (i - 7)) if i <= 12 else 0.65
            latency = 1500 + (i * 120)
            det = "Timeout API Gemini / Caída de red. Conmutado a heurística local."
            if viability < 0.70:
                evt = "CRITICAL_VIABILITY_ALERT"
                det += " Alerta de viabilidad celular < 0.70."
        else:
            evt = "TELEMETRY_SYNC"
            st = "OK"
            mode = "genai_cloud"
            viability = 0.95 - (i * 0.002)
            latency = 180 + (i % 3) * 20
            det = "Conexión nominal con Gemini Interactions API."

        record = {
            "ts": ts,
            "evt": evt,
            "node": "GATEWAY_01",
            "st": st,
            "met": {
                "viability": round(viability, 3),
                "latency_ms": latency,
                "mode": mode,
                "active_electrodes": 28 if viability > 0.8 else 18
            },
            "det": det
        }
        events.append(record)
        
    with open(log_path, "w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, separators=(',', ':')) + "\n")
    print(f"Log minificado creado en {log_path} con {len(events)} eventos.")

def parse_and_plot(log_path, output_png):
    timestamps = []
    modes = []
    latencies = []
    viabilities = []
    event_types = []
    
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            dt = datetime.strptime(data["ts"], "%Y-%m-%dT%H:%M:%SZ")
            timestamps.append(dt)
            modes.append(1 if data["met"]["mode"] == "genai_cloud" else 0)
            latencies.append(data["met"]["latency_ms"])
            viabilities.append(data["met"]["viability"])
            event_types.append(data["evt"])

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), sharex=True, gridspec_kw={'height_ratios': [1, 1.2]})
    
    # --- Panel 1: Modo de Conmutación de Red & Latencia ---
    ax1_twin = ax1.twinx()
    
    # Latencia (línea gris)
    ax1_twin.plot(timestamps, latencies, color='#888888', linestyle='--', linewidth=1.5, alpha=0.7, label='Latencia (ms)')
    ax1_twin.set_ylabel('Latencia (ms)', color='#555555', fontsize=10)
    ax1_twin.grid(False)
    
    # Estado del Modo (Cloud vs Local)
    mode_colors = ['#d95f02' if m == 0 else '#2ca02c' for m in modes]
    ax1.scatter(timestamps, modes, color=mode_colors, s=80, zorder=3)
    ax1.plot(timestamps, modes, color='#1f77b4', linewidth=1.8, zorder=2, label='Modo Operativo')
    
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['Heurística Local\n(Fallback)', 'Cloud GenAI\n(Interactions API)'], fontsize=9, fontweight='bold')
    ax1.set_title('Conmutación Automática a Heurística Local Mantiene la Operatividad Ante Caídas de Red y Alertas', 
                  fontsize=13, fontweight='bold', pad=12, loc='left')
    ax1.set_ylabel('Modo L5', fontsize=10)
    
    # Zona sombreada de corte de red
    fallbacks = [i for i, m in enumerate(modes) if m == 0]
    if fallbacks:
        start_idx, end_idx = fallbacks[0], fallbacks[-1]
        ax1.axvspan(timestamps[start_idx], timestamps[end_idx], color='#fee0d2', alpha=0.5, label='Intervalo Caída de Red / Fallback')
        ax2.axvspan(timestamps[start_idx], timestamps[end_idx], color='#fee0d2', alpha=0.5)

    # --- Panel 2: Viabilidad Celular & Alerta Crítica ---
    ax2.plot(timestamps, viabilities, color='#1f77b4', linewidth=2.5, marker='o', markersize=4, label='Viabilidad Celular')
    ax2.axhline(0.70, color='#d95f02', linestyle=':', linewidth=2, label='Umbral Crítico (0.70)')
    
    # Marcar alerta de viabilidad crítica
    critical_indices = [i for i, v in enumerate(viabilities) if v < 0.70]
    for idx in critical_indices:
        ax2.scatter(timestamps[idx], viabilities[idx], color='red', s=130, zorder=4, edgecolor='black')
        ax2.annotate(f'ALERTA CRÍTICA\n({viabilities[idx]})', 
                     xy=(timestamps[idx], viabilities[idx]), 
                     xytext=(timestamps[idx], viabilities[idx] + 0.08),
                     arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                     fontsize=9, fontweight='bold', color='red', ha='center')

    ax2.set_ylabel('Índice de Viabilidad Celular', fontsize=10)
    ax2.set_xlabel('Tiempo de Evento (HH:MM:SS)', fontsize=10)
    ax2.set_ylim(0.5, 1.05)
    
    # Formato del eje X
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=0)
    
    sns.despine(fig=fig)
    plt.tight_layout()
    
    fig.savefig(output_png, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Diagrama temporal generado en {output_png}")

if __name__ == "__main__":
    log_file = "/workspace/scratch/hybrix_events_sample.log"
    chart_file = "/workspace/scratch/diagrama_temporal_conmutaciones.png"
    generate_sample_logs(log_file)
    parse_and_plot(log_file, chart_file)
