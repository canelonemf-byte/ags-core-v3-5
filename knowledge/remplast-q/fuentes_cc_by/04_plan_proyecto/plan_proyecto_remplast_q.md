# plan_proyecto_remplast_q (v1)

## meta
- proyecto: REMPLAST-Q
- usuario: Lázaro López Paz
- documento: plan_proyecto_remplast_q
- version: v1
- fecha: 2026-10-18
- idioma: es
- duracion_propuesta: 36 meses, del 1-9-2027 al 31-8-2030 (la AEI permite 3 o 4 años y no admite inicio antes del 1-9-2027)
- leyenda_verificacion: estado_verificacion: TC=cifra comprobada en texto completo; RES=solo resumen/abstract; SEC=fuente secundaria (reseña que cita a otro); COM=fuente comercial/proveedor; FRAG=fragmento de buscador o página no leída completa; OFI=texto oficial (EUR-Lex/BOE); EST=estimación propia justificada
- nota: los objetivos numéricos de KPI son propuestas (EST) basadas en la literatura citada, no resultados

## objetivo
- demostrar a escala piloto en una EDAR un tren terciario que reduzca MPs ≥20 µm en el efluente, midiendo con un método alineado con la Directiva (UE) 2024/3019 y la Decisión Delegada (UE) 2024/1441
- cuantificar eficiencia por etapa, transferencia al lodo y coste €/m3 para decidir el escalado
- comparar arena, arena+biochar y UF (referencia) y validar una ruta térmica de lodos

## datos_clave
- calendario_aei: AEI PGC 2026: 3–24 nov 2026 [aei2026] (OFI)
- metodo_ue: metodología de referencia: DD 2024/1441 (20 µm–5 mm, cascada 100/20 µm, blancos ≥10, spike 100±40 %) [dd2024_1441] (OFI)
- plazo_metodo_aguas_residuales: actos de ejecución de la Directiva 2024/3019 con metodología a más tardar el 2-7-2027 [uwwtd2024] (OFI)

## tren_recomendado
- e1_existente: pretratamiento + primario + secundario existentes: retienen 95–99 % acumulado (>125 µm) [sccwrp2024] (estado: base)
- e2_terciario_a: coagulación ligera en línea + filtración rápida en arena: 97 % en EDAR terciario, OPEX de tren 0,08–0,12 €/m3, bajo consumo (0,097 kWh/m3) [talvitie2017] [iglesias2017] [gcamejo2023] [zhao2024] (estado: recomendado)
- e2_terciario_b: variante: arena con capa de biochar: >95 % vs 60–80 % arena en laboratorio, sin datos a escala real ni de coste → objeto de innovación del proyecto [wang2020] [olubusoye2024] (estado: a_ensayar)
- e2_referencia_c: UF terciaria como referencia de máxima retención (99,3–100 % en ETAP) y para reutilización; mayor coste (0,18 €/m3 OPEX) [npj2025] [iglesias2017] (estado: referencia)
- e3_opcional_ec: electrocoagulación solo para corrientes concentradas (p. ej., lavanderías/industria): 92 % fibras; riesgo de fragmentación [senathirajah2023] [kim2026] (estado: opcional)
- e4_cuarta_etapa: si la EDAR necesita 4ª etapa: ozono antes de la filtración para que el filtro retenga fragmentos; ozono no se usa como barrera de MPs por fragmentación y resistencia de PVC/PTFE (hipótesis a verificar) [wieland2025] [topkaya2025] [vsa2024] (estado: condicional)
- e5_lodos: lodo: pirólisis ≥450–500 °C (MPs en biochar ~99,6–99,9 % menos) o monoincineración con recuperación de P, frente a uso agrícola directo [ni2020] [keller2024] [jrc2023sludge] (estado: recomendado)

