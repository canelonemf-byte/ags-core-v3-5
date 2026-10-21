# comparativa_costes (v1)

## meta
- proyecto: REMPLAST-Q
- usuario: Lázaro López Paz
- documento: comparativa_costes_tecnologias_microplasticos
- version: v1
- fecha: 2026-10-18
- idioma: es
- leyenda_verificacion: estado_verificacion: TC=cifra comprobada en texto completo; RES=solo resumen/abstract; SEC=fuente secundaria (reseña que cita a otro); COM=fuente comercial/proveedor; FRAG=fragmento de buscador o página no leída completa; OFI=texto oficial (EUR-Lex/BOE); EST=estimación propia justificada
- regla: sin cifras inventadas: "" = sin dato localizado; las monedas y años se mantienen como en la fuente (sin conversión ni actualización por inflación)
- aviso: casi ningún coste es específico de MPs: son costes generales de la tecnología (campo especifico_mps)

## objetivo
- comparar CAPEX/OPEX/energía de las tecnologías candidatas para la barrera de MPs
- señalar qué cifra es específica de MPs, general de la tecnología o comercial

## datos_clave
- opex_menor: entre los procesos con fuente revisada por pares o informe técnico, los OPEX más bajos por m3 son filtración en profundidad (0,08–0,12 €/m3 para tren completo) y 4ª etapa (0,02–0,09 CHF/m3 de explotación); MBR y UF terciaria son más caros (0,18–0,45 €/m3) [iglesias2017] [vsa2024] (SEC)
- energia: energía: filtración por gravedad 0,097 < UF 0,156 << MBR 0,6–1,2 kWh/m3 [gcamejo2023] [iglesias2017] (FRAG)
- coste_eficacia: el análisis coste-eficacia finlandés sitúa MBR + incineración de fango como la opción más coste-efectiva [vuori2022] (RES)
- hueco: no hay costes publicados de filtros de arena con biochar ni de DAF terciario para MPs ("")  (EST)

