#!/usr/bin/env python3
"""Dossier completo OMNISCIENCE: portada + metadatos + anexos (maestro, MV1, C-VIB)."""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image as PILImage
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Raíz configurable (antes fija en /workspace, la raíz del proyecto web OMNISCIENCE).
# OMNISCIENCE_DOSSIER_ROOT=<dir> (por defecto "."); debe contener public/ y .grok/ como la web original.
ROOT = Path(os.environ.get("OMNISCIENCE_DOSSIER_ROOT", "."))
PUBLIC = ROOT / "public"
STAGE = ROOT / ".grok" / "OMNISCIENCE_dossier_front.pdf"
OUT = ROOT / "public" / "docs" / "OMNISCIENCE_dossier_completo.pdf"

NAVY = HexColor("#0c1016")
TEAL = HexColor("#2a9d8f")
MUTED = HexColor("#5c6864")
LINE = HexColor("#2a3438")
PAPER = HexColor("#f4f6f4")
OK = HexColor("#3d9b74")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerifBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuMono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))


def styles():
    base = getSampleStyleSheet()
    s = {
        "cover_kicker": ParagraphStyle(
            "cover_kicker", fontName="DejaVu", fontSize=9, textColor=TEAL,
            tracking=2, alignment=TA_CENTER, spaceAfter=8,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", fontName="DejaVuSerifBold", fontSize=28, textColor=NAVY,
            alignment=TA_CENTER, leading=34, spaceAfter=6,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub", fontName="DejaVuSerif", fontSize=12, textColor=MUTED,
            alignment=TA_CENTER, leading=16, spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "h1", fontName="DejaVuSerifBold", fontSize=16, textColor=NAVY,
            spaceBefore=16, spaceAfter=8, leading=20,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="DejaVuBold", fontSize=12, textColor=TEAL,
            spaceBefore=12, spaceAfter=6, leading=16,
        ),
        "body": ParagraphStyle(
            "body", fontName="DejaVu", fontSize=9.5, textColor=NAVY,
            alignment=TA_JUSTIFY, leading=13.5, spaceAfter=7,
        ),
        "caption": ParagraphStyle(
            "caption", fontName="DejaVu", fontSize=8, textColor=MUTED,
            alignment=TA_CENTER, spaceBefore=3, spaceAfter=10,
        ),
        "cell": ParagraphStyle(
            "cell", fontName="DejaVu", fontSize=8, textColor=NAVY, leading=11,
        ),
        "cellb": ParagraphStyle(
            "cellb", fontName="DejaVuBold", fontSize=8, textColor=NAVY, leading=11,
        ),
        "mono": ParagraphStyle(
            "mono", fontName="DejaVuMono", fontSize=7.5, textColor=NAVY, leading=10.5,
        ),
        "foot": ParagraphStyle(
            "foot", fontName="DejaVu", fontSize=8, textColor=MUTED, alignment=TA_CENTER,
        ),
    }
    return s


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 14 * mm, A4[0], 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(22 * mm, A4[1] - 9 * mm, "OMNISCIENCE")
    canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 9 * mm, "Dossier completo")
    canvas.setFillColor(TEAL)
    canvas.rect(0, 0, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(22 * mm, 4.5 * mm, "Lázaro López Paz  ·  28 agosto 2026")
    canvas.drawRightString(A4[0] - 22 * mm, 4.5 * mm, str(doc.page))
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    og = str(PUBLIC / "og.jpg")
    w = A4[0]
    h = w * 630 / 1200
    canvas.drawImage(og, 0, A4[1] - h - 8 * mm, width=w, height=h, preserveAspectRatio=True, anchor="n")
    y = A4[1] - h - 22 * mm
    canvas.setFillColor(TEAL)
    canvas.setFont("DejaVu", 9)
    canvas.drawCentredString(A4[0] / 2, y, "DOSSIER COMPLETO")
    canvas.setFillColor(white)
    canvas.setFont("DejaVuSerifBold", 26)
    canvas.drawCentredString(A4[0] / 2, y - 16 * mm, "OMNISCIENCE")
    canvas.setFont("DejaVuSerif", 11)
    canvas.drawCentredString(A4[0] / 2, y - 24 * mm, "Universal Autonomous Scientific Discovery Engine")
    canvas.setFont("DejaVu", 9)
    canvas.drawCentredString(A4[0] / 2, y - 34 * mm,
                             "Arquitectura · MV1 · C-VIB-001 · Python · PROV-O")
    canvas.drawCentredString(A4[0] / 2, y - 40 * mm,
                             "Open Graph · Twitter Cards · JSON-LD · zonas seguras")
    canvas.setFillColor(TEAL)
    canvas.rect(0, 38 * mm, A4[0], 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont("DejaVu", 8)
    canvas.drawCentredString(A4[0] / 2, 28 * mm, "LÁZARO LÓPEZ PAZ")
    canvas.drawCentredString(A4[0] / 2, 20 * mm, "28 agosto 2026  ·  El Prat de Llobregat")
    canvas.restoreState()


def table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, 0), "DejaVuBold"),
                ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 1), (-1, -1), NAVY),
                ("BACKGROUND", (0, 1), (-1, -1), PAPER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
            ]
        )
    )
    return t


