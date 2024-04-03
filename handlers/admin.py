from aiogram import F, Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.get_from_excel import get_data_from_excel
from sqlalchemy.ext.asyncio import AsyncSession
from filters.chat_types import ChatTypeFilter, IsAdmin
from database.orm_query import orm_get_chats_ids
from kbds.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


async def _send_to_users(session: AsyncSession, data: str, bot: Bot):
    users = await orm_get_chats_ids(session)
    for chat_id in users:
        await bot.send_message(chat_id, data, parse_mode='HTML')


class Settings(StatesGroup):
    receiving = State()
    received = State()


@admin_router.message(Command("send"))
async def admin_sending(message: types.Message, state: FSMContext):
    await message.answer("Отправьте excel файл")
    await state.set_state(Settings.receiving)


@admin_router.message(Settings.receiving)
@admin_router.message(F.content_type.in_({'document'}))
async def receiving_excel(message: types.Message, state: FSMContext, bot: Bot):
    document = message.document
    if document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        await bot.download(document, "C:\\Users\\alvir\\PycharmProjects\\etpbot\\utils\\{}".format(document.file_name))
        await state.update_data(receiving=document.file_name)
        await message.answer("Начать рассылку?",
                             reply_markup=get_keyboard(["Да", "Нет"], placeholder="Ответ:", sizes=(2,), ))
        await state.set_state(Settings.received)


@admin_router.message(Settings.received)
@admin_router.message(F.text == "Да")
async def confirm_send(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    data = await state.get_data()
    res = get_data_from_excel(data['receiving'])
    await _send_to_users(session, res, bot)
    await message.answer("Отправлено", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()


@admin_router.message(Settings.received)
@admin_router.message(F.text == "Нет")
async def confirm_send(message: types.Message, state: FSMContext):
    await message.answer("Действия отменены.", reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
