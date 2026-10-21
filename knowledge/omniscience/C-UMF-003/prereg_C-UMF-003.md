# Prerregistro C-UMF-003
meta:
  id: C-UMF-003
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)"
  fecha: 2026-10-20 (UTC+2)
  estado: congelado antes de cualquier cálculo (sha256 en prereg_C-UMF-003.sha256)
  origen: C-UMF-002 (UM-18): MatterSim/PBE ordenan anatasa por debajo de rutilo; MgCl2, CaI2, MgBr2 con volumen +11/+16/+20 %.
objetivo: "A) ¿Un método más allá de PBE (PBE+U o r2SCAN) ordena bien rutilo < anatasa? B) ¿Una corrección D3(BJ) sobre MatterSim corrige el volumen de los haluros en capas sin estropear sólidos densos?"
datos_clave:
  referencia_A: "ΔH(anatasa − rutilo) = +2.61 ± 0.41 kJ/mol TiO2 = +9.0 ± 1.4 meV/átomo (calorimetría; Ranade et al., PNAS 99, 6476, 2002, doi:10.1073/pnas.251534898, verificado en Crossref)"
  metodo_A:
    codigo: "GPAW 25.1.0, ondas planas 600 eV, FermiDirac 0.01 eV, kpts con gamma: rutilo 5x5x8 (celda de 6 át.), anatasa primitiva 6x6x6 (6 át.)"
    geometria: "experimental fija (sin relajar): rutilo a=4.594, c=2.959 Å, u=0.3048; anatasa a=3.785, c=9.514 Å, z=0.2081"
    metodos: {M1: PBE, M2: "PBE+U Dudarev, U_eff(Ti 3d) = 4.0 eV fijado a priori, sin ajustar", M3: "r2SCAN autoconsistente (libxc MGGA_X_R2SCAN+MGGA_C_R2SCAN) con datasets PAW de PBE"}
    magnitud: "ΔE_AR = E(anatasa)/6 − E(rutilo)/6 en meV/átomo; se compara con ΔH sin corrección vibracional (incertidumbre declarada, ya cubierta por la tolerancia)"
  metodo_B:
    modelo: "MatterSim-v1.0.0-5M (float64) igual que C-UMF-002, sin y con D3(BJ, parámetros PBE; torch-dftd 0.5.3), relajación completa FrechetCellFilter+BFGS, fmax 1e-3 eV/Å, máx. 3000 pasos"
    capas: [MgCl2, CaI2, MgBr2]
    controles_densos: [NaCl, KCl, MgO, CaF2, LiF, TiO2]
    V_exp: "volumen de la celda inicial (misma que C-UMF-001/002)"
    error: "ΔV/V = (V_rel − V_exp)/V_exp"
  refs: ["D3: doi:10.1063/1.3382344", "BJ: doi:10.1002/jcc.21759", "r2SCAN: doi:10.1021/acs.jpclett.0c02405", "DFT+U: doi:10.1103/PhysRevB.57.1505", "GPAW: doi:10.1063/5.0182685"]
hipotesis:
  H-A1: "CONTROL. PBE da ΔE_AR < 0 (reproduce el fallo conocido)."
  H-A2: "PRINCIPAL. r2SCAN da ΔE_AR > 0."
  H-A3: "PBE+U(4 eV) da ΔE_AR > 0."
  H-A4: "PRINCIPAL. Al menos uno de M2/M3 cumple |ΔE_AR − 9.0| ≤ 10 meV/átomo."
  H-A5: "r2SCAN cumple |ΔE_AR − 9.0| ≤ 10 meV/átomo."
  H-B1: "PRINCIPAL. Con D3, |ΔV/V| ≤ 5 % en los tres haluros en capas."
  H-B2: "Con D3, el |ΔV/V| medio de las capas baja al menos un 50 % respecto a sin D3."
  H-B3: "PRINCIPAL. Con D3, |ΔV/V| medio de los 6 densos ≤ 3 % y no más de 2 puntos peor que sin D3."
  H-REP: "Réplica: B repetida completa (run2); A: PBE y PBE+U repetidos con distinto nº de procesos MPI; |diferencia| ≤ 1 meV/átomo en ΔE_AR y ≤ 0.1 % en V; mismos veredictos."
criterios_E: "E3 si pasan H-A2, H-A4, H-B1, H-B3 y H-REP; E2 si pasa al menos una principal de cada parte o todas las de una parte; E1 en otro caso."
factibilidad:
  - "Tras congelar, una prueba de humo (una SCF PBE de rutilo) mide el tiempo; su energía no se usa."
  - "Si la parte A completa proyecta > 8 h con 3 procesos MPI, se reduce en este orden: kpts rutilo 4x4x6 y anatasa 5x5x5; después ecut 500 eV. Se declara como desviación."
  - "Si r2SCAN no converge en 300 iteraciones SCF, H-A2/H-A5 = NO EVALUABLE (no pasa)."
  - "Réplica r2SCAN solo si el tiempo lo permite (descriptiva)."
  - "No se para el trabajo DFT de C-MAT-006; esta campaña usa como máximo 3 procesos."
riesgos: ["datasets PAW de PBE con r2SCAN (inconsistencia conocida)", "D3 sumado a un potencial entrenado sin dispersión puede contraer de más los densos (eso mide H-B3)", "geometría fija experimental: mide la energía electrónica, no la relajada"]
decisiones: ["evaluación exacta según el texto", "desviaciones en sección aparte", "contenido original, citas solo por DOI"]
proximo_paso: "congelar y ejecutar"
