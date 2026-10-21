# revision_tratamiento_microplasticos (v2)

## meta
- proyecto: REMPLAST-Q
- usuario: Lázaro López Paz
- documento: revision_tratamiento_microplasticos
- version: v2
- fecha: 2026-10-18
- idioma: es
- alcance: agua_residual_edar, agua_potable_etap, aguas_naturales, lodos_suelos
- metodo: búsqueda web de reseñas 2022-2026, artículos revisados por pares e informes oficiales; metadatos de todas las referencias con DOI comprobados en Crossref (18-10-2026); texto completo leído cuando hubo acceso abierto (Europe PMC, repositorios institucionales, MDPI/Springer vía web)
- nota_trl: TRL marcados '(estimación)' son valoración propia a partir de la escala de demostración descrita en la fuente
- nota_eficiencia: % no comparables entre estudios: tamaño mínimo detectado, método analítico, base partículas/masa y etapa de referencia
- leyenda_verificacion: estado_verificacion: TC=cifra comprobada en texto completo; RES=solo resumen/abstract; SEC=fuente secundaria (reseña que cita a otro); COM=fuente comercial/proveedor; FRAG=fragmento de buscador o página no leída completa; OFI=texto oficial (EUR-Lex/BOE); EST=estimación propia justificada

## objetivo
- mapear tecnologías de separación, coagulación, adsorción, degradación y biodegradación de MPs
- por tecnología: mecanismo, rango_tamano, eficiencia, trl_aprox, coste_escalabilidad, ventajas, limitaciones, riesgos y estado de verificación de cada cifra
- identificar opciones maduras, prometedoras y huecos de evidencia para REMPLAST-Q

## datos_clave
- edar_california: eliminación acumulada 95,3±6,7 % tras primario, 99,1±0,7 % tras secundario, 99,9 % tras terciario; el terciario retira 85,0±7,1 % de lo que queda (>125 µm, 7 EDAR, 2022-2023) [sccwrp2024] (TC)
- edar_por_etapa: primer escalón 16,5–98,4 %; biológico 78,1–99,9 % acumulado (valor alto con MBR) [bodzek2024] (RES)
- sumidero_lodo: potencialmente >65 % de los MPs entrantes en la EDAR acaban en el lodo [carnevale2024] (RES)
- terciarios_finlandia: MBR 99,9 % (6,9→0,005 MP/L), filtro rápido de arena 97 %, DAF 95 %, filtro de discos 40–98,5 % [talvitie2017] (TC)
- contraevidencia_mbr: seguimiento a largo plazo (Alemania, filtración de gran volumen ≥10 µm): efluente MBR 15,1 MP/L y 4ª etapa con CAP 15,1 MP/L frente a 21,8 MP/L en planta convencional, sin diferencia significativa; el afluente del MBR no se midió, por lo que no da % de eliminación; autores vinculados a Wasser 3.0 [sturm2025] (TC)
- etap_10_plantas: ETAP convencionales 98,7–99,4 %; MF 97,5 %; UF 99,3–100 % (≥2 µm, Raman); la coagulación-floculación-sedimentación no fue barrera consistente [npj2025] (TC)
- etap_tamano_critico: filtración granular 86,9 % para 10–20 µm frente a 99,9 % >100 µm; coagulación-sedimentación sola <2 % [zhang2020] (TC)
- coagulacion_rangos: coagulación convencional 8,28–98,2 %; electrocoagulación 8,24–99,4 % (rangos de reseña) [pu2023] (RES)
- biochar: filtros de biochar >95 % frente a 60–80 % de la arena (esferas 10 µm, laboratorio) [wang2020] (TC)
- ozono: 83 % de eliminación en efluente secundario (laboratorio, MPs 200–5000 µm) con coste energético calculado de 0,094 €/m3; PTFE y PVC resisten la ozonización [topkaya2025] [wieland2025] (TC)
- enzimas: LCC mejorada: ≥90 % de despolimerización de PET pretratado en <10 h (productividad 16,7 g TA/L/h) [tournier2020] (TC)
- degradacion_general: pérdida de masa ≠ mineralización; la mayoría de POA/fotocatálisis/plasma no cuantifican CO2 [iervolino2026] [he2023] (RES)
- regulacion_ue: Directiva (UE) 2024/3019 art. 21: monitorizar MPs en entrada y salida de EDAR ≥10.000 h-e y en lodos cuando proceda (en particular si se reutilizan en agricultura); sin valor límite; actos de ejecución con metodología a más tardar el 2-7-2027 [uwwtd2024] (OFI)
- coste_resumen: no existen costes €/m3 específicos de MPs a escala real; se usan costes generales de tecnología (ver 03_costes) [iglesias2017] [vsa2024] [vuori2022] (TC)

