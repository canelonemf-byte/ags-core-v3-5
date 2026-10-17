# MEI-RIT proto1 — monografía de principio a fin
Metasurface-Enhanced Iodine RF Ion Thruster  
Autor de pack: Lázaro López Paz · cierre de ingeniería 2026-09-22  
Clase dominante: **E2** (diseño calculable). Química I₂ de literatura: **E6**. Hardware propio: **E0–E1**.

Canon máquina: `llp/proyectos/MEI-RIT.json`  
Ejecutables: `mei_rit_design.py` · `mei_rit_realizable.py` · `mei_rit_banco.py`

Este texto no inventa ensayos. Donde hay número de banco propio se etiqueta E2.

---

## 0. Problema

CubeSats 6U+ necesitan Δv de cientos de m/s a decenas de W. El xenón exige tanque de alta presión y coste alto. El yodo sólido se guarda a presión de vapor (kPa), densidad ~4.9 g/cm³, y ya voló en NPT30-I2 (ThrustMe) y se demostró en BIT-3 (Busek). El hueco que MEI-RIT declara: mejorar el acoplo RF y la uniformidad del plasma en una cámara de ~3 cm.

El pack v2.0 mezclaba tres errores que este cierre corrige:

1. Periodo 8–18 μm tratado como metasuperficie de RF (λ a 13.56 MHz es 22.1 m).
2. 13.56 MHz y 2.45 GHz como si fueran la misma máquina.
3. 1.12 mN / 2540 s / η 36–46 % presentados como resultado.

---

## 1. Qué es el sistema (congelado)

GIT de RF, propelente I₂ sólido, descarga ICP a **13.56 MHz**, no dual-band.

Cadena: tanque 90 °C → capilar PTFE 192 μm × 60 mm → cámara Al₂O₃ Ø32×36 mm + bobina 5 vueltas + anillo lumped 8 mm bajo ALD → rejillas grafito Ø28 mm @ 1200 / −200 V → haz I⁺/I₂⁺ + filamento W.

Punto lab: \(P_{\mathrm{RF}}=22\,\mathrm{W}\), \(I_b=16\,\mathrm{mA}\), \(T\approx0.95\,\mathrm{mN}\), \(I_{\mathrm{sp,sys}}\approx2800\,\mathrm{s}\) si \(\eta_m=0.68\).

2.45 GHz queda como rama B (ECR, \(B=87.5\,\mathrm{mT}\)), otra máquina.

---

## 2. Tecnologías

| Capa | Tecnología | Estado |
|---|---|---|
| Descarga | ICP 13.56 MHz ISM | heritage RIT / NPT30 / BIT-3 |
| Propelente | I₂ sólido + sublimación térmica | E5 de terceros |
| Feed | tanque T + capilar viscoso PTFE | E2 dimensionado |
| Matching | red L Cs–Cp | E2 calculada |
| “Metasuperficie” proto1 | anillo 8 mm lumped + ALD | E1, no FSS |
| Textura μm | opcional, escala Debye | E1, no RF |
| Óptica | 2 rejillas grafito | E2 layout |
| Neutralización proto1 | filamento W | E4 genérico, E1 en I₂ propio |
| Neutralización proto2 | RF-cathode | no en proto1 |
| Diagnóstico | coupler, Langmuir, RPA, OES | plan |
| QC | VQE I₂ ECP (10e,8o) | E1, fuera del banco |
| QC | QUBO topología anillo | E1 toy |
| Banco | Ar gate luego I₂ + cold trap | procedimiento |

---

## 3. Metamateriales — escala correcta

Una metasuperficie EM periódica exige \(p/\lambda\) no nulo. Aquí:

\[
\lambda_{13.56}=22.1\,\mathrm{m},\qquad
\frac{p}{\lambda}\Big|_{p=8\,\mathrm{mm}}=3.6\times10^{-4}.
\]

