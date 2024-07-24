# -*- coding: utf-8 -*-
import signal
import asyncio

from aiogram import F
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject

from config import Config
import utils

# Initialize bot and dispatcher

VERSION = '0.0.1'
API_TOKEN = Config.app('token')

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message, command: CommandObject):
    await bot.send_message(chat_id=message.chat.id, text=f'<code><b>admins v{VERSION}</b></code>')


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
            await bot.send_message(Config.app('info_channel_chat_id'), 'test post')
        else:
            await bot.delete_message(message.chat.id, message.message_id)

    except Exception as e:
        utils.log_error(f".text_message_handler error: {e}>")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


if __name__ == '__main__':
    asyncio.run(main())


def handle_sigint(_signal, _frame):
    print('SIGINT received, cancelling tasks...')
    for task in asyncio.all_tasks():
        task.cancel()


signal.signal(signal.SIGINT, handle_sigint)
