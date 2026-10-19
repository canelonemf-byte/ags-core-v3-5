<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/1VGOI1jsNGD74z5GtXcDKUCYgZjzH9s6XzEiQAsOl-Mg/edit · copia de texto, sin cambios de contenido -->

# Análisis de discrepancias — Reactor QMC-H3

**Fuentes:** Resumen maestro (123 KB), *QMC-H3_Proyecto_Maestro_Final.pdf* (4 jun 2026) y el código 0D incrustado.
**Comprobación:** reproducción numérica independiente, 30 ago 2026.
**No es un rediseño.** Es un mapa de contradicciones para que NotebookLM y la revisión humana no mezclen retórica con el modelo.

---

## 1. Hallazgo principal

El mismo paquete afirma dos cosas incompatibles:

| Voz retórica | Voz del modelo 0D (reproducida) |
|---|---|
| Estado «Perfecto / Integrado» | Q = **0,036** |
| «Puede alcanzar regímenes de alto Q» / «Q > 1–5+ con facilidad» | Para Q = 1, con *las mismas* n, T y P_rad = 2 P_tr, hace falta τ_E ≈ **69 s** (factor **×46** sobre 1,5 s), no ×3 |
| Auto-calentamiento «maximizado» 85 % | 85 % de 29 MW = **25 MW** frente a **821 MW** de pérdidas |
| Triple producto «supera ≈ 5× el requisito D-³He» | nTτ = **1,58×10²³** m⁻³ keV s ≈ **0,3×** un Lawson típico de ignición D-³He (~5×10²³) |

Los números internos del código **cuadran entre sí**. Lo que no cuadra es el relato con esos números.

---

## 2. Reproducción del 0D (cierra con el PDF)

Parámetros: R = 2 m, a = 1 m, κ = 2, V = 2π² R a² κ ≈ **79 m³**, n = 5×10²⁰ m⁻³ (50/50), T_i/T_e = 70/60 keV, ⟨σv⟩ = 2×10⁻²⁴ m³/s, E = 18,3 MeV, τ_E = 1,5 × 3 = 4,5 s, P_rad := 2 P_transporte, f_self = 0,85.

| Magnitud | PDF | Recalculado |
|---|---:|---:|
| V | 79 m³ | 78,96 m³ |
| P_fusión | ≈ 29 MW | 28,9 MW |
| W_plasma | (no destacado) | 1,23 GJ |
| P_transporte | — | 274 MW |
| P_radiación | — | 547 MW |
| P_loss | ≈ 821 MW | 821 MW |
| P_auto | ≈ 25 MW | 24,6 MW |
| P_aux | — | 797 MW |
| Q | ≈ 0,04 | **0,036** |
| nTτ | 1,58×10²³ | 1,575×10²³ |

Radio de Larmor del protón 14,7 MeV: 55 mm solo si B ≈ **10 T** (a 8 T son 69 mm; a 12 T, 46 mm). El texto dice «8–12 T → 55 mm» como si fuera un solo valor.

---

## 3. Discrepancias internas (el propio expediente)

### 3.1 «×3 en τ_E multiplica Q ×3» frente a «Q > 1 con facilidad»

En *este* modelo P_aux ≈ P_loss ≫ P_fusión, así que Q escala casi lineal con τ_E. Eso es cierto y trivial:

- ×1 → Q ≈ 0,012
- ×3 → Q ≈ 0,036
- ×5 → Q ≈ 0,062
- ×10 → Q ≈ 0,13
- ×20 → Q ≈ 0,29
- ×45 → Q ≈ 0,96

El gráfico del PDF pone el eje Y hasta 15 y líneas Q = 1 y Q = 5, lo que sugiere que ×3 se acerca al break-even. **No es así.** ×3 deja Q en el 4 % del break-even.

Para Q = 1 sin tocar n ni T hay que pasar de 4,5 s a ~69 s.
Para Q = 1 con τ_E = 4,5 s hay que subir n por un factor ~**15** (n ≈ 7,7×10²¹ m⁻³), fuera del «valor moderado para estabilidad» que justifica 5×10²⁰.

### 3.2 0D frente a 1D

El maestro añade un 1D y dice P_fusión integrada ≈ **7 MW**. El 0D da **29 MW**. Factor ~4. El 1D no «confirma» el 0D; lo contradice. χ_eff = 2,0 → 0,67 m²/s es otro ×3 impuesto, no derivado de MHD.

### 3.3 Máquina no única

Se presenta como tokamak esférico compacto **o** stellarator. A = R/a = 2 es un ST razonable; un stellarator no comparte el mismo solenoide central ni el mismo β. Son dos conceptos.

### 3.4 Estado del proyecto

«No se requiere trabajo adicional para considerarlo completo» y, a la vez, «listo para Fase 1 de simulación detallada». Completo como *dossier conceptual* ≠ cerrado como *ingeniería*.

### 3.5 Aneutrónico

La reacción D-³He es de productos cargados; el mix 50/50 produce D-D (y T-D) y un canal neutrónico que el 0D no modela. «Aneutrónico» en el título es una aproximación, no un resultado del código.

---

## 4. Discrepancias de modelado (el 0D no es física de D-³He)

### 4.1 P_rad = 2 × P_transporte

