
# 📂 プロジェクト全体構成

本プロジェクト（n8n-japan-rpa-lite）は、**n8nを裏側に据えた日本向けRPAライトOSS** です。
自治体・中小企業が簡単に利用できる「業務シナリオ」を提供し、OSSコミュニティによる拡張を想定しています。

---

## 🏗 ディレクトリ構成

```
n8n-japan-rpa-lite/
├─ frontend/                # フロントエンド (Next.js / Electron)
│   ├─ public/              # 静的ファイル (icons, images)
│   ├─ src/
│   │   ├─ components/      # Reactコンポーネント
│   │   ├─ pages/           # ページ (Next.jsの場合)
│   │   ├─ hooks/           # React Hooks
│   │   ├─ services/        # API呼び出し (Backendと連携)
│   │   └─ styles/          # CSS/SCSS
│   └─ package.json

├─ backend/                 # バックエンド (FastAPI / Express/NestJS)
│   ├─ src/
│   │   ├─ api/             # REST APIエンドポイント
│   │   ├─ core/            # 共通ロジック (認証, ログ, DB)
│   │   ├─ models/          # DBモデル
│   │   ├─ services/        # n8n REST API呼び出し, Secrets管理
│   │   └─ templates/       # Meta Template 処理ロジック
│   └─ requirements.txt / package.json

├─ templates/               # 業務シナリオ (Meta Templates)
│   ├─ invoice/             # 請求書発行
│   │   ├─ meta.yaml        # Meta Template定義 (入力項目, 必須フィールド)
│   │   └─ workflow.json    # 実際のn8nワークフロー
│   ├─ ec-orders/           # EC受注処理
│   │   ├─ meta.yaml
│   │   └─ workflow.json
│   └─ ...

├─ docs/                    # ドキュメント
│   ├─ architecture.puml    # アーキテクチャ図 (PlantUML)
│   ├─ diagrams/            # 自動生成されたPNG
│   ├─ requirements.md      # 要件定義
│   ├─ roadmap.md           # ロードマップ
│   └─ structure.md         # このファイル

├─ scripts/                 # CI/CDやユーティリティスクリプト
│   └─ seed_templates.py    # テンプレート初期投入

├─ tests/                   # テスト (pytest, jest など)
│   ├─ frontend/
│   ├─ backend/
│   └─ e2e/                 # end-to-endテスト (n8n連携含む)

├─ .github/
│   └─ workflows/           # GitHub Actions (CI, PlantUML変換など)

├─ .gitignore
├─ docker-compose.yml       # n8n + backend + frontend の統合環境
├─ README.md
└─ LICENSE
```

---

## 📌 各ディレクトリの役割

### frontend/
- 中小企業や自治体の担当者が操作する **GUI**
- ウィザード型の業務シナリオ作成、テスト実行ボタン、ログ確認機能を提供

### backend/
- **Meta Template** を読み込み、ユーザー入力を反映させて n8n に渡す
- 認証情報（Secrets）を安全に管理
- 実行ログを取得してフロントに返却

### templates/
- 業務シナリオのコア部分
- `meta.yaml`: ユーザー入力フォームの定義（質問項目、型、必須）
- `workflow.json`: 実際に n8n で動くワークフロー

### docs/
- プロジェクト設計・アーキテクチャ資料
- PlantUML図を含む。GitHub Actionsで PNG 自動生成

### scripts/
- 開発やデプロイ補助用のユーティリティ

### tests/
- ユニットテスト、統合テスト、E2Eテストを格納

### .github/workflows/
- CI/CD（例: PlantUML変換、Lint、テスト）

---

## 🚀 最初に着手すべき部分
1. **backend/** に最小のAPIを作成（n8n連携）
2. **templates/** に請求書発行など簡単なシナリオを追加
3. **docs/** にアーキテクチャ図・要件定義をまとめる
4. **frontend/** は最初はシンプルなフォームUIから開始
