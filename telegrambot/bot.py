from datetime import datetime
import os
from os import getenv
import django
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from main.models import Survey, Question, QueText, Client, Answer

from aiogram.types import ReplyKeyboardMarkup

from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
storage = MemoryStorage()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)

# Состояния
class UserForm(StatesGroup):
    name = State()
    phone = State()
    email = State()

class QuestionForm(StatesGroup):
    waiting_for_answer = State()


@dp.message_handler(commands=['start'])
async def get_message(message: Message):
    username_in_chat = message.from_user.username
    print(username_in_chat)
    try:
        now_client = Client.objects.get(acc_tg=message.from_user.username)
        my_chat = message.chat.id
        my_text = 'Готов пройти опрос?'
        button1 = 'Готов'
        button2 = 'Нет, спасибо, позже'
        menu = ReplyKeyboardMarkup(resize_keyboard=True).add(button1, button2)
        await bot.send_message(chat_id=my_chat, text=my_text, reply_markup=menu)
    except Client.DoesNotExist:
        await bot.send_message(chat_id=my_chat, text="Мы с вами не знакомы! Напишите команду /me", reply_markup=ReplyKeyboardRemove())
        await start(message)
        return


@dp.message_handler(text='Готов')
async def asking(message: Message, state: FSMContext):
    if not Survey.objects.filter(active=True).exists():
        await bot.send_message(chat_id=message.chat.id, text="На данный момент нет активных опросов.", reply_markup=ReplyKeyboardRemove())
        return

    now_survey = Survey.objects.get(active=True)
    await state.update_data(survey_id=now_survey.id, current_question=1)
    await ask_survey(message, state)


async def ask_survey(message: Message, state: FSMContext):
    user_data = await state.get_data()
    survey_id = user_data.get("survey_id")
    current_question = user_data.get("current_question")

    now_survey = Survey.objects.get(id=survey_id)
    total_questions = now_survey.counting

    if current_question > total_questions:
        await message.answer("Спасибо за участие в опросе!")
        await state.finish()
        return

    now_question = Question.objects.filter(survey=now_survey, numb=current_question).first()
    if now_question:
        que_text = QueText.objects.filter(que=now_question).first()
        if que_text:
            await bot.send_message(chat_id=message.chat.id, text=que_text.your_text, reply_markup=ReplyKeyboardRemove())
            await QuestionForm.waiting_for_answer.set()
        else:
            await message.answer("Ошибка: текст вопроса отсутствует.")
            await state.finish()
    else:
        await message.answer("Ошибка: вопрос не найден.")
        await state.finish()


@dp.message_handler(state=QuestionForm.waiting_for_answer)
async def handle_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    survey_id = user_data.get("survey_id")
    current_question = user_data.get("current_question")

    now_client = Client.objects.get(acc_tg=message.from_user.username)
    now_survey = Survey.objects.get(id=survey_id)
    now_question = Question.objects.filter(survey=now_survey, numb=current_question).first()

    if now_question:
        Answer.objects.create(
            client=now_client,
            que=now_question,
            ans=message.text,
            date=datetime.now()
        )
        await state.update_data(current_question=current_question + 1)
        await ask_survey(message, state)
    else:
        await message.answer("Ошибка: текущий вопрос не найден.")
        await state.finish()


@dp.message_handler(commands=['me'])
async def start(message: Message):
    await UserForm.name.set()

@dp.message_handler(state=UserForm.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Спасибо! Теперь напишите ваш номер телефона.")
    await UserForm.phone.set()

@dp.message_handler(state=UserForm.phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Отлично! Теперь введите вашу почту.")
    await UserForm.email.set()

@dp.message_handler(state=UserForm.email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if not email or "@" not in email:
        await message.answer("Пожалуйста, введите корректный email.")
        return

    await state.update_data(email=email)
    user_data = await state.get_data()
    Client.objects.create(
        name=user_data.get("name"),
        acc_tg=message.from_user.username,
        phone=user_data.get("phone"),
        email=email,
    )
    await message.answer("Спасибо! Вы зарегистрированы. Теперь введите /start для начала опроса.")
    await state.finish()




#executor.start_polling(dp)
async def main():
    # Запуск бота
    try:
        await dp.start_polling()
    finally:
        await bot.close()