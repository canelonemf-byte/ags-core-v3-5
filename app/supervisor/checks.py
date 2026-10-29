"""Revisiones deterministas por proyecto (sin LLM). Cada revisión trabaja por archivo para
poder repartirse entre sub-agentes y luego fusionar hallazgos.

Tipos:
- review_claims  : afirmaciones sin respaldo (superlativos, física dudosa, cifras sin fuente)
- missing_pieces : piezas que faltan (código, tests, referencias, licencia, archivos en Drive)
- license_check  : originalidad / licencia / atribuciones (derechos reservados vs MIT,
                   nombres de terceros, código derivado sin atribución, texto generado por IA)
"""
import re
from pathlib import Path

from projects.knowledge import CODE_EXT, DOC_EXT, plain

KINDS = ("review_claims", "missing_pieces", "license_check")

HYPE = [
    "revolucionari", "sin precedentes", "inquebrantable", "inhackeable", "invulnerable",
    "100% segur", "100 % segur", "garantiza", "garantizad", "infinit", "ilimitad",
    "perfecto", "perfecta", "inmunidad total", "total immunity", "unbreakable", "guaranteed",
    "first ever", "world's first", "world first", "primera vez en la historia", "primero del mundo",
    "unico en el mundo", "cura definitiva", "cura el", "cura la", "elimina por completo",
    "sin efectos secundarios", "100% eficien", "eficiencia del 100", "omnisciente", "omnipotente",
]
PHYSICS = [
    "teletransport", "antigravedad", "anti-gravedad", "antigravity", "control del tiempo",
    "control temporal", "viaje en el tiempo", "time travel", "superluminal", "mas rapido que la luz",
    "faster than light", "energia libre", "free energy", "movimiento perpetuo", "perpetual motion",
    "energia del punto cero", "zero-point energy", "energia infinita", "retrocausal",
]
DFT_OUTPUT = re.compile(r"(free energy|energia libre)\s*[:=]\s*[-+]?\d")  # salida de código DFT (energía libre de Mermin/smearing), no afirmación
GIBBS = re.compile(r"gibbs|helmholtz|barrera|delta ?g|δg|\\delta|activacion|de union|binding|kcal|kj/mol")
VALIDATION_WORDS = ["demostrado", "validado", "probado", "comprobado", "certificado", "proven", "validated", "certified"]
UNIT = re.compile(
    r"\b\d[\d.,]*\s?(?:%|mw|gw|kw|tw|kwh|mwh|kg/h|t/dia|t/día|toneladas|kev|mev|ev|k\b|kelvin|tesla|\bt\b|qubits?|ghz|thz|nm|"
    r"€|eur|usd|\$|años|years|x\s?mas|veces|ms\b|µs|us\b|db\b|n\b|mn\b|km/s|m/s)",
    re.I,
)
CITE = re.compile(r"\[\d+\]|\(\w[\w\s.&-]*,?\s(19|20)\d\d\)|doi|arxiv|https?://|et al\.?|fuente:|source:|ref\.", re.I)

HYPOTHESIS = re.compile(r"hipotesis e0|\be0\b|especulativ|hypothesis|sin evidencia experimental")

