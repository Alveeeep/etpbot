from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Admin, User


async def orm_get_admins_ids(session: AsyncSession):
    query = select(Admin.tg_id)
    res = await session.execute(query)
    return res.scalars().all()


async def orm_get_chats_ids(session: AsyncSession):
    query = select(User.tg_id)
    res = await session.execute(query)
    return res.scalars().all()


async def orm_add_user(user_id: int, session: AsyncSession):
    obj = User(tg_id=user_id)
    session.add(obj)
    await session.commit()
