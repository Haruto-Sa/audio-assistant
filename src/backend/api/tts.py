import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io

# TTSサービスのインポート
from services.tts_service import get_tts_service

router = APIRouter()

class SpeechRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "default"
    language: Optional[str] = "ja"
    speed: Optional[float] = 1.0

@router.post("/synthesize")
async def synthesize_speech(request: SpeechRequest):
    """
    テキストを音声に変換するエンドポイント
    """
    try:
        # TTSサービスの取得（オンライン/オフラインモードに応じて切り替え）
        tts_service = get_tts_service()
        
        # テキストから音声への変換
        audio_data = await tts_service.synthesize(
            text=request.text,
            voice_id=request.voice_id,
            language=request.language,
            speed=request.speed
        )
        
        # バイナリデータとして音声を返す
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/wav"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音声合成エラー: {str(e)}")

@router.get("/voices")
async def list_voices(language: Optional[str] = None):
    """
    利用可能な音声一覧を取得
    """
    tts_service = get_tts_service()
    voices = await tts_service.list_voices(language)
    return {"voices": voices}

@router.get("/info")
async def get_tts_info():
    """
    現在使用中のTTSサービス情報を取得
    """
    tts_service = get_tts_service()
    return {
        "service_name": tts_service.name,
        "is_local": tts_service.is_local,
        "supported_languages": tts_service.supported_languages
    } 