RESERVED = [
    ("todos los derechos reservados", "high"), ("all rights reserved", "high"),
    ("derechos reservados", "high"), ("prohibida su reproduccion", "high"),
    ("prohibida la reproduccion", "high"), ("cc by-nc", "high"), ("nocomercial", "high"),
    ("noncommercial", "high"), ("confidencial", "medium"), ("propiedad intelectual protegida", "medium"),
    ("patente en tramite", "medium"), ("patente pendiente", "medium"), ("patent pending", "medium"),
    ("inventado y patentado", "medium"), ("apache license", "medium"), ("gnu general public license", "medium"), ("proprietary technical", "low"), ("propietario intelectual", "low"),
]
THIRD_PARTY = {
    # nombre normalizado -> tipo
    "openai": "empresa", "chatgpt": "producto IA", "gpt-4": "producto IA", "grok": "producto IA", "xai": "empresa",
    "claude": "producto IA", "anthropic": "empresa", "gemini": "producto IA", "deepseek": "producto IA",
    "google": "empresa", "microsoft": "empresa", "ibm": "empresa", "qiskit": "software", "nvidia": "empresa",
    "intel": "empresa", "iqm": "empresa", "d-wave": "empresa", "rigetti": "empresa", "ionq": "empresa",
    "tesla": "empresa", "spacex": "empresa", "nasa": "agencia", "iter": "organismo",
    "helion": "empresa", "tae technologies": "empresa", "neuralink": "empresa",
    "pfizer": "empresa", "moderna": "empresa", "karpathy": "persona", "nanogpt": "software", "mingpt": "software",
    "loralib": "software", "hugging face": "empresa", "huggingface": "empresa", "sarfatti": "persona",
    "zenodo": "plataforma", "streamlit": "software", "pytorch": "software", "tensorflow": "software",
    "nist": "organismo", "pennylane": "software", "cirq": "software", "quantinuum": "empresa",
}
_TP_RE = {n: re.compile(r"(?<![a-z0-9])" + re.escape(n) + r"(?![a-z0-9])") for n in THIRD_PARTY}
NEEDS_NOTICE = {"karpathy", "nanogpt", "mingpt", "loralib", "sarfatti"}
DERIVED = re.compile(r"\b(basado en|adaptado de|copiado de|tomado de|based on|adapted from|copied from|taken from|fork of|port of)\b", re.I)
AI_GEN = re.compile(
    r"(as an ai language model|como modelo de lenguaje|como ia,? no puedo|generado (?:por|con) (?:chatgpt|grok|claude|gemini|deepseek|ia)|"
    r"generated (?:by|with) (?:chatgpt|grok|claude|gemini|deepseek|ai)|aqui tienes|here is (?:a|the|your)|espero que (?:esto|te) (?:te )?(?:sirva|ayude)|"
    r"¿quieres que|would you like me to)",
    re.I,
)
EXTERNAL_COPYRIGHT = re.compile(r"(?:copyright\b|©)\s*(?:\(c\)\s*)?(?:(?:19|20)\d\d\s*)?([^\n]{0,80})", re.I)
URL = re.compile(r"https?://\S+|\b[\w.-]+\.(?:com|org|net|io|es)/\S*")


def _is_owner(s: str) -> bool:
    t = re.sub(r"[^a-z]", "", plain(s))
    return any(o in t for o in ("lazarolopezpaz", "lopezpaz", "canelon"))


def _sentences(text: str):
    for ln, line in enumerate(text.splitlines(), 1):
        for s in re.split(r"(?<=[.!?])\s+", line):
            s = s.strip()
            if len(s) > 12:
                yield ln, s


def _f(kind, sev, file, line, msg, quote="", **extra):
    d = {"kind": kind, "severity": sev, "file": file, "line": line, "message": msg, "quote": quote[:240]}
    d.update(extra)
    return d


# ---------------- revisiones por archivo (lo que ejecuta cada sub-agente) ----------------

def _is_bibliography_path(rel: str) -> bool:
    """True si el path es una lista o carpeta de referencias/bibliografía (no afirmaciones propias).

    Cubre nombres tipo referencias.md / bibliography.txt y carpetas refs/, references/,
    bibliografia/ (p. ej. C-VIB-003/refs/xia2020.txt con títulos que mencionan 'free energy').
    """
    parts = rel.replace("\\", "/").split("/")
    name = parts[-1]
    if re.match(r"(referencias|references|bibliograf)", name, re.I):
        return True
    for part in parts[:-1]:
        if re.fullmatch(r"refs?|references?|referencias|bibliograf\w*", part, re.I):
            return True
    return False


