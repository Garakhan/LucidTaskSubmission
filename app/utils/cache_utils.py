from cachetools import TTLCache
from typing import Dict

# Cache for user posts – maxsize=1000 users, TTL=5 minutes
post_cache: Dict[int, TTLCache] = {}

def get_user_cache(user_id: int):
    """Get or create a cache for a specific user."""
    if user_id not in post_cache:
        post_cache[user_id] = TTLCache(maxsize=1, ttl=300)  # TTL = 5 mins
    return post_cache[user_id]

def cache_user_posts(user_id: int, posts: list):
    """Cache the posts of a user."""
    cache = get_user_cache(user_id)
    cache['posts'] = posts

def get_cached_posts(user_id: int):
    """Return cached posts for user if available."""
    cache = get_user_cache(user_id)
    return cache.get('posts')
