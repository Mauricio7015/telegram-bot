#!/usr/bin/env python3

from bot.scheduler import start as start_scheduler
from bot.bot import start_bot

if __name__ == '__main__':
    start_scheduler()
    start_bot()
