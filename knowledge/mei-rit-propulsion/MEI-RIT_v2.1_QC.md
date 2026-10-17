# MEI-RIT v2.1-QC
Metasurface-Enhanced Iodine RF Ion Thruster — revisión con ordenadores cuánticos (acotada)

Autor: Lázaro López Paz · 2026-09-22 · pack: `llp/proyectos/MEI-RIT.json`

Fuente revisada: 3 DOCX Drive (ZIP truncado; `document.xml` extraído por inflate parcial). No se reescribió el esquema LLP.

---

## Veredicto

El concepto (GIT de RF + I₂ sólido + acoplador de campo + pasivado ALD) es coherente con el estado del arte 2022–2025 (ThrustMe NPT30-I2, Busek BIT-3, Lafleur et al. 2022, review IOP 2025).  

Tres fallos estructurales del pack v2.0:

1. **Escala EM incorrecta.** Periodo 8–18 μm (y 11.78 μm “integrado”) no es metasuperficie de RF a 13.56 MHz ni a 2.45 GHz.
2. **Números de rendimiento presentados como resultado** (1.12 mN, 2540 s, 18.5 mN/kW) sin mallado, solver, ni ensayo. Clase **E2**, no E3/E4.
3. **QC mal enfocado si se usa para Maxwell 3D.** El reenfoque VQE de I₂ del v2.0 es la única vía cuántica defendible. Se formaliza y se limita.

QC no “perfecciona el propulsor”. Acota química de huecos y busca topologías discretas. El EM y el PIC siguen clásicos.

---

## 1. Qué se conservó (no duplicar)

- Propelente I₂ sólido + sublimación.
- Cámara cuarzo HP / Al₂O₃.
- Conductor de patrón encapsulado ALD (Si₃N₄ o Al₂O₃) por sputtering de I⁺/I₂⁺.
- Rejillas de grafito pirolítico; 800–1500 V.
- Neutralizador (RF o cátodo hueco) obligatorio.
- MRCO sin `np.clip`; resonancia Lorentz + C parásita del dieléctrico.
- Bandas-objetivo de diseño: 50–80 W, 0.7–1.3 mN, 2300–2800 s, η 36–46 %.
- Plan 18 meses TRL2→TRL4.
- Claims de patente 1–10 (redibujar claim 1: periodo en **mm**, no μm).

## 2. Corrección de escala (conflicto resuelto)

| Magnitud | Valor | Implicación |
|---|---|---|
| λ₀ @ 13.56 MHz | 22.1 m | Periodo μm es 10⁶× sub-λ. No hay “resonancia de metasuperficie RF”. |
| λ₀ @ 2.45 GHz | 122 mm | Periodo útil de HIS/FSS: **3–15 mm** (p ≲ λ/8). |
| λ_D (T_e=4 eV, n_e=10¹⁷ m⁻³) | ~47 μm | 8–18 μm es escala de **vaina/Debye**, no de RF. |
| δ_s piel Al @ 13.56 MHz | ~22 μm | El metal de μm es espesor de piel, no periodo de array. |

Arquitectura dual-escala v2.1:

- **Escala RF (mm):** superficie de alta impedancia / electrodo ranurado / anillo de matching en la pared o en la tapa RF. Objetivo: Γ↓, uniformidad E_θ, ignición.
- **Escala plasma (μm, opcional):** textura ≤ λ_D bajo ALD. Hipótesis E1: γ_se y campo de vaina. No vender como metasuperficie RF.
- **Antena:** hélice/bobina ICP clásica + matching; la “metasuperficie” es auxiliar, no sustituye la bobina.

Claim 1 reescrito (fondo): periodo **3–15 mm**, fill 0.25–0.70, metal 5–50 μm **espesor**, dieléctrico ALD 50–300 nm.

## 3. Química de I₂ — hechos vs huecos

Hechos de literatura (E6 umbrales; tasas E4/E5 según fuente):

