import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# LLMサービスのインポート
from services.llm_service import get_llm_service

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    conversation_id: Optional[str] = None
    max_tokens: Optional[int] = 1024
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    message: Message
    conversation_id: str
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    テキストチャット応答を生成するエンドポイント
    """
    try:
        # LLMサービスの取得（オンライン/オフラインモードに応じて切り替え）
        llm_service = get_llm_service()
        
        # LLMでの応答生成
        result = await llm_service.generate_response(
            messages=request.messages,
            conversation_id=request.conversation_id,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return ChatResponse(
            message=Message(role="assistant", content=result["text"]),
            conversation_id=result["conversation_id"],
            finish_reason=result.get("finish_reason"),
            usage=result.get("usage")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"テキスト生成エラー: {str(e)}")

@router.get("/info")
async def get_llm_info():
    """
    現在使用中のLLMサービス情報を取得
    """
    llm_service = get_llm_service()
    return {
        "service_name": llm_service.name,
        "is_local": llm_service.is_local,
        "model": llm_service.model_name
    } 