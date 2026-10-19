# Zenodo — inventario 30 ago 2026 y huecos

Autor en los records: Lázaro López Paz (El Prat de Llobregat).    
No se ha publicado nada nuevo desde esta sesión: hace falta token de la API o subir a mano en https://zenodo.org/uploads.

## Ya publicados (15)

| Fecha | DOI | Título en Zenodo | Qué cubre del portfolio |  
|---|---|---|---|  
| 19 jun | [10.5281/zenodo.20761277](https://doi.org/10.5281/zenodo.20761277) | GlyD-QSense | Termometría orgánica |  
| 23 jun | [10.5281/zenodo.20812704](https://doi.org/10.5281/zenodo.20812704) | Liberación neuroprotectora | Parkinson/Alzheimer PK |  
| 7 jul | [10.5281/zenodo.21238123](https://doi.org/10.5281/zenodo.21238123) | Metamateriales 6G/7G | Fractal / CymaQuantum |  
| 12 jul | [10.5281/zenodo.21321630](https://doi.org/10.5281/zenodo.21321630) | QSM MetaLub | Lubricación articular |  
| 13 jul | [10.5281/zenodo.21345185](https://doi.org/10.5281/zenodo.21345185) | Fotónica fractal | Hardware fractal |  
| 14 jul | [10.5281/zenodo.21361772](https://doi.org/10.5281/zenodo.21361772) | Meta Nano Microbiota | CQDs + gLV (incluye stubs 3–6 KB) |  
| 16 jul | [10.5281/zenodo.21401153](https://doi.org/10.5281/zenodo.21401153) | Lo último en propulsión espacial | **MEI-RIT** |  
| 23 jul | [10.5281/zenodo.21513673](https://doi.org/10.5281/zenodo.21513673) | Software ordenador cuántico | Canelone_mf |  
| 28 jul | [10.5281/zenodo.21640446](https://doi.org/10.5281/zenodo.21640446) | Vida entre las estrellas | LCPB / astrobiología |  
| 31 jul | [10.5281/zenodo.21721963](https://doi.org/10.5281/zenodo.21721963) | Vibración y gravedad | Informe viabilidad + digital twin |  
| 5 ago | [10.5281/zenodo.21806526](https://doi.org/10.5281/zenodo.21806526) | Péptidos v3 | NeuroPlastin / Senolyt-X |  
| 20 ago | [10.5281/zenodo.22028729](https://doi.org/10.5281/zenodo.22028729) | Hibridación IA–biología–QM | FMO-HEOM-IA |  
| 27 ago | [10.5281/zenodo.22131030](https://doi.org/10.5281/zenodo.22131030) | Proyectos helio-3 | **HelioAtlas**, no el 0D QMC-H3 |  
| 27 ago | [10.5281/zenodo.22131440](https://doi.org/10.5281/zenodo.22131440) | Péptidos IA | Solapa con 21806526 |  
| 28 ago | [10.5281/zenodo.22150378](https://doi.org/10.5281/zenodo.22150378) | Vibración / OMNISCIENCE | App + zip de workspace |

## No están como depósito propio

| Proyecto | Por qué falta |  
|---|---|  
| QMC-H3 reactor (0D, Q ≈ 0,04) | HelioAtlas ≠ tokamak. Publicar el maestro **con** la nota de discrepancias |  
| MetaNO Quantum Patch v2 | No hay record con ese nombre |  
| CERO-A (NH₃, CC0) | No hay record |  
| LD-Chip | No hay record |  
| IQM-He3-Anti | No hay record (capa C; opcional) |  
| Libro Blanco sensores NV/OPM/OoC | GlyD no sustituye el blanco CC BY |  
| Atlas + mapa de evidencia | Interno Drive/NotebookLM |  
| Recolección ³He regolito vs viento solar | Dentro de HelioAtlas a lo sumo, no aislado |

Borradores en `/me/uploads` siguen invisibles sin tu sesión.

## Problemas de metadatos (corregir en versiones nuevas)

1. **Creador mal puesto.** En varios records el «creator» es BIST, Peptides International, IN2UB, Fundación Medina, Acoustic Metamaterials Group. Esas entidades no firman el trabajo. El creador debe ser `López Paz, Lázaro` y la afiliación, si acaso, «independiente, El Prat de Llobregat». Poner un instituto ajeno como autor es incorrecto y puede leerse como afiliación falsa.    
2. Títulos con faltas (`Pedtidos`, `Mata materiale`, `dé hoy`, `Alzeimer`).    
3. Microbiota: los PDF de 3–6 KB ya están en Zenodo; no son GMP.    
4. Helio-3 en Zenodo no incluye el código 0D ni Q ≈ 0,04.

## Cómo publicar los que faltan (tú en 10–15 min)

1. Entra en https://zenodo.org/uploads → New upload.    
2. Usa un paquete de la carpeta NotebookLM (Docs 07, 08, 09, DISCREPANCIAS + PDF canónico de Drive).    
3. Creator: **López Paz, Lázaro**.    
4. Tipo: Preprint o Technical note.    
5. Licencia: CC BY 4.0 (CERO-A: CC0, como el ejecutivo).    
6. Descripción: copiar el bloque «Estado / Pregunta / Evidencia / No evidencia» del atlas.    
7. Publish.

Orden recomendado: **QMC-H3 + discrepancias**, **MetaNO**, **CERO-A**, **Libro Blanco sensores**, **LD-Chip**.

API: con un token personal (`deposit:write`) se podría automatizar. Aquí no hay token ni conector Zenodo; no se ha creado ningún record nuevo.  