## sintesis_por_familia
### separacion_fisica
- primario/secundario: barrera principal por volumen, pero transfiere MPs al lodo [bodzek2024][sccwrp2024][carnevale2024]
- filtros_arena: robustos y baratos; tamizado >20 µm y adhesión <20 µm; punto débil 10–20 µm [zhang2020][na2021]
- mbr_membranas: mayor eficiencia documentada en campañas cortas, pero contraevidencia a largo plazo; fibras y defectos limitan; las membranas poliméricas pueden liberar MPs [talvitie2017][sturm2025][bodzek2025][maliwan2025]
- daf: 95 % en un único estudio a escala real [talvitie2017]
### coagulacion
- convencional: muy dependiente de polímero, pH y MON; débil <20 µm [zhang2020][pu2023]
- electrocoagulación: 92 % fibras / 88 % fragmentos; altera superficie, riesgo de nanoplásticos [senathirajah2023]
- organosilanos (Wasser 3.0): 86±8 % en piloto EDAR; dato del propio desarrollador [wasser30]
### adsorcion
- biochar >95 % vs 60–80 % arena [wang2020]; columnas 86,6–92,6 % [olubusoye2024]
- MOFs hasta 95,5 % [chen2020mof]; magnéticos 78–93 % [grbic2019]; esponjas 89,8 % [sun2020]
### degradacion
- ozonización 83 % [topkaya2025]; catalítica 70 % mineralización NPs PS [nieto2024]; PVC/PTFE resistentes [wieland2025]
- Fenton/persulfato: 56–98 % de pérdida de masa en condiciones severas [singh2024][lin2024][miao2020]
- fotocatálisis y plasma: escala de gramos/horas, mineralización rara vez demostrada [he2023][velasquez2024][iervolino2026]
### biodegradacion
- enzimas solo PET [tournier2020][lu2022]; planta Carbios en pausa [carbios2026]
- bacterias/hongos 6–43 % en 14–90 d [sust2023]; microalgas 84–98 % por agregación [gao2023][esmaeili2023]
### lodos_suelos
- compostaje hipertermófilo 43,7 % en 45 d; detalle completo en 02_lodos [chen2020comp]
### emergente
- microrobots magnéticos vivos 60–96 % en 1 h, laboratorio [song2025]

