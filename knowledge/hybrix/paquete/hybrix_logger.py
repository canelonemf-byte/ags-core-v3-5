#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HYBRIX System Logger: Sistema de registro en formato JSON minificado 
para almacenar métricas de conmutación de red, eventos de fallback y telemetría biológica.
"""

import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class HybrixMinifiedLogger:
    """
    Logger estructurado de alto rendimiento que emite registros en JSON minificado (1 línea por evento)
    para minimizar consumo de almacenamiento, tokens y latencia I/O.
    """
    def __init__(self, log_file_path: str = "/workspace/scratch/hybrix_events.jsonl"):
        self.log_file_path = log_file_path
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)

    def log_event(self, event_type: str, node_id: str, status: str, metrics: Dict[str, Any], details: str = "") -> Dict[str, Any]:
        """
        Registra un evento codificado en JSON minificado.
        """
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "evt": event_type,
            "node": node_id,
            "st": status,
            "met": metrics,
            "det": details
        }
        # Formateo minificado sin espacios extras
        minified_json = json.dumps(record, separators=(',', ':'))
        
        with open(self.log_file_path, "a", encoding="utf-8") as f:
            f.write(minified_json + "\n")
            
        return record

    def get_recent_events(self, limit: int = 50) -> list:
        """
        Recupera los eventos más recientes del registro persistente.
        """
        if not os.path.exists(self.log_file_path):
            return []
            
        events = []
        with open(self.log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-limit:]:
                if line.strip():
                    events.append(json.loads(line.strip()))
        return events

def run_tests():
    logger = HybrixMinifiedLogger("/workspace/scratch/test_hybrix_events.jsonl")
    
    # Test 1: Registro de evento de conmutación de red (Fallback)
    rec1 = logger.log_event(
        event_type="L5_GENAI_FALLBACK",
        node_id="GATEWAY_01",
        status="WARNING",
        metrics={"viability": 0.88, "latency_ms": 1500, "mode": "heuristic_local"},
        details="Timeout de API Gemini. Conmutado a heurística local."
    )
    assert rec1["evt"] == "L5_GENAI_FALLBACK"
    
    # Test 2: Registro de alerta de viabilidad crítica
    rec2 = logger.log_event(
        event_type="CRITICAL_VIABILITY_ALERT",
        node_id="BIO_CORE_02",
        status="CRITICAL",
        metrics={"viability": 0.64, "active_electrodes": 8, "stim_uA": 20.0},
        details="Viabilidad < 0.70. Exportación CSV y modo conservación activados."
    )
    assert rec2["st"] == "CRITICAL"
    
    # Test 3: Lectura y deserialización
    events = logger.get_recent_events(limit=10)
    assert len(events) == 2
    assert events[0]["node"] == "GATEWAY_01"
    assert events[1]["node"] == "BIO_CORE_02"
    
    print("[OK] Todas las pruebas unitarias de HybrixMinifiedLogger pasaron correctamente.")

if __name__ == "__main__":
    run_tests()
