# テスト

このディレクトリには、音声アシスタントプロジェクトのテストコードが含まれています。

## 📁 ディレクトリ構成

```
tests/
├── unit/                   # ユニットテスト
│   ├── backend/           # バックエンドユニットテスト
│   │   ├── test_api/      # APIエンドポイントテスト
│   │   ├── test_services/ # サービス層テスト
│   │   ├── test_models/   # データモデルテスト
│   │   └── test_utils/    # ユーティリティテスト
│   └── frontend/          # フロントエンドユニットテスト
│       ├── test_electron/ # Electronアプリテスト
│       └── test_mobile/   # モバイルアプリテスト
├── integration/            # 統合テスト
│   ├── test_api_integration.py    # API統合テスト
│   ├── test_stt_llm_tts.py       # STT→LLM→TTS統合テスト
│   └── test_database.py          # データベース統合テスト
├── e2e/                   # E2Eテスト
│   ├── test_electron_app.py      # Electronアプリ全体テスト
│   ├── test_voice_workflow.py    # 音声処理ワークフローテスト
│   └── test_mobile_app.py        # モバイルアプリテスト
├── performance/           # パフォーマンステスト
│   ├── test_stt_performance.py   # STT性能テスト
│   ├── test_llm_performance.py   # LLM性能テスト
│   └── test_tts_performance.py   # TTS性能テスト
├── fixtures/              # テストデータ
│   ├── audio/            # テスト用音声ファイル
│   ├── models/           # テスト用モデル
│   └── data/             # テストデータ
├── conftest.py            # pytest設定
├── jest.config.js         # Jest設定（フロントエンド）
└── playwright.config.js   # Playwright設定（E2E）
```

## 🧪 テストの種類

### 1. ユニットテスト
個別のモジュール・関数・クラスの動作を検証します。

#### バックエンド（Python + pytest）
```bash
# 全ユニットテスト実行
pytest tests/unit/backend/

# 特定モジュールのテスト
pytest tests/unit/backend/test_services/test_stt_service.py

# カバレッジ付きテスト
pytest tests/unit/backend/ --cov=src/backend --cov-report=html
```

#### フロントエンド（JavaScript + Jest）
```bash
# Electronアプリのテスト
cd src/frontend/electron
npm test

# 特定ファイルのテスト
npm test -- --testPathPattern=main.test.js

# ウォッチモード
npm test -- --watch
```

### 2. 統合テスト
複数のモジュール間の連携を検証します。

```bash
# API統合テスト
pytest tests/integration/test_api_integration.py

# STT→LLM→TTS統合テスト
pytest tests/integration/test_stt_llm_tts.py

# データベース統合テスト
pytest tests/integration/test_database.py
```

### 3. E2Eテスト
アプリケーション全体の動作を検証します。

```bash
# Electronアプリ E2Eテスト
npx playwright test tests/e2e/test_electron_app.py

# 音声処理ワークフローテスト
pytest tests/e2e/test_voice_workflow.py

# ヘッドレスモードで実行
npx playwright test --headed=false
```

### 4. パフォーマンステスト
システムの性能を測定・検証します。

```bash
# STT性能テスト
pytest tests/performance/test_stt_performance.py

# LLM性能テスト
pytest tests/performance/test_llm_performance.py

# ベンチマークレポート生成
pytest tests/performance/ --benchmark-only --benchmark-html=reports/benchmark.html
```

## ⚙️ テスト設定

### pytest設定（conftest.py）
```python
import pytest
import asyncio
from unittest.mock import Mock
from src.backend.utils.config import Config
from src.backend.services.db import DatabaseService

@pytest.fixture(scope="session")
def event_loop():
    """イベントループのフィクスチャ"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_config():
    """設定のモック"""
    config = Mock(spec=Config)
    config.USE_LOCAL_MODE = True
    config.OPENAI_API_KEY = "test_key"
    return config

@pytest.fixture
async def test_db():
    """テスト用データベース"""
    db = DatabaseService(database_url="sqlite:///:memory:")
    await db.init_tables()
    yield db
    await db.close()

@pytest.fixture
def sample_audio_file():
    """サンプル音声ファイル"""
    return "tests/fixtures/audio/sample.wav"
```

