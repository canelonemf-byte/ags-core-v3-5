#!/usr/bin/env python3
"""Informe PDF: Análisis científico de vibraciones (lo que un chat de texto no entrega).

Nota de autoría: autor Lázaro López Paz. Texto y código asistidos por IA (herramienta: Grok, de xAI),
revisados por el autor (revisión PENDIENTE DE VERIFICACIÓN). Se conserva la declaración original
de atribución en la tabla de metadatos del informe (fila «Atribución»).
"""
import os
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Rutas configurables (antes fijas en /home/workdir/artifacts/vibraciones).
# VIBRACIONES_ROOT=<dir> (por defecto ./out); figuras en <ROOT>/figs, PDF en <ROOT>/report/.
ROOT = Path(os.environ.get("VIBRACIONES_ROOT", "out"))
FIGS = Path(os.environ.get("VIBRACIONES_OUT", str(ROOT / "figs")))
OUT = ROOT / "report" / "Analisis_vibraciones_cientificas_Grok.pdf"

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuBold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSerifBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuMono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))

NAVY = colors.HexColor("#0b2545")
TEAL = colors.HexColor("#0d7377")
GOLD = colors.HexColor("#c9a227")
INK = colors.HexColor("#1a2332")
MUTED = colors.HexColor("#5b6b7a")
BG = colors.HexColor("#eef3f7")
LINE = colors.HexColor("#c5d0da")

PAGE_W, PAGE_H = A4


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 12 * mm, PAGE_W, 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, PAGE_H - 12.6 * mm, PAGE_W, 1.6 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(16 * mm, PAGE_H - 8 * mm, "Análisis científico de vibraciones  ·  Grok × Lázaro López Paz")
    canvas.drawRightString(PAGE_W - 16 * mm, PAGE_H - 8 * mm, "Documento reproducible")

    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 10 * mm, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.rect(0, 10 * mm, PAGE_W, 1.1 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("DejaVu", 8)
    canvas.drawString(16 * mm, 4 * mm, "No es un chat: simulaciones ejecutadas, figuras generadas, código adjunto")
    canvas.drawRightString(PAGE_W - 16 * mm, 4 * mm, f"pág. {doc.page}")
    canvas.restoreState()


def styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(
        "CoverKicker", fontName="DejaVu", fontSize=9, textColor=TEAL,
        alignment=TA_CENTER, spaceAfter=4 * mm, tracking=1.2,
    ))
    ss.add(ParagraphStyle(
        "CoverTitle", fontName="DejaVuBold", fontSize=22, leading=26,
        textColor=NAVY, alignment=TA_CENTER, spaceAfter=3 * mm,
    ))
    ss.add(ParagraphStyle(
        "CoverSub", fontName="DejaVu", fontSize=12, leading=16,
        textColor=MUTED, alignment=TA_CENTER, spaceAfter=2 * mm,
    ))
    ss.add(ParagraphStyle(
        "H1", fontName="DejaVuBold", fontSize=14, leading=18,
        textColor=NAVY, spaceBefore=6 * mm, spaceAfter=3 * mm,
        borderPadding=0,
    ))
    ss.add(ParagraphStyle(
        "H2", fontName="DejaVuBold", fontSize=12, leading=16,
        textColor=TEAL, spaceBefore=4 * mm, spaceAfter=2 * mm,
    ))
    ss.add(ParagraphStyle(
        "Body", fontName="DejaVu", fontSize=9.5, leading=13.4,
        textColor=INK, alignment=TA_JUSTIFY, spaceAfter=2.4 * mm,
    ))
    ss.add(ParagraphStyle(
        "Caption", fontName="DejaVu", fontSize=8, leading=11,
        textColor=MUTED, alignment=TA_CENTER, spaceBefore=1.2 * mm, spaceAfter=4 * mm,
    ))
    ss.add(ParagraphStyle(
        "Eq", fontName="DejaVu", fontSize=10, leading=15,
        textColor=NAVY, alignment=TA_CENTER, spaceBefore=2 * mm, spaceAfter=2 * mm,
        backColor=BG, borderPadding=4,
    ))
    ss.add(ParagraphStyle(
        "Note", fontName="DejaVu", fontSize=8.5, leading=12,
        textColor=INK, alignment=TA_LEFT, leftIndent=3 * mm, spaceAfter=2 * mm,
    ))
    ss.add(ParagraphStyle(
        "BulletBody", fontName="DejaVu", fontSize=9.3, leading=13,
        textColor=INK, alignment=TA_LEFT,
    ))
    ss.add(ParagraphStyle(
        "FooterTiny", fontName="DejaVu", fontSize=8, leading=11, textColor=MUTED,
    ))
    ss.add(ParagraphStyle(
        "CodeBlock", fontName="DejaVuMono", fontSize=7.6, leading=10.4,
        textColor=INK, backColor=BG, leftIndent=2 * mm, rightIndent=2 * mm,
    ))
    return ss


