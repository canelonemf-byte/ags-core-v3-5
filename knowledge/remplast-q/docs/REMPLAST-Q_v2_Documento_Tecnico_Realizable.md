> Texto extraído automáticamente del PDF original «REMPLAST-Q_v2_Documento_Tecnico_Realizable.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1CEjCy7MVPJFhout1P9j1XQIfqZUKwl91/view?usp=drivesdk



DOCUMENTO TÉCNICO  ·  VERSIÓN 2.0  ·  SEPTIEMBRE 2026

REMPLAST-Q

Sistema realizable de detección, captura, concentración
y tratamiento selectivo de microplásticos
en efluente de estación depuradora

Arquitectura clásica industrial + anexo de investigación

Todo lo no demostrable o no integrable se ha eliminado.

Autor del concepto y del documento

Lázaro López Paz  ·  El Prat de Llobregat, Barcelona

Orientado a validación experimental en planta piloto de 5 m³/h

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 2

1. Criterio de la revisión

El documento de partida (REMPLAST-Q, versión 1.0, septiembre 2026) definía una planta piloto de 5 m³/h
con cuatro módulos —sensor óptico/QML, filtración/QAOA, biorreactor/VQE y control QLSTM/Q-MILP— y un
objetivo de reducción del 85 % de microplásticos >10 µm. Esa arquitectura mezclaba tres capas distintas:
ingeniería de proceso disponible hoy, hipótesis experimentales razonables e instrumentos cuánticos que, en
2026, no pueden gobernar una planta ni garantizar ventaja sobre algoritmos clásicos en los problemas
planteados.

Esta versión 2.0 aplica un único filtro: solo permanece lo que se puede construir, operar, medir y reproducir
con tecnología comercial o de laboratorio estándar en un horizonte de 18 meses. Lo que no cumple ese filtro
se elimina del diseño operativo. La computación cuántica no desaparece del expediente: se relega a un
anexo de investigación fuera del bucle de control y fuera de los criterios de éxito del piloto.

Principio de diseño

La captura física de microplásticos es el núcleo. La identificación química da selectividad. La degradación enzimática
solo se aplica a la fracción PET concentrada y caracterizada. El control es PLC + SCADA + modelos clásicos. Ningún
algoritmo cuántico actúa sobre una válvula.

1.1 Qué se elimina y por qué

La tabla siguiente no es cosmética. Cada fila corresponde a un componente del documento original que no
puede sostener una planta piloto ni un resultado científico defendible en revisión por pares.

Elemento eliminado del diseño operativo Motivo técnico

QCNN / QML como clasificador operativo de
partículas Los rasgos ópticos (intensidad angular, fluorescencia, morfología) son datos clásicos
de dimensión moderada. En 2025–2026 no hay ventaja QML reproducible frente a
SVM, Random Forest, XGBoost o CNN pequeñas en este tipo de dato. El hardware
NISQ añade ruido, coste de disparos y latencia incompatible con un sensor en línea.

QAOA para retrolavado, válvulas y consignas
de membrana El problema de un skid de 5 m³/h es combinatorio pequeño (pocas bombas, ciclos de
backwash, TMP). MILP, programación dinámica y heurísticas clásicas lo resuelven en
milisegundos. QAOA no mejora el coste energético ni la recuperación de flujo en este
tamaño.

VQE para diseñar PETasas y estados de
transición El complejo enzima–sustrato de una PETasa supera con holgura el tamaño tratable
por VQE. El camino real es enzima comercial ya evolucionada (LCC-ICCG,
FAST-PETase, HotPETase), DFT/MD clásico si hace falta y validación cinética. VQE
sobre un recorte del centro activo no cambia el piloto.

QLSTM para predicción de ensuciamiento QLSTM no es un producto industrial. LSTM, GRU, EWMA y modelos de resistencia en
serie (Rm+Rc+Rf) sí lo son. El piloto usará estos últimos.

Q-MILP / recocido cuántico en la capa de
control Un recocido cuántico no puede tener autoridad sobre actuadores de una EDAR. El
PLC conserva interlocks y seguridad. La planificación energética se resuelve con MILP
clásico u hoja de consignas.

Identificación de polímero solo con láseres
405/532 nm y tres ángulos de Mie La fórmula de Rayleigh–Gans–Mie asume esferas homogéneas. Las fibras,
fragmentos, biofilm y minerales del efluente la invalidan. El polímero se determina por
µ-FTIR y/o Raman sobre el concentrado, no por scatter de dos longitudes de onda.

