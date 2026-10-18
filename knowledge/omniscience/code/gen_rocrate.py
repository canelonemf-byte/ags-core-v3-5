"""Genera ro-crate-metadata.json (RO-Crate 1.1) con sha256 de cada fichero. Ejecutar tras run.sh."""
import json, hashlib, os, datetime
files = sorted(["simular_vibraciones.py", "animar_modos.py", "verificacion_frecuencias.py", "gen_rocrate.py", "run_c_vib_001.sh", "pytest.ini",
                "requirements.txt", "checksums_c_vib_001.sha256", "README_vibraciones.md", "../CITATION.cff", "../LICENSE",
                "tests/conftest.py", "tests/test_hipotesis.py", "tests/test_verificacion_frecuencias.py", "tests/test_physics.py", "tests/test_smoke.py"]
               + ["out/figs/" + f for f in sorted(os.listdir("out/figs"))])
files = [f for f in files if os.path.exists(f)]
MIT, CCBY = "https://opensource.org/licenses/MIT", "https://creativecommons.org/licenses/by/4.0/"
g = [{"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}, "about": {"@id": "./"}},
     {"@id": "./", "@type": "Dataset", "name": "C-VIB-001: paquete de reproducibilidad (borrador)",
      "description": "Simulaciones canónicas de vibraciones 1D (oscilador, FFT, cuerda, fonones, cristal fonónico, QHO) con tests de H1–H6. Simulación, no experimento. Licencias: PROPUESTA pendiente del autor.",
      "datePublished": "2026-10-18", "author": {"@id": "#lopez-paz-lazaro"}, "license": {"@id": CCBY},
      "isBasedOn": {"@id": "https://doi.org/10.5281/zenodo.22150378"}, "hasPart": [{"@id": f} for f in files], "mentions": {"@id": "#run-1"}},
     {"@id": "#lopez-paz-lazaro", "@type": "Person", "name": "López Paz, Lázaro", "affiliation": "Investigador independiente, El Prat de Llobregat, Barcelona, España"},
     {"@id": CCBY, "@type": "CreativeWork", "name": "CC-BY-4.0 (propuesta: documentos y figuras)"},
     {"@id": MIT, "@type": "CreativeWork", "name": "MIT (propuesta: código)"},
     {"@id": "#run-1", "@type": "CreateAction", "name": "Ejecución de run.sh", "endTime": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
      "instrument": {"@id": "simular_vibraciones.py"}, "result": [{"@id": f} for f in files if f.startswith("out/")]}]
for f in files:
    code = f.endswith(".py") or f in ("run.sh", "Makefile")
    e = {"@id": f, "@type": ["File", "SoftwareSourceCode"] if code else "File", "sha256": hashlib.sha256(open(f, "rb").read()).hexdigest()}
    if code: e["license"] = {"@id": MIT}
    if f.endswith(".py"): e["programmingLanguage"] = "Python 3.13"
    g.append(e)
json.dump({"@context": "https://w3id.org/ro/crate/1.1/context", "@graph": g}, open("ro-crate-metadata.json", "w"), ensure_ascii=False, indent=1)
print("ro-crate-metadata.json:", len(files), "ficheros")
