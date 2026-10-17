# Auditoría 2026-09-23 — Programa Python ordenador cuántico

## Archivos originales (conservados)

| Archivo | Bytes | Hallazgo |
|---|---:|---|
| Canelone.mf Quantum Research.pdf | 25 326 424 | 21 págs 1376×768, sin texto extraíble (raster) |
| Canelone.mf Quantum Research.pptx | 26 988 227 | 21 slides, duplicado Drive (2 file_id) |
| Canelone.mf Research Edition.mp4 | 54 978 884 | vídeo NotebookLM |
| Canelone_mf_Research_Edition_DOCUMENTO_UNICO.pdf | 8 949 | spec v1.8, 3 págs |
| Código Python_ordenador cuántico _software.pdf | 882 179 | dump tar `canelone_mf_publish/` + mojibake, 90 págs |
| Código Python_ordenador cuántico _software (1).pdf | 884 284 | igual + cola bash install |
| Ecosistema de Investigación Cuántica.png | 4 562 740 | infografía v1.8 ES |
| Next-Gen Quantum Prototyping System.png | 5 497 577 | infografía EN |

## Defectos

1. No había `.py` en Drive. El “código” es un tar ustar pegado en Google Docs.
2. Conflicto de versión: `app.py` 1.6 vs documento/PNG 1.8.
3. UTF-8 roto (`programaciÃ³n`).
4. PPTX idéntico duplicado.
5. ⟨Z⟩ opaco (último bit).
6. Ising n>2 incompleto en el dump.
7. GitHub `canelonemf-byte/fusi-n-carpeta-` vacío.
8. DOCUMENTO_UNICO exige un solo `.py`; el pack publish tenía app+tests+docs+CI.

## Entrega nueva

`canelone_mf_v19/` + `llp/proyectos/canelone_mf.json`

No se han modificado binarios originales.