## tabla_costes_agua
| id | tecnologia | capex | opex | energia | eficiencia_mps | especifico_mps | contexto | verificacion | fuentes |
|---|---|---|---|---|---|---|---|---|---|
| filtro_arena_rapido | Filtración rápida en arena (dentro de tren CRT: coagulación + lamelas + filtración en profundidad + desinfección) | ~115 €/(m3·d) a 5.000–10.000 m3/d; ~100 €/(m3·d) a 20.000 m3/d | 0,08–0,12 €/m3 | 0,097 kWh/m3 (filtración rápida por gravedad) | 97 % (EDAR terciario) [talvitie2017] | no (coste general de regeneración) | EDAR españolas, € de 2011 | CAPEX/OPEX CRT [iglesias2017] SEC; 0,097 kWh/m3 [gcamejo2023] FRAG | [iglesias2017]; [gcamejo2023]; [talvitie2017] |
| filtro_arena_biochar | Filtro de arena con capa/enmienda de biochar | "" | "" | "" | >95 % vs 60–80 % arena (laboratorio) [wang2020] | "" | sin datos de coste publicados localizados; el coste incremental sería el del medio filtrante y su reposición | "" | [wang2020]; [li2024] |
| daf | Flotación por aire disuelto | "" | "" | 1,5–2 kWh/m3 | 95 % [talvitie2017] | no | valor de proveedor | 1,5–2 kWh/m3 [daf_vendor] COM | [daf_vendor]; [talvitie2017] |
| mbr | Biorreactor de membrana (sustituye secundario) | 700–960 €/(m3·d) (8.000–15.000 m3/d); 2.000–3.200 €/(m3·d) a 1.000–2.000 m3/d; hasta 625 €/(m3·d) y 94 €/h-e >10.000 m3/d | 0,2–0,45 €/m3 (reposición de membranas 0,02–0,04 €/m3); total comparado 0,32 €/m3 | 0,6–1,2 kWh/m3 (0,8–1,2 en comparativa de trenes) | 99,9 % en campaña corta [talvitie2017]; sin diferencia significativa a largo plazo [sturm2025] | no | EDAR españolas, € de 2011; comparado con fangos activos 0,4–0,8 kWh/m3 | CAPEX/OPEX/energía MBR [iglesias2017] SEC; MBR + incineración más coste-efectivo [vuori2022] RES | [iglesias2017]; [talvitie2017]; [sturm2025]; [vuori2022] |
| uf_terciaria | Ultrafiltración terciaria (tren ART) | ~430 €/(m3·d) | 0,18 €/m3 (terciario); total con secundario 0,40 €/m3 | 0,156 kWh/m3 (UF) | UF 99,3–100 % en ETAP [npj2025] | no | EDAR españolas, € de 2011 | 430 €/(m3·d); 0,18 €/m3 [iglesias2017] SEC; 0,156 kWh/m3 [gcamejo2023] FRAG | [iglesias2017]; [gcamejo2023]; [npj2025] |
| filtro_discos | Filtro de discos/tela | "" | 0,010–0,045 €/m3 | 0,008–0,020 kWh/m3 | 40–98,5 % [talvitie2017] | no | valor de proveedor | OPEX y energía [cloth_vendor] COM | [cloth_vendor]; [talvitie2017] |
| electrocoagulacion | Electrocoagulación | "" | 0,0667 US$/m3 | 0,167 kWh/m3 (3 mA/cm2) | 95 % (laboratorio, agua de rechazo de OI) [kim2026] | sí (laboratorio) | laboratorio; no extrapolable a escala real | 0,0667 US$/m3; 0,167 kWh/m3 [kim2026] RES | [kim2026] |
| ozono_4a_etapa | Ozonización (4ª etapa micro-contaminantes) | inversión 20–300 CHF/h-e (rango de procesos de 4ª etapa) | explotación 0,02–0,09 CHF/m3; anual con capital 0,07–0,27 CHF/m3; ozono observado 0,07–0,15 CHF/m3 (plantas grandes) y 0,15–0,22 CHF/m3 (pequeñas) | "" | 83 % laboratorio [topkaya2025]; riesgo de fragmentación | no (coste de micro-contaminantes en Suiza); 0,094 €/m3 específico de MPs pero de laboratorio y solo energía [topkaya2025] | EDAR suizas en servicio (2024) | cifras VSA [vsa2024] TC; 0,094 €/m3 [topkaya2025] TC | [vsa2024]; [topkaya2025] |
| cap_4a_etapa | Carbón activo en polvo (CAP) 4ª etapa | incluido en 20–300 CHF/h-e | CAP observado 0,09–0,16 CHF/m3 (grandes) y 0,10–0,26 CHF/m3 (pequeñas) | "" | sin diferencia significativa del efluente con CAP vs convencional [sturm2025] | no | EDAR suizas en servicio (2024) | cifras VSA [vsa2024] TC | [vsa2024]; [sturm2025] |
| cuarta_etapa_ue | 4ª etapa a escala UE (agregado) | "" | 1.480–1.800 M€/año en 2045 (UE, todas las plantas obligadas) | "" | no aplica | no | estimación JRC para la Directiva 2024/3019 | 1,48–1,8 mil M€/año [jrc2025quat] TC | [jrc2025quat] |

## tabla_costes_lodos
| id | coste | estado | fuentes |
|---|---|---|---|
| aplicacion_agricola | 15–20 €/t húmeda | SEC | [iglesias2017] |
| compostaje | 30–35 €/t húmeda | SEC | [iglesias2017] |
| secado_termico | 40–60 €/t húmeda | SEC | [iglesias2017] |
| monoincineracion | ~350 €/t MS (160–510) | TC | [jrc2023sludge] |
| pirolisis | "" | RES | [keller2024] |

## estimacion_ejemplo
- piloto de filtración por gravedad a 1 m3/h durante 12 meses (supuesto propio): 8.760 m3 × 0,097 kWh/m3 ≈ 850 kWh/año [gcamejo2023] (EST; ejemplo de cómo dimensionar; el precio de la electricidad debe darlo la EDAR)

## tareas
- t1: pedir a la EDAR piloto costes reales de energía, reactivos y gestión de lodos  (estado: pendiente)
- t2: pedir oferta a proveedores de biochar y de filtros (discos, DAF) para el piloto  (estado: pendiente)
- t3: convertir monedas y actualizar a € actuales con índice oficial (IPC/IPRI) cuando se use en presupuesto  (estado: pendiente)

## riesgos
- r1_no_especifico: los costes son de la tecnología, no de eliminar MPs; el coste por MP eliminado no se puede calcular sin datos propios [iglesias2017]
- r2_antiguedad: costes españoles en € de 2011 [iglesias2017]
- r3_comercial: DAF y discos solo con fuente de proveedor [daf_vendor] [cloth_vendor]

