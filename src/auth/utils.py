from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher

# Initialize pwdlib with BcryptHasher
password_hash = PasswordHash((BcryptHasher(),))

def generate_password_hash(password: str) -> str:
    return password_hash.hash(password[:72])

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password[:72], hashed_password)