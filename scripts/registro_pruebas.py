#!/usr/bin/env python3
"""Registro de pruebas AGs-Core v3.6: SQLite + Excel, con deduplicación.

Uso:
  python scripts/registro_pruebas.py init
  python scripts/registro_pruebas.py consultar --funcion F --parametros '{"a":1}' --semilla 7
      (exit 0 = no corrida; exit 3 = ya existe, imprime la fila previa)
  python scripts/registro_pruebas.py exportar
Clave de deduplicación: (funcion, parametros_json canónico, semilla). Comprobaciones de estado
sin semilla usan semilla "" y llevan "comprobacion_id" (fecha-hora) en parametros.

Solo se registran corridas reales. Simulación se etiqueta tipo=simulacion. Nunca E4+.
Autoría: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA.
Licencia: MIT (código); CC BY 4.0 (datos del registro).
"""
from __future__ import annotations
import argparse, hashlib, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge" / "pruebas" / "pruebas.db"
XLSX = ROOT / "knowledge" / "pruebas" / "pruebas.xlsx"
TIPOS = ("software", "simulacion", "fuente_publica", "experimento")
COLS = ["fecha", "zona", "proyecto", "funcion", "modulo", "parametros_json", "semilla", "resultado",
        "error", "evidencia", "tipo", "hash", "reproducible", "notas"]

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS pruebas(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 {", ".join(c + " TEXT NOT NULL DEFAULT ''" for c in COLS if c != "tipo")},
 tipo TEXT NOT NULL CHECK (tipo IN {TIPOS}),
 CHECK (evidencia NOT LIKE 'E4%' AND evidencia NOT LIKE 'E5%' AND evidencia NOT LIKE 'E6%'),
 UNIQUE(funcion, parametros_json, semilla));
CREATE TABLE IF NOT EXISTS funciones(
 nombre TEXT PRIMARY KEY, modulo TEXT NOT NULL DEFAULT '', parametros_schema TEXT NOT NULL DEFAULT '',
 que_prueba TEXT NOT NULL DEFAULT '', ultima_corrida TEXT NOT NULL DEFAULT '',
 no_repetir_si TEXT NOT NULL DEFAULT '', estado TEXT NOT NULL CHECK (estado IN ('posible_hoy','bloqueada')),
 motivo_bloqueo TEXT NOT NULL DEFAULT '');
"""

def canon(p) -> str:
    if isinstance(p, str):
        p = json.loads(p or "{}")
    return json.dumps(p, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def conectar(db: Path = DB) -> sqlite3.Connection:
    db.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(db); c.row_factory = sqlite3.Row; c.executescript(SCHEMA); return c

def consultar_antes_de_correr(funcion, parametros, semilla, db: Path = DB):
    """Devuelve la fila previa (dict) si funcion+parametros+semilla ya existe; si no, None."""
    with conectar(db) as c:
        r = c.execute("SELECT * FROM pruebas WHERE funcion=? AND parametros_json=? AND semilla=?",
                      (funcion, canon(parametros), str(semilla))).fetchone()
    return dict(r) if r else None

def registrar(fila: dict, db: Path = DB) -> bool:
    """Inserta una corrida real. Devuelve False si ya existía (no duplica)."""
    f = {c: str(fila.get(c, "")) for c in COLS}
    f["parametros_json"] = canon(fila.get("parametros_json", {}))
    if f["tipo"] not in TIPOS:
        raise ValueError(f"tipo inválido: {f['tipo']}")
    if f["evidencia"].upper().startswith(("E4", "E5", "E6")):
        raise ValueError("E4+ no se registra sin validación experimental independiente")
    if not f["hash"]:
        f["hash"] = hashlib.sha256(f["resultado"].encode()).hexdigest()
    with conectar(db) as c:
        cur = c.execute(f"INSERT OR IGNORE INTO pruebas({','.join(COLS)}) VALUES({','.join('?'*len(COLS))})",
                        [f[k] for k in COLS])
        return cur.rowcount == 1

def registrar_funcion(fn: dict, db: Path = DB) -> None:
    keys = ["nombre","modulo","parametros_schema","que_prueba","ultima_corrida","no_repetir_si","estado","motivo_bloqueo"]
    v = {k: (canon(fn[k]) if k == "parametros_schema" and not isinstance(fn.get(k,""), str) else str(fn.get(k, ""))) for k in keys}
    with conectar(db) as c:
        c.execute(f"INSERT OR REPLACE INTO funciones({','.join(keys)}) VALUES({','.join('?'*len(keys))})", [v[k] for k in keys])

def exportar_xlsx(db: Path = DB, out: Path = XLSX) -> dict:
    from openpyxl import Workbook
    from openpyxl.utils import get_column_letter
    c = conectar(db); wb = Workbook()
    wb.properties.creator = "Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA"
    wb.properties.description = "Licencia CC BY 4.0. Solo corridas reales; simulación etiquetada como simulación."
    def hoja(ws, cab, filas):
        ws.append(cab)
        for f in filas: ws.append(list(f))
        ws.auto_filter.ref = ws.dimensions; ws.freeze_panes = "A2"
        for i, h in enumerate(cab, 1):
            w = max([len(str(h))] + [len(str(f[i-1])) for f in filas]) if filas else len(h)
            ws.column_dimensions[get_column_letter(i)].width = min(max(w + 2, 10), 70)
    ws = wb.active; ws.title = "Pruebas"
    hoja(ws, ["id"] + COLS, [tuple(r) for r in c.execute(f"SELECT id,{','.join(COLS)} FROM pruebas ORDER BY id")])
    fk = ["nombre","modulo","parametros_schema","que_prueba","ultima_corrida","no_repetir_si","estado","motivo_bloqueo"]
    hoja(wb.create_sheet("Funciones"), fk, [tuple(r) for r in c.execute(f"SELECT {','.join(fk)} FROM funciones WHERE estado='posible_hoy' ORDER BY nombre")])
    par = []
    for r in c.execute("SELECT nombre, parametros_schema FROM funciones ORDER BY nombre"):
        for a in json.loads(r["parametros_schema"] or "{}").get("args", []):
            par.append((r["nombre"], a.get("arg",""), a.get("tipo",""), str(a.get("defecto","")), str(a.get("min","")), str(a.get("max","")), a.get("notas","")))
    hoja(wb.create_sheet("Parametros"), ["funcion","arg","tipo","defecto","min","max","notas"], par)
    hoja(wb.create_sheet("Bloqueadas"), ["nombre","modulo","que_prueba","motivo_bloqueo"],
         [tuple(r) for r in c.execute("SELECT nombre,modulo,que_prueba,motivo_bloqueo FROM funciones WHERE estado='bloqueada' ORDER BY nombre")])
    tmp = out.with_suffix(".tmp.xlsx"); wb.save(tmp); tmp.replace(out)
    return {s.title: s.max_row - 1 for s in wb.worksheets}

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init"); sub.add_parser("exportar")
    q = sub.add_parser("consultar"); q.add_argument("--funcion", required=True)
    q.add_argument("--parametros", default="{}"); q.add_argument("--semilla", default="")
    a = ap.parse_args(argv)
    if a.cmd == "init": conectar().close(); print(DB); return 0
    if a.cmd == "exportar": print(json.dumps(exportar_xlsx(), ensure_ascii=False)); return 0
    r = consultar_antes_de_correr(a.funcion, a.parametros, a.semilla)
    if r: print(json.dumps(r, ensure_ascii=False)); return 3
    print("no_corrida"); return 0

if __name__ == "__main__":
    sys.exit(main())
