# 🌤️ MCP-Weather-Demo

A **full-stack reference project** that shows how to expose a tool over the **Model-Context-Protocol (FastMCP ≥ 2.3)**, transform the raw data with an **LLM**, and serve it to a **React + Vite** front-end.

<p align="center">
  <img width="700" alt="screenshot" src="docs/screenshot.png">
</p>

---

| Stack | What it does |
|-------|--------------|
| **FastAPI + FastMCP** | Hosts the `get_current_weather` tool at `/mcp` (SSE) and a classic REST endpoint at `/api/weather`. |
| **OpenWeather API** | Supplies raw weather JSON. |
| **OpenAI GPT-4o mini** | Generates a short, friendly forecast from that JSON. |
| **React 18 + Vite** | Calls `/api/weather`, shows a glass-morphism card on a dark gradient background. |
| **Docker** | One-command local deployment (`docker compose up`). |

---

## ✨ Demo

```bash
git clone https://github.com/chetankerhalkar/MCPWeatherAssistant
cd mcp-weather-demo

# Backend -------------------------------------------------------
cd backend
python -m venv .venv && source .venv/bin/activate    # Windows: .\.venv\Scripts\activate
cp .env.example .env    # paste your keys
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000            # http://localhost:8000/api/health

# Front-end -----------------------------------------------------
cd ../frontend
npm install
npm run dev                                           # http://localhost:5173
