# CI/CD

このディレクトリには、継続的インテグレーション（CI）と継続的デプロイメント（CD）の設定ファイルが含まれています。

## 📁 ディレクトリ構成

```
ci/
├── github/                 # GitHub Actions設定
│   ├── workflows/         # ワークフロー定義
│   │   ├── test.yml      # テスト実行
│   │   ├── build.yml     # ビルド・パッケージング
│   │   ├── deploy.yml    # デプロイメント
│   │   └── release.yml   # リリース作成
│   └── actions/          # カスタムアクション
│       ├── setup-env/    # 環境セットアップ
│       └── deploy-app/   # アプリデプロイ
├── docker/               # Docker設定
│   ├── Dockerfile        # アプリケーション用
│   ├── Dockerfile.dev    # 開発環境用
│   └── docker-compose.yml # 複数サービス構成
├── scripts/              # CI/CD用スクリプト
│   ├── setup-ci.sh      # CI環境セットアップ
│   ├── run-tests.sh     # テスト実行スクリプト
│   ├── build-app.sh     # ビルドスクリプト
│   └── deploy.sh        # デプロイスクリプト
└── config/               # 設定ファイル
    ├── eslint.config.js  # ESLint設定
    ├── pytest.ini       # pytest設定
    └── sonar-project.properties # SonarQube設定
```

## 🔄 GitHub Actions ワークフロー

### test.yml - テスト実行
```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov pytest-xdist
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=src/backend --cov-report=xml
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: backend
        name: backend-coverage

  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: src/frontend/electron/package-lock.json
    
    - name: Install dependencies
      run: |
        cd src/frontend/electron
        npm ci
    
    - name: Run tests
      run: |
        cd src/frontend/electron
        npm test -- --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        directory: src/frontend/electron/coverage
        flags: frontend
        name: frontend-coverage

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        cd src/frontend/electron && npm ci
        npx playwright install
    
    - name: Start backend server
      run: |
        cd src/backend
        python main.py &
        sleep 10
    
    - name: Run E2E tests
      run: |
        npx playwright test
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: playwright-report
        path: playwright-report/
```

### build.yml - ビルド・パッケージング
```yaml
name: Build

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-electron:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: src/frontend/electron/package-lock.json
    
    - name: Install dependencies
      run: |
        cd src/frontend/electron
        npm ci
    
    - name: Build application
      run: |
        cd src/frontend/electron
        npm run build
    
    - name: Package application
      run: |
        cd src/frontend/electron
        npm run dist
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: electron-app-${{ matrix.os }}
        path: src/frontend/electron/dist/

  build-backend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pyinstaller
    
    - name: Build backend
      run: |
        cd src/backend
        pyinstaller --onefile main.py
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: backend-executable
        path: src/backend/dist/
```

### deploy.yml - デプロイメント
```yaml
name: Deploy

on:
  push:
    branches: [ main ]
  workflow_run:
    workflows: ["Tests", "Build"]
    types:
      - completed

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to staging
      run: |
        echo "Deploying to staging environment"
        # ステージング環境へのデプロイロジック

  deploy-production:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "Deploying to production environment"
        # 本番環境へのデプロイロジック
```

### release.yml - リリース作成
```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Create Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
    
    - name: Upload Release Assets
      # リリースアセットのアップロード
```

## 🐳 Docker設定

### Dockerfile - アプリケーション用
```dockerfile
# マルチステージビルド
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY src/frontend/electron/package*.json ./
RUN npm ci --only=production

COPY src/frontend/electron/ ./
RUN npm run build

FROM python:3.9-slim AS backend-builder

WORKDIR /app/backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend/ ./

FROM python:3.9-slim AS runtime

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Pythonアプリケーションのコピー
COPY --from=backend-builder /app/backend ./backend
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# フロントエンドビルド成果物のコピー
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

CMD ["python", "backend/main.py"]
```

### Dockerfile.dev - 開発環境用
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# システム依存関係
RUN apt-get update && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 開発用依存関係
RUN pip install pytest pytest-cov black isort

# Node.js依存関係
COPY src/frontend/electron/package*.json ./frontend/
RUN cd frontend && npm install

# ソースコードのマウント用ボリューム
VOLUME ["/app/src"]

CMD ["python", "src/backend/main.py"]
```

### docker-compose.yml - 複数サービス構成
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: ci/docker/Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
      - ./models:/app/models
    environment:
      - USE_LOCAL_MODE=true
      - DATABASE_URL=postgresql://user:password@db:5432/voice_assistant
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: voice_assistant
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./ci/config/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend

volumes:
  postgres_data:
```

## 📜 CI/CD用スクリプト

### setup-ci.sh - CI環境セットアップ
```bash
#!/bin/bash
set -e

echo "Setting up CI environment..."

# Python環境のセットアップ
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov pytest-xdist black isort

# Node.js環境のセットアップ
cd src/frontend/electron
npm ci
npx playwright install

# モデルファイルのダウンロード（軽量版）
cd ../../../
python scripts/models/download_models.py --lightweight

echo "CI environment setup completed!"
```

