import httpx
from fastapi import requests

from app.config import settings


async def translate(content: str, target_language: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.translation_url + "/translate", data={
                "q": content,
                "source": "auto",
                "target": target_language,
                "format": "html"
            }, timeout=None)

            return response.json()
    except ValueError:
        return None