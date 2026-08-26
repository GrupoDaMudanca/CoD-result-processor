import os
import json
from config import APP_DIR

STATE_IGNORE_FILE = os.path.join(APP_DIR, 'state_ignore.json')

def set_ignore_player(player_name: str):
    with open(STATE_IGNORE_FILE, 'w') as f:
        json.dump({"player": player_name}, f)

def get_ignore_player() -> str:
    if os.path.exists(STATE_IGNORE_FILE):
        try:
            with open(STATE_IGNORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get("player")
        except:
            return None
    return None

def clear_ignore_player():
    if os.path.exists(STATE_IGNORE_FILE):
        os.remove(STATE_IGNORE_FILE)
