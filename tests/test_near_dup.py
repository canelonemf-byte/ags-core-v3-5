import importlib.util, pathlib, pytest
pytestmark = pytest.mark.unit
spec = importlib.util.spec_from_file_location("near_dup", pathlib.Path(__file__).parents[1] / "scripts/near_dup.py")
nd = importlib.util.module_from_spec(spec); spec.loader.exec_module(nd)

def test_norm_and_cosine():
    assert nd.norm("  Hola\n MUNDO ") == "hola mundo"
    p = nd.cosine_pairs(["el gato come pescado azul en la cocina de la casa grande", "el gato come pescado azul en la cocina de la casa grande hoy", "teoría cuántica de campos"], 0.85)
    assert [(i, j) for i, j, _ in p] == [(0, 1)]

def test_leaks_detects_cross_split():
    a = {"split": "train", "file": "t", "line": 1, "id": "x"}; b = {"split": "test", "file": "s", "line": 2, "id": "y"}
    assert len(nd.leaks([], [{"similitud": 0.9, "a": a, "b": b}], [])) == 1
    assert nd.leaks([], [{"similitud": 0.9, "a": a, "b": dict(a, line=3)}], []) == []

def test_regression_b6d4ab22_alias_path_pdf_spacing():
    """Fuga b6d4ab22 (2026-10-21): mismo documento por dos rutas, cabecera distinta y espaciado de PDF roto."""
    tpl = "Convierte la siguiente nota en LLP JSON compacto con claves exactas meta, objetivo. Responde solo con el JSON.\n\nNOTA:\n"
    doc = ("ESTUDIO CONCEPTUAL DE VIABILIDAD · MONOGRAFÍA COMPLETA Arquitectura híbrida multinivel de ultra-bajo consumo. "
           "Límites físicos, estado del arte, diseño de sistema, evaluación reproducible y plan de investigación de principio a fin. ") * 3
    broken = doc.replace("Arquitectura", "Arq uitectura").replace("reproducible", "rep roducible").replace("principio", "p rincip io")
    tr = tpl + "> Texto extraído automáticamente del PDF original «x.docx.pdf». Original en Drive.\n\n" + broken
    te = tpl + "<!-- Fuente: Google Drive, x.docx.pdf. Texto extraído con read_file. -->\n\n" + doc
    mk = lambda s, ins, resp: {"split": s, "file": s, "line": 1, "id": s, "text": nd.norm(ins + " " + resp),
                               "sha": nd.sha(ins + s), "content": nd.content_key(ins)}
    items = [mk("train", tr, '{"meta":{"fuente":"docs/x.docx.md"}}'), mk("test", te, '{"meta":{"fuente":"drive/x.md"}}')]
    lk = nd.leaks([], [], items)
    assert len(lk) == 1 and lk[0]["tipo"] == "contencion" and lk[0]["split"] == "train"
    other = mk("val", tpl + "Teoría de grafos espectrales y particiones balanceadas en redes de sensores. " * 5, "{}")
    assert nd.leaks([], [], [other, items[1]]) == []
