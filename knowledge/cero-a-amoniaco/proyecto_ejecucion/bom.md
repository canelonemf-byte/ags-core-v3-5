# BOM — CERO-A piloto El Prat (50 kg/h NH₃)

- **Autoría:** Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial
- **Fecha:** 2026-11-04 (Europe/Madrid)
- **Nivel de evidencia:** E2 (simulación + literatura; sin cotizaciones firmes)
- **Escenario base:** `ppa_rfnbo_horario` (diseño v3)
- **Advertencia:** ningún precio es oferta comercial. Lo no público se marca **PENDIENTE DE VERIFICACIÓN**.

## Caudales de diseño
- H₂ nominal: **9.004 kg/h**
- Buffer H₂ útil: **127.3 kg** (14.134 h)
- N₂: **42.02 kg/h** (~33.6 Nm³/h)
- NH₃: **50 kg/h** → **422.6 t/a** (modelo)
- Tanque NH₃: **15.9 t** (< umbral SEVESO 50 t)
- PEM: **538.796 kW**; parcela **3000.0 m²**

## Resumen CAPEX indicativo
- Líneas con precio de literatura + permisos 15 %: **3 090 306 EUR**
- + punto medio de pendientes: **4 122 806 EUR**
- Rango con pendientes: **3 625 306 – 4 620 306 EUR**
- Referencia CAPEX proceso v3 (sin pendientes BOP/obra/seguridad): **2 742 506 EUR**

## Lista de materiales y equipos

