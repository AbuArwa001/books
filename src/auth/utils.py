import logging
import uuid
from datetime import datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

from src.config import Config

ACCESS_TOKEN_EXPIRE_MINUTES = 3600
# Initialize pwdlib with BcryptHasher
password_hash = PasswordHash((BcryptHasher(),))


def generate_password_hash(password: str) -> str:
    return password_hash.hash(password[:72])


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password[:72], hashed_password)


def create_access_token(
    data: dict, expires_delta: timedelta = None, refresh: bool = False
) -> str:
    """
    Create a JWT access token with the given data and expiration time.
    """
    payload = {}
    payload["user"] = data
    payload["exp"] = (
        datetime.now() + expires_delta
        if expires_delta
        else datetime.now()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    # payload.update(data)
    # payload["exp"] = datetime.utcnow() + expires_delta

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> dict:
    """
    Decode a JWT access token and return the payload.
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        raise Exception("Invalid token")
