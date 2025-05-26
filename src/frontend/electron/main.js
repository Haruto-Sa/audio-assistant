const { app, BrowserWindow, ipcMain, globalShortcut, Tray, Menu } = require('electron');
const path = require('path');
const fs = require('fs');
const axios = require('axios');
const log = require('electron-log');
const settings = require('electron-settings');
const { createClient } = require('@supabase/supabase-js');

// ロギング設定
log.transports.file.level = 'info';
log.info('アプリケーション起動中...');

// 環境変数のロード
require('dotenv').config({ path: path.join(__dirname, '.env') });

// バックエンドAPIのURL
const API_URL = process.env.API_URL || 'http://localhost:8000/api';

// Supabase設定
const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_KEY;
let supabaseClient = null;

if (supabaseUrl && supabaseKey) {
    supabaseClient = createClient(supabaseUrl, supabaseKey);
    log.info('Supabaseクライアント初期化完了');
}

// ウィンドウ参照の保持（ガベージコレクション対策）
let mainWindow;
let tray;

// ユーザー設定のロード
async function loadSettings() {
    const defaultSettings = {
    useLocalMode: false,
    apiUrl: API_URL,
    hotkey: 'CommandOrControl+Shift+Space',
    theme: 'system',
    volume: 0.8,
    saveHistory: true
    };

  // 設定がなければデフォルト値を使用
    const userSettings = await settings.get('userSettings');
    return { ...defaultSettings, ...userSettings };
}

async function createWindow() {
    const userSettings = await loadSettings();
    
  // ブラウザウィンドウの作成
    mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    title: '音声アシスタント',
    icon: path.join(__dirname, 'assets/icons/icon.png'),
    webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
        preload: path.join(__dirname, 'preload.js')
    }
    });

  // index.htmlのロード
    mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // 開発環境の場合は開発者ツールを開く
    if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
    }

  // ウィンドウが閉じられたときの処理
    mainWindow.on('closed', () => {
    mainWindow = null;
    });

  // グローバルホットキーの登録
    registerGlobalShortcut(userSettings.hotkey);
    
  // システムトレイの初期化
    initTray();
    
    log.info('メインウィンドウ初期化完了');
}

// グローバルホットキーの登録
function registerGlobalShortcut(hotkey) {
  // 既存のホットキーをすべて解除
    globalShortcut.unregisterAll();
    
  // 新しいホットキーを登録
    globalShortcut.register(hotkey, () => {
    log.info('ホットキーが押されました');
    
    // ウィンドウが最小化されていれば元に戻す
    if (mainWindow.isMinimized()) {
        mainWindow.restore();
    }
    
    // ウィンドウにフォーカスを当てる
    mainWindow.focus();
    
    // 録音開始のイベントを送信
    mainWindow.webContents.send('start-recording');
    });
    
    log.info(`ホットキー登録完了: ${hotkey}`);
}

// システムトレイの初期化
function initTray() {
    tray = new Tray(path.join(__dirname, 'assets/icons/tray-icon.png'));
    
    const contextMenu = Menu.buildFromTemplate([
    { label: '表示', click: () => mainWindow.show() },
    { label: '設定', click: () => mainWindow.webContents.send('open-settings') },
    { type: 'separator' },
    { label: '終了', click: () => app.quit() }
    ]);
    
    tray.setToolTip('音声アシスタント');
    tray.setContextMenu(contextMenu);
    
  // トレイアイコンがクリックされたらウィンドウを表示
    tray.on('click', () => {
    if (mainWindow.isVisible()) {
        mainWindow.hide();
    } else {
        mainWindow.show();
    }
    });
}

// マイク録音のIPCハンドラー
ipcMain.handle('get-microphone-input', async () => {
  // ここでマイクからの録音を実行
  // （実際の実装は複雑なので、詳細は省略）
    log.info('マイク録音開始');
    
  // デモ実装：ダミーの音声ファイルを返す
    return { success: true, audioPath: path.join(__dirname, 'assets/sample_audio.wav') };
});

