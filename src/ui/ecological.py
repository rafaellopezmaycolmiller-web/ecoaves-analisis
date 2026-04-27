import streamlit as st
import pandas as pd


def render_ecological(df: pd.DataFrame):
    st.title("Diagnóstico ecológico")
    st.caption("Interpretación automática de patrones de actividad, distribución y coherencia ecológica.")

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    especies = df["nombre_comun"].value_counts()
    zonas = df["nombre_zona"].value_counts()
    coherencia = df["coherencia_ecologica"].value_counts()
    modalidades = df["source_mode"].value_counts()

    especie_top = especies.index[0]
    zona_top = zonas.index[0]
    coherencia_top = coherencia.index[0]
    modalidad_top = modalidades.index[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Especie dominante", especie_top)
    col2.metric("Zona crítica", zona_top)
    col3.metric("Coherencia principal", coherencia_top)
    col4.metric("Modalidad dominante", modalidad_top)

    st.markdown(
        f"""
        <div class="section-card">
            <h3>Diagnóstico preliminar</h3>
            <p>
                La mayor concentración de detecciones corresponde a <b>{especie_top}</b>,
                con mayor actividad registrada en <b>{zona_top}</b>. La modalidad predominante
                fue <b>{modalidad_top}</b>, y el nivel de coherencia ecológica más frecuente fue
                <b>{coherencia_top}</b>.
            </p>
            <p>
                Este resultado sugiere que el sistema permite identificar patrones espaciales y
                ecológicos útiles para priorizar zonas de monitoreo y revisión experta.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### Especies más detectadas")
        st.bar_chart(especies)

    with col_b:
        st.markdown("### Actividad por zona")
        st.bar_chart(zonas)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("### Coherencia ecológica")
        st.bar_chart(coherencia)

    with col_d:
        st.markdown("### Modalidad de detección")
        st.bar_chart(modalidades)

    st.markdown("### Registros interpretados")
    st.dataframe(
        df[
            [
                "fecha",
                "hora",
                "nombre_comun",
                "nombre_zona",
                "ecosistema",
                "source_mode",
                "fusion_confidence",
                "coherencia_ecologica",
            ]
        ],
        use_container_width=True,
    )