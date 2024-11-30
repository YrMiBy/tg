import asyncio
import random
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, F
from aiogram.filters import  Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import TOKEN
import sqlite3
import logging
import requests

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# Кнопки
button_registr = KeyboardButton(text="Регистрация в телеграм боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finances = KeyboardButton(text="Личные финансы")

# Клавиатура
keyboards = ReplyKeyboardMarkup(keyboard=[
   [button_registr, button_exchange_rates],
   [button_tips, button_finances]
   ], resize_keyboard=True)  #Уменьшение размера кнопок

# База данных
conn = sqlite3.connect('user.db')  # Подключение к БД user.db
cursor = conn.cursor()  # Создание курсора

# создание таблицы users с категориями личных финансов и записями по категориям
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
   id INTEGER PRIMARY KEY,
   telegram_id INTEGER UNIQUE,
   name TEXT,
   category1 TEXT,  
   category2 TEXT,
   category3 TEXT,
   expenses1 REAL,
   expenses2 REAL,
   expenses3 REAL
   )
''')

conn.commit()  # Сохранение таблицы

class FinancesForm(StatesGroup):  # Класс StatesGroup состояний
   category1 = State()
   expenses1 = State()
   category2 = State()
   expenses2 = State()
   category3 = State()
   expenses3 = State()


@dp.message(Command('start'))  # Функция старт
async def send_start(message: Message):  # Асинхронная функция
   # Сообщение пользователю и подключение клавиатуры
   await message.answer("Привет! Я ваш личный финансовый помощник. Выберите одну из опций в меню:", reply_markup=keyboards)

@dp.message(F.text == "Регистрация в телеграм боте")  # Функция регистрации
async def registration(message: Message):
   telegram_id = message.from_user.id  # id пользователя
   name = message.from_user.full_name  # Имя пользователя
   #  Выбор данных и БД по id пользователя
   cursor.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
   user = cursor.fetchone()  # берем данные пользователя
   if user:  # Если есть такой пользователь
       await message.answer("Вы уже зарегистрированы!")
   else:  # Если нет, его регистрируем
       cursor.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
       conn.commit()
       await message.answer("Вы успешно зарегистрированы!")

@dp.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
   url = "https://v6.exchangerate-api.com/v6/09edf8b2bb246e1f801cbfba/latest/USD"
   try:
       response = requests.get(url)  # Запрос по адресу url
       data = response.json()  # Переменная в которую заносится информация по запросу
       if response.status_code != 200:  # Если status_code не равен 200
           await message.answer("Не удалось получить данные о курсе валют!")
           return
       usd_to_rub = data['conversion_rates']['RUB']  # стоимость доллара в рублях
       eur_to_usd = data['conversion_rates']['EUR']  # стоимость евро в долларах
       euro_to_rub = eur_to_usd * usd_to_rub  # стоимость евро в рублях
       await message.answer(f"1 USD - {usd_to_rub:.2f}  RUB\n"   # Выводим значения с 2 знаками после запятой
                            f"1 EUR - {euro_to_rub:.2f}  RUB")
   except:
       await message.answer("Произошла ошибка")

@dp.message(F.text == "Советы по экономии")
async def send_tips(message: Message):
   tips = [
       "Совет 1: Ведите бюджет и следите за своими расходами.",
       "Совет 2: Откладывайте часть доходов на сбережения.",
       "Совет 3: Покупайте товары по скидкам и распродажам."
   ]
   tip = random.choice(tips)
   await message.answer(tip)

@dp.message(F.text == "Личные финансы")
async def finances(message: Message, state: FSMContext):  # Добавление состояния
   await state.set_state(FinancesForm.category1)  # Состояние category1 из класса FinancesForm
   await message.reply("Введите первую категорию расходов:")

@dp.message(FinancesForm.category1)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category1 = message.text)  # в категории 1 будет сохраняться текст сообщения
   await state.set_state(FinancesForm.expenses1)
   await message.reply("Введите расходы для категории 1:")

@dp.message(FinancesForm.expenses1)  # в
async def finances(message: Message, state: FSMContext):
   await state.update_data(expenses1 = float(message.text))  # занесение значения в 1 категорию
   await state.set_state(FinancesForm.category2)  # запрос второй категории
   await message.reply("Введите вторую категорию расходов:")

@dp.message(FinancesForm.category2)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category2 = message.text)  # занесение значения в 12 категорию
   await state.set_state(FinancesForm.expenses2)
   await message.reply("Введите расходы для категории 2:")

@dp.message(FinancesForm.expenses2)
async def finances(message: Message, state: FSMContext):
   await state.update_data(expenses2 = float(message.text))
   await state.set_state(FinancesForm.category3)
   await message.reply("Введите третью категорию расходов:")

@dp.message(FinancesForm.category3)
async def finances(message: Message, state: FSMContext):
   await state.update_data(category3 = message.text)
   await state.set_state(FinancesForm.expenses3)
   await message.reply("Введите расходы для категории 3:")

@dp.message(FinancesForm.expenses3)
async def finances(message: Message, state: FSMContext):
   data = await state.get_data()  #  переменная, в которую сохраняются все состояния
   telegarm_id = message.from_user.id
   # Занесение полученных значений в БД по id пользователя
   cursor.execute('''UPDATE users SET category1 = ?, expenses1 = ?, category2 = ?, expenses2 = ?, 
                    category3 = ?, expenses3 = ? WHERE telegram_id = ?''',
                  (data['category1'], data['expenses1'], data['category2'],
                   data['expenses2'], data['category3'], float(message.text), telegarm_id))
   conn.commit()
   await state.clear()  # Очищаем все состояния
   await message.answer("Категории и расходы сохранены!")

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())
