# フロントエンド

音声アシスタントのフロントエンドアプリケーション群です。デスクトップ（Electron）とモバイル（React Native/Flutter）の両方をサポートします。

## 🏗️ 構成

```
frontend/
├── electron/           # Electronデスクトップアプリ
│   ├── main.js        # メインプロセス
│   ├── preload.js     # プリロードスクリプト
│   ├── index.html     # レンダラープロセス
│   ├── package.json   # 依存関係とスクリプト
│   └── assets/        # 静的リソース
└── mobile/            # モバイルアプリ（開発予定）
    ├── react-native/  # React Nativeアプリ
    └── flutter/       # Flutterアプリ
```

## 🖥️ Electron デスクトップアプリ

### 主な機能
- **音声入力**: マイクからのリアルタイム録音
- **チャットUI**: モダンな会話インターフェース
- **ホットキー**: グローバルショートカット（Ctrl+Shift+Space）
- **システムトレイ**: バックグラウンド動作とクイックアクセス
- **設定画面**: モード切替、音声選択、ホットキー設定
- **会話履歴**: 過去の対話の表示と管理

### 技術スタック
- **Electron**: クロスプラットフォームデスクトップアプリ
- **JavaScript/TypeScript**: メインロジック
- **HTML/CSS**: ユーザーインターフェース
- **IPC**: メイン・レンダラープロセス間通信

### 起動方法
```bash
cd src/frontend/electron
npm install
npm start
```

詳細は [electron/README.md](electron/README.md) を参照してください。

## 📱 モバイルアプリ（開発予定）

### React Native版
クロスプラットフォーム（iOS/Android）対応のモバイルアプリです。

#### 予定機能
- **音声入力**: スマートフォンマイクからの録音
- **タッチUI**: モバイル最適化されたインターフェース
- **プッシュ通知**: バックグラウンド応答通知
- **オフライン対応**: 基本機能のオフライン動作
- **音声再生**: TTS音声の再生とコントロール

#### 技術スタック
- **React Native**: クロスプラットフォーム開発
- **TypeScript**: 型安全な開発
- **React Navigation**: 画面遷移管理
- **AsyncStorage**: ローカルデータ保存

### Flutter版（代替案）
Dart言語によるクロスプラットフォーム開発です。

#### 予定機能
- React Native版と同等の機能
- **ネイティブパフォーマンス**: 高速な音声処理
- **カスタムUI**: Flutterの豊富なウィジェット

#### 技術スタック
- **Flutter**: Googleのクロスプラットフォームフレームワーク
- **Dart**: プログラミング言語
- **Provider**: 状態管理
- **Hive**: ローカルデータベース

## 🔗 共通アーキテクチャ

### バックエンド通信
全てのフロントエンドアプリは共通のREST APIを使用：

```typescript
// API通信の例
const apiClient = {
  stt: {
    transcribe: (audioFile: File) => POST('/api/stt/transcribe'),
    getInfo: () => GET('/api/stt/info')
  },
  llm: {
    chat: (messages: Message[]) => POST('/api/llm/chat'),
    getInfo: () => GET('/api/llm/info')
  },
  tts: {
    synthesize: (text: string) => POST('/api/tts/synthesize'),
    getVoices: () => GET('/api/tts/voices')
  }
};
```

### 状態管理
- **Electron**: IPC + ローカルストレージ
- **React Native**: Redux Toolkit + AsyncStorage
- **Flutter**: Provider + Hive

### セキュリティ
- **HTTPS通信**: 全API通信の暗号化
- **JWT認証**: ユーザー認証（将来実装）
- **CSP**: Content Security Policy（Electron）

## 🎨 UI/UX デザイン

### デザインシステム
- **カラーパレット**: ダーク/ライトテーマ対応
- **タイポグラフィ**: 読みやすいフォント選択
- **アイコン**: 統一されたアイコンセット
- **アニメーション**: スムーズなトランジション

### レスポンシブデザイン
- **デスクトップ**: 800x600px以上
- **タブレット**: 768px以上
- **スマートフォン**: 375px以上

### アクセシビリティ
- **キーボードナビゲーション**: 全機能のキーボード操作
- **スクリーンリーダー**: ARIA属性の適切な設定
- **コントラスト**: WCAG 2.1 AA準拠

## 🧪 テスト

### Electronアプリ
```bash
cd src/frontend/electron
npm test
```

### テスト構成
- **ユニットテスト**: Jest + Testing Library
- **E2Eテスト**: Playwright
- **統合テスト**: Spectron（Electron専用）

## 📦 ビルド・配布

### Electronアプリ
```bash
# 開発ビルド
npm run build

# 本番ビルド（実行ファイル作成）
npm run dist

# プラットフォーム別ビルド
npm run dist:win    # Windows
npm run dist:mac    # macOS
npm run dist:linux  # Linux
```

### モバイルアプリ（予定）
```bash
# React Native
npx react-native run-android
npx react-native run-ios

# Flutter
flutter build apk
flutter build ios
```

## 🔧 開発環境

### 必要なツール
- **Node.js**: 16.x以上
- **npm/yarn**: パッケージマネージャー
- **Electron**: デスクトップアプリ開発
- **React Native CLI**: モバイル開発（予定）
- **Flutter SDK**: モバイル開発（予定）

### 推奨エディタ設定
- **VSCode**: 推奨エディタ
- **拡張機能**: 
  - Electron
  - TypeScript
  - Prettier
  - ESLint

## 🐛 デバッグ

### Electronアプリ
```bash
# 開発者ツールを開いて起動
npm run dev

# ログ確認
# アプリ内の開発者ツール > Console
```

### 一般的な問題
1. **IPC通信エラー**: preload.jsの設定確認
2. **API接続エラー**: バックエンドサーバーの起動確認
3. **マイクアクセス**: システム権限の確認 