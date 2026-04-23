import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


def render_heatmap(df):
    st.title("Mapas de calor ecológicos")
    st.caption(
        "Representación espacial de densidad, intensidad acústico-visual y coherencia ecológica "
        "de aves en ecosistemas tropicales."
    )

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    st.markdown("### Filtros")

    col1, col2, col3, col4 = st.columns(4)

    especies = ["Todas"] + sorted(df["nombre_comun"].dropna().unique().tolist())
    zonas = ["Todas"] + sorted(df["nombre_zona"].dropna().unique().tolist())
    modalidades = ["Todas"] + sorted(df["source_mode"].dropna().unique().tolist())
    coherencias = ["Todas"] + sorted(df["coherencia_ecologica"].dropna().unique().tolist())

    especie = col1.selectbox("Especie", especies)
    zona = col2.selectbox("Zona", zonas)
    modalidad = col3.selectbox("Modalidad", modalidades)
    coherencia = col4.selectbox("Coherencia ecológica", coherencias)

    filtered = df.copy()

    if especie != "Todas":
        filtered = filtered[filtered["nombre_comun"] == especie]

    if zona != "Todas":
        filtered = filtered[filtered["nombre_zona"] == zona]

    if modalidad != "Todas":
        filtered = filtered[filtered["source_mode"] == modalidad]

    if coherencia != "Todas":
        filtered = filtered[filtered["coherencia_ecologica"] == coherencia]

    if filtered.empty:
        st.warning("No hay registros con los filtros seleccionados.")
        return

    center_lat = filtered["lat"].mean()
    center_lon = filtered["lon"].mean()

    tab1, tab2, tab3 = st.tabs(
        [
            "Densidad de detecciones",
            "Intensidad acústico-visual",
            "Coherencia ecológica",
        ]
    )

    with tab1:
        st.subheader("Mapa de densidad de detecciones")
        st.write("Muestra zonas con mayor concentración de registros.")

        density_data = (
            filtered.groupby(["lat", "lon"])
            .size()
            .reset_index(name="peso")
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        HeatMap(
            data=density_data[["lat", "lon", "peso"]].values.tolist(),
            radius=35,
            blur=25,
            min_opacity=0.35,
        ).add_to(m)

        st_folium(m, width=1100, height=520)

    with tab2:
        st.subheader("Mapa de intensidad acústico-visual")
        st.write("Muestra zonas con mayor confianza promedio del modelo multimodal.")

        intensity_data = (
            filtered.groupby(["lat", "lon"], as_index=False)
            .agg(peso=("fusion_confidence", "mean"))
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        HeatMap(
            data=intensity_data[["lat", "lon", "peso"]].values.tolist(),
            radius=35,
            blur=25,
            min_opacity=0.35,
        ).add_to(m)

        st_folium(m, width=1100, height=520)

    with tab3:
        st.subheader("Mapa de coherencia ecológica")
        st.write(
            "Muestra zonas donde las detecciones coinciden mejor con hábitat y altitud esperada."
        )

        coherence_weights = {
            "alta": 1.0,
            "media": 0.6,
            "baja": 0.3,
        }

        coherence_df = filtered.copy()
        coherence_df["peso"] = coherence_df["coherencia_ecologica"].map(coherence_weights).fillna(0.3)

        coherence_data = (
            coherence_df.groupby(["lat", "lon"], as_index=False)
            .agg(peso=("peso", "mean"))
        )

        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        HeatMap(
            data=coherence_data[["lat", "lon", "peso"]].values.tolist(),
            radius=35,
            blur=25,
            min_opacity=0.35,
        ).add_to(m)

        st_folium(m, width=1100, height=520)

    st.markdown("### Datos utilizados")
    st.dataframe(
        filtered[
            [
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
            ]
        ],
        use_container_width=True,
    )