def claims_in_file(rel: str, text: str) -> list[dict]:
    out = []
    is_ref_list = _is_bibliography_path(rel)
    for ln, s in _sentences(text):
        p = plain(s)
        cited = bool(CITE.search(s))
        for w in PHYSICS:
            if is_ref_list:  # títulos de obras citadas (p. ej. Sarfatti 2015 'Retro-Causal…'), no afirmaciones propias
                break
            if w in p and not (w in ("energia libre", "free energy") and (GIBBS.search(p) or DFT_OUTPUT.search(p))):
                if HYPOTHESIS.search(p):  # etiquetada como hipótesis/E0: sigue visible, pero no es una afirmación oculta
                    out.append(_f("physics_hypothesis", "medium", rel, ln, f"afirmación extraordinaria ('{w}') etiquetada como hipótesis E0", s))
                else:
                    out.append(_f("physics", "high", rel, ln, f"afirmación física extraordinaria ('{w}') sin evidencia experimental", s))
                break
        for w in HYPE:
            if w in p:
                out.append(_f("hype", "medium", rel, ln, f"superlativo / afirmación absoluta ('{w}')", s))
                break
        if not cited and any(w in p for w in VALIDATION_WORDS):
            out.append(_f("validation", "medium", rel, ln, "dice 'validado/demostrado' sin cita ni dato reproducible", s))
        if not cited and UNIT.search(s):
            out.append(_f("number", "low", rel, ln, "cifra cuantitativa sin fuente ni cálculo enlazado", s))
    return out


def missing_in_file(rel: str, text: str) -> list[dict]:
    out = []
    p = plain(text)
    pend = len(re.findall(r"pendiente: en drive", p))
    if pend:
        out.append(_f("drive_pending", "medium", rel, 0, f"{pend} archivo(s) siguen solo en Drive (binarios no convertidos)", count=pend))
    for ln, line in enumerate(text.splitlines(), 1):
        if re.search(r"\b(todo|tbd|fixme|por hacer|pendiente de|to be done|xxx)\b", plain(line)) and "pendiente: en drive" not in plain(line):
            out.append(_f("todo", "low", rel, ln, "marcador de trabajo pendiente", line.strip()))
    return out


def license_in_file(rel: str, text: str) -> list[dict]:
    out = []
    lines = text.splitlines()
    for ln, line in enumerate(lines, 1):
        p = plain(line)
        if "choca con la licencia mit" in p:  # nota de revisión ya escrita en el README
            continue
        for phrase, sev in RESERVED:
            if phrase in p:
                out.append(_f("reserved_clause", sev, rel, ln, f"cláusula '{phrase}' incoherente con la licencia MIT del repositorio", line.strip()))
                break
        if rel != "LICENSE":
            m = EXTERNAL_COPYRIGHT.search(line)
            if m and not _is_owner(line):
                out.append(_f("foreign_copyright", "medium", rel, ln, "aviso de copyright de un tercero: conservarlo y citarlo en NOTICE", line.strip()))
        pn = URL.sub(" ", p)
        for name, rx in _TP_RE.items():
            if rx.search(pn):
                out.append(_f("third_party", "info", rel, ln, f"menciona a un tercero ({THIRD_PARTY[name]}): {name}", line.strip(), name=name))
        reviewed = '"revision_licencia"' in line  # par revisado y atribuido (2026-10-21): queda como info, no se oculta
        if DERIVED.search(line) and (re.search(r"https?://|github", p) or Path(rel).suffix in CODE_EXT):
            if reviewed:
                out.append(_f("derived_reviewed", "info", rel, ln, "deriva de otra fuente: revisado con atribución (revision_licencia)", line.strip()))
            else:
              out.append(_f("derived", "medium", rel, ln, "indica que el contenido deriva de otra fuente: verificar licencia y atribución", line.strip()))
        if AI_GEN.search(p):
            if reviewed:
                out.append(_f("ai_text_reviewed", "info", rel, ln, "huella de IA revisada y declarada (revision_licencia)", line.strip()))
            else:
              out.append(_f("ai_text", "medium", rel, ln, "texto con huella de asistente de IA: revisar autoría y no presentarlo como redacción propia sin indicarlo", line.strip()))
    return out


