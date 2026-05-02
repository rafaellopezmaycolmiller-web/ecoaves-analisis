import streamlit as st
import pandas as pd


def render_analysis(df: pd.DataFrame):
    st.title("Análisis IA multimodal")
    st.caption(
        "Comparación entre detección acústica, visual, resultado fusionado y coherencia regional con eBird."
    )

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    # =========================
    # MÉTRICAS PRINCIPALES
    # =========================

    audio_count = (df["source_mode"] == "audio").sum() if "source_mode" in df.columns else 0
    visual_count = (df["source_mode"] == "visual").sum() if "source_mode" in df.columns else 0
    fusion_count = (df["source_mode"] == "fusionado").sum() if "source_mode" in df.columns else 0

    max_conf = (
        df["fusion_confidence"].max() * 100
        if "fusion_confidence" in df.columns and not df["fusion_confidence"].dropna().empty
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Audio dominante", audio_count)
    col2.metric("Visual dominante", visual_count)
    col3.metric("Fusionados", fusion_count)
    col4.metric("Confianza máxima", f"{max_conf:.1f}%")

    # =========================
    # COHERENCIA REGIONAL
    # =========================

    if "coherencia_regional" in df.columns:
        st.markdown("### Coherencia regional con eBird")

        regional_counts = df["coherencia_regional"].value_counts()

        col_a, col_b, col_c = st.columns(3)

        col_a.metric(
            "Presentes en eBird",
            int(regional_counts.get("Presente en eBird", 0)),
        )

        col_b.metric(
            "No registrados recientemente",
            int(regional_counts.get("No registrado recientemente", 0)),
        )

        col_c.metric(
            "Sin referencia",
            int(regional_counts.get("Sin referencia eBird", 0)),
        )

        st.info(
            """
            Esta comparación permite validar si las especies detectadas por EcoAves aparecen
            dentro de los registros recientes de eBird para la zona de análisis. No reemplaza
            la validación experta, pero ayuda a priorizar qué registros revisar.
            """
        )

    # =========================
    # FILTROS
    # =========================

    st.markdown("### Filtros")

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    species = (
        ["Todas"] + sorted(df["nombre_comun"].dropna().unique().tolist())
        if "nombre_comun" in df.columns
        else ["Todas"]
    )

    modes = (
        ["Todas"] + sorted(df["source_mode"].dropna().unique().tolist())
        if "source_mode" in df.columns
        else ["Todas"]
    )

    zones = (
        ["Todas"] + sorted(df["nombre_zona"].dropna().unique().tolist())
        if "nombre_zona" in df.columns
        else ["Todas"]
    )

    regional_states = (
        ["Todas"] + sorted(df["coherencia_regional"].dropna().unique().tolist())
        if "coherencia_regional" in df.columns
        else ["Todas"]
    )

    selected_species = col_f1.selectbox("Especie", species)
    selected_mode = col_f2.selectbox("Modalidad", modes)
    selected_zone = col_f3.selectbox("Zona", zones)
    selected_regional = col_f4.selectbox("Coherencia regional", regional_states)

    filtered = df.copy()

    if selected_species != "Todas" and "nombre_comun" in filtered.columns:
        filtered = filtered[filtered["nombre_comun"] == selected_species]

    if selected_mode != "Todas" and "source_mode" in filtered.columns:
        filtered = filtered[filtered["source_mode"] == selected_mode]

    if selected_zone != "Todas" and "nombre_zona" in filtered.columns:
        filtered = filtered[filtered["nombre_zona"] == selected_zone]

    if selected_regional != "Todas" and "coherencia_regional" in filtered.columns:
        filtered = filtered[filtered["coherencia_regional"] == selected_regional]

    # =========================
    # RESUMEN DEL FILTRO
    # =========================

    st.markdown("### Resultado filtrado")

    col_r1, col_r2, col_r3 = st.columns(3)

    col_r1.metric("Registros filtrados", len(filtered))

    if "nombre_comun" in filtered.columns:
        col_r2.metric("Especies filtradas", filtered["nombre_comun"].nunique())
    else:
        col_r2.metric("Especies filtradas", 0)

    if "fusion_confidence" in filtered.columns and not filtered["fusion_confidence"].dropna().empty:
        col_r3.metric(
            "Confianza promedio",
            f"{filtered['fusion_confidence'].mean() * 100:.1f}%",
        )
    else:
        col_r3.metric("Confianza promedio", "0%")

    # =========================
    # TABLA FINAL
    # =========================

    columnas = [
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
        "coherencia_regional",
    ]

    columnas_disponibles = [col for col in columnas if col in filtered.columns]

    st.dataframe(
        filtered[columnas_disponibles],
        use_container_width=True,
    )

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar análisis filtrado",
        data=csv,
        file_name="analisis_multimodal_ecoaves.csv",
        mime="text/csv",
    )