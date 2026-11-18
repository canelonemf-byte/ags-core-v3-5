#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suite de Pruebas Unitarias de Resiliencia y Fallback de Red para L5 GenAIMetaAgent.
Verifica que el agente conmute de forma transparente al modo heurístico local
cuando falla la red o la API de Gemini.
"""

import sys
import os
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

# Asegurar importación desde el paquete local HYBRIX
sys.path.insert(0, str(Path(__file__).resolve().parent))
from hybrix_genai_l5 import GenAIMetaAgent


class TestGenAIMetaAgentFallback(unittest.TestCase):

    def test_no_api_key_fallback(self):
        """Verifica que sin API Key el agente use inmediatamente el modo heurístico local."""
        agent = GenAIMetaAgent(api_key="")
        telemetry = [{"trial_id": 1, "viability": 0.92, "active_electrodes": 16}]
        res = agent.analyze_and_optimize(telemetry)
        
        self.assertTrue(res.get("fallback_heuristic"))
        self.assertIn("Sin API Key", res.get("reason", ""))
        self.assertEqual(res["stimulation_amplitude_uA"], 50.0)

    def test_network_failure_exception_fallback(self):
        """
        Verifica que ante una excepción de red (ConnectionError, Timeout, etc.)
        durante client.interactions.create, se capture la excepción y se retorne la heurística local.
        """
        agent = GenAIMetaAgent(api_key="test-api-key")
        # Inyectar cliente Mock que lanza ConnectionError al invocar interactions.create
        mock_client = MagicMock()
        mock_client.interactions.create.side_effect = ConnectionError("Fallo de conexión con el servidor Gemini (Simulado)")
        agent.client = mock_client
        
        telemetry = [{"trial_id": 2, "viability": 0.88, "active_electrodes": 20}]
        res = agent.analyze_and_optimize(telemetry)
        
        # Debe haber conmutado a heurística local
        self.assertTrue(res.get("fallback_heuristic"))
        self.assertIn("ConnectionError", res.get("reason", ""))
        self.assertEqual(res["lr"], 0.02)
        self.assertEqual(res["stimulation_amplitude_uA"], 50.0)

    def test_critical_viability_during_network_outage(self):
        """
        Verifica que si ocurre una caída de red MIENTRAS el cultivo tiene viabilidad crítica (< 0.70),
        la heurística local aplique inmediatamente los parámetros de protección celular (20 uA, lr 0.001).
        """
        agent = GenAIMetaAgent(api_key="test-api-key")
        mock_client = MagicMock()
        mock_client.interactions.create.side_effect = TimeoutError("Timeout en la red LoRa/Internet")
        agent.client = mock_client
        
        telemetry = [{"trial_id": 3, "viability": 0.62, "active_electrodes": 8}]
        res = agent.analyze_and_optimize(telemetry)
        
        self.assertTrue(res.get("fallback_heuristic"))
        self.assertEqual(res["stimulation_amplitude_uA"], 20.0)
        self.assertEqual(res["lr"], 0.001)
        self.assertIn("ALERTA LOCAL", res["status_diagnosis"])

    def test_successful_api_interaction(self):
        """Verifica el comportamiento normal cuando la API de Gemini responde exitosamente."""
        agent = GenAIMetaAgent(api_key="test-api-key")
        mock_client = MagicMock()
        mock_interaction = MagicMock()
        mock_interaction.id = "int-123456"
        mock_interaction.output_text = "Optimización completada por Gemini 2.5 Flash."
        mock_client.interactions.create.return_value = mock_interaction
        agent.client = mock_client
        
        telemetry = [{"trial_id": 4, "viability": 0.96, "active_electrodes": 32}]
        res = agent.analyze_and_optimize(telemetry)
        
        self.assertFalse(res.get("fallback_heuristic"))
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["interaction_id"], "int-123456")
        self.assertEqual(agent.previous_interaction_id, "int-123456")


if __name__ == "__main__":
    unittest.main()
