import asyncio
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from db import is_user_whitelisted, add_user_to_whitelist
from imei_check_service import check_imei
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")

# Функция для парсинга полученного JSON, чтоб вся информация выводилась в виде "параметр": "значение"
def extract_properties(data):
    properties = data.get("properties", {})  # Извлекаем объект properties
    result = ''
    for key, value in properties.items():
        result += f'{key}: {value}\n'
    return result

# Обработка команды start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Отправь мне IMEI для проверки.")

# Обрабатывает входящий IMEI. Если пользователя нет в вайт листе, мы его туда добавляем.
async def handle_imei(update: Update, context):
    user_id = update.message.from_user.id
    if not is_user_whitelisted(user_id):
        await update.message.reply_text("Доступ запрещен.")
        add_user_to_whitelist(user_id)
        await update.message.reply_text("Вы добавлены в Whitelist")
        return

    imei = update.message.text

    if not is_valid_imei(imei):
        await update.message.reply_text("Некорректный IMEI.")
        return

    result = check_imei(imei)
    await update.message.reply_text(f"Результат проверки: \n{extract_properties(result)}")

# Проверка является ли валидным IMEI
def is_valid_imei(imei: str) -> bool:
    return imei.isdigit() and len(imei) == 15

# Запускаем бота, регистрируем обработчиков и отправляем все в бесконечный цикл
async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_imei))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    await asyncio.Event().wait()
