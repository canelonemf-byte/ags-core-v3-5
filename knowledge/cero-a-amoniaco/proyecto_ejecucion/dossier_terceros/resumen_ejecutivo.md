# CERO-A — Resumen ejecutivo para terceros

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial  
**Fecha:** 2026-11-05 (Europe/Madrid)  
**Nivel de evidencia:** **E2 (simulación)**. No hay datos experimentales propios.  
**Rol del autor:** aporta la **idea y el proyecto** (modelo, BOM, permisos, plan). La **inversión, construcción y operación** corresponden a terceros con capacidad industrial.

---

## Qué es CERO-A

Prototipo de **amoníaco renovable (RFNBO)** a escala piloto (~50 kg/h NH₃; ~423 t/a) localizado en **El Prat de Llobregat / entorno Puerto–Zona Franca**. Cadena: electrólisis PEM → buffer H₂ → PSA N₂ → bucle Haber–Bosch → tanque NH₃. Caso preferente: **PPA renovable** con correlación horaria (Reglamentos UE 2023/1184 y 2023/1185).

## Veredicto honesto (hoy)

| Métrica | Valor |
|---|---|
| LCOA caso B (BOM, 2026-11-05) | **~2208 EUR/t** |
| LCOA v3 original (4 FTE + alquiler) | 3166 EUR/t |
| LCOA BOM anterior (4 FTE + alquiler) | 3145 EUR/t |
| Amoníaco gris (rango modelo) | **383–562 EUR/t** |
| Ratio verde / gris | **~3,9–5,8×** |
| ¿Rentable hoy frente al gris? | **No** |

**Organigrama B** (cerrado): vigilancia remota compartida (~2 FTE), **sin parcela propia**, coste de compartir instalación con partner = **PENDIENTE DE VERIFICACIÓN** (0 EUR en caso base hasta oferta).

El piloto **no** debe presentarse como negocio rentable frente al gris. Sirve para: (1) reproducir números, (2) preparar ingeniería y permisos, (3) cotizar equipos/PPA/partner, (4) situar un offtake RFNBO cuando el mercado madure.

## CAPEX orientativo

- Partidas ya precificadas (literatura / BOM): ~**3,1 M€**  
- Con pendientes a punto medio: ~**4,1 M€**  
- **No es oferta vinculante.** Precios PEM a escala ~100 MW y HB/PSA escalados desde literatura → **PENDIENTE DE VERIFICACIÓN** con cotizaciones.

## Qué lo haría más cercano a realizable / competitivo

1. **Escala:** a 50 kg/h los fijos dominan; 5–10× diluye personal (y fee de partner). Sensibilidades en `presupuesto.json` son aritméticas, no reoptimizaciones.  
2. **Partner con planta existente** (decisión tomada): evita ~724 EUR/t de alquiler; exige fee real de utilities/seguridad.  
3. **CBAM / ETS / precio del CO₂:** paridad pura solo con CO₂ del orden ~1300–1400 EUR/tCO₂ (irreal a corto plazo). Un combo **escala + prima de producto + CO₂** es más creíble que CO₂ solo.  
4. **Mandatos / offtake RFNBO** (marítimo, fertilizantes, química): prima sobre gris aún inmadura; sin contrato de compra el LCOA verde no cierra.  
5. **Ayudas:** H₂ Pioneros / Hydrogen Bank (≥5 MWe) — el piloto **0,5 MW no es elegible** en el caso base; vigilar convocatorias IDAE/PERTE.  
6. **Cotizaciones reales** (p1 suelo/partner, p2 equipos, p3 PPA) y dictamen RFNBO (p4) antes de FID.

## Qué incluye el paquete reproducible

BOM, presupuesto, permisos (SEVESO/APQ/ATEX/licencia/RFNBO), cronograma 18–24 meses, script de recálculo LCOA, código v3 y prototipos E2 previos (`v1/`, `v2/`). Índice: `dossier_terceros/indice_paquete.md`.

## Qué **no** se ha hecho

- No se ha contactado a nadie ni enviado este dossier.  
- No hay compromiso de inversión del autor.  
- No hay afiliación institucional.

## Próximo paso para un tercero interesado

Leer `modelo_colaboracion.md`, reproducir LCOA con `scripts/recalcular_lcoa_bom.py`, y —si procede— responder al borrador de contacto correspondiente **solo tras autorización expresa de Lázaro López Paz**.
