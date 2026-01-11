import json
from pathlib import Path

class DataCleaningAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.prompt = Path(
            "agents/prompts/suggest_cleaning.md"
        ).read_text()

    def suggest(self, profiling: dict) -> list[dict]:
        response = self.llm.chat(
            system=self.prompt,
            user=json.dumps(profiling),
        )

        return json.loads(response)
