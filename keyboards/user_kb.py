from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("/start"))

b1 = KeyboardButton("Добавить лекарство")
b2 = KeyboardButton("Удалить лекарство")
b3 = KeyboardButton("Удалить все лекарства")
b4 = KeyboardButton("Включить напоминания")
b5 = KeyboardButton("Выключить напоминания")

user_kb = ReplyKeyboardMarkup(resize_keyboard=True)

user_kb.row(b1, b2).add(b3).row(b4, b5)