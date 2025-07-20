from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from .database import get_session
from .poster import send_public_post, send_private_post
from .config import CRON_HOUR

scheduler = BackgroundScheduler(timezone=pytz.utc)


def start():
    trigger = CronTrigger(hour=CRON_HOUR, minute=0, timezone=pytz.utc)
    scheduler.add_job(lambda: send_public_post(get_session()), trigger)
    scheduler.add_job(lambda: send_private_post(get_session()), trigger)
    scheduler.start()
