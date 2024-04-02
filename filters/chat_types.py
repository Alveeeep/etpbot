from aiogram.filters import Filter
from aiogram import Bot, types

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_admins_ids
from database.models import Admin


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self, ) -> None:
        pass

    async def __call__(self, message: types.Message, session: AsyncSession) -> bool:
        admins_list = await orm_get_admins_ids(session)
        return message.from_user.id in admins_list
