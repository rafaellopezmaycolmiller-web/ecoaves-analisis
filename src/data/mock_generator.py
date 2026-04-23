import pandas as pd
import random
from datetime import datetime, timedelta

species_list = [
    ("SP001", "Gallito de las rocas"),
    ("SP002", "Tucán"),
    ("SP003", "Hormiguero"),
    ("SP004", "Tángara"),
    ("SP005", "Batará"),
]

zones = [
    ("Z001", -6.46, -76.36, 400),
    ("Z002", -6.49, -76.38, 420),
    ("Z003", -6.42, -76.32, 850),
    ("Z004", -6.49, -76.35, 500),
]

def generate_time():
    # aves activas en mañana/tarde
    hour = random.choice([5,6,7,17,18])
    minute = random.randint(0,59)
    return f"{hour:02d}:{minute:02d}"

def generate_confidence(base=0.8):
    noise = random.uniform(-0.3, 0.2)
    return max(0.3, min(0.98, base + noise))

def generate_mock_data(n=200):
    data = []

    start_date = datetime(2026, 4, 20)

    for i in range(n):
        sp = random.choice(species_list)
        zone = random.choice(zones)

        date = start_date + timedelta(days=random.randint(0,5))
        time = generate_time()

        # comportamiento diferente por especie
        if sp[1] == "Hormiguero":
            conf_audio = generate_confidence(0.85)
            conf_visual = generate_confidence(0.5)
        elif sp[1] == "Tucán":
            conf_audio = generate_confidence(0.6)
            conf_visual = generate_confidence(0.9)
        else:
            conf_audio = generate_confidence(0.75)
            conf_visual = generate_confidence(0.75)

        data.append({
            "event_id": f"E{i}",
            "zone_id": zone[0],
            "species_id": sp[0],
            "fecha": date.strftime("%Y-%m-%d"),
            "hora": time,
            "confidence_audio": round(conf_audio, 2),
            "confidence_visual": round(conf_visual, 2),
        })

    return pd.DataFrame(data)