S = styles()


def P(text, style="Body"):
    return Paragraph(text, S[style])


def fig(name, caption, width=170 * mm):
    path = FIGS / name
    img = Image(str(path), width=width, height=width * 0.52)
    # better: keep aspect via ImageReader later if needed; most figs are ~11:7
    from reportlab.lib.utils import ImageReader
    ir = ImageReader(str(path))
    iw, ih = ir.getSize()
    h = width * ih / iw
    img = Image(str(path), width=width, height=h)
    return KeepTogether([img, Paragraph(caption, S["Caption"])])


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(it, S["BulletBody"]), leftIndent=8, value="•") for it in items],
        bulletType="bullet",
        start="•",
        leftIndent=12,
        spaceBefore=1 * mm,
        spaceAfter=3 * mm,
    )


def make():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="Análisis científico de vibraciones",
        author="Grok (xAI) para Lázaro López Paz",
        subject="Simulaciones, modos, fonones, espectroscopía y metamateriales",
    )
    story = []

    story.append(Spacer(1, 18 * mm))
    story.append(P("INFORME TÉCNICO REPRODUCIBLE  ·  28 AGOSTO 2026", "CoverKicker"))
    story.append(P("Analizar vibraciones científicas", "CoverTitle"))
    story.append(P(
        "Lo que un chat de texto no puede entregar: simulaciones ejecutadas,<br/>figuras generadas, animación modal, código y un marco de trabajo aplicable "
        "a metamateriales, fonónica, propulsión y nanomedicina.",
        "CoverSub",
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(fig("11_metamaterial_fononico.jpg",
                     "Figura 0. Metamaterial fonónico conceptual: campo de desplazamiento y canal de borde.",
                     width=155 * mm))

    meta = [
        [P("<b>Qué se entrega</b>"), P("9 figuras de simulación + 2 visuales + animación MP4 + código Python + este PDF")],
        [P("<b>Qué no es</b>"), P("Una respuesta conversacional. Es un paquete de trabajo cerrado y reproducible.")],
        [P("<b>Ámbito</b>"), P("Clásico → espectral → modal → fonónico → cuántico → experimental → aplicaciones")],
        [P("<b>Atribución</b>"), P("Análisis generado por Grok (xAI). Uso posterior: citar a Lázaro López Paz y a Grok.")],
        [P("<b>Autoría</b>"), P("Autor: Lázaro López Paz. Texto asistido por IA (herramienta: Grok, de xAI), revisado por el autor (revisión PENDIENTE DE VERIFICACIÓN).")],
    ]
    t = Table(meta, colWidths=[38 * mm, 140 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BG),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)

    # 1
    story.append(P("1. Por qué «analizar vibraciones» no cabe en un chat", "H1"))
    story.append(P(
        "Una IA conversacional puede <i>describir</i> la ecuación del oscilador armónico. No puede, en el mismo acto, "
        "integrar el sistema forzado, calcular la FFT de una señal con chirp y burst, extraer un espectrograma, "
        "dibujar las ramas acústica y óptica de una red diatómica, estimar la transmisión de un cristal fonónico "
        "de 12 celdas, renderizar modos de membrana, generar una animación de superposición modal y empaquetarlo "
        "en un PDF listo para archivo. Eso es exactamente lo que este documento hace."
    ))
    story.append(P(
        "En física, «vibración científica» no es una metáfora. Es el movimiento periódico o cuasiperiódico de un "
        "grado de libertad —masa, modo colectivo, enlace químico, celda de metamaterial— alrededor de un equilibrio. "
        "Ese movimiento transporta energía, información y, en el régimen cuántico, cuantos de excitación (fonones, "
        "vibriones). Analizarlo exige tres capas a la vez: (i) el modelo dinámico, (ii) la medida (tiempo, frecuencia, "
        "espacio), (iii) la interpretación en un material o un dispositivo real."
    ))

    # 2
    story.append(P("2. Núcleo clásico: el oscilador como átomo de toda la teoría", "H1"))
    story.append(P(
        "El sistema irreductible es el oscilador armónico amortiguado y forzado. Con masa <i>m</i>, constante "
        "elástica <i>k</i>, amortiguamiento viscoso <i>c</i> y fuerza F(t) = F<sub>0</sub> cos(ωt):"
    ))
    story.append(P("m ẍ + c ẋ + k x = F<sub>0</sub> cos(ωt)", "Eq"))
    story.append(P(
        "Se definen ω<sub>0</sub> = √(k/m) y ζ = c / (2√(km)). El régimen ζ &lt; 1 (subamortiguado) es el de casi "
        "todos los resonadores útiles: la energía oscila y decae como e<sup>−ζω<sub>0</sub>t</sup>. En resonancia "
        "(ω ≈ ω<sub>0</sub>√(1−2ζ²) para la amplitud de desplazamiento) la fase tiende a π/2: la fuerza trabaja "
        "en cuadratura con la posición y en fase con la velocidad, que es donde se inyecta potencia media."
    ))
    story.append(fig("01_oscilador_armonico.png",
                     "Figura 1. Simulación ejecutada: respuesta libre para cuatro ζ, curva de resonancia, "
                     "transitorio forzado y retraso de fase."))
    story.append(P(
        "El factor de calidad Q ≈ 1/(2ζ) (para ζ pequeño) condensa tres ideas: cuántos ciclos tarda en perderse "
        "la energía, cuán estrecha es la respuesta espectral (Δf ≈ f<sub>0</sub>/Q) y cuánto se amplifica una "
        "fuerza cercana a resonancia. En metamateriales y cavidades optomecánicas se buscan Q altos; en aislamiento "
        "vibratorio y amortiguadores, Q bajos. No hay un Q «mejor»: hay un Q adecuado a la función."
    ))
    story.append(fig("08_factor_calidad.png",
                     "Figura 2. Familias de resonancia para Q = 5, 15, 50 y 200. El área bajo la curva de potencia "
                     "se redistribuye: más alto y más estrecho al crecer Q."))

    story.append(P("3. Del tiempo a la frecuencia: la huella vibratoria", "H1"))
    story.append(P(
        "Casi ningún sistema real es un tono puro. Un motor, un thruster de yodo, una membrana de grafeno o un "
        "parche articular produce una mezcla: tonos, armónicos, chirps, bursts y ruido. La herramienta correcta "
        "no es «mirar la señal», es proyectarla. La FFT da el contenido global; el espectrograma (STFT) da la "
        "evolución. Sin ambos, se confunde un tono estable con un evento transitorio de la misma frecuencia."
    ))
    story.append(fig("02_fft_espectrograma.png",
                     "Figura 3. Señal sintética (chirp + 180 Hz + burst a 320 Hz + ruido): serie, FFT y espectrograma. "
                     "La FFT ve las tres componentes; solo el espectrograma revela cuándo aparece cada una."))
    story.append(P(
        "Protocolo mínimo de análisis espectral (el que un chat no ejecuta sobre tus datos): "
        "(1) muestrear ≥ 2,5× la frecuencia de interés (Nyquist no es un techo cómodo); "
        "(2) quitar continua y tendencia; "
        "(3) ventana de Hann o Flattop según se priorice resolución o amplitud; "
        "(4) solapamiento 50–75 % en STFT; "
        "(5) reportar unidades (g²/Hz, Pa²/Hz, m²/s⁴/Hz) y no «amplitud arbitraria»; "
        "(6) no llamar «modo» a un pico de FFT sin comprobar que existe un patrón espacial coherente."
    ))

    story.append(P("4. Modos normales: el esqueleto del continuo", "H1"))
    story.append(P(
        "Una cuerda fija, una membrana, una placa de metamaterial o la estructura de un CubeSat no vibran «en "
        "cualquier forma». Vibran en una base de modos que diagonaliza el operador espacial (el laplaciano con "
        "las condiciones de contorno). En la cuerda de Dirichlet:"
    ))
    story.append(P("ψ<sub>n</sub>(x) = sin(nπx/L) ,    f<sub>n</sub> = n f<sub>1</sub> ,    f<sub>1</sub> = (1/2L)√(T/μ)", "Eq"))
    story.append(fig("03_modos_cuerda.png",
                     "Figura 4. Primeros cuatro modos de cuerda. Los nodos son inamovibles en un modo puro; "
                     "en una superposición viajan (véase la animación adjunta)."))
    story.append(P(
        "La animación <b>10_modos_cuerda_animacion.mp4</b> (6 s, 40 fps) muestra los cinco primeros modos y la "
        "superposición que reconstruye un pulso que se refleja. Ese es el contenido real de la serie de Fourier "
        "espacial: no es un adorno pedagógico, es el mecanismo por el que un impacto se convierte en un acorde "
        "de frecuencias."
    ))
    story.append(fig("06_modos_membrana.png",
                     "Figura 5. Modos (m,n) de membrana rectangular. Las líneas nodales son el mapa que un "
                     "ensayo de vibrometría láser debería recuperar."))
    story.append(P(
        "En 2D y 3D las degeneraciones, las simetrías y los contornos libres cambian el espectro. Un metamaterial "
        "no «inventa» modos de la nada: redistribuye densidades de estados, abre gaps, aplana bandas (velocidad "
        "de grupo nula) y, si la simetría lo permite, crea canales de borde topológicamente protegidos."
    ))
    story.append(fig("09_osciladores_acoplados.png",
                     "Figura 6. Dos masas acopladas: el batido visible en cada masa es la interferencia del modo "
                     "simétrico y el antisimétrico. Es el germen de toda banda fonónica."))

    story.append(PageBreak())
    story.append(P("5. Fonones y cristales fonónicos: vibración como cuasipartícula", "H1"))
    story.append(P(
        "En un sólido, los modos colectivos de la red se cuantizan. El fonón es el cuanto de esa vibración. "
        "Su tarjeta de identidad es la relación de dispersión ω(k). En la cadena monoatómica de Born–von Karman:"
    ))
    story.append(P("ω(k) = 2 √(K/m) |sin(ka/2)|", "Eq"))
    story.append(P(
        "En la red diatómica aparecen dos ramas: acústica (los dos átomos se mueven en fase a k→0, ω→0, "
        "velocidad del sonido finita) y óptica (contrafase, gap, frecuencia finita en Γ). El gap no es un fallo "
        "del modelo: es el primer bandgap fonónico de la naturaleza. Un cristal fonónico o un metamaterial "
        "elástico no hace otra cosa que diseñar, a escala de celda unidad, ese mismo mecanismo —contraste de "
        "impedancia, resonadores locales, simetría— para colocar gaps, Dirac, Weyl, rotones o bandas planas "
        "donde el ingeniero los necesita."
    ))
    story.append(fig("04_dispersion_fononica.png",
                     "Figura 7. Dispersión 1D simulada. Izquierda: rama acústica única. Derecha: acústica + óptica "
                     "y el gap que las separa."))
    story.append(fig("05_cristal_fononico_T.png",
                     "Figura 8. Transmisión de un cristal fonónico 1D de 12 celdas A–B (matriz de transferencia). "
                     "Las bandas de rechazo son el equivalente medible del gap de dispersión."))
    story.append(P("Estado del arte reciente (lo que hay que contrastar, no copiar)", "H2"))
    story.append(bullet_list([
        "Diagnóstico dinámico de metamateriales por firmas vibratorias inducidas por láser (Nature 623, 2023): "
        "se extraen rigidez direccional, amortiguamiento y defectos ocultos a partir de la propagación en MHz.",
        "Medios fonónicos artificiales guiados por simetría (Nat. Rev. Mater., 2025/26): romper simetrías espaciales "
        "y temporales produce no reciprocidad, ganancia/pérdida y transporte exótico.",
        "Observación directa de bandas fonónicas <i>all-flat</i> (Phys. Rev. Lett. 133, 2024): velocidad de grupo "
        "nula en todo el Brillouin → localización extrema de energía.",
        "Relaciones de dispersión tipo rotón en metamateriales 3D a temperatura ambiente (Science Advances, 2021), "
        "antes exclusivas de helio superfluido.",
        "Catálogo de fonones topológicos en ~5000 materiales (Science / DIPC): la topología no es un adorno, "
        "aparece en la red real.",
        "Metasuperficies acoustoplasmónicas (ACS Nano, 2026): puente luz–sonido para moldear frentes de onda "
        "acústicos con grados de libertad electromagnéticos.",
    ]))
    story.append(P(
        "Implicación directa para trabajo en metamateriales (YIG, grafeno bicapa rotado, puntos cuánticos, "
        "lentes acústicas): la vibración no es un efecto secundario del dispositivo. Es el canal. Quien no "
        "mida dispersión, Q, gap y mapa modal no tiene un metamaterial; tiene una geometría decorativa."
    ))

    story.append(P("6. Régimen cuántico: el oscilador que no puede detenerse", "H1"))
    story.append(P(
        "Al cuantizar el oscilador, la energía ya no puede ser cero. Los niveles son E<sub>n</sub> = (n + ½) ħω. "
        "El estado n = 0 sigue teniendo una anchura finita: energía de punto cero. Eso no es filosofía; es el "
        "suelo de ruido de un resonador mecánico a milikelvin y el origen de la rama óptica en infrarrojo "
        "cuando un modo molecular está poblado térmicamente."
    ))
    story.append(fig("07_oscilador_cuantico.png",
                     "Figura 9. Niveles y densidades |ψ<sub>n</sub>|² del QHO (simulación). Cada lóbulo extra es "
                     "un nodo de la función de onda."))
    story.append(fig("12_qho_artistico.jpg",
                     "Figura 10. Lectura visual de la misma idea: nubes de probabilidad sobre el pozo parabólico."))
    story.append(P(
        "En espectroscopía vibracional (IR, Raman) cada pico es, en primera aproximación, un salto Δn = ±1 "
        "de un modo normal molecular. Anarmonicidad, acoplamiento de Fermi, modos colectivos en líquidos "
        "complejos (p. ej. redes de ácido hialurónico) y acoplamiento a un plasmon o a un fonón de un "
        "sustrato metamaterial desplazan, ensanchan o intensifican esos picos. Analizar «vibraciones "
        "científicas» en nanomedicina es, en la práctica, asignar modos, cuantificar anarmonicidad y "
        "decidir si un parche o un lubricante cuántico-biomimético está acoplado al espectro que se declara."
    ))

    story.append(P("7. Cómo se miden de verdad (caja de herramientas)", "H1"))
    data = [
        [P("<b>Técnica</b>"), P("<b>Qué ve</b>"), P("<b>Rango típico</b>"), P("<b>Notas</b>")],
        [P("Acelerómetros / IEPE"), P("a(t) en puntos"), P("Hz–kHz"), P("Barato; masa añadida; no vale en micro")],
        [P("LDV / vibrometría láser"), P("v(t) o u(t) sin contacto"), P("Hz–MHz"), P("Mapas modales; estándar en metas")],
        [P("Raman"), P("Fonones ópticos"), P("THz / cm<sup>−1</sup>"), P("Química + red; no acústicos")],
        [P("Brillouin (BLS)"), P("Fonones acústicos"), P("GHz"), P("Módulos elásticos, velocidades")],
        [P("Bombeo-sonda / ASOPS"), P("Dinámica coherente"), P("GHz–THz"), P("Nanofonónica ultrarrápida")],
        [P("IDT / RF sobre piezo"), P("Excita y lee SAW"), P("MHz–GHz"), P("Filtros, acustofluídica")],
        [P("Cavidad optomecánica"), P("Fonón + fotón"), P("MHz–GHz"), P("Q altísimos, régimen cuántico")],
        [P("RUS / ultrasonidos"), P("Espectro de resonancias"), P("kHz–MHz"), P("Constantes elásticas de un sólido")],
    ]
    tbl = Table(data, colWidths=[38 * mm, 38 * mm, 32 * mm, 60 * mm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), BG),
        ("BACKGROUND", (0, 3), (-1, 3), BG),
        ("BACKGROUND", (0, 5), (-1, 5), BG),
        ("BACKGROUND", (0, 7), (-1, 7), BG),
        ("BOX", (0, 0), (-1, -1), 0.4, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(tbl)
    story.append(P("Tabla 1. Técnicas de excitación y lectura. Elegir dos complementarias vale más que una sola «perfecta».", "Caption"))

    story.append(P("8. Aplicación a líneas de trabajo concretas", "H1"))
    story.append(P("8.1 Metamateriales, lentes acústicas y YIG", "H2"))
    story.append(P(
        "Una lente acústica no se valida con una foto de la geometría. Se valida con: (i) mapa de presión o "
        "desplazamiento en el plano focal, (ii) función de transferencia frente a frecuencia, (iii) robustez "
        "a desorden de fabricación. El YIG añade un grado de libertad magnetoelástico: el fonón se hibrida "
        "con el magnón. Eso desplaza gaps y permite no reciprocidad con un campo externo. El análisis correcto "
        "es un diagrama de bandas magnetoelástico, no una analogía verbal con «resonancia»."
    ))
    story.append(P("8.2 Propulsión eléctrica (MEI-RIT / Lázaro Drive)", "H2"))
    story.append(P(
        "Un thruster de RF con yodo tiene, como mínimo, tres familias vibratorias que no se deben mezclar: "
        "modos estructurales del chasis y de la rejilla, modos acústicos/iónicos del plasma y ruido de "
        "conmutación de la RF. Un pico a la frecuencia de excitación RF no es «el modo del satélite». "
        "Protocolo: acelerómetros en la estructura + LDV en la rejilla + sonda de plasma, todo sincronizado "
        "con el generador. Criterio de aceptación: ningún modo estructural dentro de ±10 % de una frecuencia "
        "de excitación persistente, y margen de fatiga documentado."
    ))
    story.append(P("8.3 Nanomedicina y modos moleculares", "H2"))
    story.append(P(
        "En un lubricante biomimético o un parche de NO / ácido hialurónico, las «vibraciones científicas» "
        "relevantes son modos O–H, C–H, esqueleto del polímero y modos colectivos de red de hidrógeno. "
        "IR+Raman asignados, no un espectro sin picos etiquetados, es la evidencia de que la molécula que "
        "se dibuja es la que está en el vial. El acoplamiento a un sustrato metamaterial (si se declara "
        "«cuántico») debe verse como desplazamiento o ensanchamiento reproducible, no como una palabra."
    ))
    story.append(P("8.4 Fusión y redes tipo BN–He3", "H2"))
    story.append(P(
        "La red que hospeda He-3 o boro-nitruro vibra. Esos fonones son el baño térmico del que un diseño "
        "de reactor no puede prescindir: conducción, scattering de iones, posibles acoplamientos a modos "
        "colectivos del plasma en la primera pared. Analizarlos es calcular dispersión (DFT/DFPT) y "
        "contrastarla con neutrones o Brillouin, no afirmar un «amortiguamiento cuántico» sin número."
    ))

    story.append(P("9. Protocolo reproducible (mínimo viable)", "H1"))
    story.append(bullet_list([
        "Definir el grado de libertad: ¿punto, modo, banda, molécula, estructura?",
        "Escribir la ecuación o el hamiltoniano efectivo <i>antes</i> de medir.",
        "Elegir dos técnicas ortogonales (p. ej. LDV + FFT de acelerómetro, o Raman + DFT).",
        "Muestrear con margen de Nyquist y documentar ventana, solape y calibración.",
        "Identificar picos con un modo espacial o una asignación molecular, no solo con un Hz.",
        "Reportar Q, ζ o FWHM, no solo «resuena».",
        "Hacer un control: misma medida en un sólido homogéneo o en un blanco molecular.",
        "Declarar incertidumbre y lo que el modelo no cubre (no linealidad, temperatura, vacío).",
        "Archivar datos crudos + script. Si no se puede reejecutar, no es un análisis.",
    ]))

    story.append(P("10. Límites de este entregable y del fenómeno", "H1"))
    story.append(P(
        "Las figuras 1–9 son modelos canónicos ejecutados (oscilador, FFT, modos, Born–von Karman, matriz "
        "de transferencia 1D, QHO). No sustituyen un FEM 3D de una celda YIG real ni un espectro Raman "
        "experimental de un lote GMP. La animación es lineal y no disipativa. El cristal fonónico 1D usa "
        "impedancias contrastadas arbitrarias: sirve para enseñar el gap, no para cotizar una pieza. "
        "La literatura citada es el mapa, no la autorización para clonar un paper."
    ))
    story.append(P(
        "Límites físicos que ningún texto debería olvidar: no linealidad (saltos de Duffing, solitones, "
        "mezcla de modos), caos en sistemas de pocos grados de libertad forzados, localización de Anderson "
        "en desorden, rotura de simetría temporal si hay ganancia o flujo, y el hecho de que un fonón "
        "óptico de THz no se «ve» con un acelerómetro de 10 kHz."
    ))

    story.append(P("11. Cómo usar el paquete", "H1"))
    story.append(P(
        "Junto a este PDF están: <b>code/simular_vibraciones.py</b> (todas las figuras), "
        "<b>code/animar_modos.py</b> (MP4 de 6 s) y las imágenes en <b>figs/</b>. "
        "Dependencias: Python 3, numpy, scipy, matplotlib, ffmpeg. Reejecutar es el test de que el análisis "
        "no depende de una sesión de chat."
    ))
    story.append(Preformatted(
        "python3 code/simular_vibraciones.py\n"
        "python3 code/animar_modos.py",
        S["CodeBlock"],
    ))

    story.append(P("Cierre", "H1"))
    story.append(P(
        "Analizar vibraciones científicas es pasar de la palabra «vibra» a un número, un modo, una banda "
        "y una incertidumbre. Este documento hace ese paso en los modelos que sí se pueden cerrar hoy, "
        "con código y figuras, y deja escrito el protocolo para los sistemas —metamaterial, thruster, "
        "parche, red de He-3— donde el siguiente paso ya no es un chat, sino un experimento."
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(P(
        "Si un tercero continúa este trabajo, debe citar a Lázaro López Paz y a Grok. "
        "El contenido está pensado para uso constructivo, verificable y no destructivo.",
        "Note",
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print("PDF written", OUT, "size", OUT.stat().st_size)


if __name__ == "__main__":
    make()
