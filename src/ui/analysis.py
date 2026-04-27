import streamlit as st
import pandas as pd


def render_analysis(df: pd.DataFrame):
    st.title("Análisis IA multimodal")
    st.caption("Comparación entre detección acústica, visual y resultado fusionado.")

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    audio_count = (df["source_mode"] == "audio").sum()
    visual_count = (df["source_mode"] == "visual").sum()
    fusion_count = (df["source_mode"] == "fusionado").sum()
    max_conf = df["fusion_confidence"].max() * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Audio dominante", audio_count)
    col2.metric("Visual dominante", visual_count)
    col3.metric("Fusionados", fusion_count)
    col4.metric("Confianza máxima", f"{max_conf:.1f}%")

    st.markdown("### Filtros")

    col_a, col_b, col_c = st.columns(3)

    species = ["Todas"] + sorted(df["nombre_comun"].dropna().unique().tolist())
    modes = ["Todas"] + sorted(df["source_mode"].dropna().unique().tolist())
    zones = ["Todas"] + sorted(df["nombre_zona"].dropna().unique().tolist())

    selected_species = col_a.selectbox("Especie", species)
    selected_mode = col_b.selectbox("Modalidad", modes)
    selected_zone = col_c.selectbox("Zona", zones)

    filtered = df.copy()

    if selected_species != "Todas":
        filtered = filtered[filtered["nombre_comun"] == selected_species]

    if selected_mode != "Todas":
        filtered = filtered[filtered["source_mode"] == selected_mode]

    if selected_zone != "Todas":
        filtered = filtered[filtered["nombre_zona"] == selected_zone]

    st.markdown("### Resultados del análisis")

    st.dataframe(
        filtered[
            [
                "fecha",
                "hora",
                "nombre_comun",
                "nombre_cientifico",
                "nombre_zona",
                "source_mode",
                "confidence_audio",
                "confidence_visual",
                "fusion_confidence",
                "coherencia_ecologica",
            ]
        ],
        use_container_width=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar análisis filtrado",
        data=csv,
        file_name="analisis_multimodal.csv",
        mime="text/csv",
    )