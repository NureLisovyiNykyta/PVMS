def format_lessons(lessons) -> str:
    if not lessons:
        return "📭 На цей період пар немає."
    res = ""
    for l in lessons:
        t_name = l.teacher.full_name if l.teacher else "Не вказано"
        res += f"🔹 <b>{l.lesson_date.strftime('%d.%m.%Y %H:%M')}</b> | {l.lesson_type.value}\n"
        res += f"📚 <b>{l.title}</b> (Викл: {t_name})\n"
        if l.meet_link: res += f"🔗 Посилання: {l.meet_link}\n"
        res += "\n"
    return res

def format_tasks(tasks) -> str:
    if not tasks:
        return "📭 Завдань немає. Можна відпочивати!"
    res = ""
    for t in tasks:
        res += f"📌 <b>{t.title}</b> (Дедлайн: {t.deadline_date.strftime('%d.%m.%Y')})\n"
        if t.description: res += f"📝 <i>{t.description}</i>\n"
        res += "\n"
    return res