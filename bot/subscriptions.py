from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import CallbackContext

from .database import User, get_session

MONTHLY_PRICE = 16.90
LIFETIME_PRICE = 35.90


def create_user(telegram_id: int, username: str):
    session = get_session()
    user = session.query(User).filter_by(telegram_id=telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=username, active=False)
        session.add(user)
        session.commit()
    return user


def activate_monthly(user: User):
    user.plan = 'monthly'
    user.active = True
    user.expires_at = datetime.utcnow() + timedelta(days=30)
    session = get_session()
    session.merge(user)
    session.commit()


def activate_lifetime(user: User):
    user.plan = 'lifetime'
    user.active = True
    user.expires_at = None
    session = get_session()
    session.merge(user)
    session.commit()


def check_expirations():
    session = get_session()
    now = datetime.utcnow()
    for user in session.query(User).filter_by(plan='monthly', active=True):
        if user.expires_at and user.expires_at < now:
            user.active = False
    session.commit()
