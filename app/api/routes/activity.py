from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.dtos.activity_response_dto import ActivityResponseDTO
from app.dtos.activity_create_dto import ActivityCreateDTO
from app.services.activity_service import ActivityService, get_activity_service

router = APIRouter(prefix="/activity", tags=["Activity"])


@router.post("/", response_model=ActivityResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_create: ActivityCreateDTO,
    activity_service: ActivityService = Depends(get_activity_service),
):
    created_activity = await activity_service.create_activity(activity_create)
    return created_activity


@router.get("/{activity_id}", response_model=ActivityResponseDTO, status_code=status.HTTP_200_OK)
async def get_activity(activity_id: int, activity_service: ActivityService = Depends(get_activity_service)):
    activity = await activity_service.get_activity(activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.get("/feed/{user_id}", response_model=List[ActivityResponseDTO])
async def get_user_feed(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    activity_service: ActivityService = Depends(get_activity_service),
):
    return await activity_service.get_user_feed(user_id, limit, offset)
