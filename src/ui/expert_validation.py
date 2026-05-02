import os
from datetime import datetime

import pandas as pd
import streamlit as st


VALIDATION_PATH = "data/processed/validaciones_expertas.csv"


def load_validations() -> pd.DataFrame:
    if not os.path.exists(VALIDATION_PATH):
        return pd.DataFrame(
            columns=[
                "fecha_validacion",
                "especie",
                "nombre_cientifico",
                "zona",
                "decision",
                "categoria",
                "comentario",
                "confianza",
                "coherencia_ecologica",
                "coherencia_regional",
            ]
        )

    return pd.read_csv(VALIDATION_PATH)


def save_validation(new_row: dict):
    os.makedirs("data/processed", exist_ok=True)

    existing_df = load_validations()
    new_df = pd.DataFrame([new_row])

    final_df = pd.concat([existing_df, new_df], ignore_index=True)
    final_df.to_csv(VALIDATION_PATH, index=False, encoding="utf-8")


def render_expert_validation(fusion_df: pd.DataFrame):
    st.title("Validación experta")
    st.caption(
        "Revisión de detecciones por especialistas para mejorar la confiabilidad ecológica del sistema."
    )

    if fusion_df.empty:
        st.warning("No hay registros disponibles para validar.")
        return

    st.markdown(
        """
        <div class="section-card">
            <h3>Objetivo de la validación</h3>
            <p>
                Esta sección permite registrar la revisión de un especialista sobre las detecciones del sistema.
                Las observaciones se almacenan en un archivo CSV para ser usadas como evidencia de validación
                y mejora del prototipo.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Registros pendientes de revisión")

    columnas = [
        "fecha",
        "hora",
        "nombre_comun",
        "nombre_cientifico",
        "nombre_zona",
        "source_mode",
        "confidence_audio",
        "confidence_visual",
        "fusion_confidence",
        "coherencia_ecologica",
        "coherencia_regional",
    ]

    columnas_disponibles = [col for col in columnas if col in fusion_df.columns]

    st.dataframe(
        fusion_df[columnas_disponibles],
        use_container_width=True,
    )

    st.markdown("### Ficha de validación")

    especies = (
        sorted(fusion_df["nombre_comun"].dropna().unique().tolist())
        if "nombre_comun" in fusion_df.columns
        else []
    )

    especie = st.selectbox(
        "Especie revisada",
        especies,
        index=0 if especies else None,
    )

    registro_filtrado = fusion_df[fusion_df["nombre_comun"] == especie].copy()

    if registro_filtrado.empty:
        st.warning("No hay registros para la especie seleccionada.")
        return

    registro = registro_filtrado.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Confianza fusionada",
        f"{registro.get('fusion_confidence', 0) * 100:.1f}%",
    )

    col2.metric(
        "Coherencia ecológica",
        registro.get("coherencia_ecologica", "No disponible"),
    )

    col3.metric(
        "Coherencia regional",
        registro.get("coherencia_regional", "No disponible"),
    )

    st.markdown("### Datos del registro seleccionado")

    st.info(
        f"""
        **Especie:** {registro.get("nombre_comun", "No disponible")}  
        **Nombre científico:** {registro.get("nombre_cientifico", "No disponible")}  
        **Zona:** {registro.get("nombre_zona", "No disponible")}  
        **Modalidad:** {registro.get("source_mode", "No disponible")}
        """
    )

    decision = st.radio(
        "Decisión del experto",
        ["Aprobar", "Observar", "Descartar"],
        horizontal=True,
    )

    categoria = st.selectbox(
        "Categoría de validación",
        [
            "Identificación correcta",
            "Posible confusión de especie",
            "Hábitat no coincidente",
            "Baja confianza del modelo",
            "No registrada recientemente en eBird",
            "Requiere nueva evidencia",
        ],
    )

    comentario = st.text_area(
        "Comentario ecológico",
        placeholder="Escribe una observación sobre la especie, zona, hábitat, confianza o registro regional...",
    )

    if st.button("Guardar validación"):
        new_row = {
            "fecha_validacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "especie": registro.get("nombre_comun", ""),
            "nombre_cientifico": registro.get("nombre_cientifico", ""),
            "zona": registro.get("nombre_zona", ""),
            "decision": decision,
            "categoria": categoria,
            "comentario": comentario,
            "confianza": registro.get("fusion_confidence", ""),
            "coherencia_ecologica": registro.get("coherencia_ecologica", ""),
            "coherencia_regional": registro.get("coherencia_regional", ""),
        }

        save_validation(new_row)

        st.success("Validación guardada correctamente en CSV.")

    st.markdown("### Historial de validaciones")

    validations_df = load_validations()

    if validations_df.empty:
        st.info("Aún no hay validaciones registradas.")
    else:
        st.dataframe(validations_df, use_container_width=True)

        csv = validations_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Descargar validaciones expertas",
            data=csv,
            file_name="validaciones_expertas.csv",
            mime="text/csv",
        )