<!-- Fuente: Drive NotebookLM_Fuentes_2026-08-30 · https://docs.google.com/document/d/1p8bLwj2JHPAxDSLq6E8M2-v3d60dmNcPO_UzoJ3vaJg/edit · copia de texto, sin cambios de contenido -->

# Fuente NotebookLM — Helio-3 / Reactor QMC-H3

**Inventor:** Lázaro López Paz, El Prat de Llobregat, Barcelona.
**Estado de evidencia:** concepto + modelado 0D/1D. No es resultado experimental de plasma ni demostración de Q > 1.
**Fecha de esta fuente:** 2026-08-30.

## Ficha de gobernanza

```
Estado: hipótesis / simulación 0D-1D
Pregunta técnica: ¿puede un tokamak esférico compacto D-³He, con metamateriales magnéticos y control híbrido IA+VQA, mejorar τ_E lo bastante para acercarse a ganancia neta?
Alcance: diseño conceptual y números de un modelo 0D/1D.
Limitaciones: el propio resumen da Q inicial ≈ 0,04 y P_loss_total ≈ 821 MW frente a ~29 MW de fusión; la viabilidad depende de supuestos de τ_E ×3 y de densidad no validados en dispositivo.
Evidencia disponible: documento de resumen + PDFs de proyecto en Drive.
Próximo hito verificable: simulación 1,5D/2D (transporte + MHD) con código nombrado, malla y supuestos publicados; no un vídeo ni un PDF ilustrado.
```

## Qué es este clúster

Familia Helio-3 del portfolio:

1. Recolección / harvesting lunar o espacial de ³He.
2. Reactor de fusión aneutrónica QMC-H3 (edición española).
3. Plataforma IQM-He3-Anti.
4. HelioAtlas (web de catálogo; en Drive está incompleta: hay config Vite sin `src/`).
5. Carpeta fechada `26_8_2026_Helio 3 proyectos`.

## Arquitectura declarada del QMC-H3 (según resumen maestro)

- Máquina: tokamak esférico compacto, R = 2,0 m, a = 1,0 m, κ = 2,0, volumen de plasma ≈ 79 m³.
- Combustible: D-³He.
- Campo: imanes HTS REBCO, 8–12 T.
- Primera pared: W-Cr-Y.
- Diagnóstico propuesto: centros NV en diamante.
- Control: capa cuántica (VQA / Quantum ML) + capa clásica (PINNs + Deep RL) sobre un gemelo digital.
- Metamateriales: SRR nanoestructurados Nb/YBCO/grafeno; μ_eff \< 0 y régimen ENZ; metamateriales fotónicos para devolver sincrotrón al núcleo.

## Números del modelo 0D citados en el resumen

| Magnitud | Valor en el documento | Lectura prudente |
|---|---|---|
| n | 5×10²⁰ m⁻³ | supuesto de diseño |
| T_i / T_e | 70 / 60 keV | punto de operación D-³He típico de papel, no medido aquí |
| τ_E «mejorado» | 4,5 s (×3 vs base no detallada) | palanca principal del relato; hay que fijar el τ_E de referencia |
| Triple producto | 1,58×10²³ m⁻³ keV s | output del mismo modelo |
| P_fusión | ≈ 29 MW | |
| P_loss_total | ≈ 821 MW | incluye transporte + radiación «conservadora» |
| Auto-calentamiento | 85 % de 25 MW | coherente con P_fusión baja |
| Q inicial | ≈ 0,04 | el documento lo admite; Q > 1 queda como objetivo de escalado de densidad/τ_E |
| r_L protones 14,7 MeV | ≈ 55 mm | a 8–12 T |
| r_L alfas 3,6 MeV | ≈ 27 mm | |

Conclusión interna del propio texto: la mejora ×3 de τ_E es el impulsor para mover el diseño hacia Q > 1. Eso convierte τ_E en el supuesto que hay que atacar primero.

## Componentes físicos listados

- Solenoide central para corriente y shaping.
- Pared de wolframio de baja activación.
- Conversión directa de partículas cargadas: inducción + MHD + rectenas (concepto; sin banco de pruebas en esta fuente).

## Cómo debe responder NotebookLM sobre este proyecto

- No afirmar «reactor listo» ni «fusión neta demostrada».
- Separar: (a) estado del arte D-³He / tokamak esférico / HTS, (b) propuesta de metamaterial + control, (c) cifras 0D.
- Si se pide hoja de ruta: Fase 1 = simulación detallada y validación estructural, como dice el documento, no fabricación de un tokamak.

## Fuentes Drive recomendadas

Ver `99_MAPA_CARGAS.md` sección 1.
