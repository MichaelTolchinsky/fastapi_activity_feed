from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.activity import Activity
from app.db.session import get_db_session
from app.dtos.activity_create_dto import ActivityCreateDTO


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_activity(self, create_activity: ActivityCreateDTO) -> Activity:
        activity = Activity(
            user_id=create_activity.user_id,
            action=create_activity.action,
            target_id=create_activity.target_id,
            timestamp=create_activity.timestamp,
        )

        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def get_activity_by_id(self, activity_id: int) -> Activity | None:
        stmt = select(Activity).where(Activity.id == activity_id)
        result = await self.db.execute(stmt)
        activity = result.scalars().first()
        return activity

    async def get_user_feed(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> list[Activity]:
        stmt = (
            select(Activity)
            .where(Activity.user_id == user_id)
            .order_by(Activity.timestamp.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        activities = result.scalars().all()
        return activities


async def get_activity_repository(
    db: AsyncSession = Depends(get_db_session),
) -> ActivityRepository:
    return ActivityRepository(db)
