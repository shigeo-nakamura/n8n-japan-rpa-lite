import os
import httpx

N8N_URL = os.getenv("N8N_URL", "http://localhost:5678/api/v1")
N8N_API_KEY = os.getenv("N8N_API_KEY")


class N8NClient:
    def __init__(self, base_url: str = N8N_URL, api_key: str | None = N8N_API_KEY):
        self.base_url = base_url
        self.headers = {}
        if api_key:
            api_key = api_key.strip()
            try:
                api_key.encode("ascii")  # HTTPヘッダはASCIIのみ
            except UnicodeEncodeError:
                raise ValueError("N8N_API_KEY に全角等の非ASCII文字が含まれています。UIで発行したキーをそのまま設定してください。")
            self.headers["X-N8N-API-KEY"] = api_key
        self.timeout = httpx.Timeout(30.0)

    async def list_workflows(self):
        """既存のワークフロー一覧を取得"""
        url = f"{self.base_url}/workflows"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()

    async def create_workflow(self, workflow: dict):
        """新しいワークフローを登録"""
        url = f"{self.base_url}/workflows"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            resp = await client.post(url, json=workflow)
            if resp.status_code >= 400:
                detail = None
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise httpx.HTTPStatusError(
                    f"POST /workflows failed: {resp.status_code} - {detail}",
                    request=resp.request, response=resp
                )
            return resp.json()

    async def run_workflow(self, workflow_id: int):
        """指定ワークフローを実行"""
        url = f"{self.base_url}/workflows/{workflow_id}/run"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            resp = await client.post(url)
            resp.raise_for_status()
            return resp.json()

    async def get_execution(self, execution_id: str):
        """実行結果を取得"""
        url = f"{self.base_url}/executions/{execution_id}"
        async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()
