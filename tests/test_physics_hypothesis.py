from projects.knowledge import plain  # noqa: F401
from supervisor.checks import claims_in_file


def test_labelled_hypothesis_is_medium_not_hidden():
    f = claims_in_file("README.md", "Hipótesis E0: control del tiempo mediante convergencia tecnológica.")
    k = [x for x in f if x["kind"].startswith("physics")]
    assert k and k[0]["kind"] == "physics_hypothesis" and k[0]["severity"] == "medium"


def test_unlabelled_claim_stays_high():
    f = claims_in_file("README.md", "Conseguimos el control del tiempo con este aparato.")
    assert any(x["kind"] == "physics" and x["severity"] == "high" for x in f)
