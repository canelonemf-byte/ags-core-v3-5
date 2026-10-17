# MEI-RIT proto1 — diseño cerrado
2026-09-22. Ejecutable: `python3 artifacts/mei_rit_design.py`
Canon: `llp/proyectos/MEI-RIT.json` + `llp/proyectos/MEI-RIT_proto1_card.json`
Clase: **E2**. No hay hardware.

## Congelado
- f = **13.56 MHz** ICP. No dual-band.
- Cámara ID 32 mm, pared 1.5 mm Al₂O₃/cuarzo, L 36 mm.
- Rejilla Ø 28 mm, gap 0.60 mm, SG 1.1 mm / AG 0.70 mm, grafito, τ≈0.55.
- Bobina 5 vueltas, hilo Ø 1.6 mm, paso 4.5 mm. L≈848 nH → C_tune≈162 pF.
- Anillo matching periodo **8 mm**, fill 0.45, metal 20 μm + ALD 150 nm.
- V_b = 1200 V, V_acc = −200 V.
- P_RF fwd = 40 W (η_match 0.88). I_b diseño = 16 mA.

## Punto nominal (proyección)
T = 0.95 mN · Isp_sys = 2800 s · Isp_ion = 4116 s · η_m = 0.68 · I₂⁺ = 12 %
P_beam ≈ 19 W · P_sys ≈ 79 W · T/P ≈ 12 mN/kW (sistema, no beam).
δ_inercial/R = 0.96 @ n_e=1.2×10¹⁷ m⁻³. I_b << 0.7 I_CL.

## Qué es / qué no es
- Funcional = geometría + matching + 0D I₂ + chequeos + mapa T(P) reproducibles.
- No es medida, no es CST, no es VQE. `vqe_i2.py` es rama aparte.
- Anillo 8 mm es **lumped** (p/λ∼3.6×10⁻⁴), no FSS.
- Masa sistema sigue 0.8–2.5 kg, no 220 g.
