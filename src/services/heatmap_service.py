import pandas as pd

def build_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ["zone_id", "lat", "lon"]

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Falta la columna requerida: {col}")

    if "nombre_zona" not in df.columns:
        if "nombre_zona_x" in df.columns:
            df = df.rename(columns={"nombre_zona_x": "nombre_zona"})
        elif "nombre_zona_y" in df.columns:
            df = df.rename(columns={"nombre_zona_y": "nombre_zona"})
        else:
            raise ValueError(
                f"No se encontró la columna 'nombre_zona'. Columnas disponibles: {df.columns.tolist()}"
            )

    grouped = (
        df.groupby(["zone_id", "nombre_zona", "lat", "lon"], as_index=False)
        .agg(
            detecciones=("species_id", "count"),
            intensidad=("fusion_confidence", "mean")
        )
    )

    return grouped