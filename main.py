from conf.settings import TELEGRAM_TOKEN

from func.command import menu
from func.filter import filter_text
from func.callback import callback

from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, MessageHandler, filters

UPDATE = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

UPDATE.add_handler(CallbackQueryHandler(callback))
UPDATE.add_handler(CommandHandler('start', menu))
UPDATE.add_handler(MessageHandler(filters.TEXT, filter_text))

print("Iniciado... precione CTRL + C para cancelar.")

UPDATE.run_polling()
