import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def main():
    bot = Bot(token=TOKEN)
    updates = await bot.get_updates()
    for update in updates:
        print(f"Tu nombre: {update.message.from_user.first_name}")
        print(f"Tu CHAT_ID: {update.message.chat_id}")

if __name__ == "__main__":
    asyncio.run(main())