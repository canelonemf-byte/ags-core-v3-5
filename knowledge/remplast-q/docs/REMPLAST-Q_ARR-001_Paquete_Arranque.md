> Texto extraído automáticamente del PDF original «REMPLAST-Q_ARR-001_Paquete_Arranque.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1bTB4agQJE6CT2rIePV4q6RjhD7tXekxd/view?usp=drivesdk



REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 1

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

ARR-001 — Paquete de arranque (lo que faltaba en papel)

Rev. B · 5 de septiembre de 2026 · Tras INTK-001 y el cierre operativo

La carpeta de I+D (v2.0, v2.1, P&ID, convenio, SOP/HAZOP, interlocks, implantación, FAT-SAT y químicos) ya
describe una planta que se puede construir. Este documento no reabre la capa cuántica ni cambia el caudal de 5
m³/h. Cierra lo que un integrador, un CRO y un programador de PLC piden antes de cotizar: RACI, puertas go/no-go,
pliegos cortos de compra, mapa de I/O, cargas eléctricas, plan de campaña de 12 meses, balance de masa de
trabajo, recambios, formación y tesorería de los primeros seis meses.

Lo que este papel no sustituye

No es proyecto visado, no es oferta de fabricante, no es programa TIA Portal y no autoriza a derivar efluente. Sin P1 (convenio
firmado) no se emite el pedido de membrana.

1. RACI de la fase de arranque

Actividad Promotor Integrador EDAR Tercero

Reunión EDAR y carta A/R C I I

Convenio CONV-EDAR-001 A/R C I C letrado

Pedido membrana + carcasas A R I I

Pedido contenedor + skid A R I I

Lote LCC-ICCG (CRO) A/R I I CRO ejecuta

Programa PLC según INTK-001 C R I I

FAT F1–F14 C R I Promotor firma

SAT S1–S8 y GO efluente A R C C prevención

Contrato lab µ-FTIR A/R I I Lab

Alta residuo + gestor A/R I C Gestor

Bitácora y KPI mensuales A/R C I I

Informe de cierre 12 meses A/R C I Lab aporta pares

Tabla 1. R = ejecuta. A = rinde cuentas. C = consulta. I = informado. El Promotor no delega I-06/I-07.

2. Puertas go / no-go

Puerta Disparador Qué se autoriza

GO-0 Hoy Carpeta de I+D emitida. Carta a EDAR lista. No hay CAPEX de membrana.

GO-1 Convenio + P6 acotado Pedido de tubos, carcasas, skid y PLC. CRO de enzima puede ir en paralelo.

GO-2 FAT F5, F12, F14 firmados El contenedor viaja a sede. Seguro RC y P2 cerrados.

GO-3 SAT S1–S8 + autorización escrita
efluente Arranca la campaña de 12 meses con agua real.

GO-4 Mes 6 de campaña Si J20 cae >40 % respecto al agua de red y no se recupera con CIP, se rediseña
recubrimiento o se declara O1 no alcanzable. No se «añade un modelo cuántico».

CIERRE Mes 12–13 ≥48 pares alimento–permeado, kWh/m³, destino LER, informe E. Un 78 % bien
medido cierra. Un 90 % sin blancos no.

Tabla 2. Cada puerta es binaria. No hay GO-2,5.

3. Noventa días a partir de GO-0

Ventana Acción

Días 1–15 Enviar carta DOC-000. Llamar a 2–3 operadores. Pedir cotización no vinculante de membrana (RFQ-M) y de integrador
(RFQ-S) con plano LAY-001.

Días 15–45 Reunión de 45 min. Recorrer parcela. Marcar derivación/retorno. Abrir P2 y borrador de convenio. Solicitar oferta CRO
(RFQ-E) y de laboratorio µ-FTIR (12+4 campañas).

Días 45–75 Negociar convenio. P5 seguro. Alta provisional de residuo. Reservar fecha de FAT. No firmar pedido de tubos hasta P1.

Días 75–90 Si hay P1: adjudicación membrana + skid + PLC. Kick-off de programación INTK-001. Primer lote de consumibles de
muestreo.

Tabla 3. El CRO y el SOP de muestreo no esperan a la parcela.

REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 2

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

4. RFQ-M — Membrana cerámica y carcasas