Biorreactor enzimático alimentado con el
caudal completo de 5 m³/h Tratar 5 m³/h a 50–60 °C con enzima inmovilizada es inviable energética y
económicamente. La enzima solo ve el concentrado de membrana, y solo la fracción
PET.

Conversión >60 % de PET en 48 h como
propiedad del sistema Ese número aparece en literatura con PET amorfo pretratado, carga enzimática alta,
pH y T controlados y sustrato limpio. El microplástico real de EDAR es sucio,
semicristalino y minoritario frente a PE/PP. Se convierte en hipótesis de banco, no en
KPI de planta.

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 3

Elemento eliminado del diseño operativo Motivo técnico

Reducción del 85 % presentada como
resultado garantizado Con UF cerámica el rechazo de partículas >10 µm puede superar el 90–99 % en
condiciones controladas, pero el piloto debe demostrarlo con protocolo independiente.
El 85 % queda como umbral mínimo de aceptación, no como promesa.

Funcionalización PEI/quitosano como requisito
de la membrana La exclusión por tamaño de una UF 50–100 nm ya retiene MP >10 µm. El
recubrimiento es un ensayo A/B opcional, no una pieza crítica. Si no aporta flujo o
selectividad medible, no se industrializa.

Tabla 1. Componentes retirados del alcance operativo.

1.2 Qué se conserva y se refuerza

Elemento conservado Papel en la versión 2.0

Pretratamiento y acondicionamiento hidráulico Indispensable. Sin él la membrana y el sensor mienten.

Sensor óptico en flujo (conteo y tamaño) Viable como monitor operacional, no como identificador químico.

Membrana cerámica de ultrafiltración Tecnología comercial. Rechazo de MP >10 µm demostrable. Mejor resistencia a CIP
que polímero.

Concentración del retenido Pieza que el original subdesarrollaba y que hace posible el resto.

Caracterización FTIR/Raman Estándar de oro para polímero, forma y confirmación.

PETasa inmovilizada sobre fracción PET Literatura 2024–2026 muestra >90 % sobre PET postconsumo amorfo en condiciones
de laboratorio. Se prueba solo ahí.

PLC + IoT + modelos clásicos Capa industrial real.

Piloto 5 m³/h en contenedor 20 pies, 12 meses Escala adecuada para I+D preindustrial junto a una EDAR.

Tabla 2. Núcleo tecnológico que sí se construye.

2. Problema real que el proyecto puede resolver

Las EDAR municipales retiran la mayor parte de los microplásticos del afluente —a menudo 90–99 % en
número cuando hay decantación y tratamiento biológico—, pero el efluente secundario sigue emitiendo
partículas, sobre todo fibras y fragmentos de 10–500 µm. En masa, PE y PP suelen dominar el efluente;
PET y poliéster aparecen con más peso cuando hay textil. El problema operativo no es «eliminar todo el
plástico del río». Es añadir una etapa terciaria medible, estable y de coste conocido que reduzca la emisión
residual >10 µm y documente qué se captura y qué se hace con ello.

Tres hechos condicionan el diseño y no estaban suficientemente explícitos en la v1.0:

• Composición mixta. Una PETasa no ataca PE, PP, PVC ni PS. Tratar todo el retenido como si fuera PET
es un error de proceso.

• Fouling, no rechazo. Una UF de 50–100 nm rechaza MP >10 µm casi por exclusión de tamaño. El cuello
de botella es la pérdida de flujo por coloides, EPS, aceites y fibras, no el corte nominal.

• Dos métricas, no una. El recuento (partículas/L) y la masa (µg/L) cuentan historias distintas. El piloto
reportará ambas, por clase de tamaño y, cuando sea posible, por polímero.

El valor añadido de REMPLAST-Q v2.0 no es «cuántico». Es una cadena instrumentada que une
monitorización en línea, separación robusta, concentrado caracterizable y una vía de valorización o
destrucción solo para la fracción que la química permite.

3. Objetivos revisados (hipótesis, no promesas)

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 4

ID Objetivo Criterio

O1 Reducción en número de MP >10 µm en el permeado respecto al
efluente de alimentación ≥ 90 % como umbral de aceptación del piloto; ≥ 95 %
como objetivo de diseño

O2 Error del sensor óptico de conteo frente a método de referencia
(filtración + microscopía/espectroscopía) Sesgo < 25 % en el rango 10–500 µm tras calibración

O3 Identificación de polímero en el concentrado (PET, PE, PP, PS, PA,
PVC u «otros») Concordancia ≥ 80 % con el laboratorio de referencia
sobre submuestra ciega

