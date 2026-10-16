from base_agent import BaseAgent
from registry import register

@register
class ImageAgent(BaseAgent):
    name = "image"; domain = "multimodal"
    description = "Imagenes cientificas"
    preferred_model = "gemini-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Imagen. Segmentacion como analisis, no medida nueva."

@register
class SpectraAgent(BaseAgent):
    name = "spectra"; domain = "multimodal"
    description = "Espectros"
    preferred_model = "claude-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Espectros. Interpretacion con controles."

@register
class AudioAgent(BaseAgent):
    name = "audio"; domain = "multimodal"
    description = "Audio cientifico"
    preferred_model = "gemini-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Audio. Clasificacion."

@register
class VideoAgent(BaseAgent):
    name = "video"; domain = "multimodal"
    description = "Video cientifico"
    preferred_model = "gemini-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Video. Tracking."

