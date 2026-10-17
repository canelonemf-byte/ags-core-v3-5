> Texto extraído automáticamente del PDF original «informe_viabilidad_gravedad_tiempo.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1ZDVizrsa0l6LeQEKnDupazZEk83l8Ym5/view?usp=drivesdk



Informe de viabilidad técnico-matemático:

Control del tiempo y la gravedad mediante convergencia tecnológica

Lázaro López Paz
El Prat de Llobregat, Barcelona, España
Innovador independiente con asistencia de inteligencia arti˝cial
 31 de julio de 2026
 Abstract

Este informe presenta un análisis exhaustivo, desde la física teórica y experimental con-
temporánea (estado a julio de 2026), de las vías propuestas para el control de la gravedad,
la manipulación del ˛ujo temporal y la obtención de información del futuro. Se incluyen las
ecuaciones fundamentales de la relatividad general, las condiciones de energía, las métricas de
warp y agujeros de gusano, las desigualdades cuánticas, los modelos de gravedad análoga con
metamateriales, y algoritmos de optimización asistidos por inteligencia arti˝cial. Se distingue
rigurosamente entre efectos relativistas veri˝cados, analogías de laboratorio y propuestas de con-
trol macroscópico real. La conclusión es que el control efectivo de la curvatura del espaciotiempo
permanece fuera del alcance tecnológico actual y previsible, aunque los sistemas análogos y las
simulaciones numéricas constituyen herramientas cientí˝cas de alto valor.

Contents

1 Resumen ejecutivo 2

2 Marco teórico fundamental 2
2.1 Ecuaciones de Einstein y tensor de Einstein . . . . . . . . . . . . . . . . . . . . . . . 2
2.2 Condiciones de energía . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
2.3 Desigualdades cuánticas (Quantum Inequalities) . . . . . . . . . . . . . . . . . . . . . 3
2.4 Principio de equivalencia y parámetro post-newtoniano . . . . . . . . . . . . . . . . . 3

3 Control de la gravedad: métricas y requisitos energéticos 3
3.1 Métrica de Alcubierre . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3
3.2 Variantes de energía positiva y límites . . . . . . . . . . . . . . . . . . . . . . . . . . 3
3.3 Inconsistencia de κ(x) metamaterial . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
3.4 Gravedad análoga: métrica efectiva en metamateriales . . . . . . . . . . . . . . . . . 4
3.5 Gravedad arti˝cial rotacional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

4 Manipulación del ˛ujo del tiempo 4
4.1 Dilatación temporal . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4
4.2 Curvas temporales cerradas (CTCs) . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
4.3 Agujero de gusano de MorrisThorne . . . . . . . . . . . . . . . . . . . . . . . . . . . 5

5 Obtención de información del futuro y retrocausalidad 5
 1

6 Convergencia tecnológica y algoritmos 5
6.1 Algoritmo de diseño inverso de metamateriales para analogías gravitatorias . . . . . 5
6.2 Algoritmo de evaluación de condiciones de energía . . . . . . . . . . . . . . . . . . . 6
6.3 Uso de IA en el proyecto . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

7 Análisis de viabilidad cuantitativo 6

8 Consideraciones éticas y de seguridad 6

9 Conclusiones y recomendaciones 7

2

1. Resumen ejecutivo

El control de la gravedad y del tiempo es uno de los horizontes más ambiciosos de la física aplicada.
Este informe examina las propuestas bajo el prisma de las leyes físicas establecidas, las ecuaciones
exactas y los resultados experimentales más recientes.
Hallazgos principales:

‹ La dilatación temporal gravitatoria y cinemática es un efecto real, medido con precisión de milímet-
ros y utilizado operativamente (GPS). No constituye un control arbitrario del ˛ujo temporal local.

