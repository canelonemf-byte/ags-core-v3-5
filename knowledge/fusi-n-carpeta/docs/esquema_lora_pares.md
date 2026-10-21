# Esquema de `knowledge/<proyecto>/lora_pares.jsonl`

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. Licencia: CC BY 4.0.

Un objeto JSON por línea (UTF-8), sin `null`, claves snake_case. Lo consume `scripts/merge_pares.py`.

| campo | tipo | obligatorio | regla |
|---|---|---|---|
| `instruction` | string | sí | alias aceptado: `instruccion` |
| `response` | string | sí | alias aceptado: `respuesta`. Para LLP, JSON compacto con claves meta, objetivo, datos_clave, tareas, riesgos, decisiones, proximo_paso |
| `autor` | string | sí | debe empezar por `Lázaro López Paz`; solo se admite añadir `con asistencia de IA` y/o la localidad. Otros coautores se rechazan |
| `fuente` | string | sí | **una** ruta relativa a `ags-core-v3.6/` que exista, empezando por `knowledge/` o `docs/`. Se rechazan PDFs, URLs, DOIs, arXiv o material de terceros |
| `licencia` | string | sí | `MIT` o `CC BY 4.0` |
| `proyecto` | string | sí | igual al nombre de la carpeta `knowledge/<proyecto>/` |
| `simulado` | bool | sí | `true` si el contenido sale de datos/simulaciones sintéticas |
| `id` | string | no | se recalcula: sha256(fuente + hash normalizado)[:16] |

Ejemplo:
```json
{"instruction":"...","response":"{\"meta\":{},\"objetivo\":\"...\",\"datos_clave\":[],\"tareas\":[],\"riesgos\":[],\"decisiones\":[],\"proximo_paso\":\"...\"}","autor":"Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA","fuente":"knowledge/mi-proyecto/README.md","licencia":"CC BY 4.0","proyecto":"mi-proyecto","simulado":false}
```

Proceso: dedup exacto (id) y normalizado (sha256 de instruction+response en minúsculas NFKC y espacios colapsados). Los items existentes nunca se mueven; una fuente ya presente conserva su split; una fuente nueva va a train/val/test por sha256(`42:<fuente>`) mod 100 (80/10/10). Rechazos con motivo en `data/rechazados.jsonl` (se regenera en cada ejecución). `data/manifest_prev.json` = manifest anterior.
