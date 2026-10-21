# sim/ — MVM: baseline CMOS digital vs CIM memristivo multinivel

**Nivel de evidencia: E2 (simulación propia, no experimento, no reproducida por terceros).**

- `parametros.yaml`: todos los parámetros; **todos marcados `supuesto`** (órdenes de magnitud ilustrativos, sin fuente de literatura verificada).
- `sim_mvm.py`: MVM 256×256, 200 vectores, semilla fija 20261020. Ejecutar: `python3 sim_mvm.py` (requiere numpy, pyyaml).
- `salidas/resultados.csv|json`: error relativo (norma L2 vs MVM exacta en float) y energía por configuración.

## Modelo
- CMOS: E = K·N·M·e_mac + N·M·e_lectura_peso; pesos/entradas cuantizados a 8 bits.
- CIM: pesos diferenciales (2 celdas) cuantizados a L niveles + ruido gaussiano de programación y lectura; salida cuantizada por ADC de b bits.
  E = celdas + DAC (por fila y vector) + ADC (por columna, lineal en bits) + calibración por vector.

## Limitaciones
Sin no linealidades del dispositivo, IR-drop, deriva temporal, variabilidad ciclo a ciclo, ni tiling/acumulación parcial; ADC lineal en bits (en realidad suele crecer más rápido); el ahorro energético es consecuencia directa de los supuestos y no es una predicción.