def img(path: Path, width, max_height=None):
    with PILImage.open(path) as raw:
        iw, ih = raw.size
    height = width * ih / iw
    if max_height and height > max_height:
        scale = max_height / height
        height = max_height
        width = width * scale
    return Image(str(path), width=width, height=height)


def build_front() -> int:
    S = styles()
    story = []
    usable = A4[0] - 44 * mm

    story.append(PageBreak())

    story.append(Paragraph("1. Cómo leer este dossier", S["h1"]))
    story.append(Paragraph(
        "Este PDF reúne todo el paquete OMNISCIENCE a 28 de agosto de 2026: la plataforma viva "
        "(motores, proyectos, campaña adversarial), el documento maestro de arquitectura, la "
        "implementación técnica MV1, el informe de vibraciones C-VIB-001 y la capa de publicación "
        "(Open Graph, Twitter Cards, Schema.org JSON-LD y zonas seguras de Stories, Reels, TikTok, "
        "LinkedIn y X). No es un pitch: cada afirmación arrastra un nivel de evidencia.",
        S["body"],
    ))
    story.append(table(
        [
            [Paragraph("Bloque", S["cellb"]), Paragraph("Contenido", S["cellb"]), Paragraph("Páginas", S["cellb"])],
            [Paragraph("I. Dossier", S["cell"]), Paragraph("Identidad, motores, metadatos, zonas", S["cell"]), Paragraph("este bloque", S["cell"])],
            [Paragraph("Anexo A", S["cell"]), Paragraph("Documento maestro de arquitectura (LaTeX)", S["cell"]), Paragraph("23", S["cell"])],
            [Paragraph("Anexo B", S["cell"]), Paragraph("OMNISCIENCE-MV1 implementación técnica", S["cell"]), Paragraph("7", S["cell"])],
            [Paragraph("Anexo C", S["cell"]), Paragraph("Análisis científico de vibraciones C-VIB-001", S["cell"]), Paragraph("11", S["cell"])],
        ],
        [3.2 * cm, 10.2 * cm, 3.4 * cm],
    ))

    story.append(Paragraph("2. Niveles de evidencia", S["h1"]))
    story.append(Paragraph(
        "La plataforma crece por evidencia, no por promesas. Cada motor nuevo debe superar el mismo "
        "ciclo: hipótesis, predicción, falsación, réplica, auditoría y publicación.",
        S["body"],
    ))
    evid = [["Nivel", "Nombre", "Significado"]]
    rows = [
        ("0", "Idea", "Concepto sin evaluación formal."),
        ("1", "Hipótesis", "Propuesta falsable."),
        ("2", "Predicción", "Resultado de un modelo o algoritmo."),
        ("3", "Simulación verificada", "Reproducible bajo condiciones definidas."),
        ("4", "Observación experimental", "Medición documentada."),
        ("5", "Réplica independiente", "Confirmado por otra ruta."),
        ("6", "Conocimiento consolidado", "Evidencia convergente con límites explícitos."),
    ]
    for a, b, c in rows:
        evid.append([Paragraph(a, S["cellb"]), Paragraph(b, S["cell"]), Paragraph(c, S["cell"])])
    story.append(table(evid, [2.2 * cm, 4.6 * cm, 10 * cm]))

    story.append(Paragraph("3. Nueve motores", S["h1"]))
    mot = [["Motor", "Estado", "Contrato"]]
    engines = [
        ("Universal Matter", "MVP activo", "Eform = Etotal − Σ ni μi. MLIP MACE, fallback DFT."),
        ("Vibrational & Phonon", "C-VIB-001 E3", "D(q) eν = ων² eν. Phonopy en el orquestador."),
        ("Quantum Dynamics", "Contrato J(ω)", "ρ̇ = −i/ℏ [H,ρ] + Σ Dk(ρ)."),
        ("Quantum Sensing", "Especificado", "η ∝ Δν / (C √R)."),
        ("Metamaterial", "Oráculo 1D", "x* = arg min L[F(x), y]."),
        ("Energy & Environment", "Radar", "S = wI I + wF F − wC C."),
        ("Bio & Therapeutic", "Aprobación humana", "IR/Raman antes de cualquier célula."),
        ("Fusion Digital Twin", "Hoja UKAEA", "κL = ⅓ Σ Cν vν² τν."),
        ("Innovation Radar", "Grafo", "U(e) = E[ΔI] Pdisc V / (C R)."),
    ]
    for a, b, c in engines:
        mot.append([Paragraph(a, S["cellb"]), Paragraph(b, S["cell"]), Paragraph(c, S["cell"])])
    story.append(table(mot, [4.4 * cm, 3.4 * cm, 9 * cm]))

    story.append(Paragraph("4. Proyectos unificados", S["h1"]))
    story.append(Paragraph(
        "El ZIP unificado (maestro, LaTeX, C-VIB-001, figuras, Python, animación) y el PDF MV1 "
        "quedan heredados por todas las líneas. Ningún proyecto salta el orquestador.",
        S["body"],
    ))
    proj = [["Proyecto", "Dominio", "N", "Papel de MV1"]]
    projects = [
        ("OMNISCIENCE-MV1", "Plataforma", "3", "SQL PROV-O, MLIP, DFT adversarial, Phonopy."),
        ("C-VIB-001", "Calibración", "3", "Banco de modos canónicos antes de una celda real."),
        ("Helio-3 / HelioAtlas", "Energía y espacio", "1", "Candidatos BN–He3 por Eform y modos imaginarios."),
        ("Lázaro Drive / MEI-RIT", "Propulsión", "1", "Rejilla y YIG se relajan aquí; no se confunde RF con modo estructural."),
        ("YIG magnetoelástico", "Metamateriales", "1", "Proxy Y3Fe5O12. Gap magnetoelástico exige D(q) estable."),
        ("Lentes acústicas", "Fonónica", "2", "Cristal 1D como oráculo barato previo a FEM."),
        ("MetaNO Quantum Patch", "Nanomedicina", "1", "Modos moleculares. IR/Raman no se sustituye."),
        ("NEUROPLASTIN / MITOGUARD", "Nanomedicina", "0", "Sin modelo molecular no hay campaña Matter."),
    ]
    for a, b, c, d in projects:
        proj.append([Paragraph(a, S["cellb"]), Paragraph(b, S["cell"]), Paragraph(c, S["cellb"]), Paragraph(d, S["cell"])])
    story.append(table(proj, [4.6 * cm, 3.2 * cm, 1.2 * cm, 7.8 * cm]))

    story.append(Paragraph("5. MV1 — orquestador adversarial", S["h1"]))
    story.append(Paragraph(
        "El orquestador relaja la celda, calcula Eform, genera superceldas, predice fuerzas con MLIP "
        "(MACE) y, si max |F| > 10 eV/Å, llama a DFT. Phonopy cierra con modos imaginarios. "
        "Toda actividad deja traza PROV-O (entidad, actividad, agente). El script "
        "<font name='DejaVuMono'>omniscience_mv1.py</font> es ejecutable: numpy real, ASE/Phonopy/VASP "
        "comentados como contrato de laboratorio.",
        S["body"],
    ))
    story.append(Paragraph(
        "Criterio de falsación: un modo imaginario o una fuerza MLIP fuera de umbral no se maquilla. "
        "Se clasifica <i>falsified</i> o se escala a Ab Initio. La campaña CAMP-2026-MV1 usa Si2 de prueba.",
        S["body"],
    ))

    story.append(Paragraph("6. C-VIB-001 — banco vibracional", S["h1"]))
    story.append(Paragraph(
        "H1–H6 no falsadas en este entorno: oscilador amortiguado, FFT/espectrograma, modos de cuerda "
        "Dirichlet, dispersión Born–von Karman, cristal 1D y oscilador armónico cuántico. Nivel 3 "
        "(simulación verificada, numpy/scipy). Figuras 01–09 y 11–12 en el anexo C; animación de modos "
        "en el paquete unificado (MP4, 6 s).",
        S["body"],
    ))
    figs = PUBLIC / "figs"
    row_imgs = []
    for name in ["01_oscilador_armonico.png", "03_modos_cuerda.png", "04_dispersion_fononica.png"]:
        p = figs / name
        if p.exists():
            row_imgs.append(img(p, usable / 3 - 4))
    if row_imgs:
        story.append(Table([row_imgs], colWidths=[usable / 3] * 3))
        story.append(Paragraph("Oscilador, modos de cuerda, dispersión fonónica (C-VIB-001).", S["caption"]))

    story.append(Paragraph("7. Scripts Python", S["h1"]))
    py = [["Archivo", "Rol", "Producto"]]
    scripts = [
        ("omniscience_mv1.py", "Orquestador MV1", "status + provenance_trace"),
        ("simular_vibraciones.py", "Banco C-VIB-001", "Figuras 01–09"),
        ("animar_modos.py", "Modos de cuerda", "MP4 6 s"),
        ("crear_informe_pdf.py", "Informe C-VIB", "PDF de 11 páginas"),
    ]
    for a, b, c in scripts:
        py.append([Paragraph(a, S["mono"]), Paragraph(b, S["cell"]), Paragraph(c, S["cell"])])
    story.append(table(py, [5.2 * cm, 5.2 * cm, 6.4 * cm]))

    story.append(Paragraph("8. Identidad Open Graph y Twitter Cards", S["h1"]))
    story.append(Paragraph(
        "Las etiquetas og:* y twitter:* las emite el inyector de publicación, no la app. "
        "Título, lema e imagen están alineados. LinkedIn, Facebook, Slack y WhatsApp leen solo OG. "
        "X lee twitter:* y, si faltan, cae a OG. Descripción recortable a 94 caracteres (cabe en el "
        "preview de ~110 de Facebook).",
        S["body"],
    ))
    ogt = [["Etiqueta", "Valor"]]
    tags = [
        ("og:title / twitter:title", "OMNISCIENCE"),
        ("og:description", "OMNISCIENCE descubre materia y fonones: hipótesis, predicción, falsación y procedencia PROV-O."),
        ("og:type", "website"),
        ("og:locale", "es_ES"),
        ("og:image", "/og.jpg · 1200×630 JPEG · type image/jpeg · alt fonónico"),
        ("twitter:card", "summary_large_image"),
        ("twitter:site / creator", "omitidos (no se inventa un @handle)"),
        ("x:game:image", "/x-banner.jpg · 1200×264 (cabecera, no es la card)"),
    ]
    for a, b in tags:
        ogt.append([Paragraph(a, S["mono"]), Paragraph(b, S["cell"])])
    story.append(table(ogt, [5.6 * cm, 11.2 * cm]))
    story.append(Spacer(1, 4 * mm))
    story.append(img(PUBLIC / "og.jpg", usable))
    story.append(Paragraph("og.jpg · 1200×630 · zona inferior navy para overlay de dominio.", S["caption"]))
    story.append(img(PUBLIC / "x-banner.jpg", usable))
    story.append(Paragraph("x-banner.jpg · 1200×264 · cabecera de perfil X (50:11).", S["caption"]))

    story.append(Paragraph("9. Schema.org JSON-LD", S["h1"]))
    story.append(Paragraph(
        "Un grafo de siete nodos viaja en el HTML como <font name='DejaVuMono'>application/ld+json</font>. "
        "Google y Bing lo leen; LinkedIn y X no. Sin valoraciones inventadas ni URL absoluta hasta publicar.",
        S["body"],
    ))
    ld = [["@id", "@type", "Qué es"]]
    nodes = [
        ("#author", "Person", "Lázaro López Paz, crédito de los documentos"),
        ("#website", "WebSite", "Sitio, inLanguage es"),
        ("#app", "WebApplication + SoftwareApplication", "Producto, ScienceApplication, precio 0"),
        ("#mv1", "SoftwareSourceCode", "omniscience_mv1.py"),
        ("#cvib", "Dataset", "C-VIB-001, evidencia 3"),
        ("#engines", "ItemList", "Nueve motores"),
        ("#projects", "ItemList", "Paquete unificado"),
    ]
    for a, b, c in nodes:
        ld.append([Paragraph(a, S["mono"]), Paragraph(b, S["cell"]), Paragraph(c, S["cell"])])
    story.append(table(ld, [2.8 * cm, 6.4 * cm, 7.6 * cm]))

    story.append(Paragraph("10. Zonas seguras (Stories, Reels, TikTok, feed, OG, X)", S["h1"]))
    story.append(Paragraph(
        "Instagram y TikTok no usan Open Graph en el feed: se sube el JPEG. El lockup de OMNISCIENCE "
        "(720×260 centrado en 1080×1920) entra en todas las ventanas siguientes. Veredicto: "
        "<b>lockup dentro</b> en Stories, Reels, TikTok, feed 4:5, OG LinkedIn y X large.",
        S["body"],
    ))
    z = [["Formato", "Lienzo", "Peligro", "Lockup"]]
    zones = [
        ("Stories", "1080×1920", "268 px arriba, 384 px abajo", "60 % central"),
        ("Reels", "1080×1920", "rail derecho 132 px + pie 320 px", "centro, izq. del rail"),
        ("TikTok", "1080×1920", "rail 140 px + pie 400 px + Para ti 140 px", "40 px del rail, 460 px del pie"),
        ("Feed 4:5", "1080×1350", "perfil recorta 135 px arriba/abajo al 1:1", "cuadrado central"),
        ("OG LinkedIn", "1200×630", "72 px inferiores (dominio)", "centro; retículo no abajo"),
        ("X large", "1200×630", "recorte 2:1 (~3 % vertical)", "centro; 50:11 es otra pieza"),
    ]
    for a, b, c, d in zones:
        z.append([Paragraph(a, S["cellb"]), Paragraph(b, S["mono"]), Paragraph(c, S["cell"]), Paragraph(d, S["cell"])])
    story.append(table(z, [3.2 * cm, 3.2 * cm, 6.4 * cm, 4 * cm]))
    story.append(Spacer(1, 3 * mm))
    ig = PUBLIC / "instagram"
    names = [
        ("feed-1080.jpg", "1:1 · 1080"),
        ("feed-4x5.jpg", "4:5 · 1080×1350"),
        ("story-9x16.jpg", "9:16 · Stories/TikTok"),
    ]
    pics, caps = [], []
    for name, cap in names:
        p = ig / name
        if p.exists():
            pics.append(img(p, usable / 3 - 8, max_height=6.5 * cm))
            caps.append(Paragraph(cap, S["caption"]))
    if pics:
        story.append(Table([pics, caps], colWidths=[usable / 3] * len(pics)))

    story.append(Paragraph("11. Ciclo de crecimiento", S["h1"]))
    story.append(Paragraph(
        "Cada motor nuevo deberá superar el mismo ciclo de hipótesis, predicción, falsación, réplica, "
        "auditoría y publicación científica. Nada entra al grafo por promesa. El crédito de autoría "
        "de los documentos, patentes y de este dossier es de Lázaro López Paz; si alguien continúa "
        "el trabajo, mencione a Lázaro López Paz y a Grok.",
        S["body"],
    ))
    story.append(Paragraph(
        "Anexos a continuación: (A) documento maestro LaTeX, (B) implementación MV1, (C) informe C-VIB-001.",
        S["body"],
    ))

    STAGE.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(STAGE),
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title="OMNISCIENCE — Dossier completo",
        author="Lázaro López Paz",
        subject="Arquitectura, MV1, C-VIB-001, metadatos y zonas seguras",
        creator="OMNISCIENCE / Grok Build",
    )
    doc.build(story, onFirstPage=cover_page, onLaterPages=header_footer)
    n = len(PdfReader(str(STAGE)).pages)
    print(f"front pages: {n}")
    return n


