> Texto extraído automáticamente del PDF original «Canelone_mf_Research_Edition_DOCUMENTO_UNICO.pdf». Fórmulas, figuras y maquetación se han perdido; el original está en Drive: https://drive.google.com/file/d/1VF2K3AVvZC7AtAYRiq7yToZUFn_1XYDb/view?usp=drivesdk



Canelone.mf Research Edition

DOCUMENTO ÚNICO — Todo el proyecto unificado

Versión software: 1.8 · Julio 2026

Un solo código Python · Un solo documento · Listo para publicar y reproducir

Implementación original · Investigación personal

Este documento y el archivo Canelone_mf_Research_Edition.py constituyen la entrega unificada del proyecto. No se requieren
otros archivos de código ni de documentación para entender, ejecutar y publicar el sistema.

1. Entrega unificada

Archivo de código (único): Canelone_mf_Research_Edition.py

Archivo de documentación (único): este PDF

Instalación y ejecución:

pip install streamlit qiskit qiskit-aer qiskit-ibm-runtime matplotlib numpy scipy pillow pylatexenc
streamlit run Canelone_mf_Research_Edition.py

2. Resumen ejecutivo

Canelone.mf Research Edition es un entorno interactivo de investigación cuántica en español. Integra construcción de circuitos,
simulación con ruido, mitigación de lectura (manual y calibración automática), Zero-Noise Extrapolation (simulación y real en el
bucle VQE), VQE con siete optimizadores, el algoritmo adaptativo original CAM-VQE, y conexión opcional a IBM Quantum con
token solo en memoria de sesión.

3. Arquitectura

Usuario → Streamlit (UI en app monolítica) → AerSimulator (local prioritario) y/o IBM Quantum Runtime (opcional).

Principios: local primero; secretos no en disco; funciones de mitigación y optimización integradas en el mismo archivo.

4. Contenido del código único

• Constructor de circuitos (1Q/2Q, medida, QFT, plantillas Bell/GHZ, historial, JSON, export Qiskit)
• Simulación Aer + ruido depolarizing + shots configurables
• Mitigación de lectura: matriz tensored, parámetros P(1|0)/P(0|1), comparación raw vs mitigado
• Calibración automática de lectura (tensored / full) con ReadoutError de Aer
• ZNE en simulación: λ=1,3,5 · linear y Richardson · gráfica
• ZNE real en cada energy() de CAM-VQE (density matrix + extrapolación)
• VQE: SPSA, ADAM, COBYLA, L-BFGS-B, SLSQP, Nelder-Mead, Powell
• Hamiltonianos: ising, heisenberg, molecular + alias investigación
• CAM-VQE: meta-controlador, proxy de ruido, fases, modos standard/zne_aware
• IBM Quantum: conectar / desconectar token en sesión
• Visualización: histogramas, Bloch, fidelidad

5. Mitigación de errores (resumen)

Técnica Función Coste

Readout mitigation Corrige errores de medida ~1×

Calibración automática Estima matriz A midiendo estados conocidos 1 vez

ZNE simulación Extrapola observable a ruido cero ~3×

ZNE real en CAM-VQE ■H■ mitigada en cada evaluación ~3×/eval

Modo zne_aware Adapta SPSA/ADAM/L-BFGS-B al ruido ~1×

Orden recomendado: calibrar lectura → readout sobre counts → ZNE sobre observables → CAM-VQE (zne_aware ± ZNE real).

6. Calibración automática de lectura

Se preparan estados conocidos, se miden con ReadoutError, se estima A_ij = P(medir i | preparado j). Método tensored (rápido):
calibra 1 qubit y extiende por Kronecker. Método full: 2^n estados (n≤4). La matriz queda en sesión y se aplica con la
pseudo-inversa al mitigar counts.

7. CAM-VQE — detalles técnicos

Canelone Adaptive Mitigation Variational Quantum Eigensolver. Meta-controlador con proxy de ruido y tres fases: Exploración
(SPSA), Refinamiento (ADAM con η adaptativa), Pulido (L-BFGS-B).

Fase Condición (standard) Optimizador

Exploración noise_proxy > 0.28 SPSA

Refinamiento 0.12 < noise ≤ 0.28 ADAM

Pulido noise ≤ 0.12 L-BFGS-B

Proxy (heurístico): 0.6·min(slope,1) + 0.4·min(5·variance,1). Modo zne_aware: umbrales 0.18/0.08 y más tiempo en exploración.

ZNE real: para cada energy(θ), simula ρ con ruido λ=1,3,5, calcula Re(Tr(ρH)), extrapola a λ=0 (linear/Richardson).

8. Hamiltonianos de demostración

ising / heisenberg / molecular y alias: metamaterial_spin, propulsion_opt, he3_interaction, nanomedicine_mol. Modelos
simplificados de investigación, no gemelos digitales de alta fidelidad.

9. Seguridad

Token IBM solo en memoria de sesión Streamlit; campo password; botón desconectar/borrar; ejecución local prioritaria; no
hardcodear secretos en el código único.

10. Cómo publicar y reproducir

• Distribuir únicamente: Canelone_mf_Research_Edition.py + este PDF
• En el README del repositorio: citar el nombre del .py y el comando streamlit run
• Instalar dependencias listadas en el encabezado del .py
• No subir tokens ni resultados con datos sensibles
• Declarar autoría y versión 1.8 al publicar

11. Limitaciones

• Ruido depolarizing / ReadoutError simulados; no es caracterización real de un backend IBM
• ZNE real en el bucle es costoso (~3×); presupuestos altos no son prácticos en prototipo
• Hamiltonianos de investigación = demostración, no simulación física completa
• Gate folding unitario no implementado; el escalado de ruido es por probabilidad de error

12. Declaración de originalidad

Interfaz, flujo de proyectos, SPSA/ADAM en este contexto, CAM-VQE (proxy, fases, zne_aware, ZNE real), calibración
automática de lectura integrada y apilado de mitigaciones son implementación original de Canelone.mf Research Edition. No se
copia código ni layouts de IBM Quantum Composer, Quirk, Mitiq u otras UIs. Solo APIs públicas open-source (Qiskit Apache 2.0,
SciPy, Streamlit, etc.).

13. Checklist final

■ Código único ejecutable (Canelone_mf_Research_Edition.py)
■ Documento único (este PDF)
■ Constructor, simulación, readout, calibración automática, ZNE, VQE, CAM-VQE, IBM
■ Interfaz en español
■ Sin dependencia de otros archivos de código del proyecto

Canelone.mf Research Edition · v1.8 · Julio 2026 · Código único + Documento único

Uso de investigación personal · Implementación original
