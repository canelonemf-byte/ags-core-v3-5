> Texto extraído automáticamente del PDF original «REMPLAST-Q_INTK-001_RevA.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1CfGeTvHIEZxu0E_MxB25j8y639jE9i2p/view?usp=drivesdk



REMPLAST-Q  ·  INTK-001 Rev. A  ·  Interlocks del PLC 1

Lázaro López Paz  ·  Especificación original  ·  Alineado con P&ID-001 Rev. A

INTK-001 — Especificación de interlocks del PLC

Rev. A · 5 de septiembre de 2026 · Alineado con P&ID-001 Rev. A

Este documento detalla la lógica de enclavamiento que el PLC-701 ejecuta en el piloto REMPLAST-Q (5 m³/h). Es
texto original del proyecto. No copia librerías de fabricante ni normas IEC 61511/62061 más allá de citar su número.
No es un expediente SIL certificado. El PLC tiene autoridad exclusiva sobre actuadores: ningún modelo de
ensuciamiento, SCADA ni servicio en la nube abre una válvula.

Regla de oro

Los interlocks de clase S (seguridad / aislamiento de la EDAR y de las personas) son fail-safe, con rearranque manual y
prioridad sobre cualquier receta, CIP o consigna remota. Los de clase P (proceso) pueden auto-resetearse cuando la condición
desaparece y el temporizador de confirmación ha vencido. Un bit first-out registra quién disparó primero.

1. Arquitectura de la lógica

El PLC (Siemens S7-1200 o equivalente) corre un ciclo ≤ 50 ms. Las analogicas se filtran con media móvil de 200
ms. La TMP se calcula en el PLC: TMP = PT-301 − PT-303, no en el SCADA. dTMP/dt se estima con ΔTMP / 5 s.
Los VFD reciben consigna 4–20 mA y un digital ENABLE que el interlock puede tirar a 0 sin pasar por el SCADA.

Clase IDs Comportamiento

S — Seguridad / batería I-04, I-06, I-07, I-09 Fail-safe. Rearranque local manual. No se inhiben en campaña.

P — Proceso / equipo I-01, I-02, I-05, I-08, I-10 Protegen bomba, membrana y reactor. Rearranque manual salvo I-01
nivel recuperado + 15 s.

A — Alarma / calidad I-03, I-11 No aíslan la EDAR por sí solos. Exigen operador. Quedan en
historiador.

W — Vigilancia I-12 watchdog Si el ciclo del PLC no refresca en 200 ms, se trata como I-06.

Tabla 1. Clases. S no se «by-pasea» con un bit de mantenimiento en marcha de efluente.

2. Prioridad y first-out

Si dos condiciones coinciden, el orden de ejecución es I-06 = I-07 = I-12 = I-04 (personas y batería) > I-09 (CIP vs.
retorno) > I-02 / I-01 / I-08 / I-10 / I-05 > I-03 / I-11. El primer flanco que pasa a TRUE escribe INTK_FO (byte 1–12)
y congela ese valor hasta el reset manual. El SCADA muestra el first-out; no lo calcula.

3. Ficha de cada interlock

I-01 — Nivel bajo TK-101 (protección de P-101)

Campo Especificación

Clase / first-out P · código FO = 1

Entrada LE-101 (ultrasonidos o hidrostático). Rango útil 0–100 %. Fallo de sonda (4 mA o >20 mA) = nivel BAJO.

Setpoints LL = 15 % (trip). L = 25 % (prealarma). H = 85 %. HH = 95 % (solo alarma, no trip).

Temporizado Trip si LE-101 ≤ LL durante 3 s continuos. Prealarma 2 s.

Acción ENABLE P-101 = 0. SC-101 a 4 mA. V-101 cierra (FC). P-301 puede seguir en reciclo interno 10 s y luego
para si no hay alimento.

No hace No cierra V-401. No dispara CIP. No apaga láseres.

