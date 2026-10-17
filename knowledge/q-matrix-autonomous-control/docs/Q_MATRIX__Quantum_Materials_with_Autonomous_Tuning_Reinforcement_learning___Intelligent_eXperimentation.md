> Texto extraído automáticamente del PDF original «Q_MATRIX__Quantum_Materials_with_Autonomous_Tuning_Reinforcement_learning___Intelligent_eXperimentation.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1REDW7nFKDCRFeHd_Y_giuRvcaqSTmmiw/view?usp=drivesdk



Q-MATRIX Quantum Materials with
Autonomous Tuning Reinforcement learning
Intelligent eXperimentation

L´azaro L´opez Paz y realizado por Grok IA Prat de Llobregat, Barcelona, Espa˜na

May 2026

Abstract

Este trabajo presenta una plataforma integral de materiales 2D basada
en nitruro de boro (h-BN), dicalcogenuros de metales de transici´on (WS2,
MoS2) y grafeno defectuoso. Se integran defectos cu´anticos de spin, po-
laritones hiperb´olicos, valleytronics, terapia BNCT, composites multifun-
cionales y control aut´onomo mediante Graph Neural Networks con Active
Learning y Reinforcement Learning. Se proponen cinco inventos nove-
dosos, protocolos realizables hoy, simulaciones computacionales y explo-
raci´on exhaustiva de aplicaciones. Las integraciones completas son origi-
nales y no se encuentran patentadas como sistemas cerrados hasta 2026.

Palabras clave: h-BN, WS2, valleytronics, grafeno defectuoso, defectos de
spin, polaritones hiperb´olicos, Active Learning, BNCT inteligente.

1 Introducci´on

Se consolida todo el conocimiento desarrollado: desde propiedades b´asicas del
BN hasta sistemas h´ıbridos avanzados con TMDs y grafeno defectuoso opti-
mizados por IA.

2 Fundamentos de Materiales 2D

2.1 Nitruro de Boro (h-BN y derivados)

Aislante de banda ancha, alta conductividad t´ermica, polaritones hiperb´olicos,
defectos V−
B estables a temperatura ambiente.

2.2 WS2 y Valleytronics

Mayor acoplamiento spin-´orbita que MoS2, control de valles K/K’ con luz po-
larizada, ideal para valley qubits y spin-valley locking en heteroestructuras con
h-BN.
 1

2.3 MoS2

Semiconductor tunable, piezoelectricidad, optoelectr´onica.

2.4 Grafeno Defectuoso

Defectos (vacancias, dopaje) crean estados localizados para spins y single-photon
emitters. Excelente como capa conductora o interfaz en heteroestructuras.

3 Ecuaciones Fundamentales

Hamiltoniano para V
−
B:

ˆH = D ( ˆS2
z − 2
3
 ) + E( ˆS2
x − ˆS2
y ) + γeB · S + ∑

k Ak · S (1)

ODMR: f± = D ± √E2 + (γeB cos θ)2 (2)

Polaritones hiperb´olicos:

qHPhP = i
d
 √ εzz
εxx
 (2 arctan ( i
εeff
 ) + πL) (3)

Recompensa RL con Active Learning:

R = w1CODMR + w2T2 + w3 valley − coherencia − λ costo

4 Espectroscop´ıa ODMR (Optically Detected Mag-
netic Resonance)

La espectroscop´ıa ODMR es una t´ecnica h´ıbrida que combina excitaci´on ´optica
y resonancia magn´etica, permitiendo detectar transiciones de spin a trav´es de
cambios en la intensidad de fluorescencia. Sus principales ventajas son:

• Funcionamiento a temperatura ambiente (esencial para h-BN).

• Alta sensibilidad, capaz de detectar spines individuales.

• Resoluci´on espacial a escala nanom´etrica mediante microscop´ıa confocal.

• Compatibilidad con bio-imagen y detecci´on qu´ımica.

2

4.1 Mecanismo en el centro V
−
B de h-BN

El defecto V
−
B presenta un estado fundamental de spin-1 con estructura triplet.
El bombeo ´optico polariza preferentemente el spin en ms = 0. Al aplicar mi-
croondas en resonancia con las transiciones ms = 0 ↔ ms = ±1, la poblaci´on se
transfiere a estados oscuros, reduciendo la fotoluminiscencia. Se observan dos
picos caracter´ısticos (f+ y f−) centrados alrededor de D ≈ 3.47 GHz.
El Hamiltoniano efectivo es:

