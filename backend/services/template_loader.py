import json
import os
from pathlib import Path
from typing import List, Dict, Any
from copy import deepcopy
from .n8n_client import N8NClient

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = REPO_ROOT / "templates"

def _normalize_template(wf: Dict[str, Any]) -> Dict[str, Any]:
    """
    n8n へ POST する前に最低限の形に整える。
    - 必須: name(str), nodes(list), connections(dict), settings(dict)
    - 型が違う/欠けている場合はデフォルト補完
    """
    wf = deepcopy(wf)

    # name（必須）
    name = wf.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("workflow JSON に有効な 'name' がありません。")

    # nodes（配列）
    if not isinstance(wf.get("nodes"), list):
        wf["nodes"] = []

    # connections（オブジェクト）
    if not isinstance(wf.get("connections"), dict):
        wf["connections"] = {}

    # settings（オブジェクト）← ★今回の必須
    if not isinstance(wf.get("settings"), dict):
        wf["settings"] = {}

    return wf

def _normalize_workflows(payload: Any) -> List[Dict[str, Any]]:
    """
    n8n の /workflows の戻り値が、
    - そのまま list[dict]
    - {"data": list[dict]}
    - {"workflows": list[dict]}
    など複数パターンあり得る前提で正規化して list[dict] を返す。
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        # よくあるキー名を順に探す
        for key in ("data", "workflows", "items"):
            if key in payload and isinstance(payload[key], list):
                return payload[key]
        # dict のままワークフロー1件相当ならラップ
        if "name" in payload:
            return [payload]
    # 文字列等は不正（401で JSON に "Unauthorized" などのケース含む）
    raise TypeError(f"Unexpected /workflows response type: {type(payload).__name__} -> {payload!r}")


async def ensure_templates(n8n: N8NClient):
    """templates/ フォルダを確認し、未登録なら n8n に登録する"""
    # 既存ワークフロー名を取得（返り値の形を正規化する）
    raw = await n8n.list_workflows()
    workflows = _normalize_workflows(raw)
    existing_names = {wf.get("name") for wf in workflows if isinstance(wf, dict)}

    # templates ディレクトリ内の .json を走査
    for filename in os.listdir(TEMPLATES_DIR):
        if not filename.endswith(".json"):
            continue
        path = os.path.join(TEMPLATES_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                workflow = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"❌ JSON parse error at {path}: {e}")
            continue

        name = workflow.get("name")
        if not name:
            print(f"⚠️  {filename}: 'name' フィールドがありません。スキップします。")
            continue

        normalized = _normalize_template(workflow)

        if name in existing_names:
            print(f"✅ Already exists: {name}")
            continue

        print(f"➡️ Registering workflow: {name}")
        try:
            await n8n.create_workflow(normalized)
        except Exception as e:
            print(f"❌ Failed to register '{name}' from {path.name}: {e}")
            continue
