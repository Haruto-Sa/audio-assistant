import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import io

# STTサービスのインポート
from services.stt_service import get_stt_service

router = APIRouter()

class TranscriptionResponse(BaseModel):
    text: str
    confidence: Optional[float] = None

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = "ja"
):
    """
    音声ファイルをテキストに変換するエンドポイント
    """
    try:
        # 音声データの読み込み
        audio_data = await file.read()
        
        # STTサービスの取得（オンライン/オフラインモードに応じて切り替え）
        stt_service = get_stt_service()
        
        # 音声からテキストへの変換
        result = await stt_service.transcribe(io.BytesIO(audio_data), language)
        
        return TranscriptionResponse(
            text=result["text"],
            confidence=result.get("confidence")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音声認識エラー: {str(e)}")

@router.get("/info")
async def get_stt_info():
    """
    現在使用中のSTTサービス情報を取得
    """
    stt_service = get_stt_service()
    return {
        "service_name": stt_service.name,
        "is_local": stt_service.is_local,
        "supported_languages": stt_service.supported_languages
    } 