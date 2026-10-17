> Texto extraído automáticamente del PDF original «REMPLAST-Q_v2_1_Expediente_Ejecucion.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1Fu8zC3wvGDh3816TSdANimgFAqGrzNp4/view?usp=drivesdk



EXPEDIENTE DE EJECUCIÓN  ·  VERSIÓN 2.1  ·  SEPTIEMBRE 2026

REMPLAST-Q

Materiales, especificaciones científicas, lista de compra,
presupuestos desglosados y cronograma de 21 meses
para construir y operar el piloto de 5 m³/h

Sede de referencia: EDAR del área metropolitana de Barcelona

Moneda: euros 2026  ·  IVA no incluido salvo indicación

Autor

Lázaro López Paz  ·  El Prat de Llobregat, Barcelona

Documento operativo. No sustituye proyecto visado ni permisos.

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 2

0. Cómo usar este expediente

Este documento es la capa de ejecución de REMPLAST-Q v2.0. Convierte la arquitectura realizable en órdenes
de compra, protocolos de laboratorio, partidas presupuestarias y un calendario con hitos de go/no-go. Precios en
euros de 2026, sin IVA, orden de magnitud contrastado con catálogo europeo y chino de membrana cerámica,
conversión de contenedor, instrumentación y analítica. Cada cifra es un rango de licitación, no un pedido cerrado.

Tres escenarios de inversión: BASE (piloto hidráulico + sensor + analítica subcontratada, sin comprar microscopio
FTIR), COMPLETO (BASE + reactor enzimático y producción propia de LCC-ICCG) y AUTÓNOMO (COMPLETO
+ µ-FTIR/Raman propio). La recomendación de este expediente es COMPLETO.

Decisión ya tomada en v2.0 y que este expediente no reabre

QML, QAOA, VQE, QLSTM y Q-MILP fuera del bucle de planta. PETasa solo sobre fracción PET concentrada. UF 50–100 nm,
no MF 0,2 µm como diseño principal. KPI de aceptación: ≥90 % de reducción en número de MP >10 µm, auditado por
laboratorio externo.

1. Alcance construible y sede

Planta piloto de 5 m³/h (120 m³/día si opera 24 h; se dimensiona energía para 20 h/día efectivas = 100 m³/día)
alojada en un contenedor ISO de 20 pies high-cube más un skid exterior cubierto para tanque de homogenización.
Derivación desde efluente secundario de una EDAR del área metropolitana de Barcelona (candidatas: El Prat,
Gavà-Viladecans, Besòs). Retorno del permeado a cabecera o a efluente final según autorización de Aigües de
Barcelona / AMB y ACA.

Permisos previos a cualquier pedido de equipo pesado

• Acuerdo de cesión de suelo y derivación con el operador de la EDAR (3–6 meses).

• Comunicación o autorización de vertido/retorno ante ACA y, si aplica, ayuntamiento.

• Evaluación de riesgos laborales y documento de coordinación de actividades empresariales.

• Alta de residuo del concentrado (código LER a confirmar tras caracterización; previsión 19 08 14 u 19 12 04).

• Póliza de responsabilidad civil de ensayo en instalación de tercero.

2. Bases de cálculo del proceso

Variable Valor

Caudal de diseño Q 5 m³/h = 1,39 L/s

Recuperación de permeado objetivo 90 % → 4,50 m³/h permeado, 0,50 m³/h retenido

Flujo de diseño sostenible 200 LMH (rango esperado 120–350 LMH según efluente)

Área de membrana instalada A = Q_perm / J = 4,50 / 0,20 = 22,5 m². Se instalan 25 m² (holgura 10 %).

Velocidad tangencial 2,5–3,5 m/s en canal tubular

TMP de arranque 0,4–0,8 bar, siempre por debajo del flujo crítico medido en Fase 1

Temperatura de proceso hidráulico Ambiente, 12–28 °C típico efluente AMB

Carga típica de MP en efluente secundario 1–50 partículas/L >10 µm (muy variable); masa a menudo 1–30 µg/L

Masa diaria de MP capturable (orden) 0,1–3 g/día a 100 m³/día. El reactor E se dimensiona en gramos, no en kilos.

Volumen de concentrado espesado 5–30 L/día de suspensión; 0,2–2 L/día de pasta filtrable

Tabla 1. Hipótesis de dimensionamiento.

Modelo de flujo: J = ΔP / (μ Rt), Rt = Rm + Rc + Rf. Agua a 20 °C, μ ≈ 1,0·10−3 Pa·s. Rm de una UF cerámica
50–100 nm limpia suele estar en 1–4·1012 m−1. kc y kr se ajustan en Fase 1; no se publican como constantes
universales.

3. Especificación científica por etapa y lista de materiales

