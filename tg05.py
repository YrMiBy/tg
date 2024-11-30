import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
NEWS_API_KEY = '2d2eb739c316410887699520355c3d0a'

@dp.message((Command('new_days')))
async def start_command(message: Message):
   await message.answer("Напиши какую новость хочешь узнать.")

@dp.message()
async def get_news(message: Message):
    new_days = message.text
    url = f'https://newsapi.org/v2/everything?q={new_days}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    news = response.json()

    if news['status'] == 'ok':
        articles = news['articles']
        for article in articles[:1]:  # Отправляем только 1 новость
            await message.reply(f"{article['title']}\n{article['url']}")
    else:
        await message.reply("Такой новости нет")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())