| Proceso | Umbral (eV) | Nota |
|---|---|---|
| I₂ + e → 2 I(²P_{3/2}) + e | 1.542 | Disociación. Domina a T_e ≲ 5 eV |
| I₂ + e → I₂⁺ + 2e | 9.31 | IP molecular |
| I₂ + e → I⁺ + I + 2e | 11.63 exp / 11.94 calc | Ionización disociativa |
| I + e → I⁺ + 2e | 10.45 | |
| I₂⁺ + e → I⁺ + I + e | 2.18 | |
| I₂ + e → I⁻ + I | ~0 (resonancias) | Afinidad alta; I⁻ no despreciable upstream |
| I + e → I⁻ | EA 3.059 | |

Consecuencias de diseño (no opcionales):

- Fracción I₂⁺ en el haz ≠ 0 → I_sp efectivo y T/P cambian con ṁ y P_RF.
- I⁻ en zona fría altera balance de carga y matching.
- MRCO v2.0 (una campana Lorentz de “eficiencia”) **no** captura esto. Hay que acoplar un **0D de especies** (Lafleur 2022 / Bianchi-Garrigues) a la función de coste.

QC entra **aquí**, no en FDTD.

## 4. Ordenadores cuánticos — mapa honesto (2026)

### Hacer (ventaja potencial o al menos benchmark)

**A. VQE / SQD de espacios activos con ECP** — clase E1→E3 si converge.

I₂: 106 electrones. All-electron en NISQ = no. Protocolo:

- ECP Stuttgart/cc-pVDZ-PP (o cc-pVTZ-PP para check).
- Espacio activo mínimo disociación: (10e, 8o) σ_g, π_u, π_g, σ_u + correlato.
- Hamiltoniano fermiónico → JW/BK → ansatz UCCSD truncado o UCC-1.
- Objetivo 1: \(D_e\) vs 1.542 eV (validación de método, no descubrimiento).
- Objetivo 2 (hueco útil): curvas I₂(B), I₂⁺, resonancias de attachment, SOC (grande en I; sin SOC el PES miente).
- Métrica de parada: |E_VQE − E_CASSCF| < 1.6 mHa en puntos de la curva, no “energía total”.

Estimación de recursos (orden de magnitud, PENDIENTE de conteo exacto con PySCF+Qiskit Nature):

- (10e, 8o): ~16 spin-orbs → ~16 qubits JW. NISQ ruidoso; usable en simulador exacto y, con error mitigation, en backends ≥127q solo como demo.
- SOC + más orbs → 20–36 qubits lógicos. Eso ya es territorio SQD / early-FTQC, no un portátil.

**B. QUBO / QAOA de topología discreta de la celda RF** — clase E1.

Variable binaria \(x_{ij}\) = metal vs hueco en malla \(N\times N\) (N=8…16) de la celda mm. Coste:

\[
C(x)=w_\Gamma\hat\Gamma(x)+w_U(1-\hat U)+w_\varepsilon\hat\varepsilon_{\mathrm{diel}}+w_s\hat s_{\mathrm{sputter}}
\]

\(\hat\Gamma,\hat U\) salen de un surrogate clásico (MRCO + 1 eval CST cada k pasos), no del quantum. El QPU solo explora el binario. Hasta N≲12 el recocido clásico / CP-SAT gana. QAOA es experimento de algoritmo, no camino crítico del hardware.

### No hacer (sin ventaja 2026, o físicamente vacío)

- VQE / HHL del Maxwell 3D o PIC. Dimensión ~10⁶–10⁸. No hay QPU.
- “Simulación cuántica del plasma bajo excitación EM” como frase suelta. El campo RF es clásico; los electrones del plasma no están en un estado puro de I₂.
- Afirmar que VQE calcula la superficie de energía “bajo excitación electromagnética de 13.56 MHz”. Un fotón RF tiene \(h\nu\approx 56\,\mathrm{neV}\). No modifica el PES electrónico. La RF entra como T_e y n_e en tasas, no como término del Hamiltoniano molecular.

### Stack recomendado

