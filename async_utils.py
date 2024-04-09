import asyncio

import aiohttp


async def async_call_with_retry(async_func, args, timeout, retry_count):
    for attempt in range(retry_count + 1):
        try:
            return await asyncio.wait_for(async_func(*args), timeout)
        except (asyncio.TimeoutError, aiohttp.ClientError) as e:
            if attempt == retry_count:
                raise
            await asyncio.sleep(2 ** attempt)