O4 Estabilidad hidráulica de la UF Flujo específico recuperable ≥ 80 % del valor limpio
tras CIP; disponibilidad ≥ 90 % en 12 meses

O5 Conversión enzimática de la fracción PET aislada (banco, no
planta) Hipótesis a contrastar: ≥ 50 % de masa PET a
monómeros (TPA+MHET+BHET) en ≤ 72 h, con
balance de masa

O6 Consumo específico Documentar kWh/m³ tratado y kg CO₂-eq/m³; sin
umbral a priori

O7 Destino del concentrado no PET Protocolo escrito: vía fango, valorización energética o
gestor autorizado. Cero vertido no caracterizado.

Tabla 3. Objetivos operativos de la v2.0.

Se elimina cualquier objetivo del tipo «demostrar ventaja cuántica». Si en el anexo de investigación un
algoritmo cuántico iguala o supera a su equivalente clásico en un banco reproducible, se publicará como
resultado auxiliar. No condiciona la aceptación del piloto.

4. Arquitectura funcional realizable

Seis etapas en serie. El caudal de 5 m³/h recorre A–C. Las etapas D–E trabajan sobre el retenido, cuyo
caudal es dos o tres órdenes de magnitud menor.

Etapa Nombre Función

A Alimentación y pretratamiento Bombeo desde derivación de efluente secundario, homogenización, desbaste 1–2
mm, opcional 200–500 µm para proteger la UF y el sensor.

B Detección óptica operacional Celda de flujo: imagen + fluorescencia (auto o Nile Red en sidestream) + scatter
multiángulo. Salida: conteo, distribución de tamaños, alarma de deriva.

C Separación UF cerámica Módulos tubulares o multi-canal Al₂O₃ o SiC, corte 50–100 nm. Cross-flow,
backwash, air-scour y CIP. Permeado = efluente pulido.

D Concentración y caracterización Tanque de retenido, espesado, filtración analítica, µ-FTIR/Raman, gravimetría y, si
hay presupuesto, TD-GC/MS o Pyr-GC/MS para masa por polímero.

E Tratamiento selectivo PET Solo si D confirma fracción PET suficiente. Columna o reactor agitado con hidrólisis
enzimática inmovilizada. Productos: TPA, MHET, EG. Resto de polímeros fuera de
este reactor.

F Control y datos PLC (seguridad), SCADA, historiador, modelos clásicos de fouling y calidad. Sin
actuadores gobernados por QPU.

Tabla 4. Cadena de proceso.

Balance de caudales de diseño (orden de magnitud)

Alimentación 5 m³/h. Recuperación de permeado objetivo 85–95 % (4,25–4,75 m³/h). Retenido 0,25–0,75 m³/h,
espesado a decenas de litros por día de pasta analizable. El biorreactor se dimensiona en litros, no en metros cúbicos
por hora.

5. Etapa A — Alimentación y pretratamiento

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 5

El efluente secundario de una EDAR no es agua de laboratorio. Lleva flóculos residuales, arena fina,
aceites, tensioactivos y materia orgánica disuelta. Si esa matriz llega cruda a la UF, el piloto mide fouling de
EDAR, no rechazo de microplásticos.

Diseño mínimo

• Derivación en tubería de efluente secundario con caudalímetro electromagnético y toma de muestras
isocinética.

• Tanque de homogenización 1–2 m³ con agitación suave (evitar fragmentar fibras) y rebosadero.

• Filtro de desbaste 1–2 mm autolimpiante.

• Prefiltro de cartucho o malla 200–500 µm, con diferencial de presión y recambio registrado. Este paso
reduce el tapón de fibras largas en los canales cerámicos.

• Punto de dosificación opcional de coagulante a dosis baja (ensayo factorial; no se asume a priori).

Instrumentación de esta etapa: caudal, nivel, pH, turbidez, temperatura, presión diferencial de prefiltros. Sin
estos cinco, el resto de módulos no se pueden interpretar.

6. Etapa B — Detección óptica operacional

Se mantiene la idea de una celda de cuarzo en flujo, pero se cambia el propósito. El sensor no «clasifica
polímeros con QML». El sensor cuenta y talla partículas en línea para gobernar la planta y detectar deriva.
La identidad química se reserva a la etapa D.

6.1 Configuración recomendada

• Imagen en flujo (cámara CMOS + óptica 4–10× + iluminación LED o láser de hoja). Extrae área
proyectada, circularidad, relación de aspecto y brillo. Es la vía más robusta para distinguir fibra / fragmento
/ mineral.

