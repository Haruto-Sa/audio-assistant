const { contextBridge, ipcRenderer } = require('electron');

// APIをウィンドウオブジェクトに公開
contextBridge.exposeInMainWorld('electronAPI', {
  // マイク入力の取得
    getMicrophoneInput: () => ipcRenderer.invoke('get-microphone-input'),

  // STT（音声認識）
    performSTT: (audioPath) => ipcRenderer.invoke('perform-stt', audioPath),
    
  // LLM（テキスト生成）
    performLLM: (text, conversationId) => ipcRenderer.invoke('perform-llm', text, conversationId),
    
  // TTS（音声合成）
    performTTS: (text, voiceId) => ipcRenderer.invoke('perform-tts', text, voiceId),
    
  // 会話履歴の取得
    getConversationHistory: (conversationId) => ipcRenderer.invoke('get-conversation-history', conversationId),
    
  // 設定の保存
    saveSettings: (settings) => ipcRenderer.invoke('save-settings', settings),
    
  // イベントリスナー
    onStartRecording: (callback) => ipcRenderer.on('start-recording', callback),
    onOpenSettings: (callback) => ipcRenderer.on('open-settings', callback),
    
  // リスナーの削除
    removeStartRecordingListener: () => ipcRenderer.removeAllListeners('start-recording'),
    removeOpenSettingsListener: () => ipcRenderer.removeAllListeners('open-settings')
}); 