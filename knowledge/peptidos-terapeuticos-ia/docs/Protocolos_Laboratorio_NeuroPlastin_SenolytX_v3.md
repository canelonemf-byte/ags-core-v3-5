> Texto extraído automáticamente del PDF original «Protocolos_Laboratorio_NeuroPlastin_SenolytX_v3.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1_G8v6sgpqQAnYZ7_gyyW3M0wRT3-hsU9/view?usp=drivesdk



Protocolos de Laboratorio v3.0 Péptidos Inteligentes  Realizables

PROTOCOLOS DE LABORATORIO
NeuroPlastin v3 y Senolyt-X v3

Versión práctica y ejecutable  Agosto 2026

Complemento al Dossier PEPT-INTELIGENTES-2026-003
 Autor: Lázaro López Paz

1 Lista de Compra Exacta (Escala 0.1 mmol / 5080 mg péptido
puro)

1.1 Reactivos comunes

‹ Resina Rink Amide MBHA (0.40.6 mmol/g)  1 g (Iris Biotech / Merck / Chem-Impex)

‹ Fmoc-AA estándar (Arg(Pbf), Lys(Boc), Gly, Ser(tBu), etc.)  5 g cada uno necesario

‹ HATU o DIC + OxymaPure

‹ DIPEA, Piperidina, DMF, DCM, TFA, TIS, éter dietílico

‹ Columnas HPLC C18 preparativas y analíticas

1.2 Especí˝cos NeuroPlastin v3

‹ Phenylalanine-4'-azobenzene HCl (AzoF)  Sigma-Aldrich 914584-100MG (100 mg, ≈ 300370
EUR / $370). CAS 2137036-84-9. Se recomienda Fmoc-protegerlo o pedir Fmoc-AzoF custom si el
proveedor lo ofrece.

‹ Fmoc-Tyr, Fmoc-Arg(Pbf), Fmoc-Lys(Boc), Fmoc-Gly, Fmoc-Ser(tBu), Fmoc-Leu, etc. (los del
motivo Tat + core)

‹ mPEG-maleimide 2 kDa o 5 kDa (Thermo / Iris Biotech / Creative PEGWorks)  100500 mg

1.3 Especí˝cos Senolyt-X v3 (versión simpli˝cada)

‹ Mismos Fmoc-AA + opcionalmente un segundo AzoF o Fmoc-Lys(N3) para click posterior si se
desea foto-control.

‹ Motivo CPP + secuencia corta de interacción FOXO4-p53 optimizada (se proporciona abajo).

Coste total estimado por péptido (materiales + HPLC): 1.200  2.800 EUR (incluyendo
AzoF).

2 Secuencias Prácticas Recomendadas

NeuroPlastin v3 (prioridad máxima):
Ac-YGRKKRRQRRR-GSG-GRK(azoF)RLYSSG-NH 2

(Alternativa más corta si se quiere reducir coste: Ac-GRK(azoF)RLYSSG-NH 2 + CPP por separado
o conjugado). Senolyt-X v3 (versión lineal simpli˝cada para inicio):
Ac-(azoF o K)-FRGKKRRQRRR-QSAR-PFFL-NH 2 o la versión de novo más corta validada computacionalmente.

Se recomienda empezar sin el warhead VHL completo y añadirlo en una segunda generación.
 1

Protocolos de Laboratorio v3.0 Péptidos Inteligentes  Realizables

3 Protocolo SPPS Detallado (0.1 mmol)

1. Hinchado de resina: 1 h en DMF.

2. Desprotección Fmoc: 20% piperidina/DMF, 2 × 7 min. Lavados DMF (5x).

3. Acoplamiento AA estándar: 4 eq Fmoc-AA + 3.95 eq HATU + 8 eq DIPEA en DMF, 60 min.
Kaiser test.

4. Acoplamiento AzoF: 5 eq AzoF (o Fmoc-AzoF) + 5 eq HATU + 10 eq DIPEA en NMP/DMF,
3 h. Doble acoplamiento si Kaiser positivo. Proteger de la luz.

