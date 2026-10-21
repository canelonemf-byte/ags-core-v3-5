# Cartera de innovación OMNISCIENCE — escaneo del 18-oct-2026 (UTC+2)

**Alcance**: 16 candidatas ancladas en capacidades reales (motor fonónico, pipeline MACE-MP-0 + Phonopy de C-MAT-001, kit C-VIB-001), con re-chequeo de las 3 ideas adyacentes que contradecían la física (ADJ-01, ADJ-02, ADJ-03).
**Puntuación**: novedad × impacto × viabilidad, cada factor de 1 a 3 (máximo 27). La originalidad sale de búsquedas web acotadas (2023–2026), no de una revisión sistemática. **Ninguna idea resultó «nueva»**: las mejores son «parciales», es decir, combinaciones o aplicaciones nuevas de métodos conocidos.

## Ranking
| # | id | idea (resumen) | originalidad | E | punt. |
|---|---|---|---|---|---|
| 1 | INN-01 | σᴬ con uMLIP como compuerta de validez armónica y prefiltro low-κL | parcial | E2 (expl.) | 18 |
| 2 | INN-03 | profundidad del doble pozo (uMLIP) frente a Tc en perovskitas | parcial | E2 (expl.) | 12 |
| 3 | INN-05 | solapamiento de DOS fonónica como prefiltro de TBC | parcial | E2 (expl.) | 12 |
| 4 | INN-11 | límite de Akhiezer (Grüneisen uMLIP) para materiales HBAR cuánticos | parcial | E1 | 12 |
| 5 | INN-02 | factor de escala anti-ablandamiento con validación cruzada | conocido | E2 (expl.) | 9 |
| 6 | INN-16 | prefiltro de estabilidad dinámica con uMLIP | conocido | E2 | 9 |
| 7 | INN-10 | modos THz de α-glicina con uMLIP (núcleo correcto de GlyD-QSense) | parcial | E1 | 8 |
| 8–12 | INN-04/06/07/08/09 | κL phono3py, diseño inverso de cristales fonónicos, IR/Raman (MACE-Field), adsorbatos, estados de transición | conocido | E0 | 6 |
| 13 | INN-12 | cribado SAW | parcial | E0 | 4 |
| 14–16 | INN-15/13/14 | variantes correctas de ADJ-01/02/03 | conocido | E0 | 3–4 |

El detalle completo (fuentes, plausibilidad, viabilidad, próximo paso) está en `cartera_innovacion.json`.

## Exploratorios ejecutados (marcados EXPLORATORIOS, no confirmatorios; MACE-MP-0 medium, CPU)
- **X1, σᴬ a 300 K** (24 instantáneas, semilla 20261018):

  | Material | σᴬ |
  |---|---|
  | Si | 0.264 |
  | C | 0.203 |
  | GaAs | 0.198 |
  | MgO | 0.259 |
  | NaCl | 0.388 |
  | PbTe | 0.461 |

  - El orden general (PbTe > NaCl > el resto) es razonable.
  - Para Si, el DFT-aiMD publicado da 0.15 (Knoop 2020): MACE sobreestima, posiblemente por el rango 2×2×2 de las constantes de fuerza o por error del propio modelo.
  - ρ(σᴬ, |error TO|) = 0.70 con n = 5 y p = 0.19: no significativo.
- **X2, doble pozo ferroeléctrico** (ΔE con relajación libre, meV/f.u.):

  | Material | ΔE | Fase final |
  |---|---|---|
  | PbTiO3 | −190 | P4mm |
  | KNbO3 | −51 | — |
  | BaTiO3 | −46 | — |
  | KTaO3 | −1.4 | — |
  | SrTiO3 | −1.2 | — |

  - Spearman frente a Tc (763 / 708 / 393 / 0 / 0 K): ρ = 0.97 con n = 5. Es una muestra mínima.
  - Los no ferroeléctricos dan pozos de ~1 meV, compatibles con el comportamiento paraeléctrico cuántico, pero esto no está demostrado aquí.
  - PbTiO3 sale sobre-tetragonal, un sesgo típico de PBE.
- **X3, solapamiento de DOS**: máximo Si|MgO 0.51; mínimo C|PbTe 0.001. No se ha comparado con ninguna medida.
- **X5, escalado global LOO**: el error residual va de −14 % a +12 % (2/4 dentro del ±10 %). Confirma que un escalado global no basta, como advierte la literatura.
- **X4, re-chequeo de ADJ-02**: flagelo con EI = 3.5 pN·µm² (Darnton & Berg 2007), L = 10 µm, en agua.
  - Resultado: f₀ ≈ 0.12 MHz (flexión), **Q ≈ 3×10⁻⁴**, Re ≈ 8×10⁻⁵.
  - Está sobreamortiguado, así que la «resonancia de flagelos» queda refutada.

## Re-chequeo de las 3 contradicciones
- **ADJ-01 (GlyD-QSense)**: la variante correcta es la termometría Raman anti-Stokes/Stokes con incertidumbre calibrada (±0.4–0.5 °C según la fuente citada). Hay que re-etiquetar la parte simulada y dejar de llamarla «cuántica» (INN-15). La parte computable, modos THz de α-glicina, es INN-10.
- **ADJ-02 (antibiótico de fonones)**: el mecanismo es inviable (X4). La variante física real es la sonobactericida con microburbujas (INN-13): conocida y experimental, sujeta a gobernanza biológica.
- **ADJ-03 (meta-enfriador de qubits)**: operar a 1–2 K sigue siendo imposible con Al. La variante real son las trampas de down-conversion de fonones contra el envenenamiento por cuasipartículas (INN-14), ya demostradas.

## Advertencias honestas
- Muestras de 4 a 6 materiales: ningún exploratorio tiene potencia estadística.
- MACE-MP-0 ablanda las frecuencias (C-MAT-001: TO −12…−28 %).
- E2 significa «hay una predicción de un modelo», no que esté verificada.
- Los tres pre-registros se redactaron después de ver los exploratorios; por eso exigen conjuntos de materiales nuevos.
- No se hizo búsqueda de patentes específica ni análisis de libertad de operación.

## originalidad_y_derechos
Todo el texto, el código (`code/*.py`) y las figuras (`fig_exploratorios.png`) son de elaboración propia. No se ha copiado texto, figuras ni código de artículos ni patentes. Las ideas y los datos externos se citan con su DOI o URL y solo se usan como datos de referencia (Tc, σᴬ de Si, EI del flagelo, frecuencias).
