"""Smoke tests: los scripts se ejecutan y producen los archivos esperados (salida en tmp)."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CODE = Path(__file__).resolve().parents[1]
FIGS = ["01_oscilador_armonico.png", "02_fft_espectrograma.png", "03_modos_cuerda.png",
        "04_dispersion_fononica.png", "05_cristal_fononico_T.png", "06_modos_membrana.png",
        "07_oscilador_cuantico.png", "08_factor_calidad.png", "09_osciladores_acoplados.png"]


def run(script, env_extra, cwd):
    base = {k: v for k, v in os.environ.items()
            if k not in ("VIBRACIONES_OUT", "VIBRACIONES_ROOT", "OMNISCIENCE_DOSSIER_ROOT")}
    env = {**base, "MPLBACKEND": "Agg", **env_extra}
    return subprocess.run([sys.executable, str(CODE / script)], cwd=cwd, env=env,
                          capture_output=True, text=True, timeout=600)


@pytest.mark.smoke
def test_imports_have_no_side_effects(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import importlib
    for m in ["simular_vibraciones", "animar_modos", "omniscience_mv1"]:
        importlib.import_module(m)
    assert list(tmp_path.iterdir()) == []  # importar no crea carpetas ni archivos


@pytest.mark.smoke
def test_default_output_is_relative(tmp_path):
    r = run("simular_vibraciones.py", {}, tmp_path)
    assert r.returncode == 0, r.stderr[-2000:]
    assert "ALL FIGURES OK" in r.stdout
    for name in FIGS:
        p = tmp_path / "out" / "figs" / name
        assert p.is_file() and p.stat().st_size > 10_000, name


@pytest.mark.smoke
def test_report_pdf_builds(tmp_path):
    root = tmp_path / "vib"
    r = run("simular_vibraciones.py", {"VIBRACIONES_OUT": str(root / "figs")}, tmp_path)
    assert r.returncode == 0, r.stderr[-2000:]
    # 11_ y 12_ son imágenes que el código no genera (venían ya hechas en el paquete):
    # se sustituyen por marcadores para probar solo la maquetación.
    from PIL import Image
    for name in ["11_metamaterial_fononico.jpg", "12_qho_artistico.jpg"]:
        Image.new("RGB", (800, 500), "gray").save(root / "figs" / name)
    r = run("crear_informe_pdf.py", {"VIBRACIONES_ROOT": str(root)}, tmp_path)
    assert r.returncode == 0, r.stderr[-2000:]
    pdf = root / "report" / "Analisis_vibraciones_cientificas_Grok.pdf"
    from pypdf import PdfReader
    assert len(PdfReader(str(pdf)).pages) >= 5


@pytest.mark.smoke
@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg no instalado")
def test_animation_short(tmp_path):
    import animar_modos
    out = animar_modos.main(frames=8, out_dir=tmp_path)
    assert out.is_file() and out.stat().st_size > 1000


@pytest.mark.smoke
def test_mv1_campaign_runs():
    import numpy as np
    import omniscience_mv1 as mv1
    s = mv1.CrystalStructure("Si2", np.eye(3) * 5.4, np.zeros((2, 3)), ["Si", "Si"])
    np.random.seed(0)
    res = mv1.OmniscienceMV1Workflow("TEST").run_campaign(s)
    assert res["status"] in {"verified_prediction", "falsified"}


@pytest.mark.smoke
def test_dossier_module_imports():
    # generar_dossier_completo necesita la web original (public/, .grok/): solo se prueba que importa.
    import generar_dossier_completo as g
    assert g.OUT.name == "OMNISCIENCE_dossier_completo.pdf"
