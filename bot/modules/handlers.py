from aiogram import Bot, types, F, Dispatcher, Router
from modules import bot_logic, api
from aiogram.filters.command import Command
from aiogram.types import InputFile
from middlewares.message_middleware import message_middleware
from middlewares.callback_middleware import callback_middleware
from middlewares.inline_middleware import inline_middleware

router = Router()


router.message.middleware(message_middleware())
router.callback_query.middleware(callback_middleware())
router.inline_query.middleware(inline_middleware())

#|=============================[Commands]=============================|
# Хэндлер на /start
@router.message(Command('start'))
async def start(message: types.Message):
    text, markup = await bot_logic.start_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------
# Хэндлер на /menu
@router.message(Command('menu'))
async def menu(message: types.Message):
    text, markup = await bot_logic.menu_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------
# Хэндлер на /admin
@router.message(Command('admin'))
async def menu(message: types.Message):
    r = await api.is_admin(message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admins_cmd(message)
        await message.answer(text, reply_markup=markup, )
#--------------------------------------------------------------------------
# #Хэндлер на любой текст 
# @router.message(F.text)
# async def anymsg(message: types.Message):
    # await api.set_target(message)
@router.message(F.text)
async def anymsg(message: types.Message, bot: Bot):
    text, markup = await bot_logic.menu_cmd(message)
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
#|===========================[End Commands]===========================|




# CALLBACKS #
#|=============================[Utils]=============================|
# Обработчик для callback_data 'back_btn'
@router.callback_query(F.data.startswith("menu "))
async def back_btn(call: types.CallbackQuery):
    text, markup = await bot_logic.menu_cmd(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Коллбек на кнопку приятия соглашения 
@router.callback_query(F.data.startswith("agree "))
async def register_user(call: types.CallbackQuery):
    # await api.create_user(call.message)
    text, markup = await bot_logic.agree(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End utils]===========================|

#|=============================[Admin panel buttons]=============================|
# Обработчик для callback_data 'admin_users'
@router.callback_query(F.data.startswith("admin_users "))
async def admin_users_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_users_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level'
@router.callback_query(F.data.startswith("admin_level "))
async def admin_level_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_level_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_set'
@router.callback_query(F.data.startswith("admin_set "))
async def admin_set_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_set_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        print(r['Reason'], flush=True)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unset'
@router.callback_query(F.data.startswith("admin_unset "))
async def admin_set_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_unset_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_balance'
@router.callback_query(F.data.startswith("admin_balance "))
async def admin_balance_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_balance_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_users_list'
@router.callback_query(F.data.startswith("admin_users_list "))
async def admin_users_list_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_users_list_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_ban'
@router.callback_query(F.data.startswith("admin_ban "))
async def admin_ban_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_ban_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_unban "))
async def admin_unban_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_unban_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_add_user "))
async def admin_unban_btn(call: types.CallbackQuery):
    var = call.data.split(" ")
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_add_user_btn(call.message, var[2])
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level1'
@router.callback_query(F.data.startswith("admin_level1 "))
async def admin_level1_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_level1_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level2'
@router.callback_query(F.data.startswith("admin_level2 "))
async def admin_level2_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_level2_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level3'
@router.callback_query(F.data.startswith("admin_level3 "))
async def admin_level3_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_level3_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_grep_user'
@router.callback_query(F.data.startswith("admin_grep_user "))
async def admin_grep_user_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_grep_user_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_grep_users'
@router.callback_query(F.data.startswith("admin_grep_users "))
async def admin_grep_users_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_grep_users_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
#|===========================[End Admin panel buttons]===========================|




#|=============================[Menu buttons]=============================|
# Обработчик для callback_data 'config_gen'
@router.callback_query(F.data.startswith("config_gen "))
async def config_gen_btn(call: types.CallbackQuery):
    text, markup = await bot_logic.config_gen_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'countries'
@router.callback_query(F.data.startswith("config_menu "))
async def config_menu(call: types.CallbackQuery):
    text, markup = await bot_logic.config_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'test_country'
@router.callback_query(F.data.startswith("test_country "))
async def test_country(call: types.CallbackQuery):
    # Разбираем callback_data для получения tgid и кода страны
    _, tgid, hostname = call.data.split(" ")
    # Используйте tgid и country_code в логике обработки
    text, markup = await bot_logic.test_country_btn(tgid, hostname)

    # Обновляем сообщение с новой информацией
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'account_menu'
@router.callback_query(F.data.startswith("account_menu "))
async def account_menu_btn(call: types.CallbackQuery):
    text, markup = await bot_logic.account_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
