# ExSystem03

For MDS Experiments

## 環境セットアップ

### 前提条件

- Python 3.7以上

### インストール手順

1. リポジトリをクローンします:

   ```bash
   git clone <repository-url>
   cd ExSystem03
   ```

2. セットアップスクリプトを実行します:
   - **Windows**: `setup.bat` をダブルクリック
   - **Mac/Linux**: `bash setup.sh` を実行

   これで仮想環境が作成され、必要なパッケージが自動的にインストールされます。

## 実行手順

1. `ExSystem03` と同階層に `5_potechi_renamed` フォルダを作成し、比較対象の `.wav` ファイルを配置します:

   ```
   parent_directory/
   ├── ExSystem03/          (このプロジェクト)
   └── 5_potechi_renamed/   (WAVファイルが必要)
   ```

2. 仮想環境を有効化します:
   - **Windows (cmd)**: `.venv\Scripts\activate.bat`
   - **Windows (PowerShell)**: `.venv\Scripts\Activate.ps1`
   - **Mac/Linux**: `source .venv/bin/activate`

3. サーバーを起動します:

   ```bash
   python app.py
   ```

4. ブラウザで `http://127.0.0.1:5000` にアクセスし、氏名を入力して実験を開始します。

## 出力

- 各参加者ごとに `results/` フォルダ内に Excel ファイルが作成されます。
- 生成される Excel ファイルには、ファイル名、評価、試行順、再生回数、回答時刻が記録されます。