## tabla_comparativa
| id | familia | mecanismo | rango_tamano | eficiencia | trl_aprox | coste_escalabilidad | ventajas | limitaciones | riesgos | verificacion | fuentes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| tamizado_desbaste_primario | separacion_fisica | Cribado, desarenado/desengrasado y sedimentación/flotación por densidad | mayoritariamente >100 µm; poco eficaz para MPs pequeños y de baja densidad | 16,5–98,4 % (primer escalón EDAR); 95,3±6,7 % acumulado tras primario (7 EDAR California, >125 µm) | 9 | infraestructura existente; sin coste incremental específico | ya instalado; retiene la mayor parte de la masa de MPs | transfiere MPs a lodo; variabilidad alta entre plantas | acumulación en lodos (potencialmente >65 % de los MPs entrantes) | 16,5–98,4 % primer escalón [bodzek2024] RES; 95,3±6,7 % acumulado tras primario [sccwrp2024] TC; >65 % de MPs entrantes al lodo [carnevale2024] RES | [bodzek2024]; [sccwrp2024]; [carnevale2024] |
| biologico_fangos_activos | separacion_fisica | Incorporación a flóculos/EPS y sedimentación | micras a mm; peor para fibras y <20 µm | 78,1–99,9 % acumulado tras biológico; 99,1±0,7 % acumulado tras secundario (California) | 9 | "" | existente; alto % acumulado | efluente sigue aportando millones de partículas/día por gran volumen | MPs alteran EPS y sedimentabilidad del fango | 78,1–99,9 % acumulado tras biológico [bodzek2024] RES; 99,1±0,7 % acumulado tras secundario [sccwrp2024] TC | [bodzek2024]; [sccwrp2024]; [hybrid_acs] |
| filtro_arena_rapido | separacion_fisica | Tamizado mecánico (>20 µm) y adhesión a la superficie del grano (<20 µm) | casi total >100 µm; mínimo de eficacia en 10–20 µm | 97 % EDAR terciario (0,7→0,02 MP/L); ETAP laboratorio 86,9 % (10–20 µm) a 99,9 % (>100 µm); ~16 % de MPs de 10 µm atraviesan la arena | 9 | filtración rápida por gravedad 0,097 kWh/m3 vs UF 0,156 kWh/m3 (aguas urbanas); CAPEX ~100–115 €/(m3·d) y OPEX 0,08–0,12 €/m3 para tren coagulación+lamelas+filtración+desinfección (España, € 2011, no específico de MPs) | bajo coste operativo; robusto y escalable | paso de 10–20 µm y fibras; lavados devuelven MPs a cabecera | concentrado de lavado | 97 % (0,7→0,02 MP/L) [talvitie2017] TC; 86,9 % (10–20 µm) a 99,9 % (>100 µm) [zhang2020] TC; ~16 % de MPs de 10 µm atraviesan la arena [na2021] RES; 0,097 kWh/m3 vs UF 0,156 kWh/m3 [gcamejo2023] FRAG | [talvitie2017]; [zhang2020]; [na2021]; [gcamejo2023]; [iglesias2017] |
| filtro_discos_tela | separacion_fisica | Filtración superficial por malla/tela (≈10–20 µm) | "" | 40–98,5 % (0,5–2,0 → 0,03–0,3 MP/L) | 9 | OPEX 0,010–0,045 €/m3 (fuente comercial, no revisada por pares) | compacto | rendimiento muy variable | "" | 40–98,5 % [talvitie2017] TC | [talvitie2017]; [cloth_vendor] |
| daf | separacion_fisica | Microburbujas + coagulante que arrastran partículas de baja densidad a superficie | "" | 95 % (2,0→0,1 MP/L, efluente secundario) | 9 | 1,5–2 kWh/m3 (fuente comercial, no revisada por pares) | eficaz para polímeros flotantes (PE, PP) | evidencia a escala real limitada (pocas plantas) | consumo de reactivos | 95 % (2,0→0,1 MP/L) [talvitie2017] TC | [talvitie2017]; [daf_vendor] |
| mbr | separacion_fisica | Exclusión por tamaño en membrana + retención en fango de alta edad | retiene >0,1 µm (MF) / >0,02 µm (UF) en teoría; datos medidos sobre >20 µm | 99,9 % (6,9→0,005 MP/L, >20 µm); 99,69 % piloto escala real (507→1,58 MP/L); rango revisado 64,4–99,9 %; seguimiento alemán a largo plazo: efluente MBR 15,1 MP/L vs convencional 21,8 MP/L, sin diferencia significativa (no se midió el afluente del MBR, por lo que no hay % de eliminación) | 9 (MBR); 7–9 como barrera específica de MPs | CAPEX 700–960 €/(m3·d) y OPEX 0,2–0,45 €/m3 (MBR general, España, € 2011; no específico de MPs, ver 03_costes); MBR + incineración de fango = opción más coste-efectiva en análisis finlandés | mayor eficiencia documentada en EDAR; efluente apto reutilización | fibras pueden pasar (≈57 % de eliminación de fibras en MBR-MF); ensuciamiento | MPs se concentran en fango; membranas poliméricas pueden liberar MPs | 99,9 % (6,9→0,005 MP/L) [talvitie2017] TC; 99,69 % (507→1,58 MP/L) [egea2023] RES; 64,4–99,9 % rango revisado [bodzek2025] TC; 15,1 vs 21,8 MP/L sin diferencia significativa; afluente del MBR no medido [sturm2025] TC; MBR + incineración de fango más coste-efectivo [vuori2022] RES; ≈57 % de eliminación de fibras [hybrid_acs] FRAG; liberación de MPs desde membranas UF [maliwan2025] RES | [talvitie2017]; [egea2023]; [bodzek2025]; [sturm2025]; [vuori2022]; [hybrid_acs]; [iglesias2017]; [hybrid_acs]; [maliwan2025] |
| membranas_mf_uf_nf_oi | separacion_fisica | Exclusión por tamaño (UF ~0,02 µm; NF 1–10 nm; OI densa <1 nm) | UF: rechazo completo >1 µm en banco; NF/OI teóricamente MPs y NPs | ETAP con UF 99,3–100 %, con MF 97,5 % (≥2 µm, 10 plantas EE. UU.); NF/OI/UF/MBR en lixiviados 75–99 %; NF 96–99 % en lixiviado; OI >90 % habitualmente | 9 (proceso); 7–9 para MPs/NPs | UF 0,156 kWh/m3 (aguas urbanas); NF/OI mayor consumo (dato no hallado) | barrera más fiable incl. nanoplásticos (NF/OI) | fibras por defectos/juntas en OI; coste energético; ensuciamiento | concentrado/salmuera con MPs; liberación de MPs desde membranas poliméricas por abrasión/limpieza | UF 99,3–100 %, MF 97,5 % [npj2025] TC; 75–99 % en lixiviados; NF 96–99 % [leachate2024] FRAG; OI >90 % [acarer2023] RES | [npj2025]; [leachate2024]; [acarer2023]; [gcamejo2023]; [maliwan2025] |
| coagulacion_floculacion | coagulacion | Neutralización de carga, barrido e inclusión en flóculos | mejor ≥20 µm; débil <20 µm | 8,28–98,2 % (rango revisado); ETAP banco <2 % sedimentación con Al2(SO4)3, máx. 13,6 % con PolyDADMAC; coagulación + arena 91 % | 9 (proceso); 6–8 optimizado para MPs | coagulante ≈0,0594 ¥/t de agua con 91 % de eliminación (coagulación + arena, laboratorio/piloto) | instalado en ETAP/EDAR; barato | muy dependiente de polímero, pH, MON; en 10 ETAP reales no se observó reducción consistente por CFS | coagulantes poliméricos pueden aportar MPs | 8,28–98,2 % [pu2023] RES; <2 % sedimentación Al2(SO4)3; 13,6 % PolyDADMAC [zhang2020] TC; 91 % coagulación + arena; coagulante ≈0,0594 ¥/t [zhao2024] FRAG; CFS no fue barrera consistente [npj2025] TC; >80 % en ETAP con más etapas [xue2021] TC | [pu2023]; [zhang2020]; [zhao2024]; [npj2025]; [xue2021] |
| electrocoagulacion | coagulacion | Generación in situ de hidróxidos metálicos + electroflotación por H2 | "" | 8,24–99,4 % (rango revisado); 92 % fibras y 88 % fragmentos (agua sintética y de lavandería) | 4–6 (estimación) | 0,167 kWh/m3 y 0,0667 US$/m3 (laboratorio, agua de rechazo de OI) | sin dosificación química; compacto, apto para efluentes industriales/lavanderías | consumo de electrodos y energía; poca escala real | fragmentación y posible generación de nanoplásticos; ROS alteran superficie | 8,24–99,4 % [pu2023] RES; 92 % fibras / 88 % fragmentos [senathirajah2023] RES; 95 % a 3 mA/cm2; 0,167 kWh/m3; 0,0667 US$/m3 (laboratorio, agua de rechazo OI) [kim2026] RES | [pu2023]; [senathirajah2023]; [kim2026] |
| aglomeracion_organosilanos | coagulacion | Agentes híbridos sol-gel que aglomeran MPs en flóculos separables sin filtro | "" | 86±8 % piloto EDAR Mykonos; hasta 97,4 % masa / 99,1 % partículas en agua industrial (datos del fabricante, citando Clean Technol. 2025/2026) | 6–7 (estimación) | "" | piloto en EDAR real; sin membranas | rendimiento cae con baja concentración y matrices complejas; fuente principal es el propio desarrollador | aglomerados no aptos para vertedero; valorización térmica | 86±8 % piloto Mykonos [wasser30] COM | [wasser30] |
| biochar | adsorcion | Atrapamiento en poros, enredo, adherencia, interacciones hidrofóbicas/π–π/electrostáticas | probado con esferas de 10 µm | >95 % (filtros de biochar) vs 60–80 % arena, esferas 10 µm; 86,6–92,6 % en columnas para escorrentía agrícola | 4–5 (estimación) | bajo coste de material (cualitativo); sin €/m3 publicado hallado | valoriza residuos; compatible con filtros existentes | regeneración; validación en agua real escasa | desprendimiento de finos de biochar; fin de vida del adsorbente cargado | >95 % vs 60–80 % arena [wang2020] TC; 86,6–92,6 % [olubusoye2024] TC | [wang2020]; [olubusoye2024]; [li2024] |
| mofs | adsorcion | Interacciones electrostáticas, puentes H y coordinación en espuma porosa | "" | hasta 95,5±1,2 % (PVDF); 88,2 % PMMA; 85,7 % PS | 3–4 (estimación) | "" | reutilizable en ciclos; alta selectividad | coste y estabilidad de MOF en agua real | lixiviación de metales/ligandos | 95,5±1,2 % PVDF [chen2020mof] RES | [chen2020mof] |
| nanomateriales_magneticos | adsorcion | Adsorción hidrofóbica + separación magnética | 10 µm–>1 mm | 92 % (PE/PS 10–20 µm); 93 % agua de mar >1 mm; 84 % agua dulce; 78 % sedimento | 3–4 (estimación) | "" | recuperación sencilla; reutilización potencial | dosificación/recuperación a gran caudal no demostrada | pérdida de nanopartículas al medio | 92/93/84/78 % [grbic2019] TC | [grbic2019] |
| esponjas | adsorcion | Interacciones electrostáticas, puentes H, π–π; difusión intraparticular | PS 1 µm | 89,8 % PS neutro (24 h); 72,4 % y 88,9 % PS carboxilado/aminado tras 3 ciclos | 3 (estimación) | "" | biodegradable/reutilizable | cinética lenta (24 h); solo partículas modelo | "" | 89,8 % PS [sun2020] RES | [sun2020] |
| ozonizacion | degradacion | Oxidación directa por O3 y por •OH | "" | 83 % de eliminación en efluente secundario (pH 7, 10 ppm O3, 60 min); ozonización catalítica: 70 % mineralización de nanoplásticos de PS | 9 (proceso); 4–5 para MPs (estimación) | 0,094 €/m3 (cálculo energético de laboratorio, MPs 200–5000 µm); 4ª etapa ozono escala real Suiza 0,07–0,15 CHF/m3 (plantas grandes, no específico de MPs; ver 03_costes) | ya presente en ETAP/4ª etapa EDAR | PVC/PTFE resistentes; mineralización incompleta | fragmentación en nanoplásticos; subproductos de oxidación | 83 % (pH 7, 10 ppm, 60 min); coste 0,094 €/m3 (energía, laboratorio, MPs 200–5000 µm) [topkaya2025] TC; 70 % mineralización NPs PS [nieto2024] RES; PTFE/PVC resistentes [wieland2025] TC | [topkaya2025]; [nieto2024]; [vsa2024]; [wieland2025] |
| fenton_persulfato_hidrotermal | degradacion | Radicales •OH / SO4•− atacan cadena polimérica | 100–200 µm (PVC, electro-Fenton) | Fenton hidrotermal 98,43 % pérdida de masa en 24 h; electro-Fenton-persulfato 91,3 % PET en 12 h; electro-Fenton TiO2/grafito 56 % pérdida de masa PVC y 75 % decloración (100 °C, 6 h); Fenton 60 min: efecto modesto, PP resistente | 3–4 (estimación) | "" | destrucción (no solo transferencia) | condiciones severas (pH 3, 100 °C+); matrices reales poco estudiadas | mineralización incompleta; pérdida de masa ≠ mineralización; lixiviación de aditivos | 98,43 %/24 h [singh2024] RES; 91,3 % PET/12 h [lin2024] RES; 56 % masa PVC; 75 % decloración [miao2020] RES; Fenton 60 min efecto modesto [fenton_water2024] FRAG | [singh2024]; [lin2024]; [miao2020]; [fenton_water2024]; [he2023] |
| fotocatalisis | degradacion | Pares e−/h+ bajo luz generan ROS que oxidan la superficie | "" | ZnO: oxidación/fragilización LDPE, sin mineralización verificada; TiOx/ZnO: pérdida de masa completa en 480–816 h (sin demostrar mineralización) | 2–4 (estimación) | "" | puede usar luz solar/visible | tiempos de cientos de horas; contacto sólido-sólido ineficiente | fragmentación a nanoplásticos; UV/H2O2 aumenta toxicidad del agua tratada | ZnO oxidación LDPE [tofa2019] RES; pérdida de masa completa 480–816 h [he2023] RES | [tofa2019]; [he2023]; [na2021] |
| plasma_no_termico | degradacion | Especies reactivas (O, •OH, O3), UV y electrones | "" | 1,4–11,3 % pérdida de masa PP/LDPE en 30 min (plasma frío); 83 % pérdida de masa PS en 5 min (descarga ns); degradación completa 0,1 g PE en 3 h (DBD en aire) | 2–3 (estimación) | "" | sin reactivos; rápido | alta energía; escala de gramos | subproductos gaseosos; mineralización a verificar con CO2 | 1,4–11,3 % en 30 min [velasquez2024] RES; 83 % PS en 5 min [plasma2024] RES; 0,1 g PE en 3 h [kim2025] RES | [velasquez2024]; [plasma2024]; [kim2025]; [iervolino2026] |
| enzimas_petasa_cutinasa | biodegradacion | Hidrólisis de enlaces éster de PET a TPA/EG | probado en films/fragmentos/textil, no en MPs ambientales | LCC: ≥90 % despolimerización PET pretratado en <10 h; FAST-PETase: PET de 51 productos despolimerizado en 1 semana a 50 °C | 7–8 para reciclaje PET; 2–3 para MPs en agua (estimación) | planta Carbios Longlaville (50.000 t/año) paralizada a la espera de cierre financiero (H1 2026) | condiciones suaves; monómeros recuperables | solo poliésteres (PET); PE/PP/PS no; PET cristalino requiere pretratamiento | MPs mixtos no hidrolizables | ≥90 % en <10 h; 16,7 g TA/L/h [tournier2020] TC; 51 productos en 1 semana [lu2022] RES; Longlaville en pausa (H1 2026) [carbios2026] COM | [tournier2020]; [lu2022]; [carbios2026] |
| bacterias_hongos | biodegradacion | Biofilm, oxidación enzimática y asimilación | "" | LDPE 9,26 %/30 d (B. subtilis); PE 6,25 %/30 d (P. aeruginosa); LDPE 35 %/90 d (A. clavatus); PE 43 %/14 d (Z. maritimum) | 2–4 (estimación) | "" | bajo consumo energético | tasas lentas (% por mes); pérdida de peso no prueba mineralización | fragmentación; metabolitos | 6,25–43 % pérdida de peso [sust2023] SEC | [sust2023] |
| microalgas | biodegradacion | EPS y carga superficial agregan MPs; posible degradación | "" | Scenedesmus abundans: 84 % PS, 87 % PLA, 98 % PMMA; Chlorella vulgaris: 84 % PE (pH 10) | 3–4 (estimación) | "" | integrable con lagunaje/tratamiento de nutrientes | tiempos de retención largos; toxicidad de MPs para algas | biomasa residual cargada de MPs | 84/87/98 % [gao2023] SEC; 84 % PE pH 10 [esmaeili2023] TC | [gao2023]; [esmaeili2023] |
| compostaje_hipertermofilo_lodos | lodos_suelos | Bio-oxidación por Thermus, Bacillus, Geobacillus | "" | 43,7 % de eliminación de MPs en lodo en 45 d (escala real); PS 7,3 % en 56 d (laboratorio) | 7 (estimación) | "" | aborda el sumidero principal (lodo) | eliminación parcial | MPs residuales al suelo vía compost | 43,7 % en 45 d [chen2020comp] RES | [chen2020comp] |
| microrobots_magneticos | emergente | Enjambre 3D por campo magnético rotatorio; captura por adhesión y retirada magnética | 50 nm–~10 µm | 83–89 % PS micro/nano; 60 % PET; 96 % MPs de exfoliante (1 h); 77 % en agua de río | 2–3 (estimación) | "" | captura nanoplásticos | volúmenes de laboratorio; requiere bobinas electromagnéticas | liberación de biomasa (endotoxinas medidas bajas) | 83–89 %, 60 %, 96 %, 77 % [song2025] TC | [song2025] |