Eso no es FSS/HIS: el anillo es un **circuito concentrado** que perturba \(L\) mutua y \(E_\theta\).  
A 2.45 GHz, \(p/\lambda=0.025\)–\(0.12\) sí sería metasuperficie. Proto1 no va ahí.

La cota 8–18 μm coincide con \(\lambda_D\sim50\,\mu\mathrm{m}\) (\(T_e=4\,\mathrm{eV}\), \(n_e=10^{17}\,\mathrm{m}^{-3}\)), no con \(\lambda_{\mathrm{RF}}\). Se reserva como textura de vaina bajo ALD, hipótesis E1.

ALD (Si₃N₄ o Al₂O₃, 150 nm) no es “meta”: es pasivado contra sputtering de I⁺.

---

## 4. Fórmulas

### 4.1 Ondas y plasma
\[
\lambda_0=\frac{c}{f},\qquad
f_{pe}=\frac{1}{2\pi}\sqrt{\frac{n_e e^2}{\varepsilon_0 m_e}},\qquad
\delta_{\mathrm{in}}=\frac{c}{\omega_{pe}}.
\]
Corte a 2.45 GHz: \(n_{\mathrm{cut}}=7.45\times10^{16}\,\mathrm{m}^{-3}\).  
ECR: \(B=2\pi f m_e/e\) → 0.48 mT @ 13.56 MHz (inútil) · 87.5 mT @ 2.45 GHz.

Piel de Cu: \(\delta_{\mathrm{Cu}}=\sqrt{2/(\mu_0\sigma\omega)}\approx18\,\mu\mathrm{m}\) @ 13.56 MHz.

Diseño ICP: \(0.45\le\delta_{\mathrm{in}}/R\le1.35\). Proto1: \(R=16\,\mathrm{mm}\), \(n_e=1.2\times10^{17}\), \(\delta/R=0.96\).

### 4.2 Bobina y matching
\[
L\approx\mu_0 N^2\pi r_c^2/(l_c+0.9 r_c)\approx848\,\mathrm{nH}.
\]
\[
\omega L\approx72\,\Omega,\qquad
C_s=\frac{1}{\omega(\omega L-X_s)},\qquad
Q=\sqrt{Z_0/R_s-1},\qquad
C_p=\frac{Q}{\omega Z_0}.
\]
Con \(R_s\sim4\,\Omega\), \(Z_0=50\,\Omega\): \(C_s\approx200\,\mathrm{pF}\), \(C_p\approx796\,\mathrm{pF}\).
\[
\Gamma=\frac{Z-Z_0}{Z+Z_0},\qquad
|\Gamma|_{\mathrm{pass}}^{\mathrm{Ar}}<0.15\quad(18{-}25\,\mathrm{W}).
\]

### 4.3 Lorentz de acoplo (MRCO, sin clip)
\[
\eta_{\mathrm{rf}}(f)=\eta_\infty\frac{(\gamma/2)^2}{(f-f_0)^2+(\gamma/2)^2}\,e^{-\alpha t_{\mathrm{ALD}}}.
\]
\(f_0\) baja con \(C\) parásita del ALD. No usar `np.clip` sobre η.

### 4.4 Química I₂ (E6 umbrales)
\[
\begin{align*}
\mathrm{I_2}+e&\to 2\mathrm{I}+e && 1.542\,\mathrm{eV}\\
\mathrm{I_2}+e&\to\mathrm{I_2^+}+2e && 9.31\,\mathrm{eV}\\
\mathrm{I_2}+e&\to\mathrm{I^+}+\mathrm{I}+2e && 11.63\,\mathrm{eV}\\
\mathrm{I}+e&\to\mathrm{I^+}+2e && 10.45\,\mathrm{eV}\\
\mathrm{I_2^+}+e&\to\mathrm{I^+}+\mathrm{I}+e && 2.18\,\mathrm{eV}\\
\mathrm{EA}(\mathrm{I})&=3.059\,\mathrm{eV}.
\end{align*}
\]
Un fotón RF: \(h\nu=hf\) (logaritmo no aplica; es lineal).  
\(h\nu(13.56\,\mathrm{MHz})\approx56\,\mathrm{neV}\). No entra en el PES. VQE no sustituye tasas.

