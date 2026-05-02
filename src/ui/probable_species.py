import os
from datetime import datetime

import pandas as pd
import streamlit as st

from src.services.apis.ebird_api import (
    get_recent_observations_by_geo,
    normalize_ebird_observations,
)


TARAPOTO_LAT = -6.4869
TARAPOTO_LON = -76.3597
EBIRD_CSV_PATH = "data/raw/ebird_tarapoto_recent.csv"


def load_local_ebird_data() -> pd.DataFrame:
    if not os.path.exists(EBIRD_CSV_PATH):
        return pd.DataFrame()

    return pd.read_csv(EBIRD_CSV_PATH)


def get_file_updated_time(path: str) -> str:
    if not os.path.exists(path):
        return "No disponible"

    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def render_species_card(row):
    nombre_comun = row.get("nombre_comun", "No disponible")
    nombre_cientifico = row.get("nombre_cientifico", "No disponible")
    ubicacion = row.get("ubicacion", "No disponible")
    fecha = row.get("fecha_observacion", "No disponible")
    cantidad = row.get("cantidad", "No reportada")

    st.markdown(
        f"""
        <div class="section-card">
            <h3>{nombre_comun}</h3>
            <p><i>{nombre_cientifico}</i></p>
            <p><b>Ubicación reciente:</b> {ubicacion}</p>
            <p><b>Última observación:</b> {fecha}</p>
            <p><b>Cantidad reportada:</b> {cantidad}</p>
            <span class="tag">Candidata regional</span>
            <span class="tag">eBird</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probable_species():
    st.markdown("## Aves probables en San Martín")
    st.caption(
        "Consulta registros recientes de eBird para identificar especies observadas cerca de Tarapoto."
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>¿Por qué esta sección es importante?</h3>
            <p>
                Las aves probables permiten contextualizar las detecciones de EcoAves.
                Si una especie detectada aparece también en registros recientes de eBird,
                el sistema gana respaldo regional. Si no aparece, puede requerir validación experta.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    lat = col1.number_input("Latitud", value=TARAPOTO_LAT, format="%.6f")
    lon = col2.number_input("Longitud", value=TARAPOTO_LON, format="%.6f")
    distance = col3.slider("Radio (km)", min_value=1, max_value=50, value=25)
    days_back = col4.slider("Días atrás", min_value=1, max_value=30, value=30)

    st.markdown("### Estado de actualización")

    file_time = get_file_updated_time(EBIRD_CSV_PATH)

    s1, s2, s3 = st.columns(3)
    s1.metric("Archivo local", "Disponible" if os.path.exists(EBIRD_CSV_PATH) else "No existe")
    s2.metric("Última actualización", file_time)
    s3.metric("Fuente", "eBird API")

    if st.button("Actualizar especies desde eBird", use_container_width=True):
        with st.spinner("Consultando eBird y actualizando registros regionales..."):
            try:
                records = get_recent_observations_by_geo(
                    lat=lat,
                    lng=lon,
                    distance_km=distance,
                    days_back=days_back,
                    max_results=100,
                )

                normalized = normalize_ebird_observations(records)
                df = pd.DataFrame(normalized)

                if df.empty:
                    st.warning("eBird respondió correctamente, pero no se encontraron registros para esta zona.")
                    return

                os.makedirs("data/raw", exist_ok=True)

                df.to_csv(
                    EBIRD_CSV_PATH,
                    index=False,
                    encoding="utf-8",
                )

                st.session_state["ebird_species_df"] = df
                st.session_state["ebird_last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state["ebird_last_params"] = {
                    "lat": lat,
                    "lon": lon,
                    "distance": distance,
                    "days_back": days_back,
                    "records": len(df),
                    "species": df["nombre_cientifico"].nunique()
                    if "nombre_cientifico" in df.columns
                    else 0,
                }

                st.success(
                    f"Datos actualizados correctamente desde eBird: {len(df)} registros descargados."
                )

            except Exception as e:
                st.error(f"No se pudo consultar eBird: {e}")

    if "ebird_last_update" in st.session_state:
        params = st.session_state.get("ebird_last_params", {})

        st.success(
            f"""
            Última consulta realizada en esta sesión: **{st.session_state["ebird_last_update"]}**  
            Parámetros: lat **{params.get("lat")}**, lon **{params.get("lon")}**, radio **{params.get("distance")} km**, últimos **{params.get("days_back")} días**.  
            Resultado: **{params.get("records")} registros** y **{params.get("species")} especies únicas**.
            """
        )

    if "ebird_species_df" in st.session_state:
        df = st.session_state["ebird_species_df"]
    else:
        df = load_local_ebird_data()

    if df.empty:
        st.warning("Aún no hay datos descargados. Presiona 'Actualizar especies desde eBird'.")
        return

    especies_unicas = df.drop_duplicates(subset=["nombre_cientifico"]).copy()

    col_a, col_b, col_c, col_d = st.columns(4)

    col_a.metric("Registros eBird", len(df))
    col_b.metric("Especies únicas", especies_unicas["nombre_cientifico"].nunique())
    col_c.metric("Ubicaciones", df["ubicacion"].nunique() if "ubicacion" in df.columns else 0)
    col_d.metric("Radio analizado", f"{distance} km")

    with st.expander("Ver vista previa de la actualización", expanded=False):
        st.caption(
            "Esta vista previa confirma qué registros están cargados actualmente desde eBird."
        )

        preview_columns = [
            "nombre_comun",
            "nombre_cientifico",
            "codigo_ebird",
            "fecha_observacion",
            "ubicacion",
            "cantidad",
        ]

        existing_preview_columns = [c for c in preview_columns if c in df.columns]

        st.dataframe(
            df[existing_preview_columns].head(10),
            width="stretch",
            hide_index=True,
        )

    st.markdown("### Buscar especie")

    search = st.text_input(
        "Busca por nombre común, científico o ubicación",
        placeholder="Ejemplo: Tanager, Piaya cayana, Tarapoto...",
    )

    filtered = especies_unicas.copy()

    if search:
        search_lower = search.lower()

        filtered = filtered[
            filtered["nombre_comun"].astype(str).str.lower().str.contains(search_lower, na=False)
            | filtered["nombre_cientifico"].astype(str).str.lower().str.contains(search_lower, na=False)
            | filtered["ubicacion"].astype(str).str.lower().str.contains(search_lower, na=False)
        ]

    st.markdown("### Catálogo regional eBird")

    if filtered.empty:
        st.warning("No se encontraron especies con ese filtro.")
    else:
        rows = filtered.head(12).to_dict(orient="records")

        for i in range(0, len(rows), 3):
            cols = st.columns(3)

            for col, row in zip(cols, rows[i:i + 3]):
                with col:
                    render_species_card(row)

    with st.expander("Ver tabla completa de aves probables", expanded=False):
        columnas = [
            "nombre_comun",
            "nombre_cientifico",
            "codigo_ebird",
            "fecha_observacion",
            "ubicacion",
            "cantidad",
        ]

        columnas_disponibles = [c for c in columnas if c in especies_unicas.columns]

        st.dataframe(
            especies_unicas[columnas_disponibles],
            width="stretch",
            hide_index=True,
        )

        csv = especies_unicas.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar lista de aves probables",
            data=csv,
            file_name="aves_probables_san_martin.csv",
            mime="text/csv",
        )