## tareas
- t1: extraer tablas de eficiencia por tamaño/forma/polímero de bodzek2024, bodzek2025 y sccwrp2024 a base de datos propia [bodzek2024] [bodzek2025] [sccwrp2024] (estado: pendiente)
- t2: protocolo de medida REMPLAST-Q definido en 04_plan_proyecto (alineado con DD 2024/1441 y Directiva 2024/3019) [dd2024_1441] [uwwtd2024] (estado: hecho_v2)
- t3: priorizar tecnologías para ensayo: propuesta en 04_plan_proyecto (arena vs arena+biochar, coagulación/EC, UF como referencia)  (estado: propuesto_requiere_decision)
- t4: diseñar ensayos de degradación con balance de carbono (CO2/COT) y cuantificación de nanoplásticos  (estado: pendiente)
- t5: costes €/m3: recopilados en 03_costes (generales, no específicos de MPs) [iglesias2017] [vsa2024] (estado: hecho_v2)
- t6: obtener texto completo de las fuentes marcadas RES/FRAG (bibliotecas, préstamo interbibliotecario o autores)  (estado: pendiente)

## riesgos
- r1_comparabilidad: % dependientes del método y tamaño mínimo [npj2025] [xie2024]
- r2_transferencia_lodo: la separación física desplaza MPs al lodo y al suelo agrícola [carnevale2024] [nizzetto2016]
- r3_nanoplasticos: EC, ozono, UV/H2O2 y POA pueden fragmentar MPs en NPs [senathirajah2023] [wieland2025] [na2021]
- r4_mineralizacion_incompleta: pérdida de masa no demuestra mineralización [iervolino2026] [he2023]
- r5_autoaporte: membranas y coagulantes poliméricos pueden liberar MPs [maliwan2025] [npj2025]
- r6_sesgo_fuente: datos de proveedores y partículas modelo sobreestiman la eficiencia en agua real [wasser30]
- r7_evidencia_contradictoria_mbr: >99 % en campañas cortas vs sin diferencia significativa a largo plazo [talvitie2017] [sturm2025]

