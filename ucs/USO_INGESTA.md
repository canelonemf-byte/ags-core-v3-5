# Uso de doc_chunker.py (UCS) por proyecto

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: CC BY 4.0.

## Requisitos
- API UCS en `http://localhost:8000` (o `API_URL`).
- `AGS_API_KEY` en el entorno (no se imprime ni se guarda en ficheros).

## Ingesta
```bash
python3 ucs/doc_chunker.py <archivo.md|.txt|.tex> "<proyecto> <archivo>" [--importance 0.6] [--dry-run] [--force]
```
- Sujeto: `<proyecto> - Parte N`. Usar el nombre de carpeta de `knowledge/` como prefijo (p. ej. `omniscience`, `oraculo-mesoscopico`, `remplast-q`, `cero-a-amoniaco`, `ordenador-hibrido-no-binario`, `fusi-n-carpeta`, `gravedad`).
- Reingesta: omite lo ya ingerido salvo `--force` (manifiesto `CHUNKER_MANIFEST`).
- Importancia >= 0.95 fija la memoria (no se olvida).
- No ingerir datos simulados como experimento, ni credenciales, ni `knowledge/fusi-n-carpeta/data/` (solo FUSIÓN IA).

## Consulta
- `POST /chat {"message": "...", "top_k": 5}` y `GET /memory/stats` (con `X-API-Key`).
- UI: `http://localhost:8502`.
