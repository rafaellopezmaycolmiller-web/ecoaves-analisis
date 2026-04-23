import streamlit as st
import pandas as pd
import os
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EcoAves Perú",
    page_icon="🐦",
    layout="wide"
)

# =========================
# ESTADO
# =========================
if "tema" not in st.session_state:
    st.session_state.tema = "Claro"

if "menu" not in st.session_state:
    st.session_state.menu = "Inicio"

# =========================
# FUNCIONES
# =========================
def file_to_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

# =========================
# DATOS
# =========================
data = {
    "Ave detectada": [
        "Gallito de las rocas", "Tucán", "Colibrí", "Lechuza",
        "Águila", "Perico", "Garza", "Flamenco"
    ],
    "Confianza": [0.95, 0.89, 0.91, 0.78, 0.82, 0.88, 0.80, 0.85],
    "Región": [
        "Tarapoto", "Tarapoto", "Moyobamba", "Rioja",
        "Sierra", "Amazonía", "Costa", "Costa"
    ],
    "Hábitat": [
        "Bosques nublados", "Bosque tropical", "Zonas florales", "Bosques",
        "Zonas montañosas", "Sabana y selva baja", "Zonas húmedas", "Lagunas"
    ],
    "Descripción": [
        "Ave emblemática del Perú.",
        "Ave con pico grande y colorido.",
        "Ave pequeña que se alimenta de néctar.",
        "Ave nocturna con gran audición.",
        "Ave rapaz de gran tamaño.",
        "Ave social de colores verdes.",
        "Ave que habita cerca del agua.",
        "Ave rosada de patas largas."
    ],
    "Latitud": [-6.48, -6.48, -6.03, -6.05, -9.19, -4.21, -12.04, -15.84],
    "Longitud": [-76.37, -76.37, -77.03, -77.17, -75.01, -69.94, -77.04, -70.02],
    "Audio": [
        "audio_tarapoto_01.wav", "audio_tarapoto_02.wav", "audio_moyobamba_01.wav", "audio_rioja_01.wav",
        "audio_sierra_01.wav", "audio_amazonia_01.wav", "audio_costa_01.wav", "audio_costa_02.wav"
    ]
}
df = pd.DataFrame(data)

# =========================
# TEMA
# =========================
if st.session_state.tema == "Claro":
    BG = "#f5f7fb"
    TEXT = "#1f2937"
    HEADER = "#3f3f46"
    BOX = "#ffffff"
    MUTED = "#6b7280"
    BORDER = "#d1d5db"
    CARD_TOP = "#0f766e"
    BTN_BG = "#ffffff"
    BTN_TEXT = "#1f2937"
    BTN_BORDER = "#cbd5e1"
else:
    BG = "#0f172a"
    TEXT = "#f8fafc"
    HEADER = "#111827"
    BOX = "#1f2937"
    MUTED = "#cbd5e1"
    BORDER = "#334155"
    CARD_TOP = "#22c55e"
    BTN_BG = "#1f2937"
    BTN_TEXT = "#f8fafc"
    BTN_BORDER = "#475569"

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

.block-container {{
    max-width: 100%;
    padding-top: 0.5rem !important;
    padding-left: 1rem;
    padding-right: 1rem;
}}

header[data-testid="stHeader"] {{
    height: 0rem;
    background: transparent;
}}

[data-testid="stToolbar"] {{
    visibility: hidden;
    height: 0%;
    position: fixed;
}}
[data-testid="stDecoration"] {{
    display: none;
}}
#MainMenu {{
    visibility: hidden;
}}
footer {{
    visibility: hidden;
}}

.brand-box {{
    background: {HEADER};
    border-radius: 0 0 18px 18px;
    padding: 18px 24px;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 18px;
}}

.brand-text {{
    font-size: 46px;
    font-weight: 900;
    color: white;
    line-height: 1.1;
}}

.white-box {{
    background: {BOX};
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
}}

.section-title {{
    font-size: 30px;
    font-weight: 800;
    color: {TEXT};
    margin-bottom: 12px;
}}

.section-subtitle {{
    color: {MUTED};
    margin-bottom: 18px;
}}

.metric-card {{
    background: {BOX};
    border-radius: 18px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    border-top: 4px solid {CARD_TOP};
}}

.metric-number {{
    font-size: 34px;
    font-weight: 800;
    color: {TEXT};
}}

.metric-label {{
    font-size: 14px;
    color: {MUTED};
}}

div.stButton > button {{
    width: 100%;
    background: {BTN_BG};
    color: {BTN_TEXT};
    border: 1px solid {BTN_BORDER};
    border-radius: 999px;
    padding: 0.7rem 1rem;
    font-size: 15px;
    font-weight: 700;
}}

div.stButton > button:hover {{
    border: 1px solid {CARD_TOP};
    color: {CARD_TOP};
}}

[data-testid="stFileUploader"] {{
    background: {BOX};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 10px;
}}

[data-baseweb="select"] > div {{
    background: {BOX};
    color: {TEXT};
    border-radius: 12px;
}}

