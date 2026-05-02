import os
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv


load_dotenv()

EBIRD_API_KEY = os.getenv("EBIRD_API_KEY")
BASE_URL = "https://api.ebird.org/v2"


def get_recent_observations_by_geo(
    lat: float,
    lng: float,
    distance_km: int = 25,
    days_back: int = 14,
    max_results: int = 100,
) -> List[Dict[str, Any]]:
    """
    Consulta observaciones recientes de aves cerca de una coordenada.
    """

    if not EBIRD_API_KEY:
        raise ValueError(
            "Falta EBIRD_API_KEY. Verifica que el archivo .env esté en la raíz del proyecto."
        )

    url = f"{BASE_URL}/data/obs/geo/recent"

    headers = {
        "x-ebirdapitoken": EBIRD_API_KEY
    }

    params = {
        "lat": lat,
        "lng": lng,
        "dist": distance_km,
        "back": days_back,
        "maxResults": max_results,
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20,
    )

    response.raise_for_status()
    return response.json()


def normalize_ebird_observations(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convierte la respuesta de eBird en una estructura amigable para EcoAves.
    """

    normalized = []

    for item in records:
        normalized.append(
            {
                "nombre_comun": item.get("comName"),
                "nombre_cientifico": item.get("sciName"),
                "codigo_ebird": item.get("speciesCode"),
                "fecha_observacion": item.get("obsDt"),
                "lat": item.get("lat"),
                "lon": item.get("lng"),
                "ubicacion": item.get("locName"),
                "cantidad": item.get("howMany"),
            }
        )

    return normalized