from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .utils import decode_access_token


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(
            HTTPBearer()
        ),
    ):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing access token",
            )

        token = credentials.credentials
        token_data = decode_access_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired access token",
            )

        # Reject refresh tokens when calling protected endpoints
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token cannot be used as access token",
            )

        return token_data

    async def token_valid(self, token: str) -> bool:
        try:
            payload = decode_access_token(token)
            return payload is not None
        except Exception:
            return False