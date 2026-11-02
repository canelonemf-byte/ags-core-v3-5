"""
Simulador de Nodo Biológico para HYBRIX API (v1.9.0)
--------------------------------------------------
Este script simula el comportamiento de un nodo biológico con microfluídica y
matriz de electrodos (wetware), generando lecturas continuas de telemetría y
predicciones analíticas asociadas a ensayos biológicos.

Incluye:
  - Generación de dinámicas celulares realistas (viabilidad, electrodos activos).
  - Envío automático de telemetría y predicciones a la API HYBRIX.
  - Detección y manejo de alertas de viabilidad crítica (< 0.70).
  - Búfer local de resiliencia ante cortes de conectividad.
"""

import math
import random
import time
from typing import Dict, Any, List, Optional
import httpx


class BiologicalNodeSimulator:
    def __init__(
        self,
        api_url: str = "http://127.0.0.1:8000",
        api_key: str = "hybrix-secret-key-v190",
        node_id: str = "wetware-node-alpha",
        total_trials: int = 50
    ):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self.node_id = node_id
        self.total_trials = total_trials
        self.headers = {"X-API-Key": self.api_key}
        self.offline_buffer: List[Dict[str, Any]] = []

    def simulate_telemetry(self, trial_id: int) -> Dict[str, Any]:
        """
        Simula la viabilidad celular y el número de electrodos activos.
        Simula un patrón de degradación biológica gradual con ruido fisiológico.
        """
        # Curva de viabilidad: Comienza en ~0.95 y disminuye progresivamente tras el ensayo 30
        decay = 0.0
        if trial_id > 25:
            decay = (trial_id - 25) * 0.015
        
        base_viability = max(0.40, 0.95 - decay)
        noise = random.uniform(-0.03, 0.03)
        viability = round(min(1.0, max(0.0, base_viability + noise)), 4)
        
        # Electrodos activos proporcional al estado celular (máx 32 electrodos)
        active_electrodes = max(4, int(32 * viability + random.randint(-2, 2)))
        active_electrodes = min(32, active_electrodes)

        return {
            "trial_id": trial_id,
            "node_id": self.node_id,
            "viability": viability,
            "active_electrodes": active_electrodes,
        }

    def simulate_prediction(self, trial_id: int, viability: float) -> Dict[str, Any]:
        """
        Genera la predicción analítica del modelo IA acoplado al ensayo biológico.
        La precisión del modelo disminuye si la viabilidad decae por debajo de 0.70.
        """
        label = 1 if (trial_id % 2 == 0) else 0
        
        # Si la viabilidad cae, aumenta la probabilidad de fallo en la predicción
        if viability >= 0.70:
            error_prob = 0.05
        else:
            error_prob = 0.45  # Deriva estadística por degradación celular
            
        prediction = label if (random.random() > error_prob) else (1 - label)
        probability = round(random.uniform(0.80, 0.99) if prediction == label else random.uniform(0.50, 0.69), 4)

        return {
            "trial_id": trial_id,
            "node_id": f"{self.node_id}-ai-core",
            "label": label,
            "prediction": prediction,
            "probability": probability,
        }

    def run_simulation(self):
        print(f"=== INICIANDO SIMULACIÓN DE NODO BIOLÓGICO: {self.node_id} ===")
        print(f"Destino API: {self.api_url}\n")

        with httpx.Client(timeout=5.0) as client:
            for trial_id in range(1, self.total_trials + 1):
                telemetry = self.simulate_telemetry(trial_id)
                prediction = self.simulate_prediction(trial_id, telemetry["viability"])

                print(f"[Ensayo {trial_id:02d}] Telemetría -> Viabilidad: {telemetry['viability']:.2f} | Electrodos: {telemetry['active_electrodes']}/32")

                # Intentar enviar telemetría a la API
                try:
                    res_t = client.post(f"{self.api_url}/api/v1/hybrix/telemetry", json=telemetry, headers=self.headers)
                    if res_t.status_code == 201:
                        data = res_t.json()
                        if "alert" in data:
                            print(f"  ⚠️  [ALERTA DETECTADA]: {data['message']}")
                    else:
                        print(f"  ⚠️ Error en servidor ({res_t.status_code}), almacenando en búfer local...")
                        self.offline_buffer.append(telemetry)
                except Exception as e:
                    print(f"  ❌ Fallo de red ({e.__class__.__name__}), guardando en búfer offline.")
                    self.offline_buffer.append(telemetry)

                # Envío de predicción asociada
                try:
                    client.post(f"{self.api_url}/api/v1/hybrix/predictions", json=prediction, headers=self.headers)
                except Exception:
                    pass

                time.sleep(0.05)  # Pausa entre ensayos

            print(f"\n=== SIMULACIÓN FINALIZADA ===")
            print(f"Total ensayos ejecutados: {self.total_trials}")
            print(f"Registros en búfer offline no transmitidos: {len(self.offline_buffer)}")


if __name__ == "__main__":
    simulator = BiologicalNodeSimulator(total_trials=30)
    simulator.run_simulation()
