from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_publish_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовать", callback_data="publish"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data="reject")
        ]
    ])

def get_reject_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Сообщение отклонено", callback_data="already_rejected")
        ]
    ])