import json, re
KEYS = ["meta", "objetivo", "datos_clave", "tareas", "riesgos", "decisiones", "proximo_paso"]
SNAKE = re.compile(r"^[a-z][a-z0-9_]*$")

def _no_null_snake(o):
    if o is None: return False
    if isinstance(o, dict):
        return all(isinstance(k, str) and SNAKE.match(k) and _no_null_snake(v) for k, v in o.items())
    if isinstance(o, list): return all(_no_null_snake(v) for v in o)
    return True

def extract_json(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t)
    s, e = t.find("{"), t.rfind("}")
    return t[s:e + 1] if s >= 0 and e > s else t

def is_valid_llp(text, strict=True):
    """Válido = JSON parseable, claves exactas KEYS, sin null, claves snake_case,
    tipos: meta dict, listas en datos_clave/tareas/riesgos/decisiones, strings en objetivo/proximo_paso.
    strict=True exige que la salida sea SOLO el JSON (sin texto alrededor salvo ```)."""
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    cand = raw if strict else extract_json(text)
    try: o = json.loads(cand)
    except Exception: return False
    if not isinstance(o, dict) or set(o) != set(KEYS): return False
    if not isinstance(o["meta"], dict): return False
    if not all(isinstance(o[k], list) for k in ["datos_clave", "tareas", "riesgos", "decisiones"]): return False
    if not all(isinstance(o[k], str) for k in ["objetivo", "proximo_paso"]): return False
    return _no_null_snake(o)

def prompt(tok, instruction):
    return tok.apply_chat_template([{"role": "user", "content": instruction}], tokenize=False, add_generation_prompt=True)
