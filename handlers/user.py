from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.get_from_excel import get_data_from_excel
from sqlalchemy.ext.asyncio import AsyncSession
from filters.chat_types import ChatTypeFilter
from database.orm_query import orm_add_user, orm_get_chats_ids

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))


@user_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    await message.answer("Добро пожаловать. Бот будет присылать информацию о закупках!")
    if message.chat.id not in await orm_get_chats_ids(session):
        await orm_add_user(message.chat.id, session)
    else:
        await message.answer("Вы уже подписаны на рассылку")
