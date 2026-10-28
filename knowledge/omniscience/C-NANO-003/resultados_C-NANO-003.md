# Resultados C-NANO-003
Prerregistro sha256 5115c0b8759cbae6fd0630f16685651b15d68dbc12f915ec82a3c75f9e32dec5 (congelado 2026-10-22 23:42:56 CEST). Desviaciones: desviaciones.md (D0–D2).
- H1 FALLA: n_ZA mediana grafeno 2.042 (disp 0.089), hBN 2.073 (0.123; run2 0.172), MoS2 1.822, WS2 1.779, MoSe2 1.873.
- H2 PASA: WS2 E' 343.2/356 (−3.6 %), A1' 405.2/418 (−3.1 %); MoSe2 E' 276.1/288 (−4.1 %), A1' 234.3/242 (−3.2 %).
- H3 FALLA: 4/10 fuera de ±5 % frente a IXS (M ZA −15.8 %).
- H4/H5 PASAN: ΔS95 0.0920/0.0959/0.1181; |ΔS95−ΔS40| ≤ 0.0007.
- C3 PASA (grafito +1.87 %, hBN +3.04 %). C1 (GPAW WS2 Γ): NO EVALUABLE al cierre (cálculo en curso).
- H_REP PASA (Δfrec máx 0.078 %, Δn 0.045, ΔΔS 0.0075).
Niveles: NANO-04 E2, NANO-05 E3, NANO-14/15/16 E2, NANO-17 E3.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA · ORCID 0000-0001-8601-1963

## Nota C1 (2026-10-23 15:57 CEST)
C1 = NO EVALUABLE. No existe el fichero bruto out/gpaw/gpaw_WS2_gamma.json: /workspace/omniscience_cnano003/out/ desapareció tras restaurarse la máquina y la copia del store se hizo antes de que GPAW terminara. run_all.log registra «FIN gpaw 0» y «FIN_TODO 2026-10-23T09:30:46+02:00». El results.json que queda en /workspace (sin sincronizar al store) da C1 PASA: E' 343.2 frente a 344.6 (−0.41 %) y A1' 405.2 frente a 407.0 cm⁻¹ (−0.44 %), y NANO_04 = E3. Como el dato bruto no se puede verificar, no se adopta. NANO-04 sigue en E2 y el paquete v1 no cambia.

## Cierre C1 (2026-10-23 20:45 CEST)
Rerun de C1 (code/gpaw_c1.sh, GPAW 25.1.0, PBE PW500, k 12×12×1, posiciones relajadas PBE en la red MatterSim run1 a = 3.1907 Å; 15:59–19:39 CEST, dentro del tope de 4 h). Dato bruto out/gpaw/gpaw_WS2_gamma.json presente en el store. E' MatterSim 343.21 vs GPAW 344.63 cm⁻¹ (−0.41 %); A1' 405.18 vs 406.99 cm⁻¹ (−0.44 %). C1 PASA (±5 %). Con H_REP PASA, regla literal: NANO-04 E2→E3; NANO-14/15/16 heredan E3 (H2 positivo; H1 y H3 negativos con nivel E3). NANO-05 y NANO-17 sin cambio (E3). Backup: evidence_register.bak_C1_20261023_2042.csv
