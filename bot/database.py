from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('sqlite:///bot.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    plan = Column(String)  # monthly or lifetime
    active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

class PublicPost(Base):
    __tablename__ = 'public_posts'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    images = Column(String)  # comma separated paths to images/videos
    sent = Column(Boolean, default=False)

class PrivatePost(Base):
    __tablename__ = 'private_posts'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    images = Column(String)  # comma separated paths to images/videos
    sent = Column(Boolean, default=False)


class BotConfig(Base):
    __tablename__ = 'bot_config'
    id = Column(Integer, primary_key=True)
    public_channel_id = Column(Integer, nullable=True)
    private_channel_id = Column(Integer, nullable=True)

Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()


def get_bot_config(session: Session) -> BotConfig:
    config = session.query(BotConfig).first()
    if not config:
        config = BotConfig(id=1)
        session.add(config)
        session.commit()
    return config
