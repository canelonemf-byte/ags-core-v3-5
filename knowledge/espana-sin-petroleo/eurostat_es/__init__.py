"""eurostat_es: datos reales de Eurostat para España (energía bruta disponible de petróleo y total en ktep, y dependencia importadora del petróleo en %), descargados de la API pública y guardados en data/eurostat_es.json. Con ellos calcula la trayectoria lineal de reducción hacia el objetivo del usuario.

Referencias (verificadas):
Eurostat (2026) Complete energy balances [nrg_bal_c], actualizado 27-08-2026. https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_c/default/table
Eurostat (2026) Energy imports dependency [nrg_ind_id], actualizado 16-07-2026. https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_id/default/table

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import json, os, urllib.request
from .pendientes import cargar, dato

API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
SERIES = {"petroleo_gae_ktep": "nrg_bal_c?geo=ES&siec=O4000XBIO&nrg_bal=GAE&unit=KTOE",
          "total_gae_ktep": "nrg_bal_c?geo=ES&siec=TOTAL&nrg_bal=GAE&unit=KTOE",
          "dependencia_petroleo_pct": "nrg_ind_id?geo=ES&siec=O4000XBIO&unit=PC"}
CACHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "eurostat_es.json")


def _parse(d):
    inv = {str(i): k for k, i in d["dimension"]["time"]["category"]["index"].items()}
    return {inv[k]: v for k, v in sorted(d["value"].items(), key=lambda kv: int(kv[0]))}


def descargar(ruta=CACHE):
    out = {"fuente": "Eurostat API dissemination 1.0", "series": {}}
    for k, q in SERIES.items():
        with urllib.request.urlopen(API + q + "&lang=EN", timeout=60) as r:
            d = json.load(r)
        out["series"][k] = {"consulta": q, "actualizado": d.get("updated"), "valores": _parse(d)}
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    json.dump(out, open(ruta, "w"), indent=1)
    return out


def leer(ruta=CACHE):
    return json.load(open(ruta))


def cuota_petroleo(datos, anio):
    s = datos["series"]
    return s["petroleo_gae_ktep"]["valores"][anio] / s["total_gae_ktep"]["valores"][anio]


def trayectoria(datos, anio_base, anio_obj, fraccion_obj):
    v0 = datos["series"]["petroleo_gae_ktep"]["valores"][anio_base]
    n = int(anio_obj) - int(anio_base)
    if n <= 0:
        raise ValueError("el año objetivo debe ser posterior al año base")
    return {str(int(anio_base) + i): v0 * (1 - (1 - fraccion_obj) * i / n) for i in range(n + 1)}


def run(cfg=None):
    cfg = cfg or cargar(); d = leer()
    base = max(d["series"]["petroleo_gae_ktep"]["valores"])
    ao = dato(cfg, "anio_objetivo")[0]; fo = float(dato(cfg, "fraccion_petroleo_restante")[0])
    return {"anio_base": base, "cuota_petroleo": cuota_petroleo(d, base), "trayectoria_ktep": trayectoria(d, base, ao, fo)}