```
PySCF (ECP + CASSCF clásico)  →  verdad de referencia
Qiskit Nature / PennyLane     →  VQE en simulador, luego SQD IBM
MRCO v2.1 + 0D I2 (numpy)     →  coste de diseño
COMSOL/CST + PIC rejillas     →  EM y óptica iónica
QUBO (OSQP / dwave-ocean / QAOA opcional)
```

El sandbox actual no tiene Qiskit. El módulo `mei_rit_qc.py` corre la parte clásica y deja el hook VQE.

## 5. MRCO v2.1 (física)

Eficiencia de acoplamiento (Lorentz, sin clip):

\[
\eta_{\mathrm{rf}}(f,p)=\eta_\infty\frac{(\gamma/2)^2}{(f-f_0(p,t_{\mathrm{ALD}}))^2+(\gamma/2)^2}\,e^{-\alpha\,t_{\mathrm{ALD}}}
\]

\(f_0\) baja al crecer \(t_{\mathrm{ALD}}\) (C parásita). Penalizar sputtering si el metal no está cubierto. Añadir término 0D:

\[
J = (1-\eta_{\mathrm{rf}})+w_b|1-f_{I^+}-f_{I_2^+}|+w_m(1-\eta_m)+w_T|T-T^\star|
\]

Empuje e I_sp de diseño (proyección, no medida):

\[
T=\dot m_i\,v_i,\quad v_i=\sqrt{2qV_b/\bar m},\quad I_{\mathrm{sp}}=v_i/g_0
\]

con \(\bar m = f_{I^+}m_I+f_{I_2^+}m_{I_2}\). Sin \(f_{I_2^+}\) el I_sp se infla.

Masa sistema <220 g: **objetivo no realista** a 50–80 W con PPU + tanque + neutralizador + harness. Banda honesta de sistema: 0.8–2.5 kg hasta no haber BOM. El 220 g puede quedar como techo del *head* sin PPU, etiquetado.

## 6. Plan 18 meses (igual calendario, tareas corregidas)

| Fase | Meses | Qué sí | Qué no |
|---|---|---|---|
| 1 | 1–3 | Geometría mm + 0D I₂ + CST matching + CASSCF I₂ | “simulación cuántica del propulsor” |
| 2 | 4–7 | Cupones ALD + erosión I₂; QUBO celda; VQE demo (10e,8o) en simulador | Hardware cuántico como hito de TRL |
| 3 | 8–14 | Prototipo halogen-safe, Langmuir/RPA/OES | Comparar con 1.12 mN como si fuera baseline medida |
| 4 | 15–18 | Informe TRL4, claims OEPM con periodo mm | Masa 220 g sistema sin BOM |

Presupuesto v2.0 (54–97 k€ I+D) se conserva como orden de magnitud de *estudio + cupones*, no de campaña de vacío certificada (esa sube a 150–400 k€). PENDIENTE de desglose real.

## 7. Clasificación E

| Ítem | E |
|---|---|
| I₂ como propelente GIT | E5 (vuelo + labs) |
| Umbrales I₂ tabla §3 | E6 |
| Acoplador mm tipo HIS en GIT de I₂ | E0–E1 |
| Textura μm bajo ALD | E1 |
| VQE I₂ propio | E1 |
| Empuje/I_sp MEI-RIT | E2 (objetivo) |
| 1.12 mN / 2540 s del doc original | no E3 (sin provenance) |
| Universo consciente como mecanismo | E0, fuera |

## 8. Archivos nuevos

- `llp/proyectos/MEI-RIT.json`
- `MEI-RIT_v2.1_QC.md` (este)
- `mei_rit_qc.py` — MRCO v2.1 + 0D I₂ mínimo + PES Morse + hook VQE + QUBO toy
- DOCX Drive originales: se dejan. Están truncados; no son fuente canónica.

## 9. Próximo paso

Congelar D_cámara, f_RF (elegir 13.56 **o** 2.45, no ambos en el primer proto) y p_RF ∈ [3,15] mm. Correr `python3 mei_rit_qc.py`. Solo entonces abrir backend VQE.
