import asyncio
import uvicorn

from monitor import monitor_loop, fetch_status
from telegram_bot import dp, bot, send_alert


async def start():

    # мониторинг
    asyncio.create_task(
        monitor_loop(fetch_status, send_alert)
    )

    # телеграм бот
    asyncio.create_task(
        dp.start_polling(bot)
    )

    # веб панель
    config = uvicorn.Config(
        "web_panel:app",
        host="0.0.0.0",
        port=8000
    )

    server = uvicorn.Server(config)

    await server.serve()


asyncio.run(start())