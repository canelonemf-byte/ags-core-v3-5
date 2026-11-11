#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeminiMetaAgent — Capa L5 (Meta-Gobernanza) para HYBRIX.

Supervisa la estigmergia (bus de feromonas), acumula predicciones y pide a
Gemini ajustes de hiperparámetros (p. ej. Beta Ridge) en JSON.

Verificación API (2026-11-09 Europe/Madrid):
- Modelo `gemini-4-argon` existe en models.list(); cuota agotada en la prueba
  en vivo → default gemini-3.5-flash (2026-11-11), sobrescribible con GEMINI_MODEL.
- SDK google-genai 3.0.0: client.interactions.create y interaction.output_text
  confirmados con llamada real a gemini-3.5-flash.
- Fallback: client.models.generate_content si interactions no está disponible.

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA
Licencia: MIT
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections import deque
from typing import Any, Deque, Dict, List, Optional, Protocol

logger = logging.getLogger("hybrix.gemini_meta_agent")

try:
    from google import genai

    GENAI_AVAILABLE = True
except ImportError:  # pragma: no cover - entorno sin SDK
    genai = None  # type: ignore
    GENAI_AVAILABLE = False

# Default: gemini-3.5-flash (respondió en la prueba en vivo del 2026-11-09). gemini-4-argon existe en
# models.list() pero agotó cuota (429); se puede elegir con GEMINI_MODEL=gemini-4-argon.
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash"


class PheroBusProtocol(Protocol):
    def sniff(self, key: str) -> Any: ...
    def deposit(self, key: str, value: Any, ttl_s: float = 300.0) -> None: ...


class BioInterfaceProtocol(Protocol):
    """Reserva para telemetría celular; el agente L5 aún no la consume."""


def _extract_json_text(raw: str) -> str:
    """Extrae el primer objeto/array JSON de un texto (p. ej. con fences markdown)."""
    text = (raw or "").strip()
    if not text:
        return text
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE)
    if fence:
        text = fence.group(1).strip()
    if text.startswith("{") or text.startswith("["):
        return text
    start_obj = text.find("{")
    start_arr = text.find("[")
    starts = [i for i in (start_obj, start_arr) if i >= 0]
    if not starts:
        return text
    start = min(starts)
    return text[start:]


