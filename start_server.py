#!/usr/bin/env python3
"""
音声アシスタントサーバーの安全な起動スクリプト
"""

import os
import sys
import signal
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """依存関係をチェック"""
    try:
        import fastapi
        import uvicorn
        print("✅ 基本依存パッケージが利用可能です")
        return True
    except ImportError as e:
        print(f"❌ 依存パッケージが不足しています: {e}")
        print("python setup.py を実行してセットアップを完了してください")
        return False

def check_environment():
    """環境設定をチェック"""
    if not os.path.exists(".env"):
        print("⚠️  .envファイルが見つかりません")
        if os.path.exists(".env.example"):
            print("python setup.py を実行して.envファイルを作成してください")
        return False
    
    print("✅ 環境設定ファイルが見つかりました")
    return True

def test_imports():
    """重要なモジュールのインポートテスト"""
    try:
        # バックエンドディレクトリをパスに追加
        backend_path = Path("src/backend").resolve()
        if str(backend_path) not in sys.path:
            sys.path.insert(0, str(backend_path))
        
        # 重要なサービスのインポートテスト
        from services.tts_service import get_tts_service
        from services.stt_service import get_stt_service
        from services.llm_service import get_llm_service
        
        print("✅ 全てのサービスモジュールが正常にインポートされました")
        return True
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("モジュールの依存関係に問題があります")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def start_server():
    """サーバーを起動"""
    print("🚀 音声アシスタントサーバーを起動中...")
    
    # 作業ディレクトリをバックエンドに変更
    backend_dir = Path("src/backend")
    
    try:
        # uvicornでサーバーを起動
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--reload-dir", ".",
            "--log-level", "info"
        ]
        
        print(f"実行コマンド: {' '.join(cmd)}")
        print(f"作業ディレクトリ: {backend_dir.resolve()}")
        print("=" * 50)
        
        # サーバープロセスを起動
        process = subprocess.Popen(
            cmd,
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # シグナルハンドラーを設定（Ctrl+Cでの安全な終了）
        def signal_handler(sig, frame):
            print("\n🛑 サーバーを停止中...")
            process.terminate()
            process.wait()
            print("✅ サーバーが正常に停止しました")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # サーバーの出力をリアルタイムで表示
        print("サーバーログ:")
        print("-" * 30)
        
        for line in process.stdout:
            print(line.strip())
            
            # サーバーが正常に起動したかチェック
            if "Application startup complete" in line:
                print("\n✅ サーバーが正常に起動しました！")
                print("🌐 http://localhost:8000 でアクセス可能です")
                print("📚 API仕様書: http://localhost:8000/docs")
                print("🛑 停止するには Ctrl+C を押してください")
                print("-" * 30)
        
        # プロセスの終了を待機
        process.wait()
        
    except FileNotFoundError:
        print("❌ uvicornが見つかりません。依存パッケージをインストールしてください")
        return False
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🎤 音声アシスタント サーバー起動スクリプト")
    print("=" * 50)
    
    # 依存関係チェック
    if not check_dependencies():
        sys.exit(1)
    
    # 環境設定チェック
    if not check_environment():
        sys.exit(1)
    
    # インポートテスト
    if not test_imports():
        print("\n💡 ヒント:")
        print("- python setup.py を実行してセットアップを完了してください")
        print("- requirements.txtの依存パッケージがインストールされているか確認してください")
        sys.exit(1)
    
    print("\n🎯 全ての事前チェックが完了しました")
    print("=" * 50)
    
    # サーバー起動
    start_server()

if __name__ == "__main__":
    main() 