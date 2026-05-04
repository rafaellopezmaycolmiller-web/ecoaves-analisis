import streamlit as st
import pandas as pd

from src.ui.upload import render_upload


def _first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _safe_count(df, column=None, value=None):
    if df is None or df.empty:
        return 0

    if column is None:
        return len(df)

    if column not in df.columns:
        return 0

    return int((df[column] == value).sum())


def _safe_nunique(df, column):
    if df is None or df.empty or column not in df.columns:
        return 0
    return int(df[column].nunique())


def _build_confidence_series(df):
    if df is None or df.empty:
        return pd.Series(dtype=float)

    if "fusion_confidence" in df.columns:
        return pd.to_numeric(df["fusion_confidence"], errors="coerce").fillna(0)

    audio = pd.to_numeric(df.get("confidence_audio", 0), errors="coerce").fillna(0)
    visual = pd.to_numeric(df.get("confidence_visual", 0), errors="coerce").fillna(0)

    if len(audio) == 0 and len(visual) == 0:
        return pd.Series(dtype=float)

    return pd.concat([audio, visual], axis=1).max(axis=1)


def _get_regional_column(df):
    candidates = [
        "coherencia_regional",
        "regional_status",
        "estado_regional",
        "ebird_status",
        "coherencia_ebird",
    ]
    return _first_existing_column(df, candidates)


def _apply_filters(df, especie, modalidad, zona, coherencia):
    filtered = df.copy()

    if especie != "Todas" and "nombre_comun" in filtered.columns:
        filtered = filtered[filtered["nombre_comun"] == especie]

    if modalidad != "Todas" and "source_mode" in filtered.columns:
        filtered = filtered[filtered["source_mode"] == modalidad]

    if zona != "Todas" and "nombre_zona" in filtered.columns:
        filtered = filtered[filtered["nombre_zona"] == zona]

    regional_col = _get_regional_column(filtered)
    if coherencia != "Todas" and regional_col is not None:
        filtered = filtered[filtered[regional_col] == coherencia]

    return filtered


