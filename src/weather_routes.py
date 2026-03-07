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

@weather_router.put("/update_history/{history.id}")
async def update_history(history_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(security.get_current_user)):
    db_history = db.query(models.SearchHistory).filter(models.SearchHistory.id == history_id, models.SearchHistory.user_id == user.id).first()

    if not db_history:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    
    coords = await weather_services.get_coordinates(db_history.city_name)
    weather_data = await weather_services.get_weather_forecast(lat=coords["lat"], lon=coords["lon"])

    if "current" not in weather_data:
        raise HTTPException(status_code=400, detail="Erro ao atualizar dados via API.")
    
    db_history.temp_current = weather_data["current"]["temp"]
    db_history.temp_min = weather_data["current"]["temp_min"]
    db_history.temp_max = weather_data["current"]["temp_max"]
    db_history.feels_like = weather_data["current"]["feels_like"]
    db_history.rain_prob = weather_data["current"]["pop"]
    db_history.condition_desc = weather_data["current"]["description"]
    db_history.timestamp = datetime.now()

    db.commit()
    db.refresh(db_history)

    return {"message": "Dados atualizados com sucesso via API", "item": db_history}

@weather_router.delete("/delete_history/{history_id}")
async def delete_history(history_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(security.get_current_user)):
    db_history = db.query(models.SearchHistory).filter(models.SearchHistory.id == history_id, models.SearchHistory.user_id == user.id).first()

    if not db_history:
        raise HTTPException(status_code=404, detail="Registro não encontrado.")

    db.delete(db_history)
    db.commit()

    return {"status": "removido", "id": history_id}

@weather_router.get("/recent_history")
async def get_recent_history(db: Session = Depends(database.get_db), user: models.User = Depends(security.get_current_user)):
    query = db.query(models.SearchHistory).filter(models.SearchHistory.user_id == user.id)

    recent_searches = query.order_by(models.SearchHistory.timestamp.desc()).limit(3).all()

    return recent_searches