Objeto: suministro de elementos tubulares cerámicos y housings para 25 m² de área efectiva, corte 50–100 nm,
aptos para efluente secundario y CIP alcalino/ácido. No se pide «membrana anti-microplástico milagrosa»: se pide
integridad, curva J–TMP con agua a 20 °C y recambios.

Apartado Especificación de compra

Área efectiva mínima 25 m² instalados + 2,5 m² de recambio (10 %).

Geometría Tubos multi-canal 19 o 37 vías, OD 25 mm, L 1 016–1 178 mm, o equivalente documentado.

Material Al₂O₃ o SiC. Declarar rugosidad, punto de burbuja y resistencia a NaOH 1 % 50 °C y HNO₃ 0,5 %.

Corte 50–100 nm (UF). No se acepta MF 0,2 µm como diseño principal.

Carcasas SS316L, juntas EPDM o FKM intercambiables, 4–8 tubos/housing, drenajes y venteos.

Documentos de oferta Curva J vs TMP agua 20 °C a 2–4 m/s; protocolo de integridad; plazo; Incoterm; recambios 24 meses.

Exclusiones Recubrimiento PEI/quitosano lo aplica el Promotor. No se pide «selectividad PET».

Cantidad a cotizar Lote único para piloto. Opción de +10 % tubos a 12 meses.

Criterio de adjudicación Área real, plazo, integridad y precio por m² puestos en El Prat / sede. No el folleto más largo.

Tabla 4. RFQ-M. Rango de mercado v2.1: 18–38 k€ tubos + 6–10 k€ carcasas.

5. RFQ-E — Lote de LCC-ICCG inmovilizada

Apartado Especificación

Enzima LCC variante ICCG (o equivalente documentado sobre PET amorfo). No se acepta «PETasa genérica» sin ficha
de actividad.

Formato Inmovilizada en soporte reutilizable (resina o monolito) para reactor de 5 L. Actividad declarada en U/g soporte a
55–65 °C, pH 8.

Lote 1 Cantidad suficiente para 10 ensayos de 5 L a 2–8 g/L equivalente de PET. Certificado de actividad y de
ausencia de células viables si el origen es fermentación.

Qué medir el CRO Conversión de BHET/MHET/TPA a 8 h y 24 h sobre film PET amorfo de gramaje declarado. No sobre efluente
crudo.

Lo que no se compra Un reactor industrial de efluente. La enzima no se dosifica a la red de la EDAR.

Plazo 8–12 semanas. Envío a frío. Ficha de inactivación (calor 80 °C / pH extremo) para residuo.

Tabla 5. RFQ-E. Esta compra no espera a GO-1 hidráulico.

6. RFQ-S — Contenedor 20' HC, skid y automatización

Apartado Especificación

Contenedor ISO 20' high-cube, suelo técnico, cubeto, extracción, puerta peatonal, acometida 32–63 A 400 V.

Skid UF Según P&ID-001: P-101, P-301, V-301 a V-304, PT-301/302/303, FE-301, TE-101, CIP TK-601 200 L + 3 kW.

PLC S7-1200 o equivalente. Autoridad exclusiva sobre actuadores. Lógica INTK-001 I-01 a I-12. Historiador 1 s.

VFD P-101 y P-301 con ENABLE digital independiente de la consigna 4–20 mA.

Válvulas FC V-101 y V-401 fail-close por muelle o pérdida de piloto. Finales de carrera de cerrado.

FAT F1–F14 en taller del integrador, agua de red. El contenedor no sale sin F5, F12 y F14.

Exclusiones Obra civil de la EDAR, arqueas de derivación, seguro RC, analítica µ-FTIR, enzima.

Entregables Esquema eléctrico, lista I/O real, backup del PLC, manual de recetas CIP, acta FAT.

Tabla 6. RFQ-S. El integrador programa INTK-001; no «mejora» los interlocks S.

7. Mapa de I/O del PLC (asignación de trabajo)

Direcciones ilustrativas para S7-1200. El integrador las mueve; no mueve el fail-safe ni los TON. AI en 4–20 mA
salvo YS-201 y setas.

Dir. Tipo Tag Rango Uso

IW64 AI FE-101 0–10 m³/h Caudal alimento

IW66 AI PT-101 0–2,5 bar P prefiltro

