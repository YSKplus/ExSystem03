#!/bin/bash

echo "========================================"
echo "ExSystem03 - セットアップスクリプト"
echo "========================================"
echo ""

# 仮想環境が存在するか確認
if [ -d ".venv" ]; then
    echo "[info] 仮想環境は既に存在します"
else
    echo "[info] 仮想環境を作成中..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[error] 仮想環境の作成に失敗しました"
        exit 1
    fi
fi

echo ""
echo "[info] 仮想環境を有効化中..."
source .venv/bin/activate

echo ""
echo "[info] 依存パッケージをインストール中..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[error] パッケージのインストールに失敗しました"
    exit 1
fi

echo ""
echo "========================================"
echo "セットアップが完了しました！"
echo "========================================"
echo ""
echo "次のステップ："
echo "1. ExSystem03 と同階層に 5_potechi_renamed フォルダを作成"
echo "2. .wav ファイルを 5_potechi_renamed フォルダに配置"
echo "3. python app.py でサーバーを起動"
echo "4. http://127.0.0.1:5000 にブラウザでアクセス"
echo ""
