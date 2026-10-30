# Resultados C-VIB-006 — escalado único de fuerzas de MatterSim-v1 (fc2/fc3) con LOOCV en κL de sales de roca
```yaml
meta: {campana: C-VIB-006, fecha: "2026-10-30", zona: Europe/Madrid, autor: "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial", orcid: 0000-0001-8601-1963, prereg_sha256: 4bca003c450a61c52920138015834ed406fffd4094803b7636aa3215ed2ced49, evaluador_sha256: 1d01335436e60c0bba9365d2e8fd8e6c40d774af4be3149c532e14d351d5aea7, runner_sha256: cd07434d0f53e3ebe4137612226b30f461b9ca87ae50a89b7ca6b9844ac8aa74, run_all_sha256: 7370b06d29f854007c95cfb437bdc6d9bfc56b9a4a688d753666cb619a4197c8, congelado: "2026-10-30T09:49:32+01:00", ejecucion: "rejilla 09:50–12:58, CA 12:58–12:59, réplica 12:59–13:03, eval 13:03 y re-eval 13:05 (idéntica)", resultados: "results.json sha256 f62f1996…d653"}
objetivo: "Probar si un único factor s sobre las fuerzas de MatterSim-v1 (fc2 y fc3) en a_exp(300 K) corrige el ablandamiento de κL en 16 sales de roca (LOOCV), y contrastar g con κ(P) de Andersson 1985 si hay números abiertos"
metodo: "Receta C-VIB-004 (MatterSim-v1.0.0-5M, phono3py RTA, 2×2×2, d 0.03 Å, malla 19³, 300 K) con F'=s·F, s ∈ {1.00…1.25}; s=1.00 reutilizado de C-VIB-004; LOOCV de s*_i por media |log10(κ/κexp)| del resto"
datos_clave:
  H_A: "NO EVALUABLE (D0 a priori: Andersson 1985 sin tabla numérica abierta)"
  H1: "15/16 dentro de factor 2 tras LOOCV — PASA (umbral ≥14; a s=1.00 eran 13/16)"
  H2: "media LOOCV |log10| 0.144 — PASA (≤0.20; a s=1.00 era 0.156)"
  H3: "NaI 0.560, KBr 0.506, RbCl 0.393 → 2/3 — PASA (KBr justo en el borde)"
  H4: "mediana s* 1.15 — PASA ([1.00,1.30]); s* = 1.15 en 10 sales y 1.20 en 6"
  H5_REP: "NaCl, KBr, MgO a s=1.15 idénticos (cociente 1.0) — PASA"
  CA: "NaCl s=1.00 reproduce C-VIB-004 (−8.65e-5) — PASA"
  C1: "ν_min > −0.05 THz en 16/16 — PASA"
  s_global_ref: "1.15 (media |log10| 0.134 en las 16)"
  KI_exploratorio: "κ 0.018→0.025 W/mK en s 1.00→1.25 (κexp 2.8): sigue no físico"
  lectura: "Escalar fc2 y fc3 por s multiplica κ casi igual en todas las sales (×1.21–×1.24 a s=1.15, ≈ s^1.5). La corrección es en la práctica un factor global de calibración: mejora el conjunto (13→15/16) pero no cambia el orden ni arregla los errores específicos (RbCl sigue en 0.39·κexp, NaI 0.56, KBr 0.51; MgO pasa a 1.49 y NaF a 1.80)."
  UM-27: "nueva, E3 por regla (CA, H1, H2, H4, H5_REP y H3 pasan)"
  UM-25: "E2→E3 por regla (H1, H2, H3 pasan), con nota de alcance: es κ calibrado con un factor global ajustado por LOOCV, no MatterSim sin ajuste"
  UM-26: "E1 sin cambio; H_A NO EVALUABLE"
tareas: []
riesgos: ["El escalado equivale casi a un factor global de κ; el éxito depende de que las 16 sales compartan sesgo", "H3 pasa por un margen de 0.006 en KBr", "RTA 2×2×2, sin NAC ni 4 fonones; LOOCV sobre 16 puntos", "La réplica es un recálculo determinista en la misma máquina, no independiente", "KI excluido a priori; sigue sin κ física"]
decisiones: ["Regla prerregistrada aplicada sin cambios", "Nada subido a repositorios ni LoRA entrenada"]
originalidad: {grado: parcial, fuentes: ["https://www.nature.com/articles/s41524-024-01500-6", "https://www.osti.gov/biblio/2528028", "https://doi.org/10.1088/2632-2153/ad86a1", "https://arxiv.org/html/2601.07742v3", "https://phantomsfoundation.com/AI4AM/2025/Abstracts/AI4AM2025_Wang_Shirui_69.pdf", "https://arxiv.org/abs/2509.03401"], nota: "La corrección lineal escalar del ablandamiento de uMLIP ya está propuesta (Deng et al., npj Comput. Mater. 2025) y se ha señalado que una escala global no corrige la curvatura local (Mach. Learn.: Sci. Technol. 2024). No se encontró la prueba prerregistrada de un escalado único de fuerzas con LOOCV para κL de sales de roca con MatterSim-v1, ni la observación de que equivale a κ·s^1.5 casi uniforme."}
proximo_paso: "C-VIB-007: sustituir la escala global por fine-tuning ligero con pocas fuerzas DFT (NaI, KBr, RbCl) o por una escala por elemento, y comprobar si mejora más allá del factor global; seguir buscando valores abiertos de κ(P)"
```
