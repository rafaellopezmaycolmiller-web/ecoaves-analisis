import streamlit as st
from src.config.settings import APP_TITLE, APP_SUBTITLE

def render_home(metrics: dict):
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Registros procesados", metrics["total_registros"])
    col2.metric("Especies detectadas", metrics["especies_detectadas"])
    col3.metric("Confianza multimodal", f'{metrics["confianza_promedio"]}%')
    col4.metric("Zonas activas", metrics["zonas_activas"])

    st.markdown("### Resumen del sistema")
    st.write(
        "EcoAves Perú integra evidencia acústica, visual y espacial "
        "para detectar especies, estimar actividad biológica y generar mapas de calor."
    )