PER_FILE = {"review_claims": claims_in_file, "missing_pieces": missing_in_file, "license_check": license_in_file}


def files_for(kind: str, index, pid: str) -> list[Path]:
    if kind == "review_claims":
        return [p for p in index.doc_files(pid) if p.name not in ("LICENSE", "NOTICE")]
    if kind == "missing_pieces":
        return [p for p in index.doc_files(pid) if p.name not in ("LICENSE", "NOTICE")]
    return index.files(pid)


# ---------------- revisiones de proyecto (tras fusionar los sub-agentes) ----------------

def project_level(kind: str, index, project: dict, findings: list[dict]) -> list[dict]:
    pid = project["id"]
    files = index.files(pid)
    names = [str(p.relative_to(index.root / pid)) for p in files]
    docs_text = "\n".join(index.read(p) for p in index.doc_files(pid))
    dtp = plain(docs_text)
    extra = []
    if kind == "missing_pieces":
        code = [n for n in names if Path(n).suffix in CODE_EXT and Path(n).suffix not in (".json", ".yaml", ".yml", ".toml")]
        tests = [n for n in names if re.search(r"(^|/)(test_|tests?/)|_test\.py$", n)]
        if "LICENSE" not in names:
            extra.append(_f("no_license", "high", "-", 0, "no hay archivo LICENSE"))
        if not code:
            extra.append(_f("no_code", "high", "-", 0, "no hay código ni simulación: el proyecto es solo documental"))
        elif not tests:
            extra.append(_f("no_tests", "medium", "-", 0, f"hay {len(code)} archivo(s) de código pero ningún test"))
        if code and not any(n.endswith(("requirements.txt", "pyproject.toml", "package.json", "Cargo.toml")) for n in names) and any(n.endswith(".py") for n in code):
            extra.append(_f("no_requirements", "low", "-", 0, "código Python sin requirements.txt/pyproject: no es reproducible"))
        if not re.search(r"referencias|references|bibliograf|doi|arxiv|et al", dtp):
            extra.append(_f("no_references", "high", "-", 0, "ninguna referencia bibliográfica en los documentos"))
        if not re.search(r"resultado|experiment|medicion|medida|ensayo|prototipo|validaci|benchmark|results", dtp):
            extra.append(_f("no_validation", "medium", "-", 0, "no se describen resultados experimentales, prototipos ni validación"))
        if len(docs_text) < 1500:
            extra.append(_f("thin_docs", "high", "-", 0, f"documentación mínima ({len(docs_text)} caracteres)"))
        for b in project.get("broken_paths", []):
            extra.append(_f("broken_path", "high", "-", 0, f"archivo con nombre roto en GitHub: {b}"))
    if kind == "review_claims" and project.get("tools"):
        extra += tool_crosscheck(project, findings)
    if kind == "license_check":
        has_notice = any(n in ("NOTICE", "NOTICE.md", "ATTRIBUTION.md", "THIRD_PARTY.md") for n in names)
        lic_mit = project.get("license") == "MIT"
        if not lic_mit and project.get("license_declared_by_author"):
            # el autor decidió conservar la licencia que declaran sus documentos:
            # las cláusulas de reserva/patente/CC/Apache ya no chocan con el repo
            for f in findings:
                if f["kind"] == "reserved_clause":
                    f["kind"], f["severity"] = "declared_license", "info"
                    f["message"] = f"cláusula coherente con la licencia declarada del repositorio ({project.get('license')})"
            extra.append(_f("declared_license", "info", "-", 0, f"licencia del repo: {project.get('license')} (declarada por el autor)"))
        elif not lic_mit:
            extra.append(_f("no_mit", "high", "-", 0, f"licencia del repo: {project.get('license')} (se esperaba MIT)"))
        mentioned = sorted({f["name"] for f in findings if f["kind"] == "third_party"})
        need = [n for n in mentioned if n in NEEDS_NOTICE]
        if need and not has_notice:
            extra.append(_f("missing_attribution", "high", "-", 0, f"usa o cita trabajo de terceros ({', '.join(need)}) y no hay NOTICE con atribución"))
        if any(f["kind"] == "derived" for f in findings) and not has_notice:
            extra.append(_f("missing_attribution", "medium", "-", 0, "hay contenido marcado como derivado y no hay NOTICE"))
        imports = set()
        for p in index.code_files(pid):
            if p.suffix == ".py":
                imports |= set(re.findall(r"^\s*(?:from|import)\s+([a-zA-Z_]\w*)", index.read(p), re.M))
        thirdlibs = sorted(imports & {"qiskit", "torch", "tensorflow", "pennylane", "cirq", "streamlit", "sklearn", "numpy", "scipy", "matplotlib", "pandas", "flask", "fastapi", "transformers", "oqs", "cryptography", "pyscf", "rdkit"})
        if thirdlibs and not has_notice:
            extra.append(_f("deps_undeclared", "low", "-", 0, f"depende de librerías de terceros ({', '.join(thirdlibs)}): listar sus licencias en NOTICE"))
    return extra