## justificacion
- las separaciones físicas maduras (arena, membranas) son las únicas con datos a escala real de >95 % [talvitie2017][npj2025]
- la contraevidencia a largo plazo sobre MBR/CAP obliga a medir afluente y efluente del propio tren y no confiar en cifras de campañas cortas [sturm2025]
- degradación (POA, plasma, enzimas) sigue en TRL bajo para MPs en agua y no se incluye en el piloto [tournier2020][iervolino2026]
- la retención traslada MPs al lodo, por lo que el tren solo es completo con una ruta térmica de lodos [carnevale2024][ni2020]

## fases
| id | meses | actividades | hito | entregable | refs |
|---|---|---|---|---|---|
| f0_preparacion | M1–M3 | acuerdo con EDAR y laboratorio; diseño de piloto y puntos de muestreo; protocolo QA/QC y blancos de laboratorio | h0: protocolo aprobado y ≥10 blancos de procedimiento por tipo de filtro con LOD calculado | e0: protocolo de muestreo y análisis v1 | [dd2024_1441] |
| f1_linea_base | M3–M9 | campañas en afluente, efluentes primario/secundario, agua de lavado y lodos; variabilidad estacional | h1: línea base con eficiencia por etapa y clase de tamaño | e1: informe de línea base + base de datos | [uwwtd2024] |
| f2_banco | M6–M15 | jar-test de coagulación; columnas arena vs arena+biochar con MPs de referencia y agua real; EC en corriente concentrada (opcional) | h2: selección de 2 configuraciones para piloto | e2: informe de ensayos en banco | [wang2020]; [zhang2020] |
| f3_piloto | M12–M30 | operación en paralelo A (arena), B (arena+biochar), C (UF referencia); registro de energía, reactivos y lavados; pirólisis de lodo a 450/500/600 °C con socio | h3: ≥12 meses de operación con datos de eficiencia y coste | e3: informe de piloto y de lodos | [talvitie2017]; [ni2020] |
| f4_evaluacion | M27–M36 | análisis tecno-económico y ACV; plan de escalado; publicación y datos abiertos | h4: decisión go/no-go de escalado | e4: informe final, TEA/ACV, artículo | [vuori2022] |

## puntos_muestreo
| id | punto | matriz |
|---|---|---|
| p1 | afluente bruto tras desbaste | agua |
| p2 | efluente primario | agua |
| p3 | efluente secundario = entrada piloto | agua |
| p4 | efluente de cada línea piloto (A, B, C) | agua |
| p5 | agua de lavado de filtros / concentrado UF | agua |
| l1 | lodo primario | lodo |
| l2 | lodo secundario | lodo |
| l3 | lodo digerido/deshidratado | lodo |
| l4 | biochar de pirólisis / cenizas | solido |

