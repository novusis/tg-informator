# -*- coding: utf-8 -*-
import signal
import asyncio
import queue

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject

from config import Config
import utils

# Initialize bot and dispatcher

VERSION = '0.0.3'
API_TOKEN = Config.app('token')

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
_post_queue = queue.Queue()


@dp.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    await bot.send_message(chat_id=message.chat.id, text=f'<code><b>ip requester v{VERSION}</b></code>')


# @dp.channel_post()
# async def channel_message(message: types.MessageOriginChannel):
#     channel_chat_id = message.chat.id
#     channel_message_id = message.message_id
#     print(f".channel_message channel_chat_id <{channel_chat_id}>")
#     print(f".channel_message message <{message}>")

@dp.message(F.text)
async def text_message_handler(message: types.Message):
    try:
        if message.text.lower() == 'hello':
            await message.reply(f'Hello {message.from_user.first_name}, welcome!')
        if message.text.lower() == 'post':
            post = 'test post'
            await make_info_post(post)
        else:
            await bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        tg_bot.utils.log_error(f".text_message_handler error: {e}>")


async def start_post_waiter():
    while True:
        while not _post_queue.empty():
            await make_info_post(_post_queue.get())
        await asyncio.sleep(1)


async def make_info_post(post):
    await bot.send_message(Config.app('info_channel_chat_id'), post)


async def start_bot():
    print(f"tg_bot.start_bot {VERSION}")
    await asyncio.gather(start_bot_main(), start_post_waiter())


async def start_bot_main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML), handle_signals=False)


if __name__ == '__main__':
    asyncio.run(start_bot())


def info_post(message):
    global _post_queue
    _post_queue.put(message)


def handle_sigint(_signal, _frame):
    print(f'SIGINT received, cancelling tasks... ({len(asyncio.all_tasks())})', flush=True)
    for task in asyncio.all_tasks():
        task.cancel()


signal.signal(signal.SIGINT, handle_sigint)