class GeminiMetaAgent:
    """
    Agente de Capa L5 (Meta-Gobernanza) impulsado por Gemini.

    Lee `prediccion_final` del bus de feromonas, acumula hasta 10 ensayos y,
    cada `analysis_interval` ciclos, solicita a Gemini un JSON de ajuste.
    Solo deposita en `gemini_hyperparameters_update` si la respuesta es JSON válido.
    Sin clave API el agente permanece en estado pendiente y no rompe el bucle.
    """

    def __init__(
        self,
        phero_bus: PheroBusProtocol,
        bio_interface: Any = None,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        analysis_interval: int = 50,
        history_maxlen: int = 10,
        deposit_ttl_s: float = 300.0,
    ) -> None:
        self.phero = phero_bus
        self.bio = bio_interface
        self.cycle_count = 0
        self.analysis_interval = max(1, int(analysis_interval))
        self.history_buffer: Deque[Any] = deque(maxlen=max(1, int(history_maxlen)))
        self.deposit_ttl_s = float(deposit_ttl_s)
        self.model_name = (model or os.environ.get("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()
        self.api_key = (api_key if api_key is not None else os.environ.get("GEMINI_API_KEY", "")).strip()
        self.client = None
        self.status = "pending"  # pending | ready | error
        self.last_error: Optional[str] = None
        self._use_interactions = False

        self.system_instruction = (
            "Eres el supervisor cognitivo (Capa L5) de un procesador biológico híbrido (HYBRIX). "
            "Tu objetivo es analizar telemetría celular y ajustar hiperparámetros matemáticos (Beta Ridge). "
            "Responde estrictamente en JSON."
        )

        if not self.api_key:
            self.status = "pending"
            logger.info(
                "[GeminiMetaAgent] Sin GEMINI_API_KEY. Agente funcional en espera (pendiente); "
                "no se invocará a Gemini hasta configurar la clave."
            )
            return

        if not GENAI_AVAILABLE:
            self.status = "pending"
            logger.warning(
                "[GeminiMetaAgent] Paquete google-genai no instalado. "
                "Agente en espera (pendiente). Instala con: pip install google-genai"
            )
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
            self._use_interactions = hasattr(self.client, "interactions") and hasattr(
                getattr(self.client, "interactions", None), "create"
            )
            self.status = "ready"
            logger.info(
                "[GeminiMetaAgent] Cliente listo (modelo=%s, interactions=%s).",
                self.model_name,
                self._use_interactions,
            )
        except Exception as exc:  # pragma: no cover - fallo de init del SDK
            self.client = None
            self.status = "pending"
            self.last_error = f"{type(exc).__name__}: {exc}"
            logger.warning("[GeminiMetaAgent] No se pudo inicializar el cliente: %s", self.last_error)

    def step(self) -> None:
        """Un ciclo de estigmergia: sniff → buffer → análisis periódico."""
        self.cycle_count += 1

        try:
            pred = self.phero.sniff("prediccion_final")
        except Exception as exc:
            logger.warning("[GeminiMetaAgent] Error en sniff: %s", exc)
            pred = None

        if pred is not None:
            self.history_buffer.append(pred)

        if (
            self.cycle_count % self.analysis_interval == 0
            and len(self.history_buffer) == self.history_buffer.maxlen
        ):
            self._cotejar_con_gemini()

    def _cotejar_con_gemini(self) -> None:
        if self.status != "ready" or self.client is None:
            logger.info(
                "[GeminiMetaAgent] Análisis omitido (estado=%s). Sigue pendiente de clave/SDK.",
                self.status,
            )
            return

        payload = json.dumps(list(self.history_buffer), ensure_ascii=False, default=str)
        prompt = (
            f"{self.system_instruction}\n\n"
            f"Datos de telemetría de los últimos {len(self.history_buffer)} ensayos: {payload}"
        )

        logger.info("[GeminiMetaAgent] Iniciando análisis cognitivo con %s...", self.model_name)
        try:
            insight_raw = self._llamar_gemini(prompt)
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            logger.warning("[GeminiMetaAgent] Error en la interfaz cognitiva: %s", self.last_error)
            return

        parsed = self._parse_json_insight(insight_raw)
        if parsed is None:
            logger.warning(
                "[GeminiMetaAgent] Respuesta no es JSON válido; no se deposita. Vista previa: %s",
                repr((insight_raw or "")[:200]),
            )
            return

        try:
            self.phero.deposit("gemini_hyperparameters_update", parsed, ttl_s=self.deposit_ttl_s)
            self.history_buffer.clear()
            logger.info("[GeminiMetaAgent] Directriz JSON depositada en gemini_hyperparameters_update.")
        except Exception as exc:
            self.last_error = f"{type(exc).__name__}: {exc}"
            logger.warning("[GeminiMetaAgent] Fallo al depositar: %s", self.last_error)

    def _llamar_gemini(self, prompt: str) -> str:
        """Preferir Interactions API; si no, generate_content."""
        if self._use_interactions:
            interaction = self.client.interactions.create(
                model=self.model_name,
                input=prompt,
            )
            text = getattr(interaction, "output_text", None)
            if text:
                return str(text).strip()
            return str(interaction).strip()

        # Fallback documentado: generate_content
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        if text:
            return str(text).strip()
        return str(response).strip()

    @staticmethod
    def _parse_json_insight(raw: str) -> Optional[Any]:
        if raw is None:
            return None
        candidate = _extract_json_text(str(raw))
        if not candidate:
            return None
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Intento de recorte al primer objeto balanceado
            try:
                decoder = json.JSONDecoder()
                obj, _ = decoder.raw_decode(candidate)
                return obj
            except (json.JSONDecodeError, ValueError):
                return None


if __name__ == "__main__":
    from hybrix_phero_bus import PheromoneBus

    logging.basicConfig(level=logging.INFO)
    bus = PheromoneBus()
    agent = GeminiMetaAgent(bus, None, analysis_interval=2, history_maxlen=2)
    print("status:", agent.status, "model:", agent.model_name)
    for i in range(4):
        bus.deposit("prediccion_final", {"trial_id": i, "viability": 0.9 - 0.01 * i}, ttl_s=60)
        agent.step()
    print("depositado:", bus.sniff("gemini_hyperparameters_update"))
