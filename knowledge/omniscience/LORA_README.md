# OMNISCIENCE: pares LoRA y fuentes (formato LLP)

```yaml
meta:
  proyecto: omniscience
  autor: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial"
  orcid: 0000-0001-8601-1963
  licencia: CC BY 4.0
  fecha: 2026-10-21
  aprobacion: "Aprobado por Lázaro López Paz el 2026-10-21"
objetivo: "Integrar en AGsGPT los pares LoRA de OMNISCIENCE (Universal Matter, Phonon Engine, nano) con fuentes trazables y nivel de evidencia E0-E6"
datos_clave:
  - "lora_pares.jsonl: 181 pares, esquema FUSIÓN IA (docs/esquema_lora_pares.md), 181/181 válidos"
  - "sha256 lora_pares.jsonl: 1fc34ce32023e025011c9c0c512b714de8adb69786ba58bd37c0a0cdfbb12034"
  - "sha256 evidence_register.csv: 842990d66215091428d9e27d41445bf324c79791c9814575ace7daf560231aee"
  - "sha256 SHA256SUMS_lora_fuentes.txt: c4c3cd5ca47c48608d24c37473ee5d74a6f149cb1ca96aa0fc2c325127b00e7e (sumas de los 305 ficheros añadidos)"
  - "Fuentes: evidence_register.csv, log_avances.md, escala_E0_E6.md, campañas C-MAT-001..007, C-UMF-001..006, C-VIB-001..002, C-NANO-001, innovacion/, nano/"
  - "Nivel máximo verificado: E3 (simulación); sin E4/E5"
tareas:
  - "Ejecutar merge de pares del pipeline FUSIÓN IA cuando Lázaro lo indique"
riesgos:
  - "C-UMF-006 provisional (E1): cálculo híbrido PBE0 pendiente"
  - "El campo autor de los pares usa 'con asistencia de IA' porque el esquema solo admite esa forma"
decisiones:
  - "Excluidos PDFs, referencias de terceros (refs/), logs, trayectorias, salidas brutas (out/) y estructuras CIF/VASP"
  - "fuente = ruta relativa a ags-core-v3.6/; fuente_repo eliminado; fuentes de carpeta apuntan a resultados_<campaña>.md"
  - "Sin push ni entrenamiento"
proximo_paso: "Revisión de Lázaro y, si procede, merge de pares y push"
```
