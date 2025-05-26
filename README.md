# 音声アシスタント プロジェクト

## 概要
音声アシスタントプロジェクトのスケルトンコードです。STT（音声→テキスト）、LLM（チャット応答）、TTS（テキスト→音声）の機能を提供します。

## 技術スタック
- **バックエンド**: Python 3.12 + FastAPI
- **フロントエンド**: Electron (予定)
- **データベース**: Supabase PostgreSQL
- **音声処理**: 
  - STT: OpenAI Whisper (ローカル/クラウド)
  - LLM: LLaMA (ローカル) / OpenAI API (クラウド)
  - TTS: pyttsx3 (ローカル) / gTTS (クラウド)

## 解決済みの問題
✅ **Python 3.12互換性問題**: 
- TTSパッケージ（Coqui TTS）がPython 3.12未対応だった問題を解決
- pyttsx3（ローカル）とgTTS（クラウド）に変更
- 文字エンコーディング問題も解決

✅ **パッケージインストール**: 
- requirements.txtをUTF-8で再作成
- 全ての依存パッケージが正常にインストール完了

✅ **サーバー起動**: 
- FastAPIサーバーが正常に起動
- ヘルスチェックエンドポイント動作確認済み
- TTSエンドポイント動作確認済み

## プロジェクト構造
```
audioAuto/
├── src/
│   ├── backend/           # Python FastAPI バックエンド
│   │   ├── main.py       # エントリポイント
│   │   ├── api/          # APIエンドポイント
│   │   ├── services/     # ビジネスロジック
│   │   ├── models/       # データモデル
│   │   └── utils/        # ユーティリティ
│   ├── frontend/         # フロントエンド
│   │   └── electron/     # Electronアプリ
│   └── shared/           # 共通コード
├── models/               # AIモデル格納
├── docs/                 # ドキュメント
├── tests/                # テストコード
├── scripts/              # スクリプト
├── ci/                   # CI/CD設定
├── requirements.txt      # Python依存パッケージ
└── .env.example         # 環境変数テンプレート
```

## セットアップ手順

### 1. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

### 3. サーバーの起動
```bash
python src/backend/main.py
```

### 4. API確認
- ヘルスチェック: http://localhost:8000/health
- API仕様書: http://localhost:8000/docs

## API エンドポイント

### ヘルスチェック
- `GET /health` - サーバーの状態確認

### STT (音声→テキスト)
- `POST /api/stt/transcribe` - 音声ファイルをテキストに変換

### LLM (チャット)
- `POST /api/llm/chat` - チャット応答生成

### TTS (テキスト→音声)
- `POST /api/tts/synthesize` - テキストを音声に変換
- `GET /api/tts/voices` - 利用可能な音声一覧

## 動作モード

### ローカルモード (USE_LOCAL_MODE=true)
- STT: OpenAI Whisper (ローカル)
- LLM: LLaMA (ローカル)
- TTS: pyttsx3 (ローカル)

### クラウドモード (USE_LOCAL_MODE=false)
- STT: OpenAI Whisper API
- LLM: OpenAI GPT API
- TTS: Google Text-to-Speech (gTTS)

## 今後の開発予定
- [ ] Electronクライアントの実装
- [ ] モバイルアプリ（React Native/Flutter）
- [ ] 音声ストリーミング対応
- [ ] リアルタイム会話機能
- [ ] 多言語対応の拡張
- [ ] テストコードの追加
- [ ] CI/CD パイプラインの構築

## 開発者向け情報
- Python 3.12対応済み
- Windows、Mac、Linux対応
- GPU/CPU両対応
- オンライン/オフライン切替可能

## 主な機能
- 🎤 **音声入力**: マイクからの音声キャプチャ
- 🔤 **音声認識**: Whisper（ローカル/クラウド）による音声→テキスト変換
- 🤖 **AI会話**: LLaMA（ローカル）/OpenAI（クラウド）による対話生成
- 🔊 **音声合成**: Coqui TTS（ローカル）/クラウドAPIによるテキスト→音声変換
- 💾 **会話履歴**: Supabase PostgreSQLでの履歴管理
- ⚡ **ホットキー**: グローバルショートカットでの起動
- 🌐 **クロスプラットフォーム**: Windows/Mac/Linux対応

## セットアップ

### 1. 環境要件
- Python 3.8+
- Node.js 16+
- Git

### 2. リポジトリのクローン
```bash
git clone <repository-url>
cd audioAuto
```

### 3. バックエンドのセットアップ
```bash
# Python仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 4. フロントエンド（Electron）のセットアップ
```bash
cd src/frontend/electron
npm install
```

### 5. 環境変数の設定
```bash
# .envファイルを作成
cp .env.example .env

# .envファイルを編集して必要な設定を入力
# - OpenAI API Key（クラウドモード使用時）
# - Supabase URL/Key（会話履歴保存時）
```

### 6. ローカルモデルのダウンロード（オプション）
```bash
# modelsディレクトリを作成
mkdir models

# Whisperモデル（自動ダウンロード）
# LLaMAモデル（手動ダウンロード）
# wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.q4_0.gguf -O models/llama-7b-chat-q4.gguf
```

## 使用方法

### 基本的な起動手順

#### 1. バックエンドサーバーの起動
```bash
# プロジェクトルートで
cd src/backend
python main.py
```
サーバーは `http://localhost:8000` で起動します。

#### 2. Electronアプリの起動
```bash
# 別のターミナルで
cd src/frontend/electron
npm start
```

### モード切替

#### クラウドモード（デフォルト）
```bash
# .envファイルで設定
USE_LOCAL_MODE=false
```
- OpenAI APIを使用
- インターネット接続が必要
- 高精度・高速

#### ローカルモード
```bash
# .envファイルで設定
USE_LOCAL_MODE=true
```
- ローカルモデルを使用
- オフライン動作可能
- プライバシー重視

### 基本操作

1. **音声入力**: マイクボタンをクリックまたはホットキー（Ctrl+Shift+Space）
2. **テキスト入力**: テキストエリアに直接入力
3. **設定変更**: 設定パネルでモード切替、音声選択など
4. **会話履歴**: 自動的にSupabaseに保存（設定で無効化可能）

### API エンドポイント

バックエンドAPIは以下のエンドポイントを提供：

- `POST /api/stt/transcribe` - 音声認識
- `POST /api/llm/chat` - テキスト生成
- `POST /api/tts/synthesize` - 音声合成
- `GET /api/stt/info` - STTサービス情報
- `GET /api/llm/info` - LLMサービス情報
- `GET /api/tts/info` - TTSサービス情報

## 開発

### テストの実行
```bash
# バックエンドテスト
cd src/backend
pytest tests/

# フロントエンドテスト
cd src/frontend/electron
npm test
```

### ビルド
```bash
# Electronアプリのビルド
cd src/frontend/electron
npm run build

# 実行ファイルの作成
npm run dist
```

## トラブルシューティング

### よくある問題

1. **マイクが認識されない**
   - ブラウザ/アプリにマイクアクセス許可を与える
   - システムのマイク設定を確認

2. **ローカルモデルが動作しない**
   - モデルファイルが正しくダウンロードされているか確認
   - GPU/CPUの要件を確認

3. **Supabase接続エラー**
   - .envファイルのURL/Keyが正しいか確認
   - ネットワーク接続を確認

### ログの確認
```bash
# バックエンドログ
tail -f logs/app.log

# Electronログ
# アプリ内の開発者ツールで確認
```

## 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## サポート

問題や質問がある場合は、[Issues](https://github.com/your-repo/issues) で報告してください。 