import axios from "axios";

export async function getWeather(city: string) {
  const res = await axios.get("http://localhost:8000/api/weather", {
    params: { city }
  });
  return res.data as { weather: any; summary: string };
}