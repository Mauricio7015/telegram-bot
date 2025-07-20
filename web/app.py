from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

from bot.database import (
    get_session,
    User,
    PublicPost,
    PrivatePost,
    get_bot_config,
)
from telegram.error import TimedOut, NetworkError
from bot.poster import bot as telegram_bot
from bot.config import set_channels

app = FastAPI()
app.mount('/static', StaticFiles(directory='web/static'), name='static')
UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount('/uploads', StaticFiles(directory=UPLOAD_DIR), name='uploads')


@app.get('/')
def index():
    return FileResponse('web/static/index.html')


class ChannelConfigIn(BaseModel):
    public_channel_id: int
    private_channel_id: int


@app.post('/posts/public')
async def add_public_post(text: str = Form(...), files: List[UploadFile] = File(None)):
    session = get_session()
    filenames = []
    if files:
        for f in files:
            dest = os.path.join(UPLOAD_DIR, f.filename)
            with open(dest, 'wb') as out:
                out.write(await f.read())
            filenames.append(dest)
    obj = PublicPost(text=text, images=','.join(filenames))
    session.add(obj)
    session.commit()
    return {'status': 'ok'}


@app.get('/posts/public')
def list_public_posts():
    session = get_session()
    posts = session.query(PublicPost).order_by(PublicPost.id).all()
    data = [
        {'id': p.id, 'text': p.text, 'images': p.images, 'sent': p.sent}
        for p in posts
    ]
    return {'posts': data}


@app.post('/posts/private')
async def add_private_post(text: str = Form(...), files: List[UploadFile] = File(None)):
    session = get_session()
    filenames = []
    if files:
        for f in files:
            dest = os.path.join(UPLOAD_DIR, f.filename)
            with open(dest, 'wb') as out:
                out.write(await f.read())
            filenames.append(dest)
    obj = PrivatePost(text=text, images=','.join(filenames))
    session.add(obj)
    session.commit()
    return {'status': 'ok'}


@app.get('/posts/private')
def list_private_posts():
    session = get_session()
    posts = session.query(PrivatePost).order_by(PrivatePost.id).all()
    data = [
        {'id': p.id, 'text': p.text, 'images': p.images, 'sent': p.sent}
        for p in posts
    ]
    return {'posts': data}


@app.get('/stats')
def stats():
    session = get_session()
    total_public = session.query(User).count()
    private_active = session.query(User).filter_by(active=True).count()
    monthly = session.query(User).filter_by(plan='monthly', active=True).count()
    lifetime = session.query(User).filter_by(plan='lifetime', active=True).count()
    return {
        'usuarios_publicos': total_public,
        'usuarios_privados': private_active,
        'assinaturas_mensais': monthly,
        'assinaturas_vitalicias': lifetime,
    }


@app.get('/channels/config')
def get_channels():
    session = get_session()
    config = get_bot_config(session)
    return {
        'public_channel_id': config.public_channel_id,
        'private_channel_id': config.private_channel_id,
    }


@app.post('/channels/config')
def set_channels_endpoint(cfg: ChannelConfigIn):
    try:
        telegram_bot.get_chat(cfg.public_channel_id)
        telegram_bot.get_chat(cfg.private_channel_id)
    except Exception:
        raise HTTPException(status_code=400, detail='Bot sem acesso a algum canal')
    set_channels(cfg.public_channel_id, cfg.private_channel_id)
    return {'status': 'ok'}


@app.get('/channels/available')
def list_channels():
    try:
        updates = telegram_bot.get_updates()
    except (TimedOut, NetworkError):
        updates = []
    channels = {}
    for u in updates:
        chat = None
        if u.channel_post:
            chat = u.channel_post.chat
        elif u.my_chat_member:
            chat = u.my_chat_member.chat
        elif u.message and u.message.chat.type == 'channel':
            chat = u.message.chat
        if chat:
            channels[chat.id] = chat.title or ''
    data = [{'id': cid, 'title': title} for cid, title in channels.items()]
    return {'channels': data}
