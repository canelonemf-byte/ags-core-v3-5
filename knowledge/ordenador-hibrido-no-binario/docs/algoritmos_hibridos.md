# Algoritmos híbridos clásico-cuánticos y no binarios — ORDENADOR HÍBRIDO

Autor: Lázaro López Paz, El Prat de Llobregat, Barcelona, España + asistencia IA · Licencia CC BY 4.0 · 2026-10-21
Alcance: revisión del estado del arte y propuesta de diseño. Ningún resultado de este documento es experimental. Niveles E según `registro_evidencia.json` (ev_17–ev_26).

## 1. Variacionales híbridos (VQE, QAOA) — estado del arte
- **Bucle**: la QPU prepara un estado parametrizado |ψ(θ)⟩ y mide ⟨H⟩. Un optimizador clásico (CMOS) actualiza θ, y el ciclo se repite hasta converger. El coste está dominado por el número de disparos (shots) y por las iteraciones.
- **VQE**: busca el estado fundamental de un hamiltoniano [R1]. **QAOA**: alterna p capas de un hamiltoniano de coste y otro mezclador para resolver optimización combinatoria [R2].
- **Limitaciones conocidas**: los *barren plateaus* (gradientes que se desvanecen al crecer el sistema) [R4], el ruido NISQ y el elevado coste en mediciones [R3].
- **En el proyecto**: la QPU es un acelerador *opcional*, no forma parte del núcleo. El código VQE del Manual es ilustrativo (E2, ev_08) y no tiene salidas archivadas.

## 2. Qudits y lógica multivaluada (ternaria/MVL) — estado del arte
- **Qudits** (d>2 niveles): más información por portador y algunas descomposiciones de puertas más cortas, a cambio de un control y una calibración más complejos [R5].
- **MVL clásica** (ternaria, base-k): menos interconexión por dígito. Los márgenes de ruido se estrechan con k (ev_02) [R6].
- **Restricción física**: Landauer no se reduce por bit equivalente (ev_01). Cualquier ganancia tiene que venir de la interconexión y del movimiento de datos, no de la termodinámica.

## 3. Cómputo en memoria analógico (CIM) — estado del arte
- **MVM en crossbar**: la ley de Ohm multiplica y la de Kirchhoff suma por columna. DAC en filas y ADC en columnas [R7][R8].
- **No idealidades**: ruido de programación y lectura, deriva, no linealidad, IR-drop y conductancia finita.
- **Entrenamiento tolerante a ruido**: inyectar ruido durante el entrenamiento, calibrar y recalibrar, y usar esquemas de pesos diferenciales o multicelda. Se ha demostrado inferencia precisa en PCM con estas técnicas [R9].
- **Relación con `sim/sim_mvm.py` (E2, ev_16)**: el modelo solo incluye cuantización a 2–16 niveles, ruido de programación (2 %) y de lectura (1 %) y ADC de 4–8 bits, todo con **parámetros supuestos**. Todavía no incluye deriva, IR-drop ni entrenamiento tolerante a ruido. Resultado: ninguna configuración llega a ≤1 % (la mejor da un 10,5 %) y ADC+DAC suponen el 46–62 % de la energía CIM modelada.

## 4. Planificación heterogénea CMOS/CIM/fotónica/QPU
- **Estado del arte**: list scheduling sobre un DAG de tareas con costes distintos por procesador; HEFT es la referencia clásica [R10].
- **Propuesta propia (E0, no implementada)**: un planificador tipo HEFT cuya función de coste por tarea y destino incluye energía, latencia y **error esperado**. Si una tarea pide más precisión de la que puede dar el CIM, se descarta o se envía a CMOS. Además se contabilizan las conversiones ADC/DAC y E/O, y la QPU solo se considera para subproblemas variacionales cuando el coste en disparos está justificado.
- **Usar sim_mvm como modelo de coste**: las tablas error/energía de `sim/salidas/resultados.csv` podrían alimentar la decisión CMOS↔CIM. Solo serán significativas cuando se sustituyan los supuestos por parámetros con fuente (tarea t6).

## 5. Qué es propio del proyecto y qué no
| tema | originalidad | E |
|---|---|---|
| VQE/QAOA, qudits, MVL, CIM, HEFT | estado_del_arte | E4 (literatura con referencia) |
| Integrar CIM, entrenamiento con ruido y QPU opcional en esta arquitectura | adaptacion | E0 |
| Planificador consciente de error y conversión | propuesta_propia | E0 |
| Modelo de coste sim_mvm para planificación | propuesta_propia | E0 (los datos de la simulación son E2) |

## Referencias (comprobadas con Crossref/doi.org o la API de arXiv el 2026-10-21; solo existencia y metadatos, sin revisión técnica del contenido)
- [R1] Peruzzo et al., *A variational eigenvalue solver on a photonic quantum processor*, Nat. Commun. (2014). doi:10.1038/ncomms5213
- [R2] Farhi, Goldstone, Gutmann, *A Quantum Approximate Optimization Algorithm*, arXiv:1411.4028 (2014)
- [R3] Cerezo et al., *Variational quantum algorithms*, Nat. Rev. Phys. (2021). doi:10.1038/s42254-021-00348-9
- [R4] McClean et al., *Barren plateaus in quantum neural network training landscapes*, Nat. Commun. (2018). doi:10.1038/s41467-018-07090-4
- [R5] Wang et al., *Qudits and High-Dimensional Quantum Computing*, Front. Phys. (2020). doi:10.3389/fphy.2020.589504
- [R6] Hurst, *Multiple-Valued Logic—its Status and its Future*, IEEE Trans. Comput. C-33, 1160–1179 (1984). doi:10.1109/tc.1984.1676392
- [R7] Ielmini & Wong, *In-memory computing with resistive switching devices*, Nat. Electron. (2018). doi:10.1038/s41928-018-0092-2
- [R8] Sebastian et al., *Memory devices and applications for in-memory computing*, Nat. Nanotechnol. (2020). doi:10.1038/s41565-020-0655-z
- [R9] Joshi et al., *Accurate deep neural network inference using computational phase-change memory*, Nat. Commun. (2020). doi:10.1038/s41467-020-16108-9
- [R10] Topcuoglu, Hariri, Wu, *Performance-effective and low-complexity task scheduling for heterogeneous computing*, IEEE TPDS (2002). doi:10.1109/71.993206

Las afirmaciones cualitativas atribuidas a [R1]–[R10] proceden del conocimiento general del campo y no se han contrastado con el texto completo: quedan **PENDIENTE DE VERIFICACIÓN** en cuanto a su contenido.
