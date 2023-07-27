from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config


storage = MemoryStorage()
bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

class States(StatesGroup):
    otzyv_begin = State()
    otzyv_end = State()
    zhaloba_begin = State()
    zhaloba_end = State()

@dp.message_handler(commands=['start'])
async def start_ch(message: types.Message):
    buttons = [
        InlineKeyboardButton(text='Отзывы', callback_data='otzyvy'),
        InlineKeyboardButton(text='Жалобы', callback_data='zhaloby')
    ]
    kb = InlineKeyboardMarkup()
    kb.add(*buttons)
    await message.answer('Здравствуйте! (ТЕКСТ 2)', reply_markup=kb)

@dp.callback_query_handler(text='otzyvy')
async def otz_ch(callback: types.CallbackQuery):
    await callback.message.answer('Отправьте мне, пожалуйста, ваш отзыв.')
    await States.otzyv_begin.set()

@dp.message_handler(state=States.otzyv_begin)
async def otzyv_begin(message: types.Message, state: FSMContext):
    await state.update_data(otzyv=message.text)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text='ОТправить отзыв', callback_data='so'))
    await message.answer('Я получил ваш отзыв, подтвердите его отправку.', reply_markup=kb)
    await States.otzyv_end.set()

@dp.callback_query_handler(text='so', state=States.otzyv_end)
async def so_ch(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.answer('Спасибо за ваш отзыв, отправлен в обработку.')
    await callback.message.answer(data['otzyv'])
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
    await callback.message.answer(data['zhaloba'])
    await state.finish()
