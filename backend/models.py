from __future__ import annotations
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from backend.db import Base
def utcnow(): return datetime.utcnow()
class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    prompt: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(String(200))
    topic: Mapped[str] = mapped_column(String(80), default="general")
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    question_id: Mapped[str] = mapped_column(String(32), index=True)
    response: Mapped[str] = mapped_column(String(200))
    correct: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    coaching: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