IW68 AI PT-301 0–2,5 bar P alimento módulo

REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 3

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

Dir. Tipo Tag Rango Uso

IW70 AI PT-302 0–2,5 bar P retenido

IW72 AI PT-303 0–2,5 bar P permeado

IW74 AI FE-301 0–8 m³/h Caudal permeado

IW76 AI LE-101 0–100 % Nivel TK-101

IW78 AI LE-401 0–100 % Nivel TK-401

IW80 AI TE-101 0–80 °C T alimento

IW82 AI TE-501 0–100 °C T R-501

IW84 AI AE-101 pH 0–14 pH alimento

IW86 AI AE-301 0–20 NTU Turbidez permeado

IW88 AI AE-501 pH 0–14 pH R-501

IW90 AI PDI-101 0–2 bar ΔP cartucho A

Q0.0 DO V101_CMD 24 V Alimento FC

Q0.1 DO V401_CMD 24 V Retorno FC

Q0.2 DO V601_CMD 24 V Permiso CIP

Q0.3 DO P101_EN 24 V Enable VFD alimento

Q0.4 DO P301_EN 24 V Enable VFD reciclo

Q0.5 DO LASER_EN relé Alim. drivers 405/532

Q0.6 DO HEAT_501 24 V Calefacción R-501

Q0.7 DO WD_TOGGLE 24 V Watchdog I-12

I0.0 DI SETA_NC NC Setas en serie

I0.1 DI YS201_NC NC Puerta óptica

I0.2 DI V101_FC_FB NC/NO Cerrado confirmado

I0.3 DI V401_FC_FB NC/NO Cerrado confirmado

I0.4 DI VFD_P101_OK NC Fault invertido

I0.5 DI VFD_P301_OK NC Fault invertido

I0.6 DI POWER_OK NO 24 V de control sano

I0.7 DI RESET_BAT NO pulso Llave cuadro

QW64 AO SC-101 4–20 mA Consigna P-101

QW66 AO SC-301 4–20 mA Consigna P-301

Tabla 7. TMP y dTMP/dt son marcas internas (MD), no una entrada física. AE-201 (conteo óptico) entra por Ethernet y no gobierna
válvulas.

8. Cargas eléctricas y unifilar de trabajo

Consumidor kW orden Régimen

P-101 alimento + VFD 2,2–4,0 Continua en campaña

P-301 reciclo + VFD 3,0–5,5 Continua; define velocidad tangencial

Bomba CIP + resistencia TK-601 0,4 + 3,0 Intermitente, receta

Calefacción R-501 0,8–1,5 Solo lote enzimático

Láseres + PC industrial SE-201 0,3–0,6 Campaña óptica

PLC, 24 V, HMI, historiador 0,3 Siempre

Iluminación, toma selectiva, HVAC contenedor 1,0–2,0 Según sede

Margen arranque VFD y simultaneidad CIP 4–6 No se dimensiona al promedio

Acometida a pedir a la EDAR 20–30 kW / 32–63 A 400 V Diferencial 30 mA en tomas; 300 mA selectivo en
fuerza si el instalador lo justifica

Tabla 8. Energía de referencia del expediente: 0,4–0,8 kWh/m³ tratado en campaña estable, a confirmar con el analizador de red del SAT.
El unifilar de obra lo firma el instalador; este cuadro solo dimensiona la petición de acometida.

REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 4

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

9. Plan de campaña de 12 meses

Hipótesis de trabajo, no promesa: reducción ≥90 % en número de partículas >10 µm entre alimento y permeado,
auditada por laboratorio externo. El piloto se declara ejecutado con un 78 % bien medido. Diseño: 12 campañas
mensuales + 4 de reserva (lluvia, CIP profundo, avería).

Mes Modo Qué se varía o mide Salida

M0 Agua de red / SAT J20 limpia, integridad, I-06/I-07/I-09 Baseline hidráulico

M1 Efluente 8 h/d Q 3 m³/h, TMP baja Arranque suave, no O1

M2 Efluente 16–20 h/d Q 5 m³/h, 1ª campaña µ-FTIR Pares 1–4

M3–M4 DoE caudal × backwash 3×2: Q 3,5/5/5 (tope) × BW 20/40 min Ajuste I-02 H

