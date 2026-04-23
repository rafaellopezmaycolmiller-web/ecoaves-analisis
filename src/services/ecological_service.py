import pandas as pd

def add_ecological_consistency(fusion_df: pd.DataFrame, zones_df: pd.DataFrame, species_df: pd.DataFrame) -> pd.DataFrame:
    df = fusion_df.merge(zones_df, on="zone_id", how="left")
    df = df.merge(species_df, on="species_id", how="left")

    def evaluate(row):
        if row["altitud_min"] <= row["altitud"] <= row["altitud_max"]:
            return "alta"
        if abs(row["altitud"] - row["altitud_min"]) <= 200 or abs(row["altitud"] - row["altitud_max"]) <= 200:
            return "media"
        return "baja"

    df["coherencia_ecologica"] = df.apply(evaluate, axis=1)
    return df