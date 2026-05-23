# ExSystem03

For MDS Experiments

## 実行手順

1. `ExSystem03` と同階層に `ExSystem03_wav` フォルダを作成し、比較対象の `.wav` ファイルを配置します。
2. 必要な依存パッケージをインストールします:
   ```bash
   c:\work\ExSystem03\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. サーバーを起動します:
   ```bash
   c:\work\ExSystem03\.venv\Scripts\python.exe app.py
   ```
4. ブラウザで `http://127.0.0.1:5000` にアクセスし、氏名を入力して実験を開始します。

## 出力

- 各参加者ごとに `results/` フォルダ内に Excel ファイルが作成されます。
- 生成される Excel ファイルには、ファイル名、評価、試行順、再生回数、回答時刻が記録されます。
