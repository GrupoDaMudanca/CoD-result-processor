import requests
import logging

logger = logging.getLogger(__name__)

from app.messengers.base import MessengerClient
from config import (
    TELEGRAM_SEND_MESSAGE_ENDPOINT,
    TELEGRAM_SEND_PHOTO_ENDPOINT,
    TELEGRAM_CHAT_ID
)

class TelegramClient(MessengerClient):
    def send_message(self, text: str, reply_to_message_id: str = None, msg_type: str = "UNKNOWN", chat_id: str = None):
        target_chat = chat_id or TELEGRAM_CHAT_ID
        if not target_chat:
            return None

        params = {
            'chat_id': target_chat,
            'text': text
        }
        if reply_to_message_id:
            params['reply_to_message_id'] = reply_to_message_id

        try:
            logger.info(f"[TELEGRAM_OUTGOING] Type: {msg_type} | Message: {text}")
            response = requests.get(TELEGRAM_SEND_MESSAGE_ENDPOINT, params=params, timeout=10)
            return response.json()
        except Exception as e:
            logger.error(f'Failed to send Telegram message: {e}')
            return None

    def send_photo(self, photo_path: str, caption: str = None, reply_to_message_id: str = None, msg_type: str = "UNKNOWN", chat_id: str = None):
        target_chat = chat_id or TELEGRAM_CHAT_ID
        if not target_chat:
            return None

        try:
            with open(photo_path, 'rb') as photo:
                files = {'photo': photo}
                data = {'chat_id': target_chat}
                if caption:
                    data['caption'] = caption
                if reply_to_message_id:
                    data['reply_to_message_id'] = reply_to_message_id
                
                logger.info(f"[TELEGRAM_OUTGOING] Type: {msg_type} | Photo with caption: {caption}")
                response = requests.post(TELEGRAM_SEND_PHOTO_ENDPOINT, data=data, files=files, timeout=30)
                resp_json = response.json()
                if not resp_json.get('ok'):
                    logger.error(f"Telegram API Error in send_photo: {resp_json}")
                return resp_json
        except Exception as e:
            logger.error(f'Failed to send Telegram photo: {e}')
            return None