Es un multiplicador libre. Si mejoras τ_E, la radiación **cae** en el script. En un plasma D-³He a 60–70 keV la radiación de sincrotrón y bremsstrahlung depende de n, T, B, β y reflectividad de pared, no de τ_E. El supuesto oculta el obstáculo que el texto dice resolver con metamateriales fotónicos: esos metamateriales **no aparecen en las ecuaciones**.

### 4.2 ⟨σv⟩ fijo

2×10⁻²⁴ m³/s a 70 keV es un orden de magnitud plausible, pero no es Bosch–Hale ni depende de T. El 1D usa T(r) y, si no recalcula ⟨σv⟩(T), el perfil de fuente es inconsistente.

### 4.3 Definición de Q

Q = P_fusión / P_aux con P_aux = P_loss − 0,85 P_fusión. Es un Q de plasma 0D. No incluye recirculación de planta, criogenia HTS, ni eficiencia de conversión directa (inducción + MHD + rectenas, solo nombradas).

### 4.4 Triple producto

1,58×10²³ es ~50× un Lawson D-T de ignición (~3×10²¹) y **por debajo** de un Lawson D-³He típico (~3–10×10²³). La frase «5× el requisito D-³He» no tiene referencia ni cálculo en el PDF.

### 4.5 Metamaterial magnético vs equilibrio MHD

SRR Nb/YBCO/grafeno con μ_eff \< 0 / ENZ son estructuras de **RF / microondas**. El confinamiento 8–12 T es un equilibrio magnetohidrodinámico de campo casi-continuo. No hay puente cuantitativo entre un SRR y χ_i o el ripple. El ×3 de τ_E es un axioma, no un output.

### 4.6 Control VQA en tiempo real

Los modos MHD viven en milisegundos. VQE/VQA en hardware actual no cierra ese lazo. PINN + RL como *propuesta* de control es otra capa; no valida el ×3.

### 4.7 Primera pared y partículas rápidas

r_L (p, 14,7 MeV) ~ 5 cm en 10 T. El texto admite que hace falta control sub-mm de topología. No hay cálculo de carga de pared, ripple, pérdidas banana ni de W-Cr-Y bajo flujo de protones de 14,7 MeV.

---

## 5. Discrepancias con el resto del portfolio

| Otro documento | Tensión con QMC-H3 |
|---|---|
| Recolección ³He | Precio ~20 M USD/kg y ruta lunar TRL 5–6 de *terceros* (Interlune). Consumo 0D del QMC-H3 ≈ **1,6 kg ³He/año** a 29 MW continuos. El reactor no hace el balance de masa ni el coste de combustible. |
| IQM-He3-Anti | Misma marca ³He, otra máquina: superfluido a 130 µK, YIG, antimateria CERN. No es el tokamak de 70 keV. |
| LD-Chip | Usa ³He como baño a 0,3 K, no como combustible. Competencia de isótopo, no sinergia de reactor. |
| Informe gravedad-tiempo | Prohíbe control gravitatorio macro. IQM habla de curvatura local. QMC-H3 no debe heredar esa capa. |
| MEI-RIT | Presupuesto 53–95 k€ y 18 meses. QMC-H3 no tiene presupuesto ni TRL de dispositivo. No son el mismo «nivel de realizabilidad». |

Correo `qmc-h3@fusion-innovacion.org`: contacto conceptual; no acredita un consorcio.

---

## 6. Qué sí se sostiene

- Geometría ST compacta (A = 2, κ = 2) es un punto de partida reconocible.
- El problema D-³He (T alta, sincrotrón, partículas rápidas, reactividad menor que D-T) está bien *nombrado*.
- El código 0D es corto, ejecutable y transparente: se puede atacar.
- Larmor a 10 T está bien calculado.
- El propio Q ≈ 0,04 está escrito en el resumen; no hay que «descubrirlo». Hay que dejar de contradecirlo en el mismo párrafo.

---

## 7. Cómo reescribir el estado (propuesta)

```
Estado: concepto + modelo 0D paramétrico (Q ≈ 0,04 bajo los supuestos publicados)
Pregunta técnica: ¿qué combinación verificable de n, T, τ_E y P_rad (no un ×3 axiomático) lleva a Q_plasma ≥ 1 en D-³He?
Evidencia: script 0D + esbozo 1D inconsistente (29 MW vs 7 MW)
No evidencia: τ_E ×3 por SRR, VQA en tiempo real, Q > 1, aneutronicidad estricta, suministro lunar propio
Próximo hito: (1) sustituir P_rad = 2 P_tr por Brems + sincrotrón con reflectividad de pared;
(2) ⟨σv⟩(T) Bosch–Hale + canal D-D; (3) un solo 0D/1D con la misma P_fusión;
(4) dejar de usar «Perfecto / Integrado» en portada.
```

---

## 8. Preguntas para el cuaderno NotebookLM 01

1. «Usando solo el código 0D, ¿qué factor de τ_E hace Q = 1 sin cambiar n ni T?»
2. «¿Por qué P_fusión 0D y 1D no coinciden?»
3. «¿Qué términos harían falta para que los metamateriales fotónicos entren en P_rad?»
4. «No uses la palabra perfecto. Resume limitaciones del modelo.»
