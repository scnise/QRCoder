import asyncio
import qrcode
import io
from aiogram import Bot, Dispatcher, F
from aiogram.types import FSInputFile, Message, BufferedInputFile
from aiogram.filters import Command, CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")
dp = Dispatcher()
bot = Bot(token)
class StateM(StatesGroup):
   preqr = State()  

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📲 Создать QR-Code")], 
        [KeyboardButton(text="ℹ️ О боте")]                          
    ],
    resize_keyboard=True,         
    one_time_keyboard=True        
)
sec_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📲 Создать QR-Code")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
@dp.message(CommandStart())
async def staring(message: Message):
    await message.answer(f"Привет {message.from_user.username or message.from_user.first_name}!\nВыберите действие:", reply_markup=main_keyboard)
@dp.message(F.text == "ℹ️ О боте")
async def about(message: Message):
    await message.answer("Этот бот был создан @scnise, этот бот придуман и собран в ходе обуения", reply_markup=sec_keyboard)
@dp.message(F.text == "📲 Создать QR-Code")
async def preqrcode(message: Message, state: FSMContext):
    await state.set_state(StateM.preqr)
    await message.answer("Пришлите ссылку для которой нужно создать QR-Code(либо любой текст и тогда просто создастся ссылка на него):")
@dp.message(StateM.preqr)
async def afterqr(message: Message, state: FSMContext):
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4,)
    a = message.text
    qr.add_data(a)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_bytes = buffer.getvalue()
    photo_file = BufferedInputFile(qr_bytes, filename="qrcode.png")
    await message.answer_photo(photo=photo_file, caption="Ваш персональный QR-код!", reply_markup= main_keyboard)
    await state.clear()
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())