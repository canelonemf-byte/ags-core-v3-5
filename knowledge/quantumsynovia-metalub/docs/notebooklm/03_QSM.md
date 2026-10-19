<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/11bj0nA3Z6e19h49ZloIoiPKbJsC04PLNh9AaOJH0vRQ/edit · copia de texto, sin cambios de contenido -->

# Fuente NotebookLM — QuantumSynovia MetaLub (QSM)

**Inventor:** Lázaro López Paz, El Prat de Llobregat, Barcelona.
**Estado de evidencia:** diseño molecular + DFT/cluster + protocolos de síntesis/DoE/tribología **no ejecutados en este paquete como campaña experimental completa**.
**Clasificación regulatoria pretensión:** dispositivo/combinado; no es tratamiento aprobado.
**Fecha base del informe publicable:** julio 2026.

## Ficha de gobernanza

```
Estado: hipótesis + simulación DFT de clusters + protocolos de laboratorio
Pregunta técnica: ¿un HA de alto Mw con puente siloxano, Mg²⁺ y SPIONs puede estabilizar capas de hidratación (QHE Shells) y bajar μ por debajo de 0,005 en condiciones articulares?
Limitaciones: ΔE y Factor QHE salen de modelos de cluster, no de un tribómetro sobre cartílago humano. No hay ensayo clínico en estas fuentes.
Próximo hito verificable: síntesis de un lote de 100 mL, QC (pH, viscosidad, endotoxinas) y μ en tribómetro a 37 °C vs HA comercial y PBS.
```

Aviso: esto no es receta de uso en personas. Síntesis y ensayos solo en laboratorio autorizado. ISO 10993 / GMP / AEMPS antes de cualquier uso humano.

## Concepto

Hidrogel inyectable para osteoartritis:

- AH 1,5–3,0 MDa.
- Puente siloxano covalente (diamino-siloxano + EDC/NHS).
- Dopaje Mg²⁺ (condrogénesis) y Fe₃O₄ 5–10 nm (SPIONs).
- Idea de QHE Shells: agua estructurada sub-nm; métrica propia Factor QHE.

Objetivo declarado: lubricación de frontera duradera + microambiente regenerativo, no solo viscosuplementación de 6–12 meses.

## DFT (nivel de teoría declarado)

- Funcional B3LYP-D3BJ.
- Base 6-31G(d,p) opt; def2-TZVP single-point.
- Solvente SMD agua.
- Correcciones BSSE, ZPE, 298/310 K.
- Clusters: disacárido HA + puente siloxano + 8–20 H₂O + Mg²⁺ + cluster Fe₃O₄ pequeño.

Resultados citados en el informe:

| Magnitud | Valor |
|---|---|
| ΔE_cross HA–Si–O–Si | −55,2 kcal/mol (BSSE) |
| ΔE_hyd QHE | −18,7 kcal/mol por capa |
| Gap HOMO–LUMO | 3,21 eV |
| Factor QHE | 6,8–7,2 (meta > 5) |

Definición implementada en script:

```python
def calculate_QHE_factor(hydration_energy, gap_ev):
    if hydration_energy is None or gap_ev is None:
        return None
    qhe = abs(hydration_energy) / 10.0 * (gap_ev / 3.0)
    return min(max(qhe, 0.0), 10.0)
```

Hay entradas Gaussian `.gjf` y logs en `Proyecto lubricación articulaciones humanas`, más `QSM_DFT_Postprocessing_Improved.py`. El log «simulated» no debe venderse como output de un run Gaussian institucional sin el archivo de salida completo.

## Formulación de laboratorio (100 mL, 3 % w/v) — solo I+D

- HA pharma 3,0 g
- Siloxano diamino 0,45 g
- EDC·HCl 0,60 g; NHS 0,35 g
- MgCl₂·6H₂O 0,80 g
- Fe₃O₄ recubiertas 0,20 g
- Si-QDs / SiO₂ mesoporoso opcional 0,05 g
- PBS pH 7,4 endotoxin-free c.s.p. 100 mL

Pasos resumidos: activación HA → injerto siloxano 4–6 h pH 7,8–8,2 → dopantes + sonicación suave → pH 7,4 → diálisis MWCO 10–50 kDa 24–48 h → 0,22 µm → jeringas.

QC declarado: pH 7,2–7,6; η 800–5000 mPa·s @ 10 s⁻¹; endotoxinas \< 0,25 EU/mL; μ \< 0,01.

## DoE

Factores: %HA (2/3/4), ratio siloxano/HA (10/15/20), %Mg (0,5/0,8/1,2), %Fe₃O₄ (0,1/0,2/0,3), gelificación (térmica-pH vs foto-UV).
Diseño: 2^(5−1) resolución IV + 4–6 centros.
Respuestas: QHE, μ, viscosidad, G', COL2A1, PdI.

## Tribología propuesta

Ball-on-flat o pin-on-disk, 37 °C, 1/5/10 N, 5/20/50 mm/s, 50–100 µL, ≥3 réplicas. Contrapartes: cartílago bovino fresco y vidrio con HA/fosfolípidos. Controles: PBS, HA comercial, cartílago-cartílago.

Criterio: μ medio \< 0,01; ideal \< 0,005; deriva \< 20 %.

## Cómo debe responder NotebookLM

- Distinguir protocolo vs resultado medido.
- No afirmar cura de osteoartritis ni μ medido en paciente.
- Unificar dossier QSM + carpeta DFT; ignorar «Registro Maestro» duplicados.
