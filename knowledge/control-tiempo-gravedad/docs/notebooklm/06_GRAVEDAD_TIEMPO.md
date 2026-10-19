<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/161D72aD-yA357cMkznAoMRCTogxfkAj5lmJB7jpm2Pc/edit · copia de texto, sin cambios de contenido -->

# Fuente NotebookLM — Control de tiempo y gravedad

**Autor:** Lázaro López Paz.
**Fecha del informe de viabilidad:** 31 julio 2026.
**Clasificación del propio documento:** teórico-especulativo / computación cuántica aplicada.

## Ficha de gobernanza

```
Estado: ensayo teórico + demo de evolución temporal en Qiskit (2 qubits)
Pregunta técnica: ¿qué parte de «controlar gravedad/tiempo» es física prohibida hoy y qué parte es simulación cuántica de un Hamiltoniano?
Limitaciones: el código evoluciona H = J Z0Z1 + h(X0+X1) en 2 qubits; no es un motor de métrica ni precognición empírica.
Próximo hito verificable: el mismo circuito en hardware real (EstimatorV2) con mitigator y comparación vs statevector.
```

## Tesis del informe (respetar la jerarquía)

1. Control gravitatorio arbitrario y viaje al pasado macroscópico: **prohibidos** por conservación, causalidad y ausencia práctica de energía negativa.
2. Simulación cuántica de la evolución temporal de un sistema modelo: **viable** (Trotter, redes tensoriales, VQE).
3. CTC a escala cuántica: ruta teórica autoconsistente, densidades de energía inalcanzables.

Hay un marco filosófico (universo como información / participación). Eso no cambia la jerarquía física del punto 1.

## Matemáticas usadas

Evolución de Schrödinger:

$$i\hbar \partial_t |\psi(t)\rangle = \hat H |\psi(t)\rangle, \quad |\psi(t)\rangle = e^{-i\hat H t/\hbar}|\psi(0)\rangle$$

Trotter si $\hat H = \sum_j \hat H_j$:

$$e^{-i\hat H t} \approx \left(\prod_j e^{-i\hat H_j t/n}\right)^n$$

Tabla del informe: MPS+VQE para estado inicial; Trotter + PauliEvolutionGate para evolución; EstimatorV2/SamplerV2 para observables.

## Código de referencia (informe)

Hamiltoniano de juguete: J = 1, h = 0,5, t = π, 15 pasos LieTrotter, 2 qubits en superposición, observable ZI+IZ, StatevectorEstimator.

Sirve como **plantilla pedagógica**, no como «predicción del futuro» de un sistema físico realista.

## Material pesado en Drive (usar con cuidado)

En `Control tiempo y gravedad` hay triples de:

- Digital Twin Spacetime Blueprint.pdf (~20,5 MB × 3)
- Spacetime Engineering Convergence.pdf (~14,1 MB × 3)
- MP4 41 MB y 59 MB duplicados por nombre (`&` vs `_`)

Para NotebookLM: este markdown + el PDF de 40 KB del informe.
Si se añade un blueprint, **una sola** copia.

Carpeta canónica: sin espacio al final
https://drive.google.com/drive/folders/1lfyIKVTCnzzfT5MN3rLzz5Bg6GyhSeYg

No usar `Control tiempo y gravedad ` (con espacio, 6 ago) como maestra.

Relacionados, otro cuaderno: `Motor_warp_ Jack sarfatti` y `Proyectos_futuros_con_unió_del_Dr.Jack sarfatti`.

## Cómo debe responder NotebookLM

- Empezar por lo que el autor marca como prohibido.
- Llamar «precognición» solo a muestreo de un observable tras evolución unitaria de un modelo.
- No afirmar control de gravedad de laboratorio.
