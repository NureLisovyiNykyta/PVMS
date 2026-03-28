from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database.requests as rq
from config import ADMIN_ID
from database.models import LessonType
from keyboards.reply import (admin_main_kb, admin_schedule_kb, admin_tasks_kb,
                             admin_teachers_kb, cancel_kb, lesson_types_kb)
from keyboards.inline import (get_delete_teachers_kb, get_delete_lessons_kb,
                              get_delete_assignments_kb, get_select_teacher_kb)

admin_router = Router()


class IsAdmin(Filter):
    async def __call__(self, message: Message | CallbackQuery) -> bool:
        return message.from_user.id == ADMIN_ID


class AddTeacher(StatesGroup):
    name = State()
    contacts = State()


class AddTask(StatesGroup):
    title = State()
    desc = State()
    date = State()


class AddLesson(StatesGroup):
    title = State()
    type = State()
    date = State()
    teacher = State()
    link = State()


@admin_router.message(F.text == "🔐 Адмін-панель", IsAdmin())
@admin_router.message(F.text == "⬅️ Назад до адмінки", IsAdmin())
async def admin_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ви в панелі адміністратора 🛠", reply_markup=admin_main_kb)


@admin_router.message(F.text == "❌ Скасувати введення", StateFilter("*"), IsAdmin())
async def cancel_admin_fsm(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
    await message.answer("Дію скасовано ❌", reply_markup=admin_main_kb)


@admin_router.message(F.text == "⚙️ Управління розкладом", IsAdmin())
async def adm_sch(m: Message): await m.answer("Управління розкладом:", reply_markup=admin_schedule_kb)


@admin_router.message(F.text == "⚙️ Управління завданнями", IsAdmin())
async def adm_tsk(m: Message): await m.answer("Управління завданнями:", reply_markup=admin_tasks_kb)


@admin_router.message(F.text == "⚙️ Управління викладачами", IsAdmin())
async def adm_tch(m: Message): await m.answer("Управління викладачами:", reply_markup=admin_teachers_kb)


@admin_router.message(F.text == "➕ Додати викладача", IsAdmin())
async def add_tch_1(m: Message, state: FSMContext):
    await m.answer("Введіть ПІБ викладача (наприклад: Іванов І.І.):", reply_markup=cancel_kb)
    await state.set_state(AddTeacher.name)


@admin_router.message(AddTeacher.name, IsAdmin())
async def add_tch_2(m: Message, state: FSMContext):
    await state.update_data(name=m.text)
    await m.answer("Введіть контакти (email, telegram) або напишіть '-':")
    await state.set_state(AddTeacher.contacts)


@admin_router.message(AddTeacher.contacts, IsAdmin())
async def add_tch_3(m: Message, state: FSMContext):
    contacts = None if m.text == "-" else m.text
    data = await state.get_data()

    await rq.add_teacher(full_name=data['name'], contacts=contacts)

    await state.clear()
    await m.answer(f"✅ Викладача <b>{data['name']}</b> успішно додано!", parse_mode="HTML",
                   reply_markup=admin_teachers_kb)


@admin_router.message(F.text == "➕ Додати завдання", IsAdmin())
async def add_tsk_1(m: Message, state: FSMContext):
    await m.answer("Введіть назву завдання:", reply_markup=cancel_kb)
    await state.set_state(AddTask.title)


@admin_router.message(AddTask.title, IsAdmin())
async def add_tsk_2(m: Message, state: FSMContext):
    await state.update_data(title=m.text)
    await m.answer("Введіть опис (або напишіть '-'):")
    await state.set_state(AddTask.desc)


@admin_router.message(AddTask.desc, IsAdmin())
async def add_tsk_3(m: Message, state: FSMContext):
    desc = None if m.text == "-" else m.text
    await state.update_data(desc=desc)
    await m.answer("Введіть дедлайн у форматі ДД.ММ.РРРР:")
    await state.set_state(AddTask.date)


@admin_router.message(AddTask.date, IsAdmin())
async def add_tsk_4(m: Message, state: FSMContext):
    try:
        d_date = datetime.strptime(m.text, "%d.%m.%Y")
        data = await state.get_data()
        await rq.add_assignment(data['title'], data['desc'], d_date)
        await state.clear()
        await m.answer("✅ Завдання успішно додано!", reply_markup=admin_tasks_kb)
    except ValueError:
        await m.answer("❌ Невірний формат! Введіть дату як ДД.ММ.РРРР:")


@admin_router.message(F.text == "➕ Додати пару", IsAdmin())
async def add_les_1(m: Message, state: FSMContext):
    await m.answer("Введіть назву заняття:", reply_markup=cancel_kb)
    await state.set_state(AddLesson.title)


@admin_router.message(AddLesson.title, IsAdmin())
async def add_les_2(m: Message, state: FSMContext):
    await state.update_data(title=m.text)
    await m.answer("Оберіть тип заняття:", reply_markup=lesson_types_kb)
    await state.set_state(AddLesson.type)


@admin_router.message(AddLesson.type, IsAdmin())
async def add_les_3(m: Message, state: FSMContext):
    try:
        l_type = LessonType(m.text)
        await state.update_data(type=l_type)
        await m.answer("Введіть дату та час (ДД.ММ.РРРР ГГ:ХХ):", reply_markup=cancel_kb)
        await state.set_state(AddLesson.date)
    except ValueError:
        await m.answer("❌ Оберіть тип заняття з клавіатури!")


@admin_router.message(AddLesson.date, IsAdmin())
async def add_les_4(m: Message, state: FSMContext):
    try:
        l_date = datetime.strptime(m.text, "%d.%m.%Y %H:%M")
        await state.update_data(date=l_date)

        teachers = await rq.get_all_teachers()
        if not teachers:
            await m.answer("⚠️ Спочатку додайте хоча б одного викладача в базу!")
            await state.clear()
            return

        await m.answer("Оберіть викладача:", reply_markup=get_select_teacher_kb(teachers))
        await state.set_state(AddLesson.teacher)
    except ValueError:
        await m.answer("❌ Помилка! Введіть у форматі: 15.04.2026 10:00")


@admin_router.callback_query(AddLesson.teacher, F.data.startswith("sel_teacher_"))
async def add_les_5(call: CallbackQuery, state: FSMContext):
    t_id = int(call.data.split("_")[2])
    await state.update_data(teacher=t_id)
    await call.message.delete()
    await call.message.answer("Введіть посилання на Meet/Zoom (або '-'):")
    await state.set_state(AddLesson.link)


@admin_router.message(AddLesson.link, IsAdmin())
async def add_les_6(m: Message, state: FSMContext):
    link = None if m.text == "-" else m.text
    data = await state.get_data()

    await rq.add_lesson(
        title=data['title'], lesson_type=data['type'],
        lesson_date=data['date'], teacher_id=data['teacher'], meet_link=link
    )
    await state.clear()
    await m.answer("✅ Пару успішно додано у розклад!", reply_markup=admin_schedule_kb)


@admin_router.message(F.text == "❌ Видалити викладача", IsAdmin())
async def del_tch_menu(m: Message):
    t = await rq.get_all_teachers()
    if not t: return await m.answer("Список порожній.")
    await m.answer("Натисніть на викладача для видалення:", reply_markup=get_delete_teachers_kb(t))


@admin_router.callback_query(F.data.startswith("del_teacher_"), IsAdmin())
async def del_tch_cb(call: CallbackQuery):
    t_id = int(call.data.split("_")[2])
    await rq.delete_teacher(t_id)
    await call.message.edit_text("✅ Викладача видалено!")


@admin_router.message(F.text == "❌ Видалити пару", IsAdmin())
async def del_les_menu(m: Message):
    l = await rq.get_all_lessons()
    if not l: return await m.answer("Список порожній.")
    await m.answer("Натисніть на пару для видалення:", reply_markup=get_delete_lessons_kb(l))


@admin_router.callback_query(F.data.startswith("del_lesson_"), IsAdmin())
async def del_les_cb(call: CallbackQuery):
    l_id = int(call.data.split("_")[2])
    await rq.delete_lesson(l_id)
    await call.message.edit_text("✅ Пару видалено!")


@admin_router.message(F.text == "❌ Видалити завдання", IsAdmin())
async def del_tsk_menu(m: Message):
    t = await rq.get_all_assignments()
    if not t: return await m.answer("Список порожній.")
    await m.answer("Натисніть на завдання для видалення:", reply_markup=get_delete_assignments_kb(t))


@admin_router.callback_query(F.data.startswith("del_task_"), IsAdmin())
async def del_tsk_cb(call: CallbackQuery):
    t_id = int(call.data.split("_")[2])
    await rq.delete_assignment(t_id)
    await call.message.edit_text("✅ Завдання видалено!")


@admin_router.message(F.text == "📋 Всі викладачі", IsAdmin())
async def show_all_teachers_admin(message: Message):
    teachers = await rq.get_all_teachers()
    if not teachers:
        return await message.answer("📭 Список викладачів порожній.")

    res = "👨‍🏫 <b>Список усіх викладачів у базі:</b>\n\n"
    for t in teachers:
        res += f"▫️ <b>{t.full_name}</b>"
        if t.contacts:
            res += f" | 📞 {t.contacts}"
        res += "\n"

    await message.answer(res, parse_mode="HTML")


@admin_router.message(F.text == "📊 Статистика", IsAdmin())
async def show_stats(message: Message):
    stats = await rq.get_detailed_stats()

    res = (
        f"📈 <b>Детальна статистика бота:</b>\n\n"
        f"👥 Всього підписників: <b>{stats['total']}</b>\n"
        f"🔥 Приєдналося сьогодні: <b>{stats['today']}</b>\n\n"
        f"🆕 <b>Останні 5 підписників:</b>\n"
    )

    if not stats['latest']:
        res += "📭 Немає даних."
    else:
        for u in stats['latest']:
            name = f"@{u.username}" if u.username else f"ID: {u.telegram_id}"
            date_str = u.join_date.strftime('%d.%m %H:%M')
            res += f"▫️ {name} <i>({date_str})</i>\n"

    await message.answer(res, parse_mode="HTML")


@admin_router.message(F.text == "📋 Всі пари", IsAdmin())
async def show_all_lessons_admin(message: Message):
    lessons = await rq.get_all_lessons()
    if not lessons:
        return await message.answer("📭 Розклад порожній.")

    res = "📅 <b>Всі заплановані пари:</b>\n\n"
    for l in lessons:
        t_name = l.teacher.full_name if l.teacher else "Не вказано"
        res += f"🔹 <b>{l.lesson_date.strftime('%d.%m.%Y %H:%M')}</b> | {l.lesson_type.value}\n"
        res += f"📚 <b>{l.title}</b> (Викл: {t_name})\n"
        if l.meet_link:
            res += f"🔗 {l.meet_link}\n"
        res += "\n"

    await message.answer(res, parse_mode="HTML", disable_web_page_preview=True)


@admin_router.message(F.text == "📋 Всі завдання", IsAdmin())
async def show_all_tasks_admin(message: Message):
    tasks = await rq.get_all_assignments()
    if not tasks:
        return await message.answer("📭 Список завдань порожній.")

    res = "⏳ <b>Всі активні завдання:</b>\n\n"
    for t in tasks:
        res += f"📌 <b>{t.title}</b> (Дедлайн: {t.deadline_date.strftime('%d.%m.%Y')})\n"
        if t.description:
            res += f"📝 <i>{t.description}</i>\n"
        res += "\n"

    await message.answer(res, parse_mode="HTML")