from fastapi import Depends
from app.dtos.activity_response_dto import ActivityResponseDTO
from app.dtos.activity_create_dto import ActivityCreateDTO
from app.repositories.activity_repository import (
    ActivityRepository,
    get_activity_repository,
)


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    async def create_activity(
        self, activity_create: ActivityCreateDTO
    ) -> ActivityResponseDTO:
        activity = await self.activity_repo.create_activity(activity_create)
        return ActivityResponseDTO.model_validate(activity)

    async def get_activity(self, activity_id: int) -> ActivityResponseDTO | None:
        activity = await self.activity_repo.get_activity_by_id(activity_id)
        if activity is None:
            return None
        return ActivityResponseDTO.model_validate(activity)


async def get_activity_service(
    activity_repo: ActivityRepository = Depends(get_activity_repository),
) -> ActivityService:
    return ActivityService(activity_repo)
