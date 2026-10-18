"""UI mínima de estado de AGs-Core v3.6 (Streamlit, solo lectura).

Muestra /health, /supervisor/status, la lista de proyectos con el recuento de hallazgos
de reports/<proyecto>/*.json y reports/SUMMARY.md. La clave X-API-Key se lee en el
servidor desde data/api_key y nunca se envía al navegador.

Arranque: streamlit run ui/app.py --server.address 127.0.0.1 --server.port 8501
"""
import json
import os
from pathlib import Path

import httpx
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
API = os.getenv("AGS_BASE_URL", "http://127.0.0.1:8000")
REPORTS = ROOT / "reports"
SEVS = ("high", "medium", "low", "info")


def api_key() -> str:
    p = ROOT / "data" / "api_key"
    return p.read_text().strip() if p.exists() else os.getenv("AGS_API_KEY", "")


def get(path: str, auth: bool = False):
    headers = {"X-API-Key": api_key()} if auth else {}
    try:
        r = httpx.get(API + path, headers=headers, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except Exception as exc:  # se muestra el error tal cual, sin inventar estado
        return None, f"{type(exc).__name__}: {exc}"


def report_counts() -> dict:
    out = {}
    for d in sorted(p for p in REPORTS.iterdir() if p.is_dir()) if REPORTS.exists() else []:
        row = {s: 0 for s in SEVS}
        row["generated"] = ""
        for f in d.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for s in SEVS:
                row[s] += int(data.get("summary", {}).get("counts", {}).get(s, 0))
            row["generated"] = max(row["generated"], str(data.get("generated", "")))
        out[d.name] = row
    return out


st.set_page_config(page_title="AGs-Core v3.6 · estado", layout="wide")
st.title("AGs-Core v3.6 · estado del stack")
st.caption("Solo lectura. Los informes son indicios a revisar, no veredictos. "
           "Lo no verificado figura como PENDIENTE DE VERIFICACIÓN.")
if st.button("Recargar"):
    st.rerun()

c1, c2 = st.columns(2)
with c1:
    st.subheader("/health")
    h, err = get("/health")
    if err:
        st.error(f"API no disponible en {API}: {err}")
    else:
        st.json(h)
        if h.get("litellm") != "ok":
            st.warning(f"LiteLLM: {h.get('litellm')}. Los agentes que dependen de un LLM no funcionan.")
with c2:
    st.subheader("/supervisor/status")
    s, err = get("/supervisor/status", auth=True)
    st.error(err) if err else st.json(s)

st.subheader("Proyectos")
projects, err = get("/projects")
counts = report_counts()
if err:
    st.error(err)
else:
    rows = []
    for p in projects.get("projects", []):
        c = counts.get(p["id"], {})
        rows.append({"proyecto": p["id"], "licencia": p.get("license") or "—", "archivos": p.get("files"),
                     **{s: c.get(s, 0) for s in SEVS}, "informe": c.get("generated") or "sin informe"})
    st.write(f"{projects.get('total', len(rows))} proyectos")
    st.dataframe(rows, width="stretch", hide_index=True)

st.subheader("reports/SUMMARY.md")
summary = REPORTS / "SUMMARY.md"
st.markdown(summary.read_text(encoding="utf-8") if summary.exists() else "_Sin SUMMARY.md todavía._")