ˆH = D ( ˆS2
z − 2
3
 ) + E( ˆS2
x − ˆS2
y ) + γeB · S, (5)

donde D ≈ 3.47 GHz es el desdoblamiento axial, E el t´ermino de strain o campo
el´ectrico (0−−200 MHz), y γe ≈ 28 GHz/T el factor giromagn´etico.
Las frecuencias de resonancia vienen dadas por la ecuaci´on mostrada en la
secci´on anterior.

4.2 Interpretaci´on del espectro

• N´umero de picos: 2 para spin-1 con E ̸= 0.

• Posici´on central ≈ 3.47 GHz confirma la presencia de V
−
B.

• El desdoblamiento E codifica informaci´on sobre el entorno local (strain,
campos el´ectricos).

• La separaci´on Zeeman lineal con B permite magnetometr´ıa vectorial de
alta precisi´on (∼ µT /√Hz en nanotubos de BN).

• En heteroestructuras h-BN/WS2, efectos de strain interfacial y acoplamiento
spin-valle modifican el espectro.

4.3 Simulaci´on del espectro ODMR

La figura 1 muestra un barrido del campo magn´etico calculado con QuTiP. Se
emplean los par´ametros t´ıpicos del V
−
B y se barren campos de 0 a 20 mT.
[caption=Barrido de campo magn´etico para simular el espectro ODMR del
defecto V−
B., label=lst:odmrsim]importnumpyasnpf romqutipimport∗importmatplotlib.pyplotasplt
D = 3.47e9 E = 60e6 gammae = 28e9Bvalues = np.linspace(0, 0.02, 100)Barridodecampo
fplus = []fminus = []
for B in Bvalues : H = D ∗ (jmat(1,′ z′) ∗ ∗2 − 2/3) + E ∗ (jmat(1,′ x′) ∗ ∗2 −
jmat(1,′ y′)∗∗2)+gammae∗B∗jmat(1,′ z′)evals = H.eigenenergies()fplus.append((evals[1]−
evals[0])/1e9)fminus.append((evals[2] − evals[0])/1e9)
plt.figure(figsize=(10,6)) plt.plot(Bvalues∗1000, fplus,
′ b−
′, label =
′ f +
′)plt.plot(Bvalues∗
1000, fminus,
′ r−
′, label =
′ f −
′)plt.xlabel(′Campomagn´eticoB(mT )
′)plt.ylabel(
′F recuenciaODM R(GHz)
′)plt.title(′EspectroODM Rsimuladodeldef ectoV −
B enh−
BN ′)plt.legend()plt.grid(T rue)plt.savef ig(′odmrspectrum.png′, dpi = 400)plt.show()
Los resultados t´ıpicos muestran una separaci´on de 2E a campo nulo y un
desdoblamiento lineal con B. La anchura experimental est´a limitada por la
decoherencia T ∗
2 (10–50 MHz).
 3

odmr_spectrum.png

Figure 1: Espectro ODMR simulado: frecuencias f+ y f− en funci´on del campo
magn´etico aplicado. A campo cero, el splitting est´a determinado por el strain
E.
 4

4.4 Aplicaciones en los inventos propuestos

• Quantum Defect Foundry: ODMR como se˜nal de feedback en tiempo
real para el bucle de Active Learning.

• Sensores BNCT++: Detecci´on de cambios qu´ımicos locales (acumu-
laci´on de 10B) mediante desplazamientos en el espectro.

• Metamateriales cu´anticos: Acoplamiento de la se˜nal ODMR con po-
laritones hiperb´olicos para control coherente.

• Valleytronics en WS2: Lectura h´ıbrida spin-valle combinando ODMR
y dicro´ısmo circular.

• Grafeno defectuoso: Espectros ODMR comparativos para calibraci´on
de entornos de spin.

5 An´alisis de Decoherencia en Defectos de h-BN

5.1 Introducci´on a la decoherencia

La decoherencia es el proceso por el cual un sistema cu´antico pierde su coheren-
cia (superposici´on e interferencia) debido a la interacci´on con el entorno. En los
defectos de spin en h-BN, especialmente V−
B, constituye uno de los principales
desaf´ıos para las aplicaciones cu´anticas a temperatura ambiente. Los tiempos
caracter´ısticos son:

