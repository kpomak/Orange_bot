from aiohttp import ClientSession

from bot.config import BARD_URL


async def bard_request(query):
    async with ClientSession() as session:
        async with session.get(BARD_URL, params=query) as resp:
            data = await resp.json()
            return data.get("content")
