from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Розклад"), KeyboardButton(text="⏳ Завдання")],
        [KeyboardButton(text="👨‍🏫 Викладачі")],
        [KeyboardButton(text="🔐 Адмін-панель")]
    ], resize_keyboard=True
)

user_schedule_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сьогодні"), KeyboardButton(text="Цього тижня")],
        [KeyboardButton(text="Наступного тижня"), KeyboardButton(text="На конкретну дату")],
        [KeyboardButton(text="⬅️ Головне меню")]
    ], resize_keyboard=True
)

user_tasks_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Всі завдання"), KeyboardButton(text="Менше 7 днів")],
        [KeyboardButton(text="На X днів")],
        [KeyboardButton(text="⬅️ Головне меню")]
    ], resize_keyboard=True
)

admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⚙️ Управління розкладом"), KeyboardButton(text="⚙️ Управління завданнями")],
        [KeyboardButton(text="⚙️ Управління викладачами")],
        [KeyboardButton(text="⬅️ Режим студента")]
    ], resize_keyboard=True
)

admin_schedule_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Додати пару"), KeyboardButton(text="📋 Всі пари"), KeyboardButton(text="❌ Видалити пару")],
    [KeyboardButton(text="⬅️ Назад до адмінки")]
], resize_keyboard=True)

admin_tasks_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Додати завдання"), KeyboardButton(text="📋 Всі завдання"), KeyboardButton(text="❌ Видалити завдання")],
    [KeyboardButton(text="⬅️ Назад до адмінки")]
], resize_keyboard=True)

admin_teachers_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Додати викладача"), KeyboardButton(text="📋 Всі викладачі"), KeyboardButton(text="❌ Видалити викладача")],
    [KeyboardButton(text="⬅️ Назад до адмінки")]
], resize_keyboard=True)

cancel_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="❌ Скасувати введення")]], resize_keyboard=True)

lesson_types_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Лекція"), KeyboardButton(text="Практика")],
    [KeyboardButton(text="Лабораторна"), KeyboardButton(text="Іспит")],
    [KeyboardButton(text="❌ Скасувати введення")]
], resize_keyboard=True)