from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		case_sensitive=False,
		extra="ignore",
	)

	app_name: str = "Production Chatbot API"
	environment: str = "development"
	log_level: str = "INFO"
	api_key: str | None = Field(default=None, validation_alias="CHATBOT_API_KEY")
	auth_required: bool = True
	cors_origins: list[str] = ["http://localhost:3000"]
	groq_api_key: str | None = None
	groq_model: str = "openai/gpt-oss-20b"
	groq_base_url: str = "https://api.groq.com/openai/v1"
	max_input_characters: int = 12_000
	max_history_messages: int = 20
	conversation_ttl_seconds: int = 3_600
	max_conversations: int = 10_000


@lru_cache
def get_settings() -> Settings:
	return Settings()
