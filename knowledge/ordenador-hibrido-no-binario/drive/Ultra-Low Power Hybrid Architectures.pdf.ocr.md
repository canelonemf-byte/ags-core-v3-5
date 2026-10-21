> Nota de herramienta: Diapositivas generadas con Google Gemini NotebookLM; texto y contenido de Lázaro López Paz con asistencia de IA. Términos de uso de Google: PENDIENTE DE VERIFICACIÓN.

<!-- Fuente: Ultra-Low Power Hybrid Architectures.pdf (copia de Drive en Downloads). Texto por OCR tesseract spa+eng; puede contener errores de reconocimiento. -->

## p-01
Arquitectura
Hibrida
Multinivel de
Ultra-Bajo
Consumo

Límites físicos, diseño
de sistema y hoja de ruta
industrial (2026-2040)

ESTUDIO DE VIABILIDAD TÉCNICA Y PLAN DE
EJECUCIÓN AUDITABLE [VERSIÓN 1.0]

® Gemini Notebook

## p-02
El Arco de Síntesis: Desmitificación y Realidad

Tesis A: Reemplazo Global Tesis B: Ventaja Energética Local Tesis C: El Sistema Completo
La narrativa falsa. El prototipo plausible. El producto.
Un ordenador puramente no binario Aceleradores híbridos para cargas Convertir demostraciones en un SoC
que supera al CMOS en velocidad, frío y regulares. Reduce julios por operación comercial requiere más de una década
densidad a la vez. Físicamente útil combinando control binario con de integración 2.5D/3D, presupuestos
implausible a 15 años vista. Contradice matrices resistivas y tejido fotónico. de cientos de millones de euros y
la termodinámica del ruido y el rigurosos criterios de falsabilidad.

ecosistema de software.


## p-03
El Principio de Landauer Extendido: No Hay Atajos

-

—

El coste mínimo termodinámico para borrar un estado en base b es

casi = ica In bd.

0 1 4 ia (aly) PQ) = TA aly Portes
pri) Pbgeiter(21)) | — EG) = = (5 MA ARA)
=jkoP int E
a2 4

—

Dado que un dígito en base b transporta ba b bits de información...

La energía disipada por bit normalizada es:

kpT In b
logs b

= kpT In2 & 2.87 x 10 J (a 300K)

‘Dejar de ser binario’ no ahorra energia por bit de informacion. La ventaja debe provenir de
reducir el voltaje operativo o el movimiento fisico de datos, no de la base numérica magica.

fm Gemini Notebook


## p-04
La Fragilidad del Nivel Lógico (kT/C): La Lucha contra el Ruido

(\ »)
HUD DATA

| E
| [PARÁMETROS DEL NODO]

Capacidad: C =1fF

| Temp:
Voltaje:

T = 300 K
Vop = 0.5V

| [CÁLCULO DE MÁRGENES]
- Ruido térmico (0): pur = 2.04 mV

Separación (b=4): AV = a = 166.7 mV
Margen Señal/Ruido: AV ~ 83

(Garantiza BER < 10718) a

Takeaway: Nivel base b=4 es
viable con baja variabilidad.
Bases superiores (b=8, 16) colapsan yy)
físicamente ante el offset y mismatch del ¡+
silicio a temperatura ambiente.

C pal


## p-05
Ecosistema Físico: Inventario de Tecnologías

[TECNOLOGÍA] [ROL HONESTO & MADUREZ] [QUÉ NO SE LE PIDE (HYPE)]

CPU, control irregular, OS.

= CMOS Binario [Madurez: Foundry]

Que desaparezca. -

MAC in-memory, pesos analógicos.

[Madurez: Macros/Piloto] Una ALU exacta de 64 bits.

RRAM HfO_x (Multinivel)

Fotónica (LINbO_3 / SiPh) GEMM denso, transporte inter-chip. Control irregular de corto

[Madurez: PIC comerciales] alcance.
k Canal de bajo V;y futuro. Descubrimientos mágicos |
TMD / MoS_2 (Vacantes) [Madurez: Laboratorio] impulsados por lA.

Ciencia básica / Coprocesadores Bajar la temperatura de un

Cuántica / ADN lejanos. [Madurez: NISQ] portátil comercial.

| ft Gemini Notebook

## p-06
def

def

Fase 1: Simulación Cuántica de Materiales 2D

hamiltonian_2d(kx, ky, t=1.0, onsite=0.1, soc=0.05):
h_00 = onsite

h_11 = -onsite

h_@1 = t * (np.cos(kx) + np.cos(ky)) + 1j * soc

H = np.array([[h_00, h_01],
[np.conj(h_01), h_11]])
return H

vqe_energy_expectation(params, kx, ky):

# Circuito VQE para estimacion del estado fundamental
H4x4 = np.kron(hamiltonian_2d(kx, ky), np.eye(2))
state = np.dot(U(params), [1, 0, 0, 0])

return np.vdot(state, np.dot(H4x4, state)).real

\\