• T1 (relajaci´on longitudinal): tiempo de relajaci´on de poblaci´on entre nive-
les de spin.

• T ∗
2 (decoherencia libre): tiempo de decaimiento de coherencia incluyendo
inhomogeneidades.

• T2 (tiempo de coherencia echo): coherencia real con pulsos de refocal-
izaci´on.

Valores t´ıpicos reportados (2024-2026) en h-BN:

• T1 ≈ 10−−100 µs a temperatura ambiente.

• T ∗
2 ≈ 1−−10 µs.

• T2 (con eco) ≈ 20−−200 µs (mejorable mediante isotop´ıa y strain).

5.2 Fuentes principales de decoherencia en V
−
B de h-BN

La tabla 1 resume los mecanismos que afectan la coherencia y su mitigaci´on.

5

5.3 Simulaci´on con decoherencia Lindblad

Para ilustrar el efecto de la decoherencia, se modela el sistema con el formalismo
de Lindblad. El c´odigo siguiente (lista ??) emplea T1 = 20 µs y T ∗
2 = 3 µs,
produciendo la evoluci´on de ⟨Sz⟩ mostrada en la figura 2.
[caption=Simulaci´on de decoherencia Lindblad en V−
B., label=lst:decoherencef ull]importnumpyasnpf romqutipimport∗
importmatplotlib.pyplotasplt
Par´ametros D = 3.47e9 E = 60e6 gammae = 28e9B = 0.005
Hamiltoniano spin sz = jmat(1, ’z’) H = D*(sz**2 - 2/3) + E*(jmat(1,’x’)**2
- jmat(1,’y’)**2) + gammae ∗ B ∗ sz
Decoherencia Lindblad T1 = 20e-6 Relajaci´on T2 = 3e-6 Coherencia (T2*
aproximado)
gamma1 = 1/T1 gammaphi = 1/T 2 − 0.5/T 1
cops = [np.sqrt(gamma1)∗sz, Relajaci´onnp.sqrt(2∗gammaphi)∗szDephasingpura]
Evoluci´on psi0 = basis(3, 0) times = np.linspace(0, 15e-6, 1000) result =
mesolve(H, psi0, times, cops = cops, eops = [sz])
Gr´afica plt.figure(figsize=(10,6)) plt.plot(times*1e6, result.expect[0], ’b-’, linewidth=2.5,
label=r’⟨Sz⟩’) plt.axhline(y=0, color=’k’, linestyle=’–’, alpha=0.5) plt.xlabel(’Tiempo
(s)’) plt.ylabel(’Valor esperado 〈Sz〉’) plt.title(’Decoherencia en Defecto V
−
Bdeh−
BN (T = 20s, T ∗ = 3s)
′)plt.legend()plt.grid(T rue)plt.savef ig(′decoherencialindbladhbn.png′, dpi =
400)plt.show()

5.4 Simulaci´on de Secuencia de Eco Hahn

La secuencia de Eco Hahn es una t´ecnica est´andar de refocalizaci´on que permite
recuperar la coherencia perdida por inhomogeneidades est´aticas. Consiste en
un pulso π/2 que crea una superposici´on, seguido de evoluci´on libre durante un
tiempo τ , un pulso π que invierte la fase, otra evoluci´on libre de τ y finalmente
la medici´on del eco (reaparici´on de coherencia). Con ello se extiende el tiempo
coherente de T ∗
2 a T2.
El siguiente c´odigo implementa la secuencia de Eco Hahn en el mismo defecto
V−
B considerando los mismos par´ametros de decoherencia. La figura 3 muestra
la se˜nal de eco en funci´on de τ , donde se observa un decaimiento m´as lento que
la evoluci´on libre.
[caption=Simulaci´on de la secuencia de Eco Hahn en V
−
B., label=lst:hahnecho]importnumpyasnpf romqutipimport∗
importmatplotlib.pyplotasplt
====================== PAR ´AMETROS ======================
D = 3.47e9 Zero-field splitting E = 60e6 Strain gammae = 28e9B = 0.005Campomagn´etico(mT )
Hamiltoniano sz = jmat(1, ’z’) sx = jmat(1, ’x’) sy = jmat(1, ’y’) H =
D*(sz**2 - 2/3) + E*(sx**2 - sy**2) + gammae ∗ B ∗ sz
Decoherencia T1 = 25e-6 T2star = 2.5e-6 gamma1 = 1/T1 gammaphi =
1/T 2star − 0.5/T 1
cops = [np.sqrt(gamma1)∗sz, Relajaci´onnp.sqrt(2∗gammaphi)∗szDephasing]
Estado inicial psi0 = basis(3, 0)
Tiempos de evoluci´on taulist = np.linspace(0.1e−6, 12e−6, 80)desde0.1hasta12sechosignal =
[]
 6