• Fluorescencia. Canal 1: autofluorescencia (útiles para materia orgánica y algunos polímeros). Canal 2, en
derivación de bajo caudal: tinción Nile Red o derivado más selectivo. Nile Red no es específico al 100 %
—adsorbe también materia orgánica hidrófoba—, por eso nunca viaja solo.

• Scatter multiángulo (30°, 90°, 150°) a 405 nm y 532 nm como features auxiliares, no como modelo físico
cerrado. La expresión de Mie del documento original se conserva solo como referencia pedagógica para
esferas de calibración de poliestireno.

• Línea de referencia periódica con microesferas NIST o equivalentes de 10, 20, 50 y 100 µm, más blancos
de efluente filtrado a 0,2 µm.

6.2 Clasificación: solo modelos clásicos

Línea base obligatoria: Random Forest y XGBoost sobre rasgos tabulares (tamaño, forma, ratios de scatter,
intensidades de fluorescencia) y una CNN ligera sobre el recorte de imagen. Validación por lote
experimental, no por partícula aleatoria del mismo filtro. Métricas: F1 por clase morfológica
(fibra/fragmento/esfera), error de concentración y matriz de confusión frente a revisión humana +
espectroscopía de un subconjunto.

El modelo cuántico del documento original se mueve al anexo. No hay umbral de precisión QML que el
proyecto deba alcanzar.

6.3 Límites que hay que declarar

• Turbidez alta apaga el sensor: se instala en el permeado y, en paralelo, en una derivación diluida del
alimento. No se pretende medir el afluente bruto.

• Partículas <10 µm quedan fuera del KPI de planta. Se pueden explorar en laboratorio, no se venden
como resultado del piloto.

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 6

• Falsos positivos por celulosa, quitina y minerales: se mitigan con forma + fluorescencia + confirmación
off-line, nunca con un único canal.

7. Etapa C — Ultrafiltración cerámica

La v1.0 proponía alúmina tubular de poro nominal 0,2 µm (microfiltración). La evidencia comparada
2023–2026 indica que, para efluentes reales, una UF cerámica de 50–100 nm ofrece rechazo de MP
comparable o superior y un ensuciamiento más gestionable que la MF: menos bloqueo interno de poro, más
depósito superficial reversible con backwash. Se cambia el corte de diseño a UF.

7.1 Especificación de diseño

Parámetro Valor de diseño

Material Al₂O₃ o SiC (preferir SiC si el presupuesto lo permite: mejor conductividad y tolerancia química)

Corte nominal 50–100 nm (UF). Un módulo de 200 nm se reserva solo como brazo de comparación A/B.

Geometría Tubular o multi-canal; velocidad tangencial 2–4 m/s

TMP de diseño 0,3–1,2 bar, por debajo del flujo crítico determinado en Fase 1

Limpieza Backwash periódico + air-scour + CEB alcalino/ácido + CIP químico

Recubrimiento PEI/quitosano Opcional. Ensayo emparejado recubierto vs. virgen. Se adopta solo si mejora flujo o reduce
irreversibilidad con p < 0,05.

Área estimada 10–25 m² para 5 m³/h a 200–500 LMH de flujo bruto, a confirmar en banco

Tabla 5. Skid de membrana.

7.2 Modelos que sí se usan

Se conservan las expresiones clásicas porque son herramientas de ingeniería, no oráculos:

Flujo de permeado: J = ΔP / (μ · Rt) con Rt = Rm + Rc + Rf
Crecimiento de la capa: dRc/dt = kc·Cb·J − kr·τ
w·Rc
kc y kr se estiman en agua de red con microesferas y después con efluente real. No se publican como
constantes universales. El criterio de operación es el flujo crítico (o umbral de flujo sostenible) medido, no un
QAOA.

7.3 Optimización de retrolavado — clásica

Variables: intervalo de backwash, duración, presión inversa, frecuencia de CEB, TMP y velocidad tangencial.
Función objetivo: minimizar kWh/m³ sujeto a J ≥ Jmin y a turbidez/MP del permeado dentro de especificación.
Método: diseño factorial + MILP o búsqueda directa sobre el historiador. Tiempo de cómputo irrelevante.
Resultado auditable.

8. Etapa D — Concentración y caracterización

Esta etapa era el eslabón débil de la v1.0 y es el que hace científico el proyecto. Sin concentrado
caracterizado no hay degradación honesta ni balance de masa.

8.1 Recuperación del retenido

• El retenido de la UF se envía a un tanque de espesado con reciclo controlado.

