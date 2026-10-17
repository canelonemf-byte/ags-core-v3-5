> Texto extraído automáticamente del PDF original «REMPLAST-Q_SOP_HAZOP_RevA.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1Hfou8G2CNmD-m93LigdKYOHJ5jlrFtiq/view?usp=drivesdk



REMPLAST-Q  ·  Paquete SOP / HAZOP  ·  Rev. A  ·  2026-09-04 1

Procedimientos originales del proyecto  ·  Lázaro López Paz

PAQUETE DE PROCEDIMIENTOS Y HAZOP CORTO

SOP-MP-01 / SOP-NR-02 / SOP-CIP-03 / SOP-E-04 / HAZOP-00 · Rev. A · 2026-09-04

Originalidad

Estos procedimientos están escritos de nuevo para REMPLAST-Q. Se apoyan en principios de buenas prácticas de muestreo y
de seguridad industrial, y citan el número de la ISO 24187 solo como marco de referencia. No reproducen el texto de esa
norma, ni fichas de proveedor, ni artículos científicos. Quien ejecute el piloto debe comprar la norma oficial si necesita su
articulado.

SOP-MP-01 — Muestreo de alimento, permeado y concentrado

Objeto

Obtener muestras comparables de la derivación (alimento), del permeado y del retenido espesado para recuento
de partículas >10 µm y, en laboratorio, identificación de polímero. El sensor SE-201 no sustituye este SOP.

Material

• Bidones o frascos de vidrio o acero 5–10 L, tapón de PTFE o metal, precinto. No usar plástico nuevo sin blanco
de envase.
• Sonda de toma isocinética o derivación a la misma velocidad aproximada de la tubería.
• Nevera portátil 4 °C, cadena de custodia SOP-MP-01-CC, rotulador indeleble.
• Blanco de campo: agua Milli-Q transportada en el mismo tipo de envase.

Método

• Purgar la toma 30 s. Recoger compuesto de 24 h o, si no hay muestreador, 4 alícuotas iguales en 8–12 h.
Volumen objetivo ≥30 L por punto para efluente secundario.
• No filtrar en campo salvo que la turbidez impida el transporte; si se filtra, registrar el filtro y guardarlo.
• Etiqueta: fecha, hora inicio/fin, punto (ALIM / PERM / RET), operador, caudal instantáneo FE-101 o FE-302.
• Conservar ≤24 h a 4 °C. No congelar.
• En laboratorio: blanco de campo y blanco de sala. Si el blanco supera el 20 % de la señal de la muestra, anular
la tanda.
• Digestión con H₂O₂ 15–30 % a 40 °C solo si el filtro queda tapado de materia orgánica, y siempre con
microesferas de control para estimar pérdida.
• Clases de forma: fibra (relación de aspecto ≥3), fragmento, film, esfera. Clases de tamaño: 10–50, 50–100,
100–300, 300–500, >500 µm.
• Polímero: µ-FTIR o Raman, umbral de coincidencia ≥80 % y dos bandas diagnóstico, con revisión humana del
10 %.

SOP-NR-02 — Nile Red en sidestream (nunca en la línea)

• Stock 1,00 mg/mL en acetona HPLC, frasco ámbar, −20 °C, caducidad 3 meses. CAS 7385-67-3.
• Trabajo 10 µg/mL en Milli-Q, preparar el día de uso.
• Relación muestra:tinción 10:1 v/v. 10 min a 25 °C en oscuridad. Excitación 520–530 nm, emisión 560–640 nm.
• Cada lote: blanco de efluente filtrado 0,2 µm + control PE 50 µm teñido.
• El líquido teñido y la acetona van a bidón de disolventes. Prohibido devolverlos a TK-101, a M-301 o a la
EDAR.
• Interlock YS-201 activo antes de encender láseres.

SOP-CIP-03 — Limpieza de membrana

• Backwash: 20–40 s cada 20–40 min, 1,2–1,5 veces el caudal de permeado, V-401 permanece abierta al
retorno solo si el permeado de backwash cumple NTU; si no, desviar a TK-601.
• CIP alcalino: NaOH 0,5–1 % m/v, 45–55 °C, 30–45 min. CIP ácido: HNO₃ 0,3 % v/v, ~30 °C, 20 min. CEB:
50–100 ppm NaOCl, pH 10, 10 min, no a T alta sobre SiC.
• Antes de CIP: cerrar V-401. El CIP usado vuelve a TK-601 y se neutraliza antes de enviarlo al desagüe que la
EDAR haya escrito en el Anexo I.
• Disparar CIP cuando J20 caiga al 70 % del valor post-CIP anterior o TMP suba 0,3 bar. El modelo predictivo
solo propone; el operador o el PLC confirman.

