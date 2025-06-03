import logging.config, os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from .settings import settings
from .weather_tool import get_current_weather, get_weather_and_summary

# ─── Logging ────────────────────────────────────────────────────────────────────
LOGGING_CONFIG = os.path.join(os.path.dirname(__file__), "logging.conf")
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# ─── MCP server (no embedded llm) ───────────────────────────────────────────────
mcp = FastMCP(
    "Weather-MCP",
    tools=[get_current_weather],
)

# ─── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(title="Weather Demo – MCP + REST")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # tighten in prod if needed
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Mount MCP transport (FastMCP ≥ 2.3)
app.mount("/mcp", mcp.http_app())

@app.get("/api/health", tags=["meta"])
async def health():
    return {"status": "ok"}

@app.get("/api/weather", tags=["weather"])
async def weather(city: str):
    try:
        return await get_weather_and_summary(city)
    except Exception as exc:
        logger.exception("weather summary failed")
        raise HTTPException(status_code=400, detail=str(exc))