### Jest設定（jest.config.js）
```javascript
module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: [
    '**/__tests__/**/*.+(ts|tsx|js)',
    '**/*.(test|spec).+(ts|tsx|js)'
  ],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest'
  },
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html']
};
```

### Playwright設定（playwright.config.js）
```javascript
module.exports = {
  testDir: './tests/e2e',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    actionTimeout: 0,
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'electron',
      use: { 
        ...devices['Desktop Chrome'],
        channel: 'chrome'
      }
    }
  ]
};
```

## 📊 テストデータ

### 音声ファイル（fixtures/audio/）
```
audio/
├── sample_short.wav      # 短い音声（5秒）
├── sample_medium.wav     # 中程度の音声（30秒）
├── sample_long.wav       # 長い音声（2分）
├── japanese_speech.wav   # 日本語音声
├── english_speech.wav    # 英語音声
├── noisy_audio.wav       # ノイズ入り音声
└── silent.wav           # 無音ファイル
```

### テストモデル（fixtures/models/）
```
models/
├── whisper_tiny/         # 軽量Whisperモデル
├── llama_test/          # テスト用LLMモデル
└── tts_test/            # テスト用TTSモデル
```

### テストデータ（fixtures/data/）
```python
# test_conversations.json
{
  "conversations": [
    {
      "id": "test_conv_1",
      "messages": [
        {"role": "user", "content": "こんにちは"},
        {"role": "assistant", "content": "こんにちは！何かお手伝いできることはありますか？"}
      ]
    }
  ]
}
```

## 🚀 テスト実行

### 全テスト実行
```bash
# 全テスト（バックエンド + フロントエンド）
python scripts/dev/run_tests.py

# バックエンドのみ
pytest

# フロントエンドのみ
cd src/frontend/electron && npm test
```

### 特定カテゴリのテスト
```bash
# ユニットテストのみ
pytest tests/unit/

# 統合テストのみ
pytest tests/integration/

# E2Eテストのみ
npx playwright test

# パフォーマンステストのみ
pytest tests/performance/
```

### 詳細オプション
```bash
# 詳細出力
pytest -v

# 失敗時に停止
pytest -x

# 並列実行
pytest -n auto

# 特定のマーカーのみ
pytest -m "not slow"

# カバレッジレポート
pytest --cov=src --cov-report=html
```

## 📈 テストレポート

### カバレッジレポート
```bash
# HTMLレポート生成
pytest --cov=src --cov-report=html

# レポート確認
open htmlcov/index.html
```

### パフォーマンスレポート
```bash
# ベンチマークレポート
pytest tests/performance/ --benchmark-html=reports/benchmark.html

# メモリプロファイル
pytest tests/performance/ --profile
```

### E2Eテストレポート
```bash
# Playwrightレポート
npx playwright show-report

# スクリーンショット付きレポート
npx playwright test --reporter=html
```

## 🏷️ テストマーカー

### pytest マーカー
```python
import pytest

@pytest.mark.unit
def test_stt_service():
    """ユニットテスト"""
    pass

@pytest.mark.integration
def test_api_integration():
    """統合テスト"""
    pass

@pytest.mark.slow
def test_large_model():
    """時間のかかるテスト"""
    pass

@pytest.mark.gpu
def test_gpu_acceleration():
    """GPU必須テスト"""
    pass

@pytest.mark.parametrize("model_size", ["tiny", "base", "small"])
def test_whisper_models(model_size):
    """パラメータ化テスト"""
    pass
```

### 実行例
```bash
# 高速テストのみ
pytest -m "not slow"

# GPU必須テストを除外
pytest -m "not gpu"

# 統合テストのみ
pytest -m integration
```