def tool_crosscheck(project: dict, findings: list[dict], limit: int = 5) -> list[dict]:
    """Recalcula con las herramientas físicas locales las cifras que encajan con ellas."""
    try:
        from ags_local import get_engine
        reg = get_engine().registry
    except Exception:  # motor local no disponible
        return []
    out = []
    for f in findings:
        if f["kind"] != "number" or len(out) >= limit:
            continue
        for tid in project["tools"]:
            hit = reg.match_tool(tid, f["quote"])
            if not hit:
                continue
            name, fn = hit
            try:
                res = fn(f["quote"])
            except Exception as exc:  # una herramienta no debe tumbar la revisión
                res = f"error: {exc}"
            q = plain(f["quote"]).lstrip()
            weak = ("falta", "error", "no calculada", "sin precio", "no hay")
            if q.startswith(("{", "|")) or ("mwh" in q and name.startswith(("produccion", "mw_"))):
                break
            if res and not any(w in res.lower() for w in weak):
                out.append(_f("tool_check", "info", f["file"], f["line"],
                              f"recalculado con {tid}.{name}: comparar con la cifra del documento",
                              f["quote"], tool_output=res[:600]))
            break
    return out


SEV_ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}


def score(findings: list[dict]) -> dict:
    c = {k: 0 for k in SEV_ORDER}
    for f in findings:
        c[f["severity"]] += 1
    return c


def collapse_third_party(findings: list[dict]) -> list[dict]:
    """Una entrada por tercero mencionado, con número de menciones y archivos."""
    agg, rest = {}, []
    for f in findings:
        if f["kind"] != "third_party":
            rest.append(f)
            continue
        a = agg.setdefault(f["name"], dict(f, count=0, files=[]))
        a["count"] += 1
        if f["file"] not in a["files"]:
            a["files"].append(f["file"])
    for name, a in agg.items():
        a["message"] = (f"menciona a {name} ({THIRD_PARTY[name]}) {a['count']} vez/veces en {len(a['files'])} archivo(s): "
                        "citar como referencia o marca de terceros; no presentar su trabajo como propio")
        rest.append(a)
    return rest


def dedupe(findings: list[dict]) -> list[dict]:
    findings = collapse_third_party(findings)
    seen, out = set(), []
    for f in findings:
        key = (f["kind"], f["file"], f["line"], f.get("name", ""))
        if key not in seen:
            seen.add(key)
            out.append(f)
    out.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["file"], f["line"]))
    return out
