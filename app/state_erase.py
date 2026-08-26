import json
import os
import logging

logger = logging.getLogger(__name__)

from config import ERASE_STATE_FILE_PATH

def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def set_erase():
    """Activates erase mode."""
    _ensure_dir(ERASE_STATE_FILE_PATH)
    data = {
        'active': True
    }
    with open(ERASE_STATE_FILE_PATH, 'w') as f:
        json.dump(data, f)
    logger.info("Erase mode activated.")

def get_erase() -> bool:
    """Returns True if erase mode is active, False otherwise."""
    if not os.path.exists(ERASE_STATE_FILE_PATH):
        return False
    try:
        with open(ERASE_STATE_FILE_PATH, 'r') as f:
            data = json.load(f)
            return bool(data.get('active', False))
    except Exception as e:
        logger.error(f"Error reading erase file: {e}")
    return False

def clear_erase():
    """Deactivates erase mode by removing the state file."""
    if os.path.exists(ERASE_STATE_FILE_PATH):
        os.remove(ERASE_STATE_FILE_PATH)
        logger.info("Erase mode deactivated.")
