import asyncio
import time
from collections import OrderedDict

from .schemas import ChatMessage


class ConversationStore:
	def __init__(self, ttl_seconds: int, max_conversations: int) -> None:
		self._ttl_seconds = ttl_seconds
		self._max_conversations = max_conversations
		self._conversations: OrderedDict[str, tuple[float, list[ChatMessage]]] = OrderedDict()
		self._lock = asyncio.Lock()

	async def get(self, conversation_id: str) -> list[ChatMessage]:
		async with self._lock:
			item = self._conversations.get(conversation_id)
			if item is None:
				return []
			expires_at, messages = item
			if expires_at <= time.monotonic():
				del self._conversations[conversation_id]
				return []
			self._conversations.move_to_end(conversation_id)
			return list(messages)

	async def append(self, conversation_id: str, messages: list[ChatMessage]) -> None:
		async with self._lock:
			existing = self._conversations.get(conversation_id, (0, []))[1]
			self._conversations[conversation_id] = (
				time.monotonic() + self._ttl_seconds,
				[*existing, *messages],
			)
			self._conversations.move_to_end(conversation_id)
			while len(self._conversations) > self._max_conversations:
				self._conversations.popitem(last=False)
