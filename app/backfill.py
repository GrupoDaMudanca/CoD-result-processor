import json
import os
import logging

logger = logging.getLogger(__name__)

from config import BACKFILL_STATE_FILE_PATH, UNRESTRICT_STATE_FILE_PATH

def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def set_backfill(year: str, month: str):
    """Activates backfill mode by setting the month and year."""
    _ensure_dir(BACKFILL_STATE_FILE_PATH)
    data = {
        'active': True,
        'year': year,
        'month': month
    }
    with open(BACKFILL_STATE_FILE_PATH, 'w') as f:
        json.dump(data, f)
    logger.info(f"Backfill activated for: {month}/{year}")

def get_backfill():
    """Returns a dictionary with backfill month and year if active."""
    if not os.path.exists(BACKFILL_STATE_FILE_PATH):
        return None
    try:
        with open(BACKFILL_STATE_FILE_PATH, 'r') as f:
            data = json.load(f)
            if data.get('active'):
                return data
    except Exception as e:
        logger.error(f"Error reading backfill file: {e}")
    return None

def clear_backfill():
    """Deactivates backfill mode."""
    if os.path.exists(BACKFILL_STATE_FILE_PATH):
        os.remove(BACKFILL_STATE_FILE_PATH)
        logger.info("Backfill deactivated.")

def set_unrestricted():
    _ensure_dir(UNRESTRICT_STATE_FILE_PATH)
    with open(UNRESTRICT_STATE_FILE_PATH, 'w') as f:
        json.dump({'unrestricted': True}, f)
    logger.info("Admin commands unrestricted for all users.")

def clear_unrestricted():
    if os.path.exists(UNRESTRICT_STATE_FILE_PATH):
        os.remove(UNRESTRICT_STATE_FILE_PATH)
        logger.info("Admin commands restricted to admins.")

def is_unrestricted():
    return os.path.exists(UNRESTRICT_STATE_FILE_PATH)
