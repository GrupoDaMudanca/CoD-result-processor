
import csv
import os

import pandas as pd

from app.match import Match, MatchRecord
from config import OUTPUT_FILES_PATH, TEMP_OUTPUT_FILE_PATH, LATEST_OUTPUT_FILE_PATH


def file_valid(file_path):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return True

    return False


def read_new_match(match_data: list[dict], date: str = None) -> Match:
    # Ensure ignore_stats is passed explicitly if present, else defaults to False. 
    # MatchRecord kwargs expect ignore_stats as boolean if provided.
    return Match(*[MatchRecord(
        raw_player_name=record.get('raw_player_name'),
        score=record.get('score', 0),
        kills=record.get('kills', 0),
        assists=record.get('assists', 0),
        redeploys=record.get('redeploys', 0),
        damage=record.get('damage', 0),
        date=date,
        ignore_stats=record.get('ignore_stats', False)
    ) for record in match_data])


def write_matches(matches: list[Match]) -> None:
    header = ['match_id', 'player_id', 'player_name', 'score', 'kills', 'assists', 'redeploys', 'damage', 'date', 'ignore_stats']

    with open(
        TEMP_OUTPUT_FILE_PATH,
        mode='w',
        newline='',
        encoding='utf-8'
    ) as file:
        writer = csv.DictWriter(file, fieldnames=header)

        writer.writeheader()

        rows = [
            {
                'match_id': match.id,
                'player_id': record.player.id,
                'player_name': record.player.name,
                'score': record.score,
                'kills': record.kills,
                'assists': record.assists,
                'redeploys': record.redeploys,
                'damage': record.damage,
                'date': record.date,
                'ignore_stats': getattr(record, 'ignore_stats', False)
            }
            for match in matches
            for record in match.records
        ]

        writer.writerows(rows)


def match_exists(match_id: str) -> bool:
    """Check if a match with the given ID already exists in the latest CSV."""
    if file_valid(LATEST_OUTPUT_FILE_PATH):
        return False

    try:
        df = pd.read_csv(LATEST_OUTPUT_FILE_PATH)
        return match_id in df['match_id'].values
    except Exception:
        return False


def delete_match(match_id: str) -> int:
    """Deletes all rows with the given match_id from the latest CSV. Returns the number of deleted rows."""
    if file_valid(LATEST_OUTPUT_FILE_PATH):
        return 0

    try:
        df = pd.read_csv(LATEST_OUTPUT_FILE_PATH)
        initial_len = len(df)
        df = df[df['match_id'] != match_id]
        deleted_count = initial_len - len(df)
        if deleted_count > 0:
            df.to_csv(LATEST_OUTPUT_FILE_PATH, index=False)
        return deleted_count
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error deleting match {match_id}: {e}")
        return 0


def ignore_match_player(match_id: str, player_name: str) -> bool:
    """Sets ignore_stats to True for a specific player in a given match_id. Returns True if updated."""
    if file_valid(LATEST_OUTPUT_FILE_PATH):
        return False

    try:
        df = pd.read_csv(LATEST_OUTPUT_FILE_PATH)
        if 'ignore_stats' not in df.columns:
            df['ignore_stats'] = False
            
        mask = (df['match_id'] == match_id) & (df['player_name'] == player_name)
        if mask.any():
            df.loc[mask, 'ignore_stats'] = True
            df.to_csv(LATEST_OUTPUT_FILE_PATH, index=False)
            return True
        return False
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error ignoring player {player_name} in match {match_id}: {e}")
        return False


def get_player_names_map() -> dict:
    import json
    from config import PLAYER_NAMES_FILE_PATH
    with open(PLAYER_NAMES_FILE_PATH, 'r') as player_names_file:
        return {
            player_id: player_name
            for player_name, player_ids
            in json.loads(player_names_file.read()).items()
            for player_id in
            player_ids
        }
