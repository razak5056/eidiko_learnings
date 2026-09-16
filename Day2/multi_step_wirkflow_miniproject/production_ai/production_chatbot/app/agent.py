from collections.abc import Sequence

from openai import AsyncOpenAI

from .config import Settings
from .schemas import ChatMessage


class AgentError(RuntimeError):
	pass


class ChatAgent:
	def __init__(self, settings: Settings) -> None:
		self._settings = settings
		self._client: AsyncOpenAI | None = None

	def _get_client(self) -> AsyncOpenAI:
		if not self._settings.groq_api_key:
			raise AgentError("GROQ_API_KEY is not configured")
		if self._client is None:
			client_kwargs: dict[str, str] = {
				"api_key": self._settings.groq_api_key,
				"base_url": self._settings.groq_base_url,
			}
			self._client = AsyncOpenAI(**client_kwargs)
		return self._client

	async def reply(self, messages: Sequence[ChatMessage]) -> ChatMessage:
		client = self._get_client()
		try:
			response = await client.chat.completions.create(
				model=self._settings.groq_model,
				messages=[message.model_dump() for message in messages],
				temperature=0.2,
			)
		except Exception as exc:
			raise AgentError("The model provider request failed") from exc
		content = response.choices[0].message.content
		if not content:
			raise AgentError("The model provider returned an empty response")
		return ChatMessage(role="assistant", content=content)
