# Prerregistro C-NANO-001 — Energías superficiales con potenciales universales: 10 metales × 3 facetas y TiO2 (anatasa/rutilo), tamaño de cruce y fonones Γ de losas
meta:
  id: C-NANO-001
  proyecto: omniscience
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-21 (Europe/Madrid)"
  licencia: "CC BY 4.0"
  registro_origen: "NANO-03, NANO-02, NANO-10, NANO-09 (evidence_register.csv)"
objetivo: "Medir con MatterSim (principal) y MACE-MP-0 medium (contraste) las energías superficiales relajadas de 10 metales y de 6 facetas de TiO2, contrastarlas con referencias DFT/calorimétricas verificadas, probar una corrección lineal de un parámetro fuera de muestra y estimar el diámetro de cruce anatasa→rutilo."
datos_clave:
  codigo: "code/nano_run.py (sha256 en code_freeze.sha256)"
  potenciales: "MatterSim-v1.0.0-5M (venv_ms) y MACE-MP-0 medium float64 (venv_mace); CPU; semilla 0"
  metales: "Ag, Al, Au, Cu, Ni, Pd, Pt (fcc: 111, 100, 110) y Fe, Mo, W (bcc: 110, 100, 111). Red relajada por cada potencial. Losas 1×1, vacío total 15 Å, todos los átomos relajados (BFGS fmax 0.01 eV/Å, ≤600 pasos). Capas run1: fcc 9, bcc110/100 9, bcc111 12; run2 (réplica): 13/13/13/18."
  gamma: "γ = (E_losa − n·e_bulk)/(2A) en J/m². γ̄ = media ponderada por área de Wulff sobre las 3 facetas calculadas (pymatgen WulffShape)."
  referencia_metales: "γ̄ ponderada de Wulff PBE de Tran et al. 2016 (https://doi.org/10.1038/sdata.2016.80), leída del campo weighted_surface_energy de Materials Project (colección pública summary 2025-09-25). refs/refs_gamma_metales.json: Ag 0.7856, Al 0.7968, Au 0.7490, Cu 1.4219, Fe 2.5269, Mo 2.9108, Ni 2.0354, Pd 1.4505, Pt 1.5955, W 3.3450 J/m²."
  tio2: "Celdas: rutilo COD 9007531 (https://doi.org/10.1107/S0567740871005466), anatasa COD 9015929 (https://doi.org/10.1107/S010876819100335X); relajación completa por cada potencial. Losas pymatgen SlabGenerator: rutilo (110),(100),(101); anatasa (101),(001),(100); espesor mínimo 12 Å (run1) / 18 Å (run2), vacío 15 Å; solo terminaciones simétricas, estequiométricas y no polares (máx. 3); se toma la de menor γ tras relajar (fmax 0.02, ≤800 pasos)."
  referencias_tio2: "PBE (Lazzeri, Vittadini, Selloni, erratum https://doi.org/10.1103/PhysRevB.65.119901 a https://doi.org/10.1103/PhysRevB.63.155409): anatasa(101) 0.44 J/m², rutilo(110) 0.31 J/m². Calorimetría (https://doi.org/10.1073/pnas.251534898): entalpía superficial rutilo 2.2, anatasa 0.4 J/m² (valores de NANO-10). ΔH_bulk(A−R) experimental +9.0 meV/át = +27.0 meV/TiO2 (referencia de C-UMF-004, misma DOI de calorimetría)."
  cruce: "d* = 6(γ̄_R·V_R − γ̄_A·V_A)/ΔH_bulk con V por fórmula del potencial y ΔH_bulk = 27.0 meV/TiO2 (esfera; anatasa estable para d < d*)."
  gamma_slab: "NANO-09: ase.vibrations, desplazamiento 0.01 Å, diferencias centrales, losa completa de rutilo(110) y anatasa(101) de run1 MatterSim; ν en THz, imaginarias con signo negativo."
  control_gpaw: "GPAW PBE PW 400 eV, FermiDirac 0.05 eV, punto único en la geometría MatterSim run1 de anatasa(101) y en el bulk de anatasa MatterSim (malla k ≈ 0.25 Å⁻¹ de densidad, kz=1 en losa). γ_PBE@geomMS. Si GPAW no termina antes de 2026-10-22 08:00 (UTC+2), C1 = NO EVALUABLE."
  humo_previo_declarado: "Antes de congelar se ejecutaron humos de tiempo (smoke/): MatterSim Cu(111) 9 capas γ = 1.254 J/m²; W(111) 12 capas 3.513 J/m²; anatasa(101) 12 Å γ = 0.471 J/m² (terminación 1). Por tanto H4 se conoce parcialmente de antemano; se declara."
hipotesis:
  H1: "NANO-03a. MatterSim subestima: γ̄_MS < γ̄_ref en ≥ 8 de 10 metales."
  H2: "NANO-03b. Ajuste γ_ref = a·γ̄_MS (mínimos cuadrados por el origen) en Ag, Al, Au, Cu, Fe (orden alfabético, fijado antes de calcular); PASA si MAE en Mo, Ni, Pd, Pt, W < 0.10 J/m² Y 1.05 ≤ a ≤ 1.5."
  H3: "Contraste MACE: mismas H1 y H2 con MACE (informativas; no cambian el nivel)."
  H4: "NANO-02a. γ_MS anatasa(101) ∈ [0.308, 0.572] J/m² (±30 % de 0.44)."
  H5: "NANO-02b. d* (MatterSim) ∈ [5, 40] nm."
  H6: "NANO-10. Δγ̄ = γ̄_R − γ̄_A (MatterSim) > 0 y ∈ [0.9, 2.7] J/m² (±50 % de 1.8)."
  H7: "NANO-09. Ningún modo < −0.3 THz en Γ en las losas MatterSim de rutilo(110) y anatasa(101)."
  H_REP: "Réplica run2 (losas más gruesas, MatterSim): |γ_run2 − γ_run1| ≤ 0.05 J/m² en ≥ 90 % de las 36 losas y los veredictos de H1, H2, H4, H5, H6 no cambian."
controles:
  C1: "GPAW: |γ_MS − γ_PBE@geomMS| / γ_PBE@geomMS ≤ 0.30 para anatasa(101)."
  C2: "Todas las relajaciones convergen (relax_ok); las que no, se informan y cuentan como no evaluables."
regla_nivel_E: "E3 si H_REP PASA y C1 PASA (simulación verificada, sea cual sea el veredicto de las hipótesis); E2 si H_REP PASA y C1 falla o no es evaluable; E1 si H_REP FALLA."
tareas: ["congelar", "run1 MatterSim", "run1 MACE", "run2 MatterSim", "GPAW control", "evaluación tal cual", "figura", "registro + LoRA"]
riesgos: ["Referencia ponderada de Tran incluye facetas de mayor índice; γ̄ propia solo usa 3 facetas (sesgo hacia arriba esperable de γ̄ propia; se declara, no se corrige)", "Fe magnético: los potenciales no tratan espín explícito", "Losas 1×1 impiden reconstrucciones"]
decisiones: ["Dryad (descarga directa) bloqueado (401/403): se usa el valor ponderado de Materials Project; no hay γ por faceta de referencia, por eso H2 usa γ̄ en lugar de γ por faceta (cambio respecto a la ficha NANO-03, declarado antes de calcular)", "La referencia DFT de anatasa(101) es Lazzeri 2002 erratum (0.44)"]
proximo_paso: "Ejecutar run1 MatterSim y MACE, run2 MatterSim y control GPAW en segundo plano; evaluar con code/nano_eval.py congelado."
