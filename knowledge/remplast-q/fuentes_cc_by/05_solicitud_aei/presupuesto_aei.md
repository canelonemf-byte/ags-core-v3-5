# presupuesto_aei (v1)

## meta
- proyecto: REMPLAST-Q
- documento: presupuesto_aei_pgc_2026
- version: v1
- fecha: 2026-10-18
- idioma: es
- autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial; ORCID 0000-0001-8601-1963
- duracion: 36 meses (inicio no antes del 1-9-2027)
- regla: importes "" hasta tener ofertas o tarifas de la entidad; solo partidas elegibles según el art. 11
- leyenda_verificacion: estado_verificacion: TC=cifra comprobada en texto completo; RES=solo resumen/abstract; SEC=fuente secundaria (reseña que cita a otro); COM=fuente comercial/proveedor; FRAG=fragmento de buscador o página no leída completa; OFI=texto oficial (EUR-Lex/BOE); EST=estimación propia justificada

## datos_clave
- costes_marginales: presupuesto solo en costes marginales; ayuda hasta el 100 % (art. 11.1) [aei_conv2026] (OFI)
- indirectos: indirectos = 25 % fijo de los directos (art. 11.4) [aei_conv2026] (OFI)
- umbral_ingles: si los costes directos son ≥100.000 €, la memoria se presenta en inglés y se recomienda la justificación del presupuesto en inglés (art. 18.1.m, 18.2.a) [aei_conv2026] (OFI)
- escala_referencia: referencia de escala: ReUseMP3 (proyecto estatal sobre MPs en reutilización de agua), MCIU, 3 años, 210.830,40 €; no es un tope [reusemp3] (OFI)
- energia_piloto: energía de la filtración piloto ≈850 kWh/año para 1 m3/h (a 0,097 kWh/m3); coste = kWh × precio de la EDAR (si la paga el proyecto) [gcamejo2023] (EST)

## partidas
| id | articulo | concepto | anualidad_1 | anualidad_2 | anualidad_3 | total | base_calculo | notas |
|---|---|---|---|---|---|---|---|---|
| a_personal | 11.3.a | contrato de técnico/a de laboratorio o investigador/a posdoctoral dedicado/a al proyecto (no el IP ni el equipo de investigación) | "" | "" | "" | "" | tablas salariales de la entidad × meses × dedicación | no elegible el personal propio de capítulo I en entidades públicas |
| b_movilidad | 11.3.b | desplazamientos a la EDAR para muestreo (campañas) y congresos | "" | "" | "" | "" | normativa de dietas de la entidad; estancias ≤1.500 €/mes en España | campañas de muestreo pueden superar 1 mes |
| c_equipamiento | 11.3.c | columnas piloto (arena, arena+biochar), módulo UF de referencia, bombas, caudalímetros, turbidímetros, filtros en cascada 100/20 µm de acero inoxidable | "" | "" | "" | "" | ofertas (3 si supera el contrato menor) | uso para el fin durante ≥5 años |
| d_fungible | 11.3.d | filtros, reactivos de digestión, patrones de MPs (PE/PET, 30–70 y 120–200 µm) para recuperación, biochar comercial, consumibles de Py-GC/MS | "" | "" | "" | "" | ofertas | sin material de oficina |
| e_inmateriales | 11.3.e | software de análisis espectral / biblioteca de polímeros | "" | "" | "" | "" | ofertas | "" |
| g_datos | 11.3.g | repositorio de datos (espectros, recuentos) FAIR | "" | "" | "" | "" | tarifa del repositorio (puede ser gratuito) | "" |
| i_servicios_id | 11.3.i | servicios externos de análisis µFTIR/LDIR/µRaman o Py-GC/MS y ensayos de pirólisis, si la entidad no dispone de ellos | "" | "" | "" | "" | nº de muestras × €/muestra (ofertas) | confirmar con la oficina de investigación si cuentan como subcontratación (límite 25 %, art. 11.3.q) |
| j_publicacion | 11.3.j | publicación en acceso abierto (APC) y depósito en repositorios | "" | "" | "" | "" | APC de las revistas objetivo | no números especiales |
| l_m_difusion | 11.3.l–m | inscripción en congresos; jornada final con operadores de EDAR | "" | "" | "" | "" | tarifas | "" |
| n_servicios_centrales | 11.3.n | servicios científico-técnicos de la entidad (microscopía, FTIR, TGA) con tarifas públicas | "" | "" | "" | "" | tarifas públicas de la entidad | "" |
| q_subcontratacion | 11.3.q | subcontratación (si procede) | "" | "" | "" | "" | ≤25 % de la ayuda | identificar al subcontratista en la solicitud |
| costes_indirectos | 11.4 | costes indirectos | "" | "" | "" | "" | 25 % × total de costes directos (fijo) | se calculan sobre los directos; no se justifican |
| predoctoral_opcional | 14.3 | ayuda predoctoral asociada (opcional) | "" | "" | "" | 143.350 € (importe fijo de la convocatoria) | 32.500 €/año de contrato + 3.350 € de indemnización + 10.000 € para estancias y matrícula | se concede aparte si la comisión lo propone; el desglose por anualidad depende de la fecha de incorporación |

## tareas
- t1: pedir ofertas de análisis (µFTIR/LDIR/Raman, Py-GC/MS) y de equipos piloto  (estado: pendiente)
- t2: pedir a la oficina de investigación de la entidad las tablas salariales y las tarifas de servicios  (estado: pendiente)
- t3: decidir si los costes directos superan 100.000 € (idioma de la memoria)  (estado: pendiente)

## riesgos
- r1: infra o sobrepresupuestar penaliza la viabilidad (criterio 1.2) [aei_conv2026]

## decisiones
- dp7: importe total y anualidades  (estado: pendiente_usuario_e_ip)

## proximo_paso
- rellenar importes con ofertas antes del 12-11-2026

## referencias
- [aei_conv2026] AEI (2026). Resolución de 30-09-2026 de la Presidencia de la AEI por la que se aprueba la convocatoria de tramitación anticipada para el año 2026 de ayudas a «Proyectos de Generación de Conocimiento» y actuaciones para formación de personal investigador predoctoral (texto completo firmado, CSV GEN-bdee-fb5c-cbfb-ddaa-67eb-2c3c-e925-db73). https://www.aei.gob.es/sites/default/files/convocatory_info/file/2026-10/Convocatoria_ProyectosGeneraci%C3%B3nConocimiento_Predoc_2026_fda.pdf
- [gcamejo2023] González-Camejo J, et al. (2023). Feasibility of Rapid Gravity Filtration and Membrane Ultrafiltration for the Removal of Microplastics and Microlitter in Sewage and Wastewater from Plastic Industry. J. Water Process Eng. 51:103452. https://doi.org/10.1016/j.jwpe.2022.103452
- [reusemp3] Portal de Recerca UdG. Proyecto ReUseMP3, MCIU, 01-09-2021 a 31-08-2024, 210.830,40 €. https://recerca.udg.edu/ca/projects/integrating-nature-inspired-water-reuse-strategies-with-advanced--4/
