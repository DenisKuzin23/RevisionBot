from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
import config


storage = MemoryStorage()
bot = Bot(config.bot_token)
dp = Dispatcher(bot, storage=storage)
chat_to_naswer: int

class States(StatesGroup):
    otzyv_begin = State()
    otzyv_end = State()
    zhaloba_begin = State()
    zhaloba_end = State()
    answer = State()

@dp.message_handler(commands=['start'])
async def start_ch(message: types.Message):
    buttons = [
        InlineKeyboardButton(text='Отзывы', callback_data='otzyvy'),
        InlineKeyboardButton(text='Жалобы', callback_data='zhaloby')
    ]
    kb = InlineKeyboardMarkup()
    kb.add(*buttons)
    await message.answer(f'''
Письмо приветствия

Здравствуйте, этот бот создан для того, чтобы вы могли оставлять ваши отзывы, пожелания либо жалобы.

Если у вас возникнут вопросы по качеству питания выберете кнопку, которая будет характеризовать ваше сообщение и мы обязательно ответить на него.

В сообщении укажите как вас зовут, с какого вы города и название вашей столовой. 

Например: «здравствуйте, меня зовут Иван Иванов, г. Москва, столовая школы №1. Спасибо, было вкусно» 

Приятного аппетита!😋''', reply_markup=kb)

@dp.message_handler(commands=['aa_65399'])
async def add_admin(message: types.Message):
    config.save_admins(message.chat.id)

@dp.callback_query_handler(text='otzyvy')
async def otz_ch(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте мне, пожалуйста, ваш отзыв.')
    await States.otzyv_begin.set()

@dp.message_handler(state=States.otzyv_begin)
async def otzyv_begin(message: types.Message, state: FSMContext):
    await state.update_data(otzyv=message.text)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Отправить отзыв', callback_data='so'))
    await message.answer('Я получил ваш отзыв, подтвердите его отправку.', reply_markup=kb)
    await States.otzyv_end.set()

@dp.callback_query_handler(text='so', state=States.otzyv_end)
async def so_ch(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer('Спасибо за ваш отзыв, отправлен в обработку.')
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Ответить', callback_data=f'otzyv_{callback.message.chat.id}'))
    for admin in config.get_admins():
       await bot.send_message(admin, f'Поступил отзыв от {callback.message.from_user.username} \"{data["otzyv"]}\"', reply_markup=kb)
    await state.finish()

@dp.callback_query_handler(text='zhaloby')
async def otz_ch(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте мне, пожалуйста, вашу жалобу.')
    await States.zhaloba_begin.set()

@dp.message_handler(state=States.zhaloba_begin)
async def otzyv_begin(message: types.Message, state: FSMContext):
    await state.update_data(zhaloba=message.text)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Отправить жалобу', callback_data='sz'))
    await message.answer('Я получил вашу жалобу, подтвердите её отправку.', reply_markup=kb)
    await States.zhaloba_end.set()

@dp.callback_query_handler(text='sz', state=States.zhaloba_end)
async def so_ch(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer('Спасибо за вашу жалобу, отправлена в обработку.')
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='Ответить', callback_data=f'zhaloba_{callback.message.chat.id}'))
    for admin in config.get_admins():
        await bot.send_message(admin, f'Поступила жалоба от {callback.message.from_user.username} \"{data["zhaloba"]}\"', reply_markup=kb)

@dp.callback_query_handler(Text(startswith='zhaloba'))
async def zhaloba_handler(callback: types.CallbackQuery, state: FSMContext):
    global chat_to_naswer
    chat_id = callback.data.split('_')[1]
    chat_to_naswer = int(chat_id)
    await callback.message.answer(f'Напишите ваш ответ на жалобу.')
    await States.answer.set()

@dp.callback_query_handler(Text(startswith='otzyv'))
async def zhaloba_handler(callback: types.CallbackQuery, state: FSMContext):
    global chat_to_naswer
    chat_id = callback.data.split('_')[1]
    chat_to_naswer = int(chat_id)
    await callback.message.answer(f'Напишите ваш ответ на отзыв.')
    await States.answer.set()

@dp.message_handler(state=States.answer)
async def send_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(chat_to_naswer, f'Поступил ответ от администратора: "{message.text}"')
    await state.finish()
