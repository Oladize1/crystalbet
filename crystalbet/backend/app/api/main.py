from fastapi import APIRouter, Depends, HTTPException
from models.main import AZMenuModel, QuickLinksModel
from services.main import MainService
from schemas.main import AZMenuSchema, QuickLinksSchema, AZMenuResponse, QuickLinksResponse
from typing import List
from fastapi import status

router = APIRouter()

# Dependency injection for MainService
def get_main_service():
    return MainService()

@router.get("/", summary="Homepage Content")
async def get_homepage():
    return {"message": "Welcome to the Homepage"}

@router.get("/api/az-menu", response_model=List[AZMenuResponse], summary="Get AZ Menu Items")
async def get_az_menu(main_service: MainService = Depends(get_main_service)):
    return await main_service.get_az_menu()

@router.get("/api/quick-links", response_model=List[QuickLinksResponse], summary="Get Quick Links")
async def get_quick_links(main_service: MainService = Depends(get_main_service)):
    return await main_service.get_quick_links()

@router.post("/api/az-menu", response_model=AZMenuResponse, status_code=status.HTTP_201_CREATED, summary="Add a new AZ Menu item")
async def add_az_menu_item(item: AZMenuSchema, main_service: MainService = Depends(get_main_service)):
    try:
        return await main_service.add_az_menu_item(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/quick-links", response_model=QuickLinksResponse, status_code=status.HTTP_201_CREATED, summary="Add a new Quick Link")
async def add_quick_link(item: QuickLinksSchema, main_service: MainService = Depends(get_main_service)):
    try:
        return await main_service.add_quick_link(item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
