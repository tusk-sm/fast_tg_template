from fastapi import FastAPI, Request
import logging
from telegram import Update, ReplyKeyboardMarkup #, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio
from conf import TOKEN

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI()


# Инициализация Telegram Application
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update, context):    
     # Создаем динамическую клавиатуру
    keyboard = [
        ['Кнопка 1', 'Кнопка 2'],
        ['Кнопка 3', 'Кнопка 4'],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?")

    # keyboard = InlineKeyboardMarkup.from_button(
    #     InlineKeyboardButton(text="Continue here!", url="https://ai.nnov.ru/")
    # )
    
    await update.message.reply_text('Привет! Я ваш бот.', reply_markup=reply_markup)

# Обработчик текстовых сообщений
async def echo(update, context):
   
   
    
    await update.message.reply_text(f'Вы сказали: {update.message.text}')

# Обработчик изображений
async def handle_image(update, context):
    await update.message.reply_text('Изображения пока не поддерживаются.')

# Обработчик видео
async def handle_video(update, context):
    await update.message.reply_text('Видео пока не поддерживаются.')

# Обработчик аудио
async def handle_audio(update, context):
    await update.message.reply_text('Аудиозаписи пока не поддерживаются.')

# Обработчик документов
async def handle_document(update, context):
    await update.message.reply_text('Документы пока не поддерживаются.')

# Обработчик голосовых сообщений
async def handle_voice(update, context):
    await update.message.reply_text('Голосовые сообщения пока не поддерживаются.')

# Обработчик стикеров
async def handle_sticker(update, context):
    await update.message.reply_text('Стикеры пока не поддерживаются.')

# Обработчик геолокации
async def handle_location(update, context):
    await update.message.reply_text('Геолокация пока не поддерживается.')

# Обработчик контактов
async def handle_contact(update, context):
    await update.message.reply_text('Контакты пока не поддерживаются.')

# Добавление обработчиков в диспетчер
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
application.add_handler(MessageHandler(filters.PHOTO, handle_image))
application.add_handler(MessageHandler(filters.VIDEO, handle_video))
application.add_handler(MessageHandler(filters.AUDIO, handle_audio))
# application.add_handler(MessageHandler(filters.DOCUMENT, handle_document))
application.add_handler(MessageHandler(filters.Document, handle_document))
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
# application.add_handler(MessageHandler(filters.STICKER, handle_sticker))
application.add_handler(MessageHandler(filters.Sticker, handle_sticker))
application.add_handler(MessageHandler(filters.LOCATION, handle_location))
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))

@app.get("/")
async def get_webhook(request: Request):
    return {"check": "ok"}
# Обработка вебхука
@app.post("/")
async def webhook(request: Request):
    # Получаем данные из запроса
    data = await request.json()

    print(data)
    update = Update.de_json(data, application.bot)

    print(update)
    
    # Обрабатываем обновление
    application.update_queue.put_nowait(update)

    return {"status": "ok"}


# Фоновая задача для обработки обновлений из очереди
async def process_updates():
    while True:
        update = await application.update_queue.get()
        if update is None:
            break

        print(update)
        res = await application.process_update(update)
        print(res)

@app.on_event("startup")
async def startup_event():
    from telegram import Bot
    
    # Получаем токен бота из переменных окружения
    bot_token = TOKEN
    
    
    # Инициализация бота
    application.bot = Bot(token=bot_token)

    await application.initialize()


    asyncio.create_task(process_updates())
    

# # Запуск приложения
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)