# backend/main.py
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from fastapi import FastAPI, HTTPException, Body
from .services.n8n_client import N8NClient
from .services.ai_draft import generate_reply_draft
from .services.template_loader import ensure_templates

app = FastAPI(title="RPA Lite Backend PoC", version="0.1.0")
n8n = N8NClient()

@app.on_event("startup")
async def startup_event():
    """アプリ起動時にテンプレートを確認・登録"""
    await ensure_templates(n8n)

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: int):
    try:
        result = await n8n.run_workflow(workflow_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/executions/{execution_id}")
async def get_execution(execution_id: str):
    try:
        result = await n8n.get_execution(execution_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gmail/draft")
async def create_gmail_draft(
    subject: str = Body(..., embed=True),
    body: str = Body(..., embed=True),
    workflow_id: int = Body(..., embed=True)
):
    """
    Gmailの下書きを作成する。
    - AIで返信ドラフトを生成
    - n8n ワークフローを呼び出して Gmail API で下書き保存
    """

    # AIで返信文を生成
    draft_text = generate_reply_draft(subject, body)

    # n8n ワークフローに渡すデータ
    payload = {
        "subject": f"Re: {subject}",
        "body": draft_text,
    }

    try:
        result = await n8n.run_workflow(workflow_id)
        return {"draft": draft_text, "n8n_result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

