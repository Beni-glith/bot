import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot.config import BOT_TOKEN
from bot.handlers import start, button_handler, admin_handler
from bot.db import init_db

async def main():
    await init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
