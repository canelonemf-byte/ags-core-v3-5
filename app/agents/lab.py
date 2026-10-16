from base_agent import BaseAgent
from registry import register

@register
class ExperimentalDesignAgent(BaseAgent):
    name = "experimental_design"; domain = "lab"
    description = "Diseno experimental"
    preferred_model = "claude-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Diseno. Controles y potencia, no ejecucion."

@register
class RoboticOperatorAgent(BaseAgent):
    name = "robotic_operator"; domain = "lab"
    description = "Operacion robotica"
    preferred_model = "gpt-primary"; fallback_models = ['claude-primary']
    @property
    def system_prompt(self):
        return "Planes roboticos verificables, no actuacion."

@register
class ExperimentOptimizerAgent(BaseAgent):
    name = "experiment_optimizer"; domain = "lab"
    description = "Optimizacion experimental"
    preferred_model = "gpt-primary"; fallback_models = ['grok-primary']
    @property
    def system_prompt(self):
        return "Criterios de parada, no resultado de laboratorio."

@register
class ProtocolSimulatorAgent(BaseAgent):
    name = "protocol_simulator"; domain = "lab"
    description = "Simulacion de protocolos"
    preferred_model = "claude-primary"; fallback_models = ['gpt-primary']
    @property
    def system_prompt(self):
        return "Simulacion no es experimento."

