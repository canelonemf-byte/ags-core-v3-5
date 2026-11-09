#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests unitarios de GeminiMetaAgent (sin red).

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA
Licencia: MIT
"""

from __future__ import annotations

import json
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock

from hybrix_phero_bus import PheromoneBus
from gemini_meta_agent import GeminiMetaAgent, _extract_json_text


class FakePheroBus:
    def __init__(self) -> None:
        self.data = {}
        self.deposits = []

    def sniff(self, key: str):
        return self.data.get(key)

    def deposit(self, key: str, value, ttl_s: float = 300.0) -> None:
        self.data[key] = value
        self.deposits.append((key, value, ttl_s))


class TestPheromoneBus(unittest.TestCase):
    def test_deposit_sniff_ttl(self):
        bus = PheromoneBus()
        bus.deposit("prediccion_final", {"ok": 1}, ttl_s=60)
        self.assertEqual(bus.sniff("prediccion_final"), {"ok": 1})
        bus.clear("prediccion_final")
        self.assertIsNone(bus.sniff("prediccion_final"))


class TestGeminiMetaAgent(unittest.TestCase):
    def test_pending_without_api_key(self):
        bus = FakePheroBus()
        agent = GeminiMetaAgent(bus, None, api_key="", analysis_interval=2, history_maxlen=2)
        self.assertEqual(agent.status, "pending")
        for i in range(4):
            bus.data["prediccion_final"] = {"trial_id": i, "viability": 0.9}
            agent.step()
        self.assertEqual(agent.cycle_count, 4)
        self.assertEqual(len(bus.deposits), 0)

    def test_deposits_valid_json_via_interactions(self):
        bus = FakePheroBus()
        agent = GeminiMetaAgent(
            bus,
            None,
            api_key="test-key",
            model="gemini-4-argon",
            analysis_interval=2,
            history_maxlen=2,
        )
        mock_client = MagicMock()
        mock_client.interactions.create.return_value = SimpleNamespace(
            id="int-1",
            output_text='{"beta_ridge": 0.02, "status_diagnosis": "ok"}',
        )
        agent.client = mock_client
        agent.status = "ready"
        agent._use_interactions = True

        for i in range(4):
            bus.data["prediccion_final"] = {"trial_id": i, "viability": 0.91}
            agent.step()

        self.assertTrue(bus.deposits)
        key, value, ttl = bus.deposits[-1]
        self.assertEqual(key, "gemini_hyperparameters_update")
        self.assertEqual(value["beta_ridge"], 0.02)
        self.assertEqual(ttl, 300.0)
        self.assertEqual(len(agent.history_buffer), 0)
        mock_client.interactions.create.assert_called()

    def test_invalid_json_not_deposited(self):
        bus = FakePheroBus()
        agent = GeminiMetaAgent(bus, None, api_key="test-key", analysis_interval=2, history_maxlen=2)
        mock_client = MagicMock()
        mock_client.interactions.create.return_value = SimpleNamespace(
            output_text="esto no es json"
        )
        agent.client = mock_client
        agent.status = "ready"
        agent._use_interactions = True

        for i in range(4):
            bus.data["prediccion_final"] = {"trial_id": i}
            agent.step()

        self.assertEqual(len(bus.deposits), 0)

    def test_generate_content_fallback(self):
        bus = FakePheroBus()
        agent = GeminiMetaAgent(bus, None, api_key="test-key", analysis_interval=1, history_maxlen=1)
        mock_client = MagicMock()
        # Sin interactions
        del mock_client.interactions
        mock_client.models.generate_content.return_value = SimpleNamespace(
            text='```json\n{"beta_ridge": 0.05}\n```'
        )
        agent.client = mock_client
        agent.status = "ready"
        agent._use_interactions = False

        bus.data["prediccion_final"] = {"trial_id": 7, "viability": 0.8}
        agent.step()

        self.assertEqual(bus.deposits[-1][1]["beta_ridge"], 0.05)
        mock_client.models.generate_content.assert_called_once()

    def test_api_error_does_not_break(self):
        bus = FakePheroBus()
        agent = GeminiMetaAgent(bus, None, api_key="test-key", analysis_interval=1, history_maxlen=1)
        mock_client = MagicMock()
        mock_client.interactions.create.side_effect = ConnectionError("red caída")
        agent.client = mock_client
        agent.status = "ready"
        agent._use_interactions = True

        bus.data["prediccion_final"] = {"trial_id": 1}
        agent.step()  # no debe lanzar
        self.assertEqual(len(bus.deposits), 0)
        self.assertIn("ConnectionError", agent.last_error or "")

    def test_extract_json_from_fence(self):
        raw = 'Aquí va:\n```json\n{"a": 1}\n```\nfin'
        self.assertEqual(json.loads(_extract_json_text(raw)), {"a": 1})


if __name__ == "__main__":
    unittest.main()
