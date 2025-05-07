import pandas as pd
import requests
from config import settings

def load_knowledge_from_csv():
    return pd.read_csv(settings.CSV_PATH)

def load_knowledge_from_api():
    try:
        response = requests.get(settings.API_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)
    except Exception as e:
        raise RuntimeError(f"Gagal mengambil data dari API: {e}")

def load_knowledge():
    if settings.USE_API:
        return load_knowledge_from_api()
    return load_knowledge_from_csv()
