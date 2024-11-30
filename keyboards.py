from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Команда start
start = ReplyKeyboardMarkup(keyboard=[
   [KeyboardButton(text="Привет")],  [KeyboardButton(text="Пока")]
], resize_keyboard=True)

# Команда links
inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Видео", url='<<https://youtube.com/")>')],
   [InlineKeyboardButton(text="Новости", url='<https://lenta.ru/news/2024/11/29/sotni-boytsov-vsu-i-naemnikov-blokirovany-na-zavode-v-chasovom-yare-rossiyskie-voennye-povtorili-stsenariy-azovstali/>')],
   [InlineKeyboardButton(text="Музыка", url='<https://samplelib.com/lib/preview/wav/sample-3s.wav')]
])

# Команда dynamic
keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")
]])

keyboard =InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
    [InlineKeyboardButton(text="Опция 2", callback_data="option_2")
]])