## protocolo_muestreo_analisis
- muestreo_agua: filtración in situ en cascada 100 µm + 20 µm con registro de volumen; para agua potable la norma exige ≥1.000 L; en agua residual el volumen se fija en f0 según colmatación [dd2024_1441] (estado: OFI)
- gran_volumen: preferir filtración de gran volumen frente a muestra puntual; el proveedor indica que la puntual subestima 4,7× y que hacen falta ~21 muestras (vs 51 puntuales) para ±25 % al 95 % [wasser30] (estado: COM)
- frecuencia_legal: referencia legal: ≥2 muestras/año (≥150.000 h-e) o 1 cada 2 años (10.000–150.000 h-e); el proyecto muestrea con más frecuencia [uwwtd2024] (estado: OFI)
- rango_tamano: 20 µm–5 mm (fibras hasta 15 mm), clases 20–50, 50–100, 100–300, 300–1.000, 1.000–5.000 µm [dd2024_1441] (estado: OFI)
- identificacion: µFTIR o µRaman o QCL-IR capaces de ≤20 µm, biblioteca con PE, PP, PET, PS, PVC, PA, PU, PMMA, PTFE, PC; LDIR (QCL) para recuento rápido >20 µm; µRaman para subfracción <20 µm (hasta ~1 µm) [dd2024_1441] [xie2024] [iso16094_2] (estado: OFI)
- masa: Py-GC/MS para masa por polímero (complementa recuentos; detecta fragmentación); método ISO 16094-3 aún en elaboración [xie2024] [iso16094_3] (estado: RES)
- blancos: ≥10 blancos de procedimiento por tipo de filtro (100/20 µm); LOD = media + 3σ; filtros blanco en campo [dd2024_1441] (estado: OFI)
- recuperacion: spike de 50–150 partículas (120–200 µm y 30–70 µm, al menos PET y PE); aceptación 100 % ±40 % [dd2024_1441] (estado: OFI)
- submuestreo: ≥10 % del material / ≥20 % del área de filtro si no se analiza completo; líquidos filtrados ≤0,45 µm [dd2024_1441] (estado: OFI)
- lodos: extracción con digestión de la materia orgánica y separación por densidad con spike en cada lote; resultados en partículas/g MS y mg/kg MS [prus2024] (estado: RES)
- expresion: partículas/m3 por clase de tamaño y polímero; eliminación por etapa con afluente y efluente de la misma campaña [dd2024_1441] [sturm2025] (estado: OFI)
- control_contaminacion: material no plástico, bata de algodón, campana/flujo laminar, filtros blanco abiertos durante la manipulación [dd2024_1441] (estado: EST)
- actualizacion: adaptar al acto de ejecución de la Directiva 2024/3019 cuando se publique (plazo 2-7-2027) [uwwtd2024] (estado: OFI)

## kpis
- k1: eliminación del tren terciario para MPs ≥20 µm (por clase de tamaño) [talvitie2017] (estado: EST) | refs_obj: ≥95 % (referencia: 97 % arena)
- k2: recuperación de spike [dd2024_1441] (estado: OFI) | refs_obj: 60–140 % (100 ±40 %)
- k3: muestras por encima del LOD (μ+3σ de blancos) [dd2024_1441] (estado: OFI) | refs_obj: 100 % de resultados notificados con LOD
- k4: OPEX del tren seleccionado [iglesias2017] (estado: EST) | refs_obj: ≤0,12 €/m3 (referencia tren de filtración)
- k5: energía del tren seleccionado [gcamejo2023] (estado: EST) | refs_obj: ≤0,1 kWh/m3 (referencia filtración por gravedad)
- k6: reducción de MPs en lodo tras tratamiento térmico [ni2020] (estado: EST) | refs_obj: ≥99 % de partículas (referencia pirólisis 500 °C)
- k7: balance de masas agua + lodo  (estado: EST) | refs_obj: cierre a acordar en f0
- k8: hitos h0–h4 en plazo  (estado: EST) | refs_obj: 100 %

## riesgos
- r1_acceso_edar: sin EDAR socia no hay piloto  | mitigacion: carta de apoyo antes de solicitar financiación; EDAR alternativa
- r2_colmatacion_muestreo: filtros 20 µm se colmatan en agua residual [dd2024_1441] | mitigacion: ensayos de volumen en f0; prefiltro 100 µm; registro de volumen
- r3_contaminacion: falsos positivos por fibras ambientales [dd2024_1441] | mitigacion: blancos ≥10 por tipo, LOD μ+3σ, control de laboratorio
- r4_comparabilidad: resultados no comparables con literatura [dd2024_1441] [npj2025] | mitigacion: clases de tamaño y polímeros de la DD 2024/1441; publicar método
- r5_capacidad_analitica: coste y tiempo de µFTIR/Raman limitan nº de muestras [xie2024] | mitigacion: LDIR para cribado y µFTIR/Raman en submuestra; laboratorio externo
- r6_fragmentacion: coagulación/EC/ozono generan fragmentos <20 µm no contados [senathirajah2023] [wieland2025] | mitigacion: Py-GC/MS (masa) y µRaman en submuestras
- r7_cambio_metodo_ue: el acto de ejecución de 2027 puede cambiar el método [uwwtd2024] | mitigacion: conservar filtros y espectros; protocolo versionado
- r8_biochar: desprendimiento de finos o pérdida de eficacia del biochar [wang2020] | mitigacion: medir finos/turbidez en efluente B; lavado y reposición
- r9_financiacion: denegación o retraso de la convocatoria  | mitigacion: presentar a dos convocatorias compatibles (AEI y CDTI/LIFE) sin doble financiación