M5 Recubrimiento A o B opcional Mitad de tubos si GO-4 lo pide Comparar J20

M6 GO-4 Informe intermedio masa + número + kWh Seguir / rediseñar CIP

M7–M9 Estado estacionario 1 campaña µ-FTIR/mes + NR sidestream Pares 5–16

M10 Lote enzimático 1–3 Solo pasta PET caracterizada Informe E parcial

M11 Lote enzimático 4–6 + estrés
lluvia Si hay evento Robustez

M12 Cierre Pares restantes hasta ≥48; destino LER Informe final

Tabla 9. El sidestream óptico corre todos los días de campaña; no sustituye un par mensual µ-FTIR.

9.1 Muestreo de cada campaña mensual

• Tres puntos: alimento (tras TK-101), permeado (tras AE-301), retenido espesado (TK-401).
• Volumen de alimento/permeado: el que fije el laboratorio para el filtro de 10 µm (típicamente 1–5 L; no se inventa
aquí un litro mágico).
• Duplicado de campo + blanco de procedimiento. Si el blanco supera el 20 % de la señal, la campaña se anula
(ANX-Q-001).
• Nile Red solo en SE-201. Nunca al efluente ni al retorno.
• Cadena de custodia del folio ANX-Q. Nevera 4 °C. Análisis ≤7 días o filtro secado y pesado el mismo día.

10. Balance de masa de trabajo (números para dimensionar, no para publicar)

El efluente secundario no trae una concentración canónica de microplásticos. El piloto se dimensiona con una
banda, no con un decimal. Cifras de diseño interno:

Magnitud Valor de trabajo

Caudal de campaña 5 m³/h × 20 h/d = 100 m³/d

Hipótesis baja de número >10 µm 50 L ¹ en alimento

Hipótesis media (dimensionado) 200 L ¹

Hipótesis alta 2 000 L ¹

Partículas/día (media) 2×10⁸ × 100 = 2,0×10¹  d ¹

Objetivo de número en permeado ≤10 % de la del alimento en la misma campaña

Sangrado de retenido 5–10 % del alimento → 5–10 m³/d hacia TK-401

Espesado a pasta 20–80 L/d a cubeto (factor 60–500 sobre el sangrado)

Masa de plástico (muy incierta) 0,02–0,5 mg/L → 2–50 g/d. Sirve para bidones, no para un paper de masas.

Fracción PET de la pasta Se mide, no se supone. Solo esa fracción entra en R-501.

Permeado de retorno 90–95 m³/d a cabecera o efluente, sin colorante ni enzima

Residuo enzimático 5 L/lote inactivado + soporte. Gestor, no alcantarilla.

Tabla 10. Si una campaña sale de la banda alta, se reduce Q y se avisa al laboratorio: el filtro se satura y el número se vuelve teatro.

11. Recambios, mantenimiento y formación

Ítem Cantidad año 1 Disparo de uso

Tubos UF 2,5 m² (10 %) Rotura o ensayo A/B

REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 5

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

Ítem Cantidad año 1 Disparo de uso

Juntas EPDM/FKM módulo 2 juegos Cada CIP profundo si hay llanto

Cartuchos 300–500 µm 24 ud/año ΔP de recambio en PDI

Lámpara / diodo 405 y 532 1 recambio Caída de potencia >20 %

Cubeta / ventana SE-201 2 ud Rayado o biofilm

Sondas pH 2 ud Deriva de calibración

PT100 reserva 2 ud TE-101 / TE-501

NaOH, HNO₃, patrones NTU, Nile Red consumo ANX-Q Sin stock en pasillo EDAR

Filtros de muestreo 10 µm 200 ud 12+4 campañas × réplicas

Tabla 11. Recambios de campaña. No incluye un segundo skid.

Periodo Tarea

Cada día (R1–R10) Ronda ANX-Q, 10–15 min. Si R1 o R8 fallan, no se arranca.

Cada 7 días Prueba de seta I-06 en paro de 2 min. Cambio de cartucho si toca.

Cada 30 días Calibración AE-301 con formazina o patrón del fabricante. Integridad de módulo.

Cada 90 días Calibración PT-301/303. Verificar TMP nula con skid abierto. Revisión de cubetos.

