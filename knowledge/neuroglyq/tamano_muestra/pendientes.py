"""pendientes: carga datos_pendientes.yaml y valida cada dato. Si falta uno, lanza DatoPendiente con un mensaje claro."""
import os
import yaml

RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "datos_pendientes.yaml")


class DatoPendiente(Exception):
    pass


def cargar(ruta=None):
    with open(ruta or RUTA, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def vacio(v):
    return v is None or v == "" or v == []


def dato(cfg, clave, usar_ejemplo=True):
    """Devuelve (valor, origen). origen es 'dato_usuario' o 'ejemplo_publico'."""
    if clave not in cfg:
        raise KeyError(f"clave desconocida: {clave}")
    e = cfg[clave]
    if not vacio(e.get("valor")):
        return e["valor"], "dato_usuario"
    if usar_ejemplo and not vacio(e.get("ejemplo_publico")):
        return e["ejemplo_publico"], "ejemplo_publico (" + str(e.get("fuente_ejemplo", "")) + ")"
    raise DatoPendiente(f"PENDIENTE: falta dato {clave} ({e.get('descripcion', '')}; unidades: {e.get('unidades', '')})")


def faltan(cfg):
    return [k for k, e in cfg.items() if vacio(e.get("valor"))]