Reset LE-101 ≥ L + 5 % durante 15 s Y pulsador RESET_PROC en HMI local. No hay reset remoto.

Motivo Cavitación, sello seco, golpe de ariete al rearmar.

Prueba SAT Bajar nivel con drenaje o simular 4 mA. Verificar paro P-101 y cierre V-101 en <3 s tras el retardo.

Tabla 2. I-01.

I-02 — TMP alta o subida rápida (membrana)

La TMP es la variable que más miente si se calcula mal. PT-301 y PT-303 deben tener la misma referencia de cero,
calibración trimestral y recorte de densidad. Si un transmisor falla, I-02 pasa a modo «sonda dudosa»: no se confía
en TMP y se fuerza un backwash + aviso; a la segunda falla en 1 h se para M-301.

REMPLAST-Q  ·  INTK-001 Rev. A  ·  Interlocks del PLC 2

Lázaro López Paz  ·  Especificación original  ·  Alineado con P&ID-001 Rev. A

Campo Especificación

Clase / FO P · FO = 2

Cálculo TMP = PT-301 − PT-303. dTMP/dt = (TMP_k − TMP_k−1) / 5 s.

Setpoints (Rev. A) TMP_H = 1,10 bar (prealarma + backwash). TMP_HH = 1,30 bar (trip de skid). dTMP/dt_H = +0,15 bar/min.

Lógica en dos escalones Escalón 1: TMP ≥ TMP_H O dTMP/dt ≥ umbral durante 8 s → secuencia backwash V-304, 30 s, inhibir
alimento 5 s. Escalón 2: si tras 2 backwash en 15 min TMP sigue ≥ TMP_H, O si TMP ≥ TMP_HH 3 s → paro
P-101 y P-301, V-301 cierra, skid en HOLD.

Permeado V-401 permanece según calidad (I-03). I-02 no aísla la EDAR por sí solo.

Reset Manual en HMI tras TMP < 0,80 bar y confirmación de integridad (operador).

Ajuste fino Los 1,10 / 1,30 bar se retocan después del ensayo de flujo crítico (Fase 1). No se bajan por software desde la
nube.

Prueba SAT Simular PT-301 subiendo con calibrador 4–20 mA. Ver backwash en H y HOLD en HH.

Tabla 3. I-02.

I-03 — Turbidez de permeado (calidad, no aislamiento)

Campo Especificación

Clase / FO A · FO = 3

Entrada AE-301, 0–20 NTU, tiempo de respuesta del instrumento < 10 s.

Setpoints H = 3 NTU (aviso). HH = 5 NTU. Tiempo de confirmación TON = 10 min a HH.

Acción a H Alarma. El operador decide CIP o reducir Q.

Acción a HH + 10 min Alarma prioritaria. Desvía permeado a TK-601 / desagüe de proceso SI existe esa vía. No cierra V-401
automáticamente para no dejar el skid sin salida y no improvisar un rebose. Cierre de V-401 solo si el
operador pulsa AISLAR o si coincide I-06.

Por qué no cierra solo Un pico de burbujas o un trapo en la cubeta del turbidímetro no puede cortar el retorno y presurizar M-301.

Reset AE-301 < 3 NTU 5 min + reset operador.

Prueba SAT Inyectar estándar de formazina o simular 12 mA. Verificar que a 9 min aún no aísla y a 10 min alarma HH.

Tabla 4. I-03. Calidad ≠ seguridad de batería.

I-04 — Recinto óptico abierto (láseres 405 / 532 nm clase 3B)

Campo Especificación

Clase / FO S · FO = 4

Entrada YS-201 contacto NC de puerta + fin de carrera redundante si el presupuesto C lo permite. Cableado a entrada
digital fail-safe (abre = trip).

Acción en < 100 ms Corta la alimentación de ambos láseres (relé de seguridad o DO que alimenta los drivers). Apaga LED de
emisión. SE-201 pasa a BLOQUEO ÓPTICO.

