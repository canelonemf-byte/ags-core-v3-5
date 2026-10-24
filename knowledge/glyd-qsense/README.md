# glyd-qsense

Sensor GlyD-QSense: termometría cuántica orgánica.

**Autor:** Lázaro López Paz · **Licencia:** CC BY-NC-ND 4.0 (ver `LICENSE`)

## Carpetas de origen en Google Drive

- https://drive.google.com/drive/folders/1xmJA6__LmOUyqp0d1XSHhCHLotn2WwP3

## Archivos incluidos

- `docs/Dossier_Integral_Plan_Maestro_de_Implementacion_del_Sensor_GlyD-QSense.md` ← Dossier Integral: Plan Maestro de Implementación del Sensor GlyD-QSense
- `docs/Expediente_Tecnico_de_Validacion_Sistema_de_Termometria_Cuantica_Organica_GlyD-QSense.md` ← Expediente Técnico de Validación: Sistema de Termometría Cuántica Orgánica GlyD-QSense
- `docs/Proyecto_GlyD-QSense_Documento_Tecnico_de_Publicacion.md` ← Proyecto GlyD-QSense: Documento Técnico de Publicación
- `docs/proyecto_GlyD-QSense.md` ← proyecto GlyD-QSense,

## Pendiente: en Drive

Archivos binarios (presentaciones, PDFs grandes, vídeos, imágenes, zips, docx) que no se pudieron pasar a texto. Siguen en Drive:

- 1 proyecto.zip · pendiente: en Drive · https://drive.google.com/file/d/18TngB0N-r7b-H4TYJ-bF5uu71tarQ0bH/view?usp=drivesdk
- GlyD-QSense_Organic_Quantum_Precision.pdf · pendiente: en Drive · https://drive.google.com/file/d/1IVwbRw-IRJT1LxvX3Oc3h3retHQv4Aro/view?usp=drivesdk
- GlyD-QSense_Organic_Quantum_Precision.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1jl3S68tFV2_mgJZi4vlpo2x81Sfbi1XO/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- GlyD-QSense_Plan.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1j7QMiZukKeSZk0zFK3iCa9gXiIfU3TKz/view?usp=drivesdk
- GlyD-QSense_Quantum_Thermometry.pdf · pendiente: en Drive · https://drive.google.com/file/d/1XPJkbWNFFz-6Xa_OleTyuiUN4-oNK67d/view?usp=drivesdk
- GlyD-QSense_Quantum_Thermometry.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1BKr5QxY6SLI_m489sKXr30S_eBxIIHcx/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- GlyD-QSense__Sensor_Cuántico.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1GLB6pN1liXB9HqfjJh65voaxXqpD8Rn2/view?usp=drivesdk
- PDF_VIDEO_VIDEO_1.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1Qu5R38NCrop5_Z7sobPPBqYD_uE1MAvn/view?usp=drivesdk
- PDF_VIDEO_VIDEO_2_inglés.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1pxfdDjMDLF5vGx9qf6Gf6nYbdB9G-_RX/view?usp=drivesdk

### Subcarpetas no importadas (pendiente: en Drive)

- 1 proyecto · https://drive.google.com/drive/folders/10rR74mnpRtBNfjAo-GKoTQFfz3BR4njY

## Licencia

Documentación bajo [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/deed.es), como declara el propio dossier. Ver `LICENSE`.

---
Los archivos `.trashed-*`, las copias («- copia») y los duplicados entre carpetas no se han listado.

## Módulo funcional `termometria` (esperando datos)

termometria: termometría Raman. Incluye la temperatura absoluta por cociente anti-Stokes/Stokes, I_AS/I_S = ((ν0+ν)/(ν0−ν))^4 · exp(−hcν/kT) (Rassat y Davis 1994); la calibración lineal de un parámetro espectral frente a T; y las figuras de mérito S_r = |dX/dT|/X y δT = σ_X/|dX/dT| (Brites et al. 2012). La precisión de 0,08 °C del documento solo podrá confirmarse con los espectros reales.

`pip install -r requirements.txt && python -m pytest -q`. Los datos que faltan están en [DATOS_PENDIENTES.md](DATOS_PENDIENTES.md).
