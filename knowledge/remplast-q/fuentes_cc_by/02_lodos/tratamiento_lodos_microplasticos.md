# tratamiento_lodos_microplasticos (v1)

## meta
- proyecto: REMPLAST-Q
- usuario: Lázaro López Paz
- documento: tratamiento_lodos_biosolidos_microplasticos
- version: v1
- fecha: 2026-10-18
- idioma: es
- alcance: lodo_edar, biosolidos, aplicacion_agricola, normativa_ue_es
- metodo: artículos revisados por pares (metadatos en Crossref), informes JRC/Comisión y textos legales EUR-Lex/BOE
- leyenda_verificacion: estado_verificacion: TC=cifra comprobada en texto completo; RES=solo resumen/abstract; SEC=fuente secundaria (reseña que cita a otro); COM=fuente comercial/proveedor; FRAG=fragmento de buscador o página no leída completa; OFI=texto oficial (EUR-Lex/BOE); EST=estimación propia justificada
- nota: eliminación medida por recuento de partículas salvo indicación; recuento puede subir por fragmentación aunque baje la masa

## objetivo
- evaluar qué tratamientos de lodo reducen o destruyen MPs y con qué evidencia
- resumir el marco normativo UE/España para lodos y su uso agrícola
- proponer la ruta de lodos para REMPLAST-Q

## datos_clave
- sumidero: potencialmente >65 % de los MPs que entran en la EDAR acaban en el lodo [carnevale2024] (RES)
- concentracion_biosolidos: biosólidos de 7 EDAR de California: 3–52 partículas/g [sccwrp2024] (TC)
- aporte_suelo_europa: 63.000–430.000 t/año de MPs a suelos agrícolas europeos (estimación) [nizzetto2016] (RES)
- aporte_suelo_1_5mm: 31.000–42.000 t/año de MPs de 1–5 mm a suelos agrícolas europeos vía lodo (hasta 4,8 g/m2/año) [lofty2022] (RES)
- digestion_anaerobia: digestión mesofílica a escala real (790.000 h-e): ~30 % de reducción de carga (7.326→4.885 kg/año) dentro de la variabilidad del muestreo, no confirmada [chand2021] (RES)
- pirolisis: pirólisis a 500 °C: 550,8–960,9 → 1,4–2,3 partículas/g; PE/PP degradados por completo ≥450 °C [ni2020] (RES)
- htc: HTC: 54 % (220 °C, 2 h) con +56 % de partículas a 200 °C por fragmentación; 71±7,5 % (220 °C, 3 h) [prus2025] [jose2025] (RES)
- incineracion_ue: opción política PO2 del JRC (incineración obligatoria + recuperación de P) elimina MPs del uso agrícola; monoincineración ~350 €/t MS (160–510) [jrc2023sludge] (TC)
- norma_ue_lodos: la Directiva 86/278/CEE solo regula metales pesados; la evaluación de la Comisión señala MPs como contaminante emergente no cubierto [swd2023] (OFI)
- monitorizacion_lodos: Directiva 2024/3019 art. 21(3): monitorizar MPs en lodos cuando proceda y en particular si se reutilizan en agricultura, en aglomeraciones ≥10.000 h-e [uwwtd2024] (OFI)