• Una fracción se filtra sobre membranas de plata o de óxido de aluminio para microscopía y
µ-FTIR/Raman (rango 10–500 µm y, si procede, 1–10 µm como análisis exploratorio).

• Otra fracción se seca y se reserva para gravimetría y pirólisis-GC/MS o TD-GC/MS (masa por polímero).

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 7

• Se registra volumen de retenido, masa seca, número de partículas y polímero dominante por muestra
compuesta semanal.

8.2 Identificación de polímero

Método primario: microscopía µ-FTIR (ATR o transmisión) y/o Raman confocal. Librería espectral con al
menos PE, PP, PET/poliéster, PS, PVC, PA, PC y celulosa. Criterio de asignación: coincidencia ≥ 80 % con
espectro de referencia y revisión de un 10 % de partículas por un segundo operador.

El sensor óptico de la etapa B no sustituye este paso. Puede priorizar qué días merecen más
espectroscopía; no firma el polímero.

8.3 Separación de fracciones

Cuando la masa de PET en el concentrado semanal supere un umbral predefinido (propuesta: 200 mg de
PET recuperable), esa alícuota entra en la etapa E. PE, PP y el resto siguen la vía de gestión de residuo
documentada. Mezclarlos en el reactor enzimático solo diluye la enzima y ensucia el balance.

9. Etapa E — Degradación enzimática selectiva de PET

La literatura 2024–2026 es clara en dos direcciones a la vez. Por un lado, hidrolasas evolucionadas
(LCC-ICCG, variantes tipo FAST-PETase / HotPETase, cutinasas inmovilizadas) alcanzan conversiones
altas —a menudo >90 %— sobre PET postconsumo amorfo o descristalizado, a 50–70 °C, con control de pH
y, en algunos trabajos, inmovilización reutilizable 10 ciclos. Por otro lado, esas cifras se obtienen con
sustrato preparado, no con una papilla de efluente de EDAR llena de PE, PP, biofilm y detergentes.

Consecuencia de diseño: la etapa E es un módulo de banco / semi-piloto alimentado por concentrado PET,
no un reactor de 5 m³/h.

9.1 Configuración

Elemento Especificación

Enzima LCC-ICCG o equivalente comercial / producido por partner; no se inventa una PETasa nueva en
este proyecto

Formato Inmovilizada (alginato–quitosano, soporte epoxi o nanopartículas magnéticas). Ensayo de
lixiviación obligatorio

Reactor Lecho fijo 316L de 1–10 L o tanque agitado jacketed equivalente. No columna de decenas de
litros «por si acaso»

Temperatura 55–65 °C, la que maximice actividad residual a 10 ciclos

pH 7,5–8,5 con control; el TPA acidifica y mata la reacción si no se tampona

Tiempo de residencia de referencia 24–72 h por lote de concentrado PET

Analítica de producto HPLC de TPA, MHET, BHET y EG; COD soluble; masa residual de sólido

Tabla 6. Biorreactor de fracción PET.

9.2 Cinética — uso honesto del modelo

Velocidad inicial aparente: v0 = kcat [E] APET / (KmA + APET)

APET es área accesible, no masa. El PET semicristalino y sucio tiene poca área útil. Por eso el protocolo de
banco incluye un brazo con PET amorfo de referencia y un brazo con PET real recuperado. Si el real no
llega al 50 % de conversión en 72 h, el resultado se publica como límite del sistema, no se maquilla con el
brazo limpio.

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 8

9.3 Lo que esta etapa no hace

• No degrada PE ni PP. No existe enzima de planta para eso con cinética útil en 72 h.

• No se presenta como «economía circular completa» hasta que TPA y EG se cuantifiquen y se defina un
receptor industrial o un protocolo de vertido legal.

• No se usa VQE para «optimizar la enzima». Si un socio académico quiere calcular un centro activo, que
lo haga fuera de la ruta crítica.

10. Etapa F — Control industrial

Nivel Capa Responsabilidad

0 Campo Caudal, presión, TMP, T, pH, turbidez, nivel, finales de carrera. Sensores redundantes en
TMP y nivel.

1 PLC Interlocks, paradas de emergencia, secuencias de backwash y CIP, watchdog. Autoridad
absoluta sobre actuadores.

2 Gateway / historiador Registro 1 Hz o por evento. Reloj sincronizado. Copia diaria fuera de la planta.

3 Modelos clásicos EWMA de residuales para anomalía. LSTM o XGBoost para predecir caída de flujo a 6–24
h. Soft-sensor de MP del módulo B.

