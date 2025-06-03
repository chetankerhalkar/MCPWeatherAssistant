import { useState } from "react";
import { getWeather } from "./api";

export default function WeatherCard() {
  const [city, setCity] = useState("");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState<string | null>(null);

  const handleFetch = async () => {
    if (!city.trim()) return;
    setLoading(true);
    try {
      const { summary } = await getWeather(city.trim());
      setSummary(summary);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-wrapper">
      <h1>Weather with LLM + MCP</h1>

      <input
        type="text"
        value={city}
        placeholder="Enter a city (e.g. Chicago)"
        onChange={(e) => setCity(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleFetch()}
      />

      <button onClick={handleFetch} disabled={loading}>
        {loading ? "Loading…" : "Get Weather"}
      </button>

      {summary && <p className="summary">{summary}</p>}
    </div>
  );
}
