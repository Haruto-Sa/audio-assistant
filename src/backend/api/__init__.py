# API モジュール初期化
from fastapi import APIRouter

# ルーターのインポート
from .stt import router as stt_router
from .llm import router as llm_router
from .tts import router as tts_router

# メインルーター
api_router = APIRouter()

# サブルーターを登録
api_router.include_router(stt_router, prefix="/stt", tags=["STT"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])
api_router.include_router(tts_router, prefix="/tts", tags=["TTS"]) 