## tabla_tratamientos
| id | tratamiento | escala | eliminacion_mps | temperatura_tiempo | trl_aprox | coste | observaciones | verificacion | fuentes |
|---|---|---|---|---|---|---|---|---|---|
| digestion_anaerobia_mesofila | Digestión anaerobia mesofílica (35–37 °C) | real y laboratorio | ~30 % (no significativo, escala real); 62,1 % CSTR vs 88,6 % AnMBR (laboratorio) | mesofílica | 9 (proceso); no diseñado para MPs | "" | sugiere fragmentación más que mineralización; polímeros no degradados de forma general | ~30 % no confirmado [chand2021] RES; 88,6 % vs 62,1 % [lera2025] RES; 35/55 °C sin degradación general [lessa2024] RES | [chand2021]; [lera2025]; [lessa2024] |
| digestion_anaerobia_termofila | Digestión anaerobia termofílica (55 °C) | laboratorio | sin degradación general de los polímeros ensayados | 55 °C | 9 (proceso) | "" | "" | sin degradación general [lessa2024] RES | [lessa2024] |
| compostaje_convencional_hipertermofilo | Compostaje (hipertermófilo >70 °C) | real | 43,7 % en 45 d (hipertermófilo, real); PS 7,3 % en 56 d (laboratorio) | >70 °C, 45 d | 7 (estimación) | 30–35 €/t húmeda (compostaje, España, coste general de gestión) | el compost resultante sigue aportando MPs al suelo | 43,7 % [chen2020comp] RES; 30–35 €/t [iglesias2017] SEC | [chen2020comp]; [iglesias2017] |
| pirolisis | Pirólisis a biochar | laboratorio/piloto | ~99,6–99,9 % de partículas a 500 °C (cálculo propio a partir de 550,8–960,9 → 1,4–2,3 part./g); 91–97 % a 400–700 °C (2 h) | ≥450–500 °C | 6–7 para lodos (estimación) | análisis tecno-económico favorable (sin €/t extraído) | a temperaturas bajas pueden formarse nuevos polímeros; elimina también PFAS (100 % en el estudio) | 550,8–960,9 → 1,4–2,3 part./g [ni2020] RES; 91–97 %; PFAS 100 % [keller2024] RES | [ni2020]; [keller2024] |
| carbonizacion_hidrotermal | Carbonización hidrotermal (HTC) | laboratorio | 54 % (220 °C/2 h); 71±7,5 % (220 °C/3 h); 81–90 % por recuento y 69–78 % por masa (180–200 °C, digestato) | 180–220 °C, 2–3 h | 5–6 (estimación) | "" | a 200 °C el recuento subió 56 % (fragmentación) | 54 %; +56 % a 200 °C [prus2025] RES; 71±7,5 % [jose2025] RES; 81–90 % / 69–78 % [htc_acs2024] FRAG | [prus2025]; [jose2025]; [htc_acs2024]; [xu2022] |
| incineracion | Monoincineración / coincineración | real | sin datos directos en cenizas de lodo; en incineración de residuos urbanos persisten MPs en escorias y cenizas volantes | "" | 9 | monoincineración ~350 €/t MS (160–510 €/t MS) | permite recuperación de P de cenizas (art. 20 Directiva 2024/3019); medir MPs en escorias | 350 €/t MS (160–510) [jrc2023sludge] TC; MPs en cenizas de RSU [shen2021] RES | [jrc2023sludge]; [shen2021]; [uwwtd2024] |
| secado_termico | Secado térmico | real | "" | "" | 9 | 40–60 €/t húmeda (España, coste general) | sin datos de MPs hallados | 40–60 €/t [iglesias2017] SEC | [iglesias2017] |
| aplicacion_agricola_directa | Aplicación agrícola (referencia) | real | 0 % (vía de entrada al suelo) | "" | 9 | 15–20 €/t húmeda (España, coste general) | vía de entrada principal de MPs al suelo agrícola | 15–20 €/t [iglesias2017] SEC | [iglesias2017]; [nizzetto2016]; [lofty2022] |

## normativa
- ue_86_278: Directiva 86/278/CEE: uso agrícola de lodos; regula metales pesados; sin MPs [swd2023] (estado: vigente)
- ue_swd_2023_158: evaluación de la Comisión (2023): la directiva no cubre contaminantes emergentes como MPs; a oct-2026 no se ha localizado propuesta legislativa de revisión [swd2023] (estado: sin_propuesta_localizada)
- ue_jrc_estudio: estudio de viabilidad JRC: opciones desde monitorización + recuperación de P (PO1) hasta incineración obligatoria + recuperación de P (PO2) [jrc2023sludge] (estado: informativo)
- ue_2024_3019_art21: monitorización de MPs en entrada/salida de EDAR ≥10.000 h-e y en lodos cuando proceda; frecuencia: ≥2 muestras/año (≥150.000 h-e) y 1 cada 2 años (10.000–150.000 h-e); metodología a más tardar el 2-7-2027 [uwwtd2024] (estado: vigente) | nota: Sturm 2025 indica umbral >150.000 h-e para lodos; prevalece el texto oficial
- ue_2024_3019_art20: jerarquía de residuos para lodos y recuperación de recursos (P) [uwwtd2024] (estado: vigente)
- es_rd_1310_1990: RD 1310/1990 de uso de lodos en el sector agrario, en vigor [rd1310] (estado: vigente)
- es_modificacion: consulta pública previa de MITECO para modificar el RD 1310/1990 (cerró 21-11-2025); texto del proyecto no publicado a la fecha de esta revisión [miteco2025] (estado: en_tramitacion)

