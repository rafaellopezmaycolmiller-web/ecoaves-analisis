import streamlit as st
import pandas as pd

def render_database(df: pd.DataFrame):
    st.subheader("Registros ecológicos")
    st.dataframe(df, use_container_width=True)