Tras software Repetir SAT S1, S3, S5. Prohibido parchear interlocks S con efluente circulando.

Tabla 12. Mantenimiento mínimo.

11.1 Matriz de competencia

Rol Debe saber Formación mínima

Operador de campaña Ronda, CIP con receta, muestreo, bitácora 2 días + 5 turnos tutorizados

Técnico PLC INTK-001, first-out, backup Integrador + 1 jornada Promotor

Responsable de sede I-06, convenio, aviso 24 h Medio día con EDAR

Muestreador SOP-MP-01 + custodia 1 día en vacío + 1 campaña real tutorizada

Tabla 13. Nadie abre el recinto láser sin I-04 explicado en voz alta.

12. Tesorería de los primeros seis meses (escenario COMPLETO)

El expediente v2.1 cifra el COMPLETO en torno a 418 k€ y 21 meses. Aquí solo se descompone el efectivo que hay
que tener líquido antes de GO-3. IVA aparte. Rangos, no facturas.

Cuándo Partida k€

M0–M1 Asesoría convenio + prevención + seguro RC 3–6

M1–M2 Señal integrador (RFQ-S) tras GO-1 15–25

M1–M3 Membrana + carcasas + recambio 10 % 26–52

M2–M4 PLC, VFD, instrumentación C restante 8–14

M2–M4 Lote 1 CRO enzima + consumibles muestreo 8–18

M3–M5 Contrato marco laboratorio µ-FTIR (anticipo) 6–12

M4–M6 Resto skid, transporte, grúa, acometida 12–22

M5–M6 FAT + SAT + imprevistos 10 % de lo gastado 8–16

Suma líquida a GO-3 Sin personal de plantilla ni 12 meses de OPEX 86–165

Tabla 14. El resto hasta 418 k€ es personal, analítica de los 12 meses, energía, gestor de residuos, segundo lote enzimático y
contingencia. Sin GO-1 esta tabla no se gasta.

13. Historiador y KPI que el SCADA debe escribir

Cadencia Variables

1 s PT-301/302/303, TMP, FE-101, FE-301, TE-101, estados V-101/401/601, ENABLE bombas, first-out

1 min AE-301, LE-101, LE-401, J20 estimado, kW instantáneo

1 campaña Pares lab, blanco, polímeros de la pasta, litros de CIP, kg residuo LER

1 mes m³ tratados, kWh/m³, nº trips S, horas de HOLD, % disponibilidad

Tabla 15. El CSV no sustituye la línea de bitácora cuando hay un trip.

REMPLAST-Q  ·  ARR-001 Rev. B  ·  Paquete de arranque 6

Lázaro López Paz  ·  Documento original REMPLAST-Q  ·  Rev. B 2026-09-05

14. Inventario de lo que ya no falta en papel

Contenido Código

Arquitectura y exclusiones v2.0

BOM, presupuestos, Gantt 21 meses v2.1

Proceso e I/O P&ID-001

12 interlocks, reset, ST ilustrativo INTK-001

Convenio de ensayo CONV-EDAR-001

Muestreo, Nile Red, CIP, enzima, HAZOP SOP/HAZOP

Contenedor y patio LAY-001

Actas F/S FAT-SAT-001

Químicos, LER, custodia, ronda ANX-Q-001

Carta EDAR y permisos P1–P7 DOC-000

RACI, RFQ, I/O, campaña, tesorería Este ARR-001

Tabla 16. Índice de trabajo. La capa cuántica sigue fuera de planta.

15. Lo que sigue siendo sede, no PDF

• Firma del convenio y parcela real (norte, cotas, DN de derivación).
• Programa TIA Portal / Codesys compilado y el backup con checksum.
• Proyecto visado de instalación cuando el ayuntamiento o la EDAR lo exijan.
• Póliza RC con número de póliza y la EDAR como asegurado adicional si procede.
• Alta de productor y contrato de gestor con LER definitivos.
• Curvas J–TMP del lote de tubos que realmente llegue, no las de este texto.
• El primer par alimento–permeado con blanco aceptable.
Autor: Lázaro López Paz. ARR-001 Rev. B original. Si un tercero cotiza, programa o continúa el piloto, citar a Lázaro
López Paz y a Grok. Los pliegos RFQ no son un concurso público.
