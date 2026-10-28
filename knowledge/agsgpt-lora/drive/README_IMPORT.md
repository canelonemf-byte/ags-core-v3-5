# Import Drive AGsGPT_LoRA — 2026-10-27

Fecha de integración local: 2026-10-28 (Europe/Madrid).
Commit solo local; sin push ni entrenamiento.

## Contenido integrado (docs)

| Archivo | Qué es | vs repo |
|---------|--------|---------|
| `AGsGPT_LoRA.json` | Nodo de integración P003 (E1 declarado) | Nuevo respecto a `knowledge/agsgpt-lora/` (había README/código, no este JSON) |
| `AGsGPT_LoRA.md` | Resumen MD del mismo nodo | Nuevo |
| `agsgpt_lora.json` | Estado de tareas / flota (semilla, arquitectura d128…) | Nuevo; solapa parcialmente con `llp_pack/proyectos/P003-AGsGPT.json` |

## Solo referencia (NO producción)

| Archivo | Motivo |
|---------|--------|
| `referencia_runtime/projects_drive.json` | Catálogo de 12 proyectos con IDs distintos al `projects.json` de v3.6 (51). No reemplazar. |
| `referencia_runtime/auto_runner_drive.py` | Ciclos finitos vía `ags_core.orchestrator`. Inspección estática OK (sin red, sin subprocess, sin borrado, sin credenciales, sin git push). **No ejecutar** aquí; no sustituye `app/autopilot.py`. |
| `referencia_runtime/auto_log_drive.jsonl` | Log de una corrida previa (herramientas físicas locales). |

## Conflictos / PENDIENTE DE VERIFICACIÓN

1. Parámetros del modelo: Drive dice ~10M; `knowledge/agsgpt-lora/README.md` dice ~0,8 M. **PENDIENTE DE VERIFICACIÓN**.
2. Evidencia AGs-Core: Drive marca E1 (vídeo); el software AGs-Core/NNC/UCS en el ecosistema se trata como E3 software. No subir de nivel sin réplica.
3. `automatizacion_50k`: Drive E0 (correcto: no literal). Coherente con regla de no inventar 50k concurrentes.
4. Cifras del log (1050 kg NH3/h, CO2 evitado, Zeeman, ZNE E(0)=1.35833): salidas de herramientas con supuestos; **simulaciones E2**, no experimento.
5. Licencia modelo base LoRA 7B: ya anotada Apache-2.0 para Mistral/Qwen en correcciones previas; este import no añade pesos.
6. Autoría en JSON Drive usa "Lazaro Lopez Paz" sin tilde ni frase completa; se corrige en `AUTORIA.md` de este directorio.
7. 7 JPG del Drive no descargados.

## Inspección auto_runner (estática)

- Imports: `json`, `time`, `pathlib`, `sys`, `ags_core.orchestrator`
- Sin `requests`/`urllib`/`socket`/`subprocess`/`shutil.rmtree`
- Sin acceso a credenciales / `os.environ` / git push
- `MAX_CICLOS=20`, sleep 1s, escribe `auto_log.jsonl`
- Veredicto: seguro como referencia; no integrar como reemplazo del autopilot
