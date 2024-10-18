from fastapi import APIRouter, Depends, HTTPException
from typing import List
from services.admin import AdminService
from schemas.admin import AdminContent, AdminContentCreate, AdminContentUpdate
from core.security import get_current_admin

router = APIRouter()

@router.get("/cms", response_model=List[AdminContent])
async def get_all_content(service: AdminService = Depends()):
    return await service.get_all_content()

@router.get("/cms/{content_id}", response_model=AdminContent)
async def get_content(content_id: str, service: AdminService = Depends()):
    content = await service.get_content(content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.post("/cms", response_model=AdminContent)
async def create_content(content: AdminContentCreate, service: AdminService = Depends(), current_admin: str = Depends(get_current_admin)):
    return await service.create_content(content)

@router.put("/cms/{content_id}", response_model=AdminContent)
async def update_content(content_id: str, content: AdminContentUpdate, service: AdminService = Depends(), current_admin: str = Depends(get_current_admin)):
    updated_content = await service.update_content(content_id, content)
    if not updated_content:
        raise HTTPException(status_code=404, detail="Content not found")
    return updated_content

@router.delete("/cms/{content_id}", response_model=dict)
async def delete_content(content_id: str, service: AdminService = Depends(), current_admin: str = Depends(get_current_admin)):
    result = await service.delete_content(content_id)
    if not result:
        raise HTTPException(status_code=404, detail="Content not found")
    return {"detail": "Content deleted successfully"}
