import json
import yaml
import sys
from pathlib import Path

SCHEMA_KEYS = {"proyecto"}
PROYECTO_KEYS = {"meta", "objetivo", "datos_clave", "tareas", "riesgos", "decisiones", "proximo_paso"}
META_KEYS = {"id", "nombre", "estado", "fecha", "responsable", "tags"}
TAREA_KEYS = {"id", "tarea", "estado", "prioridad", "responsable", "fecha"}

def validar_estructura(data):
    if not isinstance(data, dict):
        return False, "La raíz debe ser un objeto/diccionario JSON/YAML."
    if "proyecto" not in data:
        return False, "Falta la clave raíz 'proyecto'."
    
    proj = data["proyecto"]
    if not isinstance(proj, dict):
        return False, "'proyecto' debe ser un objeto/diccionario."
    
    missing_proj = PROYECTO_KEYS - set(proj.keys())
    if missing_proj:
        return False, f"Faltan claves en 'proyecto': {missing_proj}"
    
    meta = proj["meta"]
    if not isinstance(meta, dict):
        return False, "'meta' debe ser un objeto/diccionario."
    missing_meta = META_KEYS - set(meta.keys())
    if missing_meta:
        return False, f"Faltan claves en 'meta': {missing_meta}"
    
    if not isinstance(proj["datos_clave"], list):
        return False, "'datos_clave' debe ser una lista."
    if not isinstance(proj["riesgos"], list):
        return False, "'riesgos' debe ser una lista."
    if not isinstance(proj["decisiones"], list):
        return False, "'decisiones' debe ser una lista."
    if not isinstance(proj["tareas"], list):
        return False, "'tareas' debe ser una lista."
    
    for idx, t in enumerate(proj["tareas"]):
        if not isinstance(t, dict):
            return False, f"La tarea #{idx} debe ser un objeto/diccionario."
        missing_t = TAREA_KEYS - set(t.keys())
        if missing_t:
            return False, f"La tarea #{idx} no contiene las claves requeridas: {missing_t}"
            
    return True, "Estructura 100% válida según las reglas del proyecto HYBRIX."

def validar_archivo(filepath):
    path = Path(filepath)
    if not path.exists():
        return False, f"El archivo {filepath} no existe."
    
    try:
        content = path.read_text(encoding="utf-8")
        if path.suffix == ".json":
            data = json.loads(content)
        elif path.suffix in [".yaml", ".yml"]:
            data = yaml.safe_load(content)
        else:
            return False, "Extensión no soportada (usar .json o .yaml)."
        
        return validar_estructura(data)
    except Exception as e:
        return False, f"Error al procesar {filepath}: {str(e)}"

if __name__ == "__main__":
    files_to_test = [
        "/workspace/scratch/resumen_estructurado_hybrix.json",
        "/workspace/scratch/resumen_estructurado_hybrix.yaml"
    ]
    all_ok = True
    for f in files_to_test:
        valido, msg = validar_archivo(f)
        print(f"[{'OK' if valido else 'ERROR'}] {Path(f).name}: {msg}")
        if not valido:
            all_ok = False
            
    if all_ok:
        print("\n¡Todos los archivos estructurados cumplen con las reglas de sintaxis y formato!")
        sys.exit(0)
    else:
        sys.exit(1)
