# Recuperación tras incidente de disco — 2026-10-21

Autor responsable: Lázaro López Paz. Documento de incidente; no contiene datos inventados.

## Incidente
Hacia las 11:30 (Europe/Madrid) del 2026-10-21 el ordenador de trabajo se reinició. Durante unos minutos el disco apareció a medio restaurar: el git local de `ags-core-v3.6` mostraba `fatal: bad object HEAD` y objetos ausentes, `knowledge/fusi-n-carpeta` aparecía casi vacía, el código de NNC no estaba y `/cursor/stores` no estaba montado.

## Resultado: pérdida transitoria, todo recuperado
Al terminar la restauración del disco (hacia las 11:40) se comprobó:
- Git de `ags-core-v3.6` íntegro (`git fsck` sin objetos ausentes); los commits locales `9514804`, `c8237d7` y `caaa02a` existen.
- `knowledge/fusi-n-carpeta` completa (datos, scripts, protocolo, esquema, `estado.json`, adaptador).
- Test congelado presente y verificado: `data/test.jsonl` sha256 `0937f06c329f1744f22570dab347aca26fa487c771356027b9bdead33e6f8ef5`. **No hace falta volver a congelarlo.**
- NNC restaurado (commit `3508bed`) y `/workspace/atlas0` con su commit `a14af4d`.

## Reconciliación con GitHub
Durante el incidente se publicó en `origin/main` un commit de recuperación (`4528bc7`) reconstruido sobre `ad84131`. Se ha fusionado en `main` (merge normal, sin force), con preferencia por el contenido original y conservando las adiciones supervivientes. Las copias intermedias quedan en `/workspace/recovery/` (`ags-core-v3.6.broken`, `ags-core-v3.6.rebuilt`).
