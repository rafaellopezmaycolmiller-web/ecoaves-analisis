import pandas as pd
from src.config.settings import FILES

def load_audio_events() -> pd.DataFrame:
    return pd.read_csv(FILES["audio_events"])

def load_visual_events() -> pd.DataFrame:
    return pd.read_csv(FILES["visual_events"])

def load_species_catalog() -> pd.DataFrame:
    return pd.read_csv(FILES["species_catalog"])

def load_zones() -> pd.DataFrame:
    return pd.read_csv(FILES["zones"])

def load_all():
    return {
        "audio": load_audio_events(),
        "visual": load_visual_events(),
        "species": load_species_catalog(),
        "zones": load_zones(),
    }