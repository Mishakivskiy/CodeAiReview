import json
from typing import Optional
from app.core.config import REDIS_URL
import aioredis

redis = aioredis.from_url(REDIS_URL)


async def cache_repo_contents(repo_url: str, contents: dict, expire: int = 3600) -> None:
    serialized_contents = json.dumps(contents)
    await redis.set(repo_url, serialized_contents, ex=expire)


async def get_cached_repo_contents(repo_url: str) -> Optional[dict]:
    cached_contents = await redis.get(repo_url)
    if cached_contents is None:
        return None
    return json.loads(cached_contents)
