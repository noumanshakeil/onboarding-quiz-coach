from __future__ import annotations
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import QuizAttempt, QuizQuestion

async def add_question(session: AsyncSession, prompt: str, answer: str, topic: str = "general") -> QuizQuestion:
    q = QuizQuestion(id=uuid.uuid4().hex[:10], prompt=prompt.strip(), answer=answer.strip()[:200], topic=topic[:80])
    session.add(q); await session.commit(); await session.refresh(q); return q

async def list_questions(session: AsyncSession) -> list[QuizQuestion]:
    return list((await session.execute(select(QuizQuestion))).scalars())

async def attempt(session: AsyncSession, question_id: str, response: str) -> QuizAttempt:
    q = await session.get(QuizQuestion, question_id)
    if not q: raise ValueError("not found")
    correct = response.strip().lower() == q.answer.strip().lower()
    coaching = ""
    if not correct:
        llm = get_llm()
        coaching = await llm.complete(
            f"Learner answered '{response}' to '{q.prompt}'. Correct is '{q.answer}'. Coach briefly.",
            system="Onboarding coach. Kind and specific.",
        )
    row = QuizAttempt(id=uuid.uuid4().hex[:10], question_id=question_id, response=response.strip()[:200],
                      correct=correct, score=1.0 if correct else 0.0, coaching=coaching)
    session.add(row); await session.commit(); await session.refresh(row); return row

async def list_attempts(session: AsyncSession) -> list[QuizAttempt]:
    return list((await session.execute(select(QuizAttempt).order_by(QuizAttempt.created_at.desc()).limit(50))).scalars())
