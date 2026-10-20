<!-- Fuente: Hybrid Non-Binary Blueprint.pdf (copia de Drive en Downloads). Texto por OCR tesseract spa+eng; puede contener errores de reconocimiento. -->

## p-01
HYBRID
NON-BINARY
COMPUTING

A Blueprint for Ultra-Low Power
Heterogeneous Architectures

DOCUMENT REF:
VERSION:
TARGET HORIZON:

CLASSIFICATION:

Feasibility Study € RED Master Plan
1.0 (Definitive for Implementation)

2026 - 2040

Technical Baseline

e

fm Gemini Notebook

## p-02
Moving Past the Hype:

The Three Theses of Feasibility

Thesis A (Rejected)

Universal Non-Binary Replacement

Physically and economically implausible.
Multi-level logic cannot globally beat binary
CMOS in density, ecosystem compatibility,

and signal robustness simultaneously.

BS —

Thesis B (Validated)

Localized Hybrid Acceleration

Highly viable. Using non-binary representatio
ns strictly where device physics naturally

support them (resistive memory, optical phase)
drastically reduces data-movement energy.

Thesis C (The Roadmap)

Full-System Integration

Requires an 8-14 year industrial R&D
pipeline. The challenge is software
compilation and ADC/DAC overhead, not
breaking the laws of physics.

Am Gemini Notebook

## p-03
Thermodynamic Reality:
The Extended Landauer Limit

Boltzmann constant | | Absolute Temperature (300K)

(1.38 x 10-23 J/K)

El andauer (0) = kT In(b)

Because a base-b digit carries log2(b) bits of | ber B
information, the energy per normalized bit is always: tn
kT In(b (e.g., Binary = 2,
| | n( a = kT In(2) Quaternary = 4)
| log2(b)

Non-binary logic does not cheat thermodynamics. At 300K, the minimum

energy per bit remains ~17.9 meV (2.87 zJ). The actual energy savings
must come from eliminating data movement, not violating physics.


## p-04
The Engineering Bottleneck:
Noise Margins vs. Multilevel Logic

Thermal noise standard deviation: sigma = sqrt(kT/C) ~ 2.04 mV (at T=300K, C=1fF)

Ideal Separation at Vp, = 0.5V >) |
on AV=500mV| Ropu
4 e Els AV= mV tFragieeeanst if noise)
5 /(apitsy  [2V=33mW | (Unviabie at room temp)
Voltage-based multi-level logic beyond b=4 is highly fragile at 300K without

increasing capacitance, which would linearly increase dynamic energy (1/2 C V*2).

fm Gemini Notebook

## p-05
Algorithmic Material Discovery:
MoS2 and Sulfur Vacancies

def vqe_energy_expectation(params, kx, ky):
# Variational circuit for MoS2 tight-binding model

U = np.array([[np.cos(theta_0)...]])
H4x4 = np.kron(hamiltonian_2d(kx, ky), np.eye(2))
return np.vdot(state, np.dot(H4x4, state)).real

Transition Metal Dichalcogenides (TMDs) like MoS2 provide
sub-nanometer channels. Sulfur vacancies—often viewed as
defects—are computationally screened here to engineer tunable

resistive states for non-binary switching at Vpp < 0.3V.

## p-06
Evolutionary Circuit Design:
Quaternary (b=4) Logic Synthesis

def fitness(self, ind):

V, C, R, area = ind

delay = 2.2 * R * C * le-3

energy = C * (Vxx2)

penalty = 0.0 if (V / 3.0) > 0.05 else 160.0

cost = (1.5 * delay) + (2.0 * energy) + (1.0 * area) + penalty
return 1.0 / (1.0 + cost)

Multi-objective optimization minimizes: Delay (ps), Energy
(fJ), and Area (um*2).

Strict noise margin penalties guarantee a minimum 50mV
separation between the 4 quaternary voltage states.


## p-07
Thermal Dynamics:
Transient Heat Transfer Modeling

eee

>

def thermal_diffusion_model(T, t, P_diss, C_therm, k_cool, T_amb): 3
return (P_diss / C_therm) - k_cool * (T - T_amb)

# Binary CMOS: High Dissipation (0.8 W/mm*2)
# Hybrid Multi-Level: Optimized Dissipation (0.2 W/mm*2)

7

e

=, JT

CMOS Baseline Results Matrix Hybrid Architecture

High data-movement energy leads to hotspots.

| Compute-In-Memory (CIM) eliminates the memory
wall, drastically lowering P_diss.

y

switching factor by keeping data stationary in memristor arrays.

Takeaway: Thermal efficiency is not magic; it is the direct mathematical result of reducing the alpha * C_eff * V_DD*2 ]

fm Gemini Notebook

## p-08
The Heterogeneous Architecture Blueprint

The Al Scheduler: An intelligent compiler layer mapping operations to the most physically efficient domain in real-time.

eee as eee - \
g " Ñ _ E : a j \
= y) |
= t y
4 i va >
7 Se á A E
Y A | t
i ‘
— if 3 -. a = 4 —
li A 4 | | 74 FS | ==
le » / 4 ts > | . 4, Aa | eer Sl SS me e
|
J — } | :
= recon | A ==
= A 5 7 po + ™
Binary CMOS Core (Control) 8-Level RRAM CIM (Compute-in-Memory) Photonic Interconnects (Data Fabric)
Standard binary precision for OS, irregular HfO2 crossbars performing ultra-low power LINbO3 optical modulators routing massive data lots
code, and general-purpose routing. vector-matrix multiplications natively in analog. between chiplets without capacitive wire penalties.
k y L j L Jj
fm Gemini Notebook


