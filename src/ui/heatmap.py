import streamlit as st
import pandas as pd
import folium

from folium.plugins import HeatMap
from streamlit_folium import st_folium


def _safe_options(df: pd.DataFrame, column: str):
    if column not in df.columns:
        return ["Todas"]

    return ["Todas"] + sorted(df[column].dropna().unique().tolist())


def _apply_filters(df, especie, zona, modalidad, coherencia):
    filtered = df.copy()

    if especie != "Todas" and "nombre_comun" in filtered.columns:
        filtered = filtered[filtered["nombre_comun"] == especie]

    if zona != "Todas" and "nombre_zona" in filtered.columns:
        filtered = filtered[filtered["nombre_zona"] == zona]

    if modalidad != "Todas" and "source_mode" in filtered.columns:
        filtered = filtered[filtered["source_mode"] == modalidad]

    if coherencia != "Todas" and "coherencia_ecologica" in filtered.columns:
        filtered = filtered[filtered["coherencia_ecologica"] == coherencia]

    return filtered


def _build_base_map(filtered):
    center_lat = filtered["lat"].mean()
    center_lon = filtered["lon"].mean()

    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles="OpenStreetMap",
    )


def _render_map_summary(filtered, map_type):
    registros = len(filtered)
    zonas = filtered["nombre_zona"].nunique() if "nombre_zona" in filtered.columns else 0
    especies = filtered["nombre_comun"].nunique() if "nombre_comun" in filtered.columns else 0

    zona_top = "Sin datos"
    especie_top = "Sin datos"

    if "nombre_zona" in filtered.columns and not filtered["nombre_zona"].dropna().empty:
        zona_top = filtered["nombre_zona"].value_counts().idxmax()

    if "nombre_comun" in filtered.columns and not filtered["nombre_comun"].dropna().empty:
        especie_top = filtered["nombre_comun"].value_counts().idxmax()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Registros usados", registros)
    col2.metric("Zonas activas", zonas)
    col3.metric("Especies", especies)
    col4.metric("Zona principal", zona_top)

    if map_type == "Densidad de detecciones":
        st.info(
            f"""
            Este mapa representa la **concentración espacial de registros**.  
            Las zonas con mayor intensidad indican lugares donde EcoAves acumuló más detecciones.
            En el conjunto filtrado, la especie más frecuente es **{especie_top}**.
            """
        )

    elif map_type == "Intensidad acústico-visual":
        avg_confidence = 0

        if "fusion_confidence" in filtered.columns and not filtered["fusion_confidence"].dropna().empty:
            avg_confidence = filtered["fusion_confidence"].mean() * 100

        st.info(
            f"""
            Este mapa representa la **confianza promedio del modelo multimodal**.  
            No mide solo cantidad de registros, sino qué zonas tienen detecciones con mayor confianza acústica,
            visual o fusionada. La confianza promedio del filtro actual es **{avg_confidence:.1f}%**.
            """
        )

    elif map_type == "Coherencia ecológica":
        coherencia_top = "Sin datos"

        if "coherencia_ecologica" in filtered.columns and not filtered["coherencia_ecologica"].dropna().empty:
            coherencia_top = filtered["coherencia_ecologica"].value_counts().idxmax()

        st.info(
            f"""
            Este mapa representa qué zonas tienen mayor **coherencia ecológica**, es decir,
            dónde las detecciones coinciden mejor con condiciones esperadas de hábitat, altitud
            y distribución. La coherencia más frecuente es **{coherencia_top}**.
            """
        )


def render_heatmap(df):
    st.markdown("## Mapas de calor ecológicos")
    st.caption(
        "Representación espacial de densidad, intensidad acústico-visual y coherencia ecológica "
        "de las detecciones del sistema."
    )

    if df is None or df.empty:
        st.warning("No hay datos disponibles para generar mapas.")
        return

    required_columns = ["lat", "lon"]

    for column in required_columns:
        if column not in df.columns:
            st.error(f"No se encontró la columna requerida: {column}")
            return

    st.markdown("### Filtros del mapa")

    col1, col2, col3, col4 = st.columns(4)

    especies = _safe_options(df, "nombre_comun")
    zonas = _safe_options(df, "nombre_zona")
    modalidades = _safe_options(df, "source_mode")
    coherencias = _safe_options(df, "coherencia_ecologica")

    especie = col1.selectbox("Especie", especies)
    zona = col2.selectbox("Zona", zonas)
    modalidad = col3.selectbox("Modalidad", modalidades)
    coherencia = col4.selectbox("Coherencia ecológica", coherencias)

    filtered = _apply_filters(
        df=df,
        especie=especie,
        zona=zona,
        modalidad=modalidad,
        coherencia=coherencia,
    )

    if filtered.empty:
        st.warning("No hay registros con los filtros seleccionados.")
        return

    st.markdown("### Tipo de análisis espacial")

    map_type = st.radio(
        "Selecciona el mapa que deseas visualizar",
        [
            "Densidad de detecciones",
            "Intensidad acústico-visual",
            "Coherencia ecológica",
        ],
        horizontal=True,
    )

    _render_map_summary(filtered, map_type)

    m = _build_base_map(filtered)

    if map_type == "Densidad de detecciones":
        heatmap_data = (
            filtered.groupby(["lat", "lon"])
            .size()
            .reset_index(name="peso")
        )

        st.markdown("### Mapa de densidad de detecciones")
        st.write(
            "Muestra las zonas donde se concentran más registros procesados por EcoAves."
        )

    elif map_type == "Intensidad acústico-visual":
        if "fusion_confidence" not in filtered.columns:
            st.warning("No existe la columna `fusion_confidence` para calcular intensidad.")
            return

        heatmap_data = (
            filtered.groupby(["lat", "lon"], as_index=False)
            .agg(peso=("fusion_confidence", "mean"))
        )

        st.markdown("### Mapa de intensidad acústico-visual")
        st.write(
            "Muestra las zonas donde el modelo presenta mayor confianza promedio en sus detecciones."
        )

    else:
        if "coherencia_ecologica" not in filtered.columns:
            st.warning("No existe la columna `coherencia_ecologica` para calcular coherencia.")
            return

        coherence_weights = {
            "alta": 1.0,
            "media": 0.6,
            "baja": 0.3,
        }

        coherence_df = filtered.copy()

        coherence_df["peso"] = (
            coherence_df["coherencia_ecologica"]
            .map(coherence_weights)
            .fillna(0.3)
        )

        heatmap_data = (
            coherence_df.groupby(["lat", "lon"], as_index=False)
            .agg(peso=("peso", "mean"))
        )

        st.markdown("### Mapa de coherencia ecológica")
        st.write(
            "Muestra las zonas donde las detecciones coinciden mejor con hábitat, altitud y distribución esperada."
        )

    HeatMap(
        data=heatmap_data[["lat", "lon", "peso"]].values.tolist(),
        radius=35,
        blur=25,
        min_opacity=0.35,
    ).add_to(m)

    st_folium(
        m,
        width=1100,
        height=520,
    )

    with st.expander("Ver registros usados para este mapa", expanded=False):
        columns = [
            "fecha",
            "hora",
            "nombre_comun",
            "nombre_cientifico",
            "nombre_zona",
            "ecosistema",
            "altitud",
            "source_mode",
            "confidence_audio",
            "confidence_visual",
            "fusion_confidence",
            "coherencia_ecologica",
            "coherencia_regional",
        ]

        existing_columns = [col for col in columns if col in filtered.columns]

        st.dataframe(
            filtered[existing_columns],
            width="stretch",
            hide_index=True,
        )