from base_agent import BaseAgent
from registry import register

@register
class SearcherAgent(BaseAgent):
    name = "searcher"; domain = "research"
    description = "Rastreo cientifico"
    preferred_model = "perplexity-primary"; fallback_models = ['kimi-primary']
    @property
    def system_prompt(self):
        return "Buscador. Devuelve fuentes identificables y marca lo no verificado."

@register
class SummarizerAgent(BaseAgent):
    name = "summarizer"; domain = "research"
    description = "Sintesis de corpus"
    preferred_model = "kimi-primary"; fallback_models = ['claude-primary']
    @property
    def system_prompt(self):
        return "Sintetizador. Separa datos, hipotesis y conclusiones."

@register
class CriticAgent(BaseAgent):
    name = "critic"; domain = "research"
    description = "Deteccion de gaps"
    preferred_model = "claude-primary"; fallback_models = ['grok-primary']
    @property
    def system_prompt(self):
        return "Critico. Busca sesgos, lagunas y alternativas."

@register
class VerifierAgent(BaseAgent):
    name = "verifier"; domain = "research"
    description = "Validacion de citas"
    preferred_model = "claude-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Verificador. No afirma una cita sin evidencia disponible."

@register
class WriterAgent(BaseAgent):
    name = "writer"; domain = "research"
    description = "Redaccion IMRyD"
    preferred_model = "claude-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Escritor. Distingue evidencia de interpretacion."

