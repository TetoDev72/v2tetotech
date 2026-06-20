from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.main import main_keyboard

router = Router()

WELCOME_TEXT = """👋 Привет!
Я бот v2tetotech. К сожалению не дам пиццу (у меня нету 🍕), но могу:

• 🔓 Дешифровать криптоссылки по типу happ://crypt*
• 🔗 Сделать v2tetotech ссылку в конструкторе или автоматически
• 🛡️ Обойти лимит устройств или блокировки на "только хахапп"
• 🐱 Помочь сделать ссылку для добавления ссылки в Mihomo клиенты
• 🔗 Сделать диплинк для вашей подписки с обходом

Просто нажми на кнопку на клавиатуре или отправь (крипто)ссылку. Жду!"""

HELP_TEXT = """📋 <b>Список команд:</b>

/sync (ссылка) - делает sync ссылку
/fetch (ссылка) - делает fetch ссылку
/pg (ссылка) - делает advsync ссылку (конструктор)
/wlify (ссылка) - делает ссылку с обходом российского whitelist
/deeplink (ссылка) - делает диплинки
/batch (ссылки через пробел) - делает batch ссылку
/auto (ссылка) - делает auto ссылку
/charity - выдает charity ссылку с сообщением от разработчиков
/decrypt (ссылка) - дешифрует ссылку

💡 Просто отправь ссылку — бот сам сделает auto и sync ссылки!"""

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=main_keyboard())

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT)
