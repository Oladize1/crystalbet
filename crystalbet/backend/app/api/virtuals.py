# api/virtuals.py

from fastapi import APIRouter, HTTPException
from models.virtual import VirtualSport
from schemas.virtual import VirtualSportCreate, VirtualSportResponse
from services.virtual import VirtualSportService

router = APIRouter()
service = VirtualSportService()

@router.post("/", response_model=VirtualSportResponse)
async def create_virtual_sport(virtual_sport: VirtualSportCreate):
    try:
        created_sport = await service.create_virtual_sport(virtual_sport)
        return created_sport
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[VirtualSportResponse])
async def get_virtual_sports():
    try:
        sports = await service.get_all_virtual_sports()
        return sports
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{sport_id}", response_model=VirtualSportResponse)
async def get_virtual_sport(sport_id: str):
    try:
        sport = await service.get_virtual_sport(sport_id)
        if not sport:
            raise HTTPException(status_code=404, detail="Virtual sport not found")
        return sport
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