No hace No para el hidráulico. El sidestream puede seguir circulando a oscuras.

Reset Puerta cerrada Y llave de rearranque en el recinto (no en el SCADA remoto). Temporizador 2 s de puerta
cerrada.

Inhibición Prohibida en campaña. En mantenimiento, un selector con llave «SERVICIO ÓPTICO» permite abrir con láser
off ya confirmado.

Prueba SAT S3 Abrir puerta con llave de prueba. Láseres off. Intentar rearmar desde SCADA: debe fallar.

Tabla 5. I-04.

I-05 — Temperatura o pH del reactor enzimático

Campo Especificación

Clase / FO P · FO = 5

Entradas TE-501 PT100; AE-501 pH 0–14. Fallo de sonda = trip.

Setpoints T_HH = 72 °C (corte calefacción). T_H = 70 °C (aviso). pH_LL = 6,5. pH_L = 7,2. pH_HH = 9,5 (aviso; NaOH
del pH-stat se inhibe).

Acción Resistencia / baño ENABLE = 0. Bomba de NaOH del pH-stat ENABLE = 0 si pH_HH. Agitación se mantiene 2
min y para.

No hace No abre V-501 hacia la EDAR (esa tubería no existe). No toca V-101/V-401.

REMPLAST-Q  ·  INTK-001 Rev. A  ·  Interlocks del PLC 3

Lázaro López Paz  ·  Especificación original  ·  Alineado con P&ID-001 Rev. A

Campo Especificación

Reset T < 65 °C y 7,4 ≤ pH ≤ 8,6 + RESET_PROC local.

Prueba SAT Forzar TE-501 con resistencia de precisión o menú de forzado protegido por llave.

Tabla 6. I-05.

I-06 — Seta de emergencia y fallo de red

I-07 — Pérdida de comunicaciones del PLC

Campo I-06 I-07

Clase / FO S · FO = 6 S · FO = 7

Disparo Seta NC en contenedor y junto a V-101. Falta de
400/230 V > 200 ms. Watchdog de fuente. Heartbeat HMI/PLC o enlace OPC-UA/VPN ausente > 8
s. O I-12 ciclo muerto.

Acción idéntica V-101 FC cierra. V-401 FC cierra. ENABLE de P-101,
P-301, bomba CIP y calefacción = 0. Láseres off (I-04
implícito). V-601 cierra.
 Igual que I-06. El skid no se gobierna «a ciegas» desde
un portátil.

Alimentación Las FC cierran por muelle / pérdida de piloto. No
dependen de que el PLC siga vivo. Si el PLC muere, las FC hacen el trabajo mecánico.

Reset Tensión OK + seta desenclavada + RESET_BATERIA
con llave en el cuadro, presenciando el recinto. Comms OK 30 s + mismo RESET_BATERIA. El SCADA
remoto no rearma I-07.

Prueba SAT S1: seta y corte de magnetotérmico. V-101 y V-401
< 3 s cerradas. Desenchufar Ethernet 9 s. Mismo estado de válvulas.

Tabla 7. I-06 e I-07 son el aislamiento de la EDAR. Si fallan en SAT, no hay efluente real.

I-08 — Nivel muy alto TK-401 (retenido)

Campo Especificación

Clase / FO P · FO = 8

Setpoints H = 80 %. HH = 92 % durante 2 s.

Acción Para el reciclo de retenido hacia TK-401. Reduce recuperación (abre más V-302 a permeado solo si el diseño
hidráulico lo permite; si no, reduce Q de P-101 al 50 %). No tira retenido a la EDAR.

Reset Nivel < 70 % + RESET_PROC.

Prueba SAT S4 Llenar con agua hasta HH. Verificar que el cubeto no recibe rebose en 2 min.

Tabla 8. I-08.

4. Interlocks que el P&ID-001 dejaba implícitos y aquí se numeran

