from datetime import datetime, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from database.engine import async_session
from database.models import User, Teacher, Lesson, Assignment


# ==========================================
# Users
# ==========================================

async def add_user(telegram_id: int, username: str = None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if not user:
            new_user = User(telegram_id=telegram_id, username=username)
            session.add(new_user)
            await session.commit()


async def get_users_count() -> int:
    async with async_session() as session:
        result = await session.scalar(select(func.count(User.id)))
        return result or 0


async def get_detailed_stats():
    today = datetime.now().date()
    start_of_today = datetime.combine(today, datetime.min.time())

    async with async_session() as session:
        total_users = await session.scalar(select(func.count(User.id)))

        users_today = await session.scalar(
            select(func.count(User.id)).where(User.join_date >= start_of_today)
        )

        latest_users_query = select(User).order_by(User.join_date.desc()).limit(5)
        latest_users = await session.scalars(latest_users_query)

        return {
            "total": total_users or 0,
            "today": users_today or 0,
            "latest": latest_users.all()
        }


# ==========================================
# Teacher
# ==========================================

async def add_teacher(full_name: str, contacts: str = None):
    async with async_session() as session:
        session.add(Teacher(full_name=full_name, contacts=contacts))
        await session.commit()


async def get_all_teachers():
    async with async_session() as session:
        result = await session.scalars(select(Teacher))
        return result.all()


async def delete_teacher(teacher_id: int):
    async with async_session() as session:
        teacher = await session.get(Teacher, teacher_id)
        if teacher:
            await session.delete(teacher)
            await session.commit()


# ==========================================
# Lessons
# ==========================================

async def add_lesson(title: str, lesson_type, lesson_date: datetime, teacher_id: int, meet_link: str = None):
    async with async_session() as session:
        new_lesson = Lesson(
            title=title,
            lesson_type=lesson_type,
            lesson_date=lesson_date,
            teacher_id=teacher_id,
            meet_link=meet_link
        )
        session.add(new_lesson)
        await session.commit()


async def get_all_lessons():
    async with async_session() as session:
        query = select(Lesson).options(joinedload(Lesson.teacher)).order_by(Lesson.lesson_date)
        result = await session.scalars(query)
        return result.all()


async def get_lessons_by_date(target_date: datetime.date):
    start_of_day = datetime.combine(target_date, datetime.min.time())
    end_of_day = datetime.combine(target_date, datetime.max.time())

    async with async_session() as session:
        query = select(Lesson).options(joinedload(Lesson.teacher)) \
            .where(Lesson.lesson_date >= start_of_day, Lesson.lesson_date <= end_of_day) \
            .order_by(Lesson.lesson_date)
        result = await session.scalars(query)
        return result.all()


async def get_lessons_this_week():
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    start_of_week = datetime.combine(monday, datetime.min.time())
    end_of_week = datetime.combine(sunday, datetime.max.time())

    async with async_session() as session:
        query = select(Lesson).options(joinedload(Lesson.teacher)) \
            .where(Lesson.lesson_date >= start_of_week, Lesson.lesson_date <= end_of_week) \
            .order_by(Lesson.lesson_date)
        result = await session.scalars(query)
        return result.all()


async def get_lessons_next_week():
    today = datetime.now().date()
    next_monday = today - timedelta(days=today.weekday()) + timedelta(days=7)
    next_sunday = next_monday + timedelta(days=6)

    start_of_week = datetime.combine(next_monday, datetime.min.time())
    end_of_week = datetime.combine(next_sunday, datetime.max.time())

    async with async_session() as session:
        query = select(Lesson).options(joinedload(Lesson.teacher)) \
            .where(Lesson.lesson_date >= start_of_week, Lesson.lesson_date <= end_of_week) \
            .order_by(Lesson.lesson_date)
        result = await session.scalars(query)
        return result.all()


async def delete_lesson(lesson_id: int):
    async with async_session() as session:
        lesson = await session.get(Lesson, lesson_id)
        if lesson:
            await session.delete(lesson)
            await session.commit()


# ==========================================
# Assignments
# ==========================================

async def add_assignment(title: str, description: str, deadline_date: datetime):
    async with async_session() as session:
        new_assignment = Assignment(title=title, description=description, deadline_date=deadline_date)
        session.add(new_assignment)
        await session.commit()


async def get_all_assignments():
    now = datetime.now()
    async with async_session() as session:
        query = select(Assignment).where(Assignment.deadline_date >= now).order_by(Assignment.deadline_date)
        result = await session.scalars(query)
        return result.all()


async def get_upcoming_assignments(days: int = 3):
    now = datetime.now()
    future_date = now + timedelta(days=days)

    async with async_session() as session:
        query = select(Assignment) \
            .where(Assignment.deadline_date >= now, Assignment.deadline_date <= future_date) \
            .order_by(Assignment.deadline_date)
        result = await session.scalars(query)
        return result.all()


async def delete_assignment(assignment_id: int):
    async with async_session() as session:
        assignment = await session.get(Assignment, assignment_id)
        if assignment:
            await session.delete(assignment)
            await session.commit()