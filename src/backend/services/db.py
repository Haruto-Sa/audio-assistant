import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import logging
from datetime import datetime
import json
import uuid

# スタブ実装（実際には supabase-py を使用）
# from supabase import create_client, Client

# 環境変数のロード
load_dotenv()

# Supabase接続設定
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USE_SUPABASE = all([SUPABASE_URL, SUPABASE_KEY])

# ロガー設定
logger = logging.getLogger(__name__)

class DatabaseService:
    """
    Supabaseデータベース接続サービス
    """
    def __init__(
        self,
        supabase_url: Optional[str] = None,
        supabase_key: Optional[str] = None
    ):
        self.supabase_url = supabase_url or SUPABASE_URL
        self.supabase_key = supabase_key or SUPABASE_KEY
        
        # スタブ実装（実際には Supabase クライアントを初期化）
        # if USE_SUPABASE:
        #     self.client = create_client(self.supabase_url, self.supabase_key)
        # else:
        self.client = None
        
        if not USE_SUPABASE:
            logger.warning("Supabase接続情報が設定されていないため、DB機能は使用できません")
    
    async def get_conversation_history(
        self,
        conversation_id: str,
        limit: int = 50,
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        会話履歴を取得する
        
        Parameters:
        -----------
        conversation_id : str
            会話ID
        limit : int, optional
            取得する最大件数 (デフォルト: 50)
        user_id : Optional[str], optional
            ユーザーID (デフォルト: None)
            
        Returns:
        --------
        List[Dict[str, Any]]
            会話履歴のリスト
        """
        if not USE_SUPABASE:
            return []
            
        try:
            # 実際の実装
            # query = self.client.table("conversations").select("*") \
            #     .eq("conversation_id", conversation_id) \
            #     .order("created_at", desc=False) \
            #     .limit(limit)
            # 
            # if user_id:
            #     query = query.eq("user_id", user_id)
            #     
            # response = query.execute()
            # return response.data
            
            # スタブ実装
            return [
                {
                    "id": 1,
                    "conversation_id": conversation_id,
                    "user_id": user_id or "anonymous",
                    "role": "user",
                    "content": "こんにちは、調子はどうですか？",
                    "created_at": "2023-05-15T10:00:00"
                },
                {
                    "id": 2,
                    "conversation_id": conversation_id,
                    "user_id": user_id or "anonymous",
                    "role": "assistant",
                    "content": "こんにちは！元気です。あなたはどうですか？",
                    "created_at": "2023-05-15T10:00:05"
                }
            ]
        except Exception as e:
            logger.error(f"会話履歴の取得に失敗しました: {e}")
            return []
    
    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        user_id: Optional[str] = None
    ) -> bool:
        """
        メッセージを保存する
        
        Parameters:
        -----------
        conversation_id : str
            会話ID
        role : str
            メッセージの役割 ("user" または "assistant")
        content : str
            メッセージの内容
        user_id : Optional[str], optional
            ユーザーID (デフォルト: None)
            
        Returns:
        --------
        bool
            保存に成功したかどうか
        """
        if not USE_SUPABASE:
            return True
            
        try:
            # 実際の実装
            # data = {
            #     "conversation_id": conversation_id,
            #     "user_id": user_id or "anonymous",
            #     "role": role,
            #     "content": content,
            #     "created_at": datetime.now().isoformat()
            # }
            # 
            # response = self.client.table("conversations").insert(data).execute()
            # return len(response.data) > 0
            
            # スタブ実装
            logger.info(f"メッセージを保存しました: {conversation_id} ({role})")
            return True
        except Exception as e:
            logger.error(f"メッセージの保存に失敗しました: {e}")
            return False
    
    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        ユーザーの会話一覧を取得する
        
        Parameters:
        -----------
        user_id : str
            ユーザーID
        limit : int, optional
            取得する最大件数 (デフォルト: 10)
            
        Returns:
        --------
        List[Dict[str, Any]]
            会話一覧
        """
        if not USE_SUPABASE:
            return []
            
        try:
            # 実際の実装
            # # 会話IDとタイムスタンプの一覧を取得
            # query = self.client.table("conversations") \
            #     .select("conversation_id, MAX(created_at) as last_updated") \
            #     .eq("user_id", user_id) \
            #     .group_by("conversation_id") \
            #     .order("last_updated", desc=True) \
            #     .limit(limit)
            # 
            # response = query.execute()
            # conversations = response.data
            # 
            # # 各会話の最新メッセージを取得
            # result = []
            # for conv in conversations:
            #     conv_id = conv["conversation_id"]
            #     latest_msg = self.client.table("conversations") \
            #         .select("*") \
            #         .eq("conversation_id", conv_id) \
            #         .order("created_at", desc=True) \
            #         .limit(1) \
            #         .execute()
            #     
            #     if latest_msg.data:
            #         result.append({
            #             "conversation_id": conv_id,
            #             "last_message": latest_msg.data[0]["content"],
            #             "updated_at": conv["last_updated"]
            #         })
            # 
            # return result
            
            # スタブ実装
            return [
                {
                    "conversation_id": str(uuid.uuid4()),
                    "last_message": "こんにちは！元気です。あなたはどうですか？",
                    "updated_at": "2023-05-15T10:00:05"
                },
                {
                    "conversation_id": str(uuid.uuid4()),
                    "last_message": "明日の天気予報を教えてください。",
                    "updated_at": "2023-05-14T15:30:20"
                }
            ]
        except Exception as e:
            logger.error(f"ユーザーの会話一覧の取得に失敗しました: {e}")
            return []

# Supabaseデータベースサービスのシングルトンインスタンス
_db_service: Optional[DatabaseService] = None

def get_db_service() -> DatabaseService:
    """
    データベースサービスのインスタンスを取得する
    """
    global _db_service
    
    if _db_service is None:
        _db_service = DatabaseService()
        
    return _db_service 