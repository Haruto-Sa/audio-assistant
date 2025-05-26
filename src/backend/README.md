# バックエンド (Python + FastAPI)

音声アシスタントのバックエンドAPIサーバーです。STT（音声認識）、LLM（会話生成）、TTS（音声合成）の各機能をREST APIとして提供します。

## 🏗️ アーキテクチャ

```
backend/
├── main.py              # FastAPIアプリケーションエントリポイント
├── api/                 # REST APIエンドポイント定義
│   ├── __init__.py
│   ├── stt.py          # 音声認識API
│   ├── llm.py          # テキスト生成API
│   └── tts.py          # 音声合成API
├── services/            # ビジネスロジック層
│   ├── __init__.py
│   ├── stt_service.py  # STTサービス（Whisper）
│   ├── llm_service.py  # LLMサービス（LLaMA/OpenAI）
│   ├── tts_service.py  # TTSサービス（Coqui/Cloud）
│   └── db.py           # データベースサービス（Supabase）
├── models/              # データモデル定義
│   ├── __init__.py
│   └── conversation.py # 会話履歴モデル
└── utils/               # ユーティリティ
    ├── __init__.py
    └── config.py       # 設定管理
```

## 🚀 起動方法

### 1. 依存関係のインストール
```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# パッケージのインストール
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
# .envファイルを作成
cp .env.example .env

# 必要な設定を入力
# USE_LOCAL_MODE=false
# OPENAI_API_KEY=your_openai_api_key
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_key
```

### 3. サーバーの起動
```bash
python main.py
```

サーバーは `http://localhost:8000` で起動します。

## 📡 API エンドポイント

### 音声認識 (STT)
- `POST /api/stt/transcribe` - 音声ファイルをテキストに変換
- `GET /api/stt/info` - STTサービス情報を取得

### テキスト生成 (LLM)
- `POST /api/llm/chat` - チャット応答を生成
- `GET /api/llm/info` - LLMサービス情報を取得

### 音声合成 (TTS)
- `POST /api/tts/synthesize` - テキストを音声に変換
- `GET /api/tts/voices` - 利用可能な音声一覧を取得
- `GET /api/tts/info` - TTSサービス情報を取得

### その他
- `GET /` - サーバー情報とモード表示
- `GET /health` - ヘルスチェック

## 🔧 設定

### モード切替
環境変数 `USE_LOCAL_MODE` でオンライン/オフラインモードを切り替えます：

#### クラウドモード (USE_LOCAL_MODE=false)
- **STT**: OpenAI Whisper API
- **LLM**: OpenAI GPT API
- **TTS**: クラウドTTS API
- **要件**: インターネット接続、APIキー

#### ローカルモード (USE_LOCAL_MODE=true)
- **STT**: ローカルWhisperモデル
- **LLM**: ローカルLLaMAモデル
- **TTS**: Coqui TTSモデル
- **要件**: ローカルモデルファイル

### 環境変数一覧
```bash
# モード設定
USE_LOCAL_MODE=false

# サーバー設定
PORT=8000
HOST=0.0.0.0

# OpenAI API（クラウドモード）
OPENAI_API_KEY=your_api_key

# Supabase（会話履歴保存）
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# ローカルモデルパス
WHISPER_MODEL_PATH=models/whisper/base
LLAMA_MODEL_PATH=models/llama-7b-chat-q4.gguf
TTS_MODEL_PATH=models/tts/kokoro

# ログ設定
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🧩 モジュール詳細

### api/ - REST APIエンドポイント
各APIエンドポイントの定義とリクエスト/レスポンス処理を担当します。

#### stt.py
- 音声ファイルのアップロード処理
- STTサービスとの連携
- エラーハンドリング

#### llm.py
- チャットメッセージの処理
- 会話履歴の管理
- ストリーミング応答対応

#### tts.py
- テキスト音声変換
- 音声ファイルのストリーミング配信
- 音声設定の管理

### services/ - ビジネスロジック層
実際のAI処理とデータベース操作を担当します。

#### stt_service.py
- **BaseSTTService**: STTサービスの抽象基底クラス
- **LocalWhisperService**: ローカルWhisperモデル
- **CloudSTTService**: OpenAI Whisper API

#### llm_service.py
- **BaseLLMService**: LLMサービスの抽象基底クラス
- **LocalLLMService**: ローカルLLaMAモデル
- **CloudLLMService**: OpenAI GPT API

#### tts_service.py
- **BaseTTSService**: TTSサービスの抽象基底クラス
- **LocalTTSService**: Coqui TTSモデル
- **CloudTTSService**: クラウドTTS API

#### db.py
- **DatabaseService**: Supabaseデータベース操作
- 会話履歴の保存・取得
- ユーザー管理

### models/ - データモデル
Pydanticベースのデータモデル定義です。

#### conversation.py
- **Message**: メッセージモデル
- **Conversation**: 会話モデル
- **ConversationSummary**: 会話要約モデル
- PostgreSQL DDL定義

### utils/ - ユーティリティ
共通機能とヘルパー関数です。

#### config.py
- **Config**: 設定管理クラス
- 環境変数とファイル設定の統合
- モード判定ロジック

## 🧪 テスト

### テストの実行
```bash
# 全テストの実行
pytest

# カバレッジ付きテスト
pytest --cov=. --cov-report=html

# 特定のテストファイル
pytest tests/test_stt_service.py
```

### テスト構成
```
tests/
├── test_api/           # APIエンドポイントテスト
├── test_services/      # サービス層テスト
├── test_models/        # モデルテスト
└── conftest.py         # テスト設定
```

## 🐛 デバッグ

### ログ確認
```bash
# リアルタイムログ
tail -f logs/app.log

# エラーログのみ
grep ERROR logs/app.log
```

### 開発モード
```bash
# デバッグモードで起動
uvicorn main:app --reload --log-level debug
```

## 📦 依存パッケージ

### 主要パッケージ
- `fastapi`: Web APIフレームワーク
- `uvicorn`: ASGIサーバー
- `pydantic`: データバリデーション
- `python-dotenv`: 環境変数管理

### AI関連パッケージ
- `openai-whisper`: ローカル音声認識
- `llama-cpp-python`: ローカルLLM推論
- `TTS`: ローカル音声合成
- `openai`: OpenAI API クライアント

### データベース
- `supabase`: Supabaseクライアント
- `psycopg2-binary`: PostgreSQLドライバー

### 開発・テスト
- `pytest`: テストフレームワーク
- `pytest-cov`: カバレッジ測定
- `black`: コードフォーマッター
- `isort`: インポート整理 