‹ Las métricas de tipo Alcubierre y variantes (incluidas las de energía positiva subluminal) exigen
densidades de energía o con˝guraciones de estrés-energía extremas. Propuestas de acoplamiento
gravitatorio variable κ(x) mediante metamateriales son inconsistentes con las identidades de
Bianchi y excluidas experimentalmente.

‹ Los metamateriales permiten métricas efectivas para ondas electromagnéticas o acústicas (gravedad
análoga). No modi˝can la curvatura real del espaciotiempo ni generan fuerzas gravitatorias sobre
la materia.

‹ Las curvas temporales cerradas (CTCs) y los agujeros de gusano atravesables requieren violación
de las condiciones de energía. La conjetura de protección de la cronología y los análisis semiclasicos
indican que los efectos cuánticos impiden su formación estable.

‹ La convergencia de IA, nanotecnología y metamateriales acelera el diseño de analogías y la opti-
mización de estructuras, pero no altera los límites fundamentales.

La viabilidad de un control tecnológico de la gravedad o del tiempo (generación local de curvatura
arbitraria o inversión del ˛ujo temporal macroscópico) se evalúa como extremadamente baja en
el horizonte de las próximas décadas.

2. Marco teórico fundamental

2.1 Ecuaciones de Einstein y tensor de Einstein

La relatividad general relaciona la geometría del espaciotiempo con el contenido de energía-momento:
 Gµν ≡ Rµν − 1
2 Rgµν = 8πG
c4 Tµν ≡ κ0Tµν, (1)

donde Rµν es el tensor de Ricci, R = gµνRµν el escalar de Ricci, gµν la métrica y Tµν el tensor de
energía-momento. La identidad de Bianchi contraída implica la conservación local de energía-momento:
 ∇µGµν ≡ 0 ⇒ ∇µTµν = 0. (2)

Cualquier modi˝cación que introduzca un acoplamiento espacialmente variable κ(x) de forma no
dinámica viola esta identidad, forzando ∇µTµν ̸= 0.

2.2 Condiciones de energía

Para un vector nulo kµ y un vector tipo tiempo tµ normalizado:

Condición de energía nula (NEC): Tµνkµkν ≥ 0, (3)

Condición de energía débil (WEC): Tµνtµtν ≥ 0, (4)

Condición de energía dominante (DEC): WEC + T µνtν es causal , (5)

Condición de energía fuerte (SEC): (
Tµν − 1
2 T gµν
) tµt
ν ≥ 0. (6)

3

La materia ordinaria satisface todas. La materia exótica necesaria para warp drives y agujeros
de gusano atravesables viola al menos la NEC.

2.3 Desigualdades cuánticas (Quantum Inequalities)

En teoría cuántica de campos, la densidad de energía observada por un observador inercial a lo largo
de una trayectoria x(τ ) satisface, para un estado de vacío o próximo, ∫ ∞

−∞⟨Tµν⟩u
µu
ν f (τ ) dτ ≥ − C
τ 4
0 , (7)

donde f (τ ) es una función de muestreo de ancho τ0 y C una constante positiva del orden de ℏc.
Esto limita severamente la magnitud y duración de las regiones de energía negativa.

2.4 Principio de equivalencia y parámetro post-newtoniano

El parámetro PPN γ mide la desviación del principio de equivalencia fuerte. Los límites actuales
son: |γ − 1| ≲ 10
−5 (8)

(procedentes de interferometría de radio de muy larga base, láser lunar y temporización de púl-
sares). Cualquier campo escalar de largo alcance que medie una modi˝cación de κ está fuertemente
restringido.

3. Control de la gravedad: métricas y requisitos energéticos

3.1 Métrica de Alcubierre

La métrica original de Alcubierre (1994) en coordenadas (t, x, y, z) es:

ds
2 = −c
2dt2 + [dx − vs(t)f (rs) dt]2 + dy2 + dz2, (9)

donde rs = √
(x − xs(t))2 + y2 + z2 es la distancia al centro de la burbuja que se mueve con velocidad
vs = dxs/dt, y f (rs) es una función de forma (típicamente un per˝l tipo top-hat suavizado):

