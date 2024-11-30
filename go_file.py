import types
from gc import get_objects
from itertools import count
from main.models import Survey

from aiogram.types import ReplyKeyboardMarkup

from aiogram import Bot, Dispatcher
from aiogram.utils import executor

from main.models import Survey

bot = Bot(token='7633849931:AAH8A8I6_Ft6gkfRe-yoq9B1IWt5ZJ8ENZE')
dp = Dispatcher(bot)
menu = ReplyKeyboardMarkup(resize_keyboard=True)

@dp.message_handler(commands=['start'])
async def get_message(message):
    my_chat = message.chat.id
    my_text = 'Привет! Готов пройти опрос?'
    menu.add('Да').add('Нет, спасибо, позже')
    await bot.send_message(chat_id=my_chat, text=my_text, reply_markup=menu)

@dp.message_handler(text='Да')
async def asking(message):
    my_chat = message.chat.id
    surveyes = Survey.get_objects.count()

executor.start_polling(dp)