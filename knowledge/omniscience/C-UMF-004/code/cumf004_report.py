#!/usr/bin/env python3
"""C-UMF-004: informe MD y fila UM-21 del registro a partir de results.json (sin escribir dos veces).
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial (ORCID 0000-0001-8601-1963)."""
import csv, json, os, shutil, datetime
H = os.path.dirname(os.path.abspath(__file__)) + "/.."; R = json.load(open(H + "/results.json")); A, B, h = R["A"], R["B"], R["hipotesis"]
ST = "/cursor/stores/store-228d687d-cb00-4ece-829b-9a5115f9c989/omniscience"; f2 = lambda x: "—" if x is None else f"{x:.1f}"
dev = open(H + "/desviaciones.md").read() if os.path.exists(H + "/desviaciones.md") else "Ninguna."
md = f"""# Resultados C-UMF-004 (prereg sha256 845ad29a…be31, congelado 20-oct-2026 17:09:44 UTC+2)
autoria: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de inteligencia artificial · ORCID 0000-0001-8601-1963
## A. ΔE(anatasa−rutilo) meV/át (experimento +9.0±1.4)
PBE relajada {f2(A['dE_PBE_relaj'])} · r2SCAN relajada {f2(A['dE_R2SCAN_relaj'])} (réplica {f2(A['dE_R2SCAN_relaj_run2'])}) · ΔH_vib(298) {f2(A['dH_vib298'])} (ΔZPE {f2(A['dZPE'])}) · r2SCAN+vib {f2(A['dH_R2SCAN_vib'])} · HSE06 k reducido {f2(A['dE_HSE06_reducido'])}
## B. MatterSim+D3 ΔfH (protocolo C-UMF-002)
MAE LOOCV {f2(B.get('MAE_loocv_D3'))} (base 32.6, n={B.get('n')}) · capas {json.dumps({k: round(v, 1) for k, v in B.get('err_capas_D3', {}).items()})} MAE {f2(B.get('MAE_capas_D3'))} (base 51.8) · máx {f2(B.get('max_abs_D3'))} ({B.get('peor')}) · test Ti {f2(B.get('MAE_test_Ti_D3'))} · MP2020 {f2(B.get('MAE_mp2020_D3'))}
## Hipótesis
{json.dumps(h, ensure_ascii=False)}
controles: {json.dumps(R['controles'], default=str)}
nivel: **{R['nivel_E']}**
## Desviaciones
{dev}
## Limitación declarada (F1)
r2SCAN con setups PAW-PBE: GPAW 25.1 no genera setups meta-GGA (NotImplementedError).
figura: figs/C-UMF-004_resumen.png · referencias: ver prereg (DOI)
"""
open(H + "/resultados_C-UMF-004.md", "w").write(md)
reg = ST + "/evidence_register.csv"
if "UM-21," not in open(reg).read():
    shutil.copy(reg, ST + "/evidence_register.bak_cumf004.csv"); shutil.copy(ST + "/log_avances.md", ST + "/log_avances.bak_cumf004.md")
    hdr = next(csv.reader(open(reg))); row = ["UM-21", "Universal Matter (MV1)",
        "Campaña C-UMF-004 «Anatasa/rutilo: PBE relajado + r2SCAN (setups PBE) + ΔH_vib MatterSim + HSE06 k reducido; MatterSim+D3(BJ) en ΔfH de C-UMF-002» (ejecutada 20-oct-2026)",
        "C-UMF-004/ (prereg sha256 845ad29a…be31)", R["nivel_E"],
        f"Congelación 17:09:44 UTC+2. ΔE(A−R) meV/át: PBE relaj {f2(A['dE_PBE_relaj'])}, r2SCAN relaj {f2(A['dE_R2SCAN_relaj'])}, ΔH_vib {f2(A['dH_vib298'])}, r2SCAN+vib {f2(A['dH_R2SCAN_vib'])}, HSE06 {f2(A['dE_HSE06_reducido'])} frente a +9.0. "
        f"D3: MAE LOOCV {f2(B.get('MAE_loocv_D3'))} (base 32.6), capas {f2(B.get('MAE_capas_D3'))} (base 51.8), máx {f2(B.get('max_abs_D3'))}. " + "; ".join(f"{k} {v}" for k, v in h.items()),
        "C-UMF-005 según resultado (ver informe)",
        "https://doi.org/10.1073/pnas.251534898 ; https://doi.org/10.1021/acs.jpclett.0c02405 ; https://doi.org/10.1002/jcc.21759 ; https://doi.org/10.1063/1.2204597 . Aportación: prueba prerregistrada con réplica; métodos publicados"]
    row = row[:len(hdr)] + [""] * (len(hdr) - len(row))
    with open(reg, "a", newline="") as fh: csv.writer(fh).writerow(row)
    with open(ST + "/log_avances.md", "a") as fh: fh.write(f"\n## {datetime.datetime.now().isoformat(timespec='minutes')} C-UMF-004 → {R['nivel_E']} (UM-21)\n{json.dumps(h, ensure_ascii=False)}\n")
print(md)
