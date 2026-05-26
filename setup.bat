@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo ExSystem03 - セットアップスクリプト
echo ========================================
echo.

REM 仮想環境が存在するか確認
if exist ".venv" (
    echo [info] 仮想環境は既に存在します
) else (
    echo [info] 仮想環境を作成中...
    python -m venv .venv
    if !errorlevel! neq 0 (
        echo [error] 仮想環境の作成に失敗しました
        exit /b 1
    )
)

echo.
echo [info] 仮想環境を有効化中...
call .venv\Scripts\activate.bat

echo.
echo [info] 依存パッケージをインストール中...
pip install -r requirements.txt
if !errorlevel! neq 0 (
    echo [error] パッケージのインストールに失敗しました
    exit /b 1
)

echo.
echo ========================================
echo セットアップが完了しました！
echo ========================================
echo.
echo 次のステップ：
echo 1. ExSystem03 と同階層に 5_potechi_renamed フォルダを作成
echo 2. .wav ファイルを 5_potechi_renamed フォルダに配置
echo 3. python app.py でサーバーを起動
echo 4. http://127.0.0.1:5000 にブラウザでアクセス
echo.
pause
