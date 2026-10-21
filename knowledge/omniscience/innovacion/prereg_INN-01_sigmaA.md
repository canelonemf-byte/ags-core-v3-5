# Pre-registro (borrador) INN-01 — σᴬ con uMLIP como compuerta de validez armónica
Estado: BORRADOR, no congelado ni ejecutado. Redactado el 18-oct-2026 (UTC+2) **después** de ver el exploratorio X1; por eso la prueba confirmatoria usa materiales que no aparecen en X1.

**Hipótesis**
- H-A1: σᴬ(300 K) calculado con MACE-MP-0 (one-shot, armónico) ordena los materiales igual que σᴬ DFT-aiMD publicado (Knoop et al., PRMaterials 4, 083809). Criterio: ρ de Spearman ≥ 0.8, con n ≥ 10.
- H-A2: el sesgo absoluto medio |σᴬ_MACE − σᴬ_DFT| es ≤ 0.05.
- H-A3 (compuerta): con el umbral fijado de antemano σᴬ ≥ 0.30, todos los materiales con error armónico en el TO de Γ > 50 % quedan marcados, y se marca ≤ 30 % de los que tienen error ≤ 15 %.

**Método**
- Conjunto: ≥ 10 sólidos binarios con σᴬ DFT publicado en la SM de Knoop 2020, excluidos los 6 de X1. La lista y los valores se fijan y verifican antes de ejecutar.
- Estructura de partida: experimental; relajación como en C-MAT-001.
- Constantes de fuerza: 3×3×3, 0.01 Å.
- Muestreo: 24 instantáneas armónicas a 300 K (Phonopy, semilla 20261018).
- σᴬ = √(Σ⟨(F−F⁽²⁾)²⟩/Σ⟨F²⟩); IC95 por bootstrap.
- Control de método: MD Langevin de 5 ps a 300 K en 2 materiales.

**Controles**
- Positivo armónico: Si (DFT 0.15).
- Positivos anarmónicos: según la lista verificada.
- Control trivial: con fuerzas sustituidas por F⁽²⁾ debe salir σᴬ = 0.
- Sensibilidad: FC 2×2×2 frente a 3×3×3.

**Falsación**: H-A1 se rechaza si ρ < 0.8 o si el IC95 de ρ incluye 0. H-A2 y H-A3 se rechazan según los criterios anteriores.
**Coste estimado**: ~30–60 min de CPU.
