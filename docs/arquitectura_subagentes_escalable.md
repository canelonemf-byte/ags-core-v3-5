# arquitectura_subagentes_escalable
meta: {proyecto: agsgpt_lora_nnc, fecha: "2026-10-20", autor: "Lázaro López Paz, con asistencia de IA", evidencia: E1, estado: conceptual}
objetivo: "Arquitectura escalable de sub-agentes supervisados por AGs-Core v3.6; 50000 sub-agentes = diseño conceptual, no implementado."
datos_clave:
  - "Implementado (E3 software): AGs-Core v3.6, 85 agentes registrados en API :8000, autopilot SQLite (review_claims, missing_pieces, license_check), UCS memoria."
  - "NNC/ags-core, sistema-nnc-ags-core-corregido-1.0.0 y artifacts/agsgpt/estado.json: NO encontrados en box, stores ni Drive (PENDIENTE DE VERIFICACIÓN)."
  - "AGsGPT+LoRA: sin código ni pesos en box (E1/E2 conceptual)."
  - "Escalado propuesto: supervisor -> jefes de dominio (6 proyectos) -> pools de workers efímeros por tipo de tarea, cola SQLite->Redis/Postgres al superar ~1e3 tareas/min (estimación, PENDIENTE DE VERIFICACIÓN)."
tareas:
  - "Aportar código NNC/AGsGPT para integrarlo como proyecto."
  - "Definir workers como procesos sin estado leyendo de la cola compartida."
  - "Ciclo falsación E0-E6 por proyecto (propuesto, no creado)."
riesgos:
  - "Afirmar 64 agentes/61 subagentes/ciclo 16/7-7 PASS sin artefactos."
  - "Pesos de terceros en LoRA requieren licencia del modelo base."
decisiones:
  - "No se simula ni inventa estado de NNC."
proximo_paso: "Usuario sube NNC (zip o repo) al box o Drive; supervisor lo integra en projects.json, knowledge/ y ingest_ucs.sh."

## Actualización 2026-10-21: simulación E1–E2
Ver `docs/subagentes_2026-10-21.md` y `scripts/sim_subagentes.py` (workers simulados, no agentes reales). Sub-agentes reales: 7.
