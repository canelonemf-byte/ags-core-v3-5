# Escala de evidencia OMNISCIENCE (E0–E6)

**Origen:** escala tomada **literalmente de los propios documentos**, no propuesta por el agente.
Fuente canónica elegida: `OMNISCIENCE_maestro.tex`, tabla «Niveles de evidencia de OMNISCIENCE» (`tab:niveles`), idéntica en contenido a `docs/OMNISCIENCE_PUBLICACION_v1.0.0.md` §4. El prefijo «E» es solo notación del registro.

| Nivel | Estado | Significado (literal, OMNISCIENCE_maestro.tex) |
|---|---|---|
| E0 | Idea | Concepto sin evaluación formal. |
| E1 | Hipótesis | Propuesta falsable. |
| E2 | Predicción | Resultado de un modelo o algoritmo. |
| E3 | Simulación verificada | Resultado reproducible bajo condiciones definidas. |
| E4 | Observación experimental | Medición documentada. |
| E5 | Réplica independiente | Resultado confirmado por otra ruta. |
| E6 | Conocimiento consolidado | Evidencia convergente con limitaciones explícitas. |

Variante en la Publicación v1.0.0 (§4), mismo sentido: 0 Idea «Concepto sin evaluación formal» · 1 Hipótesis «Propuesta falsable» · 2 Predicción «Resultado de un modelo o algoritmo» · 3 Simulación verificada «Reproducible en condiciones declaradas» · 4 Observación experimental «Medición documentada» · 5 Réplica independiente «Confirmado por otra ruta» · 6 Conocimiento consolidado «Evidencia convergente con límites explícitos».

## ⚠️ Inconsistencia detectada: el Documento Maestro 2026 usa 8 niveles (0–7)
`OMNISCIENCE_Documento_Maestro_2026.tex/.md` §4:
0 Idea · 1 Hipótesis («Propuesta explícita y falsable») · 2 Predicción («Resultado derivado de un modelo o algoritmo») · 3 **Simulación reproducible** («Resultado que puede repetirse bajo condiciones documentadas») · 4 Observación experimental («Medición documentada con incertidumbre») · 5 Réplica independiente («Confirmación mediante una ruta metodológica independiente») · **6 Evidencia convergente** («Varias líneas independientes apuntan al mismo resultado») · **7 Conocimiento consolidado** («Resultado robusto, replicado y con límites conocidos»).

Equivalencia: niveles 0–5 coinciden; el 6 de la escala 0–6 fusiona los niveles 6 y 7 del Documento Maestro. Recomendación: el autor debe fijar una única escala canónica y versionarla (la 0–6 es la usada por la campaña ejecutada C-VIB-001 y por la publicación v1.0.0).

## Reglas de aplicación usadas en este registro (convenciones del agente, no de los documentos)
1. **Nivel = evidencia verificable hoy.** Si un documento *declara* un nivel pero los artefactos no están disponibles para comprobarlo (scripts, datos, hashes), se registra el nivel verificable y se anota el declarado. Ej.: C-VIB-001 declarado E3 → registrado E2 porque código/figuras/SHA256SUMS solo están en Drive.
2. **[externo] vs [interno].** Fórmulas y resultados de física establecida que el proyecto adopta (matriz dinámica, E_form, κL cinética…) se registran como E6 *por la literatura*, marcados `[externo]`; esto **no** significa que OMNISCIENCE los haya implementado o verificado.
3. **Resultados de libro de texto como calibración** (H1–H6 de C-VIB-001) se tratan como calibración del motor, no como descubrimiento, tal como dice el propio documento.
4. Para subir de nivel: E2→E3 exige re-ejecución reproducible (mismo entorno, semilla, hashes); E3→E4 exige medida documentada; E4/E3→E5 exige ruta metodológica distinta (otro código, funcional, instrumento u operador); E6 exige convergencia de varias líneas con límites explícitos.
5. Gobernanza heredada: C-BIO-001 y C-FUS-001 no avanzan de E1 sin aprobación humana; toda acción física de riesgo requiere revisión humana.