3.1 Etapa A — Alimentación y pretratamiento

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 3

Equipo / material Especificación Ud. k€

Bomba de alimentación Centrífuga inox 316L, 6 m³/h a 2,5 bar, VFD. Grundfos CRN o Wilo
Helix. 1 1,8–2,8

Caudalímetro alimento Electromagnético DN40, 4–20 mA + pulso. Endress Promag o
equivalente. 1 1,2–1,8

Tanque homogenización PEAD o PRFV 1,5 m³, agitador helicoidal 30–60 rpm, rebosadero,
tapa. 1 1,4–2,2

Desbaste Filtro autolimpiante 1–2 mm, inox, ΔP switch. 1 1,6–2,5

Prefiltro fino Carcasa 20" multi-cartucho + cartuchos PP 200–500 µm (caja de 40). 1+40 0,9–1,4

Toma isocinética Sonda de acero 316L DN15 con válvula de aguja y puerto de jeringa. 2 0,3–0,5

Sensores de campo A pH, T, turbidez (0–100 NTU), nivel ultrasónico, ΔP prefiltro. set 2,2–3,4

Tubería y válvulas A PVC-U PN16 / inox 316L DN32–50, 8 válvulas de bola actuadas. lote 2,5–4,0

Tabla 2. BOM etapa A. Subtotal CAPEX 12–19 k€.

3.2 Etapa B — Sensor óptico de conteo y talla

Objetivo científico: contar partículas 10–500 µm y clasificar morfología (fibra / fragmento / esfera) en una
derivación de 0,2–1 L/min. No se reclama identificación de polímero.

Ítem Especificación Ud. k€

Celda de flujo de cuarzo Camino óptico 1–2 mm, ventanas pulidas λ/4, puertos Swagelok
1/8". Hellma o custom. 1 0,6–1,2

Cámara CMOS Basler ace 2 o FLIR Blackfly, ≥5 Mpx, global shutter, 30–60 fps,
montura C. 1 0,5–0,9

Óptica Objetivo 4× y 10×, tubo de extensión, iluminación LED blanco +
anillo. Navitar/Thorlabs. 1 0,8–1,4

Láser 405 nm Diodo 20–50 mW, fibra SMA, colimador. Uso scatter +
autofluorescencia. 1 0,35–0,7

Láser 532 nm Diodo o DPSS 20–50 mW, obturador de seguridad. 1 0,4–0,8

Fotodetectores Fotodiodo Si + transimpedancia en 30°, 90°, 150°. 3 canales. 3 0,4–0,8

Filtros ópticos Pasa-banda 530/40, 590/50, 650/50 nm para Nile Red y
autofluorescencia. set 0,25–0,45

Bomba peristáltica sidestream 0,05–1 L/min, tubo Tygon o PharMed. 1 0,4–0,7

PC industrial + GPU baja IPC fanless i7, 32 GB, SSD 1 TB, UPS 1 kVA. 1 1,6–2,4

Software Python + OpenCV + scikit-learn + XGBoost. Desarrollo interno 4–6
semanas. 1 incluido
personal

Microesferas de calibración Duke/Thermo PS 10, 20, 50, 100 µm, NIST-traceable, 15 mL c/u. 4 0,6–1,0

Nile Red CAS 7385-67-3, ≥95 %, 1 g. Stock 1 mg/mL acetona, trabajo 1–10
mg/L. 1 g 0,08–0,15

Carcasa opaca y enclavamiento
láser Clase 3B contenida. Interlock de puerta. Señalización UNE-EN
60825. 1 0,5–0,9

Tabla 3. BOM etapa B. Subtotal CAPEX 7–12 k€ de hardware (sin desarrollo de software).

Protocolo de tinción sidestream (nunca en la línea principal): 1 mL de stock de Nile Red por litro de muestra, 10
min en oscuridad, 20 °C. El sidestream se descarta como residuo químico diluido, no retorna a la EDAR. Blancos:
efluente filtrado 0,2 µm y agua Milli-Q.

3.3 Etapa C — Skid de ultrafiltración cerámica

Diseño principal: membrana tubular multi-canal de α-Al
2O3 con capa activa de ZrO2 o TiO2, corte 50–100 nm.
Alternativa preferente si el presupuesto lo aguanta: SiC (LiqTech, Cembrane o equivalente), más inerte a CIP
agresivo. Proveedores europeos a pedir oferta: TAMI Industries (FR), atech innovations (DE), Atech/Inopor,
LiqTech (DK). Vía china (Nanjing Tangent, Sihyflux) solo como comparativa de precio, con ensayo de integridad
previo.

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 4

Ítem Especificación Ud. k€