div[data-baseweb="select"] {{
    margin-top: 2px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR REAL
# =========================
nav1, nav2, nav3, nav4, nav5, nav6 = st.columns([3.5, 1, 1.2, 1, 1.2, 1.3])

with nav1:
    st.markdown(f"""
    <div class="brand-box">
        <div class="brand-text">EcoAves Perú</div>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    if st.button("Analizar"):
        st.session_state.menu = "Analizar"

with nav3:
    if st.button("Mapa de calor"):
        st.session_state.menu = "Mapa de calor"

with nav4:
    if st.button("Audios"):
        st.session_state.menu = "Audios"

with nav5:
    if st.button("Base de datos"):
        st.session_state.menu = "Base de datos"

with nav6:
    tema = st.selectbox(
        "",
        ["Claro", "Oscuro"],
        index=0 if st.session_state.tema == "Claro" else 1,
        label_visibility="collapsed"
    )
    if tema != st.session_state.tema:
        st.session_state.tema = tema
        st.rerun()

st.write("")

menu = st.session_state.menu

# =========================
# INICIO
# =========================
if menu == "Inicio":
    portada1 = file_to_base64("imagenes/portada1.jpg")
    portada2 = file_to_base64("imagenes/portada2.jpg")
    portada3 = file_to_base64("imagenes/portada3.jpg")

    imagenes = []
    if portada1:
        imagenes.append(portada1)
    if portada2:
        imagenes.append(portada2)
    if portada3:
        imagenes.append(portada3)

    if len(imagenes) > 0:
        slides = ""
        indicadores = ""

        textos = [
            ("Aves en ecosistemas peruanos", "Registro visual de especies presentes en entornos naturales."),
            ("Biodiversidad y monitoreo", "Observación de aves como apoyo al análisis ambiental."),
            ("Especies y hábitats", "Representación de aves asociadas a distintas zonas del Perú.")
        ]

        for i, img in enumerate(imagenes):
            active = "active" if i == 0 else ""
            titulo, descripcion = textos[i] if i < len(textos) else ("EcoAves Perú", "Sistema de monitoreo de aves.")

            slides += f"""
            <div class="carousel-item {active}">
                <img src="data:image/jpg;base64,{img}" class="d-block w-100">
                <div class="carousel-caption d-none d-md-block">
                    <h5>{titulo}</h5>
                    <p>{descripcion}</p>
                </div>
            </div>
            """

            indicadores += f"""
            <button type="button" data-bs-target="#carouselExampleCaptions"
                    data-bs-slide-to="{i}" class="{active}"
                    {'aria-current="true"' if i == 0 else ''}></button>
            """

        carousel_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background: transparent;
                }}
                .carousel-item img {{
                    height: 430px;
                    object-fit: cover;
                    border-radius: 20px;
                }}
                .carousel-caption {{
                    background: rgba(0,0,0,0.35);
                    border-radius: 16px;
                    padding: 18px;
                }}
                .carousel-caption h5 {{
                    font-size: 30px;
                    font-weight: bold;
                }}
                .carousel-caption p {{
                    font-size: 18px;
                }}
            </style>
        </head>
        <body>
            <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    {indicadores}
                </div>

                <div class="carousel-inner">
                    {slides}
                </div>

                <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span>
                </button>

                <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span>
                </button>
            </div>

            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
        </body>
        </html>
        """

        components.html(carousel_html, height=470, scrolling=False)
    else:
        st.warning("No hay imágenes disponibles en la carpeta imagenes.")

    st.write("")

    c0, c1, c2, c3 = st.columns([1, 1, 1, 1])

    with c0:
        if st.button("Inicio"):
            st.session_state.menu = "Inicio"

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{len(df)}</div>
            <div class="metric-label">Registros disponibles</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        prom = round(df["Confianza"].mean() * 100, 1)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{prom}%</div>
            <div class="metric-label">Confianza promedio</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        zonas = df["Región"].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{zonas}</div>
            <div class="metric-label">Zonas registradas</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# ANALIZAR
# =========================
elif menu == "Analizar":
    st.markdown('<div class="section-title">Analizar por región</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Selecciona una región y genera resultados preliminares.</div>', unsafe_allow_html=True)

    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    region = st.selectbox("Selecciona una región", sorted(df["Región"].unique()))
    st.file_uploader("Sube un archivo de audio", type=["wav", "mp3"])
    analizar = st.button("Analizar registros")

    if analizar:
        df_region = df[df["Región"] == region].copy()
        st.success(f"Se analizaron los registros de la región: {region}")
        st.dataframe(df_region, use_container_width=True)

        csv = df_region.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Descargar resultados CSV",
            data=csv,
            file_name=f"resultados_{region.lower()}.csv",
            mime="text/csv"
        )

    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Mapa de calor":
    st.markdown('<div class="section-title">Mapa de detección</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Visualización geográfica referencial de registros por región.</div>', unsafe_allow_html=True)

    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    region_mapa = st.selectbox("Filtrar por región", ["Todas"] + sorted(df["Región"].unique()))

    if region_mapa == "Todas":
        df_mapa = df.copy()
    else:
        df_mapa = df[df["Región"] == region_mapa].copy()

    df_mapa_mostrar = df_mapa.rename(columns={
        "Latitud": "lat",
        "Longitud": "lon"
    })

    st.map(df_mapa_mostrar[["lat", "lon"]])
    st.info("Aquí se mostrará el mapa de calor en una siguiente versión del sistema.")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Audios":
    st.markdown('<div class="section-title">Audios registrados</div>', unsafe_allow_html=True)

    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    st.dataframe(df[["Audio", "Ave detectada", "Región", "Confianza"]], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "Base de datos":
    st.markdown('<div class="section-title">Base de datos preliminar</div>', unsafe_allow_html=True)

    st.markdown('<div class="white-box">', unsafe_allow_html=True)
    filtro = st.selectbox("Filtrar por región", ["Todas"] + sorted(df["Región"].unique()))

    if filtro == "Todas":
        df_filtrado = df.copy()
    else:
        df_filtrado = df[df["Región"] == filtro].copy()

    st.dataframe(df_filtrado, use_container_width=True)
    st.subheader("Frecuencia de especies")
    st.bar_chart(df_filtrado["Ave detectada"].value_counts())
    st.markdown('</div>', unsafe_allow_html=True)