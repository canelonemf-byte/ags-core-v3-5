"""Compara la reactividad D-T y D-3He (Bosch y Hale 1992) y la potencia a densidad fija."""
import json
import fusionrate as f
out = []
for T in (10, 20, 50, 70, 100):
    out.append({"T_keV": T, "sv_DT_m3_s": float(f.reactivity(T, "DT")), "sv_DHe3_m3_s": float(f.reactivity(T, "DHe3")),
                "cociente_DHe3_DT": float(f.reactivity(T, "DHe3") / f.reactivity(T, "DT"))})
print(json.dumps(out, indent=2))
