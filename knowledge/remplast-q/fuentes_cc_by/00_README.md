# REMPLAST-Q · paquete de documentación (v2.1 pública, 2026-10-20)

## meta
- proyecto: REMPLAST-Q (detección y tratamiento de microplásticos, MPs)
- usuario: Lázaro López Paz
- idioma: es · formato: Markdown compacto (para leer) + JSON (para máquinas; claves snake_case, sin null, vacío = "" o [])
- regla de datos: ninguna cifra sin fuente enlazada; "" = sin dato localizado; cada cifra lleva estado de verificación

## licencia_y_autorizacion
- autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España · ORCID 0000-0001-8601-1963 (https://orcid.org/0000-0001-8601-1963); elaborado con asistencia de inteligencia artificial
- licencia: Creative Commons Atribución 4.0 Internacional (CC BY 4.0) – https://creativecommons.org/licenses/by/4.0/deed.es (libre uso, copia, adaptación y uso comercial citando la autoría)
- autorización: El autor autoriza expresamente a cualquier grupo, entidad o persona a ejecutar el proyecto REMPLAST-Q, total o parcialmente, sin necesidad de su participación.
- petición: Única petición (no es condición de la licencia): si se realiza el proyecto, comunicar los resultados obtenidos al autor.

## estructura
```
remplast_q/
├── 00_README.md                  ← este índice
├── LICENSE.md                    ← licencia CC BY 4.0
├── remplast_q.json               ← resumen maestro (meta/objetivo/datos_clave/tareas/riesgos/decisiones/proximo_paso)
├── referencias.md / .json        ← bibliografía unificada (90 entradas; 55 DOI comprobados en Crossref)
├── 01_revision_tratamiento/      ← estado del arte v2 (23 tecnologías) + verificacion_crossref.json
├── 02_lodos/                     ← MPs en lodos y biosólidos, tratamientos y normativa UE/España
├── 03_costes/                    ← CAPEX/OPEX/energía comparados (generales vs específicos de MPs)
├── 04_plan_proyecto/             ← plan realizable: tren, fases, protocolo, KPIs, riesgos, presupuesto, financiación
└── 05_solicitud_aei/             ← solicitud AEI PGC 2026: requisitos, memoria (anexo VII), presupuesto, checklist, correo-plantilla
```

## orden_de_lectura
1. remplast_q.json o este README (visión global, 5 min)
2. 05_solicitud_aei/requisitos_aei.md (BLOQUEANTE de afiliación y opciones) y checklist_solicitud.md (fechas hasta el 24-11-2026)
3. 04_plan_proyecto/plan_proyecto_remplast_q.md (qué hacer y qué decidir)
4. 05_solicitud_aei/memoria_cientifico_tecnica.md y presupuesto_aei.md
5. 01_revision_tratamiento (por qué ese tren)
6. 02_lodos y 03_costes (soporte del tren y del presupuesto)
7. referencias.md (comprobar cualquier cifra)

## leyenda_verificacion
- TC: cifra comprobada en texto completo · RES: solo resumen · SEC: reseña que cita a otro estudio · COM: proveedor/comercial · FRAG: fragmento de buscador o página no leída completa · OFI: texto oficial EUR-Lex/BOE · EST: estimación propia justificada

## resumen
- tren recomendado: primario+secundario existentes → coagulación ligera + filtración rápida en arena (A) frente a arena+biochar (B), con UF como referencia (C); ozono solo si hay 4ª etapa y antes del filtro; lodo a pirólisis ≥450–500 °C o monoincineración con recuperación de P
- fases: f0 preparación (M1–M3) · f1 línea base (M3–M9) · f2 banco (M6–M15) · f3 piloto + lodos (M12–M30) · f4 evaluación (M27–M36)
- decisión dp2 RESUELTA: AEI Proyectos de Generación de Conocimiento 2026, solicitada por universidad u organismo público (plazo 3–24-11-2026, 14:00 Europe/Madrid)
- BLOQUEANTE: el IP debe ser doctor/a (antes del 1-1-2025) y estar vinculado/a a una entidad elegible; Lázaro López Paz, sin afiliación, solo puede estar en el equipo de trabajo → el proyecto requiere un IP doctor/a vinculado/a a una entidad elegible
- plan ajustado a 36 meses (1-9-2027 a 31-8-2030; la AEI no admite inicio anterior)
- decisiones pendientes: dp1, dp3–dp7 (04_plan_proyecto) y modalidad/tipo/predoctoral (05_solicitud_aei)

## limitaciones
- varias fuentes solo se leyeron en resumen (RES/FRAG): se indica en cada cifra
- costes casi nunca específicos de MPs; costes españoles en € de 2011; suizos en CHF de 2024 (sin conversión)
- DAF y filtros de discos: costes solo de proveedores
- Horizon Europe (plazos) y CDTI/LIFE (condiciones) proceden de páginas no oficiales o fichas: verificar en el portal oficial
- KPIs numéricos y estimación de energía del piloto son propuestas (EST)
- los modelos 2026 de memoria y CVA no estaban publicados en la web AEI a 18-10-2026: se siguió el anexo VII 2026 y los epígrafes del modelo 2025
- la ficha BDNS 918664 no cargó desde el entorno; el texto completo se leyó en aei.gob.es

## autoria_05
- Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial; ORCID 0000-0001-8601-1963
