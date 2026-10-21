# Recuperación tras pérdida de datos — 2026-10-21

Autor responsable: Lázaro López Paz. Documento de incidente; no contiene datos inventados.

## Incidente
Hacia las 11:30 (Europe/Madrid) del 2026-10-21 el ordenador de trabajo se reinició. Tras el reinicio, el repositorio local `ags-core-v3.6` quedó con el git corrupto (`fatal: bad object HEAD`, 136 blobs ausentes) y se perdieron archivos de trabajo.

## Perdido (no recuperable desde el box ni desde GitHub)
- Commits locales nunca subidos: `9514804` (correcciones aprobadas 2026-10-21), `c8237d7` (license_check, NOTICEs, autoría), `caaa02a` (llp_pack: cero_a, remplast_q, helioatlas, mei_rit, esqueleto v1.1). El reflog conserva sus mensajes, pero no sus objetos.
- `knowledge/fusi-n-carpeta`: datos del dataset LoRA (splits train/val/test), scripts (`merge_pares.py`, scorer de `sin_respuesta`), protocolo de comparación, esquema `esquema_lora_pares.md`, `manifest.json`, `estado.json`, resultados y adaptador de la prueba pequeña (`adapters/smoke_lowmem`).
- Código de NNC (`/workspace/agsgpt/NNC`: solo quedó `logs/` y un `.git` vacío).
- Objetos git de `/workspace/atlas0` (los archivos de trabajo sobrevivieron).

## Test congelado
El test congelado (sha256 `0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5`; splits 817/201/66) **no es recuperable**: ningún archivo del box coincide con ese hash. Si no aparece una copia en otro agente que coincida con el hash, debe **volver a congelarse mediante una enmienda fechada del protocolo** antes de cualquier entrenamiento o evaluación. Cualquier resultado anterior calculado sobre el test perdido queda sin verificación reproducible.

## Recuperado
- Historial hasta `ad84131` desde `github.com/canelonemf-byte/ags-core-v3-5` (rama `main`).
- Archivos del árbol de trabajo que sobrevivieron al reinicio, superpuestos sobre `ad84131` (incluye las correcciones de `9514804`/`c8237d7` presentes en el árbol, `knowledge/llp_pack/`, `knowledge/remplast-q/fuentes_cc_by/`, `docs/arquitectura_subagentes_escalable.md`).
- `knowledge/llp_pack/proyectos/{cero_a,remplast_q,helioatlas,mei_rit}.json` y `knowledge/llp_pack/esqueleto.json`, recreados con el contenido exacto pegado por el usuario el 2026-10-21.

## Pendiente
- Pedir a los agentes (CERO-A, ORDENADOR HÍBRIDO, REMPLAST-Q, OMNISCIENCE, ORÁCULO, FUSIÓN IA) copias de sus pares y scripts; verificar por hash antes de reintegrar.
- Reconstruir `fusi-n-carpeta` y volver a congelar el test con enmienda fechada.
- Recuperar el código de NNC desde su remoto (PENDIENTE DE VERIFICACIÓN: remoto desconocido).
- Copia rota conservada en `/workspace/recovery/ags-core-v3.6.broken`.
