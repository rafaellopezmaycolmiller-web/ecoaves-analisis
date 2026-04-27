import streamlit as st
import pandas as pd


def render_upload():
    st.title("Carga de datos")
    st.caption("Sube archivos CSV para reemplazar la data de prueba del sistema.")

    st.markdown(
        """
        <div class="section-card">
            <h3>Archivos requeridos</h3>
            <p>
                Para ejecutar el análisis multimodal se necesitan registros acústicos, visuales,
                catálogo de especies y zonas geográficas.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    audio_file = st.file_uploader("CSV de eventos acústicos", type=["csv"])
    visual_file = st.file_uploader("CSV de eventos visuales", type=["csv"])
    species_file = st.file_uploader("CSV de catálogo de especies", type=["csv"])
    zones_file = st.file_uploader("CSV de zonas geográficas", type=["csv"])

    if audio_file and visual_file and species_file and zones_file:
        audio_df = pd.read_csv(audio_file)
        visual_df = pd.read_csv(visual_file)
        species_df = pd.read_csv(species_file)
        zones_df = pd.read_csv(zones_file)

        st.session_state["custom_data"] = {
            "audio": audio_df,
            "visual": visual_df,
            "species": species_df,
            "zones": zones_df,
        }

        st.success("Datos cargados correctamente. Ya puedes ir a Análisis IA o Mapas de calor.")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Audio", len(audio_df))
        col2.metric("Visual", len(visual_df))
        col3.metric("Especies", len(species_df))
        col4.metric("Zonas", len(zones_df))

    else:
        st.info("Puedes seguir usando la data de prueba mientras no cargues archivos reales.")