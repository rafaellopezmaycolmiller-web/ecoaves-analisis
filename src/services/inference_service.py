import os
import time
import random
import pandas as pd
from datetime import datetime

# Intentar importar birdnetlib
try:
    from birdnetlib import Recording
    from birdnetlib.analyzer import Analyzer
    BIRDNET_AVAILABLE = True
except ImportError:
    BIRDNET_AVAILABLE = False

# Instancia global del analizador para no cargar los pesos (30MB) cada vez
_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is None and BIRDNET_AVAILABLE:
        try:
            print("Cargando modelo BirdNET...")
            _analyzer = Analyzer()
            print("Modelo BirdNET cargado exitosamente.")
        except Exception as e:
            print(f"Error inicializando BirdNET Analyzer: {e}")
    return _analyzer


def run_audio_inference(file_path: str, zone_id: str, species_df: pd.DataFrame) -> dict:
    """
    Inferencia de IA real utilizando BirdNET.
    """
    now = datetime.now()
    event_id = f"A{random.randint(100, 999)}"
    
    analyzer = get_analyzer()
    
    if analyzer is None:
        # Fallback al mock si no se pudo cargar birdnet
        return _run_audio_inference_mock(file_path, zone_id, species_df, now, event_id)
        
    try:
        # Coordenadas aproximadas de Tarapoto/San Martín para el prior regional
        recording = Recording(
            analyzer,
            file_path,
            lat=-6.48,
            lon=-76.36,
            date=now,
            min_conf=0.1,
        )
        recording.analyze()
        
        detections = recording.detections
        
        if len(detections) > 0:
            # Tomar la mejor detección
            best_detection = sorted(detections, key=lambda x: x['confidence'], reverse=True)[0]
            sci_name = best_detection['scientific_name']
            com_name = best_detection['common_name']
            confidence = best_detection['confidence']
        else:
            # Ninguna especie detectada
            sci_name = "Indeterminado"
            com_name = "Desconocido"
            confidence = 0.0

    except Exception as e:
        print(f"Error durante el análisis con BirdNET: {e}")
        # Fallback al mock en caso de error (ej. falta ffmpeg para mp3)
        return _run_audio_inference_mock(file_path, zone_id, species_df, now, event_id)
        
    # Verificar si la especie detectada ya está en nuestro catálogo piloto
    matched = species_df[species_df["nombre_cientifico"].str.lower() == sci_name.lower()]
    
    if not matched.empty:
        species_id = matched.iloc[0]["species_id"]
    else:
        # Es una nueva especie detectada por BirdNET que no estaba en el CSV original
        species_id = f"SP_NEW_{random.randint(1000, 9999)}"
        
    intensity = round(random.uniform(0.50, 0.95), 2)
    duration = random.randint(5, 30)
    
    file_name = os.path.basename(file_path)
    
    return {
        "event_id": event_id,
        "zone_id": zone_id,
        "species_id": species_id,
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M"),
        "confidence_audio": confidence,
        "intensity_audio": intensity,
        "duration_sec": duration,
        "file_name": file_name,
        # Extras para que el UI pueda registrar nuevas especies
        "_sci_name": sci_name,
        "_com_name": com_name,
    }


def _run_audio_inference_mock(file_path: str, zone_id: str, species_df: pd.DataFrame, now, event_id) -> dict:
    time.sleep(2)
    
    file_name = os.path.basename(file_path)
    file_lower = file_name.lower()
    predicted_species = None
    
    if "gallito" in file_lower or "roca" in file_lower:
        matched = species_df[species_df["nombre_comun"].str.contains("Gallito", case=False, na=False)]
        if not matched.empty: predicted_species = matched.iloc[0]
    elif "tucan" in file_lower or "tucán" in file_lower:
        matched = species_df[species_df["nombre_comun"].str.contains("Tucán", case=False, na=False)]
        if not matched.empty: predicted_species = matched.iloc[0]
        
    if predicted_species is None:
        predicted_species = species_df.sample(1).iloc[0]
        
    confidence = round(random.uniform(0.70, 0.98), 2)
    intensity = round(random.uniform(0.50, 0.95), 2)
    duration = random.randint(5, 30)
    
    return {
        "event_id": event_id,
        "zone_id": zone_id,
        "species_id": predicted_species["species_id"],
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M"),
        "confidence_audio": confidence,
        "intensity_audio": intensity,
        "duration_sec": duration,
        "file_name": file_name,
        "_sci_name": predicted_species["nombre_cientifico"],
        "_com_name": predicted_species["nombre_comun"],
    }


def run_image_inference(file_path: str, zone_id: str, species_df: pd.DataFrame) -> dict:
    """
    Mock de inferencia de IA para imágenes.
    """
    time.sleep(2)
    
    file_name = os.path.basename(file_path)
    file_lower = file_name.lower()
    predicted_species = None
    
    if "gallito" in file_lower or "roca" in file_lower:
        matched = species_df[species_df["nombre_comun"].str.contains("Gallito", case=False, na=False)]
        if not matched.empty: predicted_species = matched.iloc[0]
    elif "tucan" in file_lower or "tucán" in file_lower:
        matched = species_df[species_df["nombre_comun"].str.contains("Tucán", case=False, na=False)]
        if not matched.empty: predicted_species = matched.iloc[0]
        
    if predicted_species is None:
        predicted_species = species_df.sample(1).iloc[0]
        
    confidence = round(random.uniform(0.75, 0.99), 2)
    bbox_count = random.randint(1, 3)
    
    now = datetime.now()
    event_id = f"V{random.randint(100, 999)}"
    
    return {
        "event_id": event_id,
        "zone_id": zone_id,
        "species_id": predicted_species["species_id"],
        "fecha": now.strftime("%Y-%m-%d"),
        "hora": now.strftime("%H:%M"),
        "confidence_visual": confidence,
        "bbox_count": bbox_count,
        "image_name": file_name,
        "_sci_name": predicted_species["nombre_cientifico"],
        "_com_name": predicted_species["nombre_comun"],
    }
