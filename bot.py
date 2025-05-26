from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)
async def start(update, context):
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

async def hello(update, context):
    user_message = update.message.text
    await send_text(update, context, "Привет!")
    await send_text(update, context, "Как дела?")
    await send_text(update, context, "Вы написали " + user_message)

    await send_photo(update, context, "avatar_main")
    await send_text_buttons(update, context, "Запустить процесс.", {
        "start": "Запустить",
        "stop": "Остановить"
    })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update,context, "Процесс запущен.")
    else:
        await send_text(update, context, "Процесс остановлен.")

app = ApplicationBuilder().token("8031207381:AAE2YUJJEYQPoGiG9bJICktas_cwVKhrThE").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
