from aiogram import Bot, types, F, Dispatcher, Router
from modules import logic, api
from aiogram.filters.command import Command
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
    text, markup = await logic.start_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------
# Хэндлер на /menu
@router.message(Command('menu'))
async def menu(message: types.Message):
    text, markup = await logic.menu_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------
# Хэндлер на /admin
@router.message(Command('admin'))
async def menu(message: types.Message):
    r = await api.is_admin(message.chat.id)
    if r['Success']:
        text, markup = await logic.admins_cmd(message)
        await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------
#Хэндлер на любой текст 
@router.message(F.text)
async def anymsg(message: types.Message):
    await api.set_target(message)
# @router.message(F.text)
# async def anymsg(message: types.Message, bot: Bot):
#     await api.set_target(message)
#     text, markup = await logic.message_encode(message)
#     await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
#|===========================[End Commands]===========================|




# CALLBACKS #
#|=============================[Utils]=============================|
# Обработчик для callback_data 'back_btn'
@router.callback_query(F.data.startswith("menu "))
async def back_btn(call: types.CallbackQuery):
    text, markup = await logic.menu_cmd(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'target'
@router.callback_query(F.data.startswith("target "))
async def target_btn(call: types.CallbackQuery):
    text, markup = await logic.target_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'save_result'
@router.callback_query(F.data.startswith("save_result "))
async def save_result_btn(call: types.CallbackQuery):
    text, markup = await logic.save_result_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Коллбек на кнопку приятия соглашения 
@router.callback_query(F.data.startswith("agree "))
async def register_user(call: types.CallbackQuery):
    # await api.create_user(call.message)
    text, markup = await logic.agree(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End utils]===========================|

#|=============================[Admin panel buttons]=============================|
# Обработчик для callback_data 'admin_users'
@router.callback_query(F.data.startswith("admin_users "))
async def admin_users_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_users_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level'
@router.callback_query(F.data.startswith("admin_level "))
async def admin_level_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_level_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_set'
@router.callback_query(F.data.startswith("admin_set "))
async def admin_set_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_set_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        print(r['Reason'], flush=True)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unset'
@router.callback_query(F.data.startswith("admin_unset "))
async def admin_set_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_unset_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_balance'
@router.callback_query(F.data.startswith("admin_balance "))
async def admin_balance_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_balance_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_users_list'
@router.callback_query(F.data.startswith("admin_users_list "))
async def admin_users_list_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_users_list_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_ban'
@router.callback_query(F.data.startswith("admin_ban "))
async def admin_ban_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_ban_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_unban "))
async def admin_unban_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_unban_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_add_user "))
async def admin_unban_btn(call: types.CallbackQuery):
    var = call.data.split(" ")
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_add_user_btn(call.message, var[2])
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level1'
@router.callback_query(F.data.startswith("admin_level1 "))
async def admin_level1_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_level1_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level2'
@router.callback_query(F.data.startswith("admin_level2 "))
async def admin_level2_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_level2_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_level3'
@router.callback_query(F.data.startswith("admin_level3 "))
async def admin_level3_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_level3_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_grep_user'
@router.callback_query(F.data.startswith("admin_grep_user "))
async def admin_grep_user_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_grep_user_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_grep_users'
@router.callback_query(F.data.startswith("admin_grep_users "))
async def admin_grep_users_btn(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await logic.admin_grep_users_btn(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
#|===========================[End Admin panel buttons]===========================|




#|=============================[Menu buttons]=============================|
# Обработчик для callback_data 'url_menu'
@router.callback_query(F.data.startswith("url_menu "))
async def url_menu_btn(call: types.CallbackQuery):
    text, markup = await logic.url_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'ip_menu'
@router.callback_query(F.data.startswith("ip_menu "))
async def ip_menu_btn(call: types.CallbackQuery):
    text, markup = await logic.ip_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'hardware_menu'
@router.callback_query(F.data.startswith("hardware_menu "))
async def hardware_menu_btn(call: types.CallbackQuery):
    text, markup = await logic.hardware_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'account_menu'
@router.callback_query(F.data.startswith("account_menu "))
async def account_menu_btn(call: types.CallbackQuery):
    text, markup = await logic.account_menu_btn(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'temp mail'
@router.callback_query(F.data.startswith("temp_mail "))
async def temp_mail_btn(call: types.CallbackQuery):
    text, markup = await logic.temp_mail_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'imei_lookup'
@router.callback_query(F.data.startswith("imei_lookup "))
async def imei_lookup_btn(call: types.CallbackQuery):
    text, markup = await logic.imei_lookup_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'subdomains'
@router.callback_query(F.data.startswith("subdomains "))
async def subdomains_btn(call: types.CallbackQuery):
    text, markup = await logic.subdomains_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'fuzzing'
@router.callback_query(F.data.startswith("fuzzing "))
async def fuzzing_btn(call: types.CallbackQuery):
    text, markup = await logic.fuzzing_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'nmap'
@router.callback_query(F.data.startswith("nmap "))
async def nmap_btn(call: types.CallbackQuery):
    text, markup = await logic.nmap_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'saved_results'
@router.callback_query(F.data.startswith("saved_results "))
async def saved_results_btn(call: types.CallbackQuery):
    text, markup = await logic.saved_results_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'ip_lookup'
@router.callback_query(F.data.startswith("ip_lookup "))
async def ip_lookup_btn(call: types.CallbackQuery):
    text, markup = await logic.ip_lookup_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'checkhost'
@router.callback_query(F.data.startswith("checkhost "))
async def checkhost_btn(call: types.CallbackQuery):
    text, markup = await logic.checkhost_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'mac_lookup'
@router.callback_query(F.data.startswith("mac_lookup "))
async def mac_lookup_btn(call: types.CallbackQuery):
    text, markup = await logic.mac_lookup_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'what_cms'
@router.callback_query(F.data.startswith("what_cms "))
async def what_cms_btn(call: types.CallbackQuery):
    text, markup = await logic.what_cms_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End Menu buttons]===========================|






#|=============================[Subdomains buttons]=============================|
# Обработчик для callback_data 'subdomains_scan'
@router.callback_query(F.data.startswith("subdomains_scan "))
async def subdomains_scan_btn(call: types.CallbackQuery):
    text, markup = await logic.subdomains_scan_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'dns_scan'
@router.callback_query(F.data.startswith("dns "))
async def dns_btn(call: types.CallbackQuery):
    text, markup = await logic.dns_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'dns_scan'
@router.callback_query(F.data.startswith("dns_scan "))
async def dns_scan_btn(call: types.CallbackQuery):
    text, markup = await logic.dns_scan_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End subdomains buttons]===========================|

#|=============================[Nmap buttons]=============================|
# Обработчик для callback_data 'nmap_flag'
@router.callback_query(F.data.startswith("nmap_flag "))
async def nmap_flag_btn(call: types.CallbackQuery):
    text, markup = await logic.nmap_flag_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'nmap_scan'
@router.callback_query(F.data.startswith("nmap_scan "))
async def nmap_scan_btn(call: types.CallbackQuery):
    text, markup = await logic.nmap_scan_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End nmap buttons]===========================|
    
#|=============================[Fuzzing buttons]=============================|
# Обработчик для callback_data 'fuzzing_flag'
@router.callback_query(F.data.startswith("fuzzing_flag "))
async def fuzzing_flag_btn(call: types.CallbackQuery):
    text, markup = await logic.fuzzing_flag_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End fuzzing buttons]===========================|
    
