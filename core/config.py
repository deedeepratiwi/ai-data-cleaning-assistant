from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MCP_URL: str = "http://mcp:9000"

    class Config:
        env_file = ".env"


settings = Settings()
