"""Genera ro-crate-metadata.json (RO-Crate 1.1) con sha256 de cada fichero. Ejecutar tras run_c_vib_001.sh (o sin salidas).

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, ORCID 0000-0001-8601-1963, con asistencia de IA.
Licencia: MIT. La IA no es autora.
"""
import json, hashlib, os, datetime

base = [
    "simular_vibraciones.py", "animar_modos.py", "verificacion_frecuencias.py",
    "gen_rocrate.py", "run_c_vib_001.sh", "pytest.ini", "requirements.txt",
    "checksums_c_vib_001.sha256", "README_vibraciones.md",
    "crear_informe_pdf.py", "generar_dossier_completo.py", "omniscience_mv1.py",
    "../CITATION.cff", "../LICENSE", "../NOTICE", "../README.md",
    "tests/conftest.py", "tests/test_hipotesis.py", "tests/test_verificacion_frecuencias.py",
    "tests/test_physics.py", "tests/test_smoke.py",
]
figs = []
if os.path.isdir("out/figs"):
    figs = ["out/figs/" + f for f in sorted(os.listdir("out/figs"))]
files = [f for f in sorted(base) + figs if os.path.exists(f)]

MIT, CCBY = "https://opensource.org/licenses/MIT", "https://creativecommons.org/licenses/by/4.0/"
orcid = "https://orcid.org/0000-0001-8601-1963"
g = [
    {"@id": "ro-crate-metadata.json", "@type": "CreativeWork",
     "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}, "about": {"@id": "./"}},
    {"@id": "./", "@type": "Dataset",
     "name": "C-VIB-001: paquete de reproducibilidad (1.0.1)",
     "description": (
         "Simulaciones canónicas de vibraciones 1D (oscilador, FFT, cuerda, fonones, "
         "cristal fonónico, QHO) con tests de H1–H6. Simulación, no experimento. "
         "Licencias: MIT (código) y CC BY 4.0 (documentos y figuras). "
         "Elaborado con asistencia de IA; la IA no es autora."
     ),
     "datePublished": "2026-10-18",
     "author": {"@id": orcid},
     "license": {"@id": CCBY},
     "isBasedOn": {"@id": "https://doi.org/10.5281/zenodo.22150377"},
     "hasPart": [{"@id": f} for f in files],
     "mentions": {"@id": "#run-1"}},
    {"@id": orcid, "@type": "Person",
     "name": "López Paz, Lázaro",
     "affiliation": "El Prat de Llobregat, Barcelona, España",
     "identifier": orcid},
    {"@id": CCBY, "@type": "CreativeWork", "name": "CC BY 4.0 (documentos y figuras)"},
    {"@id": MIT, "@type": "CreativeWork", "name": "MIT (código)"},
    {"@id": "#run-1", "@type": "CreateAction",
     "name": "Ejecución de run_c_vib_001.sh",
     "endTime": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
     "instrument": {"@id": "simular_vibraciones.py"},
     "result": [{"@id": f} for f in files if f.startswith("out/")]},
]
for f in files:
    code = f.endswith(".py") or f.endswith(".sh")
    e = {
        "@id": f,
        "@type": ["File", "SoftwareSourceCode"] if code else "File",
        "sha256": hashlib.sha256(open(f, "rb").read()).hexdigest(),
    }
    if code:
        e["license"] = {"@id": MIT}
    elif f.endswith((".md", ".cff", ".csv", ".json")) or "NOTICE" in f or "LICENSE" in f:
        # documentos / metadatos del paquete
        if f.endswith("LICENSE") or f == "../LICENSE":
            e["license"] = {"@id": MIT}
        else:
            e["license"] = {"@id": CCBY}
    if f.endswith(".py"):
        e["programmingLanguage"] = "Python 3"
    g.append(e)

json.dump(
    {"@context": "https://w3id.org/ro/crate/1.1/context", "@graph": g},
    open("ro-crate-metadata.json", "w", encoding="utf-8"),
    ensure_ascii=False, indent=1,
)
print("ro-crate-metadata.json:", len(files), "ficheros")