## presupuesto
- nota: importes "" donde no hay dato con fuente; completar con ofertas reales. Referencias de escala abajo
| id | concepto | importe_eur | base | fuente |
|---|---|---|---|---|
| personal | investigador/a + técnico/a de laboratorio | "" | tablas salariales de la entidad | "" |
| analitica | análisis µFTIR/LDIR/Raman y Py-GC/MS (nº de muestras × €/muestra) | "" | ofertas de laboratorio; nº de muestras según dp5 y protocolo | "" |
| piloto | columnas de arena/arena+biochar, módulo UF, bombas, instrumentación | "" | ofertas de proveedores (CAPEX de planta real no aplica a piloto) | "" |
| energia_piloto | energía de la línea de filtración | "" | ≈850 kWh/año para 1 m3/h a 0,097 kWh/m3 (EST) × precio eléctrico de la EDAR | [gcamejo2023] |
| lodos_pirolisis | servicio de pirólisis y caracterización de biochar | "" | oferta de socio tecnológico | "" |
| consumibles | filtros, reactivos, patrones de MPs para spike | "" | ofertas | "" |
| difusion | publicación en abierto, congresos | "" | tarifas APC de la revista elegida | "" |
- cdti_minimo: CDTI Proyectos de I+D: presupuesto mínimo 175.000 € por empresa [cdti_pid] (FRAG)
- life_cofin: LIFE SAP: cofinanciación máxima 60 % [life2026] [life_sap] (FRAG)

## financiacion
| id | programa | plazo | dotacion | beneficiarios | encaje | enlace | estado_verificacion |
|---|---|---|---|---|---|---|---|
| aei_pgc_2026 | AEI Proyectos de Generación de Conocimiento 2026 | solicitudes 3–24 nov 2026, 14:00 hora peninsular (Europe/Madrid) | 724 M€ (total convocatoria) | organismos públicos de investigación, universidades y centros tecnológicos (ver requisitos en la convocatoria) | alto si el solicitante es universidad/OPI; fases f0–f4 | https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-31900 https://www.ciencia.gob.es/Convocatorias/2026/PID2026.html | OFI |
| cdti_pid | CDTI Proyectos de I+D | convocatoria abierta todo el año (verificar en CDTI) | "" | empresas | alto si lidera una empresa (tecnología de filtración/biochar) | https://www.cdti.es/sites/default/files/2026-02/1._proyectos_de_id_2026_02.pdf | FRAG |
| life_sap_env | LIFE Circular Economy and Quality of Life (LIFE-2026-SAP-ENV) | 2026 cerrada (22 sep 2026); próxima convocatoria 2027, fecha "" | "" | entidades públicas y privadas de la UE | alto para demostración piloto en EDAR | https://cinea.ec.europa.eu/life-calls-proposals-2026_en https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/life/wp-call/2026/call-fiche_life-2026-sap-env_en.pdf | FRAG |
| horizon_cl6_zeropollution | Horizon Europe Cluster 6 – HORIZON-CL6-2026-01-ZEROPOLLUTION-01-two-stage (Decontaminate and bioremediate aquatic pollution) | primera etapa probablemente cerrada (16-04-2026 según página no oficial); revisar temas 2027 en el programa de trabajo | "" | consorcios internacionales | medio-alto (micro/nanoplásticos en agua residual y potable) | https://cordis.europa.eu/programme/id/HORIZON_HORIZON-CL6-2026-01-ZEROPOLLUTION-01-two-stage https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-9-food-bioeconomy-natural-resources-agriculture-and-environment_horizon-2026-2027_en.pdf | FRAG |

