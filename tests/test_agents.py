import pytest
from registry import all_agents, get_agent, agents_by_domain
from agents.project_agents import PROJECT_AGENTS
pytestmark = pytest.mark.unit
CORE = 38  # agentes de la v3.5
from agents.subagents import WORKERS
EXPECTED = CORE + len(PROJECT_AGENTS) + len(WORKERS) + 22  # + matriz_el_prat (5+15+actualizar_todo) + gemini_reviewer

def test_registry_count():
    assert len(all_agents()) == EXPECTED

def test_required_fields():
    for name, a in all_agents().items():
        assert a.name == name and a.domain and a.description and a.system_prompt
        assert a.preferred_model and isinstance(a.fallback_models, list)

def test_domains():
    assert len(agents_by_domain("research")) == 5
    assert len(agents_by_domain("compute")) == 5
    assert len(agents_by_domain("domain")) == 6
    assert len(agents_by_domain("multimodal")) == 4
    assert len(agents_by_domain("lab")) == 4
    assert len(agents_by_domain("validation")) == 5  # + gemini_reviewer
    assert len(agents_by_domain("orchestration")) == 3
    assert len(agents_by_domain("tools")) == 6
    assert len(agents_by_domain("local")) == 1

def test_unknown_agent():
    with pytest.raises(KeyError):
        get_agent("nonexistent")
