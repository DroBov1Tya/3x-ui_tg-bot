import base64
from modules import BTN, api

#|=============================[Menu]=============================|
async def config_menu_btn(tgid):
    servers = await api.servers_count()
    text, markup = '''
<b>🏴 Выбор стран 🏴</b>
Выберете один из предложенных вариантов
''', BTN.config_menu(tgid, servers)
    return text, markup
#--------------------------------------------------------------------------
async def account_menu_btn(tgid):
    text, markup = '''
<b>👤 Аккаунт</b>
''', BTN.account_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------

#|===========================[End menu]===========================|

#|=============================[admins panel]=============================|
#Админка
async def admins_cmd(message):
    tgid = message.chat.id
    text, markup = '''
<b>DuckSayCrack 🦆</b>
Админ - панель
<i>Можно взаимодействовать с пользователями - банить, удалять, повышать привилегии итд...
Так же для есть возможность разом выкачать всех пользователей из БД</i>
''', BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_users_btn(message):
    tgid = message.chat.id
    text, markup = "Управление", BTN.admin_users_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_level_btn(message):
    tgid = message.chat.id
    text, markup = "Назначение уровня доступа", BTN.admin_level_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_set_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_set(target)
    text, markup = f"Пользователь {target} назначен администратором", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_unset_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_unset(target)
    text, markup = f"Пользователь {target} Разжалован", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_balance_btn(message):
    tgid = message.chat.id
#--------------------------------------------------------------------------
async def admin_users_list_btn(message):
    tgid = message.chat.id
    text, markup = f"Получение информации о пользователе / пользователях", BTN.admin_users_list_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_ban_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_ban(target)
    text, markup = f"Пользователь {target} забанен", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_unban_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_unban(target)
    text, markup = f"Пользователь {target} разбанен", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_add_user_btn(message, target):
    await api.admin_unban(target)
    text, markup = f"Пользователь {target} разбанен", BTN.admin(message.chat.id)
    await message.bot.send_message(chat_id=target, text = '''
<b>DuckSayCrack 🦆</b>

<b>Ваш tgid:</b> <code>{tgid}</code>

<b>Возможности:</b>
<i>Поиск поддоменов и уязвимостей сайтов
Поиск информации по ip адрессу включая открытые порты
Создание одноразовых почтовых ящиков
Поиск информации по железу (Мак адресс, имей)</i>

Для указания цели достаточно просто отправить сообщение

<b>Beta 1.0.2</b>
''', reply_markup=BTN.menu(target))
    return text, markup
#--------------------------------------------------------------------------
async def admin_level1_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_level1(target)
    text, markup = f"Пользователю {target} назначен уровень 1: Demo", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_level2_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_level2(target)
    text, markup = f"Пользователю {target} назначен уровень 2: Advanced", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_level3_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_level3(target)
    text, markup = f"Пользователю {target} назначен уровень 3: Premium", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_grep_user_btn(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    user = await api.user_info(target)
    user_info = {
                "<b>User</b>":         user['user']['tgid'],
                "<b>Nickname</b>":     f"@{user['user']['nickname']}",
                "<b>First name</b>":   user['user']['first_name'],
                "<b>Last name</b>":    user['user']['last_name'],
                "<b>Balance</b>":      user['user']['balance'],
                "<b>User level</b>":   user['user']['user_level'],
                "<b>Is banned</b>":    user['user']['is_banned'],
                "<b>Is admin</b>":     user['user']['is_admin'],
                "<b>Create date</b>":  user['user']['created_at'],
                "<b>Target</b>":       user['user']['target']
            }
    output = str()
    for key, value in user_info.items():
        output += f"{key}: {value}\n"
    text, markup = output, BTN.admin_users_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_grep_users_btn(message):
    tgid = message.chat.id
#--------------------------------------------------------------------------
#|===========================[End admins panel]===========================|
#|=============================[Comands]=============================|
#Событие команды start
async def start_cmd(message):
        # get user info
        userinfo = await api.user_info(message.chat.id)
        # if user not found
        if not userinfo["Success"]:
            # init agree button
            markup = BTN.agree(message.chat.id)
            # agreement message text
            text = 'Пользовательское соглашение'
        # if user found
        else: 
            text, markup = await menu_cmd(message)
        return text, markup
#--------------------------------------------------------------------------
# Собитие кнопки и команды Menu
async def menu_cmd(message):
    tgid = message.chat.id
    text, markup = f'''
<b>Spoof skuf bot 🏴‍☠️</b>

<b>Ваш tgid:</b> <code>{tgid}</code>
<b>Возможности:</b>
<i>Создание впн конфигов нажатием одной кнопки</i>

<b>Beta 1.0.2</b>
''', BTN.menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def test_country_btn(tgid, hostname):
    data, qr_file = await api.test_country(hostname)
    config = data["config"]

    text, markup = f"{config}", BTN.menu(tgid)
    return text, markup, qr_file
#|===========================[Endcomands]===========================|

