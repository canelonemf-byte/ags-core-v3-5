"""Tests del registro de pruebas (MIT). Autoría: Lázaro López Paz con asistencia de IA."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import registro_pruebas as R

def _fila(**k):
    f = dict(fecha="2026-11-11T00:00:00+01:00", zona="Europe/Madrid", funcion="f", parametros_json={"b": 2, "a": 1},
             semilla="7", resultado="x", tipo="software", evidencia="E3_software")
    f.update(k); return f

def test_dedup_y_consulta(tmp_path):
    db = tmp_path / "p.db"
    assert R.consultar_antes_de_correr("f", {"a": 1, "b": 2}, 7, db) is None
    assert R.registrar(_fila(), db) is True
    assert R.registrar(_fila(resultado="y"), db) is False
    assert R.consultar_antes_de_correr("f", '{"b":2,"a":1}', "7", db)["resultado"] == "x"

def test_tipo_invalido(tmp_path):
    with pytest.raises(ValueError):
        R.registrar(_fila(tipo="real"), tmp_path / "p.db")

def test_e4_rechazado(tmp_path):
    with pytest.raises(ValueError):
        R.registrar(_fila(evidencia="E4_experimento"), tmp_path / "p.db")
