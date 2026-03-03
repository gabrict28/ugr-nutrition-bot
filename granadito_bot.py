import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from macros_tgbot import resumen_telegram 

load_dotenv()

async def enviar_menu():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_ID")
    
    bot = Bot(token=token)

    texto_menu = resumen_telegram("info_nutricional_menu.json")
    
    await bot.send_message(chat_id=chat_id, text=texto_menu, parse_mode='Markdown')

if __name__ == "__main__":
    asyncio.run(enviar_menu())