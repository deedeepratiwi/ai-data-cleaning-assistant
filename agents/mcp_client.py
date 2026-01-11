import httpx
from core.config import settings

class MCPClient:
    def __init__(self):
        self.base_url = settings.MCP_URL

    def call(self, tool: str, payload: dict) -> dict:
        response = httpx.post(
            f"{self.base_url}/mcp",
            json={
                "tool": tool,
                "payload": payload,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["result"]


def get_llm_client():
    """
    Replace this with:
    - OpenAI
    - Anthropic
    - MCP server
    - Local model
    """
    raise NotImplementedError("LLM client not configured")