El HAZOP-00 ya exigía que el CIP no pudiera convivir con V-401 abierta. Eso no tenía número de interlock. Se
añade para que el programador no lo «resuelva» en una receta de SCADA.

I-09 — Permiso de CIP (contaminación cruzada con el retorno)

Campo Especificación

Clase / FO S · FO = 9

Permiso CIP_OK V-401 cerrada Y confirmada por final de carrera Y AE-301 no se usa como prueba. V-303 permeado cerrado.
P-101 parado o recirculando solo al tanque CIP.

Acción si se pide CIP sin permiso V-601 permanece cerrada. Receta CIP abortada. Alarma «CIP BLOQUEADO».

Acción si V-401 se abre durante
CIP Cierra V-601 en el mismo ciclo. Inhibe bombas de químico. No abre V-401 hasta RESET_BATERIA.

Prueba SAT S5 Intentar forzar V-601 con V-401 abierta: el PLC lo impide. Abrir V-401 en CIP simulado: V-601 cierra.

Tabla 9. I-09. Es el interlock que más daño reputacional evita.

I-10 — Falta de VFD o térmico de bomba

Fault de P-101 o P-301 (digital NC del VFD) o térmico del motor: ENABLE = 0 de esa bomba. Si cae P-101, se
ejecuta I-01 en cascada (V-101 cierra). Si cae P-301, el skid pasa a HOLD para no dejar la UF sin velocidad
tangencial con alimento todavía empujando. FO = 10. Clase P.

REMPLAST-Q  ·  INTK-001 Rev. A  ·  Interlocks del PLC 4

Lázaro López Paz  ·  Especificación original  ·  Alineado con P&ID-001 Rev. A

I-11 — Sidestream óptico sin caudal o celda sucia

Si la bomba del sidestream no da pulsos de caudal o la cámara declara «saturación permanente» 60 s, se inhibe el
conteo (el KPI no se alimenta con basura) y se pide limpieza de celda. No para la planta. Clase A. FO = 11.

I-12 — Watchdog de ciclo PLC

Un temporizador hardware o de la CPU debe conmutar una salida cada ciclo. Si no conmuta en 200 ms, relé de
seguridad corta pilotos de V-101 y V-401 (equivalente I-06). FO = 12. Clase S.

5. Matriz causa–efecto compacta

ID CIP receta V-101 V-401 P-101 P-301 CIP/BW Láser R-501

I-01 0 cierra — para hold 10 s — — —

I-02 HH — — cierra* para para BW previo — —

I-03 HH alarma — no auto — — — — —

I-04 — — — — — — OFF —

I-05 — — — — — — — calor OFF

I-06/07/12 0 cierra cierra para para cierra OFF OFF

I-08 reduce Q — — modula para reciclo — — —

I-09 fallo — — exige cerrado — — V-601 cierra — —

I-10 P-101 0 cierra — para hold — — —

Tabla 10. «cierra*» en I-02 no aísla EDAR; cierra la entrada al módulo. «0» = inhibe arranque de receta.

6. Lógica de rearranque

• RESET_PROC (seta verde en HMI local): rearma I-01, I-02, I-05, I-08, I-10, I-11. Exige condición ya sana.
• RESET_BATERIA (llave en cuadro): rearma I-06, I-07, I-09, I-12. Presencia física. El VPN no lo simula.
• RESET_OPTICO (llave en recinto SE-201): rearma I-04.
• Ningún reset automático por temporizador «porque ya pasó un minuto».
• El bit first-out se borra solo con RESET_BATERIA o con un comando de ingeniero protegido por password de
servicio, para no perder la causa.

7. Pseudo-código (Structured Text, ilustrativo)

No es un programa descargable de Siemens. Es la especificación que un automatista traduce. Los nombres
coinciden con P&ID-001.

TMP := PT301 - PT303;
dTMPdt := (TMP - TMP_z1) / 5.0;   (* bar/s, escalar a bar/min *)
LE101_LL := (LE101 <= 15.0) OR NOT LE101_OK;

