# Electron デスクトップアプリ

音声アシスタントのElectronベースデスクトップアプリケーションです。Windows、macOS、Linuxで動作するクロスプラットフォーム対応のGUIアプリです。

## 🚀 クイックスタート

```bash
# 依存関係のインストール
npm install

# 開発モードで起動
npm start

# 本番ビルド
npm run build

# 実行ファイル作成
npm run dist
```

## 🏗️ アーキテクチャ

### プロセス構成
```
Electronアプリ
├── メインプロセス (main.js)
│   ├── ウィンドウ管理
│   ├── システムトレイ
│   ├── グローバルホットキー
│   └── IPC通信ハンドラー
└── レンダラープロセス (index.html)
    ├── ユーザーインターフェース
    ├── 音声録音・再生
    └── API通信
```

### ファイル構成
```
electron/
├── main.js              # メインプロセス
├── preload.js           # プリロードスクリプト（セキュリティ）
├── index.html           # メインウィンドウ
├── package.json         # 依存関係とスクリプト
├── assets/              # 静的リソース
│   ├── css/
│   │   └── styles.css   # スタイルシート
│   ├── js/
│   │   └── app.js       # フロントエンドロジック
│   └── icons/           # アプリケーションアイコン
└── dist/                # ビルド成果物
```

## 🎯 主な機能

### 1. 音声入力・処理
- **マイク録音**: リアルタイム音声キャプチャ
- **音声認識**: バックエンドSTT APIとの連携
- **音声合成**: TTS APIからの音声再生
- **音声コントロール**: 再生・停止・音量調整

### 2. チャットインターフェース
- **会話表示**: ユーザーとアシスタントのメッセージ表示
- **テキスト入力**: キーボードからの直接入力
- **履歴管理**: 過去の会話の表示と検索
- **エクスポート**: 会話履歴のファイル出力

### 3. グローバルホットキー
- **デフォルト**: `Ctrl+Shift+Space`（Windows/Linux）、`Cmd+Shift+Space`（macOS）
- **カスタマイズ**: 設定画面でのホットキー変更
- **動作**: アプリの表示・非表示切り替え、録音開始

### 4. システムトレイ
- **バックグラウンド動作**: ウィンドウを閉じてもアプリ継続
- **クイックアクセス**: 右クリックメニューから機能実行
- **ステータス表示**: 接続状態やモードの視覚的表示

### 5. 設定管理
- **モード切替**: クラウド/ローカルモードの選択
- **音声設定**: TTS音声の選択、音量調整
- **UI設定**: テーマ、言語、フォントサイズ
- **ホットキー**: グローバルショートカットの設定

## 🔧 技術詳細

### IPC通信
メインプロセスとレンダラープロセス間の安全な通信：

```javascript
// preload.js - セキュアなAPI公開
contextBridge.exposeInMainWorld('electronAPI', {
  // 音声処理
  getMicrophoneInput: () => ipcRenderer.invoke('get-microphone-input'),
  performSTT: (audioPath) => ipcRenderer.invoke('perform-stt', audioPath),
  performLLM: (text, conversationId) => ipcRenderer.invoke('perform-llm', text, conversationId),
  performTTS: (text, voiceId) => ipcRenderer.invoke('perform-tts', text, voiceId),
  
  // データ管理
  getConversationHistory: (conversationId) => ipcRenderer.invoke('get-conversation-history', conversationId),
  saveSettings: (settings) => ipcRenderer.invoke('save-settings', settings),
  
  // イベントリスナー
  onStartRecording: (callback) => ipcRenderer.on('start-recording', callback),
  onOpenSettings: (callback) => ipcRenderer.on('open-settings', callback)
});
```

### セキュリティ
- **contextIsolation**: レンダラープロセスの分離
- **nodeIntegration**: 無効化によるセキュリティ強化
- **preload**: 安全なAPI公開メカニズム
- **CSP**: Content Security Policyの適用

### 状態管理
```javascript
// アプリケーション状態
const appState = {
  isRecording: false,
  currentConversationId: null,
  settings: {
    useLocalMode: false,
    hotkey: 'CommandOrControl+Shift+Space',
    theme: 'system',
    volume: 0.8
  },
  connectionStatus: 'connected'
};
```

## 🎨 ユーザーインターフェース

### レイアウト構成
```html
<div class="app-container">
  <header class="app-header">
    <!-- タイトル、モード表示、接続状態 -->
  </header>
  
  <main class="chat-container">
    <div class="conversation-history">
      <!-- 会話履歴の表示エリア -->
    </div>
    
    <div class="input-container">
      <!-- テキスト入力、マイクボタン、送信ボタン -->
    </div>
  </main>
  
  <div class="settings-panel">
    <!-- 設定画面（オーバーレイ表示） -->
  </div>
</div>
```

