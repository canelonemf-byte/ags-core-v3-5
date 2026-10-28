# Desviaciones C-VIB-003
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963

D1 (declarada antes de calcular, 2026-10-27T09:12+01:00): antes de congelar se hicieron dos pruebas de humo no evaluables: (i) recuento de desplazamientos fc3 (blenda 3×3×3: 716; sal de roca 2×2×2: 146) y tiempo de una fuerza MatterSim en 216 átomos (BN 5.3 s, PbTe 0.5 s); (ii) NaCl con malla 7³ para comprobar la API LBTE de phono3py 4.8.2 (borrado). El código no cambió tras las pruebas salvo para escribirlo completo. El evaluador lee C-VIB-002 run1 desde una copia local (/workspace/omniscience_cvib003/out_cvib002_run1, 15 JSON idénticos a los originales).

D2 (2026-10-28 09:15+01:00, tras evaluar): la ejecución diaria del 27-oct terminó como fallida antes de volcar el cierre al registro; el cálculo y el evaluador congelado terminaron bien a las 17:29. El cierre se hace hoy sin recalcular nada. Además, C1 falló en KI y el evaluador no excluyó KI de C_H2–C_H5 como dice el prereg; no se toca el evaluador congelado y no cambia el nivel (UM-25 E2 por H_REP + C_H3).
