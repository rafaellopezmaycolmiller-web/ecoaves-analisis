import pandas as pd

def build_dashboard_metrics(df: pd.DataFrame) -> dict:
    total_registros = len(df)
    especies_detectadas = df["species_id"].nunique()
    confianza_promedio = round(df["fusion_confidence"].mean() * 100, 1) if total_registros > 0 else 0
    zonas_activas = df["zone_id"].nunique()

    return {
        "total_registros": total_registros,
        "especies_detectadas": especies_detectadas,
        "confianza_promedio": confianza_promedio,
        "zonas_activas": zonas_activas,
    }