### スタイリング
- **CSS Grid/Flexbox**: レスポンシブレイアウト
- **CSS Variables**: テーマ切り替え対応
- **アニメーション**: スムーズなトランジション
- **アイコン**: SVGベースのスケーラブルアイコン

### テーマ対応
```css
:root {
  /* ライトテーマ */
  --bg-primary: #ffffff;
  --text-primary: #333333;
  --accent-color: #007acc;
}

[data-theme="dark"] {
  /* ダークテーマ */
  --bg-primary: #1e1e1e;
  --text-primary: #ffffff;
  --accent-color: #4fc3f7;
}
```

## 📡 API連携

### バックエンド通信
```javascript
const API_BASE_URL = 'http://localhost:8000/api';

// STT API呼び出し
async function transcribeAudio(audioFile) {
  const formData = new FormData();
  formData.append('file', audioFile);
  
  const response = await fetch(`${API_BASE_URL}/stt/transcribe`, {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// LLM API呼び出し
async function generateResponse(messages, conversationId) {
  const response = await fetch(`${API_BASE_URL}/llm/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages,
      conversation_id: conversationId
    })
  });
  
  return await response.json();
}
```

### エラーハンドリング
- **ネットワークエラー**: 接続失敗時の再試行ロジック
- **APIエラー**: サーバーエラーの適切な表示
- **タイムアウト**: 長時間応答なしの処理
- **フォールバック**: オフライン時の代替動作

## 🧪 テスト

### テスト構成
```
tests/
├── unit/               # ユニットテスト
│   ├── main.test.js   # メインプロセステスト
│   └── renderer.test.js # レンダラープロセステスト
├── integration/        # 統合テスト
│   └── ipc.test.js    # IPC通信テスト
└── e2e/               # E2Eテスト
    └── app.test.js    # アプリケーション全体テスト
```

### テスト実行
```bash
# 全テスト実行
npm test

# ユニットテストのみ
npm run test:unit

# E2Eテストのみ
npm run test:e2e

# カバレッジ付きテスト
npm run test:coverage
```

## 📦 ビルド・配布

### 開発ビルド
```bash
# 開発用ビルド
npm run build:dev

# ウォッチモード
npm run build:watch
```

### 本番ビルド
```bash
# 本番用ビルド
npm run build

# プラットフォーム別ビルド
npm run build:win     # Windows
npm run build:mac     # macOS
npm run build:linux   # Linux

# 全プラットフォーム
npm run build:all
```

### 配布パッケージ
```bash
# インストーラー作成
npm run dist

# ポータブル版作成
npm run dist:portable

# アップデート用パッケージ
npm run dist:update
```

## 🔧 設定

### package.json設定
```json
{
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "dev": "electron . --dev",
    "build": "electron-builder",
    "dist": "electron-builder --publish=never"
  },
  "build": {
    "appId": "com.example.voice-assistant",
    "productName": "音声アシスタント",
    "directories": {
      "output": "dist"
    },
    "files": [
      "main.js",
      "preload.js",
      "index.html",
      "assets/**/*"
    ],
    "win": {
      "target": "nsis",
      "icon": "assets/icons/icon.ico"
    },
    "mac": {
      "target": "dmg",
      "icon": "assets/icons/icon.icns"
    },
    "linux": {
      "target": "AppImage",
      "icon": "assets/icons/icon.png"
    }
  }
}
```

### 環境変数
```bash
# 開発環境
NODE_ENV=development
API_URL=http://localhost:8000/api

# 本番環境
NODE_ENV=production
API_URL=https://api.example.com
```

## 🐛 デバッグ

### 開発者ツール
```javascript
// メインプロセスでの開発者ツール表示
if (process.env.NODE_ENV === 'development') {
  mainWindow.webContents.openDevTools();
}
```

### ログ出力
```javascript
// electron-logを使用したログ出力
const log = require('electron-log');

log.info('アプリケーション起動');
log.error('エラーが発生しました:', error);
log.debug('デバッグ情報:', data);
```

### 一般的な問題と解決策

1. **アプリが起動しない**
   - Node.jsバージョンの確認
   - 依存関係の再インストール: `npm ci`

2. **IPC通信エラー**
   - preload.jsの読み込み確認
   - contextIsolationの設定確認

3. **マイクアクセスエラー**
   - システムのマイク権限確認
   - ブラウザ権限の設定確認

4. **ホットキーが動作しない**
   - 他のアプリとの競合確認
   - 管理者権限での実行

## 📚 参考資料

- [Electron公式ドキュメント](https://www.electronjs.org/docs)
- [Electron Security](https://www.electronjs.org/docs/tutorial/security)
- [IPC通信ガイド](https://www.electronjs.org/docs/tutorial/ipc)
- [アプリ配布ガイド](https://www.electronjs.org/docs/tutorial/distribution) 