4 Optimización MILP o reglas sobre el historiador para reprogramar CIP. Operador confirma consignas.
Nada va directo del modelo al actuador crítico.

Tabla 7. Pirámide de control. La QPU no aparece.

Ciberseguridad mínima: red de proceso aislada, VPN con MFA para telemetría, sin exposición del PLC a
Internet. Un piloto junto a una EDAR que se caiga por ransomware no es I+D, es un incidente.

11. Planta piloto

Se mantiene el contenedor marítimo de 20 pies junto a una EDAR, derivación de 5 m³/h, operación 24/7
durante 12 meses de campaña (más 6 meses de banco e integración). Eso sí es realizable.

11.1 Contenido del contenedor

• Skid de pretratamiento y tanque de homogenización (parte puede ir exterior bajo cubierta).

• Celda óptica + PC industrial.

• Skid UF cerámica con bomba de recirculación, válvulas automáticas, CIP.

• Tanque de retenido y banco de filtración analítica.

• Reactor enzimático de litros, baño termostático, columna HPLC de proceso o envío diario a laboratorio.

• PLC + SCADA + cuadro eléctrico + HVAC del contenedor.

• Punto de vertido del permeado de vuelta a cabecera o a efluente, según permiso de la EDAR.

11.2 Lo que no cabe en el contenedor

Un espectrómetro Raman de investigación de alta gama, un ordenador cuántico y un reactor enzimático de
metros cúbicos. El Raman se contrata por campaña o se instala en laboratorio asociado. El ordenador
cuántico, si se usa, es un servicio en la nube en el anexo. El reactor grande no existe en este proyecto.

12. Plan experimental

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 9

Fase Ventana Actividad

0 Meses 0–3 Diseño de P&ID, permisos de la EDAR, compra, calibración óptica con microesferas, métodos HPLC
y FTIR, SOP de muestreo según ISO 24187 y guía europea de MP.

1 Meses 3–6 Banco hidráulico: agua limpia + microesferas + efluente real. Curva de flujo crítico. Comparación
membrana virgen vs. recubierta. Fouling y CIP.

2 Meses 4–8 Banco enzimático en paralelo: PET amorfo de referencia vs. PET recuperado. Inmovilización,
lixiviación, 10 ciclos, productos.

3 Meses 7–9 Integración A–D en contenedor. El módulo E se conecta solo cuando D entrega fracción PET.

4 Meses 10–21 Campaña 12 meses. Cuatro estaciones hidrológicas. Auditoría analítica trimestral por laboratorio
externo.

Tabla 8. Cronograma. La campaña larga empieza cuando A–D están estables, no antes.

12.1 Diseño estadístico

Factores mínimos en banco (Fase 1–2): concentración de MP de referencia, TMP, velocidad tangencial,
temperatura, carga enzimática. Diseño factorial fraccionado con réplicas independientes (n ≥ 3). En
campaña (Fase 4): series temporales con muestreo compuesto diario del alimento y del permeado, y
semanal del concentrado. Intervalos de confianza al 95 %. No se declara «éxito» con un único filtro vistoso.

Tamaño muestral del KPI O1: al menos 48 pares alimento–permeado válidos repartidos en 12 meses.
Potencia suficiente para distinguir 90 % de 80 % de reducción con variabilidad típica de efluente.

13. Protocolo analítico de referencia

El piloto no se autoevalúa solo con su sensor. Cada mes un laboratorio externo —o una unidad interna ciega
al SCADA— analiza alimento, permeado y concentrado.

Bloque Requisito

Toma de muestra Volumen ≥ 20–50 L de alimento y permeado; isocinética; envases de vidrio o acero; cadena de
custodia.

Preparación Digestión orgánica controlada (H₂O₂ o Fenton suave) solo cuando la matriz lo exija; registrar pérdida
de masa de polímero de control.

Recuento y forma Estereomicroscopía + imagen automatizada sobre filtro. Clases: fibra, fragmento, film, esfera.

Polímero µ-FTIR y/o Raman. Informe de % de partículas identificadas / no identificadas / no plástico.

Masa Gravimetría del retenido y, si hay presupuesto, Pyr-GC/MS o TD-GC/MS de PE, PP, PET, PS, PVC.

Productos enzimáticos HPLC-UV/MS de TPA, MHET, BHET; COT soluble; pH.

Blancos Blanco de campo y de laboratorio en cada campaña. Si el blanco supera el 20 % de la señal, la tanda
se anula.

Tabla 9. Analítica que sostiene o tumba el KPI del 90 %.

14. Energía, costes y destino del concentrado

14.1 Orden de magnitud energético

