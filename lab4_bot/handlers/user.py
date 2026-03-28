from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database.requests as rq
from utils.formatters import format_lessons, format_tasks
from keyboards.reply import user_main_kb, user_schedule_kb, user_tasks_kb, cancel_kb

user_router = Router()

class UserStates(StatesGroup):
    waiting_for_date = State()
    waiting_for_days = State()

@user_router.message(CommandStart())
@user_router.message(F.text == "⬅️ Головне меню")
@user_router.message(F.text == "⬅️ Режим студента")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await rq.add_user(message.from_user.id, message.from_user.username)
    await message.answer("Головне меню студента 🎓", reply_markup=user_main_kb)

@user_router.message(F.text == "❌ Скасувати введення", StateFilter("*"))
async def cancel_input(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Дію скасовано.", reply_markup=user_main_kb)

@user_router.message(F.text == "📅 Розклад")
async def menu_schedule(message: Message):
    await message.answer("Оберіть період для розкладу:", reply_markup=user_schedule_kb)

@user_router.message(F.text == "⏳ Завдання")
async def menu_tasks(message: Message):
    await message.answer("Оберіть період для завдань:", reply_markup=user_tasks_kb)

@user_router.message(F.text == "👨‍🏫 Викладачі")
async def menu_teachers(message: Message):
    teachers = await rq.get_all_teachers()
    if not teachers:
        await message.answer("📭 Список викладачів порожній.")
        return
    res = "👨‍🏫 <b>Наші викладачі:</b>\n\n"
    for t in teachers:
        res += f"👤 <b>{t.full_name}</b>"
        if t.contacts: res += f" | 📞 {t.contacts}"
        res += "\n"
    await message.answer(res, parse_mode="HTML")

@user_router.message(F.text == "Сьогодні")
async def sch_today(message: Message):
    lessons = await rq.get_lessons_by_date(datetime.now().date())
    await message.answer(format_lessons(lessons), parse_mode="HTML")

@user_router.message(F.text == "Цього тижня")
async def sch_this_week(message: Message):
    lessons = await rq.get_lessons_this_week()
    await message.answer(format_lessons(lessons), parse_mode="HTML")

@user_router.message(F.text == "Наступного тижня")
async def sch_next_week(message: Message):
    lessons = await rq.get_lessons_next_week()
    await message.answer(format_lessons(lessons), parse_mode="HTML")

@user_router.message(F.text == "На конкретну дату")
async def sch_custom_date(message: Message, state: FSMContext):
    await message.answer("Введіть дату у форматі ДД.ММ.РРРР (наприклад, 15.04.2026):", reply_markup=cancel_kb)
    await state.set_state(UserStates.waiting_for_date)

@user_router.message(UserStates.waiting_for_date)
async def process_custom_date(message: Message, state: FSMContext):
    try:
        target_date = datetime.strptime(message.text, "%d.%m.%Y").date()
        lessons = await rq.get_lessons_by_date(target_date)
        await message.answer(format_lessons(lessons), parse_mode="HTML", reply_markup=user_schedule_kb)
        await state.clear()
    except ValueError:
        await message.answer("❌ Помилка формату! Введіть дату саме як ДД.ММ.РРРР:")

@user_router.message(F.text == "Всі завдання")
async def tsk_all(message: Message):
    tasks = await rq.get_all_assignments()
    await message.answer(format_tasks(tasks), parse_mode="HTML")

@user_router.message(F.text == "Менше 7 днів")
async def tsk_7_days(message: Message):
    tasks = await rq.get_upcoming_assignments(7)
    await message.answer(format_tasks(tasks), parse_mode="HTML")

@user_router.message(F.text == "На X днів")
async def tsk_x_days(message: Message, state: FSMContext):
    await message.answer("Введіть кількість днів (цифрою):", reply_markup=cancel_kb)
    await state.set_state(UserStates.waiting_for_days)

@user_router.message(UserStates.waiting_for_days)
async def process_x_days(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введіть ціле число!")
        return
    days = int(message.text)
    tasks = await rq.get_upcoming_assignments(days)
    await message.answer(format_tasks(tasks), parse_mode="HTML", reply_markup=user_tasks_kb)
    await state.clear()