# ローカルモデル

このディレクトリには、オフラインモードで使用するAIモデルファイルを配置します。

## 📁 ディレクトリ構成

```
models/
├── whisper/            # 音声認識モデル（Whisper）
│   ├── tiny/
│   ├── base/
│   ├── small/
│   ├── medium/
│   └── large/
├── llm/                # 大規模言語モデル
│   ├── llama-7b-chat-q4.gguf
│   ├── llama-13b-chat-q4.gguf
│   └── codellama-7b-instruct.gguf
├── tts/                # 音声合成モデル
│   ├── kokoro/         # 日本語女性音声
│   ├── takumi/         # 日本語男性音声
│   └── multilingual/   # 多言語対応
└── sample_audio.wav    # テスト用サンプル音声
```

## 🎤 Whisperモデル（音声認識）

### モデルサイズと性能
| モデル | サイズ | VRAM | 精度 | 速度 |
|--------|--------|------|------|------|
| tiny   | 39MB   | 1GB  | 低   | 高速 |
| base   | 74MB   | 1GB  | 中   | 高速 |
| small  | 244MB  | 2GB  | 中   | 中速 |
| medium | 769MB  | 5GB  | 高   | 中速 |
| large  | 1550MB | 10GB | 最高 | 低速 |

### ダウンロード方法
```bash
# Python環境でWhisperをインストール
pip install openai-whisper

# モデルの自動ダウンロード（初回実行時）
python -c "import whisper; whisper.load_model('base')"
```

### 手動配置
```bash
# Hugging Faceからダウンロード
wget https://huggingface.co/openai/whisper-base/resolve/main/pytorch_model.bin -O models/whisper/base/pytorch_model.bin
```

## 🤖 LLMモデル（大規模言語モデル）

### 推奨モデル
1. **LLaMA 2 7B Chat (Q4)** - バランス型
   - サイズ: 約4GB
   - VRAM: 6GB以上推奨
   - 用途: 一般的な会話

2. **LLaMA 2 13B Chat (Q4)** - 高性能型
   - サイズ: 約8GB
   - VRAM: 12GB以上推奨
   - 用途: 高品質な会話

3. **Code Llama 7B Instruct** - コード特化型
   - サイズ: 約4GB
   - VRAM: 6GB以上推奨
   - 用途: プログラミング支援

### ダウンロード方法
```bash
# LLaMA 2 7B Chat Q4量子化版
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.q4_0.gguf -O models/llm/llama-7b-chat-q4.gguf

# LLaMA 2 13B Chat Q4量子化版
wget https://huggingface.co/TheBloke/Llama-2-13B-Chat-GGUF/resolve/main/llama-2-13b-chat.q4_0.gguf -O models/llm/llama-13b-chat-q4.gguf

# Code Llama 7B Instruct
wget https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF/resolve/main/codellama-7b-instruct.q4_0.gguf -O models/llm/codellama-7b-instruct.gguf
```

### 量子化について
- **Q4_0**: 4bit量子化、サイズ小、速度高、精度中
- **Q5_0**: 5bit量子化、サイズ中、速度中、精度高
- **Q8_0**: 8bit量子化、サイズ大、速度低、精度最高

## 🔊 TTSモデル（音声合成）

### 日本語音声モデル
1. **Kokoro（女性音声）**
   - 自然な日本語発音
   - 感情表現対応

2. **Takumi（男性音声）**
   - 落ち着いた男性音声
   - ビジネス用途に適している

### ダウンロード方法
```bash
# Coqui TTSのインストール
pip install TTS

# 日本語モデルのダウンロード
python -c "from TTS.api import TTS; TTS(model_name='tts_models/ja/kokoro/tacotron2-DDC')"
```

### カスタム音声の作成
```bash
# 音声クローニング用のサンプル音声を準備
# models/tts/custom/sample.wav

# 音声クローニングの実行
python scripts/clone_voice.py --input models/tts/custom/sample.wav --output models/tts/custom/
```

## ⚙️ 設定

### 環境変数での指定
```bash
# .envファイルでモデルパスを指定
WHISPER_MODEL_PATH=models/whisper/base
LLAMA_MODEL_PATH=models/llm/llama-7b-chat-q4.gguf
TTS_MODEL_PATH=models/tts/kokoro
```

### 設定ファイルでの指定
```yaml
# config.yaml
services:
  stt:
    local:
      model_path: "models/whisper/base"
      model_type: "base"
  llm:
    local:
      model_path: "models/llm/llama-7b-chat-q4.gguf"
      context_length: 2048
  tts:
    local:
      model_path: "models/tts/kokoro"
      default_voice: "kokoro"
```

## 💾 ストレージ要件

### 最小構成（約5GB）
- Whisper base: 74MB
- LLaMA 7B Q4: 4GB
- TTS Kokoro: 500MB

### 推奨構成（約10GB）
- Whisper small: 244MB
- LLaMA 13B Q4: 8GB
- TTS複数音声: 1.5GB

### フル構成（約20GB）
- Whisper large: 1.5GB
- LLaMA 13B Q5: 10GB
- 複数LLMモデル: 8GB

## 🚀 パフォーマンス最適化

### GPU使用時
```bash
# CUDA対応PyTorchのインストール
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# GPU使用の確認
python -c "import torch; print(torch.cuda.is_available())"
```

### CPU最適化
```bash
# OpenBLAS最適化
export OPENBLAS_NUM_THREADS=4

# MKL最適化（Intel CPU）
pip install mkl
```

### メモリ最適化
```python
# モデル読み込み時のメモリ最適化
import torch
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = False
```

## 🔧 管理スクリプト

### モデルダウンロードスクリプト
```bash
# 全モデルの一括ダウンロード
python scripts/download_models.py --all

# 特定モデルのダウンロード
python scripts/download_models.py --whisper base --llm llama-7b --tts kokoro
```

### モデル検証スクリプト
```bash
# モデルファイルの整合性チェック
python scripts/verify_models.py

# モデルの動作テスト
python scripts/test_models.py
```

### ディスク使用量確認
```bash
# モデルディレクトリの使用量
du -sh models/

# モデル別の使用量
du -sh models/*/
```

## 🐛 トラブルシューティング

### よくある問題

1. **モデルファイルが見つからない**
   - パスの確認: `ls -la models/`
   - 権限の確認: `chmod 644 models/**/*`

2. **メモリ不足エラー**
   - より小さなモデルを使用
   - スワップファイルの増加
   - 不要なプロセスの終了

3. **GPU認識エラー**
   - CUDAドライバーの確認
   - PyTorchのGPU対応版インストール

4. **音声品質が悪い**
   - より大きなTTSモデルを使用
   - サンプリングレートの調整
   - 音声後処理の適用

### ログ確認
```bash
# モデル読み込みログ
grep "model" logs/app.log

# エラーログ
grep "ERROR" logs/app.log | grep -i model
```

## 📚 参考資料

- [Whisper公式リポジトリ](https://github.com/openai/whisper)
- [LLaMA.cpp](https://github.com/ggerganov/llama.cpp)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [Hugging Face Model Hub](https://huggingface.co/models) 