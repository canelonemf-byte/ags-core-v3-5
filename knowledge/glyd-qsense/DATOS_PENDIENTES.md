# Datos pendientes: glyd-qsense

El código funciona; donde falte un dato lanza `PENDIENTE: falta dato X`. Rellena `datos_pendientes.yaml` (campo `valor`).

| clave | descripción | unidades | estado |
|---|---|---|---|
| `temperaturas_calibracion_k` | temperaturas de referencia de la calibración | K (lista) | PENDIENTE |
| `parametro_espectral` | parámetro Raman medido en cada temperatura (posición de la banda C-D, cociente...) | cm⁻¹ o adimensional (lista) | PENDIENTE |
| `sigma_parametro` | desviación típica del parámetro en medidas repetidas | mismas que el parámetro | PENDIENTE |
| `espectros_crudos` | ruta a los espectros Raman crudos para la 1D-CNN | ruta | PENDIENTE |