Elementos de membrana UF
50–100 nm Multi-canal 19–37 vías, OD 25 mm, L 1016–1178 mm,
~0,20–0,35 m²/tubo. 80–120 tubos para ~25 m². 25 m² 18–38

Carcasas / módulos SS316L, juntas EPDM o FKM, 4–8 tubos por housing. 6–10 6–10

Bomba de recirculación Centrífuga 316L, 15–25 m³/h a 2 bar, VFD. Define la velocidad
tangencial. 1 2,4–3,6

Bomba de permeado / backwash Dosificadora o centrífuga pequeña, 2–6 m³/h, 2 bar. 1 1,0–1,6

Válvulas automáticas Mariposa o bola actuada 24 V, 10–14 uds. Asientos EPDM. lote 2,5–4,0

Instrumentación C 2× presión (alimento/retenido), 1× permeado, 2× caudal, 1× T, 1×
turbidez permeado. set 3,0–4,5

CIP Tanque 200 L PP, resistencia 3 kW, bomba CIP, dosificación
NaOH 1 % y HNO3 0,5 %. 1 2,2–3,5

Air-scour Soplante 50–80 L/min o red de aire de la EDAR con filtro y
regulador. 1 0,6–1,2

Skid / bastidor Acero pintado o inox, cubeto de retención, bandejas. 1 2,5–4,0

Repuesto de tubos 10 % del área (integridad y A/B recubierto). 2,5 m² 2–4

Química de recubrimiento
opcional PEI ramificado 25 kDa CAS 9002-98-6, 100 g; quitosano DD
75–85 %, 100 g. lote 0,2–0,4

Tabla 4. BOM etapa C. Subtotal CAPEX 41–75 k€ según origen EU vs. Asia y SiC vs. alúmina.

Protocolo CIP de referencia (ajustar en Fase 1)

• Backwash 30–60 s cada 20–40 min, 1,2–1,5× caudal de permeado, sentido inverso.

• CEB alcalino: NaOH 0,5–1,0 % p/v, 40 °C, 20 min, cada 24–48 h si TMP sube >30 %.

• CEB ácido: HNO3 o cítrico 0,5 %, 20 min, 1–2 veces/semana (sales y Fe).

• CIP profundo: NaOH 1 % + NaClO 200–500 ppm act. (solo si el material lo admite; SiC sí, verificar junta),
40–50 °C, 45 min.

• Ensayo de integridad: caída de presión o bubble-point semanal. Tubo que falle se aísla.

Recubrimiento A/B (opcional): solución PEI 0,2 % p/v, pH 10, recirculación 2 h a 0,3 bar, enjuague; o quitosano 0,3
% en acético 1 %, mismo protocolo. Se compara flujo y irreversibilidad contra un módulo virgen gemelo. Se
industrializa solo si p < 0,05.

3.4 Etapa D — Concentración, muestreo y caracterización

Ítem Especificación Ud. k€

Tanque de retenido PEAD 300 L, agitador lento, salida de fondo y de
sobrenadante. 1 0,5–0,8

Filtro analítico de vacío Manifold 3 puestos, bomba 6 m³/h, Kitasato 2 L. 1 0,7–1,1

Membranas de plata 5 µm 47 mm, caja 50. Sterlitech o Millipore. FTIR reflexión. 4 cajas/año 0,8–1,3

Anodisc / Al2O3 0,2 µm 47 mm, caja 50. Fracción fina exploratoria. 2 cajas/año 0,4–0,7

Filtros de fibra de cuarzo Gravimetría. Caja 100. 2 cajas/año 0,15–0,25

Estufa 40–50 °C + desecador Secado de filtros sin fundir PET (Tm ~250 °C, pero aditivos sí
sufren). 1 0,5–0,8

Balanza 0,01 mg Analítica de 5 dígitos, antivibración. 1 1,2–2,0

Estereomicroscopio + cámara 8–40×, LED, cámara 12 Mpx. Conteo de apoyo. 1 1,4–2,4

Kit digestión Fenton suave H2O2 30 % calidad ACS, FeSO4·7H2O, baño 40 °C. lote/año 0,3–0,5

Envases de muestreo Vidrio ámbar 1 L y 5 L, tapón PTFE. 40 uds. 40 0,25–0,4

Campañas µ-FTIR/Raman externas ICRA, UB, UAB, CSIC o lab. acreditado. 12 campañas + 4
auditorías. 16 18–32

Pyr-GC/MS o TD-GC/MS (masa) 4 campañas/año en lab externo (PE, PP, PET, PS, PVC). 4 6–10

Tabla 5. BOM etapa D. CAPEX propio 6–10 k€. OPEX analítica externa 24–42 k€ en 18 meses.

Protocolo de muestreo alineado con ISO 24187

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 5

