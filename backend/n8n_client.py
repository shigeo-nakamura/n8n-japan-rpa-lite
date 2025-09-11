import httpx
import os

N8N_URL = os.getenv("N8N_URL", "http://localhost:5678/api/v1")

class N8NClient:
    def __init__(self, base_url: str = N8N_URL):
        self.base_url = base_url

    async def run_workflow(self, workflow_id: int):
        url = f"{self.base_url}/workflows/{workflow_id}/run"
        async with httpx.AsyncClient() as client:
            resp = await client.post(url)
            resp.raise_for_status()
            return resp.json()

    async def get_execution(self, execution_id: str):
        url = f"{self.base_url}/executions/{execution_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()

