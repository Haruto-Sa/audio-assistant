# プロジェクトディレクトリ構成


project-root/
├── docs/
│   ├── 要件定義.md
│   ├── directory.md
│   ├── prompt.md
│   └── best_practices.md
├── src/
│   ├── backend/
│   │   ├── main.py       # FastAPI/NestJS エントリポイント
│   │   ├── api/          # ルーティング定義
│   │   ├── services/     # STT/LLM/TTS ラッパー
│   │   ├── models/       # データベーススキーマ
│   │   └── utils/        # 共通ユーティリティ
│   ├── frontend/
│   │   ├── electron/     # Electron + TS GUI
│   │   └── mobile/       # React Native or Flutter
│   └── shared/           # フロント⇔バック共通型定義, utils
├── models/               # ローカルモデル配置例
├── scripts/              # セットアップ・デプロイスクリプト
├── tests/                # ユニット・統合テスト
├── ci/                   # GitHub Actions / CI 設定
├── .env.example          # 環境変数テンプレート
├── README.md
└── LICENSE


---

# prompt.md

```markdown
以下の要件定義.mdとdirectory.mdを参照し、音声アシスタントプロジェクトの基本テンプレートを生成してください。

- フォルダ／ファイルごとに雛形コードや必要な設定ファイルを作成
- モード切替（オンライン／オフライン）ロジックを示す
- Supabase認証／DB接続設定例を含める
- Electronおよびモバイルクライアント（React Native or Flutter）のエントリポイントを用意
- 各モジュール（STT／LLM／TTS）の依存パッケージリストを明記

生成物は、project-root 以下のディレクトリ構成に対応したコードベースとして出力してください。