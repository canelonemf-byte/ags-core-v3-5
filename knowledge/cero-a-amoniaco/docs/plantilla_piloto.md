# plantilla_piloto

- autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial
- nivel_evidencia: e2 (organigrama propuesto; valores = supuestos del modelo o fuentes citadas)
- fecha: 2026-11-05 (Europe/Madrid)
- detalle: ver tambien proyecto_ejecucion/cronograma.md y proyecto_ejecucion/scripts/recalcular_lcoa_bom.py
- decision: **opcion B — vigilancia remota compartida** (cerrada p6; Lazaro 2026-11-05)
- rol_autor: Lazaro y la IA aportan idea y proyecto; inversion, ejecucion y operacion = terceros con planta existente

## datos con fuente
- XXI convenio general industria quimica, tablas 2026 (BOE-A-2026-3870): minimos brutos grupos 1-8 20311-53825 EUR/a; proceso continuo 25024-58538 EUR/a (recogido 2026-10-26)
- INE ETCL/EACL 2024: coste laboral medio 37525.40 EUR/trabajador/a
- produccion modelo v3: 422.6 t NH3/a

## supuestos (no verificados)
- cotizacion empresa ~30 % sobre bruto: coste grupos 4-6 ~34-45 kEUR/a
- coste_fte base del modelo: 45000 EUR/a (rango 37525-60000)
- partner con planta quimica / H2 existente en El Prat o entorno industrial (Puerto / Zona Franca / poligono): permite vigilancia remota compartida y evita alquiler de parcela propia

## organigrama cerrado — Opcion B

| Rol | FTE | Notas | Fuente |
|---|---:|---|---|
| Responsable tecnico (diurno + guardias) | 1.0 | Unico interlocutor APQ/ATEX | supuesto organigrama |
| Operador diurno / mantenimiento | 0.5-1.0 | Rondas, muestreo, cisternas | supuesto |
| Centro de control remoto compartido | 0.3-0.5 | Contrato con partner; coste del servicio **PENDIENTE DE VERIFICACION** | supuesto |
| **Total** | **1.5-2.5** | Caso base LCOA BOM: **2.0 FTE** | recalcular_lcoa_bom.py |

### Coste personal caso base B
- 2.0 FTE × 45000 EUR/a = **90000 EUR/a** → **213 EUR/t** NH3
- Rango sensible: 1.5 FTE → 160 EUR/t; 2.5 FTE → 266 EUR/t (a 45 kEUR/a)

### Opcion A (descartada para este paquete)
- turnos propios 24/7 ≈ 5.5 FTE; 190-265 kEUR/a; mas cara que el modelo v3 (4 FTE)
- queda documentada solo como alternativa si un tercero exige presencia continua sin partner

## emplazamiento — socio con planta existente
- sin alquiler de parcela propia (antes 3000 m2 × 8.5 EUR/m2/mes = 306000 EUR/a ≈ 724 EUR/t)
- coste de compartir instalacion (canon, utilities, seguridad, seguros prorrateados): **PENDIENTE DE VERIFICACION** (0 EUR en caso base hasta oferta del partner)
- impacto LCOA si el partner cobra 50-150 kEUR/a: +118 a +355 EUR/t (aritmetica; no sustituye cotizacion)

## sensibilidad aritmetica: coste de personal EUR/t NH3 = fte * coste_fte / 422.6
| fte | 34 kEUR/a | 37.5 kEUR/a | 45 kEUR/a (base) | 60 kEUR/a |
|---|---|---|---|---|
| 1.5 | 121 | 133 | 160 | 213 |
| 2 | 161 | 178 | 213 | 284 |
| 2.5 | 201 | 222 | 266 | 355 |
| 4 | 322 | 355 | 426 | 568 |
| 5.5 | 443 | 488 | 586 | 781 |

## cierre p6
- [x] Lazaro elige B (vigilancia remota compartida)
- [x] LCOA recalculado con personal B, sin alquiler propio, compartir instalacion = PENDIENTE
- [ ] confirmar convenio provincial o de empresa del partner
- [ ] sustituir rango personal_fte/coste_fte y fee de partner en simulacion v4 tras cotizaciones
