# Prerregistro C-NANO-003 — Exponente ZA robusto en 5 monocapas, Raman de WS2/MoSe2, contraste M/K del grafeno con IXS y D3 a 95 bohr
meta:
  id: C-NANO-003
  proyecto: omniscience
  autoria: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963"
  fecha: "2026-10-22/23 (Europe/Madrid)"
  licencia: "CC BY 4.0"
  origen: "Próximo paso de C-NANO-002 (H_REP falló solo por |Δn_ZA| h-BN = 0.104 > 0.10; H2 falló en M ZA). Registro: NANO-04 (E1), NANO-05 (E1)."
objetivo: "Comprobar con MatterSim si el exponente ZA es estable frente a la amplitud de desplazamiento, si las frecuencias Raman de WS2 y MoSe2 monocapa se reproducen, si las frecuencias M/K del grafeno concuerdan con IXS experimental de grafito, y si ΔS monocapa−masivo cambia al pasar el corte D3 de 40 a 95 bohr."
datos_clave:
  codigo: "code/nano3_run.py, code/base_nano2.py (copia de nano2_run.py de C-NANO-002 con dos cambios declarados: D3_CUT_BOHR = 95 y peso metálico Mo o W en caracter()), code/nano3_eval.py, code/gpaw_ws2.py, code/gpaw_c1.sh, code/guardia.py; sha256 en code_freeze.sha256"
  potencial: "MatterSim-v1.0.0-5M float64; D3(BJ, PBE) torch_dftd, corte 95 bohr, solo en masivos. CPU, 2 hilos."
  monocapas: "grafeno, h-BN, MoS2-1H, WS2-1H, MoSe2-1H; vacío 20 Å; relajación de a y posiciones (FixSymmetry); phonopy supercelda 6×6×1; solo regla de suma traslacional (no hay regla rotacional disponible en el entorno: hiphive no instalado; se sustituye por el ajuste ZA a 3 amplitudes, opción prevista)."
  ZA: "ν_ZA en Γ–M, q = (0.04…0.15)·|ΓM| (12 puntos), n = pendiente log-log, calculado a 3 amplitudes. run1: 0.005/0.010/0.015 Å; run2: 0.007/0.012/0.017 Å. n_med = mediana; dispersión = máx − mín."
  frecuencias: "Γ/M/K y entropías con la amplitud central (0.010 run1 / 0.012 run2). Asignación de modos idéntica a C-NANO-002; en MX2 el peso metálico es Mo o W."
  masivos: "grafito AB, h-BN AA', 2H-MoS2 con MatterSim+D3 a 95 bohr (superceldas 3×3×2, 3×3×2, 3×3×1; humo de memoria smoke/smoke_mem95.log: pico ~10.1 GB, solo tiempos/memoria, ninguna frecuencia)."
  entropia: "S_vib(298.15 K) con la regla R0–R4 (C-MAT-006). Mallas run1 48×48×1 / 24×24×8; run2 36×36×1 / 18×18×6."
  referencias_experimentales:
    WS2: "Berkdemir et al. 2013, https://doi.org/10.1038/srep01755: monocapa, λ = 488 nm, E' (E¹2g) 356 cm⁻¹ y A1' (A1g) 418 cm⁻¹ (texto del artículo)."
    MoSe2: "Soubelet et al. 2016, https://doi.org/10.1103/PhysRevB.93.155407 (arXiv 1603.05172): monocapa, 465 nm, A'1 242 cm⁻¹, E' 288 cm⁻¹ (texto)."
    IXS_grafito: "Mohr et al. 2007, https://doi.org/10.1103/PhysRevB.76.035439 (arXiv 0705.2418v1, pies de las figuras 7 y 8, valores IXS): K: K6 67.2, K2 124.9, K5 151.0 meV (K1 no resuelto); M: M3+ 60.0, M2− 77.8, M2+ 78.1, M4− 160.0, M1+ 166.2, M3− 173.4 meV. Conversión 1 meV = 8.065544 cm⁻¹."
    asignacion_IXS: "K6 (E'') → ZA y ZO de grafeno en K (degenerados); K2 → TA; K5 → LA/LO; M3+ → ZA; {M2−, M2+} → par {TA, ZO} comparado ordenado (diferencia 0.3 meV, la asignación individual no afecta); M4− → LA; M1+ → LO; M3− → TO. Grafito (IXS) frente a grafeno (cálculo): diferencia de sistema declarada como riesgo."
    S298_JANAF: "Chase 1998, https://doi.org/10.18434/T42S31: C(grafito) 5.740, BN(cr) 14.795 J/(K·mol)."
