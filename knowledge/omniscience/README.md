# C-VIB-001 — paquete de reproducibilidad (OMNISCIENCE) v1.0.1

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España · ORCID 0000-0001-8601-1963  
**Licencias:** MIT (código; ver `LICENSE`) · CC BY 4.0 (documentos del paquete: este README, NOTICE, CITATION.cff)  
Elaborado con asistencia de inteligencia artificial (p. ej. Grok/xAI). **La IA no es autora.** Autor responsable: Lázaro López Paz.

Este README describe el **contenido del zip de código** `c-vib-001-code.zip` (depósito Zenodo 1.0.1). No lista materiales que solo existen en el repositorio completo.

## Contenido de este paquete (zip)

```
c-vib-001/
  CITATION.cff
  LICENSE                 # MIT
  NOTICE
  README.md               # este fichero
  code/
    *.py, run_c_vib_001.sh, requirements.txt, pytest.ini
    checksums_c_vib_001.sha256   # integridad de fuentes del paquete
    gen_rocrate.py → ro-crate-metadata.json (generado al ejecutar)
    README_vibraciones.md
    tests/
```

No incluye: documentos `.tex`, carpeta `docs/`, aplicación web `app/`, campañas C-VIB-00x posteriores, pares LoRA ni salidas `out/figs/` (se regeneran al ejecutar).

## Ejecución y tests

```bash
pip install -r code/requirements.txt   # además: ffmpeg (animación) y fuentes DejaVu (informe PDF)
cd code && python -m pytest -q         # smoke + física
python simular_vibraciones.py          # figuras en ./out/figs  (VIBRACIONES_OUT)
python animar_modos.py                 # MP4 en ./out/figs
./run_c_vib_001.sh                     # venv + figuras + tests + checksums de fuentes + RO-Crate
```

Los tests de física comprueban relaciones que el propio código declara; no validan frente a experimento.  
`omniscience_mv1.py` usa un surrogate aleatorio: su `verified_prediction` no es un resultado físico.  
Dependencias de terceros: `NOTICE`.

Las figuras `out/figs/*` **no** van en el zip: se generan con los scripts anteriores. El fichero `checksums_c_vib_001.sha256` cubre **solo archivos presentes en el zip** (integridad del código). Tras regenerar figuras, puedes archivar tus propios checksums de `out/figs/` localmente.

## En el repositorio completo (no en este zip)

Materiales adicionales en el árbol `knowledge/omniscience/` del repo AGs-Core (p. ej. GitHub `ags-core-v3-5`), **fuera** de `c-vib-001-code.zip`:

- `OMNISCIENCE_Documento_Maestro_2026.tex`, `OMNISCIENCE_maestro.tex`
- `docs/*.md` (publicación, dossier, arquitectura OCR, etc.)
- `app/lib/*.ts`, `app/routes/*.tsx` (web OMNISCIENCE)
- Campañas `C-VIB-002`…, registro de evidencias, pares LoRA

Origen histórico de parte del material: Zenodo 10.5281/zenodo.22150378 (versión 1). DOI de concepto: 10.5281/zenodo.22150377. DOI de la versión 1.0.1: PENDIENTE DE VERIFICACIÓN.

## Excluidos del depósito

No se redistribuyen ficheros con datos personales de autoría en Drive (`Lazaro_Lopez_Paz_autor.json`, etc.) ni el anexo `grok-workspace-2.zip` (espacio de trabajo; permanece en la v1 de Zenodo).
