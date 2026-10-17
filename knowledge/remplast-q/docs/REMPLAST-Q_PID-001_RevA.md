> Texto extraído automáticamente del PDF original «REMPLAST-Q_PID-001_RevA.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1bXHdzafvPFBFQ4rlTM2EvB1E0Yc6uD1e/view?usp=drivesdk



REMPLAST-Q   P&ID-001   Rev. A   2026-09-04 Hoja 1/2  ·  Diagrama de proceso e instrumentación

Autor del concepto: Lázaro López Paz  ·  Dibujo original REMPLAST-Q  ·  No es plano visado Caudal de diseño 5 m³/h  ·  UF 25 m²  ·  Retorno a EDAR

Leyenda de líneas

Proceso / alimento Permeado pulido Retenido / concentrado CIP / químico Señal / sidestream analítico

EDAR — EFLUENTE 2°

Derivación DN50/80
Titular: operador EDAR

LÍMITE DE BATERÍA
 Q=5 m³/h FE
101
 TK-101

Homogenización
1,5 m³  agitación suave
LE-101  TE-101

AE
101

pH / T / nivel
 F-101

Desbaste 1–2 mm
autolimpiante
PDI-101
 F-102

Cartucho 200–500 µm
PDI-102  recambio
 P-101

Alimentación
5 m³/h  VFD
2 bar  316/inox

SC
101
10–80 mL/min

SE-201 CELDA ÓPTICA

Imagen + scatter 405/532
Nile Red SOLO sidestream
NO retorna a proceso AE
201

Residuo tinción → gestor
 alimento UF

PT
301 M-301  UF CERÁMICA

Al₂O₃ o SiC  50–100 nm
25 m²  cross-flow
2,5–3,5 m/s   TMP 0,4–1,0 bar
PT-301/302/303   FE-302
 P-301

Recirc. 8–15 m³/h
VFD cross-flow

perm. 4,5 m³/h

FE
302
 AE
301

NTU
 RETORNO EDAR

Cabecera/efluente
V-401 fail-close

retenido 0,5 m³/h

TK-401 RETENIDO

0,4 m³ espesado
LE-401
20–80 L/d pasta
 BANCO D

Filtros plata
FTIR/Raman
fuera de línea
 R-501 PETASA

5 L  55–68 °C pH 8
LCC-ICCG inmov.
NO a efluente EDAR

TK-601  CIP

200 L  NaOH / HNO₃ / CEB
6 kW  TE-601
Nunca cruza con E
 CIP a M-301
 PLC-701  /  SCADA

S7-1200 o equiv.
Interlocks: TMP alta, nivel bajo,
puerta láser, T reactor
Historiador 1 s P/Q

Notas de diseño (Rev. A)

1. El PLC tiene autoridad exclusiva sobre actuadores. Ningún modelo ML ni servicio en la nube abre una válvula.
2. Nile Red y enzima no se dosifican al efluente ni al retorno. Sidestream SE-201 y efluente de R-501 van a residuo gestionado.
3. V-401 (retorno) y V-101 (alimento) cierran en fallo de red o de comunicación. La EDAR permanece aislada.
4. Este P&ID es un diagrama de I+D original del proyecto REMPLAST-Q. No copia planos de terceros. No sustituye ingeniería visada.
5. Revisión A — 4 septiembre 2026 — Lázaro López Paz. Si un tercero ejecuta el dibujo, citar a Lázaro López Paz y a Grok.

REMPLAST-Q   P&ID-001   Rev. A Hoja 2/2  ·  Señales, interlocks y válvulas

Lázaro López Paz  ·  Lista de I/O original del piloto 5 m³/h 2026-09-04

Lista de señales (mínimo de campaña)

Tag Tipo Descripción Rango / equipo Uso
FE-101 AI Caudal alimento DN50 mag. 0–8 m³/h
FE-302 AI Caudal permeado DN40 mag. 0–8 m³/h
PT-101 AI P descarga P-101 0–4 bar Alarma 3 bar
PT-301 AI P alimento UF 0–4 bar TMP = PT-301−PT-303
PT-302 AI P retenido UF 0–4 bar
PT-303 AI P permeado UF 0–4 bar
PDI-101 AI ΔP F-101 0–2 bar Cambio malla
PDI-102 AI ΔP F-102 0–2 bar Cambio cartucho
LE-101 AI Nivel TK-101 ultrasónico Marcha P-101
LE-401 AI Nivel TK-401 hidrostático Alto → parar reciclo
TE-101 AI T alimento PT100 Corrección J20
TE-501 AI T R-501 PT100 Corte >72 °C
AE-101 AI pH alimento 0–14 Registro
AE-301 AI Turbidez permeado 0–20 NTU Alarma 5 NTU
AE-201 DI/ETH Conteo SE-201 PC industrial Soft-sensor
AE-501 AI pH R-501 0–14 pH-stat
SC-101 AO VFD P-101 4–20 mA Caudal consigna
SC-301 AO VFD P-301 4–20 mA Vel. tangencial
YS-201 DI Interlock láser puerta SE-201 Corte emisión

Interlocks (el PLC los ejecuta sin consultar modelos)

ID Condición Acción Motivo

I-01 LE-101 bajo Para P-101 y cierra V-101 Evitar cavitación

I-02 TMP > 1,3 bar o dTMP/dt alto Backwash; si persiste, para M-301 Integridad / fouling

I-03 AE-301 > 5 NTU 10 min Alarma; no cierra retorno solo Calidad permeado

I-04 Puerta SE-201 abierta Corta láseres 405/532 Seguridad óptica

I-05 TE-501 > 72 °C o pH < 6,5 Para calef. R-501 Enzima / operador

I-06 Seta / fallo de red Cierra V-101 y V-401; bombas off Aislar EDAR

I-07 Comms PLC perdidas > 8 s Mismo que I-06 (fail-safe) No control remoto ciego

I-08 LE-401 muy alto Para P-301 reciclo de retenido Rebose

Válvulas críticas

Tag Servicio Fallo Nota

V-101 Alimento desde EDAR FC fail-close Aislamiento batería

V-401 Retorno permeado a EDAR FC fail-close Aislamiento batería

V-301 Entrada UF FO en marcha Proceso

V-302 Salida retenido Modulante / on-off Recuperación

V-303 Permeado On-off Proceso

V-304 Backwash inverso On-off Limpieza

V-601 CIP hacia M-301 Interlock con V-401 cerrado No CIP al río

V-501 Drenaje R-501 a residuo Manual+auto Nunca a EDAR

Rev. A  ·  Dibujo y lista de I/O originales  ·  No reproducen P&ID comerciales ni figuras publicadas.
