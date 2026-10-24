from registry import all_agents
import agents  # noqa: F401


def test_matriz_registrados():
    names = [n for n in all_agents() if n.startswith("matriz_")]
    assert len(names) == 21
    a = all_agents()["matriz_sub_1_3_gestor_rom_secretaria"]
    assert "ciudadanía" in a.system_prompt


def test_matriz_analisis_bice():
    from matriz_el_prat import agentes as MA
    an = {r["id"]: r for r in MA.analizar_propuestas()}
    assert an["PRAT-FIS-002"]["calculo"]["tipo_actual_pct"] == 1.3