## tareas
- t1: obtener carta de apoyo de la EDAR (dp1)  (estado: pendiente)
- t2: pedir ofertas de análisis y de equipos piloto para cerrar presupuesto  (estado: pendiente)
- t3: comprobar requisitos y plazo de la convocatoria elegida en la web oficial [aei2026web] (estado: pendiente)
- t4: redactar memoria técnica a partir de este plan  (estado: pendiente)

## decisiones
- dp1: EDAR objetivo (nombre, h-e, caudal) y si existe 4ª etapa prevista  (estado: pendiente_usuario)
- dp2: RESUELTA: AEI Proyectos de Generación de Conocimiento 2026 solicitada por universidad u organismo público (3–24-11-2026); requiere IP doctor/a vinculado/a; ver 05_solicitud_aei [aei_conv2026] (estado: resuelta_usuario)
- dp3: líneas piloto: A arena (+coagulación), B arena+biochar, C UF referencia; ¿EC opcional?  (estado: pendiente_usuario)
- dp4: incluir línea de lodos (pirólisis) o dejarla fuera (24 meses)  (estado: pendiente_usuario)
- dp5: tamaño mínimo: 20 µm (método UE, µFTIR/LDIR) o bajar a 1–10 µm con µRaman (más caro y lento) [dd2024_1441] [xie2024] (estado: pendiente_usuario)
- dp6: laboratorio analítico propio o externo y técnicas disponibles  (estado: pendiente_usuario)
- dp7: presupuesto máximo y duración  (estado: pendiente_usuario)

## proximo_paso
- conseguir IP vinculado/a antes del 30-10-2026 y completar 05_solicitud_aei para presentar entre el 3 y el 24-11-2026 (14:00 Europe/Madrid)