#|=============================[Ip lookup]=============================|
# Обработчик для callback_data 'ip lookup'
@router.callback_query(F.data.startswith("ip_lookup_check "))
async def ip_lookup_check_btn(call: types.CallbackQuery):
    text, markup = await logic.ip_lookup_check_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End ip lookup]===========================|
    
#|=============================[checkhost]=============================|
# Обработчик для callback_data 'checkhost'
@router.callback_query(F.data.startswith("checkhost_check "))
async def checkhost_check_btn(call: types.CallbackQuery):
    text, markup = await logic.checkhost_check_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End ip lookup]===========================|
    
#|=============================[Mac lookup]=============================|
# Обработчик для callback_data 'mac lookup'
@router.callback_query(F.data.startswith("mac_lookup_check "))
async def mac_lookup_check_btn(call: types.CallbackQuery):
    text, markup = await logic.mac_lookup_check_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End mac lookup]===========================|
    
#|=============================[Imei lookup]=============================|
# Обработчик для callback_data 'ip lookup'
@router.callback_query(F.data.startswith("Imei_lookup_check "))
async def imei_lookup_check_btn(call: types.CallbackQuery):
    text, markup = await logic.imei_lookup_check_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End Imei lookup]===========================|
    

#|=============================[What cms]=============================|
# Обработчик для callback_data 'what_cms'
@router.callback_query(F.data.startswith("what_cms_check "))
async def what_cms_check_btn(call: types.CallbackQuery):
    text, markup = await logic.what_cms_check_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End What cms]===========================|

#|=============================[temp mail]=============================|
# Обработчик для callback_data 'create mail'
@router.callback_query(F.data.startswith("create_mail "))
async def create_mail_btn(call: types.CallbackQuery):
    text, markup = await logic.create_mail_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("check_mailbox "))
async def check_mailbox_btn(call: types.CallbackQuery):
    text, markup = await logic.check_mailbox_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("check_mail_message "))
async def check_mail_message_btn(call: types.CallbackQuery):
    text, markup = await logic.check_mail_message_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End temp mail]=============================|

#|=============================[Fuzz]=============================|
# Обработчик для callback_data 'fuzz'
@router.callback_query(F.data.startswith("fuzz "))
async def fuzzing_scan_btn(call: types.CallbackQuery):
    text, markup = await logic.fuzzing_scan_btn(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#|===========================[End Fuzz]===========================|