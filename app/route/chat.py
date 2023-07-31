from fastapi import APIRouter

from app.core.handler_chat_adv import ask_questions

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/ask")
async def route_user_all(prompt: str):
    return ask_questions(prompt)
