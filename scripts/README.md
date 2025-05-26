# スクリプト

このディレクトリには、開発・運用・メンテナンス用のスクリプトが含まれています。

## 📁 ディレクトリ構成

```
scripts/
├── setup/              # セットアップ関連
│   ├── install_deps.py    # 依存関係の一括インストール
│   ├── setup_env.py       # 環境設定の自動化
│   └── init_db.py         # データベース初期化
├── models/             # モデル管理
│   ├── download_models.py # モデルファイルのダウンロード
│   ├── verify_models.py   # モデルの整合性チェック
│   └── test_models.py     # モデルの動作テスト
├── dev/                # 開発支援
│   ├── start_dev.py       # 開発環境の起動
│   ├── run_tests.py       # テストの実行
│   └── format_code.py     # コードフォーマット
├── deploy/             # デプロイ関連
│   ├── build_app.py       # アプリケーションビルド
│   ├── package_dist.py    # 配布パッケージ作成
│   └── deploy_server.py   # サーバーデプロイ
└── utils/              # ユーティリティ
    ├── backup_data.py     # データバックアップ
    ├── cleanup.py         # 不要ファイル削除
    └── health_check.py    # システムヘルスチェック
```

## 🚀 セットアップスクリプト

### install_deps.py
プロジェクトの依存関係を一括インストールします。

```bash
# 基本インストール
python scripts/setup/install_deps.py

# GPU対応版のインストール
python scripts/setup/install_deps.py --gpu

# 開発用依存関係も含める
python scripts/setup/install_deps.py --dev
```

**機能:**
- Python依存パッケージのインストール
- Node.js依存関係のインストール
- システム要件のチェック
- GPU対応ライブラリの選択的インストール

### setup_env.py
環境設定を自動化します。

```bash
# 基本環境設定
python scripts/setup/setup_env.py

# 本番環境用設定
python scripts/setup/setup_env.py --production

# カスタム設定ファイルを使用
python scripts/setup/setup_env.py --config custom_config.yaml
```

**機能:**
- .envファイルの生成
- 設定ファイルのテンプレート作成
- ディレクトリ権限の設定
- ログディレクトリの作成

### init_db.py
データベースの初期化を行います。

```bash
# データベース初期化
python scripts/setup/init_db.py

# テストデータも含める
python scripts/setup/init_db.py --with-test-data

# 既存データを削除して再初期化
python scripts/setup/init_db.py --reset
```

**機能:**
- Supabaseプロジェクトの設定確認
- テーブルの作成
- 初期データの投入
- インデックスの作成

## 🤖 モデル管理スクリプト

### download_models.py
AIモデルファイルのダウンロードを自動化します。

```bash
# 全モデルのダウンロード
python scripts/models/download_models.py --all

# 特定モデルのダウンロード
python scripts/models/download_models.py --whisper base --llm llama-7b --tts kokoro

# 軽量版モデルのみ
python scripts/models/download_models.py --lightweight

# 進行状況を表示
python scripts/models/download_models.py --all --verbose
```

**機能:**
- Hugging Faceからのモデルダウンロード
- ダウンロード進行状況の表示
- ファイル整合性の検証
- 自動的なディレクトリ作成

### verify_models.py
モデルファイルの整合性をチェックします。

```bash
# 全モデルの検証
python scripts/models/verify_models.py

# 特定モデルの検証
python scripts/models/verify_models.py --model whisper/base

# 詳細レポート出力
python scripts/models/verify_models.py --detailed
```

**機能:**
- ファイルサイズの確認
- チェックサムの検証
- モデル読み込みテスト
- 破損ファイルの検出

### test_models.py
モデルの動作テストを実行します。

```bash
# 全モデルのテスト
python scripts/models/test_models.py

# 特定モデルのテスト
python scripts/models/test_models.py --stt --llm

# ベンチマークテスト
python scripts/models/test_models.py --benchmark
```

**機能:**
- STT/LLM/TTSの動作確認
- パフォーマンス測定
- メモリ使用量の監視
- エラーレポートの生成

## 🛠️ 開発支援スクリプト

### start_dev.py
開発環境を一括起動します。

```bash
# 開発環境の起動
python scripts/dev/start_dev.py

# バックエンドのみ起動
python scripts/dev/start_dev.py --backend-only

# フロントエンドのみ起動
python scripts/dev/start_dev.py --frontend-only

# デバッグモードで起動
python scripts/dev/start_dev.py --debug
```

**機能:**
- バックエンドサーバーの起動
- Electronアプリの起動
- ホットリロードの有効化
- ログ出力の統合表示

### run_tests.py
テストスイートを実行します。

```bash
# 全テストの実行
python scripts/dev/run_tests.py

# ユニットテストのみ
python scripts/dev/run_tests.py --unit

# E2Eテストのみ
python scripts/dev/run_tests.py --e2e

# カバレッジレポート付き
python scripts/dev/run_tests.py --coverage
```

**機能:**
- pytest/jestテストの実行
- カバレッジレポートの生成
- テスト結果のHTML出力
- CI/CD連携

### format_code.py
コードフォーマットを実行します。

```bash
# 全ファイルのフォーマット
python scripts/dev/format_code.py

# Pythonファイルのみ
python scripts/dev/format_code.py --python

# TypeScriptファイルのみ
python scripts/dev/format_code.py --typescript

# チェックのみ（修正しない）
python scripts/dev/format_code.py --check
```