### run-tests.sh - テスト実行スクリプト
```bash
#!/bin/bash
set -e

echo "Running tests..."

# バックエンドテスト
echo "Running backend tests..."
pytest tests/unit/backend/ -v --cov=src/backend --cov-report=xml

# フロントエンドテスト
echo "Running frontend tests..."
cd src/frontend/electron
npm test -- --coverage
cd ../../../

# 統合テスト
echo "Running integration tests..."
pytest tests/integration/ -v

# E2Eテスト（オプション）
if [ "$RUN_E2E" = "true" ]; then
    echo "Running E2E tests..."
    npx playwright test
fi

echo "All tests completed!"
```

### build-app.sh - ビルドスクリプト
```bash
#!/bin/bash
set -e

echo "Building application..."

# バックエンドビルド
echo "Building backend..."
cd src/backend
pip install pyinstaller
pyinstaller --onefile main.py
cd ../../

# フロントエンドビルド
echo "Building frontend..."
cd src/frontend/electron
npm run build
npm run dist
cd ../../../

echo "Build completed!"
```

## ⚙️ 設定ファイル

### eslint.config.js - ESLint設定
```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended'
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module'
  },
  plugins: [
    '@typescript-eslint'
  ],
  rules: {
    'indent': ['error', 2],
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always']
  }
};
```

### pytest.ini - pytest設定
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    gpu: Tests requiring GPU
```

### sonar-project.properties - SonarQube設定
```properties
sonar.projectKey=voice-assistant
sonar.projectName=Voice Assistant
sonar.projectVersion=1.0

sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/dist/**,**/coverage/**

sonar.python.coverage.reportPaths=coverage.xml
sonar.javascript.lcov.reportPaths=src/frontend/electron/coverage/lcov.info

sonar.python.xunit.reportPath=test-results.xml
```

## 🔧 環境別設定

### 開発環境
```yaml
# .github/workflows/dev.yml
name: Development

on:
  push:
    branches: [ develop ]

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Run tests
      run: ./ci/scripts/run-tests.sh
    
    - name: Deploy to dev environment
      run: ./ci/scripts/deploy.sh dev
```

### ステージング環境
```yaml
# .github/workflows/staging.yml
name: Staging

on:
  push:
    branches: [ staging ]

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
    - name: Deploy to staging
      run: ./ci/scripts/deploy.sh staging
```

### 本番環境
```yaml
# .github/workflows/production.yml
name: Production

on:
  push:
    branches: [ main ]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
    - name: Deploy to production
      run: ./ci/scripts/deploy.sh production
```

## 📊 品質管理

### コードカバレッジ
- **目標**: 80%以上
- **ツール**: pytest-cov, Jest
- **レポート**: Codecov

### 静的解析
- **Python**: Black, isort, flake8, mypy
- **JavaScript/TypeScript**: ESLint, Prettier
- **セキュリティ**: Bandit, npm audit

### パフォーマンス監視
- **ベンチマーク**: pytest-benchmark
- **プロファイリング**: cProfile, memory_profiler
- **監視**: New Relic, DataDog

## 🚀 デプロイメント戦略

### ブルーグリーンデプロイ
```bash
# 新バージョンのデプロイ
./ci/scripts/deploy.sh production --strategy=blue-green

# ヘルスチェック後の切り替え
./ci/scripts/switch-traffic.sh blue-to-green
```

### カナリアデプロイ
```bash
# 一部トラフィックでのテスト
./ci/scripts/deploy.sh production --strategy=canary --traffic=10%

# 段階的なトラフィック増加
./ci/scripts/scale-traffic.sh --target=50%
```

### ロールバック
```bash
# 前バージョンへのロールバック
./ci/scripts/rollback.sh production --version=v1.2.3
```

## 🔐 セキュリティ

### シークレット管理
```yaml
# GitHub Secrets
OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
DEPLOY_SSH_KEY: ${{ secrets.DEPLOY_SSH_KEY }}
```

### 脆弱性スキャン
```yaml
- name: Security scan
  uses: github/super-linter@v4
  env:
    DEFAULT_BRANCH: main
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📈 監視・アラート

### ヘルスチェック
```bash
# アプリケーションの健全性確認
curl -f http://localhost:8000/health || exit 1
```

### ログ監視
```yaml
- name: Check logs for errors
  run: |
    if grep -q "ERROR" logs/app.log; then
      echo "Errors found in logs"
      exit 1
    fi
```

## 🐛 トラブルシューティング

### よくある問題

1. **テスト失敗**
   - ログの確認: `cat test-results.xml`
   - 依存関係の更新: `pip install -r requirements.txt --upgrade`

2. **ビルド失敗**
   - キャッシュのクリア: `npm ci --cache .npm`
   - 権限の確認: `chmod +x ci/scripts/*.sh`

3. **デプロイ失敗**
   - 接続確認: `ssh -T git@github.com`
   - 環境変数の確認: `echo $DEPLOY_SSH_KEY`

### ログ確認
```bash
# GitHub Actionsログ
gh run list
gh run view <run-id>

# ローカルログ
tail -f logs/ci.log
``` 