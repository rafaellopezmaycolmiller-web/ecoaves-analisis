import pandas as pd


def build_ecological_alerts(df: pd.DataFrame) -> list:
    alerts = []

    if df.empty:
        return alerts

    zone_counts = df["nombre_zona"].value_counts()
    top_zone = zone_counts.index[0]
    top_zone_count = zone_counts.iloc[0]

    if top_zone_count >= 3:
        alerts.append({
            "type": "critical",
            "title": "Zona de alta actividad detectada",
            "message": f"La zona {top_zone} concentra {top_zone_count} detecciones. Puede considerarse prioritaria para monitoreo."
        })

    low_conf = df[df["fusion_confidence"] < 0.55]
    if len(low_conf) > 0:
        alerts.append({
            "type": "warning",
            "title": "Detecciones de baja confianza",
            "message": f"Existen {len(low_conf)} registros con confianza menor a 55%. Requieren revisión experta."
        })

    low_ecology = df[df["coherencia_ecologica"].isin(["media", "baja"])]
    if len(low_ecology) > 0:
        alerts.append({
            "type": "warning",
            "title": "Posibles inconsistencias ecológicas",
            "message": f"Se encontraron {len(low_ecology)} registros con coherencia ecológica media o baja."
        })

    fusion_count = (df["source_mode"] == "fusionado").sum()
    if fusion_count > 0:
        alerts.append({
            "type": "success",
            "title": "Fusión multimodal activa",
            "message": f"{fusion_count} registros combinan evidencia acústica y visual, aumentando la robustez del análisis."
        })

    return alerts