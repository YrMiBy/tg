import asyncio
from aiogram.filters import CommandStart, Command
from config import TOKEN
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда старт (Привет, Пока)
@dp.message(CommandStart())
async def start(message: Message):
   await message.answer(f'Приветствие', reply_markup=kb.start)

@dp.message(F.text == "Привет") # Обработка кнопки
async def test_button(message: Message):
   await message.answer(f'Привет {message.from_user.full_name}')

@dp.message(F.text == "Пока")
async def test_button(message: Message):
   await message.answer(f'Пока {message.from_user.full_name}')

# Кнопки с URL-ссылками
@dp.message(Command('links'))
async def start(message: Message):
    await message.answer('Видео', reply_markup=kb.inline_keyboard)
    await message.answer('Новости', reply_markup=kb.inline_keyboard)
    await message.answer('Музыка', reply_markup=kb.inline_keyboard)

# Команда dinamic
# Обработчик команды /dynamic
@dp.message(Command('dynamic'))
async def send_dynamic(message: Message):
    await message.answer("Нажмите кнопку ниже:", reply_markup=kb.keyboard1)

# Обработчик нажатия на кнопку "Показать больше"
@dp.callback_query(lambda c: c.data == 'show_more')
async def process_show_more(callback_query: types.CallbackQuery):
    await bot.edit_message_text("Выберите опцию:", chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id, reply_markup=kb.keyboard)

# Обработчик нажатия на кнопки "Опция 1" и "Опция 2"
@dp.callback_query(lambda c: c.data in ['option_1', 'option_2'])
async def process_option(callback_query: types.CallbackQuery):
    option_text = "Вы выбрали " + ("Опцию 1" if callback_query.data == 'option_1' else "Опцию 2")
    await bot.send_message(callback_query.from_user.id, option_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
