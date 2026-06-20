from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="🔗 Sync"),
            KeyboardButton(text="⚡ Auto"),
            KeyboardButton(text="🛡️ WL Bypass")
        ],
        [
            KeyboardButton(text="🔓 Decrypt"),
            KeyboardButton(text="🎁 Charity"),
            KeyboardButton(text="📦 Batch")
        ],
        [
            KeyboardButton(text="📋 Help")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
