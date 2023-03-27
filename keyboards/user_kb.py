from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("/start"))

b1 = KeyboardButton("Добавить лекарство")
b2 = KeyboardButton("Удалить лекарство")
b3 = KeyboardButton("Удалить все лекарства")
b4 = KeyboardButton("Включить напоминания")
b5 = KeyboardButton("Выключить напоминания")
b6 = KeyboardButton("Посмотреть лекарства")

user_kb = ReplyKeyboardMarkup(resize_keyboard=True)

user_kb.row(b1, b6).row(b2, b3).row(b4, b5)
# Когда принимаем? (до, во время или после пищи, вне зависимости от приема)\nДо - 0\nВо время - 1\nПосле - 2\nВне зависимости - 3"
ib1 = InlineKeyboardButton("До", callback_data="0")
ib2 = InlineKeyboardButton("Во время", callback_data="1")
ib3 = InlineKeyboardButton("После", callback_data="2")
ib4 = InlineKeyboardButton("Вне зависимости", callback_data="3")
time_kb = InlineKeyboardMarkup().add(ib1).add(ib2).add(ib3).add(ib4)