**機能:**
- Black（Python）によるフォーマット
- Prettier（TypeScript）によるフォーマット
- isortによるインポート整理
- ESLintによる構文チェック

## 📦 デプロイスクリプト

### build_app.py
アプリケーションをビルドします。

```bash
# 開発ビルド
python scripts/deploy/build_app.py

# 本番ビルド
python scripts/deploy/build_app.py --production

# 特定プラットフォーム向け
python scripts/deploy/build_app.py --platform windows

# 全プラットフォーム
python scripts/deploy/build_app.py --all-platforms
```

**機能:**
- Electronアプリのビルド
- 依存関係の最適化
- アセットの圧縮
- プラットフォーム別パッケージング

### package_dist.py
配布パッケージを作成します。

```bash
# 配布パッケージ作成
python scripts/deploy/package_dist.py

# インストーラー作成
python scripts/deploy/package_dist.py --installer

# ポータブル版作成
python scripts/deploy/package_dist.py --portable

# 署名付きパッケージ
python scripts/deploy/package_dist.py --signed
```

**機能:**
- 実行ファイルの作成
- インストーラーの生成
- デジタル署名の適用
- 配布用アーカイブの作成

### deploy_server.py
サーバーへのデプロイを実行します。

```bash
# 本番サーバーへのデプロイ
python scripts/deploy/deploy_server.py --production

# ステージング環境へのデプロイ
python scripts/deploy/deploy_server.py --staging

# ロールバック
python scripts/deploy/deploy_server.py --rollback
```

**機能:**
- サーバーへのファイル転送
- サービスの再起動
- ヘルスチェック
- ロールバック機能

## 🔧 ユーティリティスクリプト

### backup_data.py
データのバックアップを実行します。

```bash
# 全データのバックアップ
python scripts/utils/backup_data.py

# データベースのみ
python scripts/utils/backup_data.py --database-only

# 設定ファイルのみ
python scripts/utils/backup_data.py --config-only

# 自動バックアップ設定
python scripts/utils/backup_data.py --schedule daily
```

**機能:**
- データベースのダンプ
- 設定ファイルのバックアップ
- ログファイルのアーカイブ
- 自動バックアップのスケジューリング

### cleanup.py
不要ファイルの削除を行います。

```bash
# 一般的な不要ファイル削除
python scripts/utils/cleanup.py

# ログファイルの削除
python scripts/utils/cleanup.py --logs

# キャッシュファイルの削除
python scripts/utils/cleanup.py --cache

# 古いバックアップの削除
python scripts/utils/cleanup.py --old-backups
```

**機能:**
- 一時ファイルの削除
- 古いログファイルの削除
- キャッシュのクリア
- 不要なバックアップの削除

### health_check.py
システムの健全性をチェックします。

```bash
# 基本ヘルスチェック
python scripts/utils/health_check.py

# 詳細チェック
python scripts/utils/health_check.py --detailed

# 継続監視モード
python scripts/utils/health_check.py --monitor

# レポート出力
python scripts/utils/health_check.py --report
```

**機能:**
- サーバーの応答確認
- データベース接続テスト
- ディスク使用量チェック
- メモリ使用量監視

## ⚙️ 共通設定

### 環境変数
```bash
# スクリプト共通の環境変数
export SCRIPT_LOG_LEVEL=INFO
export SCRIPT_OUTPUT_DIR=logs/scripts
export SCRIPT_CONFIG_FILE=config/scripts.yaml
```

### 設定ファイル
```yaml
# config/scripts.yaml
scripts:
  models:
    download_timeout: 3600
    verify_checksum: true
  dev:
    auto_reload: true
    open_browser: true
  deploy:
    backup_before_deploy: true
    health_check_timeout: 300
```

## 🧪 テスト

### スクリプトテスト
```bash
# スクリプトのテスト実行
python -m pytest tests/scripts/

# 特定スクリプトのテスト
python -m pytest tests/scripts/test_download_models.py
```

### 統合テスト
```bash
# スクリプト間の連携テスト
python scripts/dev/run_tests.py --integration
```

## 📚 カスタムスクリプト作成

### テンプレート
```python
#!/usr/bin/env python3
"""
カスタムスクリプトのテンプレート
"""
import argparse
import logging
from pathlib import Path

def setup_logging():
    """ログ設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='カスタムスクリプト')
    parser.add_argument('--verbose', action='store_true', help='詳細出力')
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("スクリプト開始")
    # ここに処理を記述
    logger.info("スクリプト完了")

if __name__ == '__main__':
    main()
```

### 実行権限の設定
```bash
# スクリプトに実行権限を付与
chmod +x scripts/custom/my_script.py

# 全スクリプトに実行権限を付与
find scripts/ -name "*.py" -exec chmod +x {} \;
```

## 🐛 トラブルシューティング

### よくある問題

1. **権限エラー**
   ```bash
   # 実行権限の確認
   ls -la scripts/
   
   # 権限の修正
   chmod +x scripts/**/*.py
   ```

2. **依存関係エラー**
   ```bash
   # 依存関係の再インストール
   python scripts/setup/install_deps.py --force
   ```

3. **パスエラー**
   ```bash
   # 作業ディレクトリの確認
   pwd
   
   # プロジェクトルートから実行
   cd /path/to/project
   python scripts/...
   ```

### ログ確認
```bash
# スクリプトログの確認
tail -f logs/scripts/script.log

# エラーログの確認
grep ERROR logs/scripts/*.log
``` 