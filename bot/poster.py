from datetime import datetime
from pathlib import Path
from typing import List
from telegram import Bot, InputMediaPhoto
from sqlalchemy.orm import Session

from .config import BOT_TOKEN, PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID
from .database import PublicPost, PrivatePost, get_session

bot = Bot(BOT_TOKEN)


def _send_images(chat_id: int, text: str, images: List[str]):
    media = [InputMediaPhoto(open(path, 'rb')) for path in images]
    if media:
        bot.send_media_group(chat_id=chat_id, media=media)
    if text:
        bot.send_message(chat_id=chat_id, text=text)


def send_public_post(session: Session):
    post = session.query(PublicPost).order_by(PublicPost.id).first()
    if not post:
        return
    images = [img.strip() for img in (post.images or '').split(',') if img.strip()]
    _send_images(PUBLIC_CHANNEL_ID, post.text, images)
    session.delete(post)
    session.commit()


def send_private_post(session: Session):
    post = session.query(PrivatePost).order_by(PrivatePost.id).first()
    if not post:
        return
    images = [img.strip() for img in (post.images or '').split(',') if img.strip()]
    _send_images(PRIVATE_CHANNEL_ID, post.text, images)
    session.delete(post)
    session.commit()
