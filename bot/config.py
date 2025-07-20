import os

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PUBLIC_CHANNEL_ID = int(os.getenv('PUBLIC_CHANNEL_ID', '0'))
PRIVATE_CHANNEL_ID = int(os.getenv('PRIVATE_CHANNEL_ID', '0'))
MERCADO_PAGO_TOKEN = os.getenv('MERCADO_PAGO_TOKEN')

# Default cron hour for daily posts
CRON_HOUR = int(os.getenv('CRON_HOUR', '9'))  # 9 AM
