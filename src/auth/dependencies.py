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
        if credentials:
            token = credentials.credentials
            token_data = decode_access_token(token)
            if not await self.token_valid(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired access token",
                )
            if token_data is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired access token",
                )
            if token_data.get("refresh", False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Refresh token cannot be used as access token",
                )
            print("Token data:", token_data)
            if not token_data.get("refresh", False):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid or expired access token",
                )

            return token_data
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing access token",
            )

    async def token_valid(self, token: str) -> bool:
        try:
            payload = decode_access_token(token)
            if payload is None:
                return False
            return True
        except Exception:
            return False
