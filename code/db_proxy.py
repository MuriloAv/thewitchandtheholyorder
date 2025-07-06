# code/db_proxy.py
import json
import os
from datetime import datetime


SCORE_FILENAME = "high_scores.json"

def load_data():
    """Carrega dados do arquivo JSON. Retorna uma lista vazia se o arquivo não existir ou estiver corrompido."""
    if not os.path.exists(SCORE_FILENAME):
        return []
    try:
        with open(SCORE_FILENAME, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Salva dados (uma lista de scores) no arquivo JSON."""
    try:
        with open(SCORE_FILENAME, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        pass