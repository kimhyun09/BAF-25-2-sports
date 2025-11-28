from fastapi import APIRouter, HTTPException
import logging
from app.modules.bot.schemas import ChatRequest, ChatResponse
from app.modules.bot.service import process_bot_message

router = APIRouter(prefix="/chatbot", tags=["Bot"])
logger = logging.getLogger(__name__)

@router.post("/message", response_model=ChatResponse)
def chatbot_message(req: ChatRequest):
    try:
        answer = process_bot_message(req)
        return ChatResponse(answer=answer)
    except Exception as e:
        logger.exception("Error in /chatbot/message")
        raise HTTPException(status_code=500, detail=str(e))