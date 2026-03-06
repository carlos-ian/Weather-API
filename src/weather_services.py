import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL_GEO = "http://api.openweathermap.org/geo/1.0/direct"

async def get_coordinates(city_name: str):
    params = {
        "q": city_name,
        "limit": 1,
        "appid": API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL_GEO, params=params)
            response.raise_for_status()

            data = response.json()

            if not data:
                raise HTTPException(status_code=404, detail="Cidade Não Encontrada")
            
            location = data[0]

            return {
                "lat": location["lat"],
                "lon": location["lon"],
                "name": location["name"],
                "display_name": f"{location['name']} {location.get('state', '')}, {location['country']}" 
            }
        
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=500, detail="Erro na API de Localização")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro Inesperado: {str(e)}")
        
BASE_URL_WEATHER = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather_forecast(lat: float, lon: float):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "pt_br"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL_WEATHER, params=params)
            response.raise_for_status()

            data = response.json()

            return {
                "current": {
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "temp_min": data["main"]["temp_min"],
                    "temp_max": data["main"]["temp_max"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "pop": data.get("pop", 0) * 100
                },
            }
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar clima: {str(e)}")
