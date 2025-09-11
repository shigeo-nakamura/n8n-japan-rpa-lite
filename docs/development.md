# 開発環境セットアップ手順

このプロジェクトは **FastAPI + n8n** を組み合わせて動作します。
以下の手順でローカル環境を準備してください。

---

## 1. 事前準備

- Docker / Docker Compose がインストール済みであること
- Python 3.12 以上がインストールされていること
- `git clone` 済みであること

---

## 2. n8n の起動（Docker Compose）

### 2.1 `.env` ファイルを作成

プロジェクトルートにある `.env.example` をコピーして `.env` を作成してください。

```bash
cp .env.example .env
```

その後 .env を編集して環境変数を設定します：

```bash
# n8n の暗号化キー（必ず固定の長いランダム文字列を指定）
N8N_ENCRYPTION_KEY=your-long-random-string

# n8n の API URL
N8N_URL=http://localhost:5678/api/v1

# n8n の API Key（起動後に UI から発行して追記）
N8N_API_KEY=
```

### 2.2 `docker-compose.yml` を利用

プロジェクトルートにはすでに docker-compose.yml が用意されています。

### 2.3 起動

```bash
docker compose up -d
```
もしくは
```bash
docker-compose up -d
```

- UI: http://localhost:5678
- API: http://localhost:5678/api/v1

---

## 2.4 初回起動時のアカウントセットアップ

1. ブラウザで http://localhost:5678 を開いてください
   初回アクセス時に **オーナーアカウント作成画面** が表示されます
   → Email, 名前, パスワードを入力して管理者アカウントを作成してください

2. 設定メニューから **API Key を発行**し、`.env` の `N8N_API_KEY` に追記してください

---

## 3. Python バックエンドのセットアップ

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 4. FastAPI の起動

FastAPI 側は `.env` の設定を利用して n8n に接続します。

```bash
source backend/.venv/bin/activate
uvicorn backend.main:app --reload
```

起動時に `templates/` フォルダを確認し、未登録のワークフローを自動で n8n に登録します。
ログに以下のようなメッセージが表示されれば成功です：

```
➡️ Registering workflow: Gmail Draft Generator
✅ Already exists: Invoice Issuer
```

---

## 5. 動作確認

- FastAPI: http://127.0.0.1:8000
- n8n UI: http://localhost:5678
  - ワークフロー一覧に「Gmail Draft Generator」などが登録されていることを確認してください

---

## 6. よくある問題

- **依存パッケージが入らない場合**
  → 仮想環境を作り直してください
  ```bash
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

- **n8n API に接続できない場合**
  → `.env` の `N8N_URL` と `N8N_API_KEY` を確認してください
  ```bash
  export N8N_URL="http://localhost:5678/api/v1"
  export N8N_API_KEY="your_generated_api_key"
  ```

---

これで開発環境の準備は完了です 🎉
