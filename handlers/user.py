from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot
from utils.get_from_excel import get_data_from_excel
from sqlalchemy.ext.asyncio import AsyncSession
from filters.chat_types import ChatTypeFilter
from database.orm_query import orm_add_user

user_router = Router()
user_router.message.filter(ChatTypeFilter(['private']))


@user_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    await message.answer("Добро пожаловать. Бот будет присылать информацию о закупках!")
    await orm_add_user(message.from_user.id, session)