## 🔧 モック・スタブ

### APIモック
```python
import pytest
from unittest.mock import Mock, patch

@patch('src.backend.services.stt_service.openai.Audio.transcribe')
def test_cloud_stt_service(mock_transcribe):
    """OpenAI APIのモック"""
    mock_transcribe.return_value = {"text": "テスト音声"}
    # テスト実行
```

### データベースモック
```python
@pytest.fixture
def mock_db():
    """データベースのモック"""
    db = Mock()
    db.save_conversation.return_value = "conv_123"
    db.get_conversation.return_value = {"id": "conv_123"}
    return db
```

### ファイルシステムモック
```python
from unittest.mock import mock_open, patch

@patch('builtins.open', new_callable=mock_open, read_data='test audio data')
def test_audio_file_processing(mock_file):
    """ファイル読み込みのモック"""
    # テスト実行
```

## 🐛 テストデバッグ

### デバッグ実行
```bash
# pdbデバッガー付きテスト
pytest --pdb

# 失敗時のみpdb起動
pytest --pdb-trace

# ログ出力付きテスト
pytest -s --log-cli-level=DEBUG
```

### テスト分離
```bash
# 特定のテストのみ実行
pytest tests/unit/backend/test_services/test_stt_service.py::test_local_whisper

# キーワード検索
pytest -k "stt and not slow"
```

## 📚 テスト作成ガイド

### ユニットテストの例
```python
import pytest
from src.backend.services.stt_service import LocalWhisperService

class TestLocalWhisperService:
    """STTサービスのテストクラス"""
    
    @pytest.fixture
    def stt_service(self, mock_config):
        """STTサービスのフィクスチャ"""
        return LocalWhisperService(mock_config)
    
    def test_transcribe_audio(self, stt_service, sample_audio_file):
        """音声認識テスト"""
        result = stt_service.transcribe(sample_audio_file)
        assert result["text"] is not None
        assert len(result["text"]) > 0
    
    def test_invalid_audio_file(self, stt_service):
        """無効な音声ファイルのテスト"""
        with pytest.raises(FileNotFoundError):
            stt_service.transcribe("nonexistent.wav")
```

### 統合テストの例
```python
import pytest
import asyncio

@pytest.mark.integration
class TestVoiceWorkflow:
    """音声処理ワークフローの統合テスト"""
    
    async def test_full_voice_workflow(self, test_app, sample_audio_file):
        """STT→LLM→TTSの完全ワークフロー"""
        # 1. 音声認識
        stt_response = await test_app.post(
            "/api/stt/transcribe",
            files={"file": open(sample_audio_file, "rb")}
        )
        assert stt_response.status_code == 200
        text = stt_response.json()["text"]
        
        # 2. テキスト生成
        llm_response = await test_app.post(
            "/api/llm/chat",
            json={"messages": [{"role": "user", "content": text}]}
        )
        assert llm_response.status_code == 200
        reply = llm_response.json()["response"]
        
        # 3. 音声合成
        tts_response = await test_app.post(
            "/api/tts/synthesize",
            json={"text": reply}
        )
        assert tts_response.status_code == 200
        assert tts_response.headers["content-type"] == "audio/wav"
```

## 🔄 CI/CD統合

### GitHub Actions設定
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### テスト自動化
```bash
# pre-commitフック設定
pip install pre-commit
pre-commit install

# コミット前に自動テスト実行
git commit -m "新機能追加"
```

## 📋 テストチェックリスト

### 新機能追加時
- [ ] ユニットテストの作成
- [ ] 統合テストの更新
- [ ] E2Eテストの確認
- [ ] パフォーマンステストの実行
- [ ] カバレッジの確認（80%以上）

### リリース前
- [ ] 全テストの実行
- [ ] パフォーマンステストの実行
- [ ] E2Eテストの実行
- [ ] テストレポートの確認
- [ ] カバレッジレポートの確認 