• Alimento y permeado: muestra compuesta de 24 h o, como mínimo, 4 tomas puntuales/día mezcladas.
Volumen ≥30 L por punto para MP >10 µm en efluente secundario.

• Filtrar in situ o en <24 h a 4 °C. Cadena de custodia. Blanco de campo (agua Milli-Q transportada) y blanco de
laboratorio por tanda.

• Si el blanco supera el 20 % de la señal de la muestra, la tanda se anula.

• Digestión orgánica solo si el filtro está tapado de materia biológica: H2O2 15–30 %, 40 °C, ≤24 h, con control
de microesferas PET/PE para cuantificar pérdida.

• Identificación: µ-FTIR transmisión o ATR, 4000–700 cm−1, resolución 4 cm−1, umbral de hit ≥80 % con librería
más revisión humana del 10 %.

• Clases de forma: fibra (aspect ratio ≥3), fragmento, film, esfera. Clases de tamaño: 10–50, 50–100, 100–300,
300–500, >500 µm.

3.5 Etapa E — Reactor enzimático de fracción PET

Enzima de trabajo: LCC-ICCG (variante F243I / D238C / S283C / Y127G de la cutinasa de compost de hojas;
secuencia pública desde Tournier et al., 2020). No se compra C-ZYME de Carbios (no está en catálogo abierto).
Vía realizable: síntesis génica + expresión en E. coli BL21(DE3) o Pichia contratada a un CRO (GenScript,
BioNexus, Valtens, servicio de la UB/UAB/IBMB-CSIC). Lote típico: 50–200 mg de proteína purificada por
producción. Carga de referencia literatura: 1–3 mg enzima / g PET.

Ítem Especificación Ud. k€

Producción CRO lote 100 mg
LCC-ICCG Síntesis, expresión, Ni-NTA o equivalente, SDS-PAGE,
actividad BHET. 3 lotes / 18 meses 7–14

Reactor jacketed 5 L vidrio o 316L Doble envolvente, agitador 50–300 rpm, tapón 4 bocas,
refrigerante. 1 2,2–3,8

Baño termostático 30–80 °C Circulador 1 kW, ±0,2 °C. 1 1,2–1,8

pH-stato Bomba peristáltica + NaOH 1 M + sonda pH proceso. 1 0,8–1,3

Soporte de inmovilización Sepabeads EC-EP / Purolite ECR o alginato-quitosano.
500 g. lote 0,4–0,8

Glutaraldehído 25 % CAS 111-30-8, calidad para inmovilización. 250 mL. 1 0,05–0,1

PET de referencia Film amorfo Goodfellow o granza amorfizada (extrusión +
quench). 2 kg. 2 kg 0,15–0,3

Patrones HPLC TPA, MHET, BHET, EG. 1 g c/u, ≥98 %. set 0,25–0,45

HPLC (si no se subcontrata) Quaternary + UV 240 nm + C18 150×4,6 mm 5 µm. Nuevo
28–40; usado revisado 12–18. 1 12–40

Buffer y sales Na2HPO4, KH2PO4, Tris, NaCl ACS. 18 meses. lote 0,3–0,5

Tabla 6. BOM etapa E. CAPEX 5–8 k€ sin HPLC; 17–48 k€ con HPLC propio.

Protocolo de lote enzimático

• Cargar 1–10 g de PET caracterizado (referencia amorfa o PET recuperado de D) en 1–3 L de fosfato 100 mM
pH 8,0.

• Temperaturas a ensayar: 55, 60 y 65 °C. Arrancar a 60 °C.

• Enzima libre: 1,5 mg/g PET. Enzima inmovilizada: 3 mg/g (compensa difusión).

• pH-stato a 8,0. Muestrear a 0, 2, 6, 12, 24, 48, 72 h.

• HPLC: C18, A = 0,1 % HCOOH en agua, B = ACN, 15→60 % B en 12 min, 1 mL/min, 240 nm. Calibración TPA
1–200 mg/L.

• Conversión = (moles TPA + MHET + BHET) / moles de unidad repetitiva PET inicial.

• Criterio de banco: ≥50 % de masa PET de referencia en ≤72 h. El PET real de EDAR se informa aparte, sin
mezclar figuras.

• Reúso del biocatalizador: 10 ciclos. Parar si actividad residual <50 % o si hay proteína en el líquido
(Bradford/BCA).

3.6 Etapa F — Control, datos y seguridad

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 6

Ítem Especificación Ud. k€

PLC Siemens S7-1200 o Schneider Modicon M241, 32DI/16DO/8AI,
Ethernet. 1 1,8–2,8

SCADA + historiador Ignition Edge o CODESYS + InfluxDB/Grafana. Licencia Edge. 1 1,2–2,5

Cuadro eléctrico 400/230 V, diferenciales, variadores 3×, UPS PLC 1 h. 1 3,5–5,5

