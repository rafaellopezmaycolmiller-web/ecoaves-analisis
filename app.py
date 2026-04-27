import streamlit as st

from src.data.loaders import load_all
from src.services.fusion_service import build_fusion_results
from src.services.ecological_service import add_ecological_consistency
from src.services.metrics_service import build_dashboard_metrics

from src.ui.home import render_home
from src.ui.upload import render_upload
from src.ui.analysis import render_analysis
from src.ui.heatmap import render_heatmap
from src.ui.database import render_database
from src.ui.ecological import render_ecological
from src.ui.validation import render_validation
from src.ui.model_info import render_model_info
from src.ui.impact import render_impact
from src.ui.styles import load_styles


st.set_page_config(
    page_title="EcoAves Perú",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()

data = load_all()

if "custom_data" in st.session_state:
    audio_df = st.session_state["custom_data"]["audio"]
    visual_df = st.session_state["custom_data"]["visual"]
    species_df = st.session_state["custom_data"]["species"]
    zones_df = st.session_state["custom_data"]["zones"]
else:
    audio_df = data["audio"]
    visual_df = data["visual"]
    species_df = data["species"]
    zones_df = data["zones"]

fusion_df = build_fusion_results(audio_df, visual_df)
fusion_df = add_ecological_consistency(fusion_df, zones_df, species_df)

metrics = build_dashboard_metrics(fusion_df)

st.sidebar.markdown("## EcoAves Perú")
st.sidebar.caption("Monitoreo acústico-visual de aves")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Panel de navegación",
    [
        "Inicio",
        "Carga de datos",
        "Modelo IA",
        "Análisis IA",
        "Mapas de calor",
        "Resultados",
        "Impacto",
        "Validación Experta",
        "Registros",
    ],
)

if menu == "Inicio":
    render_home(metrics, fusion_df)

elif menu == "Carga de datos":
    render_upload()

elif menu == "Modelo IA":
    render_model_info()

elif menu == "Análisis IA":
    render_analysis(fusion_df)

elif menu == "Mapas de calor":
    render_heatmap(fusion_df)

elif menu == "Resultados":
    render_ecological(fusion_df)

elif menu == "Impacto":
    render_impact()

elif menu == "Validación Experta":
    render_validation(fusion_df)

elif menu == "Registros":
    render_database(fusion_df)