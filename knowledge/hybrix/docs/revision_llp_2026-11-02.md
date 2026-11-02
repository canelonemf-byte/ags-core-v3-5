# Revisión LLP — HYBRIX (proyecto nuevo)

Fecha: 2026-11-02 Europe/Madrid  
Autor revisión: AGs-Core Supervisor (importación Drive aprobada por Lázaro López Paz)  
Autoría declarada del material: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA

## Importación

- Fuente: Google Drive del propietario (archivos 2026-11-01 15:48–16:21 UTC+1)
- Paquete principal: `hybrix_sistema_completo_v2.0.zip` (953465 bytes)
- Destino: `knowledge/hybrix/` (NO dentro de ordenador-hibrido-no-binario)
- Nombres sanitizados a snake_case; sin `.bak`

## Originalidad (vs knowledge AGs-Core)

- Exact duplicates vs otros proyectos: **0**
- Near-duplicates Jaccard≥0.85 vs otros proyectos: **0**
- Duplicados internos: solo copias intencionadas del mismo paquete (p. ej. gerber anidado); se eliminaron mirrors `code/` y `docs/` redundantes
- Referencias a Cortical Labs / FinalSpark / SpiNNaker / DishBrain: citas de estado del arte, no código de terceros detectado en el paquete
- Declaración de originalidad del autor presente en Docs Drive; **no implica** verificación legal externa

## Certificado de auditoría de bioseguridad

Archivo: `drive/certificado_auditoria_bioseguridad_hybrix.pdf` (5273 bytes)

Hallazgos:
- Se autodenomina «CERTIFICADO OFICIAL DE AUDITORÍA BSL-2»
- Emisor declarado: «Laboratorio Bio-Core BSL-2», El Prat de Llobregat
- Firma co-firmante: «Dr. Aris Thorne, Oficial de Bioseguridad y Calidad ISO 14644»
- Hash declarado: `SHA256-HYB20-PASSED` (formato no es un SHA-256 real)
- ISO 14644 es norma de salas limpias / partículas, **no** es el marco emisor de acreditación BSL-2 en España
- En España, acreditaciones de laboratorio pasan por esquemas tipo ENAC / autoridades competentes; no hay evidencia de emisión por ENAC u organismo reconocible para este PDF
- «Dr. Aris Thorne» aparece como persona editorial genérica en sitios web no relacionados; **no** se verificó como auditor BSL-2 de este proyecto

**Dictamen:** documento **autogenerado / no respaldado** como certificación oficial. **No válido como acreditación BSL-2.** Marca: **PENDIENTE DE VERIFICACIÓN** / no usar como prueba regulatoria.

## gemini-code-zenodo.json

- Contenido: metadatos de creador Zenodo (nombre Lázaro López Paz + ORCID `0000-0001-8601-1963`)
- Relevancia HYBRIX: plantilla de autoría para un posible depósito futuro; **no** es código ni DOI de HYBRIX
- ORCID verificado vía API pública ORCID (2026-11-02): ese id resuelve a **Helios Energía Solar**, no a Lázaro López Paz → **conflicto de autoría / PENDIENTE DE VERIFICACIÓN**
- **No hay DOI Zenodo/Crossref** en el material HYBRIX importado

## Software y pruebas (verificación local)

- `paquete/main.py` llegaba con `SyntaxError` (string partido en `write_text`); corregido en local a `"\n".join(lines)`
- `test_suite.py` carecía de `from pathlib import Path` (NameError); import añadido
- Tras correcciones: suite unittest ejecutada (ver registro); el informe original que afirma 100% PASS / TEST-01..06 **no se toma como verificado** sin evidencia reproducible previa
- `hybrix_qmatrix_sensor.py`: clase documentada como **«Simulador»** → simulación
- `hybrix_events_sample.log` + `generate_event_logs_and_plot.py`: patrón sintético de viabilidad → simulación
- `simulador_nodo_biologico.py`: simulación explícita

## Clasificación de afirmaciones (resumen E0–E6)

Ver detalle en `docs/registro_evidencia.json`.

| Afirmación | Tipo | Nivel |
|---|---|---|
| Diseño API FastAPI telemetría/predicciones | software / hipótesis de arquitectura | E3 (código presente; tests frágiles) |
| Cultivo neuronal humano / organoide operando en Bio-Core | experimento biológico | E0 (sin evidencia experimental en el paquete) |
| Medidas ΔP -52.4 Pa, viabilidad 96.4%, ODMR 99.1%, etc. del certificado | datos de laboratorio | E0 / no verificados; probable simulación o invención |
| Q-MATRIX ODMR / NeuroGlyQ | simulación en código | E2 |
| Logs de conmutación GenAI / LoRa | simulación | E2 |
| Certificado BSL-2 oficial | documento | E0 (no válido como certificación) |
| Coste nodo 167.50 USD / BOM | estimación de diseño | E1 (lista de componentes; precios no auditados) |
| Rendimiento API 225.87 req/s | benchmark | PENDIENTE DE VERIFICACIÓN (no reproducido aquí) |

## Licencias y autoría

- Añadidos `LICENSE` (MIT) y `NOTICE` (CC BY 4.0 para documentos + créditos)
- Cadena de autoría LLP aplicada en `estado.json` / README
