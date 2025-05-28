import aiohttp
import redis.asyncio as redis
import json


r = redis.Redis(host="redis", port=6379, decode_responses=True)

async def get_weather(city: str):
    cached = await r.get(city.lower())
    if cached:
        return json.loads(cached)

    if city.lower() == "london":
        url = f"https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
    elif city.lower() == "new york":
        url = f"https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&current_weather=true"
    else:
        return {"error": "Only London and New York supported"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            await r.set(city.lower(), json.dumps(data), ex=60)
            return data

