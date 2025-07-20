import os

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
MERCADO_PAGO_TOKEN = os.getenv('MERCADO_PAGO_TOKEN')

# Default cron hour for daily posts
CRON_HOUR = int(os.getenv('CRON_HOUR', '9'))  # 9 AM

from .database import get_session, get_bot_config


def get_public_channel_id() -> int | None:
    session = get_session()
    return get_bot_config(session).public_channel_id


def get_private_channel_id() -> int | None:
    session = get_session()
    return get_bot_config(session).private_channel_id


def set_channels(public_id: int, private_id: int) -> None:
    session = get_session()
    config = get_bot_config(session)
    config.public_channel_id = public_id
    config.private_channel_id = private_id
    session.commit()
