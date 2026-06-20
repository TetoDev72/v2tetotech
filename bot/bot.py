import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, commands, text_handler
from middlewares.server_selector import ServerSelectorMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.message.middleware(ServerSelectorMiddleware())
    dp.callback_query.middleware(ServerSelectorMiddleware())
    
    dp.include_router(start.router)
    dp.include_router(commands.router)
    dp.include_router(text_handler.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    logging.info("🚀 Bot started!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("👋 Bot stopped")