PES Morse de referencia:
\[
V(r)=D_e\bigl(1-e^{-a(r-r_e)}\bigr)^2,\quad D_e=1.542\,\mathrm{eV},\; r_e=2.666\,\text{Å}.
\]

### 4.5 Haz y eficiencias
Masa media del ion: \(\bar m=f_{I^+}m_I+f_{I_2^+}m_{I_2}\).
\[
v_i=\sqrt{2qV_b/\bar m},\qquad
I_{\mathrm{sp,ion}}=v_i/g_0,\qquad
I_{\mathrm{sp,sys}}=\eta_m I_{\mathrm{sp,ion}}.
\]
\[
T=\dot m_{\mathrm{ion}}v_i,\qquad
P_{\mathrm{jet}}=I_b V_b=\tfrac12 T v_i,
\]
\[
\eta_e=\frac{P_{\mathrm{jet}}}{P_{\mathrm{sys}}},\qquad
\eta_T=\frac{T^2}{2\dot m_{\mathrm{tot}}P_{\mathrm{sys}}}=\eta_m\eta_e\eta_{\mathrm{div}}.
\]
\[
\varepsilon_b=\frac{P_{\mathrm{fwd}}(1-|\Gamma|^2)}{I_b}\quad[\mathrm{eV/ion}=\mathrm{W/A}].
\]
Objetivo lab: \(\varepsilon_b=400{-}700\,\mathrm{eV/ion}\), no 2200.

Child–Langmuir (I⁺):
\[
j_{\mathrm{CL}}=\frac{4}{9}\varepsilon_0\sqrt{2q/m_I}\,\frac{V_b^{3/2}}{d^2}.
\]
Perveance relativa proto1 ≈ 0.10 (subperveance).

T/P de beam (techo): \(T/P_{\mathrm{beam}}=2/v_i\approx49.6\,\mathrm{mN/kW}\) @ 40.4 km/s.  
T/P de sistema card 40 W: 12 mN/kW. Lean 22 W, mismo \(I_b\): ~15.5 mN/kW.

### 4.6 Sublimación (logaritmo de Antoine)
\[
\log_{10}\!\left(\frac{P_{\mathrm{vap}}}{10^5\,\mathrm{Pa}}\right)=A-\frac{B}{T+C},
\]
\(A=3.36\), \(B=1039\), \(C=-146.59\), \(T\) en K.  
90 °C → 3.65 kPa (banda NPT30 2–6 kPa).

Capilar viscoso (Hagen, orden de diseño):
\[
\dot m\sim\frac{\pi r^4\rho\,\Delta P}{8\mu L}.
\]
Cierre: \(d=192\,\mu\mathrm{m}\), \(L=60\,\mathrm{mm}\) @ 90 °C para \(35\,\mu\mathrm{g/s}\).  
Joya sónica equivalente 55 μm: **prohibida** (obturación).

Clausius–Clapeyron (equivalente físico del log):
\[
\ln P=-\frac{\Delta h_s}{R}\frac{1}{T}+\mathrm{const}.
\]

### 4.7 QUBO del anillo (algoritmo, no QPU obligatorio)
\[
C(x)=w_\Gamma\hat\Gamma(x)+w_U(1-\hat U)+w_\varepsilon\hat\varepsilon+w_s\hat s.
\]
\(x_{ij}\in\{0,1\}\) metal/hueco. Hasta \(N\sim12\), annealer clásico. QAOA es experimento.

### 4.8 VQE (fuera del banco)
Hamiltoniano electrónico en espacio activo (10e,8o)+ECP, mapa JW (~16 qubits).  
Parada: \(|E_{\mathrm{VQE}}-E_{\mathrm{CASSCF}}|<1.6\,\mathrm{mHa}\) en la curva.  
SOC obligatorio en I. Sin SOC el PES miente. No Maxwell.

