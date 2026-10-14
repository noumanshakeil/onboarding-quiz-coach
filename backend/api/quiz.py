from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import quiz as svc

class QuestionIn(BaseModel):
    prompt: str = Field(min_length=3)
    answer: str = Field(min_length=1)
    topic: str = "general"
class AttemptIn(BaseModel):
    response: str = Field(min_length=1)

router = APIRouter()

@router.get("/questions")
async def questions(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_questions(db)
    return {"questions": [{"id": q.id, "prompt": q.prompt, "topic": q.topic} for q in rows]}

@router.post("/questions")
async def create(payload: QuestionIn, db: AsyncSession = Depends(get_db)):
    q = await svc.add_question(db, payload.prompt, payload.answer, payload.topic); return {"id": q.id}

@router.post("/questions/{question_id}/attempt")
async def attempt(question_id: str, payload: AttemptIn, db: AsyncSession = Depends(get_db)):
    try:
        a = await svc.attempt(db, question_id, payload.response)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return {"id": a.id, "correct": a.correct, "score": a.score, "coaching": a.coaching}

@router.get("/attempts")
async def attempts(db: AsyncSession = Depends(get_db)):
    rows = await svc.list_attempts(db)
    return {"attempts": [{"id": a.id, "correct": a.correct, "score": a.score} for a in rows]}