Table 1: Fuentes de decoherencia y estrategias de mitigaci´on.
Fuente Tipo Efecto principal Mitigaci´on
Ba˜no de spins
nucleares (
11B,
14N)
 Fluctuaciones
magn´eticas Dephasing (T ∗
2 ) Isotop´ıa enriquecida
(
10B, 15N)

Fonones Interacci´on
spin-fon´on Relajaci´on (T1) y de-
phasing Baja temperatura o
strain engineering
Ruido de carga Fluctuaciones
el´ectricas Dephasing v´ıa Stark
shift Encapsulaci´on (h-
BN/MoS2/WS2)
Ruido
magn´etico
externo
 Campos fluctu-
antes Dephasing Blindaje + control ac-
tivo

Impurezas y de-
fectos cercanos Interacciones lo-
cales Inhomogeneidad Ingenier´ıa precisa de
defectos

decoherencia_lindblad_hbn.png

Figure 2: Decaimiento de la coherencia en el defecto V
−
B bajo relajaci´on y
dephasing. La envolvente muestra la p´erdida de coherencia en la escala de
microsegundos.
 7

for tau in taulist : P ulso/2alrededordeXUpi2 = (−1j∗np.pi/2∗sx).expm()psi =
Upi2 ∗ psi0
Evoluci´on libre psi = mesolve(H, psi, [0, tau], cops = cops).states[−1]
Pulso alrededor de Y Upi = (−1j ∗ np.pi ∗ sy).expm()psi = Upi ∗ psi
Evoluci´on libre psi = mesolve(H, psi, [0, tau], cops = cops).states[−1]
Medir ¡Sz¿ al final del eco echosignal.append(expect(sz, psi))
====================== GR ´AFICA ======================
plt.figure(figsize=(11, 7)) plt.plot(taulist ∗ 1e6, echosignal,
′ b − o
′, linewidth =
2.2, markersize = 4, label =′ Se˜naldeEcoHahn′)plt.axhline(y = 0, color =
′

k′, linestyle =
′ −−
′, alpha = 0.6)plt.xlabel(
′T iempo(s)
′)plt.ylabel(
′<Sz>aleco
′)plt.title(′Simulaci´ondeSecuenciadeEcoHahnenDef ectoV −
B deh−
BN (T = 25s, T ∗ = 2.5s)
′)plt.legend()plt.grid(T rue, alpha = 0.3)plt.savef ig(
′hahnechohbn.png′, dpi =
400, bboxinches =
′ tight
′)plt.show()
print(”Simulaci´on de Eco Hahn completada.”)
Con esta t´ecnica, T2 (eco) t´ıpicamente alcanza valores entre 20 y 200 µs, lo
que representa una mejora de 5 a 10 veces sobre T ∗
2 .

5.5 Secuencias CPMG Avanzadas