{ Objetivo: Cribado de brecha energética optima para
| transistores 2D (MoS_2).

Metodología: La lA y VQE actúan como buscadores de
parámetros y validación física (DFT/NEGF), no como

‘descubridores’ aislados de materiales.

7 AT Mm Gemini Notebook


## p-07
Síntesis de Lógica Cuaternaria: Optimización Genética

=

class GeneticGateOptimizer:

def fitness(self, ind):
V, C, R, area = ind

>| delay = 2.2*RxC

energy = C * (Vxx*2)

delta_v = V / 3.0

penalty = 0.0 if delta_v > 0.05 else 100.0

cost = (1.5*delay) + (2.0xenergy) + area + penalty

return 1.0 / (1.0 +

* le-3 # ps
# fJ

cost)

e

stricciones Físicas: La función de aptitud penaliza topologías
que no garantizan el margen de ruido base 4 (Delta V > 50 mV).
Salida: Celdas que operan en régimen no estándar (0.15 V - 0.35

V), equilibrando energía dinámica C(V,,)*2 y retardo.

0

+

~

ft Gemini Notebook

## p-08
La Arquitectura Maestra: Contrato entre Dominios

Control Binario (CMOS):
Gestiona el sistema
operativo, el código

irregular y el compilador IA.

Ejecuta aritmética exacta.

[Tecnología estándar]

Matriz Resistiva (HfO_2):
Computación In-Memory
(CIM). Multiplicación
matriz-vector analógica a
4-8 niveles de precisión
nativa.

[Núcleo de Aceleración]

—_—

Tejido Fotónico (SiPh): joa
Movimiento masivo de
datos entre mosaicos

distantes, superando el
superando el cuello de [=
botella capacitivo del cobre. q

[Autopista de Datos] h

Ne


## p-09
Flujo de Datos: Producto Matriz-Vector (GEMM)

1. Asignación (Binario)
El runtime recibe el lote a precisió
de 8-bits. Decide que el kernel baje

conductancias del HfO_2 mediante
algoritmos de pulsos con verificación


## p-10
Modelado Térmico Dinámico (ODE): La Física del Calor

ai
a A _ Baseline CMOS
thermal_model.py - SciPy P_diss = 0.8 W/mm2 >400 K
>. (Alto Calor)
“2 thermal_model.py “4
1 from scipy.integrate import odeint 2
2
3 def thermal_diffusion_model(T, t, P_diss, C_therm, k_cool, T_amb):
4 # Balance térmico del sustrato hibrido
5 dTdt = (P_diss / C_therm) - k_cool * (T - T_amb) J 298 K
6 return dTdt
7
8 # CMOS Baseline: P_diss = 0.8 W/mm2 Híbri ours
> ibrido Multinivel
9 temp_cmos = odeint(thermal_diffusion_model, 298, t, args=(0.8,...)) brido Mult c 328 K

. P_diss = 0.2 W/mm2
: (Calor Reducido)

<=

# Hybrid Target: P_diss = 0.2 W/mm2
temp_hybrid = odeint(thermal_diffusion_model, 298, t, args=(0.2,...))

3298 K

La temperatura no disminuye mágicamente por
cambiar de base. Se reduce al bajar la disipación
de potencia física (P_diss) moviendo menos datos.
Objetivo térmico: Operación sostenida < 55 *C.


## p-11
Protocolos de Fabricación en Cleanroom (Integración 2.5D/3D)

1. Sustrato 2. Canal 2D 9 3. Matriz Memristiva 4. Fotónica : 5. Packaging

Oblea Si con Si0_2 Deposición CVD de Deposición ALD de HfO_ Grabado ICP-RIE sobre |} Ensamblado 2.5D,
térmico. Limpieza MoS_2 a 750 °C. a 250 °C (10nm) y Yi capas LiNbO_3 para dicing laser y wire-
RCA estándar. Transferencia húmeda. litografía EBL para Pt/Ti. guías monomodo. J bonding a PGA.


## p-12
Métricas Objetivo: El Banco de Pruebas Prospectivo

dá Energía / Tarea Rendimiento / Vatio Latencia (End-to-End) Precisión de Red
2.0 1.2
Haas
As 99.8%) - -
>», Y a 1.0 1.0 | /. S
-60% 2x Eff +20% <1%

= : e (ADC/DAC ie

MW Wi <= EF OP

Toda ventaja debe medirse a nivel de tile o sistema incluyendo relojes, convertidores A/D y D/A, y controladores |
periféricos. NUNCA se debe aislar la celda memristiva ideal para proyectar eficiencias del sistema completo.
La latencia sufre una penalización calculada en el diseño híbrido que debe compensarse mediante un |
paralelismo extremo.

Degradación J

Nota de Rigor Metodológico:


## p-13
Hoja de Ruta Industrial (8-14 Años): Integración a Gran Escala

+ Sistema ensamblado,
calificación y validación.

Integración SiPh (fotónica) ss

y empaquetado. =
= :

E

A

INVERSIÓN TOTAL PROYECTADA:
‘© = 250 MILLONES DE EUROS

ntegración de circuitos
CIM, y compilador inicial.

“2” Fabricación dispositivos (=
elementales (TFET + Hf0_2)..

~ Modelado, materiales
2D, simulación base.

fm Gemini Notebook

## p-14
Criterios de Falsabilidad
y Gobernanza (No-Go)

Un plan de I+D sin criterios de
abandono públicos y cuantificables
no es ciencia, es un relato.

ABORTAR si la ventaja energética total (incluyendo
ADC/DAC y fotónica) no supera el 20% frente al
baseline CMOS binario actual.

ABORTAR si la deriva térmica o la variabilidad de
retención destruyen la tasa de error por encima del
umbral mitigable por ECC.

ABORTAR si la complejidad del compilador de IA
impide que un ingeniero de software estándar
despliegue un modelo real.

La meta es el rigor extremo, la reproducibilidad
trazable (objetivo E1) [corregido: original "reproducibilidad absoluta"] y la ventaja térmica estimada E1, no demostrada [corregido: original "supremacía térmica demostrada"].
Nada de magia, solo ingeniería profunda.

