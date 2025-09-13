import os, json
from services.n8n_client import N8NClient

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")

async def ensure_templates(n8n: N8NClient):
    """templates/ フォルダを確認し、未登録なら n8n に登録する"""

    # 既存ワークフロー名を取得
    existing = await n8n.list_workflows()
    existing_names = {wf["name"] for wf in existing}

    # templates ディレクトリ内のファイルを走査
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".json"):
            path = os.path.join(TEMPLATES_DIR, filename)
            with open(path) as f:
                workflow = json.load(f)

            # 名前がまだ存在しない場合のみ登録
            if workflow.get("name") not in existing_names:
                print(f"➡️ Registering workflow: {workflow.get('name')}")
                await n8n.create_workflow(workflow)
            else:
                print(f"✅ Already exists: {workflow.get('name')}")

