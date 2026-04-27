import streamlit as st


def render_impact():
    st.title("Impacto del sistema")
    st.caption("Comparación entre monitoreo tradicional y monitoreo asistido por IA.")

    st.markdown("## Comparación operativa")

    data = {
        "Criterio": [
            "Cobertura temporal",
            "Dependencia de especialistas",
            "Procesamiento de datos",
            "Visualización espacial",
            "Escalabilidad",
            "Interpretación ecológica",
        ],
        "Método tradicional": [
            "Limitada a salidas de campo",
            "Alta",
            "Manual",
            "Baja o posterior",
            "Limitada",
            "Dependiente del análisis manual",
        ],
        "EcoAves Perú": [
            "Continua o por registros acumulados",
            "Reduce carga operativa",
            "Automatizado",
            "Mapas de calor interactivos",
            "Alta mediante datasets y sensores",
            "Incluye coherencia ecológica",
        ],
    }

    st.table(data)

    st.markdown(
        """
        <div class="section-card">
            <h3>Valor agregado</h3>
            <p>
                EcoAves Perú no reemplaza al especialista, sino que organiza y prioriza información
                para facilitar la revisión experta y la toma de decisiones en conservación.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## Aplicaciones potenciales")

    col1, col2, col3 = st.columns(3)

    col1.info("🌿 Monitoreo en áreas protegidas")
    col2.info("🔬 Apoyo a investigadores")
    col3.info("📍 Identificación de zonas prioritarias")

    col4, col5, col6 = st.columns(3)

    col4.info("📊 Reportes ambientales")
    col5.info("🎧 Análisis ecoacústico")
    col6.info("🛰️ Integración con sensores remotos")