---

## 5. Algoritmos y software

| Nombre | Qué hace | Qué no |
|---|---|---|
| MRCO v2.1 | η Lorentz + penaliza escala RF y ALD | no 0D completo Lafleur |
| `mei_rit_design.py` | geo, L/C, T, Isp, checks 11/11 | no CST |
| `mei_rit_realizable.py` | Antoine, capilar, grid, BOM, 6/6 | no ensayo |
| `mei_rit_banco.py` | red L, RFQ, plantilla Γ(P) | Γ plantilla ≠ medida |
| `vqe_i2.py` | pipeline PySCF si hay backend | no empuje |
| 0D I₂ (pendiente T2) | fracciones I⁺/I₂⁺/I⁻ vs \(T_e\) | aún heurístico en card |
| PID tanque | \(T\to P_{\mathrm{vap}}\to\dot m\) | no caudalímetro de I₂ |

Flujo de diseño:
Problema → hipótesis (anillo lumped) → predicción (card E2) → banco Ar → I₂ → falsación por Γ, \(I_b\), RPA.

---

## 6. Materiales

**Permitidos en vapor I₂:** Al₂O₃, BN, grafito/C pirolítico, PTFE, FFKM, W (filamento fuera de la línea), Ni/Hastelloy si hace falta metal.

**Prohibidos proto1:** Al, Cu desnudo, latón, acero al carbono, Mo como grid sin ensayo propio.

**Cu de bobina/anillo:** solo bajo PTFE continuo o ALD 150 nm intacto.

Lista RFQ (tolerancias de corte):

- Tubo Al₂O₃ 99.7 %: ID 32.00±0.20 · OD 35.00±0.20 · L 36.00±0.50 mm  
- Capilar PTFE: ID 0.20±0.02 mm · stock 1 m  
- Grids: Ø28.00±0.10 · 316 agujeros hex pitch 1.50±0.05  
- Caps: 180 pF 5 kV + trim 10–60; 800 pF + trim 50–500  

---

## 7. Presupuesto

| Partida | EUR |
|---|---|
| Hardware BOM proto lab (19 ítems) | 4.4–15 k |
| Grids custom + ALD cupones | 1.5–5 k (dentro o extra) |
| Campaña halogen-safe (trap, liner, tiempo vasija) | 8–20 k |
| Estudio + margen pack v2.0 | 54–97 k (no es PPU espacial) |
| PPU de vuelo + RF-cathode + qual | 150–400 k+ (fuera de proto1) |

Masa: head + tanque lab 0.8–2.5 kg sistema. **No 220 g.**

---

## 8. Esquemas

Cadena y red L: `MEI-RIT_esquema_cadena.png`, `MEI-RIT_esquema_matching.png`.  
Feed Antoine: `MEI-RIT_proto1_feed.png`.  
Mapa T(P): `MEI-RIT_proto1_map.png`.  
Plantilla Γ: `MEI-RIT_proto1_gamma_plantilla.png` (sustituir por medida).

---

## 9. Plan 18 meses (realista)

| Fase | Qué | Gate |
|---|---|---|
| Pedido | RFQ-C1/C2/C3 | piezas en mano |
| Ar | matching + Γ(P) | \|Γ\|<0.15 @ 18–25 W |
| I₂ | trap + 90 °C + Ib=16 mA | RPA + OES |
| Óptica | perveance, divergencia | η_div |
| Cierre TRL4 lab | informe E4 propio | no folleto 36–46 % |

T9 (I₂) bloqueado por T8 (Ar).

---

## 10. Lo que el proyecto no es

No es un ordenador cuántico que diseña el motor.  
No es una metasuperficie óptica dentro de un RIT.  
No es un ECR de 2.45 GHz.  
No es un sistema de 220 g y 46 % medidos.  
No hay simulación CST/PIC propia archivada con mallado.

Hay un proto1 **dimensionado, comprable y con gate de banco**. Eso es el final de esta fase de papel.
