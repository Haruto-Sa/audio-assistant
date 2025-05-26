import os
import abc
from typing import Dict, Any, BinaryIO, List, Optional
import io

# オンライン/オフラインモードの設定を取得
USE_LOCAL_MODE = os.getenv("USE_LOCAL_MODE", "false").lower() == "true"

class BaseSTTService(abc.ABC):
    """
    音声認識サービスの基底クラス
    """
    def __init__(self):
        self.name = "BaseSTTService"
        self.is_local = True
        self.supported_languages = ["ja"]
        
    @abc.abstractmethod
    async def transcribe(self, audio_data: BinaryIO, language: str = "ja") -> Dict[str, Any]:
        """
        音声をテキストに変換する
        
        Parameters:
        -----------
        audio_data : BinaryIO
            音声データ
        language : str, optional
            言語コード (デフォルト: "ja")
            
        Returns:
        --------
        Dict[str, Any]
            {"text": 変換されたテキスト, "confidence": 信頼度}
        """
        pass

class LocalWhisperService(BaseSTTService):
    """
    ローカルのWhisperモデルを使用した音声認識サービス
    """
    def __init__(self, model_name: str = "base"):
        super().__init__()
        self.name = f"LocalWhisper-{model_name}"
        self.model_name = model_name
        self.is_local = True
        
        # ここでWhisperモデルをロードする
        # import whisper
        # self.model = whisper.load_model(model_name)
        
    async def transcribe(self, audio_data: BinaryIO, language: str = "ja") -> Dict[str, Any]:
        """
        Whisperを使用して音声をテキストに変換する
        """
        # 実際の実装では、Whisperを使って音声認識を行う
        # result = self.model.transcribe(audio_data, language=language)
        
        # デモ実装
        return {
            "text": "これはローカルWhisperによる音声認識のデモ出力です。",
            "confidence": 0.95
        }

class CloudSTTService(BaseSTTService):
    """
    クラウドAPIを使用した音声認識サービス
    """
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.name = "CloudSTT"
        self.is_local = False
        self.supported_languages = ["ja", "en", "zh", "ko"]
        
        # APIキーを設定
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    async def transcribe(self, audio_data: BinaryIO, language: str = "ja") -> Dict[str, Any]:
        """
        OpenAI Whisper APIを使用して音声をテキストに変換する
        """
        # 実際の実装では、OpenAI APIを呼び出す
        # import openai
        # openai.api_key = self.api_key
        # response = await openai.Audio.transcribe("whisper-1", audio_data, language=language)
        
        # デモ実装
        return {
            "text": "これはクラウドWhisper APIによる音声認識のデモ出力です。",
            "confidence": 0.98
        }

def get_stt_service() -> BaseSTTService:
    """
    設定に基づいて適切なSTTサービスのインスタンスを返す
    """
    if USE_LOCAL_MODE:
        # ローカルモードの場合はWhisperを使用
        return LocalWhisperService(model_name="base")
    else:
        # オンラインモードの場合はOpenAI APIを使用
        return CloudSTTService() 