#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HYBRIX Capa L3: Módulo de Sensores Cuánticos Q-MATRIX y Modulación NeuroGlyQ.

Implementa la lectura de potenciales de acción neuronales mediante centros
Nitrógeno-Vacante (NV) en nanodiamantes utilizando Resonancia Magnética
Detectada Ópticamente (ODMR) sin contacto invasivo.
"""

import math
import random
import time
import json
from typing import Dict, Any, List, Tuple

class QMatrixNVSensor:
    """
    Simulador de matriz de sensores de centros NV en nanodiamantes (Q-MATRIX).
    Mide los micro-campos magnéticos (nT a uT) producidos por los picos de acción
    sinápticos del cultivo biológico en lugar de electrodos metálicos directos.
    """
    def __init__(self, num_nv_centers: int = 32, center_frequency_ghz: float = 2.87, seed: int = 42):
        self.num_centers = num_nv_centers
        self.f0_ghz = center_frequency_ghz  # Frecuencia de división de campo cero (Zero-Field Splitting)
        self.gyromagnetic_ratio_mhz_per_mt = 28.0  # Gamma del espín electrónico (28 MHz/mT)
        self.rng = random.Random(seed)
        self.baseline_fields = [0.0] * num_nv_centers

    def readout_odmr(self, spiking_activity_rates: List[float]) -> Dict[str, Any]:
        """
        Lee el desplazamiento Zeeman en la frecuencia ODMR para cada centro NV.
        Devuelve la intensidad de campo magnético inducido (en nT) y la fluorescencia PL.
        """
        if len(spiking_activity_rates) != self.num_centers:
            # Rellenar o recortar para ajustar a num_centers
            rates = (spiking_activity_rates + [2.0] * self.num_centers)[:self.num_centers]
        else:
            rates = spiking_activity_rates

        magnetic_fields_nT = []
        odmr_shifts_mhz = []
        fluorescence_pl = []

        for i, rate in enumerate(rates):
            # Campo magnético local acoplado a la tasa de disparo de impulsos (1 Hz ~ 1.5 nT)
            b_field_nT = (rate * 1.8) + self.rng.gauss(0, 0.15)
            magnetic_fields_nT.append(round(b_field_nT, 3))

            # Desplazamiento de frecuencia Zeeman (Δf = gamma * B)
            # 1 nT = 1e-6 mT -> Δf = 28 MHz/mT * 1e-6 mT = 2.8e-5 MHz = 28 Hz
            shift_mhz = (b_field_nT * 1e-6) * self.gyromagnetic_ratio_mhz_per_mt
            odmr_shifts_mhz.append(round(shift_mhz * 1e6, 2))  # en Hz

            # Caída de Fotoluminiscencia (PL) al resonar en la frecuencia Zeeman
            pl_contrast = 1.0 - (0.12 * (rate / (rate + 10.0))) + self.rng.gauss(0, 0.005)
            fluorescence_pl.append(round(max(0.70, min(1.0, pl_contrast)), 4))

        return {
            "timestamp": time.time(),
            "sensor_type": "Q-MATRIX_NV_ODMR",
            "num_centers": self.num_centers,
            "magnetic_fields_nT": magnetic_fields_nT,
            "zeeman_shifts_hz": odmr_shifts_mhz,
            "fluorescence_pl": fluorescence_pl,
            "mean_field_nT": round(sum(magnetic_fields_nT) / self.num_centers, 3)
        }


class NeuroGlyQModulator:
    """
    Módulo de Modulación Acústica/Ultrasonido Focalizado NeuroGlyQ.
    Sustituye la estimulación eléctrica de alta corriente por micro-pulsos
    fonónicos acoplados a microburbujas deuteradas para inducir plasticidad sin daño.
    """
    def __init__(self, max_intensity_mw_cm2: float = 50.0):
        self.max_intensity = max_intensity_mw_cm2  # Límite térmico/mecánico seguro en mW/cm2

    def stimulate_focused_ultrasound(self, target_zones: List[int], intensity_mw: float, duration_ms: float) -> Dict[str, Any]:
        """Aplica estimulación fonónica focalizada sobre las zonas del organoide."""
        if intensity_mw > self.max_intensity:
            return {
                "accepted": False,
                "reason": f"Intensidad {intensity_mw} mW/cm2 excede el límite seguro ({self.max_intensity} mW/cm2)"
            }
        
        if duration_ms > 2000.0:
            return {
                "accepted": False,
                "reason": "Duración de pulso excede los 2000 ms máximos recomendados"
            }

        return {
            "accepted": True,
            "target_zones": target_zones,
            "intensity_mw_cm2": intensity_mw,
            "duration_ms": duration_ms,
            "estimated_viability_impact": -0.00005 * (intensity_mw / 10.0) * (duration_ms / 100.0)  # Daño celular imperceptible (<0.005%)
        }


def test_qmatrix_integration():
    print("--- Probando Módulo Q-MATRIX ODMR y Modulación NeuroGlyQ ---")
    sensor = QMatrixNVSensor(num_nv_centers=32, seed=123)
    modulator = NeuroGlyQModulator(max_intensity_mw_cm2=50.0)

    # Simular lecturas con tasas de disparo reales
    sample_rates = [random.uniform(1.0, 15.0) for _ in range(32)]
    readout = sensor.readout_odmr(sample_rates)
    
    assert len(readout["magnetic_fields_nT"]) == 32
    assert readout["mean_field_nT"] > 0.0
    print(f"[Q-MATRIX] Campo magnético medio detectado: {readout['mean_field_nT']} nT")
    print(f"[Q-MATRIX] Fotoluminiscencia PL media: {sum(readout['fluorescence_pl'])/32:.4f}")

    # Probar estimulación segura NeuroGlyQ
    stim_ok = modulator.stimulate_focused_ultrasound(target_zones=[3, 7, 12], intensity_mw=25.0, duration_ms=150.0)
    assert stim_ok["accepted"] is True
    print(f"[NeuroGlyQ] Estimulación fonónica aceptada: {stim_ok}")

    # Probar estimulación insegura (excesiva)
    stim_fail = modulator.stimulate_focused_ultrasound(target_zones=[1], intensity_mw=100.0, duration_ms=500.0)
    assert stim_fail["accepted"] is False
    print(f"[NeuroGlyQ] Estimulación insegura rechazada correctamente: {stim_fail['reason']}")

    print("¡Pruebas del módulo Q-MATRIX completadas con éxito!\n")

if __name__ == "__main__":
    test_qmatrix_integration()
