import asyncio
from functools import wraps

def sync_to_async(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_in_executor(None, func, *args, **kwargs)
    return wrapper