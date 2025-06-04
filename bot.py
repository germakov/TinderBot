from pyexpat.errors import messages
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from config import TG_BOT_TOKEN
from config import GPT_BOT_TOKEN
from gpt import *
from util import *

# тут будем писать наш код :)
async def start(update, context):
    dialog.mode = "main"
    text = load_message("main")
    await send_photo(update, context, "main")
    await send_text(update, context, text)

    await show_main_menu(update, context, {
        "start": "Запустить Бота...",
        "profile": "генерация Tinder-профиля 😎",
        "opener": "первое сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt, text)
    await send_text(update, context, answer)

async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "date_grande": "Ариана Гранде",
        "date_robbie": "Марго Робби",
        "date_zendaya": "Зендея",
        "date_gosling": "Райан Гослинг",
        "date_hardy": "Том Харди",
    })

async def date_dalog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Собеседник набирает "
                                                  "текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)
    # await send_text(update,context, answer)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update,context, query)
    await send_text(update,context, "Отличный выбор. Пригласите девушку ("
                                    "парня) на свидание за 5 сообщений.")
    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    elif dialog.mode == "date":
        await date_dalog(update, context)
    else:
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

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token=GPT_BOT_TOKEN)

app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("gpt", gpt))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date_.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
