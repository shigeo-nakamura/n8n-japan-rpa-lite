# 開発環境セットアップ手順

このプロジェクトは **FastAPI + n8n** を組み合わせて動作します。
以下の手順でローカル環境を準備してください。

---

## 1. 事前準備

- Docker / Docker Compose をインストール済みであること
- Python 3.12 以上がインストールされていること
- `git clone` 済みであること

---

## 2. n8n の起動（Docker）

```bash
docker run -it --rm   -p 5678:5678   -e N8N_BASIC_AUTH_ACTIVE=true   -e N8N_BASIC_AUTH_USER=admin   -e N8N_BASIC_AUTH_PASSWORD=secret   n8nio/n8n
```

- UI: http://localhost:5678
- API: http://localhost:5678/api/v1
- 認証ユーザー: `admin` / `secret`

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

```bash
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
  → `N8N_URL` を環境変数で上書きしてください
  ```bash
  export N8N_URL="http://localhost:5678/api/v1"
  ```

---

これで開発環境の準備は完了です 🎉