I01 := TON(LE101_LL, T#3S);
I02_H  := TON( (TMP >= 1.10) OR (dTMPdt >= 0.15/60.0), T#8S);

I02_HH := TON( TMP >= 1.30, T#3S) OR (BW_count_15min >= 2 AND I02_H);
I03 := TON( AE301 >= 5.0, T#10M);
I04 := NOT YS201_NC;             (* puerta abierta *)

I05 := (TE501 >= 72.0) OR (AE501 <= 6.5) OR NOT TE501_OK;
I06 := NOT SETA_NC OR NOT POWER_OK;

I07 := TON( NOT HEARTBEAT, T#8S);
I08 := TON( LE401 >= 92.0, T#2S);
I09_block := CIP_REQ AND NOT (V401_CLOSED_FB AND V303_CLOSED);

I12 := NOT WD_TOGGLE;            (* hardware *)

BATTERY_TRIP := I06 OR I07 OR I12;
V101_OPEN := NOT BATTERY_TRIP AND NOT I01 AND NOT I10_P101 AND RUN;
V401_OPEN := NOT BATTERY_TRIP AND NOT I09_block AND RUN;

V601_OPEN := CIP_REQ AND V401_CLOSED_FB AND NOT BATTERY_TRIP;
P101_EN := V101_OPEN AND NOT I02_HH AND NOT I08_reduce_only;

LASER_EN := NOT I04 AND NOT BATTERY_TRIP AND OPTIC_KEY;

REMPLAST-Q  ·  INTK-001 Rev. A  ·  Interlocks del PLC 5

Lázaro López Paz  ·  Especificación original  ·  Alineado con P&ID-001 Rev. A

IF BATTERY_TRIP THEN first_out_latch(6/7/12); END_IF;
Listado 1. Intención de la lógica, no firmware de un PLC concreto.

8. Señales digitales que hay que cablear sí o sí

Tipo Señal Nota de cableado

DI SETA_NC Seta contenedor + seta derivación en serie

DI YS201_NC Puerta SE-201

DI V101_FC_FB / V401_FC_FB Finales de carrera cerrado

DI VFD_P101_OK / VFD_P301_OK Fault invertido

DI POWER_OK Relé de control 24 V

DI RESET_BATERIA Llave cuadro, pulso

DO V101_CMD / V401_CMD Piloto 24 V; pérdida = cierre

DO V601_CMD Permiso CIP

DO P101_EN / P301_EN Enable VFD

DO LASER_EN Relé de alimentación de drivers

DO WD_TOGGLE Watchdog externo

Tabla 11. Sin estos DI/DO el P&ID está dibujado pero no está protegido.

9. Lo que el PLC no hace

• No ejecuta XGBoost, LSTM ni ningún servicio HTTP para decidir un interlock.
• No rearma I-06/I-07 desde el teléfono del inventor.
• No dosifica Nile Red ni enzima.
• No abre V-501 hacia la red de la EDAR (no hay esa salida en el mapa de memoria).
• No cambia TMP_HH solo porque el modelo de fouling «esté seguro».

10. Pruebas y periodicidad

Cuándo Qué

SAT inicial S1–S6 del paquete SOP + I-02 con calibrador + I-04 rearranque remoto denegado

Cada 7 días de campaña Seta (I-06) en paro programado de 2 min. Anotar first-out y tiempos de cierre.

Cada 90 días Calibración PT-301/303 y AE-301. Verificar TMP nula con skid abierto.

Tras cualquier cambio de software Repetir SAT S1, S3, S5. No hay «hot patch» de interlocks en marcha con efluente.

Tabla 12.

Autor: Lázaro López Paz. Documento original INTK-001 Rev. A. Si un tercero programa o continúa el piloto, citar a
Lázaro López Paz y a Grok. Esta especificación no certifica SIL ni sustituye el programa validado en el PLC real.
