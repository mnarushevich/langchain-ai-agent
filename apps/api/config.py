from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Model Configuration
    model_provider: str = Field(
        default="openai", env="MODEL_PROVIDER"
    )  # "openai" or "ollama"
    model_name: str = Field(default="gpt-3.5-turbo", env="MODEL_NAME")
    model_temperature: float = Field(default=0.1, env="MODEL_TEMPERATURE")
    model_max_tokens: int = Field(default=1000, env="MODEL_MAX_TOKENS")

    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # Ollama Configuration
    ollama_base_url: str = Field(
        default="http://localhost:11434", env="OLLAMA_BASE_URL"
    )

    # ExchangeRate API Configuration
    exchangerate_api_key: str = Field(
        default="3b4e8f9ca8ead17851ef11f3", env="EXCHANGERATE_API_KEY"
    )
    exchangerate_base_url: str = Field(
        default="https://v6.exchangerate-api.com/v6", env="EXCHANGERATE_BASE_URL"
    )

    # FastAPI Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    # LangChain Configuration
    langchain_tracing_v2: bool = Field(default=False, env="LANGCHAIN_TRACING_V2")
    langchain_api_key: Optional[str] = Field(default=None, env="LANGCHAIN_API_KEY")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
