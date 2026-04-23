import streamlit     as st
from src.data.loaders import load_all
from src.services.fusion_service import build_fusion_results
from src.services.ecological_service import add_ecological_consistency
from src.services.metrics_service import build_dashboard_metrics
from src.services.heatmap_service import build_heatmap_data
from src.ui.home import render_home
from src.ui.analysis import render_analysis
from src.ui.database import render_database
from src.ui.heatmap import render_heatmap
from src.data.mock_generator import generate_mock_data
from src.ui.ecological import render_ecological

st.set_page_config(
    page_title="EcoAves Perú",
    layout="wide",
    initial_sidebar_state="expanded"
)

data = load_all()
audio_df = data["audio"]
visual_df = data["visual"]
species_df = data["species"]
zones_df = data["zones"]

fusion_df = build_fusion_results(audio_df, visual_df)
fusion_df = add_ecological_consistency(fusion_df, zones_df, species_df)
df_mock = generate_mock_data(300)

metrics = build_dashboard_metrics(fusion_df)
heatmap_df = build_heatmap_data(fusion_df)

menu = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Análisis multimodal", "Mapas de calor", "Registros ecológicos", "Resultados ecológicos"]
)

if menu == "Inicio":
    render_home(metrics)
elif menu == "Análisis multimodal":
    render_analysis(fusion_df)
elif menu == "Mapas de calor":
    render_heatmap(fusion_df)
elif menu == "Registros ecológicos":
    render_database(fusion_df)
elif menu == "Resultados ecológicos":
    render_ecological(fusion_df)