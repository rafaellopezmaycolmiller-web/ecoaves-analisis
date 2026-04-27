import streamlit as st


def render_model_info():
    st.title("Cómo funciona la IA")
    st.caption("Explicación del flujo inteligente del sistema.")

    st.markdown(
        """
        <div class="section-card">
            <h3>Arquitectura propuesta</h3>
            <p>
                El sistema integra tres componentes principales: análisis acústico,
                análisis visual y fusión multimodal.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="section-card">
                <h3>Modelo acústico</h3>
                <p>
                    Convierte grabaciones de audio en espectrogramas para identificar patrones
                    de vocalización de aves.
                </p>
                <p><b>Entrada:</b> audio</p>
                <p><b>Salida:</b> especie probable + confianza</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="section-card">
                <h3>Modelo visual</h3>
                <p>
                    Analiza imágenes mediante visión por computador para reconocer características
                    morfológicas de especies.
                </p>
                <p><b>Entrada:</b> imagen</p>
                <p><b>Salida:</b> especie probable + confianza</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="section-card">
                <h3>Fusión multimodal</h3>
                <p>
                    Combina evidencia acústica y visual para obtener una predicción final más robusta.
                </p>
                <p><b>Salida:</b> confianza multimodal</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("## Flujo del sistema")
    st.info(
        "Audio + Imagen → Modelos IA → Fusión multimodal → Coordenadas → Mapas de calor → Interpretación ecológica"
    )

    st.markdown("## Estado actual del prototipo")
    st.warning(
        "Actualmente el sistema trabaja con salidas estructuradas y datos de prueba. "
        "La siguiente fase consiste en reemplazar estas salidas por modelos entrenados con datasets reales."
    )