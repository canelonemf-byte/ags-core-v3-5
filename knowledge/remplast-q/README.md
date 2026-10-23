# remplast-q

REMPLAST-Q: depuradora de microplásticos (expediente técnico e industrial).

**Autor:** Lázaro López Paz · **Licencia:** MIT (ver `LICENSE`)

## Carpetas de origen en Google Drive

- https://drive.google.com/drive/folders/17yHQXal0pbfUoGJkXsW_SHLdLWi-TVWr
- https://drive.google.com/drive/folders/1WrbYan5iBSshAoZ-bZsmPymxXvk5K8lD

## Archivos incluidos

- `docs/REMPLAST-Q_ANX-Q-001_Quimicos_Custodia.md` ← REMPLAST-Q_ANX-Q-001_Quimicos_Custodia.pdf
- `docs/REMPLAST-Q_ARR-001_Paquete_Arranque.md` ← REMPLAST-Q_ARR-001_Paquete_Arranque.pdf
- `docs/REMPLAST-Q_CONV-EDAR-001_RevA.md` ← REMPLAST-Q_CONV-EDAR-001_RevA.pdf
- `docs/REMPLAST-Q_DOC-000_Indice_Carta_Permisos.md` ← REMPLAST-Q_DOC-000_Indice_Carta_Permisos.pdf
- `docs/REMPLAST-Q_ENV-001_Pack_Envio_GO0.md` ← REMPLAST-Q_ENV-001_Pack_Envio_GO0.pdf
- `docs/REMPLAST-Q_FAT-SAT-001_RevA.md` ← REMPLAST-Q_FAT-SAT-001_RevA.pdf
- `docs/REMPLAST-Q_INTK-001_RevA.md` ← REMPLAST-Q_INTK-001_RevA.pdf
- `docs/REMPLAST-Q_LAY-001_Implantacion.md` ← REMPLAST-Q_LAY-001_Implantacion.pdf
- `docs/REMPLAST-Q_PID-001_RevA.md` ← REMPLAST-Q_PID-001_RevA.pdf
- `docs/REMPLAST-Q_SOP_HAZOP_RevA.md` ← REMPLAST-Q_SOP_HAZOP_RevA.pdf
- `docs/REMPLAST-Q_v2_1_Expediente_Ejecucion.md` ← REMPLAST-Q_v2_1_Expediente_Ejecucion.pdf
- `docs/REMPLAST-Q_v2_Documento_Tecnico_Realizable.md` ← REMPLAST-Q_v2_Documento_Tecnico_Realizable.pdf

## Pendiente: en Drive

Archivos binarios (presentaciones, PDFs grandes, vídeos, imágenes, zips, docx) que no se pudieron pasar a texto. Siguen en Drive:

- Proyecto REMPLAST-Q.mp4 · pendiente: en Drive · https://drive.google.com/file/d/13tRZLs4n1QaOuzyxztkvrNTrchqUF-pE/view?usp=drivesdk
- REMPLAST-Q V2.0 Industrial Reality.pdf · pendiente: en Drive · https://drive.google.com/file/d/1DP10WRoyL0l3ckHg4pI1TpMhdBysEuYq/view?usp=drivesdk
- REMPLAST-Q V2.0 Industrial Reality.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1lUcjqDTYU_ArK8iL-gujIXv9OcnnezTp/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- REMPLAST-Q v2.0 Industrial Twin.pdf · pendiente: en Drive · https://drive.google.com/file/d/1aNKwICRgMiNTOuJU_R-J8tvs_LAgHonp/view?usp=drivesdk
- REMPLAST-Q v2.0 Industrial Twin.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1494sZnKad7_hWXXAktts0inWgybXDuMQ/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- REMPLAST-Q_Carpeta_ID_RevC.zip · pendiente: en Drive · https://drive.google.com/file/d/1h-pdrjCSU_H7t3D9l65Rb1ep-opZWsJk/view?usp=drivesdk
- REMPLAST-Q_V2.0_Industrial_Reality_imagenes.zip · pendiente: en Drive · https://drive.google.com/file/d/19Up0zSnR2lo99gQF9pQueXr_vFzog1yu/view?usp=drivesdk
- REMPLAST-Q_v2.0_Industrial_Twin_imagenes.zip · pendiente: en Drive · https://drive.google.com/file/d/1Vy73byINXXcj1naPyQiPt-sOxXfw5kfS/view?usp=drivesdk

### Subcarpetas no importadas (pendiente: en Drive)

- REMPLAST-Q_Carpeta_ID_RevC · https://drive.google.com/drive/folders/1_7ov1oa1MS06bCE_wzChxtXYfkKuZReT
- REMPLAST-Q_V2.0_Industrial_Reality_imagenes · https://drive.google.com/drive/folders/1VSolDiV3ZnpIQUAREsRynL5oLoQCyfZV
- REMPLAST-Q_v2.0_Industrial_Twin_imagenes · https://drive.google.com/drive/folders/1GUCWrZy2gyZwzc4W_XRk_S07ShUzVp6T

## Excluidos

No se han subido por contener material o nombres de terceros, o datos personales:

- Lázaro LP.json · https://drive.google.com/file/d/15TprbFFXiTH2SIj58gcRHYaseod8yT2_/view?usp=drivesdk

---
Los archivos `.trashed-*`, las copias («- copia») y los duplicados entre carpetas no se han listado.

## Módulo funcional `membrana` (esperando datos)

membrana: dimensionado de la etapa de membrana del expediente REMPLAST-Q v2.1 (Q = 5 m³/h, recuperación 90 %, J = 200 LMH, así que A = 22,5 m²) y flujo por solución-difusión, J = Lp·(ΔP − Δπ).

`pip install -r requirements.txt && python -m pytest -q`. Los datos que faltan están en [DATOS_PENDIENTES.md](DATOS_PENDIENTES.md).