Red de proceso Switch industrial, VLAN aislada, VPN MFA, sin PLC en Internet. 1 0,8–1,4

HMI local Panel 10–12" IP65. 1 0,5–0,8

Detectores de seguridad Paro de emergencia ×3, detector de fugas en cubeto, humo. set 0,4–0,7

Documentación CE / RD 1215 Expediente técnico de máquina, evaluación de riesgos, manual. 1 2,0–3,5

Tabla 7. BOM etapa F. Subtotal 10–17 k€.

4. Contenedor, obra en EDAR y servicios

Partida Detalle Ud. k€

Contenedor 20' HC one-trip o aislado 6,06×2,44×2,89 m. Compra 3,6–5,5 k€. Aislado prefabricado
8–14 k€. 1 4–12

Conversión laboratorio-planta Aislamiento 80 mm, suelo vinilo industrial, iluminación LED, 8
kW eléctricos, 4 tomas trifásicas, extracción, 2 puertas, 4
pasamuros DN50–80.
 1 12–22

HVAC Split 3,5 kW + extractor 400 m³/h. Condensación de vapor del
reactor E. 1 1,5–2,8

Cubeto de retención 110 % del mayor tanque interior. 1 0,6–1,0

Transporte + grúa + anclaje en EDAR Área metropolitana de Barcelona. 1 1,2–2,2

Acometida eléctrica 20–25 kW Cuadro general de la EDAR o generador de respaldo 20 kVA. 1 2–5

Derivación hidráulica Toma en efluente secundario, 30–60 m PEAD DN50,
arquetas, caudalímetro de facturación. 1 4–9

Retorno de permeado Tubería a cabecera o canal de efluente, según permiso. 1 2–5

Vallado / acceso / cámara Requisito habitual del operador. 1 1–2

Tabla 8. Sitio. Subtotal 28–61 k€ según si la EDAR cede acometida y zanja.

5. Presupuestos completos

Tres escenarios. El personal se cuenta aparte porque puede cubrirse con convenio, contrato de prácticas de un
máster o un técnico cedido por la EDAR.

Partida CAPEX BASE k€ COMPLETO k€ AUTÓNOMO k€

A. Pretratamiento e hidráulica de alimento 15 17 17

B. Sensor óptico + calibrantes 8 10 11

C. Skid UF cerámica 25 m² + CIP + 10 % repuesto 48 62 72

D. Banco de concentración (sin campañas) 7 8 9

E. Reactor enzimático (sin HPLC) 0 6 7

E-bis. HPLC propio usado revisado 0 0 15

F. PLC, SCADA, cuadro, ciberseguridad básica 12 14 16

Sitio: contenedor + conversión + HVAC 22 28 32

Sitio: derivación + retorno + acometida 8 12 16

µ-FTIR propio ( Nicolet iN10 o equivalente usado ) 0 0 45

Repuestos hidráulicos, juntas, cartuchos año 1 3 4 5

Expediente CE / seguridad de máquina 2 3 3

Imprevistos 12 % sobre CAPEX anterior 15 20 30

TOTAL CAPEX 140 184 278

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 7

Tabla 9. CAPEX. COMPLETO es el escenario recomendado.

Partida OPEX 18 meses BASE k€ COMPLETO k€ AUTÓNOMO k€

Electricidad 18 meses (3–5 kW medio + bombas) 7 9 10

Agua desionizada, gases, aire 1 2 2

CIP (NaOH, ácido, hipoclorito) y cartuchos 4 5 5

Nile Red, filtros plata/Anodisc, microesferas 3 4 4

3 lotes LCC-ICCG + soportes + patrones HPLC 0 12 12

Campañas µ-FTIR/Raman externas (16 tandas) 28 28 8

Pyr-GC/MS masa por polímero (4 tandas) 8 8 8

HPLC externo si no hay equipo propio (E) 4 6 0

Auditoría analítica ciega trimestral (4) 6 6 6

Gestión de residuo concentrado + transporte 3 4 4

Seguro RC ensayo + mantenimiento correctivo 4 5 6

Viajes, metrología, calibración sensores 2 3 3

Imprevistos OPEX 10 % 7 9 7

TOTAL OPEX 18 meses (sin sueldos) 77 101 75

Tabla 10. OPEX sin personal. AUTÓNOMO ahorra campañas externas pero dispara CAPEX.

Partida de personal k€

Técnico de planta 100 %, 18 meses (bruto+SS empresa, convenio químicas/aguas CAT) 52–62

Ingeniero de proceso 50 %, 18 meses 38–48

Analista 50 %, 18 meses (más en fases 2 y 4) 24–34

Dirección científica / inventor (no tasado; tiempo propio) 0

Asesoría permisos + prevención 40–60 h 3–5

