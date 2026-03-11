from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from monitor import bots_data
from monitor import monitor_enabled
import monitor
from monitor import monitor_enabled
from database import get_incidents

TOKEN = "8682526573:AAEva2QVfxoy0AoLekt6CsiPwoLziOXJiNA"

bot = Bot(TOKEN)
dp = Dispatcher()

subscribers = set()
user_monitor = {}

def main_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Статус",
                    callback_data="status"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📉 История падений",
                    callback_data="history"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⏸ Выключить мониторинг",
                    callback_data="stop"
                ),
                InlineKeyboardButton(
                    text="▶️ Включить мониторинг",
                    callback_data="start"
                ),
            ],
        ]
    )


@dp.message(Command("start"))
async def start(message: Message):

    chat_id = message.chat.id

    subscribers.add(chat_id)

    user_monitor[chat_id] = True

    await message.answer(
        "🤖 Панель управления мониторингом",
        reply_markup=main_keyboard()
    )


async def send_alert(botname):

    for user in subscribers:

        if user_monitor.get(user, True):

            await bot.send_message(
                user,
                f"🚨 Бот {botname} OFFLINE!"
            )
from aiogram.types import CallbackQuery
from monitor import bots_data
from monitor import monitor_enabled
import monitor


@dp.callback_query(lambda c: c.data == "status")
async def status(call: CallbackQuery):

    text = "📊 Статус ботов\n\n"

    for name, status in bots_data.items():

        icon = "🟢" if status == "ONLINE" else "🔴"

        text += f"{icon} {name} — {status}\n"

    await call.message.answer(text)


@dp.callback_query(lambda c: c.data == "history")
async def history(call: CallbackQuery):

    rows = get_incidents()

    text = "📉 Последние падения\n\n"

    for bot, time in rows:

        text += f"{bot} — {time}\n"

    await call.message.answer(text)


@dp.callback_query(lambda c: c.data == "stop")
async def stop(call: CallbackQuery):

    user_monitor[call.message.chat.id] = False

    await call.message.answer("⏸ Мониторинг выключен только для вас")


@dp.callback_query(lambda c: c.data == "start")
async def start_monitor(call: CallbackQuery):

    user_monitor[call.message.chat.id] = True

    await call.message.answer("▶️ Мониторинг включён для вас")