from typing import List
from telegram import Bot, InputMediaPhoto, InputMediaVideo
from sqlalchemy.orm import Session

from .config import (
    BOT_TOKEN,
    get_public_channel_id,
    get_private_channel_id,
)
from .database import PublicPost, PrivatePost

bot = Bot(BOT_TOKEN)


def _send_media(chat_id: int, text: str, files: List[str]):
    media = []
    for path in files:
        if path.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm', '.mpg', '.mpeg')):
            media.append(InputMediaVideo(open(path, 'rb')))
        else:
            media.append(InputMediaPhoto(open(path, 'rb')))
    if media:
        bot.send_media_group(chat_id=chat_id, media=media)
    if text:
        bot.send_message(chat_id=chat_id, text=text)


def send_public_post(session: Session):
    post = (
        session.query(PublicPost)
        .filter_by(sent=False)
        .order_by(PublicPost.id)
        .first()
    )
    if not post:
        return
    images = [img.strip() for img in (post.images or '').split(',') if img.strip()]
    channel_id = get_public_channel_id()
    if channel_id:
        _send_media(channel_id, post.text, images)
    post.sent = True
    session.commit()


def send_private_post(session: Session):
    post = (
        session.query(PrivatePost)
        .filter_by(sent=False)
        .order_by(PrivatePost.id)
        .first()
    )
    if not post:
        return
    images = [img.strip() for img in (post.images or '').split(',') if img.strip()]
    channel_id = get_private_channel_id()
    if channel_id:
        _send_media(channel_id, post.text, images)
    post.sent = True
    session.commit()