## decisiones
- d1: eficiencia por etapa y tamaño mínimo como metadatos obligatorios de cada cifra  (estado: propuesta)
- d2: distinguir 'eliminación' (separación) de 'degradación' (mineralización)  (estado: propuesta)
- d3: TRL como estimación propia a validar por el equipo  (estado: propuesta)
- d4: selección de tecnologías para piloto (ver 04_plan_proyecto, decisión dp3)  (estado: pendiente_usuario)

## proximo_paso
- revisar con el usuario las decisiones de 04_plan_proyecto y conseguir texto completo de las fuentes RES/FRAG prioritarias (bodzek2024, egea2023, pu2023, senathirajah2023)

## huecos_evidencia
- costes €/m3 específicos de MPs prácticamente inexistentes [iglesias2017][vuori2022]
- nanoplásticos <1 µm: casi sin datos a escala real; la mayoría de estudios miden >10–125 µm [sccwrp2024][npj2025]
- degradación en matrices reales con balance de carbono: escasa [iervolino2026]
- biochar en filtros a escala real: sin datos de campo [wang2020][li2024]

## cambios_v2
- referencias unificadas con clave (referencias.md); todos los DOI comprobados en Crossref
- González-Camejo corregido a 2023 (J. Water Process Eng. 51:103452)
- Carnevale Miino 2024 (STOTEN 930:172675) y Bodzek & Bodzek 2025 (Membranes 15:82) identificados (antes solo URL)
- Olubusoye: DOI sin sufijo /full
- Talvitie 2017 y Tournier 2020: metadatos confirmados y cifras comprobadas en texto completo
- MBR: aclarado que Sturm 2025 no midió el afluente del MBR
- añadidos coste de ozono 0,094 €/m3 (Topkaya), costes generales de MBR/filtración (Iglesias 2017), EC (Kim 2026) y estado_verificacion por cifra

