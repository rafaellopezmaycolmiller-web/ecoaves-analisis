import streamlit as st
import pandas as pd

def render_analysis(df: pd.DataFrame):
    st.subheader("Análisis multimodal")

    species = ["Todas"] + sorted(df["nombre_comun"].dropna().unique().tolist())
    selected_species = st.selectbox("Filtrar por especie", species)

    filtered = df.copy()
    if selected_species != "Todas":
        filtered = filtered[filtered["nombre_comun"] == selected_species]

    st.dataframe(
        filtered[
            [
                "fecha", "hora", "nombre_comun", "nombre_cientifico",
                "source_mode", "confidence_audio", "confidence_visual",
                "fusion_confidence", "coherencia_ecologica", "nombre_zona"
            ]
        ],
        use_container_width=True
    )