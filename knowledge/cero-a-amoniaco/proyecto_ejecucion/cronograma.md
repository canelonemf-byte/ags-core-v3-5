# Cronograma, riesgos, organigrama y contactos públicos — CERO-A

- **Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial
- **Fecha:** 2026-11-05 (Europe/Madrid)
- **Advertencia:** **NO se ha contactado a nadie.** Las direcciones son públicas; cualquier envío requiere aprobación explícita de Lázaro.

## 1. Cronograma realizable (18–24 meses a FID/arranque frío)

| Fase | Meses | Actividades | Hito | Dependencias |
|---|---|---|---|---|
| F0 Preparación | 0–2 | Cerrar modo de operación; brief EPC; NDA plantillas; lista RFIs equipos | Kick-off interno | Decisión Lázaro |
| F1 Cotizaciones | 1–4 | p1 suelo (≥3 ofertas); p2 PEM+HB+PSA+buffer+tanque; p3 PPA; p7 e-distribución | CAPEX ±25 % | F0 |
| F2 Ingeniería básica | 3–7 | FEL-2: P&ID, ATEX, APQ, layout, balance masa/energía; p4 dictamen RFNBO | Basic design | F1 parcial |
| F3 Permisos | 5–14 | Licencia ambiental El Prat; APQ; PCI; conexión MT; (SEVESO si aplica) | Licencias presentadas / obtenidas | F2 |
| F4 FID | 8–12 | Ofertas firmes; contrato PPA; offtake; seguro; financiación | Go / no-go | F1–F3 |
| F5 Compra y obra | 12–20 | Pedido skids (lead time PEM/HB 9–15 meses típico **PENDIENTE DE VERIFICACIÓN**); obra civil | FAT / SAT | FID |
| F6 Comisionado | 18–24 | Pruebas H₂/N₂/NH₃; certificación RFNBO si procede; formación | Primer NH₃ especificación | F5 |
| F7 Operación piloto | 24+ | Campaña E3; datos para v4/v5 | Informe E3 | F6 |

**Ruta crítica:** cotización HB modular + licencia ambiental + lead time electrolizador.

## 2. Organigrama — dos opciones

### Opción A — Turnos propios 24/7 (proceso continuo)

Hipótesis: planta siempre atendida; convenio química proceso continuo.

| Rol | FTE | Perfil / grupo orientativo | Coste laboral orientativo EUR/a | Fuente |
|---|---:|---|---:|---|
| Responsable de planta / proceso | 1 | Grupo 6–7 | 45–60 k (bruto+cotiz. empresa ~) | XXI convenio + supuesto cotización |
| Operador turno A/B/C/D | 4 | Grupo 4–5 continuo | 34–45 k c/u | plantilla_piloto.md |
| Mantenimiento / instrumentación (compartido) | 0,5 | Grupo 5 | 20–25 k prorrateado | supuesto |
| **Total** | **~5,5** | | **~190–265 k** | |

- Modelo v3 usaba **4 FTE × 45 k = 180 k EUR/a** (426 EUR/t). Opción A es **más cara** que el modelo.
- Cobertura 24/7 real suele exigir ≥5 personas en rotación.

### Opción B — Vigilancia remota compartida (recomendada a escala piloto si hay partner)

Hipótesis: skids altamente automatizados; parada segura ante alarma; vigilancia compartida con instalación vecina (química / H₂) o empresa de monitoreo industrial; visitas diurnas.

| Rol | FTE | Notas |
|---|---:|---|
| Responsable técnico (diurno + guardias) | 1 | Único interlocutor APQ/ATEX |
| Operador diurno / mantenimiento | 0,5–1 | Rondas, muestreo, cisternas |
| Centro de control remoto compartido | 0,3–0,5 | Contrato con partner; **PENDIENTE DE VERIFICACIÓN** coste |
| **Total** | **~1,5–2,5** | Alineado al mínimo del rango modelo (2 FTE) |

**Impacto LCOA (2026-11-05):** opción B con **2 FTE** + sin alquiler propio → LCOA ≈ **2208 EUR/t** (sigue sin ser rentable vs gris; fee partner = PENDIENTE).

**Decisión cerrada:** **B** (Lázaro 2026-11-05). Autor solo idea/proyecto; ejecución por terceros con planta existente.

## 3. Riesgos (registro operativo)