hipotesis:
  H1: "ZA robusto: en las 5 monocapas n_med ∈ [1.8, 2.2] y dispersión entre amplitudes ≤ 0.10."
  H2: "Raman WS2/MoSe2: E' y A1' de WS2 y MoSe2 (4 valores) dentro de ±5 % del experimento (4/4)."
  H3: "IXS: 10 frecuencias de grafeno en M/K (M ZA, M TA/ZO bajo, M TA/ZO alto, M LA, M LO, M TO, K ZA, K ZO, K TA, K LA/LO) dentro de ±5 % de IXS: PASA si ≤ 2 de 10 fuera. K TO solo informativo (no resuelto en IXS)."
  H4: "Corte D3: |ΔS(95 bohr) − ΔS(40 bohr, C-NANO-002 mismo run)| ≤ 0.02 k_B/át en las 3 parejas."
  H5: "ΔS(95) = S_mono − S_masivo(MS+D3-95) ∈ [0.05, 0.6] k_B/át en las 3 parejas."
  H_REP: "run2 vs run1: frecuencias de H2 (Γ de MoS2, WS2, MoSe2: A1', A2'', E'', E') y de M/K grafeno cambian ≤ 1 %; |Δn_med| ≤ 0.10 en las 5 monocapas; |ΔΔS(95)| ≤ 0.02 en las 3 parejas; veredictos H1–H5 iguales."
controles:
  C1: "GPAW PBE Γ de WS2 monocapa en la red MatterSim run1: E' y A1' MatterSim dentro de ±5 % de GPAW. Si GPAW no está disponible o no termina en 4 h: NO EVALUABLE."
  C2: "Consistencia: Γ de MoS2 (amplitud 0.010, run1) igual a C-NANO-002 run1 dentro de 0.5 % (mismo código base)."
  C3: "S298 masivo MS+D3-95 de grafito y h-BN dentro de ±10 % de NIST-JANAF."
regla_nivel_E:
  NANO_04: "E3 si H_REP PASA y C1 PASA; E2 si H_REP PASA y C1 falla o no evaluable; E1 si H_REP FALLA (sea cual sea H1–H3)."
  NANO_05: "E3 si H_REP PASA y C3 PASA; E2 si H_REP PASA y C3 falla; E1 si H_REP FALLA."
  filas_nuevas: "NANO-14 (H1), NANO-15 (H2), NANO-16 (H3), NANO-17 (H4/H5) heredan el nivel de NANO-04 (H1–H3) o NANO-05 (H4–H5) si su hipótesis PASA; si FALLA se registran como resultado negativo con el mismo nivel de verificación."
riesgos: ["Sin regla rotacional verdadera", "IXS de grafito vs grafeno calculado", "Raman experimental sobre sustrato y a 300 K vs armónico", "D3 95 bohr cerca del límite de RAM (guardia aborta < 700 MB)", "GPAW quizá no disponible tras restaurar la máquina"]
decisiones: ["Evaluación literal con code/nano3_eval.py congelado", "Desviaciones en desviaciones.md"]
proximo_paso: "Congelar; run1 y run2 (monocapas, masivos D3-95), GPAW C1, evaluación."
