import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.filters import CommandStart, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import BaseFilter
import basedata
from environ import bot_id


logging.basicConfig(level=logging.INFO)
bot_token = bot_id
bot = Bot(token=bot_token)
dp = Dispatcher()

basedata.connet()


@dp.message(CommandStart())
async def start(message: types.Message):
    button_help = types.KeyboardButton(text='Помощь')
    button_calendar = types.KeyboardButton(text='Функционал')
    keyboard = [[button_help, button_calendar]]
    keyboard_ready = types.reply_keyboard_markup.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text='Привет, Это бот для создания напоминаний!', reply_markup=keyboard_ready)


@dp.message(F.text == 'Помощь')
async def helping(message: types.Message):
    await message.answer('Сам ищи список комманд, мне лень')


@dp.message(F.text == 'Функционал')
async def go(message: types.Message):
    button_add_napominanie = types.KeyboardButton(text='Добавить напомнание')
    button_all_napominaniya = types.KeyboardButton(text='Глянуть все напоминания')
    button_delete_napominanie = types.KeyboardButton(text='Удалить напоминание')
    keyboard = [
        [button_add_napominanie],
        [button_all_napominaniya],
        [button_delete_napominanie]
    ]
    keyboard_ready = types.reply_keyboard_markup.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text='Пока только так умею!', reply_markup=keyboard_ready)


@dp.message(F.text == 'Добавить напомнание')
async def cmd_add(message: types.Message):
    await message.answer(text='Напиши мне дату в формате День:Месяц:Описание!\nК примеру,  24:Декабря:Святой день')


class Napominanie(BaseFilter):
    async def __call__(self, message: types.Message):
        divide = message.text.split(':')
        return len(divide) == 3 and divide[0].isdigit()


@dp.message(Napominanie())
async def cmd_real_add(message: types.Message):
    basedata.add_bd(message)
    await message.answer('Записал!')


@dp.message(F.text == 'Глянуть все напоминания')
async def cmd_show(message: types.Message):
    results = basedata.show_all_bd(message)
    if results:
        for num in results:
            await message.answer(f'{num}: {results[num]}')
    else:
        await message.answer('Пустовато тут')


@dp.message(F.text == 'Удалить напоминание')
async def cmd_show(message: types.Message):
    await message.answer(text='Просто выведи все напоминания и напиши цифру ненужного!')


@dp.message(F.text.isdigit())
async def cmd_delete(message: types.Message):
    if basedata.delete_bd(message):
        await message.answer(text='готово!')
    else:
        await message.answer(text='Не ломай бота!')


@dp.message()
async def cmd_other(message: types.Message):
    await message.answer(text='Не понял что ты написал!')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
