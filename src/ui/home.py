import base64
from pathlib import Path

import pandas as pd
import streamlit as st


HERO_IMAGE_PATH = "imagenes/portada1.jpg"


def image_to_base64(path: str) -> str:
    image_path = Path(path)

    if not image_path.exists():
        return ""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def go_to(page_name: str):
    st.session_state["go_to_page"] = page_name
    st.rerun()


def get_top_values(fusion_df: pd.DataFrame):
    especie_top = "Sin datos"
    zona_top = "Sin datos"
    modalidad_top = "Sin datos"

    if not fusion_df.empty:
        if "nombre_comun" in fusion_df.columns and not fusion_df["nombre_comun"].dropna().empty:
            especie_top = fusion_df["nombre_comun"].value_counts().idxmax()

        if "nombre_zona" in fusion_df.columns and not fusion_df["nombre_zona"].dropna().empty:
            zona_top = fusion_df["nombre_zona"].value_counts().idxmax()

        if "source_mode" in fusion_df.columns and not fusion_df["source_mode"].dropna().empty:
            modalidad_top = fusion_df["source_mode"].value_counts().idxmax()

    return especie_top, zona_top, modalidad_top


def render_home(metrics, fusion_df=None, regional_coverage=None):
    if fusion_df is None:
        fusion_df = pd.DataFrame()

    hero_image = image_to_base64(HERO_IMAGE_PATH)

    if hero_image:
        background_style = f"""
            background-image:
                linear-gradient(90deg, rgba(2, 8, 23, 0.92), rgba(2, 20, 26, 0.82), rgba(2, 8, 23, 0.30)),
                url("data:image/jpg;base64,{hero_image}");
            background-size: cover;
            background-position: center;
        """
    else:
        background_style = """
            background: linear-gradient(135deg, #052e2b 0%, #0f172a 60%, #111827 100%);
        """

    cobertura = 0
    especies_probables = 0
    coincidencias = 0
    brecha = 0

    if regional_coverage:
        cobertura = regional_coverage.get("cobertura_porcentaje", 0)
        especies_probables = regional_coverage.get("especies_probables", 0)
        coincidencias = regional_coverage.get("especies_coincidentes", 0)
        brecha = regional_coverage.get("brecha_regional", 0)

    especie_top, zona_top, modalidad_top = get_top_values(fusion_df)

    st.markdown(
        f"""
        <div class="clean-hero" style='{background_style}'>
            <div class="hero-badge">● Plataforma piloto activa</div>
            <h1>EcoAves Perú</h1>
            <h2>Monitoreo acústico-visual de aves en San Martín</h2>
            <p>
                Sistema web para integrar detecciones por audio e imagen, registros regionales de eBird,
                mapas de calor y validación experta en el monitoreo ecológico de aves.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Estado general del prototipo")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""
            <div class="clean-kpi">
                <span>Registros procesados</span>
                <h3>{metrics.get("total_registros", 0)}</h3>
                <p>detecciones piloto</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="clean-kpi">
                <span>Especies EcoAves</span>
                <h3>{metrics.get("especies_detectadas", 0)}</h3>
                <p>catálogo inicial</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="clean-kpi">
                <span>Aves probables eBird</span>
                <h3>{especies_probables}</h3>
                <p>referencia regional</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="clean-kpi highlight">
                <span>Cobertura piloto</span>
                <h3>{cobertura}%</h3>
                <p>{coincidencias} coincidencias regionales</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Módulos principales")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-icon">🎙️</div>
                <h3>Monitoreo</h3>
                <p>
                    Carga evidencia, revisa detecciones acústicas y visuales,
                    y consulta la confianza del modelo piloto.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Abrir Monitoreo", use_container_width=True):
            go_to("Monitoreo")

    with m2:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-icon">🌿</div>
                <h3>Inteligencia ecológica</h3>
                <p>
                    Explora aves probables desde eBird, mapas de calor,
                    cobertura regional y brechas de ampliación.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Abrir Inteligencia ecológica", use_container_width=True):
            go_to("Inteligencia ecológica")

    with m3:
        st.markdown(
            """
            <div class="module-card">
                <div class="module-icon">✅</div>
                <h3>Validación experta</h3>
                <p>
                    Registra observaciones de especialistas y guarda la revisión
                    en archivos CSV para futuras mejoras del sistema.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Abrir Validación", use_container_width=True):
            go_to("Validación")

    st.markdown("### Lectura ejecutiva")

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown(
            f"""
            <div class="executive-card">
                <h3>Resumen del monitoreo actual</h3>
                <p>
                    La especie con mayor presencia en el conjunto piloto es
                    <b>{especie_top}</b>. La zona con mayor actividad registrada es
                    <b>{zona_top}</b> y la modalidad predominante de detección es
                    <b>{modalidad_top}</b>.
                </p>
                <p>
                    EcoAves contrasta actualmente <b>{metrics.get("especies_detectadas", 0)}</b>
                    especies del prototipo frente a <b>{especies_probables}</b> especies probables
                    obtenidas desde eBird para la región.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="status-card">
                <h3>Alcance piloto</h3>
                <div class="status-line">
                    <span>eBird conectado</span>
                    <b>Activo</b>
                </div>
                <div class="status-line">
                    <span>Brecha regional</span>
                    <b>{brecha} especies</b>
                </div>
                <div class="status-line">
                    <span>Validación experta</span>
                    <b>CSV local</b>
                </div>
                <div class="status-line">
                    <span>Estado del sistema</span>
                    <b>Piloto funcional</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )