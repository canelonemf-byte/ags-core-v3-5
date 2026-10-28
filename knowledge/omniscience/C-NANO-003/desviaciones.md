- D0 (antes de congelar): sin regla rotacional (hiphive ausente) → ajuste ZA a 3 amplitudes. base_nano2.py cambia D3_CUT a 95 y peso metálico Mo/W.
- D1 (antes de congelar): GPAW de apt desapareció tras restaurar la máquina; reinstalación intentada (logs/apt_gpaw.log).
- D2 (durante la evaluación, antes de la evaluación final): /workspace/omniscience_cnano002/out faltaba tras la restauración de la máquina (C2 salía no evaluable por ruta). Se restauró copiando C-NANO-002/out del store (datos de entrada, sin cambiar código).
D3: rerun C1 2026-10-23 tras restauración; GPAW reinstalado (apt gpaw 25.1.0); salida sincronizada al store cada 60 s
