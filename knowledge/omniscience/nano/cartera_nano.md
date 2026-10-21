# Cartera nano OMNISCIENCE

Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963 · 2026-10-21 09:25 Europe/Madrid

## objetivo
Especialización en nanotecnología: llevar resultados Universal Matter/Phonon (UM-16..UM-22) a escala nano con hipótesis falsables

## datos_clave
### NANO-01 · Entropía vibracional de nanopartículas (E1)
- afirmacion: La entropía vibracional por átomo de nanopartículas de Cu, Ag, Au y MgO calculada con MatterSim/phonopy (modos de superficie blandos) excede la del sólido masivo con un exceso ΔS(298 K) que escala linealmente con la fracción de átomos de superficie (R² ≥ 0.9) para diámetros 1.5–4 nm
- criterio_falsacion: R² < 0.9 en el ajuste ΔS frente a fracción superficial, o ΔS(298) < 0 en algún tamaño ≥ 2 nm
- simulacion: MatterSim (UM-19, E3 en sólidos masivos) + phonopy en clústeres aislados (caja de vacío ≥ 12 Å, sin q), 4 tamaños por material; control MACE-MP-0; control DFT GPAW de un clúster Cu55
- doi: https://doi.org/10.1016/j.pmatsci.2009.05.002 ; https://doi.org/10.1016/j.scriptamat.2015.07.021 ; https://doi.org/10.48550/arXiv.2405.04967
- originalidad: Parcialmente publicado: el exceso de entropía vibracional en nanocristales se conoce (revisión de Fultz). No hallado: prueba prerregistrada con potenciales universales frente a una ley de escala fijada de antemano

### NANO-02 · Cruce de tamaño anatasa/rutilo (E1)
- afirmacion: Con E_bulk(A−R) tomado del experimento (+9 meV/át, UM-18/UM-22 muestran que MatterSim y DFT invierten el signo) y energías de superficie de MatterSim, el diámetro de cruce anatasa→rutilo predicho cae en 5–40 nm
- criterio_falsacion: Diámetro de cruce fuera de 5–40 nm o energía superficial anatasa(101) MatterSim fuera de ±30 % de la referencia DFT publicada
- simulacion: MatterSim y MACE: losas TiO2 rutilo (110),(100),(101) y anatasa (101),(001),(100), 6–10 capas; construcción de Wulff propia; modelo termodinámico ΔG(d)=ΔH_bulk+ (6/d)Δγ·V_m; control GPAW PBE de anatasa(101)
- doi: https://doi.org/10.1073/pnas.251534898 ; https://doi.org/10.1039/a802619j ; https://doi.org/10.1103/PhysRevB.70.235403 ; https://doi.org/10.1103/PhysRevB.63.155409
- originalidad: Mayormente publicado (Zhang–Banfield 1998; Barnard 2004 con DFT). Nuevo solo: separar error bulk (conocido en este proyecto) de error de superficie con potenciales universales, prerregistrado

### NANO-03 · Energías de superficie con potenciales universales (E1)
- afirmacion: MatterSim subestima las energías superficiales de elementos metálicos (Cu, Ag, Au, Al, Ni, Pt, Pd, W, Mo, Fe) de forma sistemática; una corrección lineal única γ_corr=a·γ_ML ajustada en 5 elementos reduce el MAE fuera de muestra por debajo de 0.10 J/m²
- criterio_falsacion: MAE fuera de muestra con corrección ≥ 0.10 J/m² o pendiente a fuera de 1.05–1.5
- simulacion: MatterSim/MACE: losas (111),(100),(110) relajadas; referencia DFT del conjunto de Tran et al.; partición 5/5 fijada por orden alfabético antes de calcular
- doi: https://doi.org/10.1038/sdata.2016.80 ; https://doi.org/10.1038/s41524-024-01500-6 ; https://doi.org/10.1021/acsami.4c03815
- originalidad: El ablandamiento sistemático ya está publicado (Deng et al., Focassio et al.). Nuevo: corrección de un parámetro prerregistrada y evaluada fuera de muestra para MatterSim

### NANO-04 · Fonones de materiales 2D (E1)
- afirmacion: Las frecuencias ZA/TA/LA y de modos ópticos en Γ de grafeno, h-BN y MoS2 monocapa con MatterSim quedan dentro de ±5 % de referencias DFT/experimentales publicadas, y la dispersión ZA es cuadrática (ω∝q², exponente 1.8–2.2) cerca de Γ tras aplicar la regla de suma rotacional
- criterio_falsacion: Más de 2 de 9 frecuencias fuera de ±5 % o exponente ZA fuera de 1.8–2.2
- simulacion: MatterSim + phonopy, supercelda 6×6×1, vacío 20 Å; control MACE-MP-0; control GPAW PBE para grafeno en Γ
- doi: https://doi.org/10.1103/PhysRevB.71.205214 ; https://doi.org/10.1103/PhysRevB.84.155413 ; https://doi.org/10.1038/s41524-025-01650-1
- originalidad: Benchmarks de fonones con potenciales universales existen para sólidos masivos; no hallé uno prerregistrado centrado en el modo ZA de monocapas. Originalidad parcial

