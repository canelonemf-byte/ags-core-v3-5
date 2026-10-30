"""Agente Gemini: segunda opinión / contraste frente a resultados de Grok u otros LLM.
Usa LiteLLM (gemini-2.5-flash → gemini-2.5-pro → grok). Si no hay clave, LiteLLM caído o falla la red,
devuelve estado degradado sin lanzar excepción. No inventa evidencia: marca E0_proveedor.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. MIT."""
from __future__ import annotations

import os
from typing import Any

import httpx

from base_agent import BaseAgent
from config import settings
from registry import register


def _gemini_key_present() -> bool:
    if os.getenv("GEMINI_API_KEY"):
        return True
    path = os.path.expanduser(os.getenv("GEMINI_ENV_FILE", "~/.secrets/gemini.env"))
    try:
        for line in open(path, encoding="utf-8"):
            if line.strip().startswith("GEMINI_API_KEY=") and line.split("=", 1)[1].strip().strip("\"'"):
                return True
    except OSError:
        pass
    return False


@register
class GeminiReviewerAgent(BaseAgent):
    """Segunda opinión con Gemini: contraste afirmaciones, huecos y cifras dudosas."""

    name = "gemini_reviewer"
    domain = "validation"
    description = "Segunda opinión Gemini: contrasta resultados de Grok u otros LLM y marca huecos"
    preferred_model = "gemini"
    fallback_models = ["gemini-3.5-flash", "gemini-primary", "gemini-2.5-flash", "grok"]

    @property
    def system_prompt(self) -> str:
        return (
            "Eres un revisor crítico (segunda opinión). Contrasta el texto o resultado dado: "
            "señala afirmaciones sin fuente, cifras no justificadas, contradicciones y alternativas. "
            "No inventes datos ni bibliografía. Si falta evidencia, dilo y marca PENDIENTE. "
            "Responde en castellano, breve y estructurado (Hallazgos / Huecos / Conclusión)."
        )

    def _prompt(self, task, context):
        base = super()._prompt(task, context)
        if context and context.get("resultado_previo"):
            return (
                f"{base}\n\nRESULTADO PREVIO A CONTRASTAR (p. ej. Grok):\n"
                f"{context['resultado_previo']}\n\n"
                "Devuelve una segunda opinión: qué sostienes, qué cuestionas y qué falta."
            )
        return base

    async def run(self, task: str, context: dict[str, Any] | None = None):
        if os.getenv("AGS_GEMINI_OFF") == "1":
            return self._degraded("desactivado (AGS_GEMINI_OFF=1)", task)
        if not _gemini_key_present() and not os.getenv("LITELLM_ALLOW_NO_KEY"):
            # LiteLLM puede tener la clave en su propio proceso; intentamos igual, pero
            # si ni el proxy responde degradamos con mensaje claro.
            pass
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": self._prompt(task, context or {})},
        ]
        last_error = None
        try:
            async with httpx.AsyncClient(
                base_url=settings.LITELLM_BASE_URL,
                headers={"Authorization": f"Bearer {settings.LITELLM_API_KEY}"},
                timeout=120.0,
            ) as client:
                for model in [self.preferred_model, *self.fallback_models]:
                    try:
                        r = await client.post("/chat/completions", json={"model": model, "messages": messages})
                        r.raise_for_status()
                        data = r.json()
                        return {
                            "agent": self.name,
                            "domain": self.domain,
                            "model_used": model,
                            "output": data["choices"][0]["message"]["content"],
                            "status": "ok",
                            "evidencia": "E0_proveedor",
                            "es_evidencia": False,
                        }
                    except Exception as exc:  # noqa: BLE001
                        last_error = exc
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        return self._degraded(f"{type(last_error).__name__ if last_error else 'sin_respuesta'}", task)

    def _degraded(self, reason: str, task: str) -> dict:
        return {
            "agent": self.name,
            "domain": self.domain,
            "model_used": "",
            "output": (
                f"[gemini_reviewer degradado: {reason}] No hay segunda opinión generativa. "
                f"Revisa manualmente la tarea: {task[:200]}"
            ),
            "status": "degraded",
            "evidencia": "E0_degradado",
            "es_evidencia": False,
        }
