# Índice del paquete reproducible CERO-A (para terceros)

**Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial  
**Fecha:** 2026-11-05 (Europe/Madrid)  
**Evidencia:** E2 simulado · **Rentabilidad hoy vs gris:** no (LCOA B ≈ **2208 EUR/t**)  
**Envíos realizados:** ninguno

Rutas relativas a `proyecto_ejecucion/` salvo indicación.

## 0. Empezar aquí

| Documento | Contenido |
|---|---|
| [resumen_ejecutivo.md](resumen_ejecutivo.md) | 2 páginas: qué es, veredicto, palancas |
| [modelo_colaboracion.md](modelo_colaboracion.md) | Roles autor vs tercero; opciones L1–L4 (no consejo legal) |
| [../README_reproducible.md](../README_reproducible.md) | Cómo reproducir v3 y el LCOA BOM |
| [../interesados.md](../interesados.md) | Entidades con interés demostrable + contactos públicos |
| [../interesados.json](../interesados.json) | Misma lista en formato LLP/JSON |
| [../borradores_contacto/](../borradores_contacto/) | Borradores de correo (no enviados) |

## 1. Costes y materiales

| Documento | Contenido |
|---|---|
| [../bom.json](../bom.json) / [../bom.md](../bom.md) | Lista de materiales, proveedores, URLs, precios citados |
| [../presupuesto.json](../presupuesto.json) / [../presupuesto.md](../presupuesto.md) | CAPEX/OPEX/LCOA + sensibilidad |
| [../data/lcoa_bom_recalc.json](../data/lcoa_bom_recalc.json) | Último recálculo (opción B) |
| [../scripts/recalcular_lcoa_bom.py](../scripts/recalcular_lcoa_bom.py) | Script reproducible |

## 2. Permisos, plan y personal

| Documento | Contenido |
|---|---|
| [../permisos_y_normativa.md](../permisos_y_normativa.md) | SEVESO, APQ, ATEX, licencia El Prat, RFNBO |
| [../cronograma.md](../cronograma.md) | 18–24 meses, riesgos, contactos públicos |
| [../../docs/plantilla_piloto.md](../../docs/plantilla_piloto.md) | Organigrama **B** cerrado (p6) |
| [../estado_llp.json](../estado_llp.json) | Estado del paquete de ejecución |

## 3. Modelo y prototipos (raíz `/workspace/cero-a/` o clon)

| Ruta | Rol |
|---|---|
| `../../simulacion_cero_a_v3.py` | Núcleo LCOA + RFNBO + Monte Carlo |
| `../../construir_v3.py` | Orquestación / informe / gráficos |
| `../../datos_cero_a.py` | Series |
| `../../resultados.json` | Salida canónica v3 |
| `../../informe.md` | Informe humano v3 |
| `../../estado_cero_a.json` | Estado LLP del proyecto |
| `../../v1/`, `../../v2/` | **Prototipos E2 previos — conservar** |
| Knowledge AGs-Core | `agsgpt/ags-core-v3.6/knowledge/cero-a-amoniaco/` |

## 4. Reproducción rápida

```bash
cd /workspace/cero-a   # o ruta local del clon
python3 proyecto_ejecucion/scripts/recalcular_lcoa_bom.py
# → data/lcoa_bom_recalc.json  (debe dar ~2208 EUR/t en opción B)
```

## 5. Formato LLP (meta)

```yaml
meta:
  proyecto: cero_a
  documento: indice_paquete_terceros
  fecha: "2026-11-05"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial"
  nivel_evidencia: e2
objetivo: indexar_paquete_reproducible_sin_envio
datos_clave:
  lcoa_opcion_b_eur_t: 2208
  rentable_hoy_vs_gris: false
  envios_realizados: []
tareas: []
riesgos: []
decisiones:
  - decision: organigrama_b
    estado: hecho
  - decision: solo_idea_y_proyecto_autor
    estado: hecho
proximo_paso: autorizacion_envio_borradores_por_destinatario
```
