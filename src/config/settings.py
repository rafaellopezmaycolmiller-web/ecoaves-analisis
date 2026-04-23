from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXPORTS_DIR = DATA_DIR / "exports"
ASSETS_DIR = BASE_DIR / "assets" / "imagenes"

APP_TITLE = "EcoAves Perú"
APP_SUBTITLE = (
    "Sistema de inteligencia artificial ligera para el monitoreo "
    "acústico-visual de aves y la generación de mapas de calor ecológicos."
)

USE_MOCK_DATA = True

FILES = {
    "audio_events": RAW_DATA_DIR / "mock_audio_events.csv",
    "visual_events": RAW_DATA_DIR / "mock_visual_events.csv",
    "species_catalog": RAW_DATA_DIR / "mock_species_catalog.csv",
    "zones": RAW_DATA_DIR / "mock_zones.csv",
    "fusion_results": PROCESSED_DATA_DIR / "fusion_results.csv",
}