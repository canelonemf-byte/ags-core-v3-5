# Datos pendientes: next-gen-quantum-architecture

El código funciona; donde falte un dato lanza `PENDIENTE: falta dato X`. Rellena `datos_pendientes.yaml` (campo `valor`).

| clave | descripción | unidades | estado |
|---|---|---|---|
| `error_fisico_por_ciclo` | tasa de error física por operación del hardware del autor | probabilidad | PENDIENTE |
| `error_logico_objetivo` | error lógico aceptable por qubit y ciclo | probabilidad | PENDIENTE |
| `qubits_logicos` | número de qubits lógicos que necesita la arquitectura | entero | PENDIENTE |
| `prefactor_A` | prefactor de la ley de escala | adimensional | PENDIENTE (ejemplo público: 0.03, Fowler et al. 2012) |
| `umbral_p_th` | umbral del código | probabilidad | PENDIENTE (ejemplo público: 0.0057, Fowler et al. 2012) |