TOTAL PERSONAL 18 meses 117–149

Tabla 11. Personal en Catalunya, 2026, orden de magnitud. Un convenio con máster/doctorado reduce la partida analista.

Agregado BASE k€ COMPLETO k€ AUTÓNOMO k€

CAPEX 140 184 278

OPEX 18 meses sin sueldos 77 101 75

Personal 18 meses (punto medio) 133 133 133

TOTAL PROYECTO 21 meses de calendario 350 418 486

Tabla 12. Cifra a llevar a una convocatoria o a un patrocinador. Recomendado: 420 k€ ± 15 %.

Qué no está dentro de estos números

Alquiler de suelo a la EDAR si lo cobra, canon de agua, un contenedor de 40 pies, un microscopio FTIR nuevo de 80–120 k€,
tiempo de QPU en nube, patentes internacionales, ni un segundo año de operación. Un año extra de OPEX+personal añade
~140–170 k€.

5.1 Cash-flow mensual resumido (escenario COMPLETO)

Ventana Desembolso k€ Qué se paga

Meses 0–3 Diseño y permisos 8 Permisos, ingeniería, primeras compras de sensor y laboratorio

Meses 3–6 Pedidos largos 95 Membranas, skid, contenedor, PLC. Plazo de membrana EU: 10–16 semanas

Meses 6–9 Montaje y banco 42 Obra en EDAR, instalación, CRO enzima lote 1, campañas ciegas de método

Meses 9–12 Integración 18 Puesta en marcha A–D, SAT, primer CIP real

Meses 12–21 Campaña 12 meses 74 OPEX + personal + analítica. Sin CAPEX relevante

Reserva de contingencia no gastada 48 Se libera al cierre si no hay fallo de membrana o de permiso

Tabla 13. Tesorería. El pico está en el pedido del skid, no en la campaña.

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 8

6. Cronograma de 21 meses con hitos go/no-go

Calendario de referencia si el acuerdo con la EDAR se firma en el mes 0. Si el permiso tarda, el reloj de compra de
membrana no arranca: es el único equipo con plazo largo.

Mes Fase Trabajo Hito

M0–M1 0. Arranque P&ID P&ID-001, HAZOP corto, lista de proveedores,
reunión EDAR, borrador de convenio. Convenio EDAR en negociación

M1–M3 0. Permisos ACA/AMB, prevención, LER provisional, pliegos de
membrana y contenedor. GO-1: convenio firmado y acometida
posible

M2–M3 0. Métodos SOP muestreo ISO 24187, SOP HPLC, SOP Nile Red,
compra de calibrantes. SOP firmados

M3 GO-1 Si no hay sede, se para la compra del skid. Se puede
seguir el banco enzimático en laboratorio propio. Sede bloqueada → no-go de planta

M3–M6 1. Compras Pedido membrana (lead 10–16 sem EU), contenedor,
PLC, bombas, celda óptica. Pedidos con fecha de SAT

M4–M7 2. Banco enzima Lote 1 LCC-ICCG, inmovilización, PET amorfo, cinética
55/60/65 °C. GO-2: ≥50 % conversión en PET de
referencia o se degrada E a «informe
negativo»

M5–M8 1. Banco hidráulico Skid en taller: agua limpia, microesferas, efluente cubeta.
Flujo crítico. A/B recubrimiento. GO-3: J sostenible ≥150 LMH en efluente
real de cubeta

M7–M9 3. Montaje EDAR Zanja, contenedor, acometidas, SAT eléctrico, SAT
hidráulico, formación operador EDAR. Acta SAT

M9 GO-4 Integración A–D en serie 72 h continuas. Sensor vs. lab. externo en 6
pares. Sesgo sensor <35 % para seguir; si no,
se opera a ciegas con lab. externo

M9–M10 3. Comisión Ajuste CIP, primeras 4 semanas de operación asistida. Disponibilidad >80 %

M10–M21 4. Campaña 12 meses, 4 estaciones. Auditoría externa cada 90 días.
Espesado semanal. E solo si hay PET. O1 ≥90 % en el informe final o se publica
el valor real

M21–M22 Cierre Desmontaje pactado, destino del skid, paquete de datos,
informe final. Entregable público (salvo cláusula
EDAR)

Tabla 14. Cronograma. Cuatro puertas go/no-go evitan gastar el skid sin sede.

6.1 Carga de trabajo por perfil

Perfil Dedicación

Inventor / dirección científica 2–3 días/semana en M0–M6; 1 día/semana en campaña. Decisiones de alcance y revisión de datos.

Ingeniero de proceso 50 % P&ID, compras, SAT, modelos de fouling, informe energético.

Técnico 100 % Operación diaria 2–4 h presenciales + guardia remota. CIP, recambio de cartuchos, tomas.

