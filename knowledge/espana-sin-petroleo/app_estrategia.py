# -*- coding: utf-8 -*-  
import streamlit as st  
import pandas as pd  
import plotly.express as px  
import folium  
from streamlit_folium import st_folium

st.set_page_config(page_title="Estrategia Nacional Descarbonización 2026", page_icon="🇪🇸", layout="wide")

@st.cache_data  
def cargar_datos_proyectos():  
    return pd.DataFrame([  
        {"Proyecto": "Moeve Biocombustibles 2G", "Ubicación": "Palos de la Frontera (Huelva)", "Tipo": "Biocombustible", "Producción (t/año)": 500000, "Inversión (M€)": 1200, "Estado": "Construcción", "Lat": 37.229, "Lon": -6.895, "Descripción": "Mayor complejo de biocombustibles 2G del sur de Europa. SAF y diésel renovable."},  
        {"Proyecto": "Dreexo Energy Hub", "Ubicación": "Zona Franca de Cádiz", "Tipo": "Biocombustible", "Producción (t/año)": 100000, "Inversión (M€)": 46, "Estado": "Permisos", "Lat": 36.500, "Lon": -6.250, "Descripción": "Primera planta de pretratamiento de doble cómputo para UCO y grasas animales."},  
        {"Proyecto": "Bioetanol Galicia", "Ubicación": "Curtis (A Coruña)", "Tipo": "Biocombustible", "Producción (t/año)": 150000, "Inversión (M€)": 60, "Estado": "Operativo", "Lat": 43.150, "Lon": -8.150, "Descripción": "Bioetanol a partir de maíz y biomasa + captura de 150.000 t/año de CO₂."},  
        {"Proyecto": "Valle Andaluz H₂ Verde", "Ubicación": "Andalucía (Huelva)", "Tipo": "H₂ verde", "Producción (t/año)": 300000, "Inversión (M€)": 3000, "Estado": "Construcción", "Lat": 37.177, "Lon": -3.598, "Descripción": "2.000 MW de electrólisis. Proyecto de país. 300.000 t/año de H₂ verde."},  
        {"Proyecto": "COMPOSTILLA GREEN", "Ubicación": "Cubillos del Sil (León)", "Tipo": "H₂ verde", "Producción (t/año)": 36208, "Inversión (M€)": 261, "Estado": "Construcción", "Lat": 42.633, "Lon": -6.633, "Descripción": "220 MWe de electrólisis. 36.208 t/año de H₂ renovable."},  
        {"Proyecto": "QUIXOTGEN", "Ubicación": "Villarrobledo (Albacete)", "Tipo": "H₂ verde", "Producción (t/año)": 0, "Inversión (M€)": 50.2, "Estado": "Aprobado", "Lat": 39.267, "Lon": -2.600, "Descripción": "30 MW de electrólisis para H₂ verde."},  
        {"Proyecto": "H2Pro / Sun Systems", "Ubicación": "Tarragona", "Tipo": "H₂ verde", "Producción (t/año)": 0, "Inversión (M€)": 300, "Estado": "Planificado", "Lat": 41.118, "Lon": 1.244, "Descripción": "150 MW de electrólisis previstos para 2032."},  
        {"Proyecto": "H2Duero Garray", "Ubicación": "Garray (Soria)", "Tipo": "H₂ verde", "Producción (t/año)": 300, "Inversión (M€)": 0, "Estado": "Operativo", "Lat": 41.817, "Lon": -2.450, "Descripción": "Electrolizador PEM de 3 MW."},  
        {"Proyecto": "Armonia Green Castellón", "Ubicación": "Castellón de la Plana", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 861236, "Inversión (M€)": 1425, "Estado": "Tramitación", "Lat": 39.986, "Lon": -0.051, "Descripción": "861.236 t/año de NH₃ verde. 1.425 M€. Fases 2027, 2029, 2031."},  
        {"Proyecto": "Armonia Green Burgos", "Ubicación": "Melgar de Fernamental (Burgos)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 0, "Inversión (M€)": 0, "Estado": "Tramitación", "Lat": 42.400, "Lon": -4.250, "Descripción": "500 MW eléctricos renovables para amoníaco verde."},  
        {"Proyecto": "Green Ammonia Asturias", "Ubicación": "Avilés (Asturias)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 180000, "Inversión (M€)": 0, "Estado": "Financial Close", "Lat": 43.556, "Lon": -5.925, "Descripción": "180.000 t/año de amoníaco verde."},  
        {"Proyecto": "Moeve Amoníaco San Roque", "Ubicación": "San Roque (Cádiz)", "Tipo": "Amoníaco NH₃", "Producción (t/año)": 600000, "Inversión (M€)": 0, "Estado": "Aprobado 2030", "Lat": 36.210, "Lon": -5.385, "Descripción": "600.000 t/año de amoníaco verde para transporte marítimo."},  
        {"Proyecto": "Petronor e-Fuels", "Ubicación": "Puerto de Bilbao (Bizkaia)", "Tipo": "e-Fuels", "Producción (t/año)": 2000, "Inversión (M€)": 146, "Estado": "Construcción", "Lat": 43.263, "Lon": -2.935, "Descripción": "2.000 t/año de e-diésel, e-SAF y e-nafta. Operativo 2027."},  
        {"Proyecto": "La Robla Green", "Ubicación": "La Robla (León)", "Tipo": "e-Metanol", "Producción (t/año)": 140000, "Inversión (M€)": 750, "Estado": "Aprobado", "Lat": 42.800, "Lon": -5.633, "Descripción": "140.000 t/año de e-metanol verde. 750 M€."},  
        {"Proyecto": "Metabarri", "Ubicación": "Artigas (Bizkaia)", "Tipo": "Biogás", "Producción (t/año)": 50000, "Inversión (M€)": 25, "Estado": "Operativo 2026", "Lat": 43.300, "Lon": -2.900, "Descripción": "Transforma residuos orgánicos en biometano. 12.700 hogares."},  
        {"Proyecto": "Cemex SOMZERO", "Ubicación": "Alcanar (Tarragona)", "Tipo": "Captura CO₂", "Producción (t/año)": 500000, "Inversión (M€)": 450, "Estado": "Desarrollo", "Lat": 40.542, "Lon": 0.478, "Descripción": "Captura de >500.000 t/año de CO₂. Hub de CO₂ en Cataluña."}  
    ])

@st.cache_data  
def cargar_metadatos_archivos():  
    try:  
        return pd.read_csv("table_20260925.csv")  
    except Exception:  
        return pd.DataFrame(columns=["Archivo", "Formato", "Uso"])

df_proyectos = cargar_datos_proyectos()  
df_archivos = cargar_metadatos_archivos()

colores = {"Biocombustible": "#2E8B57", "H₂ verde": "#1F77B4", "Amoníaco NH₃": "#8E44AD", "e-Fuels": "#E67E22", "e-Metanol": "#C0392B", "Biogás": "#17A2B8", "Captura CO₂": "#7F8C8D"}

seccion = st.sidebar.radio("Navegación:", ["📊 Dashboard y Análisis", "🗺️ Mapa Interactivo", "📑 Documentación Técnica", "✉️ Carta MITECO"])

if seccion == "📊 Dashboard y Análisis":  
    st.title("Estrategia Nacional para la Descarbonización (2026)")  
    df_filtrado = df_proyectos.copy()  
      
    k1, k2, k3, k4 = st.columns(4)  
    k1.metric("Proyectos", len(df_filtrado))  
    k2.metric("Inversión (M€)", f"{df_filtrado['Inversión (M€)'].sum():,.0f}")  
    k3.metric("Producción (t/año)", f"{df_filtrado['Producción (t/año)'].sum():,}")  
    k4.metric("Tecnologías", df_filtrado["Tipo"].nunique())

    col_g1, col_g2 = st.columns(2)  
    with col_g1:  
        df_inv = df_filtrado[df_filtrado["Inversión (M€)"] > 0].sort_values("Inversión (M€)")  
        if not df_inv.empty:  
            fig1 = px.bar(df_inv, x="Inversión (M€)", y="Proyecto", orientation="h", color="Tipo", color_discrete_map=colores, text="Inversión (M€)")  
            st.plotly_chart(fig1, use_container_width=True)  
    with col_g2:  
        df_prod = df_filtrado[df_filtrado["Producción (t/año)"] > 0].groupby("Tipo")["Producción (t/año)"].sum().reset_index()  
        if not df_prod.empty:  
            fig2 = px.pie(df_prod, values="Producción (t/año)", names="Tipo", color="Tipo", color_discrete_map=colores, hole=0.4)  
            st.plotly_chart(fig2, use_container_width=True)

elif seccion == "🗺️ Mapa Interactivo":  
    st.title("Mapa de Proyectos")  
    m = folium.Map(location=[40.0, -3.5], zoom_start=6, tiles="CartoDB positron")  
    for _, row in df_proyectos.dropna(subset=["Lat", "Lon"]).iterrows():  
        folium.Marker(location=[row["Lat"], row["Lon"]], tooltip=row['Proyecto']).add_to(m)  
    st_folium(m, width=1200, height=650)

elif seccion == "📑 Documentación Técnica":  
    st.title("Documentación y Entregables")  
    st.dataframe(df_archivos, use_container_width=True, hide_index=True)  
    st.code("xelatex 03_propuesta.tex", language="bash")

elif seccion == "✉️ Carta MITECO":  
    st.title("Carta de Presentación")  
    st.markdown("Documento listo para registro oficial.")  
