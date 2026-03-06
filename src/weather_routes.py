from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, security, weather_services
from datetime import datetime

weather_router = APIRouter(prefix="/weather", tags=["weather"])

@weather_router.get("/get_city")
async def citySearch(city_name: str, db: Session = Depends(database.get_db), user: models.User = Depends(security.get_current_user)):
    coords = await weather_services.get_coordinates(city_name)
    weather_data = await weather_services.get_weather_forecast(lat=coords["lat"], lon=coords["lon"])

    if "current" not in weather_data:
        raise HTTPException(status_code=404, detail="Não foi possível obter os dados climáticos.")
    
    return {
        "usuario_logado": user.username,
        "localizacao": {
            "cidade": coords["name"],
            "lat": coords["lat"],
            "lon": coords["lon"] 
        },
        "clima": weather_data,
    }

@weather_router.post("/post_history")
async def sendCity(city_name: str, db: Session = Depends(database.get_db), user: models.User = Depends(security.get_current_user)):
    coords = await weather_services.get_coordinates(city_name)
    weather_data = await weather_services.get_weather_forecast(lat=coords["lat"], lon=coords["lon"])

    if "current" not in weather_data:
        raise HTTPException(status_code=400, detail="Dados da API incompletos ou cidade inválida.")
    
    new_history = models.SearchHistory (
        user_id = user.id,
        city_name = coords["name"],
        temp_current = weather_data["current"]["temp"],
        temp_min = weather_data["current"]["temp_min"],
        temp_max = weather_data["current"]["temp_max"],
        feels_like = weather_data["current"]["feels_like"],
        rain_prob = weather_data["current"]["pop"],
        condition_desc = weather_data["current"]["description"],
        timestamp = datetime.now() 
    )

    db.add(new_history)
    db.commit()
    db.refresh(new_history)

    return {"status": "sucesso", "id": new_history.id}