# MEI-RIT proto1 realizable
2026-09-22. Corre: `python3 artifacts/mei_rit_realizable.py`
Checks: 6/6. Clase E2. Cero horas de fuego I2 propias.

## Qué se puede construir ahora
Head ICP 13.56 MHz + tanque PTFE/Al2O3 + capilar 192 μm × 60 mm + filamento W + grids grafito Ø28 + RF lab + HV lab.
No PPU de vuelo. No RF-cathode. No 2.45 GHz. No VQE en el banco.

## Cerrado
- T_tank = 90 C → Pvap = 3.65 kPa (banda NPT30 2–6 kPa, T 80–100 C, no fundir a 113.7 C).
- Caudal 35 μg/s por capilar PTFE, no joya sónica de 55 μm (se tapa).
- 316 agujeros, pitch 1.50 mm, τ=0.49, perveance 0.10 (subperveance, optica limpia).
- P_RF lab = 22 W fwd para Ib=16 mA. 40 W era desperdicio (2200 eV/ion).
- Neutralizador proto1 = filamento W aguas abajo, fuera del vapor de I2.
- Lineas 110 C > tanque. Apagado: tanque frio, lineas calientes.

## Materiales
OK: Al2O3, BN, grafito, PTFE, FFKM, W (filamento), Ni/Hastelloy si hace falta metal.
NO: Al, Cu, laton, acero al carbono, Mo como grid de I2 sin ensayo propio.
Cu de bobina y anillo solo bajo PTFE/ALD continuo.

## Banco
Camara con liner + cold trap I2. No ventear I2 a la turbo. N2 seco al abrir.
Secuencia de 10 pasos en `MEI-RIT_proto1_BOM.xlsx` hoja secuencia_banco.

## Coste proto lab
BOM min-max ~4.4–15 k€ de hardware (sin camara de vacio ni personal).
Campaña halogen-safe + grids custom empuja 15–40 k€.
54–97 k€ del pack v2.0 = estudio + cupones + margen, no PPU espacial.

## No realizable aun
Masa 220 g sistema. η 36–46 % medida. Lifetime grids. Claim 1 con periodo μm. Dual-band.
