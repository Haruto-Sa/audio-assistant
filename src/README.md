# ソースコード

このディレクトリには、音声アシスタントアプリケーションのソースコードが含まれています。

## ディレクトリ構成

```
src/
├── backend/          # Python FastAPI バックエンド
├── frontend/         # フロントエンドアプリケーション
│   ├── electron/     # Electron デスクトップアプリ
│   └── mobile/       # モバイルアプリ（React Native/Flutter）
└── shared/           # フロント・バック共通コード
```

## 🐍 backend/
Python + FastAPIで実装されたバックエンドサーバーです。

### 主な機能
- **REST API**: STT、LLM、TTSのエンドポイント提供
- **モード切替**: オンライン/オフラインモードの自動切替
- **データベース**: Supabase PostgreSQLとの連携
- **設定管理**: 環境変数とYAML/JSON設定ファイル対応

### 起動方法
```bash
cd src/backend
python main.py
```

詳細は [backend/README.md](backend/README.md) を参照してください。

## 🖥️ frontend/electron/
Electron + TypeScriptで実装されたデスクトップアプリケーションです。

### 主な機能
- **音声入力**: マイクからの録音とリアルタイム処理
- **GUI**: モダンなチャットインターフェース
- **ホットキー**: グローバルショートカット対応
- **システムトレイ**: バックグラウンド動作
- **設定画面**: モード切替、音声選択等

### 起動方法
```bash
cd src/frontend/electron
npm install
npm start
```

詳細は [frontend/electron/README.md](frontend/electron/README.md) を参照してください。

## 📱 frontend/mobile/
React Native または Flutterで実装予定のモバイルアプリケーションです。

### 予定機能
- **音声入力**: スマートフォンマイクからの録音
- **タッチUI**: モバイル最適化されたインターフェース
- **プッシュ通知**: バックグラウンド応答通知
- **オフライン対応**: 基本機能のオフライン動作

現在は開発準備中です。

## 🔗 shared/
フロントエンドとバックエンドで共有されるコードです。

### 含まれる内容
- **型定義**: TypeScript型定義ファイル
- **ユーティリティ**: 共通関数とヘルパー
- **定数**: API エンドポイント、設定値等
- **バリデーション**: 入力値検証ロジック

## 開発ガイドライン

### コーディング規約
- **Python**: PEP 8準拠、Black + isortでフォーマット
- **TypeScript**: ESLint + Prettierでフォーマット
- **コメント**: 日本語でのドキュメント記述

### テスト
- **バックエンド**: pytest使用
- **フロントエンド**: Jest + Testing Library使用
- **カバレッジ**: 80%以上を目標

### ブランチ戦略
- **main**: 本番リリース用
- **develop**: 開発統合用
- **feature/***: 機能開発用
- **hotfix/***: 緊急修正用

## 依存関係

### バックエンド主要パッケージ
- `fastapi`: Web APIフレームワーク
- `whisper`: 音声認識（ローカル）
- `llama-cpp-python`: LLM推論（ローカル）
- `TTS`: 音声合成（ローカル）
- `supabase`: データベース接続

### フロントエンド主要パッケージ
- `electron`: デスクトップアプリフレームワーク
- `typescript`: 型安全な開発
- `axios`: HTTP通信
- `electron-settings`: 設定管理 