| ID | Ítem | Cant. | Ud. | Proveedor candidato | Precio total EUR | Estado | Fuente / fecha |
|---|---|---:|---|---|---:|---|---|
| eq_pem_01 | electrolizador_pem_containerizado | 538.8 | kW | Nel Hydrogen (MC Series; unidad comercia… | 1183196 | literatura_citada | European Hydrogen Observatory, Electrolyser cost 2025: PEM t… (2025) |
| eq_alk_alt | electrolizador_alcalino_alternativa | 538.8 | kW | Nel Hydrogen / Stiesdal (referencia de m… | 1118002 | literatura_citada | EHO 2025: alkaline total CAPEX 2075 EUR/kW (100 MWel)… (2025) |
| eq_buf_01 | buffer_h2_comprimido | 127.3 | kg_h2_util | Luxfer Gas Cylinders (G-Stor Pro Bundle)… | 110278 | literatura_citada | Haber-Bosch 2.0, Energy Environ. Sci. 2026 Tabla 2: 26 EUR/k… (2026) |
| eq_comp_01 | compresor_h2_booster | 1 | ud | Howden / PDC Machines / Maximator | PENDIENTE (80000–250000) | pendiente_verificacion | — |
| eq_psa_01 | generador_n2_psa | 1 | ud | CEZIUM CZ-N2M-50B / Parker Industrial Ga… | 183000 | literatura_citada | EES 2026 Tabla 2: ASU 1720 EUR/(kg N2/h) a 20 t/d, escalado … (2026) |
| eq_hb_01 | lazo_haber_bosch_modular | 1 | ud | Proton Ventures (NFUEL / Casale license)… | 1090000 | literatura_citada | EES 2026 Tabla 2: 8600 EUR/(kg NH3/h) a 20 t/d escalado exp … (2026) |
| eq_nh3_01 | tanque_nh3_presurizado | 15.9 | t_capacidad | Fabricantes EN 13445 / ASME (cotizar a t… | 44069 | literatura_citada | Rouwenhorst et al. 2021 Techno-Economic Challenges of Green … (2021) |
| eq_h2o_01 | tratamiento_agua_ro_edi | 1 | ud | Veolia / SUEZ / integrado en skid PEM (Nel MC incl | PENDIENTE (25000–80000) | pendiente_verificacion | — |
| eq_bop_01 | tuberias_valvulas_intercambiadores_instrumentacion | 1 | lote | Ingenieria EPC local + Emerson/Siemens/Endress+Hau | PENDIENTE (150000–400000) | pendiente_verificacion | — |
| eq_seg_01 | sistemas_seguridad_atex_deteccion_pci | 1 | lote | Organismo de control + instalador ATEX (p.ej. Appl | PENDIENTE (80000–200000) | pendiente_verificacion | — |
| eq_civ_01 | obra_civil_cimentaciones_cubetos_vallado | 3000.0 | m2_parcela | Constructora industrial local (El Prat / Zona Fran | PENDIENTE (200000–600000) | pendiente_verificacion | — |
| eq_elec_01 | conexion_mt_trafo_cuadros | 1 | lote | e-distribución (consulta punto de conexi… | 94792 | literatura_citada | Derechos extension+acceso CNMC 1-36 kV suelo urbanizado 32.7… (2013-2024) |
| eq_fv_opt | fv_cubierta_opcional_no_caso_base | 0 | kWp | Instaladores UNEF / fabricantes modulos… | — | literatura_citada | IRENA RPGC 2023 Espana utility 671 USD/kW + prima piloto; mo… (2023) |

## Detalle por línea
### eq_pem_01 — electrolizador_pem_containerizado
- Categoría: `electrolisis`
- Especificación: PEM containerizado ~0.54 MW, carga minima <=10 %, rampa <=10 %/s, H2 ~30 barg, pureza >=99.999 %, agua RO/EDI integrada preferible
- Proveedor candidato: Nel Hydrogen (MC Series; unidad comercial minima MC250 = 1.25 MW — sobredimensionado vs diseño 0.54 MW)
- URL: https://nelhydrogen.com/product/mc-series-pem/
- Precio unitario: 2196 EUR/kW
- Precio total: **1183196 EUR**
- Rango literatura: 1755 – 3000 EUR
- Fuente precio: European Hydrogen Observatory, Electrolyser cost 2025: PEM total CAPEX 2196 EUR/kW (stack 494 + BoP 567 + utilities 608 + other 527) para proyecto representativo 100 MWel
- Fecha fuente: 2025
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN cotización a escala 0.5-1 MW. Alternativas: H-TEC ME450 (1 MW) https://www.h-tec.com/en/products/detail/h-tec-pem-electrolyser-me450/me450 ; ITM Power https://itm-power.com/products/ ; Siemens Energy Silyzer https://www.siemens-energy.com/global/en/home/products-services/product-offerings/hydrogen-solutions.html. Pedidos Nel históricos ~1600-2080 USD/kW (2020-2021, no comparables 1:1). Modelo v3 usaba 2263 EUR/kW.

### eq_alk_alt — electrolizador_alcalino_alternativa
- Categoría: `electrolisis_alternativa`
- Especificación: Alcalino (alternativa a PEM): menor CAPEX, peor rampa; evaluar si RFNBO horario lo permite con buffer
- Proveedor candidato: Nel Hydrogen / Stiesdal (referencia de mercado ~500-2075 EUR/kW segun alcance)
- URL: https://observatory.clean-hydrogen.europa.eu/hydrogen-landscape/production-trade-and-cost/electrolyser-cost
- Precio unitario: 2075 EUR/kW
- Precio total: **1118002 EUR**
- Rango literatura: 500 – 2310 EUR
- Fuente precio: EHO 2025: alkaline total CAPEX 2075 EUR/kW (100 MWel)
- Fecha fuente: 2025
- Estado: **literatura_citada**
- Notas: NO incluido en CAPEX base (caso base = PEM). Stiesdal 6.5 MW ~500 EUR/kW sistema (prensa 2026) PENDIENTE DE VERIFICACIÓN alcance. Marca alternativa informativa.

### eq_buf_01 — buffer_h2_comprimido
- Categoría: `almacenamiento_h2`
- Especificación: Almacenamiento H2 ~127 kg utiles (~14.134 h a caudal nominal 9.0 kg/h), 200-450 bar tipico, packs de botellas o tubos
- Proveedor candidato: Luxfer Gas Cylinders (G-Stor Pro Bundle) / Hexagon Purus (X-STORE)
- URL: https://www.luxfercylinders.com/product/g-stor-pro-bundle/
- Precio unitario: 866.58 EUR/kg_h2_util
- Precio total: **110278 EUR**
- Rango literatura: 535 – 1000 EUR
- Fuente precio: Haber-Bosch 2.0, Energy Environ. Sci. 2026 Tabla 2: 26 EUR/kWh (=867 EUR/kg); ENTEC/Fraunhofer 2022 ~535 EUR/kg tanques
- Fecha fuente: 2026
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN cotización. Sin precio público EUR/kg en fichas Luxfer/Hexagon. Trailer 1000 kg ~450 EUR/kg payload citado en literatura FCH (referencia de orden).

### eq_comp_01 — compresor_h2_booster
- Categoría: `compresion`
- Especificación: Booster H2 desde ~30 barg (salida PEM tipica) hasta presion de buffer (200-450 bar), caudal ~9 kg/h, ATEX
- Proveedor candidato: Howden / PDC Machines / Maximator
- URL: https://www.howden.com/en-gb/products/compressors/hydrogen-compressors
- Rango literatura: 80000 – 250000 EUR
- Fuente precio: PENDIENTE DE VERIFICACIÓN
- Fecha fuente: —
- Estado: **pendiente_verificacion**
- Notas: PENDIENTE DE VERIFICACIÓN. Rango orden de magnitud para booster pequena escala (sin ficha de precio publica verificada 2026-11-04). Parte del BoP PEM puede incluir compresion hasta 30 bar; booster a buffer es adicional.

### eq_psa_01 — generador_n2_psa
- Categoría: `nitrogeno`
- Especificación: PSA N2 >=99.9 %, caudal >= 40.3 Nm3/h (margen 20 % sobre 33.6 Nm3/h = 42.0 kg/h), ~0.3-0.6 kWh/Nm3
- Proveedor candidato: CEZIUM CZ-N2M-50B / Parker Industrial Gas / Air Products PRISM
- URL: https://cezium.eu/en/produits/generators/nitrogen-psa/cz-n2m-50b/
- Precio unitario: 183000 EUR/ud
- Precio total: **183000 EUR**
- Rango literatura: 126000 – 222000 EUR
- Fuente precio: EES 2026 Tabla 2: ASU 1720 EUR/(kg N2/h) a 20 t/d, escalado exp 0.6-0.8 a 42 kg N2/h (base modelo v3)
- Fecha fuente: 2026
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN cotización industrial. WAVE N2-40 (40 Nm3/h 99.9 %) lista ~24900 EUR neto (https://www.wave.cc/de/product/wave-n2-40) pero pureza/servicio industrial y comisionado aparte — no usado como base por alcance distinto.

### eq_hb_01 — lazo_haber_bosch_modular
- Categoría: `sintesis_nh3`
- Especificación: Loop HB electrico modular 50 kg/h NH3 (1.2 t/d), carga minima ~20-40 %, rampa ~20 %/h, conversion global ~98 %, consumo ~0.6-3.6 kWh/kg NH3
- Proveedor candidato: Proton Ventures (NFUEL / Casale license) / Casale SMART-N / thyssenkrupp Uhde dynamic ammonia
- URL: https://protonventures.com/what-we-do/ammonia-production/
- Precio unitario: 1090000 EUR/ud
- Precio total: **1090000 EUR**
- Rango literatura: 750000 – 1900000 EUR
- Fuente precio: EES 2026 Tabla 2: 8600 EUR/(kg NH3/h) a 20 t/d escalado exp 0.6-0.8 a 50 kg/h; max Malmali et al. Processes 2018
- Fecha fuente: 2026
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN cotización. NFUEL brochure: capacidades tipicas 1000/4000/20000 t/a (piloto 423 t/a es sub-escala). Casale SkiGA 100 t/d Noruega (2026) sin CAPEX publicado. Stamicarbon NX STAMI: https://www.stamicarbon.com/

### eq_nh3_01 — tanque_nh3_presurizado
- Categoría: `almacenamiento_nh3`
- Especificación: Tanque NH3 anhidro presurizado ~16 t (~7 dias produccion), bajo umbral SEVESO 50 t (nivel inferior), conforme APQ-4
- Proveedor candidato: Fabricantes EN 13445 / ASME (cotizar a taller homologado ES); referencia tecnica Rouwenhorst 2021
- URL: https://www.boe.es/eli/es/rd/2017/06/23/656
- Precio unitario: 2772 EUR/t_capacidad
- Precio total: **44069 EUR**
- Rango literatura: 1848 – 3695 EUR
- Fuente precio: Rouwenhorst et al. 2021 Techno-Economic Challenges of Green Ammonia ~3000 USD/t presurizado pequena escala; cambio USD->EUR 1/1.0824
- Fecha fuente: 2021
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN cotización taller ES. SEVESO: NH3 50 t umbral inferior / 200 t superior (RD 840/2015 Anexo I).

### eq_h2o_01 — tratamiento_agua_ro_edi
- Categoría: `agua`
- Especificación: RO+EDI o equivalente para agua de electrolisis (~9-10 L/kg H2) + servicios; caudal pico ~0.1 m3/h
- Proveedor candidato: Veolia / SUEZ / integrado en skid PEM (Nel MC incluye RO/EDI)
- URL: https://nelhydrogen.com/product/mc-series-pem/
- Rango literatura: 25000 – 80000 EUR
- Fuente precio: PENDIENTE DE VERIFICACIÓN
- Fecha fuente: —
- Estado: **pendiente_verificacion**
- Notas: PENDIENTE DE VERIFICACIÓN. Si el skid PEM lo incluye (Nel MC), coste marginal bajo; si se compra aparte, rango de literatura pequena planta.

### eq_bop_01 — tuberias_valvulas_intercambiadores_instrumentacion
- Categoría: `bop_proceso`
- Especificación: Piping H2/N2/NH3, valvulas ATEX, HEX, instrumentacion (caudal, P, T, analitica H2/NH3), PLC/SCADA, cableado
- Proveedor candidato: Ingenieria EPC local + Emerson/Siemens/Endress+Hauser
- URL: https://www.siemens.com/global/en/products/automation.html
- Rango literatura: 150000 – 400000 EUR
- Fuente precio: PENDIENTE DE VERIFICACIÓN
- Fecha fuente: —
- Estado: **pendiente_verificacion**
- Notas: PENDIENTE DE VERIFICACIÓN. Parcialmente cubierto en 'other utilities' del EHO PEM y en CAPEX HB modular; evitar doble conteo al cotizar.

### eq_seg_01 — sistemas_seguridad_atex_deteccion_pci
- Categoría: `seguridad`
- Especificación: Clasificacion ATEX (RD 681/2003), detectores H2/NH3, ventilacion, alivio, PCI (extincion, hidrantes), EPIs, sirenas, paro de emergencia
- Proveedor candidato: Organismo de control + instalador ATEX (p.ej. Applus, SGS, Bureau Veritas como OCA)
- URL: https://www.boe.es/buscar/act.php?id=BOE-A-2003-11833
- Rango literatura: 80000 – 200000 EUR
- Fuente precio: PENDIENTE DE VERIFICACIÓN
- Fecha fuente: —
- Estado: **pendiente_verificacion**
- Notas: PENDIENTE DE VERIFICACIÓN. Incluye proyecto ATEX, certificado, equipos. RD 681/2003 ATEX lugares de trabajo.

### eq_civ_01 — obra_civil_cimentaciones_cubetos_vallado
- Categoría: `obra_civil`
- Especificación: Cimentaciones skids, cubetos APQ, drenajes, viales internos, vallado, caseta control ~3000 m2 parcela
- Proveedor candidato: Constructora industrial local (El Prat / Zona Franca)
- URL: https://www.elprat.cat/
- Rango literatura: 200000 – 600000 EUR
- Fuente precio: PENDIENTE DE VERIFICACIÓN
- Fecha fuente: —
- Estado: **pendiente_verificacion**
- Notas: PENDIENTE DE VERIFICACIÓN. Modelo v3 no desglosa obra civil aparte (parcial en permisos/ingenieria 15 % y en alquiler). Rango bruto piloto.

### eq_elec_01 — conexion_mt_trafo_cuadros
- Categoría: `electrica`
- Especificación: Punto conexion MT, ~655.0 kW contratados, linea 0.5 km, trafo, cuadros BT, protecciones
- Proveedor candidato: e-distribución (consulta punto de conexion) + instalador autorizado
- URL: https://www.edistribucion.com/
- Precio unitario: 94792 EUR/lote
- Precio total: **94792 EUR**
- Rango literatura: 50772 – 457412 EUR
- Fuente precio: Derechos extension+acceso CNMC 1-36 kV suelo urbanizado 32.7112 EUR/kW; linea MT subterranea simple CNMC 2013: 146733 EUR/km
- Fecha fuente: 2013-2024
- Estado: **literatura_citada**
- Notas: PENDIENTE DE VERIFICACIÓN pliego e-distribucion (tarea p7). Valores CNMC 2013 sin actualizar a EUR 2026.

### eq_fv_opt — fv_cubierta_opcional_no_caso_base
- Categoría: `fv_opcional`
- Especificación: FV in situ NO es el caso base (PPA). Si se elige cubierta: ~3.7 MWp escenario fv_cubierta_red_aux
- Proveedor candidato: Instaladores UNEF / fabricantes modulos
- URL: https://www.unef.es/
- Rango literatura: 620 – 1000 EUR
- Fuente precio: IRENA RPGC 2023 Espana utility 671 USD/kW + prima piloto; modelo 800 EUR/kWp
- Fecha fuente: 2023
- Estado: **literatura_citada**
- Notas: Excluido del CAPEX base PPA. Incluido solo como opcion.

## Formato LLP (resumen)
```json
{
  "meta": {
    "proyecto": "cero_a",
    "documento": "bom_piloto",
    "version": "ejecucion_2026-11-04",
    "fecha": "2026-11-04",
    "zona_horaria": "Europe/Madrid",
    "autoria": "Lázaro López Paz, El Prat de Llobregat, Barcelona, España; con asistencia de inteligencia artificial",
    "nivel_evidencia": "e2",
    "emplazamiento": {
      "nombre": "el_prat_de_llobregat",
      "lat": 41.3,
      "lon": 2.08
    },
    "escenario_base": "ppa_rfnbo_horario",
    "advertencia": "Precios de literatura o rangos; sin cotizaciones firmes. No constituye oferta comercial ni asesoramiento de compra."
  },
  "objetivo": "lista_materiales_equipos_piloto_50_kg_h_nh3_realizable_con_fuentes",
  "datos_clave": {
    "capex_total_indicativo_eur": {
      "solo_lineas_preciadas_mas_permisos": 3090306,
      "mas_punto_medio_pendientes": 4122806,
      "rango_bajo": 3625306,
      "rango_alto": 4620306,
      "modelo_v3_referencia": 2742506
    },
    "n_items": 13,
    "pendientes": 5
  },
  "tareas": [
    {
      "id": "bom1",
      "tarea": "solicitar cotizaciones PEM 0.5-1 MW, HB+PSA 1-2 t/d, buffer H2, tanque NH3",
      "estado": "pendiente"
    },
    {
      "id": "bom2",
      "tarea": "evitar doble conteo BoP al integrar ofertas skid",
      "estado": "pendiente"
    }
  ],
  "riesgos": [
    {
      "riesgo": "EHO 2196 EUR/kW es para 100 MW; piloto 0.5 MW puede ser 1.5-3x",
      "impacto": "alto",
      "mitigacion": "cotizar Nel/H-TEC/ITM"
    },
    {
      "riesgo": "HB modular a 50 kg/h casi no tiene referencia comercial publica",
      "impacto": "alto",
      "mitigacion": "Proton Ventures/Casale/Uhde"
    },
    {
      "riesgo": "doble conteo utilities PEM vs BOP aparte",
      "impacto": "medio",
      "mitigacion": "revisar alcance de cada oferta"
    }
  ],
  "decisiones": [
    {
      "decision": "caso_base_tecnologia_pem_no_alcalino",
      "estado": "provisional",
      "motivo": "mejor rampa para RFNBO horario"
    },
    {
      "decision": "caso_base_energia_ppa_no_fv_in_situ",
      "estado": "provisional",
      "motivo": "LCOA 3166 vs 4114-19129"
    }
  ],
  "proximo_paso": "lanzar p2 (cotizaciones equipos) y p1 (suelo) en paralelo; no enviar solicitudes sin aprobacion de Lazaro"
}
```