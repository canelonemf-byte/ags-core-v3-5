# omniscience

OMNISCIENCE: motor de descubrimiento científico (documento maestro).

**Autoría:** Lázaro López Paz (El Prat de Llobregat, Barcelona, España) e inteligencia artificial · ORCID 0000-0001-8601-1963 · **Licencia:** MIT (ver `LICENSE`)

Elaborado con asistencia de inteligencia artificial (herramientas de IA generativa; p. ej. Grok/xAI). Autor responsable: Lázaro López Paz.

## Carpetas de origen en Google Drive

- https://drive.google.com/drive/folders/1DxQUgo0_XeoX73L1YnG-Ffcn81cn8jF8
- https://drive.google.com/drive/folders/1Cpvs6i_hbUle9T4tYwarCuK-_gUAM0z1

## Archivos incluidos

- `OMNISCIENCE_Documento_Maestro_2026.tex` ← OMNISCIENCE_Documento_Maestro_2026.tex
- `OMNISCIENCE_maestro.tex` ← OMNISCIENCE_maestro.tex
- `docs/OMNISCIENCE_Documento_Maestro_2026.md` ← OMNISCIENCE_Documento_Maestro_2026.pdf
- `docs/OMNISCIENCE_PUBLICACION_v1.0.0.md` ← OMNISCIENCE_PUBLICACION_v1.0.0.pdf
- `docs/OMNISCIENCE_Architecture_OCR.md` ← OMNISCIENCE Architecture.pdf (**OCR**, puede contener errores)
- `docs/OMNISCIENCE-MV1-implementacion.md` ← grok-workspace-2.zip: public/docs/OMNISCIENCE-MV1-implementacion.pdf
- `docs/OMNISCIENCE_dossier_completo.md` ← grok-workspace-2.zip: public/docs/OMNISCIENCE_dossier_completo.pdf
- `docs/Analisis_vibraciones_cientificas_Grok.md` ← grok-workspace-2.zip: public/docs/Analisis_vibraciones_cientificas_Grok.pdf
- `code/` (simular_vibraciones.py, animar_modos.py, crear_informe_pdf.py, generar_dossier_completo.py, omniscience_mv1.py, README_vibraciones.md) ← grok-workspace-2.zip: artifacts/omniscience/, artifacts/vibraciones/README.md, public/code/
- `app/lib/*.ts`, `app/routes/*.tsx` ← grok-workspace-2.zip: src/ (código propio de la web OMNISCIENCE; el andamiaje genérico de la plantilla, autenticación y scripts no se ha copiado)

## Código: ejecución y tests

    pip install -r code/requirements.txt      # además: ffmpeg y fuentes DejaVu en el sistema
    cd code && python -m pytest -q             # 14 tests: smoke (-m smoke) y coherencia física (-m physics)
    python simular_vibraciones.py              # figuras en ./out/figs  (VIBRACIONES_OUT para cambiarlo)
    python animar_modos.py                     # MP4 en ./out/figs      (VIBRACIONES_OUT)
    python crear_informe_pdf.py                # PDF en ./out/report    (VIBRACIONES_ROOT; necesita las figuras
                                               #   y 11_metamaterial_fononico.jpg / 12_qho_artistico.jpg, que el código no genera)
    OMNISCIENCE_DOSSIER_ROOT=<web> python generar_dossier_completo.py   # requiere public/ y .grok/ de la web original

Los tests de física solo comprueban relaciones que el propio código declara (fₙ = n·f₁, límites de la
dispersión, |T|² ≤ 1, Δf ≈ f₀/Q, Eₙ = (n+½)ħω); no validan el modelo frente a experimento.
`omniscience_mv1.py` usa un surrogate aleatorio (fuerzas y frecuencias): su `verified_prediction` no es un
resultado físico. Licencias de dependencias en `NOTICE`.

## Origen de grok-workspace-2.zip

Zenodo 10.5281/zenodo.22150378 (172.130.388 bytes, mismo tamaño que la copia de Drive). Desempaquetado en el box en `/workspace/agsgpt/drive_imports/grok-workspace-2/`. `OMNISCIENCE_maestro.tex` del zip es idéntico al ya incluido. `OMNISCIENCE_dossier_front.pdf` está contenido íntegro en el dossier completo y no se ha convertido aparte.

## Pendiente: en Drive

Archivos binarios (presentaciones, PDFs grandes, vídeos, imágenes, zips, docx) que no se pudieron pasar a texto. Siguen en Drive:

- 10_modos_cuerda_animacion.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1Sp8X_ogGgeZnb8t4n0CLdmUVMr99fqNS/view?usp=drivesdk
- OMNISCIENCE Architecture.pdf · importado por OCR en docs/OMNISCIENCE_Architecture_OCR.md · https://drive.google.com/file/d/1TtM3as8l9-RMLuNyJNPsHhtY9k5KDPv9/view?usp=drivesdk
- OMNISCIENCE Architecture.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1BFmmCy6suxCwwNfNUc7To6-JbTAOskqE/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- OMNISCIENCE Discovery Engine.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1miXaMUK9CyhXVEpPCrf96IcD59uXOCi6/view?usp=drivesdk
- OMNISCIENCE Discovery Engine.pdf · pendiente: en Drive · https://drive.google.com/file/d/1BS5-6QzwDp6NQs8VTDqnGnh3WBpD9MaQ/view?usp=drivesdk
- OMNISCIENCE Discovery Engine.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1Vw7cPTekXFzs_COI_9L52r9oQs0Auh-t/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- OMNISCIENCE MV1.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1q16K17W_lvYGCi4HmGNdHsa37f4L5vUm/view?usp=drivesdk
- OMNISCIENCE_maestro_unificado (1).pdf · pendiente: en Drive · https://drive.google.com/file/d/1reh7TSvYvYKm1NJvAUH65wfD5F8xdmOD/view?usp=drivesdk
- grok-workspace-2.zip · importado (ver «Origen de grok-workspace-2.zip») · https://drive.google.com/file/d/1pyACZBxXqzJa_WR_Gc__UyaegijsrTM8/view?usp=drivesdk

### Subcarpetas no importadas (pendiente: en Drive)

- figs · https://drive.google.com/drive/folders/17tWKDUDiaFEBc_IAumtLVJQrq4LKky8n

## Excluidos

No se han subido por contener material o nombres de terceros, o datos personales:

- Lazaro_Lopez_Paz_autor.json · https://drive.google.com/file/d/1KLoDvhZAPho49aDsvsGPlj8saVCmVnvh/view?usp=drivesdk
- Lazaro_Lopez_Paz_citas.json · https://drive.google.com/file/d/1gY_PzUGPHIPmFfKLa4Ns-Rzst3TTlxEb/view?usp=drivesdk

---
Los archivos `.trashed-*`, las copias («- copia») y los duplicados entre carpetas no se han listado.
