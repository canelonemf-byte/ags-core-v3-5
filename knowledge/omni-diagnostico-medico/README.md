# omni-diagnostico-medico

OMNI: proyecto de diagnóstico médico para todos.

**Autor:** Lázaro López Paz · **Licencia:** CC BY-NC-SA 4.0 (ver `LICENSE`)

## Carpetas de origen en Google Drive

- https://drive.google.com/drive/folders/1Sd_45QszLqCMe4ZRvvN3QoL5hjYBMKNf

## Archivos incluidos

- `docs/omni_2_proyecto.md` ← omni_2_proyecto.pdf
- `docs/proyecto_diagnostico_medico_para_todos.md` ← proyecto_diagnóstico_médico_para_todos.pdf
- `gemini-code-1790593049750.txt` ← gemini-code-1790593049750.txt

## Pendiente: en Drive

Archivos binarios (presentaciones, PDFs grandes, vídeos, imágenes, zips, docx) que no se pudieron pasar a texto. Siguen en Drive:


### Subcarpetas no importadas (pendiente: en Drive)

- OMNI_k_llp_elprat-APP · https://drive.google.com/drive/folders/1PFiFoq--z0qFofIXV2FQx2XzAxtrWW5J

## Licencia

Bajo [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es), como declaran los documentos del proyecto. Ver `LICENSE`.

---
Los archivos `.trashed-*`, las copias («- copia») y los duplicados entre carpetas no se han listado.

## Referencias
Ver [REFERENCIAS.md](REFERENCIAS.md).

## Módulo funcional `diagnostico` (esperando datos)

diagnostico: métricas de evaluación de una prueba diagnóstica a partir de la tabla 2×2: sensibilidad, especificidad, valores predictivos según la prevalencia (Bayes), razones de verosimilitud e intervalos de Wilson al 95 % (Altman y Bland 1994).

AVISO MÉDICO: herramienta estadística de investigación. NO diagnostica, NO es un producto sanitario, NO sustituye el juicio clínico y NO está validada clínicamente. Cualquier uso clínico requiere estudios de validación y marcado CE conforme al Reglamento (UE) 2017/745.

`pip install -r requirements.txt && python -m pytest -q`. Los datos que faltan están en [DATOS_PENDIENTES.md](DATOS_PENDIENTES.md).
