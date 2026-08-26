import os
import json
from config import IGNORE_STATE_FILE_PATH

def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def set_ignore_player(player_name: str):
    _ensure_dir(IGNORE_STATE_FILE_PATH)
    with open(IGNORE_STATE_FILE_PATH, 'w') as f:
        json.dump({"player": player_name}, f)

def get_ignore_player() -> str:
    if os.path.exists(IGNORE_STATE_FILE_PATH):
        try:
            with open(IGNORE_STATE_FILE_PATH, 'r') as f:
                data = json.load(f)
                return data.get("player")
        except:
            return None
    return None

def clear_ignore_player():
    if os.path.exists(IGNORE_STATE_FILE_PATH):
        os.remove(IGNORE_STATE_FILE_PATH)
