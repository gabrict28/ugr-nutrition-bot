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

    print(f"[{datetime.now()}] Iniciando difusión diaria...")
    
    token = os.getenv("TELEGRAM_TOKEN")
    canal_id = os.getenv("TELEGRAM_ID") # Aquí pondrás el ID del canal
    
    bot = Bot(token=token)
    
    # Generamos el mensaje
    texto_menu = resumen_telegram("info_nutricional_menu.json")
    
    # Enviamos al canal
    await bot.send_message(chat_id=canal_id, text=texto_menu, parse_mode='Markdown')

async def main():
    scheduler = AsyncIOScheduler()
    
    #Progrado de lunes a sábado a las 10:00 AM
    scheduler.add_job(tarea_difusion, 'cron', day_of_week='mon-sat', hour=10, minute=0)
    
    scheduler.start()

    #Mantenemos el script vivo 
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())