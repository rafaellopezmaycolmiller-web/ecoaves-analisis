import streamlit as st

from src.data.loaders import load_all
from src.services.fusion_service import build_fusion_results
from src.services.ecological_service import add_ecological_consistency
from src.services.metrics_service import build_dashboard_metrics

from src.services.regional_service import (
    load_ebird_species,
    add_regional_coherence,
    calculate_regional_coverage,
    get_priority_species_to_add,
)

from src.ui.styles import load_styles

from src.ui.dashboard_home import render_dashboard_home
from src.ui.monitoring import render_monitoring
from src.ui.ecological_intelligence import render_ecological_intelligence
from src.ui.expert_validation import render_expert_validation


st.set_page_config(
    page_title="EcoAves Perú",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_styles()

# =========================
# CARGA DE DATOS
# =========================

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

# =========================
# PROCESAMIENTO PRINCIPAL
# =========================

fusion_df = build_fusion_results(audio_df, visual_df)
fusion_df = add_ecological_consistency(fusion_df, zones_df, species_df)

# =========================
# INTEGRACIÓN REGIONAL EBIRD
# =========================

ebird_df = load_ebird_species()

fusion_df = add_regional_coherence(
    fusion_df=fusion_df,
    ebird_df=ebird_df,
)

regional_coverage = calculate_regional_coverage(
    fusion_df=fusion_df,
    ebird_df=ebird_df,
)

priority_species_df = get_priority_species_to_add(
    fusion_df=fusion_df,
    ebird_df=ebird_df,
    limit=10,
)

# =========================
# MÉTRICAS
# =========================

metrics = build_dashboard_metrics(fusion_df)

# =========================
# SIDEBAR
# =========================

pages = [
    "Inicio",
    "Monitoreo",
    "Inteligencia ecológica",
    "Validación",
]

if "main_menu" not in st.session_state:
    st.session_state["main_menu"] = "Inicio"

if "go_to_page" in st.session_state:
    st.session_state["main_menu"] = st.session_state["go_to_page"]
    del st.session_state["go_to_page"]

st.sidebar.markdown("## EcoAves Perú")
st.sidebar.caption("Monitoreo acústico-visual de aves")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Panel de navegación",
    pages,
    key="main_menu",
)

# =========================
# NAVEGACIÓN PRINCIPAL
# =========================

if menu == "Inicio":
    render_dashboard_home(
        metrics=metrics,
        fusion_df=fusion_df,
        regional_coverage=regional_coverage,
    )

elif menu == "Monitoreo":
    render_monitoring(
        fusion_df=fusion_df,
        audio_df=audio_df,
        visual_df=visual_df,
    )

elif menu == "Inteligencia ecológica":
    render_ecological_intelligence(
        fusion_df=fusion_df,
        heatmap_df=fusion_df,
        regional_coverage=regional_coverage,
        priority_species_df=priority_species_df,
    )

elif menu == "Validación":
    render_expert_validation(fusion_df)