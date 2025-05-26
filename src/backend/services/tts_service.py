import os
import abc
import io
import tempfile
from typing import Dict, Any, List, Optional, BinaryIO

# オンライン/オフラインモードの設定を取得
USE_LOCAL_MODE = os.getenv("USE_LOCAL_MODE", "false").lower() == "true"

class BaseTTSService(abc.ABC):
    """
    テキスト音声変換サービスの基底クラス
    """
    def __init__(self):
        self.name = "BaseTTSService"
        self.is_local = True
        self.supported_languages = ["ja"]
        
    @abc.abstractmethod
    async def synthesize(
        self,
        text: str,
        voice_id: str = "default",
        language: str = "ja",
        speed: float = 1.0
    ) -> bytes:
        """
        テキストを音声に変換する
        
        Parameters:
        -----------
        text : str
            音声に変換するテキスト
        voice_id : str, optional
            使用する音声ID (デフォルト: "default")
        language : str, optional
            言語コード (デフォルト: "ja")
        speed : float, optional
            再生速度 (デフォルト: 1.0)
            
        Returns:
        --------
        bytes
            生成された音声データ（WAVフォーマット）
        """
        pass
    
    @abc.abstractmethod
    async def list_voices(self, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        利用可能な音声一覧を取得する
        
        Parameters:
        -----------
        language : Optional[str], optional
            言語コードでフィルタリング (デフォルト: None)
            
        Returns:
        --------
        List[Dict[str, Any]]
            [{"id": 音声ID, "name": 音声名, "language": 言語コード}, ...]
        """
        pass

class LocalTTSService(BaseTTSService):
    """
    ローカルのTTSエンジン（pyttsx3）を使用した音声合成サービス
    """
    def __init__(self):
        super().__init__()
        self.name = "LocalTTS"
        self.is_local = True
        self.supported_languages = ["ja", "en"]
        
        # pyttsx3エンジンの初期化
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # 音声設定
            voices = self.engine.getProperty('voices')
            if voices:
                # 日本語音声があれば設定
                for voice in voices:
                    if 'ja' in voice.id.lower() or 'japanese' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                        
            # 速度設定
            self.engine.setProperty('rate', 150)  # 150 words per minute
            
        except ImportError:
            print("Warning: pyttsx3 not available, using fallback")
            self.engine = None
        
    async def synthesize(
        self,
        text: str,
        voice_id: str = "default",
        language: str = "ja",
        speed: float = 1.0
    ) -> bytes:
        """
        ローカルTTSエンジンを使用してテキストを音声に変換する
        """
        if not self.engine:
            # フォールバック: ダミーのWAVファイルを返す
            sample_path = os.path.join(os.getcwd(), "models", "sample_audio.wav")
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    return f.read()
            else:
                # 最小限のWAVヘッダーを生成
                return self._generate_dummy_wav()
        
        try:
            # 一時ファイルに音声を保存
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                
            # 速度設定
            current_rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', int(current_rate * speed))
            
            # 音声ファイルに保存
            self.engine.save_to_file(text, temp_path)
            self.engine.runAndWait()
            
            # ファイルを読み込んでバイト列として返す
            with open(temp_path, "rb") as f:
                audio_data = f.read()
                
            # 一時ファイルを削除
            os.unlink(temp_path)
            
            return audio_data
            
        except Exception as e:
            print(f"TTS synthesis error: {e}")
            return self._generate_dummy_wav()
    
    def _generate_dummy_wav(self) -> bytes:
        """ダミーのWAVファイルを生成"""
        # 最小限のWAVヘッダー（44バイト）+ 無音データ
        wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        return wav_header
    
    async def list_voices(self, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        利用可能な音声一覧を取得する
        """
        voices = []
        
        if self.engine:
            try:
                system_voices = self.engine.getProperty('voices')
                for i, voice in enumerate(system_voices):
                    # 言語を推定
                    voice_lang = "en"  # デフォルト
                    if 'ja' in voice.id.lower() or 'japanese' in voice.name.lower():
                        voice_lang = "ja"
                    
                    voices.append({
                        "id": voice.id,
                        "name": voice.name,
                        "language": voice_lang
                    })
            except Exception as e:
                print(f"Error getting voices: {e}")
        
        # デフォルト音声を追加
        if not voices:
            voices = [
                {"id": "default", "name": "Default Voice", "language": "en"},
                {"id": "japanese", "name": "Japanese Voice", "language": "ja"}
            ]
        
        if language:
            voices = [v for v in voices if v["language"] == language]
            
        return voices

class CloudTTSService(BaseTTSService):
    """
    クラウドAPIを使用した音声合成サービス（gTTS使用）
    """
    def __init__(self, api_key: Optional[str] = None):
        super().__init__()
        self.name = "CloudTTS"
        self.is_local = False
        self.supported_languages = ["ja", "en", "zh", "ko", "fr", "de", "es"]
        
        # APIキーを設定（gTTSは無料なのでAPIキー不要）
        self.api_key = api_key or os.getenv("CLOUD_TTS_API_KEY")
        
    async def synthesize(
        self,
        text: str,
        voice_id: str = "default",
        language: str = "ja",
        speed: float = 1.0
    ) -> bytes:
        """
        gTTSを使用してテキストを音声に変換する
        """
        try:
            from gtts import gTTS
            
            # gTTSで音声合成
            tts = gTTS(text=text, lang=language, slow=(speed < 0.8))
            
            # メモリ上のバイトストリームに保存
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
            
        except ImportError:
            print("Warning: gTTS not available, using fallback")
            return self._generate_dummy_wav()
        except Exception as e:
            print(f"gTTS synthesis error: {e}")
            return self._generate_dummy_wav()
    
    def _generate_dummy_wav(self) -> bytes:
        """ダミーのWAVファイルを生成"""
        # 最小限のWAVヘッダー（44バイト）+ 無音データ
        wav_header = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        return wav_header
    
    async def list_voices(self, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        利用可能な音声一覧を取得する
        """
        # gTTSでサポートされている言語
        voices = [
            {"id": "ja", "name": "Japanese (Google)", "language": "ja"},
            {"id": "en", "name": "English (Google)", "language": "en"},
            {"id": "zh", "name": "Chinese (Google)", "language": "zh"},
            {"id": "ko", "name": "Korean (Google)", "language": "ko"},
            {"id": "fr", "name": "French (Google)", "language": "fr"},
            {"id": "de", "name": "German (Google)", "language": "de"},
            {"id": "es", "name": "Spanish (Google)", "language": "es"}
        ]
        
        if language:
            voices = [v for v in voices if v["language"] == language]
            
        return voices

def get_tts_service() -> BaseTTSService:
    """
    設定に基づいて適切なTTSサービスのインスタンスを返す
    """
    if USE_LOCAL_MODE:
        # ローカルモードの場合はpyttsx3を使用
        return LocalTTSService()
    else:
        # オンラインモードの場合はgTTSを使用
        return CloudTTSService() 