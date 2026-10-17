> Texto extraído automáticamente del PDF original «Dossier_Peptidos_Inteligentes_v3_Realizable_Laboratorio.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1vqlLPt-ySDgcRZqbX89hEdaGiktTko4-/view?usp=drivesdk



Dossier v3.0  Realizable en Laboratorio Péptidos Inteligentes

0.0.4em DOSSIER TÉCNICO INTEGRADO

Péptidos Inteligentes de Nueva Generación para la Mejora Humana

Versión 3.0  Realizable en cualquier laboratorio estándar
 5 de agosto de 2026

ID: PEPT-INTELIGENTES-2026-003

Autor principal: Lázaro López Paz
(Asistencia técnica de investigación y rediseño de viabilidad)

Resumen Ejecutivo y Declaración de Viabilidad

Esta versión 3.0 es el resultado de una revisión crítica de viabilidad real a fecha de agosto de
2026. Se han eliminado o simpli˝cado todos los elementos que requieren equipamiento o expertise
no habituales (RAFT custom de pSB, DNA origami completo con AFM, múltiples ncAAs poco
comerciales, ciclaciones complejas de bajo rendimiento).
Resultado: Todos los péptidos y protocolos aquí descritos pueden ejecutarse hoy en un laboratorio
universitario o de CRO que disponga de:

‹ Sintetizador de péptidos (automático o manual) + HPLC preparativa/analítica + MS.

‹ Cultivo celular básico y espectrofotómetro UV-Vis.

‹ LEDs o lámparas UV/visible de longitudes de onda estándar (365 nm y 450660 nm).

‹ Reactivos comerciales de proveedores habituales (Sigma, Iris Biotech, Merck, Thermo, Bachem,
etc.).
 Se priorizan aplicaciones terapéuticas (senescencia, recuperación cardíaca, sarcopenia, neuroprotección)
sobre la mejora puramente electiva.

1 Matriz de Viabilidad 2026

Elemento Viabilidad Acción en v3.0

SPPS péptidos 1020 aa Alta Protocolos detallados
AzoF comercial (Sigma) Media-Alta Usado como ncAA principal
azoLys / azoPro Baja Limitado o sustituido
Ciclación lactama +
Statina Media Versión disulfuro o lineal prioritaria

pSB por RAFT Baja Sustituido por mPEG-maleimide comercial
DNA origami completo Baja Opcional; sustituido por CPP + PEG + aplicación local
Ensayos celulares básicos Alta Protocolos con líneas estándar

2 Plataforma Práctica (Laboratorio Estándar)

2.1 Síntesis en Fase Sólida (SPPS)  Protocolo Genérico Realizable

Escala recomendada: 0.050.1 mmol (obtiene 2080 mg de péptido puro tras HPLC).

1. Resina: Rink Amide MBHA o equivalente (carga 0.30.7 mmol/g).

2. Desprotección Fmoc: 20% piperidina en DMF (2 × 510 min). Control UV 301 nm.

3. Acoplamiento AA estándar: 4 eq Fmoc-AA + 4 eq HATU (o DIC/Oxyma) + 8 eq DIPEA, 4560
min, DMF.

4. Para AzoF (comercial): 5 eq, 23 h, doble acoplamiento si Kaiser positivo. Disolver en NMP si es
necesario.

5. Lavados: DMF, DCM.

6. Escisión: TFA/TIS/H 2O (95:2.5:2.5) o con DODT, 2 h, precipitación en éter frío.

7. Puri˝cación: HPLC C18 (gradiente ACN/H 2O + 0.1% TFA). Pureza objetivo > 95%.

1

Dossier v3.0  Realizable en Laboratorio Péptidos Inteligentes

8. Caracterización: HPLC analítica + MS (ESI o MALDI).

Fuentes comerciales clave:

‹ Fmoc-AAs estándar: Iris Biotech, Merck, Bachem, Chem-Impex, Carl Roth.

‹ Phenylalanine-4-azobenzene HCl (AzoF): Sigma-Aldrich (CAS 2137036-84-9), ≈ 250370 EUR /
100 mg. Se puede Fmoc-proteger o pedir custom.

‹ mPEG-maleimide (210 kDa): Thermo Fisher, Creative PEGWorks, Iris Biotech.

‹ Resinas y reactivos de acoplamiento: proveedores habituales de química de péptidos.

2.2 Conjugación y Vectorización Accesible

‹ Motivos CPP (Tat o fragmentos) ya incluidos en las secuencias prioritarias.

‹ Conjugación tiol-maleimida con mPEG comercial (péptido con Cys libre + mPEG-maleimide, PBS
pH 7.07.4, 12 h, > 8590% rendimiento típico).

‹ Alternativas: liposomas o nanopartículas PLGA comerciales (kits), o aplicación local directa (parche,
inyección subcutánea/intratecal controlada, LED).

‹ DNA origami se deja como opción avanzada para grupos especializados; no es requisito.

2.3 Foto-control

Usar LEDs comerciales de 365 nm (trans →cis) y 450530 nm o rojo (cis →trans). Intensidades de
520 mW/cm 2 son su˝cientes para ensayos in vitro. Vida media del isómero cis de AzoF a 37 ° C suele
estar en el rango de horas.

