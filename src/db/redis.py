import redis.asyncio as aioredis
from src.config import Config


JTI_EXPIRATION_TIME = 3600  # 1 hour in seconds
token_blacklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0
)

async def add_jti_to_blacklist(jti: str) -> None:
    """
    Add a JTI to the Redis blacklist with an expiration time.
    """
    await token_blacklist.setex(
        name=jti, 
        time=JTI_EXPIRATION_TIME, 
        value=""
    )
async def token_in_blacklist(jti: str) -> bool:
    """
    Check if a JTI is in the Redis blacklist.
    """
    return await token_blacklist.exists(jti) > 0