from aiogram import Router, F
from aiogram.types import (
    Message, 
    CallbackQuery,
    PhotoSize,
    Document,
    Sticker,
    Audio,
    Video,
    Animation,
    Voice
)
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.enums import ContentType

from app.database import db
from app.keyboards import get_publish_keyboard, get_reject_keyboard
from app.logger import logger
from config import ADMIN_GROUP_ID, CHANNEL_ID

router = Router()

async def prepare_media_caption(message: Message) -> str:
    """Формирует подпись для медиафайлов"""
    caption = ""
    if message.caption:
        caption = message.caption
    elif message.text:
        caption = message.text
    return f"От @{message.from_user.username}:\n\n{caption}" if caption else f"Медиа от @{message.from_user.username}"

async def handle_media(message: Message, bot, media_type: str):
    """Обработчик для всех типов медиа"""
    try:
        caption = await prepare_media_caption(message)
        
        # Получаем медиа-объект
        if media_type == 'photo':
            # Для фото берем последнюю (самую большую) версию
            media_obj = message.photo[-1]
        else:
            media_obj = getattr(message, media_type)
        
        # Формируем сообщение для группы модерации
        send_method = getattr(bot, f"send_{media_type}")
        media_message = await send_method(
            chat_id=ADMIN_GROUP_ID,
            caption=caption,
            reply_markup=get_publish_keyboard(),
            **{media_type: media_obj.file_id}
        )
        
        # Сохраняем в БД
        db.add_suggestion(
            original_msg_id=message.message_id,
            moderated_msg_id=media_message.message_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            text=caption,
            media_type=media_type,
            media_id=media_obj.file_id
        )
        
        logger.info(f"New {media_type} from @{message.from_user.username} forwarded to admin group")
    except Exception as e:
        logger.error(f"Error handling {media_type}: {e}")
        await message.answer("Произошла ошибка при обработке файла. Попробуйте позже.")
        
        logger.info(f"New {media_type} from @{message.from_user.username} forwarded to admin group")
    except Exception as e:
        logger.error(f"Error handling {media_type}: {e}")
        await message.answer("Произошла ошибка при обработке файла. Попробуйте позже.")

@router.message(Command("start"))
async def start_command(message: Message):
    try:
        logger.info(f"/start from @{message.from_user.username}")
        await message.answer("Привет! Отправь мне сообщение или файл, и я перешлю его модераторам.")
    except Exception as e:
        logger.error(f"Error in /start: {e}")

@router.message(F.content_type == ContentType.TEXT)
async def handle_text(message: Message, bot):
    try:
        if message.chat.id == ADMIN_GROUP_ID:
            return
            
        forwarded = await bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"Сообщение от @{message.from_user.username}:\n\n{message.text}",
            reply_markup=get_publish_keyboard()
        )
        
        db.add_suggestion(
            original_msg_id=message.message_id,
            moderated_msg_id=forwarded.message_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            text=message.text,
            media_type="text"
        )
        
        logger.info(f"Text message from @{message.from_user.username} forwarded")
    except Exception as e:
        logger.error(f"Error handling text: {e}")
        await message.answer("Ошибка обработки текста")

# Регистрируем обработчики для всех типов медиа
@router.message(F.content_type == ContentType.PHOTO)
async def handle_photo(message: Message, bot):
    await handle_media(message, bot, "photo")

@router.message(F.content_type == ContentType.DOCUMENT)
async def handle_document(message: Message, bot):
    await handle_media(message, bot, "document")

@router.message(F.content_type == ContentType.STICKER)
async def handle_sticker(message: Message, bot):
    await handle_media(message, bot, "sticker")

@router.message(F.content_type == ContentType.AUDIO)
async def handle_audio(message: Message, bot):
    await handle_media(message, bot, "audio")

@router.message(F.content_type == ContentType.VIDEO)
async def handle_video(message: Message, bot):
    await handle_media(message, bot, "video")

@router.message(F.content_type == ContentType.ANIMATION)
async def handle_animation(message: Message, bot):
    await handle_media(message, bot, "animation")

@router.message(F.content_type == ContentType.VOICE)
async def handle_voice(message: Message, bot):
    await handle_media(message, bot, "voice")

@router.callback_query(F.data == "publish")
async def publish_message(callback: CallbackQuery, bot):
    try:
        suggestion = db.get_suggestion(callback.message.message_id)
        if not suggestion:
            await callback.answer("Сообщение не найдено!")
            return
            
        if suggestion['status'] != 'pending':
            await callback.answer("Уже обработано!")
            return
            
        # Формируем чистый текст без username
        clean_text = suggestion['text'].split("\n\n", 1)[-1] if "\n\n" in suggestion['text'] else ""
        
        # Отправляем в канал
        if suggestion['media_type'] == 'text':
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=clean_text
            )
        else:
            send_method = getattr(bot, f"send_{suggestion['media_type']}")
            await send_method(
                chat_id=CHANNEL_ID,
                caption=clean_text,
                **{suggestion['media_type']: suggestion['media_id']}
            )
        
        db.update_status(callback.message.message_id, 'approved')
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.answer("Опубликовано!")
    except Exception as e:
        logger.error(f"Publish error: {e}")
        await callback.answer("Ошибка публикации!")

@router.callback_query(F.data == "reject")
async def reject_message(callback: CallbackQuery):
    try:
        db.update_status(callback.message.message_id, 'rejected')
        await callback.message.edit_reply_markup(reply_markup=get_reject_keyboard())
        await callback.answer("Отклонено!")
    except Exception as e:
        logger.error(f"Reject error: {e}")
        await callback.answer("Ошибка отклонения!")