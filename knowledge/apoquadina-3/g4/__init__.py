"""g4: búsqueda de motivos G-cuádruplex con la regla de Huppert y Balasubramanian (2005), G3+ N1-7 G3+ N1-7 G3+ N1-7 G3+, en las dos hebras. El ejemplo público es la repetición telomérica humana; la diana G4 del autor está pendiente.

Referencias (verificadas):
Huppert J.L., Balasubramanian S. (2005) Prevalence of quadruplexes in the human genome. Nucleic Acids Res. 33, 2908-2916. doi:10.1093/nar/gki609
Moyzis R.K. et al. (1988) A highly conserved repetitive DNA sequence, (TTAGGG)n, present at the telomeres of human chromosomes. PNAS 85, 6622. doi:10.1073/pnas.85.18.6622

Autor del código: Lázaro López Paz, El Prat de Llobregat, Barcelona, España, con asistencia de IA. ORCID 0000-0001-8601-1963. Licencia MIT.
"""
import re
from .pendientes import cargar, dato

PATRON = re.compile(r"(?=(G{3,}[ACGTN]{1,7}?G{3,}[ACGTN]{1,7}?G{3,}[ACGTN]{1,7}?G{3,}))")


def revcomp(s):
    return s.translate(str.maketrans("ACGTN", "TGCAN"))[::-1]


def find_g4(seq):
    s = seq.upper().replace("U", "T")
    if set(s) - set("ACGTN"):
        raise ValueError("secuencia con caracteres no válidos")
    hits = [("+", m.start(), m.group(1)) for m in PATRON.finditer(s)]
    rc = revcomp(s)
    hits += [("-", len(s) - m.start() - len(m.group(1)), m.group(1)) for m in PATRON.finditer(rc)]
    return hits


def run(cfg=None):
    cfg = cfg or cargar()
    s, o = dato(cfg, "secuencia_diana")
    return {"motivos": find_g4(s), "origen": o}