| ID | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | No rentable vs gris a 50 kg/h | alta | alto | no vender como negocio; buscar offtake premium / escala |
| R2 | Alquiler 6,5–11 EUR/m²·mes domina LCOA | alta | alto | p1; suelo propio; partner en planta existente |
| R3 | Sin cotización HB a 1–2 t/d | alta | alto | Proton Ventures / Casale / Uhde; aceptar lead time |
| R4 | Adicionalidad PPA / activos existentes ES | alta | alto | p3+p4; calendario <2028; vigilar revisión 1184 |
| R5 | Servidumbres aeropuerto El Prat | media | alto | consulta Aena / urbanismo antes de parcela |
| R6 | Double-counting BoP en ofertas | media | medio | matriz de alcances en RFI |
| R7 | Ayudas no elegibles (<5 MWe) | alta | medio | fuera de caso base |
| R8 | Interpretar E2 como E3 experimental | media | alto | watermark en todos los docs |
| R9 | Fuga H₂/NH₃ / ATEX | baja–media | alto | diseño APQ, detectores, formación |
| R10 | Retraso licencia Annex II | media | medio | preconsulta municipal mes 1 |

## 4. Proveedores candidatos (solo contactos públicos — no contactar)

### Equipos

| Equipo | Organización | URL pública |
|---|---|---|
| PEM | Nel Hydrogen | https://nelhydrogen.com/product/mc-series-pem/ |
| PEM | H-TEC SYSTEMS (ME450) | https://www.h-tec.com/en/products/detail/h-tec-pem-electrolyser-me450/me450 |
| PEM | ITM Power | https://itm-power.com/products/ |
| PEM | Siemens Energy | https://www.siemens-energy.com/global/en/home/products-services/product-offerings/hydrogen-solutions.html |
| HB modular | Proton Ventures | https://protonventures.com/what-we-do/ammonia-production/ |
| HB / license | Casale SA | https://www.casale.ch/ |
| HB | thyssenkrupp Uhde | https://www.thyssenkrupp-uhde.com/ |
| HB | Stamicarbon NX STAMI | https://www.stamicarbon.com/ |
| PSA N₂ | CEZIUM | https://cezium.eu/en/produits/generators/nitrogen-psa/cz-n2m-50b/ |
| PSA / gases | Air Products | https://www.airproducts.com/ |
| Buffer H₂ | Luxfer | https://www.luxfercylinders.com/product/g-stor-pro-bundle/ |
| Buffer H₂ | Hexagon Purus | https://www.hexagonpurus.com/ |
| Compresión H₂ | Howden | https://www.howden.com/en-gb/products/compressors/hydrogen-compressors |
| Benchmark costes | European Hydrogen Observatory | https://observatory.clean-hydrogen.europa.eu/hydrogen-landscape/production-trade-and-cost/electrolyser-cost |

### Interesados / ecosistema (públicos)

| Actor | Por qué | URL / contacto público |
|---|---|---|
| Ajuntament del Prat | Licencia / suelo | https://www.elprat.cat/ ; sede: https://seu.elprat.cat/ |
| Zona Franca Barcelona | Suelo industrial | https://www.zfbarcelona.es/ |
| Port de Barcelona | Logística NH₃ / H₂ | https://www.portdebarcelona.cat/ |
| IREC | I+D energía | https://www.irec.cat/ |
| Clúster hidrógeno / AEH2 | Networking H₂ | https://www.aeh2.org/ |
| CIDETE / química BCN | Offtake industrial | buscar en directorios públicos — **PENDIENTE** lista nominativa verificada |
| ISCC / CertifHy | Certificación RFNBO | https://www.iscc-system.org/ ; https://www.certifhy.eu/ |
| IDAE | Ayudas (si abre convocatoria) | https://www.idae.es/ |
| e-distribución | Conexión MT | https://www.edistribucion.com/ |

**Política de contacto:** borrador de RFI en `data/` solo tras “sí” explícito de Lázaro con destinatario y texto.

## 5. Formato LLP

```yaml
meta:
  proyecto: cero_a
  documento: cronograma_organigrama_contactos
  fecha: "2026-11-04"
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial"
objetivo: plan_ejecucion_18_24_meses_sin_contactos_externos
datos_clave:
  duracion_meses: [18, 24]
  organigrama_opciones: [turnos_24_7, vigilancia_remota]
  contactos_realizados: []
tareas:
  - id: c1
    tarea: decision A vs B organigrama
    estado: pendiente_lazaro
riesgos: [R1, R2, R3, R4, R5]
decisiones:
  - decision: no_contactar_sin_aprobacion
    estado: hecho
proximo_paso: Lazaro elige opcion A o B y autoriza o no RFIs
```
