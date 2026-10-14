from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import quiz as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Onboarding Quiz Coach",
        "questions": await svc.list_questions(db), "attempts": await svc.list_attempts(db)})

@router.post("/ui/questions")
async def ui_q(prompt: str = Form(...), answer: str = Form(...), topic: str = Form("general"), db: AsyncSession = Depends(get_db)):
    await svc.add_question(db, prompt, answer, topic); return RedirectResponse("/", status_code=303)

@router.post("/ui/attempt")
async def ui_a(question_id: str = Form(...), response: str = Form(...), db: AsyncSession = Depends(get_db)):
    await svc.attempt(db, question_id, response); return RedirectResponse("/", status_code=303)
