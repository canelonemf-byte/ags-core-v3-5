# Prerregistro C-UMF-001 — Entalpías de formación con potenciales universales (MatterSim, MACE) frente a NIST-JANAF ΔfH°(0 K)

meta:
  campana: C-UMF-001
  modulo: Universal Matter (UM-02, UM-07)
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha: 2026-10-20
  estado: congelado antes de cualquier cálculo del estudio (el hash de este archivo se guarda en prereg_C-UMF-001.sha256)

## objetivo
Añadir el paso E_form que falta en el flujo MV1 (UM-07) y comprobar si las energías de dos potenciales universales (uMLIP) entrenados con PBE/MPtrj dan entalpías de formación experimentales: (a) en bruto, (b) con las correcciones aniónicas fijas de Materials Project 2020 (MP2020) y (c) con correcciones por anión reajustadas con validación cruzada dejando uno fuera (LOOCV).

## datos_clave
- Referencia experimental: ΔfH°(0 K) de las tablas NIST-JANAF 4.ª ed. (Chase 1998, https://janaf.nist.gov), ya descargadas con hash en campañas previas. Conversión: kJ/mol de fórmula / 96.4853 / n_átomos → eV/átomo. Se informa también 298.15 K de forma descriptiva.
- Compuestos (28 + AlN = 29, lista fija): óxidos MgO, CaO, SrO, BeO, Al2O3, Li2O, Na2O, SiO2 (cuarzo-α), TiO2 (rutilo), ZrO2 (monoclínico), MgAl2O4, BeAl2O4, MgTiO3, ZrSiO4; fluoruros LiF, NaF, KF, CaF2, SrF2, BaF2, MgF2; cloruros NaCl, KCl, LiCl, CsCl; bromuros KBr, NaBr; yoduro KI; nitruro AlN. Excluidos a priori: SiC (referencia de carbono grafito con vdW), K2O (sin ΔfH a 0 K), MgCl2 y Mg2SiO4 (sin estructura preparada).
- Estructuras iniciales: las mismas funciones de C-MAT-004/C-MAT-005 (celdas experimentales); relajación completa con simetría fija (FixSymmetry + FrechetCellFilter, BFGS, fmax 1e-3 eV/Å, ≤3000 pasos), float64, CPU, 4 hilos, semilla 0.
- Referencias elementales: metales y Si en su fase de ASE por defecto (Mg, Be, Ti, Zr hcp; Al, Ca, Sr fcc; Li, Na, K, Cs, Ba bcc; Si diamante), relajadas igual. O2, N2, F2, Cl2, Br2, I2 como moléculas aisladas en caja cúbica de 20 Å (relajación de posiciones). Sin espín (los uMLIP no lo modelan).
- Modelos: MatterSim-v1.0.0-5M (principal) y MACE-MP-0 medium (línea base).
- Correcciones MP2020 (eV por átomo de anión): óxido −0.687, F −0.462, Cl −0.614, Br −0.534, I −0.379, N −0.361 (pymatgen v2024.6.10, MP2020Compatibility.yaml, sha256 90a5af21…6d9a; Wang et al. 2021, doi:10.1038/s41598-021-94550-5).
- LOOCV: para cada compuesto i se ajusta por mínimos cuadrados un δ_X por anión (O, F, Cl, Br) con los demás compuestos (error por átomo) y se predice i. I y N aparecen una sola vez → fuera de la LOOCV (n = 27).

## tareas (hipótesis y umbrales fijados ahora)
- H-F1 (bruto, MatterSim, óxidos con O2 molecular): error (pred − exp) positivo en ≥12/14 óxidos y media del error por átomo de O en [0.40, 1.00] eV.
- H-F2: MAE LOOCV de MatterSim ≤ 60 meV/átomo (n = 27).
- H-F3: |error| máximo LOOCV de MatterSim ≤ 150 meV/átomo.
- H-F4: MAE LOOCV MatterSim ≤ MAE LOOCV MACE.
- H-F5: δ_O, δ_F y δ_Cl ajustados con todos los datos (MatterSim) a ≤0.15 eV/átomo de los valores MP2020 (los tres).
- H-F6: MatterSim + MP2020 fijo (sin ajuste) MAE ≤ 80 meV/átomo en los 26 compuestos de O, F, Cl y N (Br y I, solo descriptivo: su referencia de 0 K es sólida y aquí se usa molécula).
- H-F7: Spearman ρ(pred LOOCV, exp) ≥ 0.95 (MatterSim, n = 27).
- H-REP: segunda ejecución completa; diferencia relativa de cada energía total ≤ 1e-6 en ambos modelos.
- Controles: C1 todas las relajaciones convergen; C2 volumen relajado de cada compuesto a ±8 % del inicial (descriptivo, marca patologías); C3 MatterSim da Mg hcp por debajo de Mg fcc.

## riesgos
- Se desprecia la energía de punto cero (incertidumbre sistemática estimada ≤0.03 eV/átomo; en parte la absorbe δ_X).
- Moléculas aisladas fuera del dominio de entrenamiento de los uMLIP; O2 sin triplete.
- Incertidumbre JANAF típica 0.01–0.02 eV/átomo.
- Li y Na: la fase de 0 K real no es bcc (error de pocos meV/átomo).

## decisiones
- El veredicto se da con los criterios de arriba aunque fallen; cualquier desviación se declara como D1, D2…
- Nivel E: la nueva fila queda en E2 si falla algún criterio principal (H-F2, H-F6); E3 solo si H-F2, H-F3, H-F6 y H-REP pasan.

## proximo_paso
Ejecutar run1 y run2, evaluar y actualizar el registro de evidencia.
