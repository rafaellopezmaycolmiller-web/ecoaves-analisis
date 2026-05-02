import os
import pandas as pd


VALIDATION_PATH = "data/processed/validaciones_expertas.csv"


def load_validations(path: str = VALIDATION_PATH) -> pd.DataFrame:
    if not os.path.exists(path):
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

    return pd.read_csv(path)


def build_validation_metrics(validations_df: pd.DataFrame) -> dict:
    if validations_df.empty or "decision" not in validations_df.columns:
        return {
            "total": 0,
            "aprobadas": 0,
            "observadas": 0,
            "descartadas": 0,
        }

    decision_counts = validations_df["decision"].value_counts()

    return {
        "total": len(validations_df),
        "aprobadas": int(decision_counts.get("Aprobar", 0)),
        "observadas": int(decision_counts.get("Observar", 0)),
        "descartadas": int(decision_counts.get("Descartar", 0)),
    }