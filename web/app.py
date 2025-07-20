from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from bot.database import get_session, User, PublicPost, PrivatePost

app = FastAPI()


class PostIn(BaseModel):
    text: str
    images: str  # comma separated paths


@app.post('/posts/public')
def add_public_post(post: PostIn):
    session = get_session()
    obj = PublicPost(text=post.text, images=post.images)
    session.add(obj)
    session.commit()
    return {'status': 'ok'}


@app.post('/posts/private')
def add_private_post(post: PostIn):
    session = get_session()
    obj = PrivatePost(text=post.text, images=post.images)
    session.add(obj)
    session.commit()
    return {'status': 'ok'}


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
