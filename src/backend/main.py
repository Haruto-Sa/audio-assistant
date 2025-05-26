import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 環境変数のロード
load_dotenv()

# オンライン/オフラインモードの設定
USE_LOCAL_MODE = os.getenv("USE_LOCAL_MODE", "false").lower() == "true"

app = FastAPI(
    title="音声アシスタント API",
    description="音声アシスタントのバックエンドAPI",
    version="0.1.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限すること
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターのインポート
from api.stt import router as stt_router
from api.llm import router as llm_router
from api.tts import router as tts_router

# ルーターの登録
app.include_router(stt_router, prefix="/api/stt", tags=["STT"])
app.include_router(llm_router, prefix="/api/llm", tags=["LLM"])
app.include_router(tts_router, prefix="/api/tts", tags=["TTS"])

@app.get("/")
async def root():
    return {
        "message": "音声アシスタントAPIサーバー",
        "mode": "ローカルモード" if USE_LOCAL_MODE else "クラウドモード"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 