### NANO-05 · Entropía de monocapas frente a masivo (E0)
- afirmacion: La entropía vibracional S(298) por átomo de MoS2, h-BN y grafeno monocapa excede la del masivo en 0.05–0.6 k_B/át, y D3 (UM-20) en el masivo cambia esa diferencia menos de 0.1 k_B/át
- criterio_falsacion: ΔS(mono−masivo) fuera de 0.05–0.6 k_B/át en alguno, o efecto D3 ≥ 0.1 k_B/át
- simulacion: MatterSim(+D3 para masivo) + phonopy; mismas mallas de q; réplica con semilla y malla distintas
- doi: https://doi.org/10.1103/PhysRevB.71.205214 ; https://doi.org/10.1103/PhysRevB.84.155413 ; https://doi.org/10.1063/1.3382344
- originalidad: Cálculos individuales existen en la literatura; la prueba comparativa con D3 es propia. Originalidad parcial

### NANO-06 · Energía de exfoliación de haluros en capas (E1)
- afirmacion: MatterSim+D3 (UM-20 corrige volúmenes de MgCl2, CaI2, MgBr2 a <1.1 %) reproduce energías de exfoliación de compuestos en capas dentro de ±25 % frente a la referencia vdW-DF/RPA publicada
- criterio_falsacion: Más de 1 de 6 compuestos (grafito, h-BN, MoS2, MgCl2, CaI2, MgBr2) fuera de ±25 %
- simulacion: MatterSim+D3(BJ): E_exf = (E_mono − E_bulk/n)/A; compara con cálculos de alta jerarquía publicados
- doi: https://doi.org/10.1103/PhysRevLett.108.235502 ; https://doi.org/10.1038/s41565-017-0035-5 ; https://doi.org/10.1063/1.3382344
- originalidad: Energías de exfoliación DFT publicadas a gran escala (Mounet 2018, Björkman 2012). Nuevo: test con potencial universal+D3 heredado de UM-20

### NANO-07 · Conductividad térmica de nanohilos de Si (E0)
- afirmacion: La conductividad térmica de nanohilos de Si de 2–5 nm calculada con MatterSim (dinámica molecular de no equilibrio) disminuye con el diámetro y, extrapolada, queda dentro de un factor 2 de medidas en nanohilos de 22–115 nm
- criterio_falsacion: Tendencia no monótona o desacuerdo > factor 2 con la medida
- simulacion: MatterSim NEMD (ASE), longitudes 10–40 nm; control de convergencia en longitud; coste alto
- doi: https://doi.org/10.1063/1.1616981
- originalidad: Ampliamente estudiado con potenciales clásicos. Bajo grado de novedad; solo como test de transferencia

### NANO-08 · Conductividad térmica de grafeno con potencial universal (E0)
- afirmacion: κ de grafeno monocapa calculado con MatterSim (BTE con fuerzas de tercer orden) queda en el rango experimental 2000–5300 W/m·K
- criterio_falsacion: κ(300 K) fuera de 2000–5300 W/m·K
- simulacion: MatterSim + phono3py (no instalado: requiere instalación) supercelda 5×5×1; control MACE
- doi: https://doi.org/10.1021/nl0731872 ; https://doi.org/10.1016/j.scriptamat.2015.07.021
- originalidad: κ de grafeno con potenciales ML ya se ha estudiado; benchmark Matbench incluye κ de sólidos. Originalidad baja

### NANO-09 · Estabilidad dinámica de superficies (E0)
- afirmacion: Las losas de TiO2 rutilo(110) y anatasa(101) relajadas con MatterSim no muestran modos imaginarios <−0.3 THz en Γ, al contrario que el rutilo masivo fuera de volumen experimental (UM-16)
- criterio_falsacion: Algún modo < −0.3 THz en Γ en las losas relajadas
- simulacion: MatterSim + phonopy en Γ de losas 6 capas; control MACE; control GPAW Γ-only en anatasa(101) 4 capas
- doi: https://doi.org/10.1103/PhysRevB.63.155409 ; https://doi.org/10.1016/j.scriptamat.2015.07.021
- originalidad: No hallé prueba prerregistrada con potenciales universales; conexión con UM-16 propia

### NANO-10 · Entalpía de superficie de nanopolvos por calorimetría (E1)
- afirmacion: La diferencia de entalpía superficial anatasa−rutilo derivada de MatterSim (γ con Wulff) reproduce el signo y está dentro de ±50 % de la diferencia calorimétrica publicada (rutilo 2.2, anatasa 0.4 J/m²)
- criterio_falsacion: Signo erróneo o fuera de ±50 %
- simulacion: Mismas losas que NANO-02; reutiliza su cálculo (coste marginal cero)
- doi: https://doi.org/10.1073/pnas.251534898 ; https://doi.org/10.1021/acsami.4c03815
- originalidad: Comparaciones DFT–calorimetría publicadas; con potencial universal prerregistrado no hallado

## tareas
- prerregistrar C-NANO-001
- congelar código antes de calcular
- instalar phono3py solo si se aprueba NANO-08

## riesgos
- ablandamiento sistemático de potenciales universales en superficies
- orden bulk TiO2 invertido (UM-22): NANO-02 usa ΔH_bulk experimental
- ninguna hipótesis es totalmente nueva

## decisiones
- nivel máximo E1: no se ha ejecutado ningún cálculo
- sin escritura en repositorios, sin entrenar ni publicar

## proximo_paso
{"campana": "C-NANO-001", "base": ["NANO-03", "NANO-02", "NANO-10"], "alcance": "10 metales × 3 facetas (NANO-03) + 6 losas TiO2 (NANO-02/10) con MatterSim y MACE, 1 control GPAW anatasa(101)", "coste_estimado": "MatterSim/MACE: ~2–4 h CPU; control GPAW: ~6–10 h en segundo plano", "razon": "reutiliza pipeline y datos de UM-18/UM-22; criterios numéricos con referencias DFT/calorimétricas; E2 alcanzable con prerregistro, E3 con réplica y control"}
