from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from .config import Settings, get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(
	provided_key: str | None = Security(api_key_header),
	settings: Settings = Depends(get_settings),
) -> None:
	if not settings.auth_required:
		return
	if not settings.api_key or provided_key != settings.api_key:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid or missing API key",
		)
