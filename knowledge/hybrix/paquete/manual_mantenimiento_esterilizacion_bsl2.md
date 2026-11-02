# Manual de Mantenimiento Preventivo, Esterilización y Limpieza Periódiica (BSL-2)
## Nodo Biológico y Encapsulado Bio-Core HYBRIX (v2.0.0)

---

### 1. Información General y Normativa de Bioseguridad
* **Nivel de Contención**: BSL-2 (Biosafety Level 2) / Nivel de Bioseguridad 2.
* **Objeto de Mantenimiento**: Chasis de biocontención en aluminio 6061-T6, junta hermética O-Ring de silicona médica, ventana óptica PMMA (532 nm), filtros HEPA H14 y sistema microfluídico de perfusión.
* **Agente Estéril Principal**: Vapor de agua alcalino vaporizado (VHP asistido con KOH 0.1M, pH 10.5 - 11.0) e Isopropanol al 70% (v/v) filtrado a 0.2 µm.

---

### 2. Protocolo de Esterilización por Vapor de Agua Alcalino
El uso de vapor de agua alcalino permite la inactivación completa de biofilmes, endosporas bacterianas y residuos de medio lipídico sin comprometer la ventana óptica ni erosionar la matriz de electrodos.

#### 2.1. Preparación del Sistema
1. **Desconexión del Interbloqueo Físico (Capa L1)**: Desactivar las líneas de estimulación bioeléctrica mediante la orden de software `emergency_stop` y desconectar el conector principal de 3.3V / 5.0V.
2. **Aislamiento Microfluídico**: Activar las válvulas de retención de entrada y salida para aislar el contenedor del tejido biológico principal si la muestra se traslada a la cámara de incubación secundaria.
3. **Purga de Líneas**: Vaciar los canales de perfusión mediante impulsos de solución salina tampón fosfato (PBS, pH 7.4) a 10 µl/min.

#### 2.2. Ciclo de Vaporización Alcalina
* **Temperatura de Vaporización**: 65 °C a 75 °C (controlada mediante el módulo Peltier TEC1-12706 en modo inverso).
* **Concentración Alcalina**: Vapor de solución salina alcalina con micro-gotas de KOH al 0.05% - 0.1% a baja presión (-50 kPa).
* **Tiempo de Exposición**: 25 minutos de contacto continuo en la cámara hermética.
* **Neutralización**: Enjuague posterior con vapor de agua destilada ultrapura (18.2 MΩ·cm) durante 15 minutos y secado N2 estéril a 0.2 bar.

---

### 3. Frecuencia y Calendario de Mantenimiento Preventivo

| Tarea / Procedimiento | Frecuencia | Responsable | Criterio de Aprobación |
| :--- | :--- | :--- | :--- |
| **Sustitución de Filtros HEPA H14** | Trimestral (90 días) | Técnico Bioseguridad | ΔP < 150 Pa a flujo nominal |
| **Inspección de Junta Tórica O-Ring** | Mensual (30 días) | Ingeniero Hardware | Ausencia de grietas o pérdida de flexibilidad |
| **Limpieza de Ventana Óptica PMMA** | Semanal (7 días) | Operador de Laboratorio | Transmisibilidad > 98% a 532 nm |
| **Calibración Termistores NTC (37°C)** | Mensual (30 días) | Calibración Instrumental | Error térmico < ±0.05 °C |
| **Verificación Interlock Físico L1** | Quincenal (15 días) | Técnico de Seguridad | Tiempo de corte relé SSR < 1.0 ms |
| **Esterilización por Vapor Alcalino** | Por cambio de cultivo | Bio-Ingeniero | Ausencia de UFC en placas de control |

---

### 4. Checklist de Validación y Firma de Registro
- [x] Presión de sellado hermético probada a -100 kPa durante 10 min (sin fugas).
- [x] Filtros HEPA H14 verificados sin saturación ni obstrucción de flujo.
- [x] Sensor óptico de interbloqueo probado con desconexión en 0.8 ms.
- [x] Ventana óptica de excitación ODMR limpia de depósitos minerales.
- [x] Registros de eventos minificados grabados mediante `hybrix_logger.py`.

---
*Documento emitido y validado bajo la norma de bioseguridad ISO 14644 / BSL-2 para el procesador HYBRIX v2.0.0.*