REMPLAST-Q  ·  Paquete SOP / HAZOP  ·  Rev. A  ·  2026-09-04 2

Procedimientos originales del proyecto  ·  Lázaro López Paz

SOP-E-04 — Lote enzimático de fracción PET

• Solo entra PET confirmado por SOP-MP-01. PE, PP y «no plástico» no entran en R-501.
• Carga 1–10 g PET en 1–3 L de fosfato 100 mM pH 8,0. T de arranque 60 °C (ensayar 55 y 65 °C en banco).
• Enzima libre 1,5 mg/g PET; inmovilizada 3 mg/g. pH-stat a 8,0. Muestreo 0, 2, 6, 12, 24, 48, 72 h.
• HPLC C18, A = 0,1 % HCOOH en agua, B = acetonitrilo, 15→60 % B en 12 min, 1 mL/min, 240 nm.
• Conversión = (moles TPA+MHET+BHET) / moles de unidad repetitiva inicial. Cierre de masa 85–115 % o el
lote se declara no válido.
• El líquido de R-501 y las perlas van a residuo del Promotor. V-501 no tiene tubería hacia la EDAR.
• Parar si actividad residual <50 % o si hay proteína soluble por Bradford.

HAZOP-00 — Revisión corta previa al SAT

Nodo a nodo, desviaciones guía: más caudal, menos caudal, más presión, más temperatura, flujo inverso, fuga,
contaminación cruzada, fallo de señal. No sustituye un HAZOP formal si la EDAR o el asegurador lo exigen.

Nodo Desviación Consecuencia Safeguard Riesgo residual

Alimento V-101 Más Q Golpe a F-101 / UF FE-101 + VFD P-101 saturado Medio

Alimento Menos Q / vacío Cavita P-101 I-01 nivel bajo Bajo si I-01 prueba

UF M-301 Más TMP Compacta cake / rota junta I-02 backwash y paro Medio

UF CIP con V-401 abierta Químico a retorno EDAR Interlock V-601 / V-401 Alto si se anula

SE-201 Puerta abierta + láser Exposición ocular I-04 corte emisión Alto sin interlock

SE-201 Retorno de Nile Red Colorante a proceso Tubería a residuo, sin te Alto si se «improvisa»

TK-401 Rebose Pasta al suelo del contenedor I-08 + cubeto Medio

R-501 Más T / menos pH Pierde enzima / vapor I-05 Medio

R-501 Válvula mal tendida a
EDAR Proteína a efluente No existe esa tubería en P&ID Alto si se añade

PLC Pérdida de comms Planta a ciegas I-07 fail-safe Alto sin prueba SAT

Eléctrico Fallo de red Paro no aislado I-06 cierra V-101/401 Medio

Personas EDAR Acceso a contenedor Químico / láser Cerradura + formación CAE Medio

Tabla HAZOP-00. Acciones previas al SAT: probar I-01 a I-08 con agua de red y acta firmada.

Pruebas SAT mínimas (agua de red, sin efluente)

ID Prueba Criterio de pasa

S1 Cerrar V-101 por seta y por corte de red; cronometrar V-101 y V-401 cerradas <3 s

S2 Simular TMP alta Arranca backwash; si persiste, para P-301

S3 Abrir puerta SE-201 con llave de prueba Láseres off; no rearmar solos

S4 Llenar TK-401 hasta alarma Para reciclo; no rebosa cubeto

S5 Intentar abrir V-601 con V-401 abierta PLC lo impide

S6 Historiador 15 min P, Q, T y estados de válvula grabados

Tabla SAT-00. Sin acta S1–S6 no hay GO de efluente real.

Declaración de no plagio

El P&ID-001, este paquete SOP/HAZOP y el modelo CONV-EDAR-001 han sido redactados y dibujados de nuevo
para REMPLAST-Q. No se ha insertado texto literal de normas ISO, de pliegos de Aigües de Barcelona, AMB o
ACA, ni de artículos sobre PETasas, membranas o detección óptica. Las referencias a ISO 24187, a LCC-ICCG y
a proveedores (TAMI, Siemens, Hellma, etc.) son menciones de marco o de mercado, no transcripciones. Las
fórmulas de flujo de membrana y los rangos de operación son ingeniería de proceso de dominio público, reescrita
y dimensionada al piloto de 5 m³/h.

Autor: Lázaro López Paz. Asistencia de redacción: Grok. Si un tercero ejecuta o continúa el proyecto, debe citar a
ambos.
