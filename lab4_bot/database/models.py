# database/models.py
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class LessonType(enum.Enum):
    LECTURE = "Лекція"
    PRACTICE = "Практика"
    LAB = "Лабораторна"
    CONSULTATION = "Консультація"
    EXAM = "Іспит"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(255))
    join_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contacts: Mapped[Optional[str]] = mapped_column(String(255))

    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="teacher", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    lesson_type: Mapped[LessonType] = mapped_column(nullable=False)
    lesson_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    meet_link: Mapped[Optional[str]] = mapped_column(String(255))

    teacher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teachers.id"))

    teacher: Mapped[Optional["Teacher"]] = relationship("Teacher", back_populates="lessons")


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    deadline_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)