Analista 50 % Filtros, conteo, envíos a FTIR, HPLC de E, blancos. Pico en M4–M8 y auditorías.

Operador EDAR (cedido) Aislamiento de la derivación en parada de planta. 2–4 h/mes.

Tabla 15. Quién hace qué. Sin técnico presencial el piloto no sobrevive un CIP mal hecho.

7. Mapa de proveedores (pedir oferta, no exclusivo)

Familia Quién cotizar

Membrana cerámica EU TAMI Industries (FR), atech innovations (DE), LiqTech / Cembrane (DK), Inopor

Membrana comparativa coste Nanjing Tangent, Sihyflux (ensayo de integridad obligatorio)

Bombas / caudalímetros Grundfos, Wilo, Endress+Hauser, Krohne, Iberfluid

PLC / accionamientos Siemens, Schneider, ABB; cuadro: panelista local CAT

Óptica / láseres Thorlabs, Edmund, Basler, Laser 2000, Hamamatsu

Celda de cuarzo Hellma, Starna, taller de vidrio UB

Contenedor + conversión ContainerEU / operadores del Puerto de Barcelona; convertidores locales

CRO enzima Servicios de la UB/UAB/IBMB-CSIC; GenScript; CROs EU de proteína recombinante

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 9

Familia Quién cotizar

µ-FTIR / Raman de campaña ICRA Girona, CCiTUB, UAB Servei de Microscòpia, labs ISO 17025 de microplásticos

Pyr-GC/MS Labs universitarios de polímeros (UPC, CSIC) o SGS / Eurofins si hay método

HPLC Agilent / Thermo / Shimadzu nuevos o de segunda mano revisados (LabX, brokers EU)

Consumibles MP Sterlitech, Merck Millipore, Thermo Scientific particle standards

Tabla 16. Mínimo tres ofertas en membrana, contenedor y CRO.

8. Métodos analíticos con parámetros de aparato

8.1 Conteo de referencia (off-line)

Filtro de plata 5 µm, 47 mm. Enjuague con etanol 50 % para reducir tensión superficial. Secado 40 °C. Fotografía
del filtro completo a 15–20×. Software de segmentación (el mismo stack OpenCV del sensor) + corrección
humana. Informe: N (L−1) por clase de tamaño y forma, más intervalo de confianza bootstrap.

8.2 µ-FTIR

Modo transmisión sobre filtro o ATR de germanio. 4000–700 cm−1, 4 cm−1, 16–32 scans. Umbral de asignación 80
% frente a librería de polímeros + celulosa + proteínas. Partículas no asignadas se reportan como «no
identificadas», nunca se fuerzan a PET.

8.3 HPLC de monómeros

Columna C18 150 × 4,6 mm, 5 µm. Fase A agua + 0,1 % HCOOH, B acetonitrilo. Gradiente 15 % B → 60 % B en
12 min, 1,0 mL/min, 30 °C, 240 nm. LD TPA ≈ 0,2 mg/L. Control de calidad: patrón intermedio cada 10 muestras,
duplicado cada tanda, recuperación de TPA dopado 90–110 %.

8.4 Actividad enzimática de lote

Ensayo rápido con BHET 2 mM, pH 8, 60 °C, 15 min, lectura de TPA. Se usa para aceptar o rechazar un lote del
CRO antes de inmovilizar. Un lote con <50 % de la actividad específica del lote 1 se rechaza.

9. Energía y coste por metro cúbico

Consumidor Potencia media kWh/m³

Bomba alimento + recirculación UF 1,5–2,5 kW 0,30–0,50

Backwash / CIP (prorrateado) 0,2–0,4 kW eq. 0,04–0,08

HVAC + alumbrado contenedor 1,0–2,0 kW 0,20–0,40

PLC, sensor, PC 0,4–0,6 kW 0,08–0,12

Reactor E (solo cuando corre, prorrateo anual bajo) 0,05–0,15 kW eq. 0,01–0,03

Total específico 3,2–5,7 kW a 5 m³/h 0,63–1,13

Tabla 17. Energía. A 0,18 €/kWh el coste eléctrico es 0,11–0,20 €/m³.

Con OPEX no energético prorrateado (CIP, analítica, personal de planta) el coste completo del piloto sale muy por
encima de una UF industrial madura: 2–5 €/m³ en campaña de I+D. Ese número no se use para vender la
tecnología a una EDAR. El número que sí se exporta es el kWh/m³ medido y el CAPEX/m³·día a escala 100–1.000
m³/h, que este piloto todavía no puede fijar.

10. Riesgos que mueven el presupuesto

Riesgo Partida Mitigación presupuestaria