Las secuencias CPMG (Carr-Purcell-Meiboom-Gill) extienden el concepto de
eco de Hahn mediante m´ultiples pulsos de refocalizaci´on π intercalados con
evoluciones libres de duraci´on 2τ . Esto permite filtrar ruidos de baja frecuencia
y alargar a´un m´as el tiempo de coherencia efectivo. La simulaci´on mostrada
en el listado ?? eval´ua la coherencia remanente ⟨Sz⟩ tras aplicar n pulsos π
(con n = 1, 4, 8, 16, 32) en funci´on del tiempo interpulsos τ . Los resultados se
presentan en la figura 4.
[caption=Simulaci´on de secuencias CPMG con distinto n´umero de pulsos.,
label=lst:cpmg] import numpy as np from qutip import * import matplotlib.pyplot
as plt
====================== PAR ´AMETROS ======================
D = 3.47e9 E = 60e6 gammae = 28e9B = 0.005
sz = jmat(1, ’z’) sx = jmat(1, ’x’) sy = jmat(1, ’y’) H = D*(sz**2 - 2/3) +
E*(sx**2 - sy**2) + gammae ∗ B ∗ sz
Decoherencia realista T1 = 25e-6 T2star = 2.0e-6 gamma1 = 1/T1 gammaphi =
1/T 2star − 0.5/T 1
cops = [np.sqrt(gamma1) ∗ sz, np.sqrt(2 ∗ gammaphi) ∗ sz]
psi0 = basis(3, 0)
Par´ametros CPMG totaltime = 20e−6npulseslist = [1, 4, 8, 16, 32]N ´umerodepulsostauvalues =
np.linspace(0.2e − 6, 8e − 6, 60)
coherenceresults =
for n in npulseslist : signal = []f ortauintauvalues : ttotal = 2 ∗ n ∗
tauif ttotal > totaltime : signal.append(0)continue
psi = psi0
Pulso /2 inicial (X) psi = (-1j * np.pi/2 * sx).expm() * psi
for i in range(n): Evoluci´on libre psi = mesolve(H, psi, [0, tau], cops =
cops).states[−1]
Pulso (Y) psi = (-1j * np.pi * sy).expm() * psi

8

hahn_echo_hbn.png

Figure 3: Se˜nal de eco de Hahn para el centro V−
B. La refocalizaci´on permite
recuperar la coherencia hasta tiempos de vuelo 2τ mucho mayores que T ∗
2 .

9

Evoluci´on libre psi = mesolve(H, psi, [0, tau], cops = cops).states[−1]
Medir coherencia ¡Sz¿ signal.append(expect(sz, psi))
coherenceresults[n] = signal
====================== GR ´AFICA ======================
plt.figure(figsize=(12, 8)) colors = [’blue’, ’orange’, ’green’, ’red’, ’purple’]
for i, n in enumerate(npulseslist) : plt.plot(tauvalues∗1e6, coherenceresults[n], color =
colors[i], linewidth = 2.2, marker =
′ o′, markersize = 3, label = f ′CP M G(n =
npulsos)
′)
plt.xlabel(’Tiempo interpulsos (s)’) plt.ylabel(’〈Sz>alf inaldelasecuencia
′)plt.title(′SecuenciasCP M GAvanzadasenDef ectoV −
B deh−
BN (T = 25s, T ∗ = 2s)
′)plt.legend()plt.grid(T rue, alpha = 0.3)plt.savef ig(
′cpmgadvancedhbn.png′, dpi =
400, bboxinches =
′ tight
′)plt.show()
print(”Simulaci´on CPMG avanzada completada.”)
La secuencia CPMG demuestra que con un n´umero suficiente de pulsos de
refocalizaci´on se pueden alcanzar tiempos de coherencia notablemente extendi-
dos, lo cual es crucial para aplicaciones de sensing y puertas cu´anticas en los
inventos propuestos.

5.6 Impacto en los sistemas propuestos

• Quantum Defect Foundry: La decoherencia limita el tiempo de op-
eraci´on → Active Learning debe optimizar strain y posici´on de defectos
para maximizar T2.

• Metamateriales Hiperb´olicos: El acoplamiento spin-polarit´on compite
con la decoherencia → se necesita r´egimen de acoplamiento fuerte (g >
tasa de decoherencia).

• BNCT++: La decoherencia reduce la sensibilidad temporal → se em-
plean ensembles de defectos o secuencias de eco.

• Valleytronics en WS2: El SOC ayuda, pero la decoherencia del valle
es otro desaf´ıo (mitigable con encapsulaci´on en h-BN).

• Reservoir Computing: La decoherencia natural puede ser beneficiosa
(proporciona “fading memory”).

5.7 Estrategias de mitigaci´on prioritarias

1. Isotop´ıa enriquecida (
1
 10

cpmg_advanced_hbn.png

Figure 4: Coherencia remanente tras secuencias CPMG con distinto n´umero de
pulsos. Un mayor n permite mantener la coherencia hasta valores de τ m´as
largos, reflejando una extensi´on del tiempo de coherencia efectivo.

11
