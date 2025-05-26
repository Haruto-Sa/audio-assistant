#!/usr/bin/env python3
"""
音声アシスタントプロジェクトのセットアップスクリプト
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8以上が必要です。")
        print(f"現在のバージョン: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def create_directories():
    """必要なディレクトリを作成"""
    directories = [
        "models",
        "logs",
        "tmp",
        "src/frontend/mobile"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ ディレクトリ作成: {directory}")

def install_requirements():
    """依存パッケージをインストール"""
    print("📦 依存パッケージをインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依存パッケージのインストール完了")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存パッケージのインストールに失敗: {e}")
        return False

def create_env_file():
    """環境変数ファイルを作成"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("✅ .envファイルを作成しました")
            print("⚠️  .envファイルを編集して必要な設定を行ってください")
        else:
            print("⚠️  .env.exampleファイルが見つかりません")
    else:
        print("✅ .envファイルは既に存在します")

def test_server():
    """サーバーのテスト起動"""
    print("🧪 サーバーのテスト起動中...")
    try:
        # サーバーを短時間起動してテスト
        import sys
        sys.path.append("src/backend")
        
        # インポートテスト
        from services.tts_service import get_tts_service
        from services.stt_service import get_stt_service
        from services.llm_service import get_llm_service
        
        print("✅ 全てのサービスが正常にインポートされました")
        return True
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🚀 音声アシスタントプロジェクトのセットアップを開始します")
    print("=" * 50)
    
    # Python バージョンチェック
    if not check_python_version():
        sys.exit(1)
    
    # ディレクトリ作成
    create_directories()
    
    # 依存パッケージインストール
    if not install_requirements():
        sys.exit(1)
    
    # 環境変数ファイル作成
    create_env_file()
    
    # サーバーテスト
    if not test_server():
        print("⚠️  サーバーテストに失敗しましたが、セットアップは継続します")
    
    print("=" * 50)
    print("✅ セットアップが完了しました！")
    print()
    print("次のステップ:")
    print("1. .envファイルを編集して必要な設定を行う")
    print("2. python start_server.py でサーバーを起動")
    print("3. ブラウザで http://localhost:8000/docs にアクセス")

if __name__ == "__main__":
    main() 