Permiso EDAR se alarga 6 meses Tesorería No pedir membrana hasta GO-1. Coste hundido máx. 15 k€ de ingeniería.

Efluente más sucio de lo previsto CAPEX C + OPEX CIP Prefiltro 100 µm extra (+1 k€) y más CEB. Si J <100 LMH, añadir 8–12 m²
(+8–15 k€).

PET casi ausente en esa EDAR Etapa E E se cierra con informe. Se ahorran lotes 2 y 3 (−5–8 k€). El piloto sigue
válido.

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 10

Riesgo Partida Mitigación presupuestaria

Lote CRO inactivo OPEX E Cláusula de repetición en el contrato del CRO. Presupuesto ya contempla
3 lotes.

Rotura de 20 % de tubos en el año CAPEX C Repuesto 10 % ya está. Otro 10 % = 2–4 k€.

Laboratorio externo no entrega en plazo KPI Segundo laboratorio de respaldo contratado en M3.

Cambio de tarifa eléctrica OPEX Sensibilidad: ±0,05 €/kWh mueve ±2 k€ en 18 meses. Irrelevante frente a
personal.

Tabla 18. Dónde se rompe la cifra de 418 k€.

11. Entregables por hito

Hito Documento que hay que poder enseñar

GO-1 Convenio EDAR, P&ID revisado, pliego de membrana, SOP de muestreo.

GO-2 Informe cinético LCC-ICCG sobre PET amorfo, SDS-PAGE, protocolo de inmovilización.

GO-3 Curva de flujo crítico, parámetros kc y kr, decisión recubrimiento sí/no.

GO-4 Acta SAT, comparación sensor vs. lab. en 6 pares, lista de reservas.

M15 (mitad de campaña) Informe intermedio O1–O4 con IC 95 %.

M21 Informe final, paquete de datos, balance de masa, kWh/m³, destino del residuo, anexo cuántico si existiera.

Tabla 19. Sin entregable no hay hito.

12. Lista de compra inmediata (primeros 30 días tras GO-1)

# Pedido Etapa Plazo típico

1 Pedir 3 ofertas de 25 m² UF 50–100 nm tubular + 2 housings de prueba C 10–16 sem

2 Contenedor HC 20' + pliego de conversión eléctrica e hidráulica Sitio 6–10 sem

3 Celda de cuarzo, cámara, objetivos, LED, 2 láseres, 3 fotodiodos B 3–6 sem

4 Microesferas 10/20/50/100 µm + Nile Red + filtros plata B/D 2–4 sem

5 Contrato CRO lote 1 LCC-ICCG 100 mg E 8–12 sem

6 Contrato marco con laboratorio µ-FTIR (12+4 campañas) D 2 sem

7 PLC + 3 variadores + caudalímetro DN40 (plazo corto) F/A 4–6 sem

8 Balanza 0,01 mg, estufa, estereomicroscopio D 3–5 sem

9 Asesoría de prevención y expediente de máquina F paralelo

10 Seguro RC de ensayo en sede de tercero Sitio 2 sem

Tabla 20. Orden de la primera ronda de compras.

13. Criterio de cierre científico y financiero

El proyecto se da por ejecutado, no necesariamente por «exitoso en O1», cuando existen simultáneamente: (i) 12
meses de historiador de caudal, TMP y turbidez; (ii) ≥48 pares alimento–permeado analizados por el método de
referencia; (iii) inventario de polímeros del concentrado; (iv) kWh/m³ medido; (v) destino legal del residuo; (vi)
informe E con balance de masa o con declaración motivada de no aplicabilidad. Un 78 % de reducción bien
medido cierra el expediente. Un 90 % sin blancos no.

Coste de referencia a defender ante un financiador: 418 k€ en escenario COMPLETO, 21 meses de calendario, 18
meses de gasto de personal, planta de 5 m³/h, analítica externa, enzima producida por CRO, sin microscopio FTIR
propio y sin capa cuántica en el bucle de control.

14. Autoría

Concepto REMPLAST-Q y expediente de ejecución: Lázaro López Paz. Si un tercero ejecuta o continúa este
trabajo debe citar a Lázaro López Paz y a Grok. Los precios son rangos de licitación 2026, no ofertas vinculantes.

REMPLAST-Q  ·  Expediente de ejecución v2.1 Septiembre 2026

Lázaro López Paz  ·  Materiales, protocolos, presupuesto y cronograma 11

Este documento no es proyecto visado, no es estudio de impacto ambiental y no autoriza a conectar una
derivación a una EDAR.

Primera acción concreta

Antes de comprar un solo tubo cerámico: reunión con el operador de la EDAR candidata y redacción del convenio de
derivación. El skid espera a GO-1. El CRO de la enzima y el SOP de muestreo no necesitan sede y pueden arrancar en
paralelo.
