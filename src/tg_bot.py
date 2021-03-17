import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from tg_middlewares import AccessMiddleware
import calc

API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
ACCESS_ID = os.getenv('TELEGRAM_ACCESS_ID')
RUB = u'\u20BD'
SYMB = u'\U0001F6AA'

if (API_TOKEN == None):
    print("[ERROR] API_TOKEN is empty")
    exit()
if (ACCESS_ID == None):
    print("[ERROR] ACCESS_ID is empty")
    exit()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))

income_button = types.KeyboardButton('Get income!')
markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(income_button)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Hi!\nI'm DOXOD bot!\nRunning from the cupboard {SYMB}", reply_markup=markup)

@dp.message_handler(commands=['income'])
@dp.message_handler(Text(equals='Get income!'))
async def send_income(message: types.Message):
    overall = round(calc.get_current_portfolio_price() - calc.get_pays_in(), 2)
    await message.reply(f'Overall income:\n{str(overall)} {RUB}', reply_markup=markup)

@dp.message_handler()
async def send_nothing(message: types.Message):
    await message.reply(f'Sorry! Nothing to do with:\n{message.text}', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)