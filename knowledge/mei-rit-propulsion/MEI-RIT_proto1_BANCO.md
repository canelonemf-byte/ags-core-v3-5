# MEI-RIT proto1 — ejecución de los 3 pasos
2026-09-22. Este entorno no compra ni enciende. El pack es el protocolo de banco.

Matching nominal (Rs plasma ~4 Ω): Cs=200 pF · Cp=796 pF · L=848 nH · 13.56 MHz.
Catálogo: 180 pF + trimmer 10–60 pF serie; 800 pF + trimmer 50–500 pF paralelo. 5 kV.

## Paso 1 — Pedir
Ver `MEI-RIT_proto1_RFQ.md` y hoja RFQ del xlsx.
Crítico: tubo ID 32.00±0.20 / capilar ID 0.20±0.02 / grids pitch 1.50±0.05.
No Al, no Cu expuesto, no joya 55 μm.

## Paso 2 — Argón (obligatorio antes de I2)
1. Montar tubo + bobina 5× paso 4.5 mm + red LC. Coupler en línea.
2. Vacío 2e-5–8e-5 mbar. Ar 5.0 a 0.15–0.6 Pa.
3. Barrido P_fwd 5→30 W. Anotar P_fwd, P_ref, C trimmer.
4. PASS si a 18–25 W: |Γ|<0.15, plasma estable, T_bobina<80 C, sin arco.
5. FAIL / no abrir I2 si |Γ|>0.25 a 22 W o trimmer al tope.
Sustituir `MEI-RIT_proto1_gamma_plantilla.png` por la curva medida (misma abscisa).

## Paso 3 — I2 solo con gate Ar en PASS
1. Cold trap ON (≤−70 C) + liner. Turbo protegida.
2. Líneas 110 C, tanque rampa 90 C. Capilar 60 mm ya cortado.
3. Filamento W ON, emisión >1.2 Ib.
4. RF 10 W → 22 W. HV −150 luego +1200 V.
5. Target Ib=16 mA. Log Γ, T_tank, T_line, Ib, Iacc.
6. Apagado: HV/RF off; tanque 40 C con líneas calientes; N2 seco al airear.

## Gate
Ar PASS → I2 permitido.
Ar FAIL → no I2. Rehacer matching o presión, no “probar yodo a ver”.
