"""Simulación E2: MVM baseline CMOS digital vs CIM memristivo multinivel.
Modelo simple y explícito; todos los parámetros en parametros.yaml (supuestos)."""
import json, csv, pathlib, numpy as np, yaml
D = pathlib.Path(__file__).parent
P = yaml.safe_load(open(D / "parametros.yaml"))
v = lambda k1, k2: P[k1][k2]["valor"]
rng = np.random.default_rng(P["semilla"]["valor"])
N, M, K = v("tarea","filas"), v("tarea","columnas"), v("tarea","n_vectores")
W = rng.uniform(-1, 1, (N, M)); X = rng.uniform(0, 1, (K, M))
Y_ref = X @ W.T
def quant(a, bits, lo, hi):
    q = 2**bits - 1; a = np.clip(a, lo, hi)
    return np.round((a - lo) / (hi - lo) * q) / q * (hi - lo) + lo
def rel_err(Y): return float(np.linalg.norm(Y - Y_ref) / np.linalg.norm(Y_ref))
b = v("cmos","bits")
Y_cmos = quant(X, b, 0, 1) @ quant(W, b, -1, 1).T
e_cmos = K*N*M*v("cmos","e_mac_pj") + N*M*v("cmos","e_lectura_peso_pj")  # pesos leídos una vez por lote
filas = [{"config":"cmos_digital","niveles":2**b,"bits_adc":0,"error_rel":rel_err(Y_cmos),
          "energia_total_pj":e_cmos,"energia_por_mac_pj":e_cmos/(K*N*M),"ahorro_vs_cmos":0.0,"frac_adc_dac":0.0}]
C = P["cim"]; sp, sr = C["ruido_programacion_rel"]["valor"], C["ruido_lectura_rel"]["valor"]
for L in C["niveles_conductancia"]["valores"]:
    bitsw = np.log2(L)
    # pesos diferenciales G+ - G-, cuantizados a L niveles, ruido de programación
    Wq = np.round((W + 1) / 2 * (L - 1)) / (L - 1) * 2 - 1
    Wp = Wq + rng.normal(0, 2*sp, W.shape)
    for ba in C["bits_adc"]["valores"]:
        Y = X @ Wp.T + rng.normal(0, 2*sr, (K, N)) * np.sqrt(M) * 0.5
        lim = np.abs(Y_ref).max() * 1.05
        Y = quant(Y, ba, -lim, lim)
        e_arr = K*N*M*C["e_celda_pj"]["valor"]*2
        e_dac = K*M*C["e_dac_pj"]["valor"]
        e_adc = K*N*ba*C["e_adc_pj_por_bit"]["valor"]
        e_cal = K*C["e_calibracion_pj_por_vector"]["valor"]
        e = e_arr+e_dac+e_adc+e_cal
        filas.append({"config":"cim_memristivo","niveles":L,"bits_adc":ba,"error_rel":rel_err(Y),
            "energia_total_pj":e,"energia_por_mac_pj":e/(K*N*M),"ahorro_vs_cmos":1-e/e_cmos,
            "frac_adc_dac":(e_adc+e_dac)/e})
out = D / "salidas"; out.mkdir(exist_ok=True)
with open(out/"resultados.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=filas[0].keys()); w.writeheader(); w.writerows(filas)
json.dump({"nivel_evidencia":"E2","tipo":"simulacion","nota":"modelo simple con parámetros supuestos; no es experimento",
           "semilla":P["semilla"]["valor"],"tarea":f"MVM {N}x{M}, {K} vectores","resultados":filas},
          open(out/"resultados.json","w"), indent=1, ensure_ascii=False)
for r in filas: print({k:(round(x,4) if isinstance(x,float) else x) for k,x in r.items()})
