# logarithmus-biologicus-quanticus

Logarithmus Biologicus Quanticus / índice LCPB: algoritmo cuántico para evaluar el potencial biológico de exoplanetas.

**Autor:** Lázaro López Paz · **Licencia:** MIT (ver `LICENSE`)

## Carpetas de origen en Google Drive

- https://drive.google.com/drive/folders/1Q3D3JFYQdr9x380h0cTB6hBlbHJ9YnSu
- https://drive.google.com/drive/folders/1cwzY4KhEQrjgS6i5q8G09CyY2HC1N4rq
- https://drive.google.com/drive/folders/1IALl7u5DTVYdcAmnu7W-4-pqM-_dfmqC

## Archivos incluidos

- `codigo_Python__Research_Edition.py.txt` ← código Python _Research_Edition.py.txt
- `docs/Logarithmus_Biologicus_Quanticus_v2.0.md` ← Logarithmus_Biologicus_Quanticus_v2.0.pdf
- `lcpb_final_completo.py` ← lcpb_final_completo.py

## Pendiente: en Drive

Archivos binarios (presentaciones, PDFs grandes, vídeos, imágenes, zips, docx) que no se pudieron pasar a texto. Siguen en Drive:

- Código Python_ordenador cuántico _software.pdf · pendiente: en Drive · https://drive.google.com/file/d/1bghPoDGKSIk62cmmoj0w8rpZqTpLo3Zk/view?usp=drivesdk
- El_Futuro_de_la_Astrobiología.png · pendiente: en Drive · https://drive.google.com/file/d/1JcPH06v7-oGhHx6z5gfYBOi08UpVVFbK/view?usp=drivesdk
- Evolución_del_Índice_Biológico_Cuántico.png · pendiente: en Drive · https://drive.google.com/file/d/1VoWuvhc9Fnnv4xQWUn9C1HM3EiKgp5PH/view?usp=drivesdk
- Identificar_exoplanetas_habitables_con_computación_cuántica.m4a · pendiente: en Drive · https://drive.google.com/file/d/1wsI1HAK7dqtv0Hu0KISs-l10JKUofvFW/view?usp=drivesdk
- LCPB_Quantum_Astrobiology.pdf · pendiente: en Drive · https://drive.google.com/file/d/1IOXundRwKqYdbq4orA0YjPUUCdn2oVPq/view?usp=drivesdk
- LCPB_Quantum_Astrobiology.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/19Ud6rJBcqZbeLLfIshsrjiyy2sj3zwgx/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- LCPB_Quantum_Framework.pdf · pendiente: en Drive · https://drive.google.com/file/d/1bXMoJLk1r55WLF9ge60qKtdtk7kujbfA/view?usp=drivesdk
- LCPB_Quantum_Framework.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1g0ZgH6w_reD3X92dOq8QuLhxzeMj2OZn/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- LCPB__Quantum_Astrobiology.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1wEJTW4vYDhXbAyJ6dNgWnNS-EHCjL_UN/view?usp=drivesdk
- Quantum_Biological_Potential_Index.pdf · pendiente: en Drive · https://drive.google.com/file/d/1NFwx_jaNS9APx6hA-i-Yu90kpZ-yUOdh/view?usp=drivesdk
- Quantum_Biological_Potential_Index.pptx · pendiente: en Drive · https://docs.google.com/presentation/d/1xl9gZMhTKklDCdKIE4IIJK734W8Aj92N/edit?usp=drivesdk&ouid=104725215047766891127&rtpof=true&sd=true
- Quantum_Scale_for_Alien_Life.png · pendiente: en Drive · https://drive.google.com/file/d/1X5DerRLgfStogQUYeD8uk7Rwz5uDN36l/view?usp=drivesdk
- files.zip · pendiente: en Drive · https://drive.google.com/file/d/1Lr89At3YKMHFvpbWyOlhk6IbQ9s4L1_W/view?usp=drivesdk
- Índice_LCPB_Cuántico(1).mp4 · pendiente: en Drive · https://drive.google.com/file/d/1tRSGndq6CBjOocatU1Pf8vkyeuqNr7hc/view?usp=drivesdk
- Índice_LCPB_Cuántico.mp4 · pendiente: en Drive · https://drive.google.com/file/d/1pc95fJOCqwAjLOYSq07ZwiGiR5_PxQsg/view?usp=drivesdk

### Subcarpetas no importadas (pendiente: en Drive)

- files · https://drive.google.com/drive/folders/1PWMb6FRhABhjtGR6e95SDNUq7FbCUDv4
- files · https://drive.google.com/drive/folders/1lyqgc8SRgjQQj6zqB9FLbYUgfBv79nLN
- LCPB Quantum Astrobiology · https://drive.google.com/drive/folders/1HijLDRVBWn7Zk3BXnNifPDoe6kbjKGjH
- files · https://drive.google.com/drive/folders/1UYslXRy40qTLc0XcEj2Bvr7yLhb6qiJU

---
Los archivos `.trashed-*`, las copias («- copia») y los duplicados entre carpetas no se han listado.

## Código ejecutable (lcpb)

`pip install -r requirements.txt && python -m pytest -q`

**Hallazgo:** en el código original, γ hace que Λ_final = Λ_MCMC para todos los planetas, así que los datos del planeta se cancelan. lcpb usa γ=0 y el test lo demuestra. Índice exploratorio (E0/E1).

> **Aviso:** la tabla LCPB v2.0 del documento no es válida, porque Λ es igual para todos los planetas. Ver [AVISO_TABLA_V2.md](AVISO_TABLA_V2.md).