def merge(front_pages: int) -> None:
    writer = PdfWriter()
    front = PdfReader(str(STAGE))
    maestro = PdfReader(str(PUBLIC / "docs" / "OMNISCIENCE_maestro_unificado.pdf"))
    mv1 = PdfReader(str(PUBLIC / "docs" / "OMNISCIENCE-MV1-implementacion.pdf"))
    cvib = PdfReader(str(PUBLIC / "docs" / "Analisis_vibraciones_cientificas_Grok.pdf"))

    for p in front.pages:
        writer.add_page(p)
    a0 = len(writer.pages)
    for p in maestro.pages:
        writer.add_page(p)
    b0 = len(writer.pages)
    for p in mv1.pages:
        writer.add_page(p)
    c0 = len(writer.pages)
    for p in cvib.pages:
        writer.add_page(p)

    writer.add_outline_item("I. Dossier — identidad, motores, metadatos, zonas", 0)
    writer.add_outline_item("Anexo A — Documento maestro de arquitectura", a0)
    writer.add_outline_item("Anexo B — OMNISCIENCE-MV1 implementación técnica", b0)
    writer.add_outline_item("Anexo C — Análisis científico de vibraciones C-VIB-001", c0)

    writer.add_metadata({
        "/Title": "OMNISCIENCE — Dossier completo",
        "/Author": "Lázaro López Paz",
        "/Subject": "Arquitectura, MV1, C-VIB-001, Open Graph, JSON-LD y zonas seguras",
        "/Keywords": "OMNISCIENCE, PROV-O, fonones, Open Graph, TikTok, Instagram, JSON-LD",
        "/Creator": "OMNISCIENCE / Grok Build",
    })

    tmp = ROOT / ".grok" / "OMNISCIENCE_dossier_completo.pdf"
    with tmp.open("wb") as f:
        writer.write(f)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(tmp.read_bytes())
    print(f"wrote {OUT}  pages={len(writer.pages)}  bytes={OUT.stat().st_size}")


if __name__ == "__main__":
    n = build_front()
    merge(n)
