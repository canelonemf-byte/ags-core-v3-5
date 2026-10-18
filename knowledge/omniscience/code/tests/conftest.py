import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
CODE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE))


import pytest  # noqa: E402


@pytest.fixture
def captured(monkeypatch):
    """Sustituye save() de simular_vibraciones para quedarse con la figura en vez de escribirla."""
    import matplotlib.pyplot as plt
    import simular_vibraciones as sv

    figs = {}

    def fake_save(fig, name):
        figs[name] = fig

    monkeypatch.setattr(sv, "save", fake_save)
    yield sv, figs
    plt.close("all")


@pytest.fixture
def capture(monkeypatch, tmp_path):
    """(ORÁCULO) Ejecuta una función de figura de simular_vibraciones y devuelve la figura."""
    import simular_vibraciones as sv
    figs = {}
    monkeypatch.setattr(sv, "OUT", tmp_path)
    monkeypatch.setattr(sv, "save", lambda fig, name: figs.__setitem__(name, fig))

    def run(fn):
        figs.clear()
        getattr(sv, fn)()
        (name, fig), = figs.items()
        return fig
    return run
