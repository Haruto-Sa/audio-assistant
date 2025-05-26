import os
import yaml
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

# ロガー設定
logger = logging.getLogger(__name__)

# デフォルト設定
DEFAULT_CONFIG = {
    "app": {
        "name": "音声アシスタント",
        "version": "0.1.0"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 8000
    },
    "services": {
        "stt": {
            "default_engine": "cloud",  # "cloud" または "local"
            "cloud": {
                "api_url": "https://api.openai.com/v1/audio/transcriptions",
                "model": "whisper-1"
            },
            "local": {
                "model_path": "models/whisper/base",
                "model_type": "base"  # "tiny", "base", "small", "medium", "large"
            }
        },
        "llm": {
            "default_engine": "cloud",  # "cloud" または "local"
            "cloud": {
                "api_url": "https://api.openai.com/v1",
                "model": "gpt-3.5-turbo"
            },
            "local": {
                "model_path": "models/llama-7b-chat-q4.gguf",
                "context_length": 2048
            }
        },
        "tts": {
            "default_engine": "cloud",  # "cloud" または "local"
            "cloud": {
                "api_url": "https://api.example.com/tts",
                "default_voice": "ja-female-1"
            },
            "local": {
                "model_path": "models/tts/kokoro",
                "default_voice": "kokoro"
            }
        }
    },
    "database": {
        "use_supabase": True,
    },
    "logging": {
        "level": "INFO",
        "file": "logs/app.log"
    }
}

class Config:
    """
    アプリケーション設定クラス
    """
    def __init__(self, config_path: Optional[str] = None):
        """
        設定を初期化する
        
        Parameters:
        -----------
        config_path : Optional[str], optional
            設定ファイルのパス (デフォルト: None)
        """
        self._config = DEFAULT_CONFIG.copy()
        
        # 設定ファイルが指定されている場合は読み込む
        if config_path and os.path.exists(config_path):
            self._load_from_file(config_path)
            
        # 環境変数から設定を上書き
        self._load_from_env()
    
    def _load_from_file(self, config_path: str) -> None:
        """
        ファイルから設定を読み込む
        
        Parameters:
        -----------
        config_path : str
            設定ファイルのパス
        """
        try:
            ext = Path(config_path).suffix.lower()
            
            if ext in ['.yaml', '.yml']:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self._update_config(config)
            elif ext == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self._update_config(config)
            else:
                logger.warning(f"未対応の設定ファイル形式です: {ext}")
        except Exception as e:
            logger.error(f"設定ファイルの読み込みに失敗しました: {e}")
            
    def _load_from_env(self) -> None:
        """
        環境変数から設定を読み込む
        """
        # STT設定
        if os.getenv("STT_ENGINE"):
            self._config["services"]["stt"]["default_engine"] = os.getenv("STT_ENGINE")
            
        # LLM設定
        if os.getenv("LLM_ENGINE"):
            self._config["services"]["llm"]["default_engine"] = os.getenv("LLM_ENGINE")
            
        if os.getenv("LLM_MODEL"):
            engine = self._config["services"]["llm"]["default_engine"]
            self._config["services"]["llm"][engine]["model"] = os.getenv("LLM_MODEL")
            
        # TTS設定
        if os.getenv("TTS_ENGINE"):
            self._config["services"]["tts"]["default_engine"] = os.getenv("TTS_ENGINE")
            
        # ローカルモードが指定されている場合は全てローカルに設定
        if os.getenv("USE_LOCAL_MODE", "").lower() == "true":
            self._config["services"]["stt"]["default_engine"] = "local"
            self._config["services"]["llm"]["default_engine"] = "local"
            self._config["services"]["tts"]["default_engine"] = "local"
            
        # クラウドモードが指定されている場合は全てクラウドに設定
        if os.getenv("USE_CLOUD_MODE", "").lower() == "true":
            self._config["services"]["stt"]["default_engine"] = "cloud"
            self._config["services"]["llm"]["default_engine"] = "cloud"
            self._config["services"]["tts"]["default_engine"] = "cloud"
            
        # Supabase設定
        if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
            self._config["database"]["use_supabase"] = True
        else:
            # URLまたはキーがない場合はSupabaseを無効化
            self._config["database"]["use_supabase"] = False
            
    def _update_config(self, new_config: Dict[str, Any]) -> None:
        """
        設定を更新する（再帰的）
        
        Parameters:
        -----------
        new_config : Dict[str, Any]
            新しい設定
        """
        def _update(target, source):
            for key, value in source.items():
                if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                    _update(target[key], value)
                else:
                    target[key] = value
                    
        _update(self._config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        設定値を取得する
        
        Parameters:
        -----------
        key : str
            設定キー（ドット区切り）
        default : Any, optional
            デフォルト値 (デフォルト: None)
            
        Returns:
        --------
        Any
            設定値
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def is_local_mode(self) -> bool:
        """
        ローカルモードかどうかを判定する
        
        Returns:
        --------
        bool
            ローカルモードならTrue
        """
        # サービス毎の設定がバラバラの場合は、LLMの設定を優先
        llm_engine = self.get("services.llm.default_engine")
        return llm_engine == "local"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        設定を辞書として取得する
        
        Returns:
        --------
        Dict[str, Any]
            設定辞書
        """
        return self._config.copy()

# シングルトンインスタンス
_config: Optional[Config] = None

def get_config() -> Config:
    """
    設定インスタンスを取得する
    
    Returns:
    --------
    Config
        設定インスタンス
    """
    global _config
    
    if _config is None:
        config_path = os.getenv("CONFIG_PATH")
        _config = Config(config_path)
        
    return _config 