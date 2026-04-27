import streamlit as st
from src.services.alert_service import build_ecological_alerts


def render_home(metrics, df):
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">EcoAves Perú</div>
            <div class="hero-subtitle">
                Plataforma de monitoreo inteligente para aves en ecosistemas tropicales.
                Integra audio, visión computacional, fusión multimodal y mapas de calor ecológicos.
            </div>
            <br>
            <span class="tag">IA ligera</span>
            <span class="tag">Audio + Imagen</span>
            <span class="tag">Mapas ecológicos</span>
            <span class="tag">Validación experta</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Registros procesados", metrics["total_registros"])
    col2.metric("Especies monitoreadas", metrics["especies_detectadas"])
    col3.metric("Confianza multimodal", f'{metrics["confianza_promedio"]}%')
    col4.metric("Zonas activas", metrics["zonas_activas"])

    st.markdown("## Alertas ecológicas")

    alerts = build_ecological_alerts(df)

    for alert in alerts:
        if alert["type"] == "critical":
            st.error(f"🚨 **{alert['title']}**\n\n{alert['message']}")
        elif alert["type"] == "warning":
            st.warning(f"⚠️ **{alert['title']}**\n\n{alert['message']}")
        else:
            st.success(f"✅ **{alert['title']}**\n\n{alert['message']}")

    st.markdown(
        """
        <div class="section-card">
            <h3>¿Qué problema resuelve?</h3>
            <p>
                El monitoreo de aves suele depender de observación manual, personal especializado y visitas
                de campo. EcoAves Perú propone una herramienta de apoyo que permite organizar, analizar e
                interpretar registros acústicos, visuales y espaciales para identificar patrones de actividad.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>Flujo del sistema</h3>
            <p style="font-size:18px;">
                🔊 Audio → 🖼️ Imagen → 🤖 Fusión IA → 📍 Georreferenciación → 🔥 Mapas de calor → 🌿 Interpretación ecológica
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(
            """
            <div class="section-card">
                <h3>Detección</h3>
                <p>Identificación acústica y visual de especies mediante salidas simuladas de modelos IA.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            """
            <div class="section-card">
                <h3>Representación</h3>
                <p>Generación de mapas de densidad, intensidad y coherencia ecológica.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_c:
        st.markdown(
            """
            <div class="section-card">
                <h3>Decisión</h3>
                <p>Apoyo para identificar zonas prioritarias y validar resultados con especialistas.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )