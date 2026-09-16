from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
	model_config = ConfigDict(extra="forbid")

	role: Literal["user", "assistant", "system"]
	content: str = Field(min_length=1, max_length=12_000)


class ChatRequest(BaseModel):
	model_config = ConfigDict(extra="forbid")

	message: str = Field(min_length=1, max_length=12_000)
	conversation_id: str | None = Field(default=None, min_length=1, max_length=128)
	history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatResponse(BaseModel):
	conversation_id: str
	message: ChatMessage


class HealthResponse(BaseModel):
	status: Literal["ok"]
	service: str
	environment: str
