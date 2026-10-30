# Desviaciones C-VIB-004 (2026-10-29, Europe/Madrid)
- D1 entorno: el venv compartido /workspace/omniscience_cmat003/venv_ms tenía ase sin ase/build (mtime 09:02). No se tocó; se instaló ase==3.29.0 con uv (--no-deps) en /workspace/omniscience_cvib004/pylib y se usó vía PYTHONPATH. Declarado antes de ejecutar (riesgos del prereg).
- D1b prueba de humo: NaCl a a_exp con malla 7³ (no evaluable, borrada) antes del prerregistro: P 0.747 GPa, κ 5.856, ν_min 1.018 THz, 39 s, ~1.7 GB. Solo sirvió para fijar memoria/tiempo; no entra en la evaluación.
- D2 sin /usr/bin/time: maxrss lo registra el propio script (resource).
- D3 KI: C1 pasa por poco a d=0.03 Å (ν_min +0.022 THz) pero con d=0.01 Å sale ν_min −0.355 THz y κ×2.0 (B_H1 falla solo en KI). κ(KI, a_exp)=0.018 W/mK es no físico (×0.006 del experimental): se trata como inestabilidad marginal del modelo, no como resultado. El evaluador congelado lo incluye (regla prerregistrada) y no se recalcula la decisión.
- D4 análisis exploratorio post hoc (NO decisorio): sin KI, media |log10| 0.156 y 13/16 dentro de factor 2.
- D5 LoRA: el recuento real antes de esta campaña es 230 pares (regeneración 28-oct 13:40, LORA_REGEN_REPORT_20261028_1340.json), no 199 como en el informe del 28-oct.
- D6 no se hicieron NAC ni 4 fonones/SCPH (fuera de alcance del prereg; motivos en prereg).
