> Texto extraído automáticamente del PDF original «OMNISCIENCE_PUBLICACION_v1.0.0.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1tCq3-SjVM_ghsYm2DaPuJOECI6nU8wmt/view?usp=drivesdk



DOCUMENTO ÚNICO DE PUBLICACIÓN  ·  v1.0.0

OMNISCIENCE

Universal Autonomous Scientific Discovery Engine

README · checklist · repositorio · procedencia · C-VIB-001

Evidencia máxima: nivel 3  ·  Sin experimento  ·  Sin réplica

LÁZARO LÓPEZ PAZ

El Prat de Llobregat  ·  29 agosto 2026  ·  revisión editorial pendiente

OMNISCIENCE  v1.0.0 Documento de publicación

Lázaro López Paz  ·  29 agosto 2026 2

1. Cómo leer este documento

Este PDF es el documento único de publicación v1.0.0. Reúne README, metadatos YAML, checklist
editorial, árbol del repositorio, metodología, gobernanza, citación y el estado real de evidencia. No
anexa los PDFs maestros (están referenciados). Ningún resultado se presenta como experimento ni
como conocimiento consolidado.

2. Metadatos de publicación

Campo Valor

versión 1.0.0 · 2026-08-29

estado preparada para revisión editorial

autor Lázaro López Paz, El Prat de Llobregat, Barcelona, ES

evidencia máxima 3 — simulación verificada

validación experimental false

réplica independiente false

campaña ejecutada C-VIB-001

campañas propuestas C-MAT-001, C-META-001, C-QDY-001, C-QSN-001, C-ENE-001, C-BIO-001,
C-FUS-001

revisión humana final obligatoria antes de DOI

licencia pendiente (CC BY 4.0 docs · MIT/Apache código)

3. Checklist editorial

Catorce ítems cubiertos por este paquete. Seis pendientes, declarados. La revisión humana final no
se marca hecha.

Ítem Hecho Nota

Portada y metadatos sí OG, JSON-LD, author.json

Autoría confirmada sí Lázaro López Paz

Versión v1.0.0 sí 2026-08-29

README / este documento sí único

Documento maestro sí 23 p. LaTeX

Informe C-VIB-001 sí nivel 3

Suplemento técnico (06) no PDF separado pendiente

Hoja de ruta sí campañas en §5

Gobernanza y seguridad sí §8

Bibliografía auditada (09) no audit_log.csv pendiente

Código asociado sí cuatro scripts

Datos asociados no series crudas no empaquetadas

Figuras asociadas sí 01–09, 11–12

Manifiesto de procedencia sí PROV-O + YAML

Pruebas automáticas no pytest no publicado

Sumas SHA-256 sí SHA256SUMS.txt

Licencias revisadas no pendiente de firmar

Estado de evidencia sí máximo 3

OMNISCIENCE  v1.0.0 Documento de publicación

Lázaro López Paz  ·  29 agosto 2026 3

Ítem Hecho Nota

Declaración de limitaciones sí §8 C-VIB-001

Revisión humana final no bloquea el DOI

4. Visión y ciclo

OMNISCIENCE no genera respuestas sin verificación. Gestiona campañas: problema → hipótesis
falsable → predicción cuantitativa → simulación o experimento autorizado → falsación → réplica
independiente → conocimiento consolidado. Nueve motores federados. La regla no negociable:
ningún resultado se presenta como descubrimiento experimental o conocimiento consolidado sin el
nivel, los artefactos y la verificación que correspondan.

Nivel Estado Definición

0 Idea Concepto sin evaluación formal

1 Hipótesis Propuesta falsable

2 Predicción Resultado de un modelo o algoritmo

3 Simulación verificada Reproducible en condiciones declaradas

4 Observación experimental Medición documentada

5 Réplica independiente Confirmado por otra ruta

6 Conocimiento consolidado Evidencia convergente con límites explícitos

5. Proyectos y campañas

ID Proyecto Motor Estado N

C-VIB-001 Vibraciones, modos y fonones 1D Phonon Ejecutado 3

C-MAT-001 Estabilidad y fonones cristalinos Matter Propuesto 1

C-META-001 Metamateriales y cristales fonónicos Metamaterial Propuesto 1

C-QDY-001 Dinámica cuántica abierta, FMO, Lindblad Quantum Dyn. Propuesto 1

C-QSN-001 Sensores cuánticos y ruido Sensing Propuesto 1

C-ENE-001 Energía y transporte térmico Energy Propuesto 1

C-BIO-001 Biomateriales y terapéutica Bio Propuesto 1

C-FUS-001 Materiales de fusión y gemelo digital Fusion Propuesto 1

C-VIB-001 cubre H1–H6: oscilador amortiguado, FFT/espectrograma, modos de cuerda y membrana,
masas acopladas, dispersión 1D, cristal fonónico, QHO. Predicciones y falsación declaradas antes de
evaluar. Semilla 7. No sustituye FEM 3D ni DFT/DFPT.

6. Serie documental 00–09

n Archivo Papel

00 PORTADA_Y_GUIA_DE_LECTURA Este documento