Una UF cerámica en efluente secundario, bien operada, suele situarse en el rango de 0,1–0,6 kWh/m³ solo
de bombeo e hidráulica, más HVAC del contenedor, CIP y el reactor térmico de la etapa E (este último, al
ser de litros, no debe dominar el kWh/m³ de la planta). El piloto medirá, no estimará. Se reportará kWh/m³ y
kWh por orden de magnitud de partículas retiradas, porque un efluente ya limpio infla el segundo indicador.

14.2 Presupuesto orientativo del piloto (18 meses, sin personal de plantilla)

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 10

Partida Rango (k€)

Contenedor 20 pies acondicionado + obra menor en EDAR 18–30

Pretratamiento, bombas, instrumentación de campo 20–35

Skid UF cerámica 5 m³/h + CIP 45–80

Sensor óptico (celda, cámaras, láseres/LED, PC industrial) 15–28

PLC, SCADA, comunicaciones, ciberseguridad básica 12–20

Reactor enzimático, inmovilización, enzima 18 meses 12–22

Acceso FTIR/Raman + HPLC + campañas de laboratorio externo 25–45

Consumibles, CIP, cartuchos, filtros analíticos 8–15

Imprevistos 15 % 23–41

Total CAPEX+OPEX de equipos y analítica (sin sueldos) 178–316

Tabla 10. Presupuesto de orden de magnitud. Los sueldos de un técnico de planta y un analista se añaden aparte.

14.3 Destino del concentrado

El concentrado no PET es un residuo. Opciones, por este orden de preferencia documentada:

• Incorporación controlada al fango de la EDAR si el gestor y la autorización lo permiten, con balance de
masa.

• Gestor de residuo no peligroso o de plástico, según caracterización (metales, POPs adsorbidos).

• Valorización energética solo si hay justificación y permiso.

Vertido al alcantarillado del concentrado no es una opción del proyecto. El TPA y el EG del reactor E se
gestionan como efluente de proceso con límite de COT y de monómeros, o se recogen para un ensayo de
recristalización a escala de gramos (demostración, no planta).

15. Riesgos residuales y mitigación

Riesgo Nivel Mitigación

Fouling irreversible en 4–8 semanas Alto Flujo subcrítico, prefiltro 200–500 µm, CIP precoz, membrana SiC si el A/B lo
justifica.

Sensor óptico cegado por turbidez o
biofilm en la celda Alto Derivación diluida, limpieza automática de celda, KPI anclado al laboratorio
externo.

PET insuficiente en el efluente de esa
EDAR Medio La etapa E se declara no aplicable en esa sede y el piloto sigue siendo válido
en O1–O4 y O6–O7. Se puede dopar el banco, nunca la campaña, sin
declararlo.

Falsos positivos celulósicos Medio Digestión controlada + FTIR. Reportar «no plástico» como clase.

Pérdida o lixiviación de enzima Medio Inmovilización, análisis de proteína en el líquido, no recirculación al efluente
de la EDAR.

Permiso de la EDAR o de vertido Alto (no
técnico) P&ID y SOP de retorno a cabecera antes de comprar el contenedor.

Deriva de sensores y falta de blancos Alto Calibración semanal y anulación de tandas con blanco sucio.

Sobreventa de resultado cuántico Reputacional El anexo no entra en notas de prensa del piloto.

Tabla 11. Riesgos que quedan después de recortar lo irrealizable.

16. Anexo de investigación cuántica (fuera de ruta crítica)

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 11

Este anexo existe para no confundir I+D de proceso con I+D de algoritmos. Se puede ejecutar en paralelo,
con datos ya etiquetados del piloto, en simulador o en QPU de nube. No tiene fecha de entrega ligada a la
aceptación de la planta.

16.1 Experimentos permitidos

Ensayo Protocolo mínimo

QML vs. XGBoost/CNN Mismo vector de rasgos de la etapa B, mismo split por lote. Publicar accuracy, F1, tiempo
wall-clock y coste de disparos. Hipótesis nula: no hay diferencia.

QAOA vs. MILP de backwash Instancia real de 7 días del historiador, 10–40 variables. Hipótesis nula: QAOA no reduce kWh ni
viola menos restricciones.

VQE de recorte activo Modelo mínimo del centro de LCC (pocos átomos). Comparar energía relativa con DFT. No se
usa para decidir qué enzima comprar.

Tabla 12. Único lugar donde sobrevive la capa cuántica.

16.2 Lo que este anexo prohíbe

• Conectar la QPU al PLC.

