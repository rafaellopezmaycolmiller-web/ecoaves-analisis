import streamlit as st
import pandas as pd


def render_ecological(df: pd.DataFrame):
    st.subheader("Resultados ecológicos")

    # Especies más frecuentes
    especies = (
        df.groupby("nombre_comun")
        .size()
        .sort_values(ascending=False)
        .head(5)
    )

    st.markdown("### Especies más detectadas")
    st.bar_chart(especies)

    # Actividad por zona
    zonas = (
        df.groupby("nombre_zona")
        .size()
        .sort_values(ascending=False)
    )

    st.markdown("### Actividad por zona")
    st.bar_chart(zonas)

    # Coherencia ecológica
    coherencia = df["coherencia_ecologica"].value_counts()

    st.markdown("### Coherencia ecológica del modelo")
    st.bar_chart(coherencia)

    # Interpretación automática
    st.markdown("### Interpretación del sistema")

    especie_top = especies.index[0] if len(especies) > 0 else "N/A"
    zona_top = zonas.index[0] if len(zonas) > 0 else "N/A"

    st.info(f"""
    - La especie con mayor actividad detectada es: **{especie_top}**
    - La zona con mayor concentración es: **{zona_top}**
    - El modelo presenta un nivel de coherencia ecológica predominante: **{coherencia.idxmax()}**
    
    Esto sugiere patrones de distribución consistentes con el comportamiento esperado de las especies en el ecosistema analizado.
    """)