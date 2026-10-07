from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .utils import decode_access_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )

        token = credentials.credentials
        token_data = decode_access_token(token)

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token",
            )

        # Let verify_token check token type and raise proper HTTPExceptions
        self.verify_token(token_data)

        return token_data

    def verify_token(self, token_data: dict) -> None:
        raise NotImplementedError(
            "Subclasses must implement verify_token method."
        )


class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token cannot be used as access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data: dict) -> None:
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access token cannot be used as refresh token",
            )