f (rs) = tanh
[σ(rs + R)
] − tanh
[
σ(rs − R)]

2 tanh(σR) . (10)

La densidad de energía en el marco de un observador euleriano es:
 T 00 = − c4

8πG v2
s ρ2

4r2
s
 ( df
drs
 )2 < 0 (11)

(con ρ2 = y2 + z2). La energía total requerida para una burbuja de radio R ∼ 100 m a vs ∼ c es del
orden de la masa de Júpiter convertida en energía negativa (estimaciones clásicas).

3.2 Variantes de energía positiva y límites

Trabajos posteriores (Lentz 2021, BobrickMartire 2021, etc.) construyen solitones con densidad de
energía predominantemente positiva, pero:

‹ Suelen ser subluminales.

‹ Requieren todavía regiones de violación de la NEC o geometrías no compactas.

‹ Las magnitudes de energía siguen siendo prohibitivas para escalas macroscópicas útiles.
 4

3.3 Inconsistencia de κ(x) metamaterial

Si se postula Gµν = κ(x)T µν con κ(x) prescrito por la respuesta electromagnética de un metamate-
rial, la identidad de Bianchi ∇µGµν = 0 fuerza:

∇µ(κ(x)T µν) = 0 ⇒ κ∇µT µν + T µν∂µκ = 0. (12)

Si ∂µκ ̸= 0 y T µν no es nulo, se viola la conservación ordinaria. Hacer κ dinámico introduce un
campo escalar que media una quinta fuerza, excluida por los límites de γ.
Además, las condiciones de unión (Israel) en cualquier interfaz donde κ salte requieren una capa
super˝cial de estrés-energía δ-funcional.

3.4 Gravedad análoga: métrica efectiva en metamateriales

En un medio electromagnético lineal con permitividad εij y permeabilidad µij, la propagación de la
luz en la aproximación de onda geométrica puede mapearse a una métrica efectiva geff
µν tal que:

ds2
eff = geff
µν dxµdxν. (13)

Para metamateriales hiperbólicos (un eje con ε∥ > 0, ε⊥ < 0 o viceversa), la métrica efectiva puede
simular un espaciotiempo de Minkowski 2 + 1 o incluso geometrías con horizontes.
Ejemplo clásico (ferro˛uidos hiperbólicos):
 ε∥ = ε0εr > 0, ε⊥ = −ε0|εr| < 0. (14)

La velocidad de fase extraordinaria se comporta como en un espaciotiempo efectivo con ˝rma
(+, −, −) a lo largo de ciertos ejes, permitiendo analogías de dos tiempos y de gravedad efectiva.
Importante: estas métricas efectivas actúan solo sobre el campo electromagnético (o acústico).
No generan curvatura real del espaciotiempo ni fuerzas gravitatorias sobre masas de prueba.

3.5 Gravedad arti˝cial rotacional

Para un hábitat rotatorio de radio R y velocidad angular ω, la aceleración centrípeta efectiva es:

aeff = ω2R = v2

R . (15)

Para aeff = g/2 ≈ 4.9 m s−2 y R = 200 m se requiere ω ≈ 0.156 rad s−1 ( v ≈ 31 m s−1). Esto es
ingeniería estructural, no relatividad general.

4. Manipulación del ˛ujo del tiempo

4.1 Dilatación temporal

La dilatación cinemática (relatividad especial) para un reloj que se mueve con velocidad v respecto
a un observador inercial es: ∆t = γ∆τ, γ = 1
√
1 − v2/c2 . (16)

La dilatación gravitatoria (aproximación de campo débil) para un reloj a potencial Φ es:

∆τ
∆t ≈ 1 + Φ
c2 . (17)

Para la Tierra, el gradiente es ≈ 1.1 × 10−16 m−1. Redes de relojes ópticos han medido este efecto
a diferencias de altura del orden de 1 mm.
 5