5. Continuar la secuencia. Al ˝nal, desproteger Fmoc y acetilar si es necesario (Ac 2O/DIPEA).

6. Escisión: TFA/TIS/H 2O (95:2.5:2.5), 2 h a temperatura ambiente, proteger de la luz.

7. Precipitar en éter frío, centrifugar, lavar 2x.

8. Lio˝lizar.

9. Puri˝car por HPLC preparativa C18 (gradiente 560% ACN en 0.1% TFA).

10. Veri˝car pureza > 95% y masa exacta por MS.

4 Conjugación mPEG (opcional pero recomendada)

1. Disolver péptido (con Cys libre o añadida) a 12 mM en PBS pH 7.07.2.

2. Añadir 1.52.5 eq mPEG-maleimide.

3. Agitar 1.52 h a temperatura ambiente.

4. Veri˝car por HPLC y MS.

5. Puri˝car si es necesario (HPLC o precipitación).

5 Caracterización Fotoquímica (NeuroPlastin / Senolyt-X)

‹ Disolver a 2050 µM en PBS o agua.

‹ Espectro UV-Vis completo.

‹ Irradiar a 365 nm (LED o lámpara) durante 15 min y registrar cambio (trans → cis).

‹ Irradiar a 450530 nm y observar recuperación.

‹ Determinar vida media térmica del cis a 25 ° C y 37 ° C (seguir abs a λmax del trans).

6 Ensayos Celulares Prioritarios (Fase 1)

6.1 NeuroPlastin v3

‹ Líneas: cultivos neuronales primarios, o SH-SY5Y, o HEK293 transfectadas con GluA1 si se dispone.

‹ Tratamiento: 120 µM péptido ± iluminación controlada.

‹ Lecturas: viabilidad (MTT), internalización de AMPA (inmuno˛uorescencia GluA1 o biotinilación
de super˝cie), si es posible electro˝siología o calcium imaging.
 2

Protocolos de Laboratorio v3.0 Péptidos Inteligentes  Realizables

6.2 Senolyt-X v3

‹ Inducir senescencia en ˝broblastos (IMR-90 o WI-38) con doxorubicina (50100 nM, 24 h) o irradiación.

‹ Tratamiento 37 días con péptido ± luz.

‹ Lecturas: SA- β-galactosidasa, p16 INK4a / p21 por western o IF, caspase-3/7, viabilidad diferencial
senescentes vs proliferantes.

7 Cronograma Recomendado 10 semanas

‹ Semanas 12: Compra de reactivos + síntesis de NeuroPlastin v3 (y opcionalmente Senolyt-X).

‹ Semana 3: Puri˝cación HPLC + MS + caracterización fotoquímica.

‹ Semana 4: Conjugación mPEG (si se desea) + formulación en PBS estéril.

‹ Semanas 57: Ensayos de citotoxicidad + ensayos funcionales básicos.

‹ Semanas 810: Optimización de dosis, selectividad luz/pH, y preparación de informe + posible
solicitud de patente provisional.

8 Notas de Seguridad y Buenas Prácticas

‹ Trabajar con AzoF y péptidos fotoactivos protegiendo de la luz (papel de aluminio, luz roja tenue).

‹ TFA y piperidina: usar campana extractora.

‹ Todos los ensayos celulares bajo normas de bioseguridad del laboratorio.

‹ Guardar stocks de péptido lio˝lizado a −20 ° C o −80 ° C, protegidos de la luz y humedad.

Declaración

Estos protocolos están diseñados para ser ejecutados con equipamiento y reactivos estándar disponibles
en 2026. Se basan en prácticas habituales de síntesis de péptidos y ensayos de senescencia/plasticidad.
El autor principal es Lázaro López Paz.
 Fin de los Protocolos de Laboratorio
Listo para ejecución inmediata  Agosto 2026
 3