## recomendacion
- evitar contar con DA o compostaje como barrera de MPs: evidencia de reducción parcial o no significativa [chand2021][lessa2024][chen2020comp]
- ruta preferente por evidencia: pirólisis ≥450–500 °C o monoincineración con recuperación de P, frente a aplicación agrícola directa [ni2020][keller2024][jrc2023sludge]
- medir tanto recuento como masa en cada etapa del lodo para detectar fragmentación [prus2025]

## tareas
- t1: medir MPs en lodo primario, secundario, digerido y deshidratado de la EDAR piloto (balance de masas) [dd2024_1441] (estado: pendiente)
- t2: ensayo de pirólisis a 450/500/600 °C con socio externo y caracterización del biochar (MPs, PFAS, metales) [ni2020] [keller2024] (estado: pendiente)
- t3: contactar al gestor de lodos de la EDAR para costes reales €/t y destino actual  (estado: pendiente)
- t4: seguir la tramitación del nuevo RD de lodos (MITECO) y los actos de ejecución de la Directiva 2024/3019 [miteco2025] [uwwtd2024] (estado: pendiente)

## riesgos
- r1_fragmentacion: DA, HTC y compostaje pueden aumentar el recuento por fragmentación mientras baja la masa: medir partículas y masa (Py-GC/MS) [prus2025] [lera2025]
- r2_metodo_lodo: extracción de MPs en matriz orgánica (digestión H2O2/enzimática) con recuperaciones variables; spike obligatorio [prus2024] [dd2024_1441]
- r3_regulatorio: el nuevo RD español o una revisión de la Directiva de lodos pueden cambiar el destino permitido [miteco2025] [swd2023]
- r4_formacion_polimeros: pirólisis a baja temperatura puede formar nuevos polímeros [ni2020]

## decisiones
- d1: ¿incluir la línea de lodos en el alcance del proyecto o solo la línea de agua?  (estado: pendiente_usuario)
- d2: tratamiento térmico a ensayar: pirólisis (recomendado por evidencia) o HTC [ni2020] [keller2024] [prus2025] (estado: pendiente_usuario)

## proximo_paso
- confirmar d1 y, si se incluye, pedir a la EDAR datos del destino actual del lodo y su coste

