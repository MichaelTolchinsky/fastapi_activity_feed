from fastapi import Depends
from app.dtos.activity_response_dto import ActivityResponseDTO
from app.dtos.activity_create_dto import ActivityCreateDTO
from app.repositories.activity_repository import (
    ActivityRepository,
    get_activity_repository,
)
from app.services.activity_cache_service import ActivityCacheService, get_activity_cache_service
from app.services.kafka_producer import KafkaProducerService, get_kafka_producer_service


class ActivityService:
    def __init__(
        self,
        activity_repo: ActivityRepository,
        activity_cache_service: ActivityCacheService,
        kafka_producer_service: KafkaProducerService,
    ):
        self.activity_repo = activity_repo
        self.activity_cache_service = activity_cache_service
        self.kafka_producer_service = kafka_producer_service

    async def create_activity(self, activity_create: ActivityCreateDTO) -> ActivityResponseDTO:
        activity = await self.activity_repo.create_activity(activity_create)
        activity_dto = ActivityResponseDTO.model_validate(activity)
        message = activity_dto.model_dump()
        message["timestamp"] = activity_dto.timestamp.isoformat()

        self.kafka_producer_service.send(
            topic="activity.created",
            message=message,
        )
        return activity_dto

    async def get_activity(self, activity_id: int) -> ActivityResponseDTO | None:
        activity = await self.activity_repo.get_activity_by_id(activity_id)
        if activity is None:
            return None
        return ActivityResponseDTO.model_validate(activity)

    async def get_user_activities(self, user_id: int, limit: int = 5, offset: int = 0) -> list[ActivityResponseDTO]:
        # 1. Try cache first
        cached_feed = await self.activity_cache_service.get_user_activities(user_id)
        if cached_feed is not None:
            return cached_feed

        # 2. Cache miss — fetch from DB
        activities = await self.activity_repo.get_user_activities(user_id, limit, offset)
        return [ActivityResponseDTO.model_validate(activity) for activity in activities]


async def get_activity_service(
    activity_repo: ActivityRepository = Depends(get_activity_repository),
    activity_cache_service: ActivityCacheService = Depends(get_activity_cache_service),
    kafka_producer_service: KafkaProducerService = Depends(get_kafka_producer_service),
) -> ActivityService:
    return ActivityService(activity_repo, activity_cache_service, kafka_producer_service)
