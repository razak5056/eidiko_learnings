import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .agent import AgentError, ChatAgent
from .config import Settings, get_settings
from .logging_config import configure_logging
from .memory import ConversationStore
from .schemas import ChatMessage, ChatRequest, ChatResponse, HealthResponse
from .tools import require_api_key

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
	app_settings = settings or get_settings()

	@asynccontextmanager
	async def lifespan(app: FastAPI):
		configure_logging(app_settings.log_level)
		app.state.store = ConversationStore(
			ttl_seconds=app_settings.conversation_ttl_seconds,
			max_conversations=app_settings.max_conversations,
		)
		app.state.agent = ChatAgent(app_settings)
		yield

	app = FastAPI(title=app_settings.app_name, version="1.0.0", lifespan=lifespan)
	app.add_middleware(
		CORSMiddleware,
		allow_origins=app_settings.cors_origins,
		allow_credentials=False,
		allow_methods=["GET", "POST"],
		allow_headers=["Content-Type", "X-API-Key"],
	)

	@app.middleware("http")
	async def add_request_id(request: Request, call_next):
		request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
		response = await call_next(request)
		response.headers["X-Request-ID"] = request_id
		return response

	@app.exception_handler(AgentError)
	async def handle_agent_error(request: Request, exc: AgentError):
		logger.exception("Chat agent failure", extra={"path": request.url.path})
		return JSONResponse(
			status_code=status.HTTP_502_BAD_GATEWAY,
			content={"detail": str(exc)},
		)

	@app.get("/health", response_model=HealthResponse, tags=["health"])
	async def health() -> HealthResponse:
		return HealthResponse(
			status="ok",
			service=app_settings.app_name,
			environment=app_settings.environment,
		)

	@app.post(
		"/v1/chat",
		response_model=ChatResponse,
		dependencies=[Depends(require_api_key)],
		tags=["chat"],
	)
	async def chat(request: ChatRequest, app_request: Request) -> ChatResponse:
		conversation_id = request.conversation_id or str(uuid.uuid4())
		stored_messages = await app_request.app.state.store.get(conversation_id)
		history = request.history or stored_messages
		messages = [*history, ChatMessage(role="user", content=request.message)]
		if len(messages) > app_settings.max_history_messages:
			messages = messages[-app_settings.max_history_messages :]
		reply = await app_request.app.state.agent.reply(messages)
		await app_request.app.state.store.append(
			conversation_id,
			[ChatMessage(role="user", content=request.message), reply],
		)
		return ChatResponse(conversation_id=conversation_id, message=reply)

	return app


app = create_app()
