import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from tgbot.creation_bot import bot
from tgbot.keyboards import user_kb, time_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import db_requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.scheduler import scheduler

enum = ["до", "во время", "после", "вне зависимости от"]


class FSMadd(StatesGroup):
    name = State()
    number_of_receptions = State()
    time_of_reception = State()  # время приема (в зависимости от пищи, до, во время или после нее) 0-3
    times = State()


async def start(message: types.Message):
    """
    Функция приветсвия в боте
    """

    await message.answer("Приветствую. Этот бот поможет не забывать выпивать таблетки в нужное время.",
                         reply_markup=user_kb)


async def add_medicine_start(message: types.Message):
    """
    Функция добавления лекартсва
    """

    await FSMadd.name.set()
    await message.answer("Напиши название лекарства")


#
async def cancel_handler(message: types.Message, state: FSMContext):
    """
        Выход из состояния машины
    """

    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer("Ok")


async def name_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMadd.next()
    await message.answer("Сколько раз в день будем принимать?")


async def number_of_receptions_add(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['number'] = int(message.text)
    except ValueError as e:
        await message.answer("Допущена ошибка. Попробуйте снова")
        return
    await FSMadd.next()
    await message.answer(
        "Когда принимаем?",
        reply_markup=time_kb)  # (до, во время или после пищи, вне зависимости от приема)\nДо - 0\nВо время - 1\nПосле - 2\nВне зависимости - 3


async def time_of_reception_add_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['time'] = int(callback.data)
    except ValueError as e:
        await callback.answer("Допущена ошибка. Попробуйте снова")
        return
    await FSMadd.next()
    await bot.send_message(callback.from_user.id,
                           text="Во сколько будем принимать лекарста? Ответь в формате: 12:00, 15:30, 19:40 и тд")


async def times_add(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['times'] = list(datetime.datetime.strptime(t, '%H:%M').time() for t in message.text.split(", "))
        except ValueError as e:
            await message.answer("Допущена ошибка. Попробуйте снова")
            return
        if len(data['times']) != data['number']:
            await message.answer("Время приемов должно совпадать с их количеством")
            return
        data['user_id'] = message.from_user.id
    async with state.proxy() as data:
        m_id = await db_requests.db_add(state)
        for t in data['times']:
            scheduler.add_job(notification, 'cron', id=f"{m_id}:{message.from_user.id}:{str(t)}",
                              args=(message.from_user.id, data["name"], data["time"]), hour=t.hour,
                              minute=t.minute)
    await state.finish()
    await message.answer("Успешно добавлено")


async def view_all(message: types.Message):
    result = await db_requests.db_read(message.from_user.id)
    result = result.all()
    if not result:
        await message.answer("Лекарств нет")
        return
    for row in result:
        times = " ".join([time.reception_time.strftime("%H:%M") for time in row.Medicine.times])
        await message.answer(f"{row.Medicine.name}\nПрием: {row.Medicine.number_of_receptions} раз(а) в день {enum[row.Medicine.time_of_reception]} еды.\nВ {times}")


async def delete_item(message: types.Message):
    result = await db_requests.db_read(message.from_user.id)
    result = result.all()
    if not result:
        await message.answer("Лекарств нет")
        return
    for row in result:
        await bot.send_message(message.from_user.id, text=f"{row.Medicine.name}\nПрием: {row.Medicine.number_of_receptions} раз(а) в день",
                               reply_markup=InlineKeyboardMarkup(). \
                               add(InlineKeyboardButton(f"Удалить", callback_data=f"del {row[0]}")))


async def delete_item_callback(callback: types.CallbackQuery):
    m_id = callback.data.replace("del ", "")
    await db_requests.db_del(int(m_id))
    jobs_to_del = [job.id for job in scheduler.get_jobs() if job.id.split(":")[0] == m_id]
    for job in jobs_to_del:
        scheduler.remove_job(job)
    del jobs_to_del
    await callback.answer(text="Лекарство удалено", show_alert=True)


async def delete_all(message: types.Message):
    await db_requests.deb_del_all(message.from_user.id)
    await delete_jobs(message.from_user.id)
    await message.answer("Все лекарства удалены")


async def delete_jobs(user_id: str):
    jobs_to_del = [job.id for job in scheduler.get_jobs() if job.id.split(":")[1] == str(user_id)]
    for job in jobs_to_del:
        scheduler.remove_job(job)
    del jobs_to_del


async def turn_on_notifications(message: types.Message):
    result = await db_requests.db_edit_notify(user_id=message.from_user.id, flag=True)
    if not result:
        await message.answer("Уведомления уже включены")
        return
    else:
        result = await db_requests.db_read(user_id=None)
        for row in result.all():
            t: datetime.time = row[4]
            scheduler.add_job(notification, 'cron', id=f"{row[0]}:{row[1]}:{str(t)}", args=(row[1], row[2], row[3]),
                              hour=t.hour, minute=t.minute)
        await message.answer("Уведомления включены")


async def turn_off_notifications(message: types.Message):
    await db_requests.db_edit_notify(user_id=message.from_user.id, flag=False)
    await delete_jobs(message.from_user.id)
    await message.answer("Все уведомления отключены")


async def schedule():
    scheduler.remove_all_jobs()
    result = await db_requests.db_read(user_id=None)
    for row in result.all():
        t: datetime.time = row[4]
        scheduler.add_job(notification, 'cron', id=f"{row[0]}:{row[1]}:{str(t)}", args=(row[1], row[2], row[3]),
                          hour=t.hour, minute=t.minute)


async def notification(user_id, medicine_name, reception_time):
    await bot.send_message(user_id, text=f"Пора принимать {medicine_name}.\nПрием {enum[reception_time]} еды.")


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(start, Text(equals="start"))
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(add_medicine_start, Text(equals="Добавить лекарство"), state=None)
    dp.register_message_handler(cancel_handler, Text(equals="Отмена"), state="*")
    dp.register_message_handler(name_add, state=FSMadd.name)
    dp.register_message_handler(number_of_receptions_add, state=FSMadd.number_of_receptions)
    dp.register_callback_query_handler(time_of_reception_add_callback, lambda n: n.data in "0123",
                                       state=FSMadd.time_of_reception)
    dp.register_message_handler(times_add, state=FSMadd.times)
    dp.register_message_handler(delete_item, Text(equals="Удалить лекарство"))
    dp.register_message_handler(delete_all, Text(equals="Удалить все лекарства"))
    dp.register_callback_query_handler(delete_item_callback, Text(startswith="del "))
    dp.register_message_handler(turn_on_notifications, Text(equals="Включить напоминания"))
    dp.register_message_handler(turn_off_notifications, Text(equals="Выключить напоминания"))
    dp.register_message_handler(view_all, Text(equals="Посмотреть лекарства"))
