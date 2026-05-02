import os
import pandas as pd


EBIRD_CSV_PATH = "data/raw/ebird_tarapoto_recent.csv"


def load_ebird_species(path: str = EBIRD_CSV_PATH) -> pd.DataFrame:
    """
    Carga el CSV generado desde eBird.
    Si no existe o está vacío, devuelve un DataFrame vacío.

    También normaliza los nombres común y científico para facilitar comparaciones.
    """

    if not os.path.exists(path):
        return pd.DataFrame()

    df = pd.read_csv(path)

    if df.empty:
        return pd.DataFrame()

    if "nombre_cientifico" in df.columns:
        df["nombre_cientifico_norm"] = (
            df["nombre_cientifico"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    if "nombre_comun" in df.columns:
        df["nombre_comun_norm"] = (
            df["nombre_comun"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    return df


def add_regional_coherence(
    fusion_df: pd.DataFrame,
    ebird_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Agrega una columna llamada 'coherencia_regional'.

    Esta columna indica si la especie detectada por EcoAves aparece en los
    registros recientes de eBird para la zona de análisis.
    """

    df = fusion_df.copy()

    if ebird_df is None:
        ebird_df = load_ebird_species()

    if df.empty:
        df["coherencia_regional"] = "Sin datos"
        return df

    if "nombre_cientifico" not in df.columns:
        df["coherencia_regional"] = "Sin nombre científico"
        return df

    if ebird_df.empty:
        df["coherencia_regional"] = "Sin referencia eBird"
        return df

    if "nombre_cientifico_norm" not in ebird_df.columns:
        if "nombre_cientifico" not in ebird_df.columns:
            df["coherencia_regional"] = "Sin referencia eBird"
            return df

        ebird_df = ebird_df.copy()
        ebird_df["nombre_cientifico_norm"] = (
            ebird_df["nombre_cientifico"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    especies_ebird = set(
        ebird_df["nombre_cientifico_norm"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .tolist()
    )

    df["nombre_cientifico_norm"] = (
        df["nombre_cientifico"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    def evaluar_coherencia(nombre_cientifico: str) -> str:
        if not nombre_cientifico or nombre_cientifico == "nan":
            return "Sin información"

        if nombre_cientifico in especies_ebird:
            return "Presente en eBird"

        return "No registrado recientemente"

    df["coherencia_regional"] = df["nombre_cientifico_norm"].apply(evaluar_coherencia)

    return df.drop(columns=["nombre_cientifico_norm"], errors="ignore")


def calculate_regional_coverage(
    fusion_df: pd.DataFrame,
    ebird_df: pd.DataFrame | None = None,
) -> dict:
    """
    Calcula la cobertura regional piloto de EcoAves.

    Compara las especies detectadas por EcoAves contra las especies observadas
    recientemente en eBird cerca de la zona de análisis.
    """

    if ebird_df is None:
        ebird_df = load_ebird_species()

    empty_result = {
        "especies_probables": 0,
        "especies_detectadas": 0,
        "especies_coincidentes": 0,
        "cobertura_porcentaje": 0.0,
        "brecha_regional": 0,
    }

    if fusion_df.empty or ebird_df.empty:
        return empty_result

    if "nombre_cientifico" not in fusion_df.columns:
        return empty_result

    if "nombre_cientifico" not in ebird_df.columns:
        return empty_result

    especies_detectadas = set(
        fusion_df["nombre_cientifico"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .tolist()
    )

    especies_probables = set(
        ebird_df["nombre_cientifico"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.lower()
        .tolist()
    )

    especies_coincidentes = especies_detectadas.intersection(especies_probables)

    total_probables = len(especies_probables)
    total_detectadas = len(especies_detectadas)
    total_coincidentes = len(especies_coincidentes)

    cobertura = (
        round((total_coincidentes / total_probables) * 100, 2)
        if total_probables > 0
        else 0.0
    )

    brecha_regional = max(total_probables - total_coincidentes, 0)

    return {
        "especies_probables": total_probables,
        "especies_detectadas": total_detectadas,
        "especies_coincidentes": total_coincidentes,
        "cobertura_porcentaje": cobertura,
        "brecha_regional": brecha_regional,
    }


def get_priority_species_to_add(
    fusion_df: pd.DataFrame,
    ebird_df: pd.DataFrame | None = None,
    limit: int = 10,
) -> pd.DataFrame:
    """
    Devuelve especies observadas en eBird que todavía no están cubiertas
    por el prototipo EcoAves.

    Estas especies sirven como candidatas prioritarias para ampliar el dataset,
    entrenar el modelo o enriquecer el catálogo regional.
    """

    if ebird_df is None:
        ebird_df = load_ebird_species()

    if ebird_df.empty:
        return pd.DataFrame()

    if "nombre_cientifico" not in ebird_df.columns:
        return pd.DataFrame()

    if fusion_df.empty or "nombre_cientifico" not in fusion_df.columns:
        especies_detectadas = set()
    else:
        especies_detectadas = set(
            fusion_df["nombre_cientifico"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.lower()
            .tolist()
        )

    ebird_df = ebird_df.copy()

    ebird_df["nombre_cientifico_norm"] = (
        ebird_df["nombre_cientifico"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    pendientes = ebird_df[
        ~ebird_df["nombre_cientifico_norm"].isin(especies_detectadas)
    ].copy()

    pendientes = pendientes.drop_duplicates(subset=["nombre_cientifico"])

    columnas = [
        "nombre_comun",
        "nombre_cientifico",
        "codigo_ebird",
        "fecha_observacion",
        "ubicacion",
        "cantidad",
    ]

    columnas_disponibles = [col for col in columnas if col in pendientes.columns]

    if not columnas_disponibles:
        return pd.DataFrame()

    return pendientes[columnas_disponibles].head(limit)