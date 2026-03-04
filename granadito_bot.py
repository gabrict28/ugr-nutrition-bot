"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: granadito_bot.py
Configuración del bot de Telegram (cómo y cuándo envía la información)
"""

import os
import asyncio
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from macros_tgbot import resumen_telegram

load_dotenv()

async def tarea_difusion():
    #Los domingos no hay menú
    if datetime.now().weekday() == 6:
        return
    
    token = os.getenv("TELEGRAM_TOKEN")
    canal_id = os.getenv("TELEGRAM_ID") #el ID del canal
    
    bot = Bot(token=token)
    
    #Generamos el mensaje
    texto_menu = resumen_telegram("info_nutricional_menu.json")
    
    #Enviamos al canal
    await bot.send_message(chat_id=canal_id, text=texto_menu, parse_mode='Markdown')

async def main():
    scheduler = AsyncIOScheduler()
    
    #Programado de lunes a sábado a las 9:00 AM
    scheduler.add_job(tarea_difusion, 'cron', day_of_week='mon-sat', hour=9, minute=0)
    
    scheduler.start()

    #Mantenemos el script vivo 
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())