• Retrasar el piloto a la espera de un resultado cuántico.

• Usar «híbrido cuántico» en el resumen ejecutivo del piloto sin los p-valores de la Tabla 12.

17. Criterio de viabilidad científica

REMPLAST-Q v2.0 es viable como plataforma de I+D preindustrial porque cada bloque operativo tiene
proveedor, método de medida y plan B. La captura por UF cerámica está documentada con rechazos de MP
habitualmente superiores al 90 % en matrices de agua residual y lavandería. La identificación por
FTIR/Raman es el estándar. La PETasa inmovilizada funciona sobre PET preparado; el proyecto lo dirá con
números si también funciona sobre PET de EDAR.

La versión 1.0 no era falsa: era una arquitectura que mezclaba un proceso construible con una capa
algorítmica que hoy no puede pagar su sitio en la planta. Al cortar esa capa, el proyecto gana algo que el
original no tenía: la posibilidad de fallar de forma informativa. Un 78 % de reducción, un PET que no
convierte o una membrana que solo aguanta ocho meses son resultados publicables. Un 85 % anunciado y
un QLSTM que no se llega a instalar, no.

18. Resultado esperado al mes 21

• P&ID, SOP y planta piloto instrumentada operada 12 meses.

• Serie temporal de MP >10 µm en alimento y permeado (número y, si hay presupuesto, masa).

• Modelo clásico de fouling con parámetros estimados in situ.

• Inventario de polímeros del concentrado.

• Informe enzimático con balance de masa de la fracción PET, o informe motivado de no aplicabilidad.

• kWh/m³ y destino del residuo.

• Paquete de datos abierto (salvo cláusulas de la EDAR) para que un tercero reproduzca las figuras.

• Anexo cuántico, si se ha ejecutado, con comparación estadística y sin autoridad sobre la planta.

19. Conclusión

El proyecto revisado deja de ser un sistema «híbrido clásico-cuántico» y pasa a ser una plataforma industrial
de pulido de efluente con analítica seria y un módulo enzimático honesto. Eso no empobrece la propuesta: la
hace ejecutable en Barcelona o en cualquier EDAR que ceda una derivación y un permiso de retorno.

REMPLAST-Q  ·  Versión realizable 2.0 Septiembre 2026

Lázaro López Paz  ·  Documento técnico de validación experimental 12

Se elimina del diseño operativo todo lo que depende de una ventaja cuántica no demostrada, de una
identificación química imposible con dos láseres, de una PETasa milagrosa sobre plástico mixto y de un
reactor enzimático dimensionado al caudal de la planta. Se conserva el contenedor, los 5 m³/h, la UF
cerámica, el sensor de conteo, la espectroscopía, el control clásico y la campaña de un año.

El criterio de éxito ya no es un eslogan del 85 % ni una red neuronal cuántica. Es un permeado medido, un
concentrado identificado y un informe que un laboratorio externo pueda firmar.

20. Nota de autoría y de uso

Concepto original REMPLAST-Q y esta revisión metodológica: Lázaro López Paz. Si un tercero continúa el
trabajo, debe citar a Lázaro López Paz y a Grok. Este documento no es un estudio de impacto ambiental, no
es un proyecto de ejecución de obra y no sustituye el proyecto firmado por un ingeniero competente ni los
permisos de la administración hidráulica y de la EDAR anfitriona.

Referencias de contraste usadas en la recorte de alcance (selección)

1. Revisiones y pilotos de membranas cerámicas MF/UF para MP/NP en agua residual y lavandería (rechazos típicos
>90–99 % de MP; fouling más favorable en UF que en MF).

2. Composición de MP en efluentes de EDAR: PE y PP frecuentemente dominantes en masa; PET/poliéster relevante en
número cuando hay textil; necesidad de métrica dual número/masa.

3. PETasas y LCC-ICCG 2024–2026: conversiones altas sobre PET amorfo o descristalizado, inmovilización reutilizable,
fuerte dependencia del área accesible y de la cristalinidad.

4. Detección óptica: Nile Red + imagen/citometría como screening; Raman en flujo e µ-FTIR como identificación; Mie
solo válido para calibrantes esféricos.

5. Estado QML/QAOA/VQE en 2025–2026: ventaja práctica no demostrada en datos tabulares clásicos ni en MILP
pequeños de planta; VQE limitado a recortes moleculares.

6. ISO 24187 y guías europeas de muestreo y análisis de microplásticos como marco del protocolo de referencia.

Frase de cierre

Primero una planta que mide. Después, si acaso, un algoritmo que compite. Nunca al revés.