// STT（音声認識）のIPCハンドラー
ipcMain.handle('perform-stt', async (event, audioPath) => {
    try {
    log.info(`STT実行: ${audioPath}`);
    
    // 音声ファイルの読み込み
    const audioData = fs.readFileSync(audioPath);
    const formData = new FormData();
    formData.append('file', new Blob([audioData]), 'audio.wav');
    
    // APIリクエスト
    const response = await axios.post(`${API_URL}/stt/transcribe`, formData, {
        headers: {
        'Content-Type': 'multipart/form-data'
        }
    });
    
    return response.data;
    } catch (error) {
    log.error('STT処理中にエラーが発生しました:', error);
    return { success: false, error: error.message };
    }
});

// LLM（テキスト生成）のIPCハンドラー
ipcMain.handle('perform-llm', async (event, textInput, conversationId) => {
    try {
    log.info(`LLM実行: ${textInput.substring(0, 30)}...`);
    
    const response = await axios.post(`${API_URL}/llm/chat`, {
        messages: [{ role: 'user', content: textInput }],
        conversation_id: conversationId
    });
    
    return response.data;
    } catch (error) {
    log.error('LLM処理中にエラーが発生しました:', error);
    return { success: false, error: error.message };
    }
});

// TTS（音声合成）のIPCハンドラー
ipcMain.handle('perform-tts', async (event, text, voiceId) => {
    try {
    log.info(`TTS実行: ${text.substring(0, 30)}...`);
    
    const response = await axios.post(`${API_URL}/tts/synthesize`, {
        text,
        voice_id: voiceId || 'default'
    }, {
        responseType: 'arraybuffer'
    });
    
    // 一時ファイルに音声データを保存
    const tempFilePath = path.join(app.getPath('temp'), `tts_${Date.now()}.wav`);
    fs.writeFileSync(tempFilePath, Buffer.from(response.data));
    
    return { success: true, audioPath: tempFilePath };
    } catch (error) {
    log.error('TTS処理中にエラーが発生しました:', error);
    return { success: false, error: error.message };
    }
});

// 会話履歴の取得
ipcMain.handle('get-conversation-history', async (event, conversationId) => {
    try {
    if (!supabaseClient) {
        return { success: false, error: 'Supabase接続が設定されていません' };
    }
    
    const { data, error } = await supabaseClient
        .from('conversations')
        .select('*')
        .eq('conversation_id', conversationId)
        .order('created_at', { ascending: true });
        
    if (error) throw error;
    
    return { success: true, history: data };
    } catch (error) {
    log.error('会話履歴の取得中にエラーが発生しました:', error);
    return { success: false, error: error.message };
    }
});

// ユーザー設定の保存
ipcMain.handle('save-settings', async (event, newSettings) => {
    try {
    await settings.set('userSettings', newSettings);
    
    // ホットキーの更新
    if (newSettings.hotkey) {
        registerGlobalShortcut(newSettings.hotkey);
    }
    
    return { success: true };
    } catch (error) {
    log.error('設定の保存中にエラーが発生しました:', error);
    return { success: false, error: error.message };
    }
});

// アプリケーションの初期化
app.on('ready', createWindow);

// すべてのウィンドウが閉じられたときの処理
app.on('window-all-closed', () => {
  // macOSの場合、ユーザーが明示的に終了するまでアプリケーションを終了しない
    if (process.platform !== 'darwin') {
    app.quit();
    }
});

app.on('activate', () => {
  // macOSの場合、ドックアイコンがクリックされたときにウィンドウが存在しなければ作成
    if (mainWindow === null) {
    createWindow();
    }
});

// アプリケーション終了時の処理
app.on('will-quit', () => {
  // グローバルホットキーの解除
    globalShortcut.unregisterAll();
}); 