## referencias
- [carnevale2024] Carnevale Miino M, Galafassi S, Zullo R, Torretta V, Rada EC (2024). Microplastics removal in wastewater treatment plants: A review of the different approaches to limit their release in the environment. Sci. Total Environ. 930:172675. https://doi.org/10.1016/j.scitotenv.2024.172675
- [chand2021] Chand R, et al. (2021). The occurrence and fate of microplastics in a mesophilic anaerobic digester receiving sewage sludge, grease, and fatty slurries. Sci. Total Environ. 798:149287. https://doi.org/10.1016/j.scitotenv.2021.149287
- [chen2020comp] Chen Z, et al. (2020). Enhanced in situ biodegradation of microplastics in sewage sludge using hyperthermophilic composting technology. J. Hazard. Mater. 384:121271. https://doi.org/10.1016/j.jhazmat.2019.121271
- [dd2024_1441] Decisión Delegada (UE) 2024/1441 de la Comisión, metodología para medir microplásticos en agua destinada al consumo humano (DO L 21-05-2024). https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024D1441
- [htc_acs2024] Exploring the Potential of Hydrothermal Treatment for Microplastics Removal in Digestate. ACS Sustainable Chem. Eng. 12(38):14187 (2024). https://pubs.acs.org/ascecg/article/12/38/14187/143565/Exploring-the-Potential-of-Hydrothermal-Treatment
- [iglesias2017] Iglesias R, Simón P, Moragas L, Arce A, Rodriguez-Roda I (2017). Cost comparison of full-scale water reclamation technologies with an emphasis on membrane bioreactors. Water Sci. Technol. 75(11):2562–2570. https://doi.org/10.2166/wst.2017.132
- [jose2025] Jose (2025). Hydrothermal carbonization as a promising approach towards the removal of polyethylene microplastics and trace organic contaminants from wastewater sludge. J. Environ. Chem. Eng. 13:118262. https://doi.org/10.1016/j.jece.2025.118262
- [jrc2023sludge] JRC (2023). Feasibility study in support of future policy developments of the Sewage Sludge Directive (86/278/EEC). JRC134591. https://publications.jrc.ec.europa.eu/repository/bitstream/JRC134591/JRC134591_01.pdf
- [keller2024] Keller AA, et al. (2024). Elimination of microplastics, PFAS, and PPCPs from biosolids via pyrolysis to produce biochar: Feasibility and techno-economic analysis. Sci. Total Environ. 947:174773. https://doi.org/10.1016/j.scitotenv.2024.174773
- [lera2025] Lera (2025). Mesophilic anaerobic digestion of mixed sludge in CSTR and AnMBR systems: A perspective on microplastics fate. J. Environ. Manage. 375:124250. https://doi.org/10.1016/j.jenvman.2025.124250
- [lessa2024] Lessa Belone MC, et al. (2024). Effects of mesophilic and thermophilic anaerobic digestion of sewage sludge on different polymers. Sci. Total Environ. 907:168014. https://doi.org/10.1016/j.scitotenv.2023.168014
- [lofty2022] Lofty J, et al. (2022). Microplastics removal from a primary settler tank in a WWTP and estimations of contamination onto European agricultural land via sewage sludge recycling. Environ. Pollut. 304:119198. https://doi.org/10.1016/j.envpol.2022.119198
- [miteco2025] MITECO (2025). Consulta pública previa del proyecto de RD que modifica el RD 1310/1990 y deroga la Orden AAA/1072/2013 (fin de plazo 21-11-2025). https://www.miteco.gob.es/es/calidad-y-evaluacion-ambiental/participacion-publica/consulta-publica-sobre-el-proyecto-del-real-decreto-que-modifica.html
- [ni2020] Ni BJ, Zhu ZR, Li W, et al. (2020). Microplastics Mitigation in Sewage Sludge through Pyrolysis: The Role of Pyrolysis Temperature. Environ. Sci. Technol. Lett. 7:961–967. https://doi.org/10.1021/acs.estlett.0c00740
- [nizzetto2016] Nizzetto L, Futter M, Langaas S (2016). Are Agricultural Soils Dumps for Microplastics of Urban Origin? Environ. Sci. Technol. 50:10777–10779. https://doi.org/10.1021/acs.est.6b04140
- [prus2024] Prus (2024). Microplastics in Sewage Sludge: Worldwide Presence in Biosolids ... Including the Hydrothermal Carbonization Process. Energies 17:4219. https://doi.org/10.3390/en17174219
- [prus2025] Prus (2025). The Effect of Hydrothermal Carbonization Temperature on Microplastic Content in Digested Sewage Sludge. Energies 18:5105. https://doi.org/10.3390/en18195105
- [rd1310] Real Decreto 1310/1990 por el que se regula la utilización de los lodos de depuración en el sector agrario (texto consolidado). https://www.boe.es/buscar/act.php?id=BOE-A-1990-26490
- [sccwrp2024] SCCWRP (2024). Characterizing the Removal of Microplastics by California Wastewater Treatment Plants: Implications for Management Strategies. Technical Report 1378. https://ftp.sccwrp.org/pub/download/DOCUMENTS/TechnicalReports/1378_MicroplasticsWastewaterPlants.pdf
- [shen2021] Shen M, et al. (2021). Can incineration completely eliminate plastic wastes? Microplastics and heavy metals in bottom ash and fly ash. Sci. Total Environ. 779:146528. https://doi.org/10.1016/j.scitotenv.2021.146528
- [swd2023] Comisión Europea (2023). Evaluation of the Sewage Sludge Directive 86/278/EEC. SWD(2023) 158 final. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=SWD%3A2023%3A158%3AFIN
- [uwwtd2024] Directiva (UE) 2024/3019 sobre tratamiento de aguas residuales urbanas (refundición), texto consolidado 12-12-2024. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02024L3019-20241212
- [xu2022] Xu (2022). Microplastic Degradation in Sewage Sludge by Hydrothermal Carbonization: Efficiency and Mechanisms. Chemosphere 297:134203. https://doi.org/10.1016/j.chemosphere.2022.134203
