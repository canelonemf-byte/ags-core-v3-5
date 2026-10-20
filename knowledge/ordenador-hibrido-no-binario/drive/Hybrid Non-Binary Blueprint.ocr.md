<!-- Fuente: Hybrid Non-Binary Blueprint.pptx (copia de Drive en Downloads). Texto por OCR tesseract spa+eng; puede contener errores de reconocimiento. -->

## s01
HYBRID
NON-BINARY
COMPUTING

A Blueprint for Ultra-Low Power
Heterogeneous Architectures

DOCUMENT REF: Feasibility Study & R&D Master Plan
VERSION: 1.0 (Definitive for Implementation)

TARGET HORIZON: 2026 - 2040

CLASSIFICATION: Technical Baseline

(Gemini Notebook

## s02
Moving Past the Hype:
The Three Theses of Feasibility

Thesis A (Rejected) Thesis B (Validated) Thesis C (The Roadmap)
Universal Non-Binary Replacement Localized Hybrid Acceleration | Full-System Integration

Physically and economically implausible. Highly viable. Using non-binary representatio | Requires an 8-14 year industrial R&D

pipeline. The challenge is software
compilation and ADC/DAC overhead, not
| breaking the laws of physics.

Multi-level logic cannot globally beat binary ns strictly where device physics naturally
CMOS in density, ecosystem compatibility, support them (resistive memory, optical phase)

and signal robustness simultaneously.

drastically reduces data-movement energy.

An Gemini Notebook

## s03
Thermodynamic Reality:
The Extended Landauer Limit

Boltzmann constant Absolute Temperature (300K)
(1.38 x 10-23 J/K)

E Landauer (b) = kT In(b)

Because a base-b digit carries log2(b) bits of

P information, the energy per normalized bit is always: dad Base
KT In(b) (e.g., Binary = 2,

[ | = kT In(2) Quaternary = 4)

log2(b)

Non-binary logic does not cheat thermodynamics. At 300K, the minimum

energy per bit remains ~17.9 meV (2.87 zJ). The actual energy savings
must come from eliminating data movement, not violating physics.

MGeminiNotebook

## s04
The Engineering Bottleneck:
Noise Margins vs. Multilevel Logic

Thermal noise standard deviation: sigma = sqrt(kT/C) ~ 2.04 mV (at T=300K, C=1fF)

Ideal Separation at Vpp = 0.5V
Mer TASA AS
aseos) AVE o
(3 Ea [AV =1O7HV precisa Limit)
4 6 mn) ANE Zi (Frage const if noise)
Sot — [AV=33mV enviale at room temp)

Voltage-based multi-level logic beyond b=4 is highly fragile at 3@@K without
increasing capacitance, which would linearly increase dynamic energy (1/2 C V*2).

(Gemini Notebook

## s05
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

(Gemini Notebook

## s06
Evolutionary Circuit Design:
Quaternary (b=4) Logic Synthesis

def fitness(self, ind):
V, C, R, area = ind
delay = 2.2 * R * C * 1e-3
energy = C * (Vxe«2)
penalty = 0.0 if (V / 3.0) > 0.05 else 180.0
cost = (1.5 * delay) + (2.0 * energy) + (1.0 * area) + penalty
return 1.0 / (1.0 + cost)

Multi-objective optimization minimizes: Delay (ps), Energy
(fJ), and Area (um*2).

Strict noise margin penalties guarantee a minimum 50mV
separation between the 4 quaternary voltage states.

(Gemini Notebook

## s07
Thermal Dynamics:

Transient Heat Transfer Modeling

ooo

def thermal_diffusion_model(T, t, P_diss, C_therm, k_cool, T_amb): i

return (P_diss / C_therm) - k_cool * (T - T_amb)

# Binary CMOS: High Dissipation (9.8 W/mm*2)

# Hybrid Multi-Level: Optimized Dissipation (0.2 W/mm*2)

CMOS Baseline Results Matrix Hybrid Architecture

High data-movement energy leads to hotspots.

Compute-In-Memory (CIM) eliminates the memory
wall, drastically lowering P_diss.

Takeaway: Thermal efficiency is not magic; it is the direct mathematical result of reducing the alpha * C_eff * V_DD*2
switching factor by keeping data stationary in memristor arrays.

J

(Gemini Notebook

## s08
The Heterogeneous Architecture Blueprint

The Al Scheduler: An intelligent compiler layer mapping operations to the most physically efficient domain in real-time.

—
—
Y
= z AA Vi PP ==
= í SF 1 Sr
Binary CMOS Core (Control) 8-Level RRAM CIM (Compute-in-Memory) Photonic Interconnects (Data Fabric)
Standard binary precision for OS, irregular HfO2 crossbars performing ultra-low power LINDO3 optical modulators routing massive data lots
code, and general-purpose routing. vector-matrix multiplications natively in analog. between chiplets without capacitive wire penalties.

(Gemini Notebook

## s09
Operational Flow:

CLASSIFIED UEG ENGINEERING BLUEPRINT

tt!

GEMM Lifecycle in a Hybrid System

Ingestion & Compilation
(Binary)

Optical Transport
(Photonics)

a
In-Memory Compute
(Multilevel RRAM)

Re-Digitization & Control

(Binary)

The runtime receives an
8-bit precision matrix
multiplication task. The
compiler maps weights to
quaternary/octal
conductances.

Activations are transmitted
across the module via silicon
photonics to avoid copper
interconnect resistance.

Hf02 crossbars execute the
Multiply-Accumulate (MAC)
operation instantaneously
via Ohm's and Kirchhoff's
laws.

ADCs deliver the binary
tensor back to the CMOS CPU
for non-linear activations
and OS handoff.

(Gemini Notebook


## s10
CLASSIFIED UEB ENGINEERING BLUEPRINT

eZ,

Cleanroom Fabrication Protocol

1. Substrate Preparation:
High-purity Si wafer with
300nm thermal oxide

(Si02/Si). RCA cleaning.

2. 2D Material Growth:
Chemical Vapor Deposition
(CVD) of MoS2 at 750
using Mo03 and sulfur
precursors.

3. Memristor Integration
(ALD): Atomic Layer
Deposition of 10nm
Hafnium Oxide (HfO2) at
250C. E-beam lithography
for PUTI electrodes.

4. Photonic Etching:
ICP-RIE plasma etching
on Lithium Niobate
(LiNbO3) layers for
single-mode waveguides
and modulators.

5. Hybrid Packaging: Laser
dicing and ultrasonic wire-
bonding to high-frequency
PGA ceramics (2.5D/3D
integration).

(Gemini Notebook


## s11
CLASSIFIED UEB ENGINEERING BLUEPRINT

Projected System Objectives vs. CMOS Baseline

Metric CMOS Baseline Hybrid Objective
Energy per Task (Normalized) 1.0 <= 0.4
Performance per Watt 1.0 >= 2.0

<= il, i

End-to-End Latency 1.0 Hate,
Application Precision % di
(Accuracy) Reference 1% difference
Temperature Delta Reference 20% reduction

The goal is not universal supremacy. CMOS retains density and programmability. The
hybrid system targets a 60% reduction in energy strictly for dense matrix workloads.

(Gemini Notebook

## s12
= = Ñ CLASSIFIED UEB ENGINEERING BLUEPRINT

Falsifiability £ & > Diagnostic Risk Matrix

“ unstable at 85C.

Statistical characterization,
differential coding, and fallback to
2-bit PIM if 8-level proves

= Co-design of mixed-signal
Conversion energy wipes out all precision; strict ‘go/no-go’ criteria
AN ADC/DAC Dominance _ in-memory compute savings. at the tile-measurement level
> a (Phase 2).

E/O conversion costs exceed
copper links at short distances.

Photonics strictly reserved for
high-bandwidth, inter-chiplet
routing above validated distance
thresholds.

Gemini Notebook

## s13
CLASSIFIED UEB ENGINEERING BLUEPRINT

The 250M Euro RSD Master Plan (14-Year Horizon)

TOTAL BUDGET:
250,000,000 EUR

Simulation & Material
Screening. Repositories,
QiskiVQE modeling,
establishing CMOS
baselines.

Phase 2 (Years 3-6) | 45M Euro Sg
ee |

Elemental Devices.
Manufacturing TFETs
and Hf02 memristors.
Measuring I-V curves
and multilevel retention.

Phase 3 (Years 6-9) | 60M Euro A. pill J
APM
uu A

My

Circuit & CIM Accelerator.
Synthesizing quaternary logic
gates. Analog vector-matrix
prototype.

Phase 4 (Years 9-12) | 80M Euro 4a ;

Photonic Integration.
LiNbO3 on-chip routing,
electro-optical interfaces,
and thermal sensors.

Full System Assembly. 2.5D/3D packaging, full-stack
compilation, and industrial benchmarking.

An uncompromising, physics-grounded pathway from thermodynamic theory to a qualified industrial product.

(Gemini Notebook
