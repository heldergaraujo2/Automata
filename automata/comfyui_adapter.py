"""Safe, opt-in ComfyUI workflow preparation and local queue submission.

No server calls are made without explicit allow_execution=True.
"""
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

def validate_endpoint(endpoint: str) -> str:
    parsed = urlparse(endpoint)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError("Somente ComfyUI HTTP local é permitido")
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
        raise ValueError("Endpoint ComfyUI inválido")
    if parsed.port is None:
        raise ValueError("Porta explícita obrigatória")
    return endpoint.rstrip("/")

def load_api_workflow(path: Path) -> dict:
    workflow = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("Workflow API JSON deve ser objeto não vazio")
    for node_id, node in workflow.items():
        if not isinstance(node, dict) or not isinstance(node.get("class_type"), str) or not isinstance(node.get("inputs"), dict):
            raise ValueError(f"Nó inválido: {node_id}")
    return workflow

def prepare_workflow(template: dict, *, prompt_node_id: str, prompt: str) -> dict:
    if not prompt.strip():
        raise ValueError("Prompt vazio")
    result = json.loads(json.dumps(template))
    node = result.get(prompt_node_id)
    if not isinstance(node, dict) or node.get("class_type") != "CLIPTextEncode":
        raise ValueError("Nó de texto CLIPTextEncode não encontrado")
    if "text" not in node.get("inputs", {}):
        raise ValueError("Entrada text ausente")
    node["inputs"]["text"] = prompt
    return result

def submit_workflow(workflow: dict, *, endpoint: str = "http://127.0.0.1:8188",
                    client_id: str = "automata", allow_execution: bool = False) -> dict:
    if not allow_execution:
        raise PermissionError("Conexão com ComfyUI bloqueada até testes locais finais")
    url = validate_endpoint(endpoint)
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("Workflow vazio")
    body = json.dumps({"prompt": workflow, "client_id": client_id}).encode("utf-8")
    request = Request(url + "/prompt", data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=30) as response:
        data = json.load(response)
    if not isinstance(data, dict) or not isinstance(data.get("prompt_id"), str):
        raise RuntimeError("Resposta ComfyUI sem prompt_id")
    return {"prompt_id": data["prompt_id"], "status": "queued_locally_not_verified"}
