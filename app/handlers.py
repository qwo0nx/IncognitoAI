import logging
import html
import re
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender
from .chain import stream_answer
from .storage import build_storage

log = logging.getLogger(__name__)
router = Router()
storage = build_storage()

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Обычный", callback_data="mode_normal")],
        [InlineKeyboardButton(text="🟡 Средний", callback_data="mode_medium")],
        [InlineKeyboardButton(text="🔴 Высокий (18+)", callback_data="mode_high")]
    ])

@router.message(Command('start'))
async def cmd_start(m: Message):
    storage.set_mode(m.from_user.id, "normal")
    await m.answer("👹 <b>Agent-Monster X5!</b>\n\nВыбери режим:", parse_mode="HTML", reply_markup=get_main_menu())

@router.message(Command('profile'))
async def cmd_profile(m: Message):
    uid = m.from_user.id
    reqs = storage.get_stats(uid)
    mode = storage.get_mode(uid)
    custom = storage.get_prompt(uid)
    
    text = (
        f"👤 <b>Твой профиль</b>\n\n"
        f"📊 Запросов сделано: <b>{reqs}</b>\n"
        f"⚙️ Текущий режим: <b>{mode}</b>\n"
        f"📝 Личный промпт: {'<i>Установлен</i>' if custom else '<i>Нет</i>'}\n\n"
        f"Чтобы сбросить личный промпт, напиши /clear_prompt"
    )
    await m.answer(text, parse_mode="HTML")

@router.message(Command('prompt'))
async def cmd_prompt(m: Message):
    text = m.text.replace('/prompt', '').strip()
    if not text:
        await m.answer("⚠️ Напиши так: /prompt Ты злой хакер, отвечай матом.")
        return
    storage.set_prompt(m.from_user.id, text)
    await m.answer("✅ Личный промпт сохранен! Теперь я буду отвечать по этим правилам.")

@router.message(Command('clear_prompt'))
async def cmd_clear_prompt(m: Message):
    storage.clear_prompt(m.from_user.id)
    await m.answer("🧹 Личный промпт удален. Вернулся к стандартным режимам.")

@router.callback_query(F.data.startswith('mode_'))
async def set_mode(c: CallbackQuery):
    mode = c.data.replace('mode_', '')
    storage.set_mode(c.from_user.id, mode)
    await c.message.edit_text(f"✅ Режим изменен на: {mode}", reply_markup=get_main_menu())

@router.message(F.text)
async def on_text(m: Message):
    uid = m.from_user.id
    storage.append(uid, 'user', m.text)
    storage.add_stat(uid)
    
    mode = storage.get_mode(uid)
    is_code = any(w in m.text.lower() for w in ["код", "html", "скрипт", "python", "чит"])
    
    wait_msg = await m.answer("👹 <i>Monster думает...</i>", parse_mode="HTML")
    
    # Генератор стриминга
    stream = await stream_answer(storage.get(uid), mode, uid)
    
    full_text = ""
    last_edit = asyncio.get_event_loop().time()
    
    async for chunk in stream:
        full_text += chunk
        # Обновляем сообщение раз в 1.5 секунды, чтобы не получить FloodWait от Telegram
        if asyncio.get_event_loop().time() - last_edit > 1.5:
            try:
                await wait_msg.edit_text(full_text[:4000] + " ▌", parse_mode="HTML")
            except:
                pass
            last_edit = asyncio.get_event_loop().time()

    # Финальный текст
    storage.append(uid, 'assistant', full_text)
    
    try:
        await wait_msg.delete()
    except:
        pass

    if is_code:
        clean = re.sub(r'```[a-zA-Z]*\n', '', full_text).replace("```", "").strip()
        ext = "html" if "html" in m.text.lower() else "py"
        file = BufferedInputFile(clean.encode('utf-8'), filename=f"code.{ext}")
        await m.answer_document(file, caption="💻 <b>Код готов!</b>", parse_mode="HTML")
    else:
        # Если текст длинный, файлом
        if len(full_text) > 4000:
            file = BufferedInputFile(full_text.encode('utf-8'), filename="report.txt")
            await m.answer_document(file, caption="📄 <b>Длинный ответ</b>", parse_mode="HTML")
        else:
            try:
                await m.answer(full_text, parse_mode="HTML")
            except:
                await m.answer(html.escape(full_text))