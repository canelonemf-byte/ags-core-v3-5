# README reproducible — CERO-A piloto El Prat

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial  
**Fecha:** 2026-11-05 (Europe/Madrid)  
**Nivel de evidencia:** **E2 (simulación)**. No hay datos experimentales propios.  
**Veredicto:** el piloto **no es rentable hoy** frente al amoníaco gris (LCOA opción B ≈ **2208 EUR/t**; antes 3145 con 4 FTE+alquiler; gris **383–562 EUR/t**).

Este paquete permite a terceros **reproducir los cálculos** y auditar supuestos **sin supervisión** del autor. No autoriza contactar proveedores ni presentar el proyecto como inversión rentable.

## 1. Contenido de `proyecto_ejecucion/`

| Archivo | Qué es |
|---|---|
| `bom.json` / `bom.md` | Lista de materiales con proveedores candidatos, URLs y precios citados |
| `presupuesto.json` / `presupuesto.md` | CAPEX/OPEX/LCOA recalculado + sensibilidad + veredicto |
| `permisos_y_normativa.md` | SEVESO, APQ, ATEX, licencia El Prat, RFNBO con enlaces oficiales |
| `cronograma.md` | Cronograma 18–24 meses, organigrama A/B, riesgos, contactos **públicos** |
| `README_reproducible.md` | Este archivo |
| `estado_llp.json` | Estado del paquete en formato LLP |
| `scripts/recalcular_lcoa_bom.py` | Recalcula LCOA a partir de unitarios BOM (opción B) |
| `dossier_terceros/` | Resumen ejecutivo, modelo colaboración, índice |
| `interesados.json` / `interesados.md` | Entidades + contactos públicos (no enviados) |
| `borradores_contacto/` | Borradores de correo (no enviados) |

## 2. Código y datos del modelo (conservados)

Raíz del proyecto: `/workspace/cero-a/` (o el clon que recibas).

| Ruta | Rol |
|---|---|
| `simulacion_cero_a_v3.py` | Núcleo LCOA + RFNBO + Monte Carlo |
| `construir_v3.py` | Orquestación / informe / gráficos |
| `datos_cero_a.py` | Descarga/preparación series |
| `resultados.json` | Salida canónica v3 |
| `informe.md` | Informe humano v3 |
| `estado_cero_a.json` | Estado LLP del proyecto |
| `docs/plantilla_piloto.md` | Personal / convenio |
| `v1/`, `v2/` | **Prototipos E2 previos — no borrar** |
| `data/` | Series meteo/precios cacheadas |
| Knowledge AGs-Core | `agsgpt/ags-core-v3.6/knowledge/cero-a-amoniaco/informe_v3.md` |

## 3. Requisitos

```bash
cd /workspace/cero-a   # o ruta local
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Sistema: Linux o macOS; ~4–8 GB RAM para MC; red solo si regeneras datos (PVGIS / Open-Meteo / Energy-Charts).

## 4. Reproducir resultados v3

```bash
# Opción A — usar resultados ya generados
python3 - <<'PY'
import json
r=json.load(open("resultados.json"))
e=r["datos_clave"]["escenarios"]["ppa_rfnbo_horario"]
print("LCOA", e["lcoa_eur_t"], "EUR/t")
print("diseño", e["diseno"])
print("RFNBO horario", e["rfnbo"]["cumple_horaria_desde_2030"])
PY

# Opción B — regenerar (costoso; ~3–5 min)
# python3 construir_v3.py
```

Emplazamiento fijado: **El Prat de Llobregat ≈ 41.30 N, 2.08 E**.

## 5. Recalcular LCOA con la BOM

```bash
python3 proyecto_ejecucion/scripts/recalcular_lcoa_bom.py
# lee bom.json + supuestos alineados a v3; escribe data/lcoa_bom_recalc.json
```

El script **no** re-optimiza el diseño ni reejecuta series horarias; usa la producción 422,6 t/a y el desglose energético del escenario PPA v3.

Caso base **2026-11-05:** organigrama **B** (2 FTE), sin alquiler de parcela propia, `compartir_instalacion=0` marcado **PENDIENTE DE VERIFICACIÓN**. Salida esperada ≈ **2208 EUR/t**.

## 6. Cómo interpretar números

1. **E2 ≠ E3:** no hay campaña experimental.
2. Precios EHO PEM **2196 EUR/kW** son de proyectos ~**100 MW**; el piloto 0,5 MW puede costar más → **PENDIENTE DE VERIFICACIÓN**.
3. CAPEX HB/PSA escalados desde literatura 20 t/d → **no son ofertas**.
4. Cumplimiento RFNBO del PPA usa **perfil nacional** Energy-Charts, no un PPA firmado.
5. Gris 383–562 EUR/t es rango de modelo; mercado spot puede diferir.

## 7. Autoría y licencia de uso

- Autoría de contenido: **Lázaro López Paz, El Prat de Llobregat, Barcelona, España**, con asistencia de IA.
- Sin afiliaciones institucionales.
- Uso permitido: auditoría, reproducción académica, preparación de cotizaciones **por el titular**.
- Uso **no** permitido sin permiso escrito: presentarlo como estudio de inversión rentable; contactar en nombre del autor; publicar omitiendo el veredicto de no rentabilidad y el nivel E2.

## 8. Formato LLP del paquete

Ver `estado_llp.json`.