## referencias
- [aei2026] BOE-B-2026-31900. Extracto convocatoria 2026 Proyectos de Generación de Conocimiento (AEI). https://www.boe.es/diario_boe/txt.php?id=BOE-B-2026-31900
- [aei2026web] Ministerio de Ciencia: Proyectos de Generación de Conocimiento 2026. https://www.ciencia.gob.es/Convocatorias/2026/PID2026.html
- [aei_conv2026] AEI (2026). Resolución de 30-09-2026 de la Presidencia de la AEI por la que se aprueba la convocatoria de tramitación anticipada para el año 2026 de ayudas a «Proyectos de Generación de Conocimiento» y actuaciones para formación de personal investigador predoctoral (texto completo firmado, CSV GEN-bdee-fb5c-cbfb-ddaa-67eb-2c3c-e925-db73). https://www.aei.gob.es/sites/default/files/convocatory_info/file/2026-10/Convocatoria_ProyectosGeneraci%C3%B3nConocimiento_Predoc_2026_fda.pdf
- [carnevale2024] Carnevale Miino M, Galafassi S, Zullo R, Torretta V, Rada EC (2024). Microplastics removal in wastewater treatment plants: A review of the different approaches to limit their release in the environment. Sci. Total Environ. 930:172675. https://doi.org/10.1016/j.scitotenv.2024.172675
- [cdti_pid] CDTI. Proyectos de I+D (ficha 2026). https://www.cdti.es/sites/default/files/2026-02/1._proyectos_de_id_2026_02.pdf
- [cl6_2026] CORDIS. HORIZON-CL6-2026-01-ZEROPOLLUTION-01-two-stage: Decontaminate and bioremediate aquatic pollution. https://cordis.europa.eu/programme/id/HORIZON_HORIZON-CL6-2026-01-ZEROPOLLUTION-01-two-stage
- [dd2024_1441] Decisión Delegada (UE) 2024/1441 de la Comisión, metodología para medir microplásticos en agua destinada al consumo humano (DO L 21-05-2024). https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024D1441
- [gcamejo2023] González-Camejo J, et al. (2023). Feasibility of Rapid Gravity Filtration and Membrane Ultrafiltration for the Removal of Microplastics and Microlitter in Sewage and Wastewater from Plastic Industry. J. Water Process Eng. 51:103452. https://doi.org/10.1016/j.jwpe.2022.103452
- [iervolino2026] Iervolino (2026). Non-thermal DBD plasma for the degradation of microplastics suspended in water: evidence from CO2 quantification. Chem. Eng. J. 528:172474. https://doi.org/10.1016/j.cej.2025.172474
- [iglesias2017] Iglesias R, Simón P, Moragas L, Arce A, Rodriguez-Roda I (2017). Cost comparison of full-scale water reclamation technologies with an emphasis on membrane bioreactors. Water Sci. Technol. 75(11):2562–2570. https://doi.org/10.2166/wst.2017.132
- [iso16094_2] ISO 16094-2:2025 Water quality — Analysis of microplastic in water — Part 2: Vibrational spectroscopy methods for waters with low content of suspended solids including drinking water. https://www.iso.org/standard/84460.html
- [iso16094_3] ISO/FDIS 16094-3 Water quality — Analysis of microplastic in water — Part 3: Thermo-analytical methods (en elaboración). https://www.iso.org/standard/84463.html
- [jrc2023sludge] JRC (2023). Feasibility study in support of future policy developments of the Sewage Sludge Directive (86/278/EEC). JRC134591. https://publications.jrc.ec.europa.eu/repository/bitstream/JRC134591/JRC134591_01.pdf
- [keller2024] Keller AA, et al. (2024). Elimination of microplastics, PFAS, and PPCPs from biosolids via pyrolysis to produce biochar: Feasibility and techno-economic analysis. Sci. Total Environ. 947:174773. https://doi.org/10.1016/j.scitotenv.2024.174773
- [kim2026] Kim (2026). Parametric study on electro-coagulation for efficient removal of microplastics from reverse osmosis wastewater. Water Sci. Technol. 93:903–915. https://doi.org/10.2166/wst.2026.239
- [life2026] CINEA. LIFE Calls for proposals 2026. https://cinea.ec.europa.eu/life-calls-proposals-2026_en
- [life_sap] Call fiche LIFE-2026-SAP-ENV (Circular Economy and Quality of Life). https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/life/wp-call/2026/call-fiche_life-2026-sap-env_en.pdf
- [ni2020] Ni BJ, Zhu ZR, Li W, et al. (2020). Microplastics Mitigation in Sewage Sludge through Pyrolysis: The Role of Pyrolysis Temperature. Environ. Sci. Technol. Lett. 7:961–967. https://doi.org/10.1021/acs.estlett.0c00740
- [npj2025] Balkenbusch F, et al. (2025). Microplastic removal across ten drinking water treatment facilities and distribution systems. npj Clean Water 8:103. https://doi.org/10.1038/s41545-025-00531-w
- [olubusoye2024] Olubusoye BS, et al. (2024). Removal of microplastics from agricultural runoff using biochar: a column feasibility study. Front. Environ. Sci. 12:1388606. https://doi.org/10.3389/fenvs.2024.1388606
- [prus2024] Prus (2024). Microplastics in Sewage Sludge: Worldwide Presence in Biosolids ... Including the Hydrothermal Carbonization Process. Energies 17:4219. https://doi.org/10.3390/en17174219
- [sccwrp2024] SCCWRP (2024). Characterizing the Removal of Microplastics by California Wastewater Treatment Plants: Implications for Management Strategies. Technical Report 1378. https://ftp.sccwrp.org/pub/download/DOCUMENTS/TechnicalReports/1378_MicroplasticsWastewaterPlants.pdf
- [senathirajah2023] Senathirajah K, et al. (2023). Fate and transformation of microplastics due to electrocoagulation treatment: Impacts of polymer type and shape. Environ. Pollut. 334:122159. https://doi.org/10.1016/j.envpol.2023.122159
- [sturm2025] Sturm MT, Argyropoulou D, Myers E, et al. (2025). Comparative Long-Term Monitoring of Microplastics in the Effluent of Three Different WWTPs with Two, Three, and Four Treatment Stages. Water 17(5):711. https://doi.org/10.3390/w17050711
- [talvitie2017] Talvitie J, Mikola A, Koistinen A, Setälä O (2017). Solutions to microplastic pollution – Removal of microplastics from wastewater effluent with advanced wastewater treatment technologies. Water Research 123:401–407. https://doi.org/10.1016/j.watres.2017.07.005
- [topkaya2025] Topkaya E, Arslan A, Veli S, Kuru S, Sezer M (2025). Removal of Microplastics by Ozone Oxidation from Urban Wastewater Using Taguchi Experimental Design. Water Air Soil Pollut. 236:606. https://doi.org/10.1007/s11270-025-08249-8
- [tournier2020] Tournier V, Topham CM, Gilles A, et al. (2020). An engineered PET depolymerase to break down and recycle plastic bottles. Nature 580:216–219. https://doi.org/10.1038/s41586-020-2149-4
- [uwwtd2024] Directiva (UE) 2024/3019 sobre tratamiento de aguas residuales urbanas (refundición), texto consolidado 12-12-2024. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02024L3019-20241212
- [vsa2024] Hunziker Betatech AG para VSA (2024). Evaluation of the energy and cost figures of processes for the elimination of micropollutants in WWTPs. Informe técnico 1490.26 (28-09-2024). https://micropoll.ch/wp-content/uploads/2025/03/Energy-and-cost-key-figures-MP-treatment.pdf
- [vuori2022] Vuori L, Ollikainen M (2022). How to remove microplastics in wastewater? A cost-effectiveness analysis. Ecological Economics 192:107246. https://doi.org/10.1016/j.ecolecon.2021.107246
- [wang2020] Wang Z, Sedighi M, Lea-Langton A (2020). Filtration of microplastic spheres by biochar: removal efficiency and immobilisation mechanisms. Water Research 184:116165. https://doi.org/10.1016/j.watres.2020.116165
- [wasser30] Wasser 3.0 gGmbH. Microplastic monitoring for municipal WWTPs (página técnica, revisada ago-2026). https://wasserdreinull.de/en/offers-and-services/wastewater-treatment/
- [wieland2025] Wieland (2025). Ozone-mediated breakdown of microplastics in aqueous environments. J. Anal. At. Spectrom. 40:2870–2878. https://doi.org/10.1039/d5ja00226e
- [wp_cl6] Horizon Europe Work Programme 2026-2027, Cluster 6. https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/wp-call/2026-2027/wp-9-food-bioeconomy-natural-resources-agriculture-and-environment_horizon-2026-2027_en.pdf
- [xie2024] Xie (2024). Analysing micro- and nanoplastics with cutting-edge infrared spectroscopy techniques: a critical review. Anal. Methods 16:2177–2197. https://doi.org/10.1039/D3AY01808C
- [zhang2020] Zhang Y, Diehl A, Lewandowski A, Gopalakrishnan K, Baker T (2020). Removal efficiency of micro- and nanoplastics (180 nm–125 μm) during drinking water treatment. Sci. Total Environ. 720:137383. https://doi.org/10.1016/j.scitotenv.2020.137383
- [zhao2024] Zhao (2024). Research on Effect of Microplastics Removal through Combination of Coagulation and Sand Filtration. E3S Web Conf. 598:01005. https://doi.org/10.1051/e3sconf/202459801005
