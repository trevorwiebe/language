# app/api/content.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.gemini_service import GeminiContentGenerator
from app.database import db
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
gemini = GeminiContentGenerator(api_key=os.getenv('GEMINI_API_KEY'))

class TextSummaryRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "auto"
    level: Optional[str] = "intermediate"

class ConversationRequest(BaseModel):
    scenario: str
    target_language: str
    source_language: Optional[str] = "English"
    level: Optional[str] = "intermediate"
    num_exchanges: Optional[int] = 6

@router.post("/text-summary")
async def create_text_summary(request: Request, summary_req: TextSummaryRequest):
    """Generate text summary in target language"""
    user_id = request.state.user_id
    
    try:
        # Generate summary
        result = await gemini.generate_text_summary(
            text=summary_req.text,
            target_language=summary_req.target_language,
            source_language=summary_req.source_language,
            level=summary_req.level
        )
        
        # Save to history
        db.save_content_history(user_id, {
            "content_type": "text_summary",
            "input_text": summary_req.text[:500],  # Save first 500 chars
            "input_language": summary_req.source_language,
            "output_language": summary_req.target_language,
            "generated_content": str(result)
        })
        
        # Update user session
        db.update_user_session(user_id)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation")
async def create_conversation(request: Request, conv_req: ConversationRequest):
    """Generate a conversation for language practice"""
    user_id = request.state.user_id
    
    try:
        result = await gemini.generate_conversation(
            scenario=conv_req.scenario,
            target_language=conv_req.target_language,
            source_language=conv_req.source_language,
            level=conv_req.level,
            num_exchanges=conv_req.num_exchanges
        )
        
        # Save to history
        db.save_content_history(user_id, {
            "content_type": "conversation",
            "input_text": conv_req.scenario,
            "input_language": conv_req.source_language,
            "output_language": conv_req.target_language,
            "generated_content": str(result)
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_user_history(request: Request, limit: int = 10):
    """Get user's content generation history"""
    user_id = request.state.user_id
    history = db.get_user_history(user_id, limit)
    return {"history": history}