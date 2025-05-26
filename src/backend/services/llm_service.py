import os
import abc
import uuid
from typing import Dict, Any, List, Optional

# オンライン/オフラインモードの設定を取得
USE_LOCAL_MODE = os.getenv("USE_LOCAL_MODE", "false").lower() == "true"

class BaseLLMService(abc.ABC):
    """
    LLMサービスの基底クラス
    """
    def __init__(self):
        self.name = "BaseLLMService"
        self.is_local = True
        self.model_name = "base"
        
    @abc.abstractmethod
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        conversation_id: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        メッセージ履歴から応答を生成する
        
        Parameters:
        -----------
        messages : List[Dict[str, str]]
            メッセージ履歴
        conversation_id : Optional[str], optional
            会話ID (デフォルト: None)
        max_tokens : int, optional
            最大トークン数 (デフォルト: 1024)
        temperature : float, optional
            多様性パラメータ (デフォルト: 0.7)
            
        Returns:
        --------
        Dict[str, Any]
            {
                "text": 生成されたテキスト,
                "conversation_id": 会話ID,
                "finish_reason": 終了理由,
                "usage": 使用量情報
            }
        """
        pass

class LocalLLMService(BaseLLMService):
    """
    ローカルLLMを使用した応答生成サービス
    """
    def __init__(self, model_path: str = None):
        super().__init__()
        self.name = "LocalLLM"
        self.is_local = True
        self.model_name = os.path.basename(model_path) if model_path else "llama-7b-chat-q4"
        
        # モデルパスが指定されていない場合はデフォルトを使用
        self.model_path = model_path or os.path.join(os.getcwd(), "models", "llama-7b-chat-q4.gguf")
        
        # ここでLLaMA CPPモデルをロードする
        # from llama_cpp import Llama
        # self.model = Llama(model_path=self.model_path, n_ctx=2048)
        
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        conversation_id: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        ローカルLLMを使用して応答を生成する
        """
        # 会話IDがない場合は新しく生成
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
            
        # 実際の実装では、LLaMA CPPを使って応答を生成
        # prompt = self._convert_messages_to_prompt(messages)
        # response = self.model.generate(
        #     prompt=prompt,
        #     max_tokens=max_tokens,
        #     temperature=temperature
        # )
        
        # デモ実装
        return {
            "text": "これはローカルLLMによる応答生成のデモ出力です。",
            "conversation_id": conversation_id,
            "finish_reason": "completed",
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "total_tokens": 120
            }
        }
        
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        メッセージをLLaMAの入力形式に変換する
        """
        prompt = ""
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt += f"<s>[INST] <<SYS>>\n{content}\n<</SYS>>\n\n"
            elif role == "user":
                prompt += f"{content} [/INST]\n\n"
            elif role == "assistant":
                prompt += f"{content} </s>\n\n"
                
        return prompt

class CloudLLMService(BaseLLMService):
    """
    クラウドLLM APIを使用した応答生成サービス
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__()
        self.name = "CloudLLM"
        self.is_local = False
        self.model_name = model
        
        # APIキーを設定
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        conversation_id: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        OpenAI APIを使用して応答を生成する
        """
        # 会話IDがない場合は新しく生成
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
            
        # 実際の実装では、OpenAI APIを呼び出す
        # import openai
        # openai.api_key = self.api_key
        # response = await openai.ChatCompletion.create(
        #     model=self.model_name,
        #     messages=messages,
        #     max_tokens=max_tokens,
        #     temperature=temperature
        # )
        
        # デモ実装
        return {
            "text": "これはクラウドLLM APIによる応答生成のデモ出力です。",
            "conversation_id": conversation_id,
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 25,
                "total_tokens": 145
            }
        }

def get_llm_service() -> BaseLLMService:
    """
    設定に基づいて適切なLLMサービスのインスタンスを返す
    """
    if USE_LOCAL_MODE:
        # ローカルモードの場合はLLaMA CPPを使用
        return LocalLLMService()
    else:
        # オンラインモードの場合はOpenAI APIを使用
        return CloudLLMService() 