3 Portfolio Práctico v3.0

3.1 NeuroPlastin v3 (Prioridad Alta  Muy Realizable)

Secuencia recomendada: Ac-YGRKKRRQRRR-GSG-GRK(azoF)RLYSSG-NH 2 o versión más
corta sin todo el Tat si se pre˝ere.

Objetivo: Estabilización de AMPA (GluA1) foto-controlada.

Síntesis: AzoF comercial + SPPS estándar.

Ensayo inicial: Cultivos neuronales o HEK expresando GluA1; fotoisomerización + medidas de
internalización o corrientes (si hay electro˝siología). Aplicación local + LED.

3.2 MitoGuard v3

Secuencia simpli˝cada centrada en el dominio de unión a PHB2 + linker + warhead accesible
(pomalidomida o análogos comerciales si se dispone). Priorizar primero la unión y penetración celular.
Ensayos: potencial de membrana mitocondrial (TMRE/JC-1) y marcadores de mitofagia en células
con estrés mitocondrial.
 2

Dossier v3.0  Realizable en Laboratorio Péptidos Inteligentes

3.3 Senolyt-X v3 (Prioridad Alta)

Versión foto-controlada o no-foto inicial. Secuencia más corta basada en motivos de interacción
FOXO4-p53 de novo o optimizados + CPP. Ensayos estándar de senescencia: SA- β-gal, p16/p21,
apoptosis selectiva en ˝broblastos senescentes vs proliferantes (inducción por doxorubicina o irradiación).

3.4 ImmuSynth v3 (Muy Realizable)

Secuencia con octahistidina + mimético PD-L1 corto. Todo con AA estándar. Ensayo: unión a PD-1
recombinante (ELISA o SPR si disponible) a pH 7.4 vs 6.06.5; reactivación de células T en co-cultivo.

3.5 MyoFlex v3

Prioridad 1: Versión lineal optimizada o cíclica por puente disulfuro (dos Cys).

Prioridad 2 (avanzada): Lactama con estatina si se consigue el building block.

Ensayos: inhibición de señalización Smad en C2C12 o reporter luciferase; hipertro˝a de miotubos.

3.6 CardioRegen v3

Secuencia corta con AzoF o azoPro (si disponible) + motivo de unión a SAV1. Aplicación local +
LED. Ensayos: proliferación de H9c2 o cardiomiocitos derivados de iPSC (si el lab tiene acceso);
marcadores de ciclo celular y YAP nuclear.

4 Planes Experimentales Prioritarios (Ejecutables Hoy)

Fase 1 (48 semanas por péptido prioritario):

1. Síntesis 50100 mg escala + puri˝cación + MS/HPLC.

2. Caracterización fotoquímica (UV-Vis, ratio cis/trans, vida media térmica).

3. Estabilidad en suero o medio de cultivo (HPLC).

4. Citotoxicidad básica (MTT/XTT) en 23 líneas celulares.

Fase 2:

‹ Ensayos de unión o funcionales especí˝cos (ELISA, ˛uorescence polarization, reporter assays).

‹ Selectividad (senescentes vs normales; pH 7.4 vs 6.2; luz vs oscuridad).

‹ Formulación simple (PBS, mPEG-conjugado, o gel de HA).

Prioridad recomendada de inicio: NeuroPlastin v3 (AzoF comercial claro) + Senolyt-X v3
(ensayos de senescencia muy estandarizados) + ImmuSynth v3 (todo AA estándar).

5 Presupuesto Orientativo (Escala Académica)

‹ Aminoácidos estándar + resina + reactivos para un péptido: 200500 EUR.

‹ AzoF 100 mg: ≈ 300 EUR.

‹ Puri˝cación HPLC (si se externaliza parcialmente): 300700 EUR.

‹ mPEG-maleimide: 100300 EUR.

‹ Total por péptido prioritario hasta material puro listo para ensayo celular: 8002.500 EUR.
 3

Dossier v3.0  Realizable en Laboratorio Péptidos Inteligentes

6 Claims y Propiedad Intelectual (Borrador Práctico)

Se mantienen los claims de la v2 adaptados a las secuencias y formulaciones simpli˝cadas de la v3.0.
Se recomienda presentar solicitud provisional nacional (España) o EPO cubriendo:

1. Secuencias especí˝cas + ncAA foto-responsivo.

2. Conjugados con PEG.

3. Usos terapéuticos (senólisis, regeneración cardíaca, etc.).

4. Métodos de activación por luz o pH.

Declaración Final

El presente Dossier v3.0 ha sido diseñado expresamente para ser reproducible en laboratorios estándar
con los recursos habituales de 2026. Todas las recomendaciones de síntesis, reactivos y ensayos se
basan en componentes comerciales o protocolos publicados ampliamente accesibles. El autor principal
es Lázaro López Paz.
Documento listo para archivo, síntesis inmediata y desarrollo experimental.
 Fin del Dossier Técnico Integrado  Versión 3.0
Realizable en Laboratorio Estándar  5 de agosto de 2026
 4