## decisiones
- d1: ¿qué caudal de diseño usar para escalar costes (tamaño de la EDAR objetivo)?  (estado: pendiente_usuario)

## proximo_paso
- con el caudal de la EDAR objetivo, recalcular CAPEX/OPEX de las 3 opciones del plan con ofertas reales

## referencias
- [cloth_vendor] Filter Systems. Wastewater Treatment OPEX: Cost Benchmark per m³ (web comercial). https://filter-systems.com/en/knowledge/operating-cost-per-cubic-metre-the-items-that-actually-move-the-number
- [daf_vendor] Sigma DAF Clarifiers. Preguntas frecuentes DAF (web comercial). https://sigmadafclarifiers.com/en/sistemas-daf/preguntas-frecuentes-daf/
- [gcamejo2023] González-Camejo J, et al. (2023). Feasibility of Rapid Gravity Filtration and Membrane Ultrafiltration for the Removal of Microplastics and Microlitter in Sewage and Wastewater from Plastic Industry. J. Water Process Eng. 51:103452. https://doi.org/10.1016/j.jwpe.2022.103452
- [iglesias2017] Iglesias R, Simón P, Moragas L, Arce A, Rodriguez-Roda I (2017). Cost comparison of full-scale water reclamation technologies with an emphasis on membrane bioreactors. Water Sci. Technol. 75(11):2562–2570. https://doi.org/10.2166/wst.2017.132
- [jrc2023sludge] JRC (2023). Feasibility study in support of future policy developments of the Sewage Sludge Directive (86/278/EEC). JRC134591. https://publications.jrc.ec.europa.eu/repository/bitstream/JRC134591/JRC134591_01.pdf
- [jrc2025quat] Pistocchi A (2025). Updated estimation of the costs of quaternary wastewater treatment in the EU. JRC144745, EUR 40579. https://data.europa.eu/doi/10.2760/6476421
- [keller2024] Keller AA, et al. (2024). Elimination of microplastics, PFAS, and PPCPs from biosolids via pyrolysis to produce biochar: Feasibility and techno-economic analysis. Sci. Total Environ. 947:174773. https://doi.org/10.1016/j.scitotenv.2024.174773
- [kim2026] Kim (2026). Parametric study on electro-coagulation for efficient removal of microplastics from reverse osmosis wastewater. Water Sci. Technol. 93:903–915. https://doi.org/10.2166/wst.2026.239
- [li2024] Li (2024). The Removal and Mitigation Effects of Biochar on Microplastics in Water and Soils. Sustainability 16:9749. https://doi.org/10.3390/su16229749
- [npj2025] Balkenbusch F, et al. (2025). Microplastic removal across ten drinking water treatment facilities and distribution systems. npj Clean Water 8:103. https://doi.org/10.1038/s41545-025-00531-w
- [sturm2025] Sturm MT, Argyropoulou D, Myers E, et al. (2025). Comparative Long-Term Monitoring of Microplastics in the Effluent of Three Different WWTPs with Two, Three, and Four Treatment Stages. Water 17(5):711. https://doi.org/10.3390/w17050711
- [talvitie2017] Talvitie J, Mikola A, Koistinen A, Setälä O (2017). Solutions to microplastic pollution – Removal of microplastics from wastewater effluent with advanced wastewater treatment technologies. Water Research 123:401–407. https://doi.org/10.1016/j.watres.2017.07.005
- [topkaya2025] Topkaya E, Arslan A, Veli S, Kuru S, Sezer M (2025). Removal of Microplastics by Ozone Oxidation from Urban Wastewater Using Taguchi Experimental Design. Water Air Soil Pollut. 236:606. https://doi.org/10.1007/s11270-025-08249-8
- [vsa2024] Hunziker Betatech AG para VSA (2024). Evaluation of the energy and cost figures of processes for the elimination of micropollutants in WWTPs. Informe técnico 1490.26 (28-09-2024). https://micropoll.ch/wp-content/uploads/2025/03/Energy-and-cost-key-figures-MP-treatment.pdf
- [vuori2022] Vuori L, Ollikainen M (2022). How to remove microplastics in wastewater? A cost-effectiveness analysis. Ecological Economics 192:107246. https://doi.org/10.1016/j.ecolecon.2021.107246
- [wang2020] Wang Z, Sedighi M, Lea-Langton A (2020). Filtration of microplastic spheres by biochar: removal efficiency and immobilisation mechanisms. Water Research 184:116165. https://doi.org/10.1016/j.watres.2020.116165
