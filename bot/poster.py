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
    """Send media files with optional text in a single message."""
    if not files:
        if text:
            bot.send_message(chat_id=chat_id, text=text)
        return

    video_exts = (
        '.mp4',
        '.mov',
        '.avi',
        '.mkv',
        '.webm',
        '.mpg',
        '.mpeg',
    )

    if len(files) == 1:
        path = files[0]
        if path.lower().endswith(video_exts):
            with open(path, 'rb') as f:
                bot.send_video(chat_id=chat_id, video=f, caption=text or None)
        else:
            with open(path, 'rb') as f:
                bot.send_photo(chat_id=chat_id, photo=f, caption=text or None)
        return

    media = []
    for i, path in enumerate(files):
        caption = text if i == 0 else None
        if path.lower().endswith(video_exts):
            media.append(InputMediaVideo(open(path, 'rb'), caption=caption))
        else:
            media.append(InputMediaPhoto(open(path, 'rb'), caption=caption))
    bot.send_media_group(chat_id=chat_id, media=media)


def send_public_post(session: Session, post_id: int | None = None, resend: bool = False):
    if post_id is not None:
        if resend:
            post = session.query(PublicPost).filter_by(id=post_id).first()
        else:
            post = session.query(PublicPost).filter_by(id=post_id, sent=False).first()
    else:
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


def send_private_post(session: Session, post_id: int | None = None, resend: bool = False):
    if post_id is not None:
        if resend:
            post = session.query(PrivatePost).filter_by(id=post_id).first()
        else:
            post = session.query(PrivatePost).filter_by(id=post_id, sent=False).first()
    else:
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