## p-09
Operational Flow:

CLASSIFIED UE6 ENGINEERING BLUEPRINT

GEMM Lifecycle in a Hybrid System

Ingestion & Compilation

The runtime receives an
8-bit precision matrix
multiplication task. The
compiler maps weights to
quaternary/octal
conductances.

Optical Transport
(Photonics)

Activations are transmitted
across the module via silicon
photonics to avoid copper
interconnect resistance.

In-Memory Compute
(Multilevel RRAM)

HfO2 crossbars execute the
Multiply-Accumulate (MAC)
operation instantaneously
via Ohm's and Kirchhoff's
laws.

Re-Digitization & Control
(Binary)

ADCs deliver the binary
tensor back to the CMOS CPU

for non-linear activations
and OS handoff.


## p-10
AS ee CLASSIFIED UEB ENGINEERING BLUEPRINT ——— a

Cleanroom Fabrication Protocol

1. Substrate Preparation: 2. 2D Material Growth: 3. Memristor Integration 4. Photonic Etching: 5. Hybrid Packaging: Laser
High-purity Si wafer with Chemical Vapor Deposition (ALD): Atomic Layer ICP-RIE plasma etching dicing and ultrasonic wire-
300nm thermal oxide (CVD) of MoS2 at 750C Deposition of 10nm on Lithium Niobate bonding to high-frequency
(Si02/Si). RCA cleaning. using MoO3 and sulfur Hafnium Oxide (HfO2) at (LINbO3) layers for PGA ceramics (2.5D/3D
_ precursors. 250C. E-beam lithography single-mode waveguides integration).
for Pt/Ti electrodes. and modulators.


## p-11
CLASSIFIED UEB ENGINEERING BLUEPRINT

Projected System Objectives vs. CMOS Baseline

Metric CMOS Baseline Hybrid Objective

Energy per Task (Normalized) 1.0 <= 0.4
Performance per Watt 1.0 >= 2.0

<=
End-to-End Latency 1.0 Ada
Application Precision is
(Accuracy) Reference 1% difference

Temperature Delta Reference 20% reduction

The goal is not universal supremacy. CMOS retains density and programmability. The
hybrid system targets a 60% reduction in energy strictly for dense matrix workloads.

fm Gemini Notebook

## p-12
CLASSIFIED UEB ENGINEERING BLUEPRINT

Falsifiability 6 Diagnostic Risk Matrix

Consequence

High Bit Error Rate (BER) leading
to constant recalibration.

Mitigation

Statistical characterization,

differential coding, and fallback to

2-bit PIM if 8-level proves

_unstable at 85C.

; EG] Co-design of mixed-signal
: Ni Conversion energy wipes out all precision; strict ‘go/no-go’ criteria
AN ADC/DAC Dominance } in-memory compute savings. at the tile-measurement level
e 7-7 J (Phase 2).

E/O conversion costs exceed
copper links at short distances.

AN Photonic Overhead

Photonics strictly reserved for
high-bandwidth, inter-chiplet
routing above validated distance
thresholds.


## p-13
CLASSIFIED UEB ENGINEERING BLUEPRINT

The 250M Euro RSD Master Plan (14-Year Horizon)

Pats a) ee TOTAL BUDGET:
250,000,000 EUR

CASE

Phase 4 (Years 9-12) | 80M Euro A
~~

Photonic Integration.
LiNbO3 on-chip routing, Phase 5 (sus 12-14) | 50M Euro
SE EAS

electro-optical interfaces,
and thermal sensors.

Full System Assembly. 2.5D/3D packaging, full-stack
compilation, and industrial benchmarking.

Simulation & Material
Screening. Repositories,
Qiskit/VQE modeling,
establishing CMOS

baselines. Elemental Devices.
Manufacturing TFETs
and Hf02 memristors.
Measuring I-V curves

and multilevel retention. Circuit & CIM Accelerator.
Synthesizing quaternary logic
gates. Analog vector-matrix
prototype.

Phase 2 (Years 3-6

) | 45M Euro

:

An uncompromising, physics-grounded pathway from thermodynamic theory to a qualified industrial product.