01 DOCUMENTO_MAESTRO_OMNISCIENCE Arquitectura y motores

02 MANIFIESTO_DE_PROYECTOS Líneas heredan MV1

03 METODOLOGIA_EVIDENCIA_Y_REPRODUCIBILIDAD Niveles 0–6

04 GOBERNANZA_ETICA_Y_SEGURIDAD Aprobación humana

05 C-VIB-001_INFORME_CIENTIFICO Campaña ejecutada

06 C-VIB-001_SUPLEMENTO_TECNICO Pendiente

OMNISCIENCE  v1.0.0 Documento de publicación

Lázaro López Paz  ·  29 agosto 2026 4

n Archivo Papel

07 C-VIB-001_DATOS_CODIGO_Y_PROCEDENCIA Scripts y PROV

08 HOJA_DE_RUTA_DE_PROYECTOS Campañas propuestas

09 BIBLIOGRAFIA_Y_AUDITORIA_DE_CITAS Pendiente

7. Repositorio (contrato de carpetas)

El árbol de publicación queda fijado. docs/ 00–06, code/src/omniscience (io, core, models, analysis,
visualization), campaigns/C-VIB-001…C-FUS-001, provenance/ con RO-Crate, data/, figures/, tests
unit/integration/regression. Este documento no sustituye el clone: describe el contrato. Reproducir
C-VIB-001: python3 campaigns/C-VIB-001/code/simular_vibraciones.py y animar_modos.py;
sha256sum -c provenance/checksums.sha256; pytest campaigns/C-VIB-001/tests. Si una figura
cambia con el mismo entorno, parámetros y semilla, la campaña pasa a inconcluso.

omniscience/
docs/00-publicacion … 06-publicaciones/v1.0.0
code/src/omniscience/{io,core,models,analysis,visualization}
code/campaigns/{C-VIB-001 … C-FUS-001}
code/tests/{unit,integration,regression}
provenance/C-VIB-001/{manifest.yaml, ro-crate-metadata.json, checksums.sha256}
figures/C-VIB-001 data/{raw,interim,processed}

8. Gobernanza, límites y metodología

Permitido sin más trámite: simulación, literatura pública, priorización, informes. Aprobación humana
obligatoria: laboratorio robotizado, síntesis, modificación biológica, células/animales, terapéutica
operativa, radiología, fusión/fisión/tritio, diagnóstico médico. C-BIO-001 y C-FUS-001 no avanzan de
nivel 1 sin esa puerta. Criterio genérico de discrepancia: z = |y − ŷ| / √(σ_pred² + σ_ref²); z > 3 exige
revisión o falsación. Umbrales de cada campaña se fijan antes de ver el resultado. Prioridad S = wI I
+ wF F + wN N + wR R + wE E − wC C − wQ Q.

Límites de C-VIB-001: modelos canónicos; cristal 1D idealizado; no FEM 3D; no DFT/DFPT; no
LDV/Raman/Brillouin/neutrones; no no-linealidad, solitones, desorden ni Anderson. No justifica
experimentos no realizados.

9. Procedencia mínima C-VIB-001

campaign: C-VIB-001
version: 1.0.0
date: 2026-08-28
evidence_level: 3
status: executed
experimental_measurement: false
independent_replication: pending
random_seed: 7
outputs: [figures/, report/, data/]

10. Citación

López Paz, L. (2026). OMNISCIENCE: Universal Autonomous Scientific Discovery Engine (versión
1.0.0). Proyecto de investigación reproducible.

López Paz, L. (2026). C-VIB-001: Análisis computacional de vibraciones, modos y fonones 1D (versión
1.0.0). OMNISCIENCE.

Archivos: CITATION.cff, author.json (Schema.org Person), citations.json (CSL). Si se continúa el
trabajo, citar a Lázaro López Paz y a Grok. Licencia aún no firmada: no redistribuir como paquete con
licencia inventada.

OMNISCIENCE  v1.0.0 Documento de publicación

Lázaro López Paz  ·  29 agosto 2026 5

11. SHA-256 del paquete

SHA-256 Archivo

53f7d840e75d4157… docs/OMNISCIENCE_dossier_completo.pdf

8226acdf4c70ba13… docs/OMNISCIENCE_maestro_unificado.pdf

d40adb874610e02c… docs/Analisis_vibraciones_cientificas_Grok.pdf

ac24fd511dbadc43… docs/OMNISCIENCE-MV1-implementacion.pdf

9fff7fbf9b0e57db… author.json

e0461cd4b4857431… citations.json

9d5988efabcb6358… publication.yaml

95994d5de64ecafc… CITATION.cff

c360f1df12166a85… code/omniscience_mv1.py

94329cad491903e6… code/simular_vibraciones.py

4e5fd1c62668416d… code/animar_modos.py

56513aadf2e407b0… code/crear_informe_pdf.py

40d6edd02a50e0c9… og.jpg

8639a090e0d14173… x-banner.jpg

Hash abreviado. El archivo SHA256SUMS.txt lleva el digest completo.
