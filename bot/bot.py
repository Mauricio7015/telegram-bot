from telegram.ext import Updater, CommandHandler

from .config import BOT_TOKEN
from .subscriptions import create_user
from .subscriptions import MONTHLY_PRICE, LIFETIME_PRICE
from .payments import create_payment

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


# Generate dummy payment links
MONTHLY_LINK = create_payment(MONTHLY_PRICE, 'Plano Mensal')
LIFETIME_LINK = create_payment(LIFETIME_PRICE, 'Plano Vitalicio')


def start(update, context):
    user = create_user(update.effective_user.id, update.effective_user.username)
    text = (
        'Bem-vindo!\n'
        'Escolha um plano:\n'
        f'/mensal - R$ {MONTHLY_PRICE}\n'
        f'/vitalicio - R$ {LIFETIME_PRICE}'
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def mensal(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Para assinar o plano mensal pague via PIX: {MONTHLY_LINK}'
    )


def vitalicio(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Para assinar o plano vitalicio pague via PIX: {LIFETIME_LINK}'
    )


def start_bot():
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('mensal', mensal))
    dispatcher.add_handler(CommandHandler('vitalicio', vitalicio))
    updater.start_polling()
    updater.idle()
