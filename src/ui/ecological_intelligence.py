import streamlit as st
import pandas as pd

from src.ui.heatmap import render_heatmap
from src.ui.ecological import render_ecological
from src.ui.probable_species import render_probable_species


def _get_top_value(df: pd.DataFrame, column: str, default: str = "Sin datos"):
    if df is None or df.empty:
        return default

    if column not in df.columns:
        return default

    if df[column].dropna().empty:
        return default

    return df[column].value_counts().idxmax()


def _safe_nunique(df: pd.DataFrame, column: str) -> int:
    if df is None or df.empty or column not in df.columns:
        return 0

    return int(df[column].nunique())


def _safe_len(df: pd.DataFrame) -> int:
    if df is None or df.empty:
        return 0

    return len(df)


def _render_priority_species(priority_species_df: pd.DataFrame | None):
    st.markdown("### Especies prioritarias por incorporar")

    if priority_species_df is None or priority_species_df.empty:
        st.info("No hay especies prioritarias disponibles por el momento.")
        return

    st.caption(
        "Estas especies aparecen en registros recientes de eBird, pero aún no están cubiertas "
        "por el catálogo piloto de EcoAves. Sirven como guía para ampliar el dataset."
    )

    display_columns = [
        "nombre_comun",
        "nombre_cientifico",
        "codigo_ebird",
        "fecha_observacion",
        "ubicacion",
        "cantidad",
    ]

    existing_columns = [
        col for col in display_columns if col in priority_species_df.columns
    ]

    st.dataframe(
        priority_species_df[existing_columns],
        width="stretch",
        hide_index=True,
    )

    csv = priority_species_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar especies prioritarias",
        data=csv,
        file_name="especies_prioritarias_ecoaves.csv",
        mime="text/csv",
    )


def render_ecological_intelligence(
    fusion_df,
    heatmap_df,
    regional_coverage=None,
    priority_species_df=None,
):
    st.markdown("## Inteligencia ecológica regional")
    st.caption(
        "Vista de interpretación ecológica: integra especies probables de eBird, "
        "cobertura regional, mapas de calor y diagnóstico del monitoreo."
    )

    if fusion_df is None:
        fusion_df = pd.DataFrame()

    if heatmap_df is None:
        heatmap_df = fusion_df

    especies_detectadas = _safe_nunique(fusion_df, "nombre_comun")
    zonas_activas = _safe_nunique(fusion_df, "nombre_zona")
    registros = _safe_len(fusion_df)

    especie_dominante = _get_top_value(fusion_df, "nombre_comun")
    zona_prioritaria = _get_top_value(fusion_df, "nombre_zona")
    coherencia_principal = _get_top_value(fusion_df, "coherencia_ecologica")

    especies_probables = 0
    coincidencias = 0
    cobertura = 0
    brecha = 0

    if regional_coverage:
        especies_probables = regional_coverage.get("especies_probables", 0)
        coincidencias = regional_coverage.get("especies_coincidentes", 0)
        cobertura = regional_coverage.get("cobertura_porcentaje", 0)
        brecha = regional_coverage.get("brecha_regional", 0)

    # ======================================
    # RESUMEN REGIONAL
    # ======================================

    st.markdown("### Resumen regional")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Registros EcoAves", registros)
    c2.metric("Especies EcoAves", especies_detectadas)
    c3.metric("Aves probables eBird", especies_probables)
    c4.metric("Cobertura piloto", f"{cobertura}%")

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("Coincidencias", coincidencias)
    c6.metric("Brecha regional", brecha)
    c7.metric("Zonas activas", zonas_activas)
    c8.metric("Coherencia principal", coherencia_principal)

    st.info(
        f"""
        EcoAves contrasta actualmente **{especies_detectadas} especies** del prototipo
        contra **{especies_probables} especies probables** registradas recientemente en eBird.
        La cobertura piloto es de **{cobertura}%**, con una brecha regional estimada de
        **{brecha} especies** por incorporar en futuras fases.
        """
    )

    # ======================================
    # INTERPRETACIÓN PRINCIPAL
    # ======================================

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            f"""
            <div class="executive-card">
                <h3>Lectura ecológica preliminar</h3>
                <p>
                    La especie con mayor presencia en el conjunto piloto es
                    <b>{especie_dominante}</b>. La zona con mayor actividad registrada es
                    <b>{zona_prioritaria}</b>. Esta información ayuda a priorizar zonas de
                    monitoreo, validar registros y orientar la ampliación del sistema.
                </p>
                <p>
                    La coherencia ecológica más frecuente es <b>{coherencia_principal}</b>,
                    lo que permite interpretar si las detecciones coinciden con condiciones
                    esperadas de hábitat, altitud y distribución.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="status-card">
                <h3>Estado regional</h3>
                <div class="status-line">
                    <span>Referencia eBird</span>
                    <b>{especies_probables} especies</b>
                </div>
                <div class="status-line">
                    <span>Catálogo EcoAves</span>
                    <b>{especies_detectadas} especies</b>
                </div>
                <div class="status-line">
                    <span>Coincidencia regional</span>
                    <b>{coincidencias} especies</b>
                </div>
                <div class="status-line">
                    <span>Brecha por ampliar</span>
                    <b>{brecha} especies</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ======================================
    # COBERTURA PILOTO
    # ======================================

    st.markdown("### Cobertura piloto regional")

    if not regional_coverage:
        st.warning("No hay información regional disponible.")
    else:
        progress_value = cobertura / 100
        progress_value = min(max(progress_value, 0), 1)

        st.progress(progress_value)

        st.warning(
            f"""
            **Brecha regional detectada:**  
            Existen **{brecha} especies observadas en eBird** que aún no están cubiertas
            por el prototipo EcoAves.

            Esta brecha no representa un fallo del sistema, sino una guía concreta para
            ampliar el dataset acústico-visual y priorizar nuevas especies regionales.
            """
        )

    _render_priority_species(priority_species_df)

    # ======================================
    # AVES PROBABLES EBIRD
    # ======================================

    with st.expander("Explorar aves probables desde eBird", expanded=False):
        render_probable_species()

    # ======================================
    # MAPAS DE CALOR
    # ======================================

    with st.expander("Ver mapas de calor ecológicos", expanded=True):
        st.caption(
            "Los mapas permiten visualizar concentración de registros, intensidad acústico-visual "
            "y coherencia ecológica de las detecciones."
        )
        render_heatmap(heatmap_df)

    # ======================================
    # DIAGNÓSTICO ECOLÓGICO
    # ======================================

    with st.expander("Ver diagnóstico ecológico detallado", expanded=False):
        render_ecological(fusion_df)