## referencias (detalle en ../referencias.md)
- [acarer2023] Acarer S (2023). A review of microplastic removal from water and wastewater by membrane technologies. Water Sci. Technol. 88:199–219. https://doi.org/10.2166/wst.2023.186
- [bodzek2024] Bodzek M, et al. (2024). Microplastics in Wastewater Treatment Plants: Characteristics, Occurrence and Removal Technologies. Water 16:3574. https://doi.org/10.3390/w16243574
- [bodzek2025] Bodzek M, Bodzek P (2025). Remediation of Micro- and Nanoplastics by Membrane Technologies. Membranes 15:82. https://doi.org/10.3390/membranes15030082
- [carbios2026] Carbios (24-09-2026). Carbios reports first-half 2026 results (nota de prensa). https://www.globenewswire.com/news-release/2026/09/24/3367956/0/en/carbios-reports-first-half-2026-results.html
- [carnevale2024] Carnevale Miino M, Galafassi S, Zullo R, Torretta V, Rada EC (2024). Microplastics removal in wastewater treatment plants: A review of the different approaches to limit their release in the environment. Sci. Total Environ. 930:172675. https://doi.org/10.1016/j.scitotenv.2024.172675
- [chen2020comp] Chen Z, et al. (2020). Enhanced in situ biodegradation of microplastics in sewage sludge using hyperthermophilic composting technology. J. Hazard. Mater. 384:121271. https://doi.org/10.1016/j.jhazmat.2019.121271
- [chen2020mof] Chen YJ, et al. (2020). Metal–organic framework-based foams for efficient microplastics removal. J. Mater. Chem. A 8:14644–14652. https://doi.org/10.1039/D0TA04891G
- [cloth_vendor] Filter Systems. Wastewater Treatment OPEX: Cost Benchmark per m³ (web comercial). https://filter-systems.com/en/knowledge/operating-cost-per-cubic-metre-the-items-that-actually-move-the-number
- [daf_vendor] Sigma DAF Clarifiers. Preguntas frecuentes DAF (web comercial). https://sigmadafclarifiers.com/en/sistemas-daf/preguntas-frecuentes-daf/
- [dd2024_1441] Decisión Delegada (UE) 2024/1441 de la Comisión, metodología para medir microplásticos en agua destinada al consumo humano (DO L 21-05-2024). https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024D1441
- [egea2023] Egea-Corbacho A, et al. (2023). Occurrence, identification and removal of microplastics in a WWTP compared to an advanced MBR technology: full-scale pilot plant. J. Environ. Chem. Eng. 11:109644. https://doi.org/10.1016/j.jece.2023.109644
- [esmaeili2023] Esmaeili Nasrabadi A, et al. (2023). Utilizing Chlorella vulgaris algae as an eco-friendly coagulant for efficient removal of polyethylene microplastics. Heliyon 9:e22338. https://doi.org/10.1016/j.heliyon.2023.e22338
- [fenton_water2024] Evaluation of Fenton, Photo-Fenton and Fenton-like Processes in Degradation of PE, PP, and PVC Microplastics. Water 16(5):673 (2024). https://www.mdpi.com/2073-4441/16/5/673
- [gao2023] Gao (2023). Feasibility, challenges, and future prospects of microalgae-based bioremediation technique for removing microplastics from wastewater. Front. Bioeng. Biotechnol. 11:1288439. https://doi.org/10.3389/fbioe.2023.1288439
- [gcamejo2023] González-Camejo J, et al. (2023). Feasibility of Rapid Gravity Filtration and Membrane Ultrafiltration for the Removal of Microplastics and Microlitter in Sewage and Wastewater from Plastic Industry. J. Water Process Eng. 51:103452. https://doi.org/10.1016/j.jwpe.2022.103452
- [grbic2019] Grbic J, et al. (2019). Magnetic Extraction of Microplastics from Environmental Samples. Environ. Sci. Technol. Lett. 6:68–72. https://doi.org/10.1021/acs.estlett.8b00671
- [he2023] He Y, Rehman AU, Xu M, et al. (2023). Photocatalytic degradation of different types of microplastics by TiOx/ZnO tetrapod photocatalysts. Heliyon 9:e22562. https://doi.org/10.1016/j.heliyon.2023.e22562
- [hybrid_acs] Hybrid Wastewater Treatment: Efficiency and Challenges in Microplastic Removal. ACS ES&T Water 6(5):2619. https://pubs.acs.org/aewcaa/article/6/5/2619/5070745/Hybrid-Wastewater-Treatment-Efficiency-and
- [iervolino2026] Iervolino (2026). Non-thermal DBD plasma for the degradation of microplastics suspended in water: evidence from CO2 quantification. Chem. Eng. J. 528:172474. https://doi.org/10.1016/j.cej.2025.172474
- [iglesias2017] Iglesias R, Simón P, Moragas L, Arce A, Rodriguez-Roda I (2017). Cost comparison of full-scale water reclamation technologies with an emphasis on membrane bioreactors. Water Sci. Technol. 75(11):2562–2570. https://doi.org/10.2166/wst.2017.132
- [kim2025] Kim (2025). Degradation of polyethylene microplastics using high-repetition-rate pulsed DBD plasma in air under mild conditions. J. Phys. D: Appl. Phys. 58:315203. https://doi.org/10.1088/1361-6463/adef64
- [kim2026] Kim (2026). Parametric study on electro-coagulation for efficient removal of microplastics from reverse osmosis wastewater. Water Sci. Technol. 93:903–915. https://doi.org/10.2166/wst.2026.239
- [leachate2024] Membrane technology as a strategy for microplastics removal from landfill leachate: a review. Water Sci. Technol. 90(9):2469 (2024). https://iwaponline.com/wst/article/90/9/2469/105412/Membrane-technology-as-a-strategy-for
- [li2024] Li (2024). The Removal and Mitigation Effects of Biochar on Microplastics in Water and Soils. Sustainability 16:9749. https://doi.org/10.3390/su16229749
- [lin2024] Lin Y, Zhang Y, Wang Y, et al. (2024). Efficient degradation and mineralization of PET microplastics ... electro-Fenton-activated persulfate oxidation system. J. Hazard. Mater. 478:135635. https://doi.org/10.1016/j.jhazmat.2024.135635
- [lu2022] Lu H, Diaz DJ, Czarnecki NJ, et al. (2022). Machine learning-aided engineering of hydrolases for PET depolymerization. Nature 604:662–667. https://doi.org/10.1038/s41586-022-04599-z
- [maliwan2025] Maliwan T, Hu J (2025). Release of microplastics from polymeric ultrafiltration membrane system for drinking water treatment under different operating conditions. Water Research 274:123047. https://doi.org/10.1016/j.watres.2024.123047
- [miao2020] Miao F, et al. (2020). Degradation of polyvinyl chloride microplastics via an electro-Fenton-like system with a TiO2/graphite cathode. J. Hazard. Mater. 399:123023. https://doi.org/10.1016/j.jhazmat.2020.123023
- [na2021] Na SH, Kim MJ, Kim JT, et al. (2021). Microplastic removal in conventional drinking water treatment processes: Performance, mechanism, and potential risk. Water Research 202:117417. https://doi.org/10.1016/j.watres.2021.117417
- [nieto2024] Nieto-Sandoval J, et al. (2024). Enhancing nanoplastics removal by metal ion-catalyzed ozonation. Chem. Eng. J. Adv. 19:100621. https://doi.org/10.1016/j.ceja.2024.100621
- [nizzetto2016] Nizzetto L, Futter M, Langaas S (2016). Are Agricultural Soils Dumps for Microplastics of Urban Origin? Environ. Sci. Technol. 50:10777–10779. https://doi.org/10.1021/acs.est.6b04140
- [npj2025] Balkenbusch F, et al. (2025). Microplastic removal across ten drinking water treatment facilities and distribution systems. npj Clean Water 8:103. https://doi.org/10.1038/s41545-025-00531-w
- [olubusoye2024] Olubusoye BS, et al. (2024). Removal of microplastics from agricultural runoff using biochar: a column feasibility study. Front. Environ. Sci. 12:1388606. https://doi.org/10.3389/fenvs.2024.1388606
- [plasma2024] Polystyrene (PS) Degradation Induced by Nanosecond Electric Discharge in Air in Contact with PS/Water. Plasma 7(1):4. https://www.mdpi.com/2571-6182/7/1/4
- [pu2023] Pu (2023). Coagulation technologies for separation of microplastics in water: current status. J. Phys.: Conf. Ser. 2608:012056. https://doi.org/10.1088/1742-6596/2608/1/012056
- [sccwrp2024] SCCWRP (2024). Characterizing the Removal of Microplastics by California Wastewater Treatment Plants: Implications for Management Strategies. Technical Report 1378. https://ftp.sccwrp.org/pub/download/DOCUMENTS/TechnicalReports/1378_MicroplasticsWastewaterPlants.pdf
- [senathirajah2023] Senathirajah K, et al. (2023). Fate and transformation of microplastics due to electrocoagulation treatment: Impacts of polymer type and shape. Environ. Pollut. 334:122159. https://doi.org/10.1016/j.envpol.2023.122159
- [singh2024] Singh (2024). Hybrid Oxidation of Microplastics with Fenton and Hydrothermal Reactions. ACS ES&T Water 4:1688–1700. https://doi.org/10.1021/acsestwater.3c00742
- [song2025] Song SJ, Kim J, Gabor R, Zboril R, Pumera M (2025). Magnetically Driven Living Microrobot Swarms for Aquatic Micro- and Nanoplastic Cleanup. ACS Nano 19:27259–27269. https://doi.org/10.1021/acsnano.5c04045
- [sturm2025] Sturm MT, Argyropoulou D, Myers E, et al. (2025). Comparative Long-Term Monitoring of Microplastics in the Effluent of Three Different WWTPs with Two, Three, and Four Treatment Stages. Water 17(5):711. https://doi.org/10.3390/w17050711
- [sun2020] Sun C, et al. (2020). Fabrication of robust and compressive chitin and graphene oxide sponges for removal of microplastics with different functional groups. Chem. Eng. J. 393:124796. https://doi.org/10.1016/j.cej.2020.124796
- [sust2023] Systematic Review of Degradation Processes for Microplastics: Progress and Prospects. Sustainability 15(17):12698 (2023). https://www.mdpi.com/2071-1050/15/17/12698
- [talvitie2017] Talvitie J, Mikola A, Koistinen A, Setälä O (2017). Solutions to microplastic pollution – Removal of microplastics from wastewater effluent with advanced wastewater treatment technologies. Water Research 123:401–407. https://doi.org/10.1016/j.watres.2017.07.005
- [tofa2019] Tofa TS, et al. (2019). Visible light photocatalytic degradation of microplastic residues with zinc oxide nanorods. Environ. Chem. Lett. 17:1341–1346. https://doi.org/10.1007/s10311-019-00859-z
- [topkaya2025] Topkaya E, Arslan A, Veli S, Kuru S, Sezer M (2025). Removal of Microplastics by Ozone Oxidation from Urban Wastewater Using Taguchi Experimental Design. Water Air Soil Pollut. 236:606. https://doi.org/10.1007/s11270-025-08249-8
- [tournier2020] Tournier V, Topham CM, Gilles A, et al. (2020). An engineered PET depolymerase to break down and recycle plastic bottles. Nature 580:216–219. https://doi.org/10.1038/s41586-020-2149-4
- [uwwtd2024] Directiva (UE) 2024/3019 sobre tratamiento de aguas residuales urbanas (refundición), texto consolidado 12-12-2024. https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A02024L3019-20241212
- [velasquez2024] Velasquez JA, Bao Y, Huang JY (2024). Atmospheric cold plasma as a novel approach to remediating microplastics pollution in water. Environ. Pollut. 356:124390. https://doi.org/10.1016/j.envpol.2024.124390
- [vsa2024] Hunziker Betatech AG para VSA (2024). Evaluation of the energy and cost figures of processes for the elimination of micropollutants in WWTPs. Informe técnico 1490.26 (28-09-2024). https://micropoll.ch/wp-content/uploads/2025/03/Energy-and-cost-key-figures-MP-treatment.pdf
- [vuori2022] Vuori L, Ollikainen M (2022). How to remove microplastics in wastewater? A cost-effectiveness analysis. Ecological Economics 192:107246. https://doi.org/10.1016/j.ecolecon.2021.107246
- [wang2020] Wang Z, Sedighi M, Lea-Langton A (2020). Filtration of microplastic spheres by biochar: removal efficiency and immobilisation mechanisms. Water Research 184:116165. https://doi.org/10.1016/j.watres.2020.116165
- [wasser30] Wasser 3.0 gGmbH. Microplastic monitoring for municipal WWTPs (página técnica, revisada ago-2026). https://wasserdreinull.de/en/offers-and-services/wastewater-treatment/
- [wieland2025] Wieland (2025). Ozone-mediated breakdown of microplastics in aqueous environments. J. Anal. At. Spectrom. 40:2870–2878. https://doi.org/10.1039/d5ja00226e
- [xie2024] Xie (2024). Analysing micro- and nanoplastics with cutting-edge infrared spectroscopy techniques: a critical review. Anal. Methods 16:2177–2197. https://doi.org/10.1039/D3AY01808C
- [xue2021] Xue J, et al. (2021). What have we known so far about microplastics in drinking water treatment? A timely review. Front. Environ. Sci. Eng. 16:58. https://doi.org/10.1007/s11783-021-1492-5
- [zhang2020] Zhang Y, Diehl A, Lewandowski A, Gopalakrishnan K, Baker T (2020). Removal efficiency of micro- and nanoplastics (180 nm–125 μm) during drinking water treatment. Sci. Total Environ. 720:137383. https://doi.org/10.1016/j.scitotenv.2020.137383
- [zhao2024] Zhao (2024). Research on Effect of Microplastics Removal through Combination of Coagulation and Sand Filtration. E3S Web Conf. 598:01005. https://doi.org/10.1051/e3sconf/202459801005
