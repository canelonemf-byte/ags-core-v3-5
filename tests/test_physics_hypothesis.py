from projects.knowledge import plain  # noqa: F401
from supervisor.checks import claims_in_file


def test_labelled_hypothesis_is_medium_not_hidden():
    f = claims_in_file("README.md", "Hipótesis E0: control del tiempo mediante convergencia tecnológica.")
    k = [x for x in f if x["kind"].startswith("physics")]
    assert k and k[0]["kind"] == "physics_hypothesis" and k[0]["severity"] == "medium"


def test_unlabelled_claim_stays_high():
    f = claims_in_file("README.md", "Conseguimos el control del tiempo con este aparato.")
    assert any(x["kind"] == "physics" and x["severity"] == "high" for x in f)


def test_free_energy_in_refs_folder_not_flagged():
    """Títulos bibliográficos en refs/ (p. ej. 'Free Energy Calculations') no son afirmaciones."""
    f = claims_in_file(
        "C-VIB-003/refs/xia2020.txt",
        "Accurate Free Energy Calculations of Solids, Phys. Rev. B 101, 184303 (2020).",
    )
    assert not any(x["kind"] == "physics" for x in f)
    f2 = claims_in_file(
        "C-VIB-003/refs/xia2020.txt",
        "Second-Order Structural Phase Transitions, Free Energy and Phonons.",
    )
    assert not any(x["kind"] == "physics" for x in f2)


def test_energia_libre_in_bibliografia_filename_not_flagged():
    f = claims_in_file("bibliografia.md", "Smith et al., Energía libre y termodinámica (2020).")
    assert not any(x["kind"] == "physics" for x in f)


def test_free_energy_claim_outside_refs_still_flagged():
    f = claims_in_file("docs/paper.md", "Hemos conseguido free energy ilimitada para todos.")
    assert any(x["kind"] == "physics" and x["severity"] == "high" for x in f)
    f2 = claims_in_file("README.md", "Hemos conseguido energía libre infinita para todos.")
    assert any(x["kind"] == "physics" and x["severity"] == "high" for x in f2)
