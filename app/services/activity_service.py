from fastapi import Depends
from app.dtos.activity_response_dto import ActivityResponseDTO
from app.dtos.activity_create_dto import ActivityCreateDTO
from app.repositories.activity_repository import (
    ActivityRepository,
    get_activity_repository,
)
from app.services.activity_cache_service import ActivityCacheService, get_activity_cache_service


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository, activity_cache_service: ActivityCacheService):
        self.activity_repo = activity_repo
        self.activity_cache_service = activity_cache_service

    async def create_activity(self, activity_create: ActivityCreateDTO) -> ActivityResponseDTO:
        activity = await self.activity_repo.create_activity(activity_create)
        return ActivityResponseDTO.model_validate(activity)

    async def get_activity(self, activity_id: int) -> ActivityResponseDTO | None:
        activity = await self.activity_repo.get_activity_by_id(activity_id)
        if activity is None:
            return None
        return ActivityResponseDTO.model_validate(activity)

    async def get_user_activities(self, user_id: int, limit: int = 10, offset: int = 0) -> list[ActivityResponseDTO]:
        # 1. Try cache first
        cached_feed = await self.activity_cache_service.get_user_activities(user_id)
        if cached_feed is not None:
            return cached_feed

        # 2. Cache miss — get from DB
        activities = await self.activity_repo.get_user_activities(user_id, limit, offset)
        response = [ActivityResponseDTO.model_validate(activity) for activity in activities]

        # 3. Store in cache
        await self.activity_cache_service.set_user_activities(user_id, response)
        return response


async def get_activity_service(
    activity_repo: ActivityRepository = Depends(get_activity_repository),
    activity_cache_service: ActivityCacheService = Depends(get_activity_cache_service),
) -> ActivityService:
    return ActivityService(activity_repo, activity_cache_service)
