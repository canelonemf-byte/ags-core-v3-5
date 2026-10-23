# Datos pendientes: espana-sin-petroleo

El código funciona; donde falte un dato lanza `PENDIENTE: falta dato X`. Rellena `datos_pendientes.yaml` (campo `valor`).

| clave | descripción | unidades | estado |
|---|---|---|---|
| `anio_objetivo` | año en que se quiere alcanzar el objetivo | año | PENDIENTE |
| `fraccion_petroleo_restante` | fracción del consumo de petróleo del año base que queda en el año objetivo (0 = eliminación) | fracción | PENDIENTE |
| `vectores_sustitucion` | reparto de la sustitución por sector (electrificación, H2, biocombustibles) con eficiencias | tabla | PENDIENTE |
| `datos_ree` | series de generación de REE si se quieren añadir (apidatos.ree.es) | tabla | PENDIENTE |
