import importlib, math, os, sys
from datetime import datetime, timedelta, timezone
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


@pytest.fixture
def store(tmp_path, monkeypatch):
    monkeypatch.setenv("UCS_MEMORY_DB", str(tmp_path / "m.db"))
    import memory_store
    return importlib.reload(memory_store)


def test_same_decay_module(store):
    import memory_decay
    assert store.memory_decay is memory_decay
    assert store.memory_decay.__file__.endswith(os.path.join("ucs", "memory_decay.py"))


@pytest.mark.parametrize("imp,acc,days", [(0.2, 0, 10), (0.6, 0, 45), (0.8, 3, 120), (0.5, 15, 365)])
def test_server_equals_simulation(store, imp, acc, days):
    import memory_decay
    m = store.Mem(1, "s", "f", [], imp, acc,
                  datetime.now(timezone.utc) - timedelta(days=days), False)
    sim = memory_decay.calculate_decay(imp, acc, days)
    assert store.retention(m) == pytest.approx(sim, rel=1e-6)
    tau = 30 * (1 + imp) * (1 + math.log(1 + acc))
    assert sim == pytest.approx(math.exp(-days / tau), rel=1e-12)


def test_pinned(store):
    import memory_decay
    old = datetime.now(timezone.utc) - timedelta(days=9999)
    assert store.retention(store.Mem(1, "s", "f", [], 0.95, 0, old, False)) == 1.0
    assert store.retention(store.Mem(1, "s", "f", [], 0.1, 0, old, True)) == 1.0
    assert memory_decay.FORGET_THRESHOLD == 0.15 and memory_decay.TAU0_DAYS == 30


def test_add_search(store):
    store.add("CERO-A", "amoniaco como vector energetico", ["amoniaco"], 0.6)
    hits = store.search("amoniaco", 5)
    assert hits and hits[0][0].subject == "CERO-A"
    assert store.stats()["total"] == 1
