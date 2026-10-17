proyecto\_espana\_app:  
  \- app.py                  \# Código principal unificado de la aplicación  
  \- requirements.txt        \# Dependencias de Python para el servidor  
  \- data:  
      \- table\_20260925.csv  \# Archivo de metadatos de los entregables

streamlit\>=1.30.0  
pandas\>=2.0.0  
plotly\>=5.18.0  
folium\>=0.15.0  
streamlit-folium\>=0.18.0

\# \-\*- coding: utf-8 \-\*-  
import streamlit as st  
import pandas as pd  
import plotly.express as px  
import folium  
from streamlit\_folium import st\_folium  
import os

\# \---------- CONFIGURACIÓN \----------  
st.set\_page\_config(  
    page\_title="Estrategia Nacional Descarbonización 2026",  
    page\_icon="🇪🇸",  
    layout="wide",  
    initial\_sidebar\_state="expanded"  
)

\# \---------- CARGA DE DATOS \----------  
@st.cache\_data  
def cargar\_datos\_proyectos():  
    data \= \[  
        {"Proyecto": "Moeve Biocombustibles 2G", "Ubicación": "Palos de la Frontera (Huelva)", "Tipo": "Biocombustible", "Producción (t/año)": 500000, "Inversión (M€)": 1200, "Estado": "Construcción", "Lat": 37.229, "Lon": \-6.895, "Descripción": "Mayor complejo de biocombustibles 2G del sur de Europa. SAF y diésel renovable."},  
        {"Proyecto": "Dreexo Energy Hub", "Ubicación": "Zona Franca de Cádiz", "Tipo": "Biocombustible", "Producción (t/año)": 100000, "Inversión (M€)": 46, "Estado": "Permisos", "Lat": 36.500, "Lon": \-6.250, "Descripción": "Primera planta de pretratamiento de doble cómputo para UCO y grasas animales."},  
        {"Proyecto": "Bioetanol Galicia", "Ubicación": "Curtis (A Coruña)", "Tipo": "Biocombustible", "Producción (t/año)": 150000, "Inversión (M€)": 60, "Estado": "Operativo", "Lat": 43.150, "Lon": \-8.150, "Descripción": "Bioetanol a partir de maíz y biomasa \+ captura de 150.000 t/año de CO₂."},  
        {"Proyecto": "Valle Andaluz H₂ Verde", "Ubicación": "Andalucía (Huelva)", "Tipo": "H₂ verde", "Producción (t/año)": 300000, "Inversión (M€)": 3000, "Estado": "Construcción", "Lat": 37.177, "Lon": \-3.598, "Descripción": "2.000 MW de electrólisis. Proyecto de país. 300.000 t/año de H₂ verde."},  
        {"Proyecto": "COMPOSTILLA GREEN", "Ubicación": "Cubillos del Sil (León)", "Tipo": "H₂ verde", "Producción (t/año)": 36208, "Inversión (M€)": 261, "Estado": "Construcción", "Lat": 42.633, "Lon": \-6.633, "Descripción": "220 MWe de electrólisis. 36.208 t/año de H₂ renovable."},  
        {"Proyecto": "QUIXOTGEN", "Ubicación": "Villarrobledo (Albacete)", "Tipo": "H₂ verde", "Producción (t/año)": 0, "Inversión (M€)": 50.2, "Estado": "Aprobado", "Lat": 39.267, "Lon": \-2.600, "Descripción": "30 MW de electrólisis para H₂ verde."},  
        {"Proyecto": "H2Pro / Sun Systems", "Ubicación": "Tarragona", "Tipo": "H₂ verde", "Producción (t/año)": 0, "Inversión (M€)": 300, "Estado": "Planificado", "Lat": 41.118, "Lon": 1.244, "Descripción": "150 MW de electrólisis previstos para 2032."},  
        {"Proyecto": "H2Duero Garray", "Ubicación": "Garray (Soria)", "Tipo": "H₂ verde", "Producción (t/año)": 300, "Inversión (M€)": 0, "Estado": "Operativo", "Lat": 41.817, "Lon": \-2.450, "Descripción": "Electrolizador PEM de 3 MW."},  
        {"Proyecto": "Armonia Green Castellón", "Ubicación": "Castellón de la Plana", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 861236, "Inversión (M€)": 1425, "Estado": "Tramitación", "Lat": 39.986, "Lon": \-0.051, "Descripción": "861.236 t/año de NH₃ verde. 1.425 M€. Fases 2027, 2029, 2031."},  
        {"Proyecto": "Armonia Green Burgos", "Ubicación": "Melgar de Fernamental (Burgos)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 0, "Inversión (M€)": 0, "Estado": "Tramitación", "Lat": 42.400, "Lon": \-4.250, "Descripción": "500 MW eléctricos renovables para amoníaco verde."},  
        {"Proyecto": "Green Ammonia Asturias", "Ubicación": "Avilés (Asturias)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 180000, "Inversión (M€)": 0, "Estado": "Financial Close", "Lat": 43.556, "Lon": \-5.925, "Descripción": "180.000 t/año de amoníaco verde."},  
        {"Proyecto": "Moeve Amoníaco San Roque", "Ubicación": "San Roque (Cádiz)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 600000, "Inversión (M€)": 0, "Estado": "Aprobado 2030", "Lat": 36.210, "Lon": \-5.385, "Descripción": "600.000 t/año de amoníaco verde para transporte marítimo."},  
        {"Proyecto": "Petronor e-Fuels", "Ubicación": "Puerto de Bilbao (Bizkaia)", "Tipo": "e-Fuels", "Producción (t/año)": 2000, "Inversión (M€)": 146, "Estado": "Construcción", "Lat": 43.263, "Lon": \-2.935, "Descripción": "2.000 t/año de e-diésel, e-SAF y e-nafta. Operativo 2027."},  
        {"Proyecto": "La Robla Green", "Ubicación": "La Robla (León)", "Tipo": "e-Metanol", "Producción (t/año)": 140000, "Inversión (M€)": 750, "Estado": "Aprobado", "Lat": 42.800, "Lon": \-5.633, "Descripción": "140.000 t/año de e-metanol verde. 750 M€."},  
        {"Proyecto": "Metabarri", "Ubicación": "Artigas (Bizkaia)", "Tipo": "Biogás", "Producción (t/año)": 50000, "Inversión (M€)": 25, "Estado": "Operativo 2026", "Lat": 43.300, "Lon": \-2.900, "Descripción": "Transforma residuos orgánicos en biometano. 12.700 hogares."},  
        {"Proyecto": "Cemex SOMZERO", "Ubicación": "Alcanar (Tarragona)", "Tipo": "Captura CO₂", "Producción (t/año)": 500000, "Inversión (M€)": 450, "Estado": "Desarrollo", "Lat": 40.542, "Lon": 0.478, "Descripción": "Captura de \>500.000 t/año de CO₂. Hub de CO₂ en Cataluña."}  
    \]  
    return pd.DataFrame(data)

@st.cache\_data  
def cargar\_metadatos\_archivos():  
    \# Intenta cargar el archivo de metadatos integrado  
    try:  
        return pd.read\_csv("data/table\_20260925.csv")  
    except FileNotFoundError:  
        return pd.DataFrame({"Aviso": \["Archivo table\_20260925.csv no encontrado en la ruta 'data/'."\]})

df \= cargar\_datos\_proyectos()  
df\_archivos \= cargar\_metadatos\_archivos()

colores \= {  
    "Biocombustible": "\#2E8B57", "H₂ verde": "\#1F77B4", "Amoníaco NH₃": "\#8E44AD",  
    "e-Fuels": "\#E67E22", "e-Metanol": "\#C0392B", "Biogás": "\#17A2B8", "Captura CO₂": "\#7F8C8D",  
}

\# \---------- SIDEBAR NAVEGACIÓN \----------  
st.sidebar.title("🇪🇸 Panel de Control")  
st.sidebar.markdown("---")  
seccion \= st.sidebar.radio("Navegación:", \[  
    "📊 Dashboard y Análisis",   
    "🗺️ Mapa Geográfico",   
    "📑 Documentación Técnica (LaTeX)",   
    "✉️ Carta MITECO"  
\])

\# \---------- SECCIÓN 1: DASHBOARD \----------  
if seccion \== "📊 Dashboard y Análisis":  
    st.title("Estrategia Nacional para la Descarbonización")  
    st.markdown("Visualización de proyectos industriales para la transición energética en España (2026).")  
      
    \# Filtros  
    col\_f1, col\_f2 \= st.columns(2)  
    tipo\_sel \= col\_f1.selectbox("Filtrar por Tipo de Proyecto", \["Todos"\] \+ sorted(df\["Tipo"\].unique().tolist()))  
    estado\_sel \= col\_f2.selectbox("Filtrar por Estado", \["Todos"\] \+ sorted(df\["Estado"\].unique().tolist()))  
      
    df\_filtrado \= df.copy()  
    if tipo\_sel \!= "Todos": df\_filtrado \= df\_filtrado\[df\_filtrado\["Tipo"\] \== tipo\_sel\]  
    if estado\_sel \!= "Todos": df\_filtrado \= df\_filtrado\[df\_filtrado\["Estado"\] \== estado\_sel\]

    \# KPIs  
    st.markdown("\#\#\# Métricas Clave")  
    k1, k2, k3, k4 \= st.columns(4)  
    k1.metric("Proyectos Listados", len(df\_filtrado))  
    k2.metric("Inversión Movilizada", f"{df\_filtrado\['Inversión (M€)'\].sum():,.0f} M€")  
    k3.metric("Capacidad de Producción", f"{df\_filtrado\['Producción (t/año)'\].sum():,} t/año")  
    k4.metric("Tecnologías", df\_filtrado\["Tipo"\].nunique())

    \# Gráficos  
    st.markdown("---")  
    col\_g1, col\_g2 \= st.columns(2)  
    with col\_g1:  
        st.subheader("Inversión por Proyecto (M€)")  
        df\_inv \= df\_filtrado\[df\_filtrado\["Inversión (M€)"\] \> 0\].sort\_values("Inversión (M€)", ascending=True)  
        if not df\_inv.empty:  
            fig1 \= px.bar(df\_inv, x="Inversión (M€)", y="Proyecto", orientation="h", color="Tipo", color\_discrete\_map=colores, text="Inversión (M€)")  
            fig1.update\_traces(texttemplate='%{text:,.0f} M€', textposition='outside')  
            fig1.update\_layout(height=450, showlegend=False, margin=dict(l=0, r=0, t=30, b=0))  
            st.plotly\_chart(fig1, use\_container\_width=True)  
      
    with col\_g2:  
        st.subheader("Producción Agregada por Tipo")  
        df\_prod \= df\_filtrado\[df\_filtrado\["Producción (t/año)"\] \> 0\].groupby("Tipo")\["Producción (t/año)"\].sum().reset\_index()  
        if not df\_prod.empty:  
            fig2 \= px.pie(df\_prod, values="Producción (t/año)", names="Tipo", color="Tipo", color\_discrete\_map=colores, hole=0.4)  
            fig2.update\_traces(textinfo='percent+label', textposition='inside')  
            fig2.update\_layout(height=450, showlegend=True, margin=dict(l=0, r=0, t=30, b=0))  
            st.plotly\_chart(fig2, use\_container\_width=True)

\# \---------- SECCIÓN 2: MAPA INTERACTIVO \----------  
elif seccion \== "🗺️ Mapa Geográfico":  
    st.title("Mapa de Proyectos Energéticos Renovables")  
    st.markdown("Distribución territorial de las infraestructuras de descarbonización.")  
      
    \# Renderización del mapa de Folium  
    m \= folium.Map(location=\[40.0, \-3.5\], zoom\_start=6, tiles="CartoDB positron")  
      
    for \_, row in df.dropna(subset=\["Lat", "Lon"\]).iterrows():  
        popup\_html \= f'''  
        \<div style="font-family:Arial; width:220px;"\>  
            \<h4 style="color:\#0B3D91; margin:0 0 5px 0;"\>{row\["Proyecto"\]}\</h4\>  
            \<b\>Tipo:\</b\> {row\["Tipo"\]}\<br\>  
            \<b\>Producción:\</b\> {row\["Producción (t/año)"\]:,} t/año\<br\>  
            \<b\>Inversión:\</b\> {row\["Inversión (M€)"\]} M€\<br\>  
            \<b\>Estado:\</b\> {row\["Estado"\]}\<br\>  
        \</div\>  
        '''  
        folium.Marker(  
            location=\[row\["Lat"\], row\["Lon"\]\],  
            popup=folium.Popup(popup\_html, max\_width=300),  
            tooltip=f"{row\['Proyecto'\]} — {row\['Tipo'\]}",  
            icon=folium.Icon(color="blue", icon="bolt", prefix="fa")  
        ).add\_to(m)

    st\_folium(m, width=1200, height=650, returned\_objects=\[\])

\# \---------- SECCIÓN 3: DOCUMENTACIÓN TÉCNICA \----------  
elif seccion \== "📑 Documentación Técnica (LaTeX)":  
    st.title("Documentación y Metadatos del Proyecto")  
      
    st.subheader("Archivos del Proyecto (Metadatos)")  
    st.markdown("Tabla generada a partir de \`table\_20260925.csv\`:")  
    st.dataframe(df\_archivos, use\_container\_width=True)  
      
    st.markdown("---")  
    st.subheader("Dosier Técnico (Sintaxis LaTeX)")  
    st.markdown("Código fuente del documento \`03\_propuesta.tex\` estructurado para renderizado de ecuaciones matemáticas y tablas formales en PDF.")  
      
    latex\_code \= r"""\\documentclass\[11pt,a4paper\]{article}  
% \---------- PAQUETES \----------  
\\usepackage\[utf8\]{inputenc}  
\\usepackage\[T1\]{fontenc}  
\\usepackage\[spanish,es-tabla\]{babel}  
\\usepackage\[margin=2.2cm\]{geometry}  
\\usepackage{xcolor}  
\\usepackage{tabularx}  
\\usepackage{booktabs}  
\\usepackage{tcolorbox}  
\\usepackage{hyperref}

\\definecolor{azul}{HTML}{0B3D91}  
\\definecolor{gris}{HTML}{F2F2F2}

\\title{\\color{azul}\\Huge\\textbf{Estrategia Nacional para la Descarbonización del Transporte}}  
\\author{\\textbf{Documento Técnico}}  
\\date{Septiembre 2026}

\\begin{document}  
\\maketitle

\\begin{tcolorbox}\[colback=gris, colframe=azul, title=\\textbf{Resumen Ejecutivo}\]  
Esta propuesta articula una estrategia nacional para reducir la dependencia del petróleo en un \\textbf{30--40\\% para 2030} combinando combustibles renovables y computación cuántica.  
\\end{tcolorbox}

\\section{Hoja de Ruta 2026--2040}  
\\begin{table}\[h\!\]  
\\centering  
\\begin{tabularx}{\\textwidth}{@{}lXXr@{}}  
\\toprule  
\\textbf{Fase} & \\textbf{Periodo} & \\textbf{Acciones clave} & \\textbf{Inversión} \\\\  
\\midrule  
1\. Despliegue & 2026--2027 & Moeve Huelva, Petronor, Dual-Fuel & 2.500 M€ \\\\  
2\. Escalado & 2027--2030 & Castellón, Valle Andaluz H\\textsubscript{2} & 6.000 M€ \\\\  
\\bottomrule  
\\end{tabularx}  
\\end{table}  
\\end{document}  
"""  
    st.code(latex\_code, language="latex")  
    st.download\_button(  
        label="📥 Descargar 03\_propuesta.tex",  
        data=latex\_code,  
        file\_name="03\_propuesta.tex",  
        mime="text/plain"  
    )

\# \---------- SECCIÓN 4: CARTA MITECO \----------  
elif seccion \== "✉️ Carta MITECO":  
    st.title("Carta de Presentación Institucional")  
    st.markdown("Propuesta de Estrategia Nacional dirigida al MITECO.")  
      
    carta\_texto \= """\*\*ENTREGABLE 1: Carta de Presentación al Ministerio\*\*  
\*\*Destinatario:\*\* Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO)  
\*\*Asunto:\*\* Propuesta de Estrategia Nacional para la Descarbonización del Transporte mediante Combustibles Renovables y Computación Cuántica

\---  
Excelentísima Señora Ministra:

Me dirijo a usted en calidad de ciudadano/a comprometido/a con la transición energética de España, para presentar una propuesta técnica que considero de interés estratégico nacional. El documento articula un plan integral para reducir la dependencia del petróleo importado mediante un ecosistema de combustibles renovables, hidrógeno y amoníaco verdes, biogás y computación cuántica aplicada a la optimización industrial.

\*\*Lo que solicitamos:\*\*  
1\. Declarar los combustibles renovables como infraestructura crítica de interés general.  
2\. Crear un fondo de 500 millones de euros para la conversión de flotas diésel a tecnología Dual-Fuel GNC.  
3\. Impulsar un programa nacional de computación cuántica aplicada a la energía dotado con 100 millones de euros.  
4\. Establecer un marco regulatorio estable que garantice la viabilidad económica a largo plazo.  
5\. Lanzar un plan de formación profesional para cubrir la demanda de especialistas industriales.

España tiene hoy la oportunidad histórica de liderar la transición energética mundial. Los proyectos ya están en marcha, la financiación ya está asignada y la tecnología ya está probada. Lo que falta es voluntad política para coordinar y acelerar."""  
      
    st.markdown(f"\<div style='background-color: \#f9f9f9; padding: 25px; border-radius: 8px; border-left: 5px solid \#0B3D91;'\>{carta\_texto}\</div\>", unsafe\_allow\_html=True)  
    st.download\_button("📥 Descargar Carta (Markdown)", data=carta\_texto, file\_name="carta\_miteco.md", mime="text/markdown")

Crea un repositorio en GitHub con la estructura YAML indicada en el paso 1\.  
Sube el código unificado dentro de app.py, el requirements.txt, y asegúrate de colocar table\_20260925.csv en la carpeta /data.  
Conecta el repositorio a Streamlit Community Cloud y despliega la rama principal. La plataforma resolverá las librerías automáticamente y publicará la herramienta con navegación integrada.
