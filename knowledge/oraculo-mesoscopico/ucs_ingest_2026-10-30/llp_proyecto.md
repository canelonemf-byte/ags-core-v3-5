# ORÁCULO MESOSCÓPICO — ficha LLP (activación 2026-10-30)

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Código MIT / documentos CC BY 4.0.

Evidencia: E0 (baseline). Modelo ≠ realidad. Simulación ≠ experimento.

**id:** oraculo-mesoscopico
**estado:** activo
**objetivo:** Registro continuo de predicciones verificables con probabilidad p=P(enunciado verdadero), incertidumbre, supuestos y límites; verificación matemática (sympy/numpy) y mutation testing de pares; integración AGs-Core Supervisor v3. Modelo≠realidad; simulación≠experimento.

## datos_clave
- predicciones: 17 (abiertas 15, anuladas 2: OM-03, OM-04)
- n_verificadas: 0; brier_score: (vacío)
- matemáticas: {'pares': '42/42 verificados', 'pytest': '28/28', 'mutacion': '42/42 detectadas', 'nota': 'evidencia de ciclo local; MA-* siguen abiertas hasta fechas de resolución'}
- lora_pares: n=50, simulado=10, no_simulado=40, errores=0; fusion=NO aprobada; 40 pares reales SIN aprobar para fusión
- zenodo: concepto 22150377 / record 22150378
- github omniscience: 404 PENDIENTE DE VERIFICACIÓN (canelonemf-byte/omniscience)

## probabilidades abiertas
- CA-01: 0.92
- CA-02: 0.07
- CA-03: 0.9
- CA-04: 0.65
- CA-05: 0.95
- RQ-01: 0.88
- RQ-02: 0.85
- RQ-03: 0.75
- RQ-04: 0.8
- OM-01: 0.85
- OM-02: 0.45
- OM-05: 0.5
- MA-01: 0.85
- MA-02: 0.9
- MA-03: 0.75

## riesgos
- Brier vacío: 0 verificadas válidas (OM-03/OM-04 anuladas fuera del score)
- Inconsistencia LCOA CERO-A entre documentos históricos (simulación≠experimento)
- Repos GitHub omniscience/remplast-q/cero-a en 404
- Zenodo 1.0.1 bloqueado por autoría/RO-Crate/CITATION en pack Supervisor
- 40 pares LoRA no simulados SIN aprobar para fusión
- Publicación irreversible requiere OK Supervisor + verificación + confirmación Lázaro

## decisiones
- Evidencia baseline E0; conservar lo verificado; no inventar DOI/datos
- Anuladas fuera del Brier; estados: abierta|verificada|fallida|indeterminada|anulada
- OM-03 anulada (DOI Zenodo ya existía); OM-04 anulada por Lázaro 2026-10-22
- Reportar a Lázaro sólo si resuelto/usable/error accionable/decisión suya; tabla completa entonces
- Pares LoRA: 10 simulado=true etiquetados simulación; 40 no fusionar sin aprobación
- Autoría: Lázaro López Paz; IA sólo como asistencia en notas; ORCID 0000-0001-8601-1963
- Licencias: MIT código / CC BY 4.0 documentos
- Activación LLP 2026-10-30 por orden Supervisor (orden Lázaro 12:52 Europe/Madrid)

**proximo_paso:** Cerrar T03 UCS (/memory/stats OK); entregar reporte LLP al Supervisor; esperar OK Supervisor+fixes pack antes de cualquier push/Zenodo; no fusionar pares LoRA.

## originalidad (resumen)
- Registro probabilístico + Brier: precedente en Metaculus, Manifold Markets, Good Judgment/Tetlock, Brier HQ, Calibration Ledger (pre-lanzamiento; PENDIENTE DE VERIFICACIÓN independencia de scores)
- Mutation testing clásico (software): lit. consolidada; LLMMutation (IEEE) aplica mutación a evaluación de datasets LLM
- Mutación de fórmulas matemáticas: MAMUT/Math Mutator (arXiv 2502.20855) genera pares equivalentes/falsificados para entrenamiento
- LoRA + verificación matemática: hay fine-tunes LoRA para correctness (p.ej. proyectos públicos GitHub/HF); no se afirma prioridad de ORÁCULO
- diferencial: Combinación local: registro de predicciones de proyectos LLP (OMNISCIENCE/REMPLAST-Q/CERO-A) + verificador sympy/numpy + mutation testing de campo 'esperado' en pares + pares LoRA con etiqueta simulado; calibración Brier aún sin n_verificadas>0
- claim_novedad: No se reclama novedad absoluta. Solapamiento parcial con forecasting platforms y MAMUT. Combinación de dominio LLP: PENDIENTE DE VERIFICACIÓN exhaustiva.
