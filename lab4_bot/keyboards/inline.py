from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_delete_teachers_kb(teachers) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for t in teachers:
        builder.button(text=f"❌ {t.full_name}", callback_data=f"del_teacher_{t.id}")
    builder.adjust(1)
    return builder.as_markup()

def get_delete_lessons_kb(lessons) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for l in lessons:
        date_str = l.lesson_date.strftime("%d.%m %H:%M")
        builder.button(text=f"❌ {date_str} - {l.title}", callback_data=f"del_lesson_{l.id}")
    builder.adjust(1)
    return builder.as_markup()

def get_delete_assignments_kb(assignments) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for a in assignments:
        builder.button(text=f"❌ {a.title}", callback_data=f"del_task_{a.id}")
    builder.adjust(1)
    return builder.as_markup()

def get_select_teacher_kb(teachers) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for t in teachers:
        builder.button(text=t.full_name, callback_data=f"sel_teacher_{t.id}")
    builder.adjust(1)
    return builder.as_markup()