def render_monitoring(fusion_df, audio_df=None, visual_df=None):
    st.markdown("## Monitoreo y captura de evidencia")
    st.caption(
        "Vista operativa del sistema: aquí cargas evidencia, revisas detecciones "
        "y consultas la coherencia regional con eBird sin cambiar de pantalla."
    )

    if fusion_df is None or fusion_df.empty:
        st.warning("No hay registros disponibles para mostrar en monitoreo.")
        with st.expander("Cargar evidencia", expanded=True):
            render_upload()
        return

    confidence_series = _build_confidence_series(fusion_df)
    regional_col = _get_regional_column(fusion_df)

    total_registros = len(fusion_df)
    total_especies = _safe_nunique(fusion_df, "nombre_comun")
    total_audio = _safe_count(fusion_df, "source_mode", "audio")
    total_visual = _safe_count(fusion_df, "source_mode", "visual")
    total_fusionados = _safe_count(fusion_df, "source_mode", "fusionado")
    confianza_promedio = float(confidence_series.mean() * 100) if len(confidence_series) > 0 else 0.0

    presentes_ebird = 0
    no_recientes = 0
    sin_referencia = 0

    if regional_col is not None:
        presentes_ebird = int((fusion_df[regional_col] == "Presente en eBird").sum())
        no_recientes = int((fusion_df[regional_col] == "No registrado recientemente").sum())
        sin_referencia = int((fusion_df[regional_col] == "Sin referencia").sum())

    # ======================================
    # RESUMEN OPERATIVO
    # ======================================
    st.markdown("### Resumen operativo")
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Registros", total_registros)
    c2.metric("Especies", total_especies)
    c3.metric("Audio", total_audio)
    c4.metric("Visual", total_visual)
    c5.metric("Fusionados", total_fusionados)

    st.markdown("### Coherencia regional")
    c6, c7, c8, c9 = st.columns(4)

    c6.metric("Presentes en eBird", presentes_ebird)
    c7.metric("No registrados recientemente", no_recientes)
    c8.metric("Sin referencia", sin_referencia)
    c9.metric("Confianza promedio", f"{confianza_promedio:.1f}%")

    st.info(
        "Esta vista resume la operación completa del monitoreo: "
        "puedes cargar evidencia, revisar la salida IA y analizar "
        "si las detecciones coinciden o no con la referencia regional de eBird."
    )

    # ======================================
    # CARGA DE EVIDENCIA
    # ======================================
    with st.expander("Ingresar nuevos registros (CSV o Inferencia IA)", expanded=False):
        st.markdown(
            "Sube archivos CSV por lotes o utiliza un archivo de audio/imagen para ejecutar "
            "una inferencia de IA en tiempo real y validar con eBird."
        )
        render_upload()

    # ======================================
    # FILTROS
    # ======================================
    st.markdown("### Filtros de análisis")

    especie_options = ["Todas"]
    modalidad_options = ["Todas"]
    zona_options = ["Todas"]
    coherencia_options = ["Todas"]

    if "nombre_comun" in fusion_df.columns:
        especie_options += sorted(fusion_df["nombre_comun"].dropna().unique().tolist())

    if "source_mode" in fusion_df.columns:
        modalidad_options += sorted(fusion_df["source_mode"].dropna().unique().tolist())

    if "nombre_zona" in fusion_df.columns:
        zona_options += sorted(fusion_df["nombre_zona"].dropna().unique().tolist())

    if regional_col is not None:
        coherencia_options += sorted(fusion_df[regional_col].dropna().unique().tolist())

    f1, f2, f3, f4 = st.columns(4)

    especie = f1.selectbox("Especie", especie_options)
    modalidad = f2.selectbox("Modalidad", modalidad_options)
    zona = f3.selectbox("Zona", zona_options)
    coherencia = f4.selectbox("Coherencia regional", coherencia_options)

    filtered_df = _apply_filters(fusion_df, especie, modalidad, zona, coherencia)

    filtered_confidence = _build_confidence_series(filtered_df)
    confianza_filtrada = float(filtered_confidence.mean() * 100) if len(filtered_confidence) > 0 else 0.0
    especies_filtradas = filtered_df["nombre_comun"].nunique() if "nombre_comun" in filtered_df.columns else 0

    # ======================================
    # RESULTADO FILTRADO
    # ======================================
    st.markdown("### Resultado filtrado")
    r1, r2, r3 = st.columns(3)

    r1.metric("Registros filtrados", len(filtered_df))
    r2.metric("Especies filtradas", especies_filtradas)
    r3.metric("Confianza promedio", f"{confianza_filtrada:.1f}%")

    display_columns = [
        "fecha",
        "hora",
        "nombre_comun",
        "nombre_cientifico",
        "nombre_zona",
        "source_mode",
        "confidence_audio",
        "confidence_visual",
        "fusion_confidence",
    ]

    if regional_col is not None and regional_col not in display_columns:
        display_columns.append(regional_col)

    existing_columns = [col for col in display_columns if col in filtered_df.columns]

    if existing_columns:
        st.dataframe(
            filtered_df[existing_columns],
            width="stretch",
            hide_index=True,
        )
    else:
        st.dataframe(
            filtered_df,
            width="stretch",
            hide_index=True,
        )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar análisis filtrado",
        data=csv_data,
        file_name="ecoaves_monitoreo_filtrado.csv",
        mime="text/csv",
    )

    # ======================================
    # REGISTROS DETECTADOS
    # ======================================
    with st.expander("Ver base completa de registros detectados", expanded=False):
        st.caption(
            "Aquí se muestra la base completa procesada por el sistema, "
            "incluyendo columnas internas del análisis multimodal."
        )
        st.dataframe(
            fusion_df,
            width="stretch",
            hide_index=True,
        )