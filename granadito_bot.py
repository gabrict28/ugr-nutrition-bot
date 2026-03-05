"""
Proyecto: Bot informativo del aporte nutricional de los menús del SCU.
GABRIEL COBO TRAVÉ - 2026 
Script: granadito_bot.py
Configuración del bot de Telegram (cómo y cuándo envía la información)
"""

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from macros_tgbot import resumen_telegram

load_dotenv()

async def tarea_difusion():
    
    token = os.getenv("TELEGRAM_TOKEN")
    canal_id = os.getenv("TELEGRAM_ID") #el ID del canal
    
    bot = Bot(token=token)
    
    #Generamos el mensaje
    texto_menu = resumen_telegram("info_nutricional_menu.json")

    if texto_menu:
        #Enviamos al canal
        await bot.send_message(chat_id=canal_id, text=texto_menu, parse_mode='Markdown')
    else:
        print("Resumen vacío, nada que enviar")
    
    

if __name__ == "__main__":
    asyncio.run(tarea_difusion())