import streamlit as st
import pandas as pd


def render_validation(df: pd.DataFrame):
    st.title("Validación experta")
    st.caption("Espacio para registrar observaciones del especialista en aves durante la revisión del prototipo.")

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    st.markdown(
        """
        <div class="section-card">
            <h3>Objetivo de esta sección</h3>
            <p>
                Permitir que un experto revise registros seleccionados, valide si la especie detectada es coherente,
                evalúe el hábitat y deje observaciones para mejorar el sistema.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sample_df = df[
        [
            "nombre_comun",
            "nombre_cientifico",
            "nombre_zona",
            "ecosistema",
            "altitud",
            "source_mode",
            "fusion_confidence",
            "coherencia_ecologica",
        ]
    ].head(15).copy()

    sample_df["¿Especie correcta?"] = ""
    sample_df["¿Hábitat coherente?"] = ""
    sample_df["Comentario del experto"] = ""

    edited_df = st.data_editor(
        sample_df,
        use_container_width=True,
        num_rows="dynamic",
    )

    csv = edited_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar validación experta",
        data=csv,
        file_name="validacion_experta.csv",
        mime="text/csv",
    )