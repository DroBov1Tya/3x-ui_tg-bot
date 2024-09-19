from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent


#|=============================[Admin panel]=============================|
#[🪄 Управление пользователями][Просмотреть логи][]
#[][][]
def admin(tgid):
    btn1 = InlineKeyboardButton(text='🪄 Управление пользователями', callback_data=f'admin_users {tgid}')
    btn2 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    #btn3 = InlineKeyboardButton(text='🎯 Set target', callback_data=f'target {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
def admin_users_menu(tgid):
#[☭ Уровень доступа][⚠️ Назначить админа][💸 Изменить баланс]
#[🧍 Пользователи][🔨 Забанить][🛠️ Разабанить]
#[🏠 Меню]
    btn1 = InlineKeyboardButton(text='☭ Уровень доступа', callback_data=f'admin_level {tgid}')
    btn2 = InlineKeyboardButton(text='🧍 Пользователи', callback_data=f'admin_users_list {tgid}')
    btn3 = InlineKeyboardButton(text='🔨 Забанить', callback_data=f'admin_ban {tgid}')
    btn4 = InlineKeyboardButton(text='🛠️ Разабанить', callback_data=f'admin_unban {tgid}')
    btn5 = InlineKeyboardButton(text='💸 Изменить баланс ❌', callback_data=f'admin_balance {tgid}')
    btn6 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4],
        [btn5, btn6]
    ] 
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[💪🏻 Level 1: Demo]
#[💪🏽 Level 2: Advanced]
#[💪🏿 Level 3: Premium]
def admin_level_menu(tgid):
    btn1 = InlineKeyboardButton(text='💪🏻 Level 1: Demo', callback_data=f'admin_level1 {tgid}')
    btn2 = InlineKeyboardButton(text='💪🏽 Level 2: Advanced', callback_data=f'admin_level2 {tgid}')
    btn3 = InlineKeyboardButton(text='💪🏿 Level 3: Premium', callback_data=f'admin_level3 {tgid}')
    btn4 = InlineKeyboardButton(text='⚠️ Level 9000: Admin', callback_data=f'admin_set {tgid}')
    btn5 = InlineKeyboardButton(text='🔪 Kill Admin', callback_data=f'admin_unset {tgid}')
    btn6 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'admin_users {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3,],
        [btn4, btn5],
        [btn6]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[🪄 Управление пользователями][Просмотреть логи][]
#[][][]
def admin_users_list_menu(tgid):
    btn1 = InlineKeyboardButton(text='👤 Получить информацию о пользователе', callback_data=f'admin_grep_user {tgid}')
    btn2 = InlineKeyboardButton(text='👥 Скачать информацию о всех пользователях ❌', callback_data=f'admin_grep_users {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'admin_users {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[Разбанить]
#[Отказать]
def admin_add_user(admin, target):
    btn1 = InlineKeyboardButton(text='🛠️ Разрешить', callback_data=f'admin_add_user {admin} {target}')
    btn2 = InlineKeyboardButton(text='🔨 Отказать', callback_data=f'admin_ban {admin} {target}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End Admin panel]===========================|

#|=============================[Start]=============================|
# [✅ Согласиться]
# [🗒️ Terms & Conditions]
def agree(tgid):
    btn1 = InlineKeyboardButton(text='✅ Согласиться', callback_data=f'agree {tgid}')
    #btn2 = InlineKeyboardButton(text='🗒️ Соглашение', url="https://telegra.ph/Test-12-21-370")
    buttons = [
        [btn1],
        #[btn2],
    ] 
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
# [🏠 Меню]
def back(tgid):
    btn1 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End Start]===========================|




#|=============================[Menu]=============================|
#[🏴‍☠️ Создать конфиг]      []
#[]      [👤Account]
def menu(tgid):
    btn1 = InlineKeyboardButton(text='🏴‍☠️ Создать конфиг', callback_data=f'config_menu {tgid}')
    btn2 = InlineKeyboardButton(text='👤Account', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1, btn2],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[]      []
#[]      []
def config_menu(tgid):
    btn1 = InlineKeyboardButton(text='🇦🇽 Test country', callback_data=f'test_country {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------🇦🇮