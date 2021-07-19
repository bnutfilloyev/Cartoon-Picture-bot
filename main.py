import logging
import cv2
from aiogram import Bot, Dispatcher, executor, types
from uuid import uuid4
from aiogram.types import InputFile

# Token
API_TOKEN = 'Token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome_message(message: types.Message):
    await message.reply('Assalomu Alaykum! Menga rasm yuboring!')


@dp.message_handler(content_types=['photo'])
async def send_photo(message: types.Message):
    name = uuid4()
    await message.reply(text='Please wait 15 seconds 💬')
    await message.photo[-1].download(f'data/downloads/{name}.jpg')
    # load image
    img = cv2.imread(f'data/downloads/{name}.jpg')

    #Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    #Cartoonazation
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # save file
    cv2.imwrite(f'data/uploads/{name}.jpg', cartoon)
    photo_bytes = InputFile(path_or_bytesio=f'data/uploads/{name}.jpg')
    await bot.send_photo(chat_id=message.from_user.id, photo=photo_bytes,
                         caption=f'Success "{message.text}" 🎉')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)