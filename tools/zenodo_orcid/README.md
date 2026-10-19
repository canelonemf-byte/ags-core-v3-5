# Herramientas Zenodo / ORCID

Scripts y notas para revisar y corregir los metadatos de los registros de Lázaro López Paz en Zenodo (autores, afiliación, ORCID, DOI relacionados). Origen: Drive `NotebookLM_Fuentes_2026-08-30`.

- Token: solo por variable de entorno `export ZENODO_TOKEN='...'` (scope `deposit:write`). Ningún archivo contiene tokens.
- Por defecto los scripts trabajan en modo prueba (dry-run); `--apply` escribe en Zenodo.
- Guía: `INSTRUCCIONES_CORRECCION_METADATOS.md`, `ZENODO_API_README.md`, `ZENODO_INVENTARIO_Y_FALTANTES.md`, `ZENODO_METADATOS_OPTIMIZADOS.md`.
- Scripts: `zenodo_api_client.py`, `zenodo_paginate.py`, `zenodo_update.py`, `zenodo_apply_all.py`, `zenodo_apply_orcid.py`, `zenodo_fix_authors.py`, `zenodo_files.py`, `zenodo_validate.py`, `datacite_validate.py`, `orcid_affiliations.py`, `ejemplo_orcid_doi.py`, `ejemplo_validar_y_corregir.py`, `run_fix.sh`.
- Datos: `zenodo_metadata.json`, `zenodo_validate_config.json`, `zenodo_validate_report.json`, `orcid_afiliaciones.json`, `zenodo_explore_snapshot.json`, `datacite_snapshot.json` (instantáneas de metadatos públicos).

Datos personales retirados: enlaces a perfiles personales (Academia.edu, YouTube) y un correo parcial en `datacite_snapshot.json`.
