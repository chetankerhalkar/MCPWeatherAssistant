"""
Pure MCP tool + utility helpers.
"""
import httpx
from pydantic import BaseModel, Field
from .settings import settings

class WeatherArgs(BaseModel):
    city: str = Field(..., description="City name in English")

async def _fetch(city: str) -> dict:
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&units=metric&appid={settings.openweather_api_key}"
    )
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()

# MCP tool (no LLM needed here)
async def get_current_weather(args: WeatherArgs) -> dict:
    """Return the raw OpenWeather JSON for the given city."""
    return await _fetch(args.city)

# Helper for the REST endpoint (separate because it calls the LLM)
async def get_weather_and_summary(city: str) -> dict:
    data = await _fetch(city)

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    messages = [
        {
            "role": "system",
            "content": "You are a friendly weather assistant. "
                       "Summarise the weather in one short paragraph."
        },
        {"role": "user", "content": f"{data}"},
    ]
    chat = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        max_tokens=120,
    )
    summary = chat.choices[0].message.content.strip()
    return {"weather": data, "summary": summary}