4.2 Curvas temporales cerradas (CTCs)

Una curva temporal cerrada es una curva γ tal que γ(0) = γ(1) y el vector tangente uµ = dγµ/dλ
es en todo punto tipo tiempo ( gµνuµuν < 0).
Ejemplos clásicos:

‹ Universo de Gödel.

‹ Interior de un agujero negro de Kerr (para a > M ).

‹ Agujeros de gusano con boca en movimiento relativista.

La conjetura de protección de la cronología a˝rma que los efectos cuánticos (divergencia del valor
esperado del tensor de energía-momento del vacío cerca del horizonte de Cauchy) destruyen la CTC
antes de que se forme.

4.3 Agujero de gusano de MorrisThorne

La métrica estática esférica de un agujero de gusano atravesable es:
 ds2 = −e2Φ(r)c
2dt2 + dr2

1 − b(r)/r + r2(dθ2 + sin2 θ dϕ2), (18)

donde b(r) es la función de forma y Φ(r) el corrimiento al rojo. La condición de ˛are-out en la
garganta r = r0 exige: b − b′r
2b2 > 0 ⇒ violación de la NEC . (19)

La densidad de energía en la garganta es negativa.

5. Obtención de información del futuro y retrocausalidad

En interpretaciones retrocausales de la mecánica cuántica, el estado de un sistema puede depender
de condiciones de contorno futuras. En el formalismo de post-selección de CTCs cuánticos (Lloyd
et al.), la evolución se describe mediante un canal que proyecta sobre el estado ˝nal deseado. Estos
esquemas son simulables experimentalmente con fotones, pero no constituyen un canal de información
clásica del futuro al pasado que viole la causalidad operativa.
No existe un algoritmo o protocolo conocido, dentro de la física establecida, que permita extraer
información utilizable del futuro más allá de las correlaciones cuánticas ordinarias.

6. Convergencia tecnológica y algoritmos

6.1 Algoritmo de diseño inverso de metamateriales para analogías gravitatorias

Entrada: Métrica objetivo gtarget
µν (x), dominio Ω, restricciones de fabricabilidad C.
Salida: Per˝les εij(x), µij(x) que minimizan el error de la métrica efectiva.

1. Inicializar una representación paramétrica θ (red neuronal, bases espectrales o parámetros ge-
ométricos) de ε y µ.

2. Mientras no se alcance convergencia:

(a) Calcular la métrica efectiva geff
µν(θ) mediante aproximación eikonal o simulación FDTD/FEM.
(b) Evaluar la función de pérdida
 L(θ) = ∥
∥geff (θ) − gtarget∥
∥2 + λ Penalizacin(C, θ).

(c) Actualizar θ mediante gradiente (Adam, L-BFGS) o algoritmo evolutivo / bayesiano.

3. Veri˝car el diseño con simulación de onda completa y, si es posible, experimentos de campo lejano.

4. Devolver ε(θ∗), µ(θ∗).
 6

6.2 Algoritmo de evaluación de condiciones de energía

Entrada: Métrica gµν(x) y dominio de evaluación.

1. Calcular el tensor de Einstein Gµν (diferencias ˝nitas, métodos espectrales o código 3+1).

2. Inferir Tµν = Gµν/κ0.

3. Para cada punto x y un conjunto de vectores nulos kµ y tipo-tiempo tµ de prueba:

(a) Evaluar Tµνkµkν, Tµνtµtν y las formas de DEC/SEC.

(b) Registrar las regiones de violación de NEC/WEC/DEC/SEC.

4. Integrar las densidades de energía negativa y estimar el presupuesto energético total.

5. Devolver mapa de violaciones y presupuesto energético.

6.3 Uso de IA en el proyecto

La inteligencia arti˝cial se emplea para:

‹ Optimización topológica de metamateriales (redes neuronales físicas, PINNs).

