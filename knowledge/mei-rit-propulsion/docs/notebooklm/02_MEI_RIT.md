<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/1MCdpL75O6BYovdejDaU9RPcO8Zgv3e5KfBF6X0YlV7Y/edit · copia de texto, sin cambios de contenido -->

# Fuente NotebookLM — MEI-RIT (Lázaro Drive)

**Inventor:** Lázaro López Paz, El Prat de Llobregat, Barcelona.
**Colaboración documental:** Grok (xAI), julio 2026.
**Estado de evidencia:** diseño conceptual + optimización surrogate (MRCO v1.1). Anclado en thrusters de yodo ya volados (literatura), no en un prototipo propio medido.
**Versión base:** MEI-RIT v1.1 (16 julio 2026).

## Ficha de gobernanza

```
Estado: concepto realizable / surrogate numérico
Pregunta técnica: ¿una metasuperficie sub-λ en la cámara de un RIT de yodo mejora el acoplamiento RF y la uniformidad de plasma lo bastante para +10–15 % vs baseline?
Alcance: prototipo de laboratorio 50–80 W, CubeSat 6U–12U.
Limitaciones: MRCO v1.1 no es full-wave; exige COMSOL/CST y luego vacío + balanza de thrust.
Evidencia externa citada: ThrustMe NPT30-I2 (órbita desde 2021), Busek BIT-3.
Próximo hito verificable: geometría final + simulación full-wave de acoplamiento y mapa de campo en la cámara.
```

## Propuesta

Propulsor iónico RF de yodo sólido (I₂) con metasuperficie integrada en la cámara de descarga para mejorar matching de impedancia y uniformidad. Parte de arquitecturas ya demostradas y añade una metasuperficie que, según el documento de julio 2026, no está en thrusters operativos de yodo.

## Objetivos de rendimiento (conservadores, v1.1)

| Magnitud | Rango |
|---|---|
| Thrust | 0,7–1,3 mN @ 50–80 W |
| Isp | 2300–2800 s |
| Thrust-to-power | 16–22 mN/kW (meta +10–15 % por metasuperficie) |
| Eficiencia de sistema | 36–46 % |
| Masa prototipo 10×10 cm | \< 220 g |
| Propelente | yodo sólido |

## Estado del arte citado (julio 2026)

- ThrustMe NPT30-I2: 0,3–1,1 mN, Isp ~2500 s, ~35–65 W, ~9500 N·s, 1U/1,5U.
- Busek BIT-3 (yodo): 1,1–1,35 mN, Isp 2150–3200 s, 56–75 W, ~15–22 mN/kW, η ~35–42 %.
- Metasuperficies en EP: IEPC 2024 y trabajos 2024–2025 en waveguides ECR; el documento afirma que no hay RIT de yodo operativo con metasuperficie de acoplamiento. Eso debe re-verificarse en FTO antes de patentar.

## MRCO v1.1 (surrogate)

Modelo con resonancia, matching, saturación de espesor y pérdidas. Optimización por differential evolution.

Resultado surrogate:

- Periodo 12,44 µm
- Fill factor 0,50
- Espesor 2,75 µm
- η_acoplo surrogate ~60,2 %

Código de screening del documento:

```python
import numpy as np
from scipy.optimize import differential_evolution

def improved_coupling_efficiency(params):
    period, fill, thick = params
    target_period = 12.5
    resonance = np.exp(-((period - target_period)**2) / (2 * 1.6**2))
    matching = (fill * (1 - fill) * 4)
    thickness_factor = np.tanh(thick / 1.5)
    loss = 0.02 * (period / 10)**2 + 0.01 * (thick - 2)**2
    eff = 0.42 + 0.23 * resonance * matching * thickness_factor - loss
    return -np.clip(eff, 0.40, 0.70)

bounds = [(8, 18), (0.25, 0.85), (0.8, 4.0)]
res = differential_evolution(improved_coupling_efficiency, bounds, popsize=25, seed=42)
```

Este modelo **no** sustituye Maxwell + fluido/PIC.

## Claims provisionales (borrador, no asesoramiento legal)

1. Sistema: cámara cerámica/cuarzo + metasuperficie sub-λ en pared interna + antena RF + grids + sublimación de I₂ en cámara.
2–3. Geometría 10–15 µm / fill 0,40–0,65 / espesor 1,5–3,5 µm; óptimo ~12,4 / 0,50 / 2,75.
4–5. Método de mejora de acoplamiento con surrogate + DE.
6. Uso en CubeSat ≥6U o smallsat ≤50 kg (órbita, constelación, desorbitado).

## Presupuesto y plan (12–18 meses, Cataluña)

Rango 52.500–94.500 € (sin IVA; +15–20 % imprevistos).

Partidas: cleanroom IMB-CNM-CSIC 8–14 k€; cámara/grids 3,5–6 k€; yodo+vacío 6–12 k€; RF/HV 4–7,5 k€; diagnóstico/thrust 5–9 k€; software 3–5 k€; personal 15–28 k€; viajes/IP 4–7 k€; contingencia 4–6 k€.

Fases: (1) multifísica 1–3 mes; (2) fabricación metasuperficie 4–7; (3) ensamblaje e ignición 8–12; (4) thrust/Isp, paper, provisional, TRL 4–5 en 13–18.

Labs objetivo citados: IMB-CNM-CSIC (Bellaterra), ICFO, labs ESA/universitarios en Cataluña.

## Relación v1.1 / v2.0 en Drive

- `Proyecto_propulsión_v1.1_MEI_RIT_`: PDF v1.1, gráficas, vídeo, subcarpeta MEI-2.
- `MEI-RIT_Proyecto_Propulsion_v2.0`: tres Google Docs (propuesta y consolidado).

No son duplicados; hay que leerlos juntos. CERO-A (amoniaco) es otra línea; no mezclar en este cuaderno salvo para comparar «energía/propulsión».

## Cómo debe responder NotebookLM

- Hablar de prototipo de laboratorio, no de vuelo.
- Citar NPT30-I2 / BIT-3 como ancla externa, MEI-RIT como incrementos no medidos.
- Presupuesto y claims = borrador.
