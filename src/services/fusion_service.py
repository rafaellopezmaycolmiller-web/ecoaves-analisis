import pandas as pd


def build_fusion_results(audio_df: pd.DataFrame, visual_df: pd.DataFrame) -> pd.DataFrame:
    audio_df = audio_df.copy()
    visual_df = visual_df.copy()

    audio_df["key"] = audio_df["zone_id"] + "_" + audio_df["species_id"] + "_" + audio_df["fecha"]
    visual_df["key"] = visual_df["zone_id"] + "_" + visual_df["species_id"] + "_" + visual_df["fecha"]

    merged = pd.merge(
        audio_df,
        visual_df,
        on="key",
        how="outer",
        suffixes=("_audio", "_visual")
    )

    merged["zone_id"] = merged["zone_id_audio"].fillna(merged["zone_id_visual"])
    merged["species_id"] = merged["species_id_audio"].fillna(merged["species_id_visual"])
    merged["fecha"] = merged["fecha_audio"].fillna(merged["fecha_visual"])
    merged["hora"] = merged["hora_audio"].fillna(merged["hora_visual"])

    merged["confidence_audio"] = merged["confidence_audio"].fillna(0)
    merged["confidence_visual"] = merged["confidence_visual"].fillna(0)

    def smart_fusion(row):
        audio = row["confidence_audio"]
        visual = row["confidence_visual"]

        if audio > 0.8 and visual > 0.8:
            return max(audio, visual)

        if audio > visual:
            return audio * 0.6 + visual * 0.4

        return visual * 0.6 + audio * 0.4

    merged["fusion_confidence"] = merged.apply(smart_fusion, axis=1)

    def get_source(row):
        if row["confidence_audio"] > 0 and row["confidence_visual"] > 0:
            return "fusionado"
        if row["confidence_audio"] > 0:
            return "audio"
        return "visual"

    merged["source_mode"] = merged.apply(get_source, axis=1)

    return merged[
        [
            "zone_id",
            "species_id",
            "fecha",
            "hora",
            "confidence_audio",
            "confidence_visual",
            "fusion_confidence",
            "source_mode",
        ]
    ]