‹ Exploración del espacio de soluciones de las ecuaciones de Einstein con restricciones de energía
positiva (búsqueda bayesiana, algoritmos genéticos).

‹ Análisis de estabilidad lineal y no lineal de métricas de warp (evolución numérica 3+1).

‹ Diseño de experimentos de precisión para acotar posibles acoplamientos residuales.

Ninguno de estos usos modi˝ca los límites fundamentales impuestos por las ecuaciones (1)(7).

7. Análisis de viabilidad cuantitativo
 Propuesta Estado Obstáculo principal (ecuación)

Dilatación temporal Realizada No es control arbitrario
Gravedad arti˝cial rota-
cional Ingeniería viable a = ω2R (no curvatura)

Gravedad análoga (meta) Experimental geff
µν solo para ondas
Warp drive clásico Teórico T 00 < 0 (Alcubierre)
κ(x) metamaterial Excluido Bianchi + |γ − 1| ≲ 10−5

CTCs / wormholes esta-
bles Protegidos Violación NEC + cronología

Acoplamiento EM
gravedad No detectado Límites ∼ nN

8. Consideraciones éticas y de seguridad

Cualquier tecnología que pretendiera alterar la causalidad o generar campos gravitatorios intensos
locales plantearía riesgos existenciales. Incluso en el dominio de las analogías, la experimentación
con densidades de energía extremas y horizontes efectivos debe regirse por protocolos estrictos. Todo
el trabajo aquí presentado se orienta al bene˝cio de la vida y a la reproducibilidad cientí˝ca.
 7

9. Conclusiones y recomendaciones

1. El control tecnológico real de la gravedad y del tiempo, más allá de los efectos relativistas cono-
cidos y de la gravedad arti˝cial rotacional, no es viable con la física actual ni con extensiones
razonablemente previsibles.

2. Las vías productivas son: (a) gravedad análoga de alta ˝delidad, (b) experimentos de precisión
sobre acoplamientos residuales, (c) IA para exploración sistemática de métricas con energía
positiva, (d) ingeniería de hábitats rotatorios.

3. Toda propuesta de metamaterial (incluidas las basadas en YIG) debe demostrar fuerzas med-
ibles sobre masas de prueba o modi˝caciones de relojes atómicos no explicables por efectos
electromagnéticos/térmicos ordinarios. Hasta la fecha no existen tales demostraciones.

4. Se recomienda mantener una distinción terminológica estricta entre analogía, simulación y
control real del espaciotiempo.

El horizonte de la física fundamental permanece abierto. La convergencia de herramientas
computacionales, nanofabricación y metamateriales permitirá explorar regímenes cada vez más in-
teresantes. Sin embargo, la viabilidad de un control efectivo de la gravedad y del tiempo sigue
perteneciendo, a día de hoy, al dominio de la especulación teórica rigurosa y de la ciencia ˝cción
informada.

Referencias seleccionadas y ecuaciones clave

‹ Einstein (1915): Ecuaciones de campo (1).

‹ Alcubierre (1994): Métrica (9).

‹ Morris & Thorne (1988): Métrica de agujero de gusano (18).

‹ Rodal (2025): arXiv:2507.09724  Inviabilidad de κ(x) metamaterial.

‹ Hawking: Conjetura de protección de la cronología.

‹ Desigualdades cuánticas: Ford & Roman, y trabajos posteriores.

‹ Experimentos de acoplamiento EMgravedad (Scienti˝c Reports 2024).

‹ Mediciones de corrimiento gravitatorio a escala mm (Nature Communications y sucesivos).

Informe elaborado con asistencia de inteligencia arti˝cial bajo supervisión y contraste del autor.
Todas las a˝rmaciones de factibilidad se basan en el estado del conocimiento cientí˝co publicado
hasta julio de 2026. Las ecuaciones se presentan en forma estándar; las implementaciones numéricas
concretas requieren códigos especializados (Einstein Toolkit, FDTD, etc.).
 8
