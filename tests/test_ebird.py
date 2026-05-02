import os
import pandas as pd

from src.services.apis.ebird_api import (
    get_recent_observations_by_geo,
    normalize_ebird_observations,
)


TARAPOTO_LAT = -6.4869
TARAPOTO_LON = -76.3597


def main():
    print("Consultando observaciones recientes cerca de Tarapoto...")

    records = get_recent_observations_by_geo(
        lat=TARAPOTO_LAT,
        lng=TARAPOTO_LON,
        distance_km=25,
        days_back=30,
        max_results=100,
    )

    normalized = normalize_ebird_observations(records)
    df = pd.DataFrame(normalized)

    if df.empty:
        print("No se encontraron registros.")
        return

    print(df.head())
    print(f"Total de registros obtenidos: {len(df)}")
    print(f"Total de especies únicas: {df['nombre_cientifico'].nunique()}")

    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/ebird_tarapoto_recent.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo generado correctamente: {output_path}")


if __name__ == "__main__":
    main()