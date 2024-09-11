from modules import BTN, api

#|=============================[Menu]=============================|
async def url_menu_btn(tgid):
    text, markup = '''
<b>🛜 Url menu</b>
Поиск уязвимостей и утечек по url
''', BTN.url_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def ip_menu_btn(tgid):
    text, markup = '''
<b>🧑‍💻 Ip menu</b>
Пробив по ip
''', BTN.ip_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def hardware_menu_btn(tgid):
    text, markup = '''
<b>💻 Hardware</b>
Поиск информации по устройству
''', BTN.hardware_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def account_menu_btn(tgid):
    text, markup = '''
<b>👤 Аккаунт</b>
''', BTN.account_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Subdomains
async def subdomains_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🌎 Subdomains</b> - поиск поддоменов у сайта
(Работает только с url, ip не указывать)
''', BTN.subdomains((tgid))
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Fuzzing
async def fuzzing_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🦴 Fuzzing</b> - Скан интересных мест на сайте: файлы, директории итд
|BETA - в таргет нужно указать сайт по примеру example.com без 
|http:// и подобного.
|Если нужен угубленный поиск в уже найденных директориях то в 
|таргет нужно указать новый адресс
|Как пример если была найдена директория api example.com/api
''', BTN.fuzzing(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Nmap
async def nmap_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🪬 Nmap</b> - Скан открытых портов и их служб у ip адресса 
''', BTN.nmap(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Saved results
async def saved_results_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>Saved results</b> [В разработке]
''', BTN.saved_results(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Ip lookup
async def ip_lookup_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🔮Ip lookup</b> - Проверка локации и хостинга ip адресса
''', BTN.ip_lookup(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на temp mail
async def temp_mail_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>✉️ Temp mail</b> - Одноразовая почта
''', BTN.temp_mail(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на mac lookup
async def mac_lookup_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🗿 Mac lookup</b> - Пробив вендора по мак адрессу
''', BTN.mac_lookup(tgid)
    return text, markup
#--------------------------------------------------------------------------\
#Событие при нажатии на what cms
async def what_cms_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🖥️ What cms</b> - Проверка бэкэнда сайта
''', BTN.what_cms(tgid)
    return text, markup
#--------------------------------------------------------------------------\
#Событие при нажатии на what cms
async def imei_lookup_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>📱 Imei lookup</b>- Проверка imei
''', BTN.imei_lookup(tgid)
    return text, markup
#--------------------------------------------------------------------------\
async def checkhost_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🩺 Checkhost</b> - Проверяет жив хост или нет, 
можно указать как ip так и домен
''', BTN.checkhost(tgid)
    return text, markup
#--------------------------------------------------------------------------\
async def dns_btn(message):
    tgid = message.chat.id
    text, markup = '''
<b>🎙️ DNS records</b> - Поиск записей в DNS серверах,
может найти хосты относящиеся к цели,
но не имеющие в названии искаемого домена
<b>Хороший пример</b>: <code>tesla.com</code>
''', BTN.dns(tgid)
    return text, markup
#--------------------------------------------------------------------------\
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
<b>DuckSayCrack 🦆</b>

<b>Ваш tgid:</b> <code>{tgid}</code>
<b>Возможности:</b>
<i>Поиск поддоменов и уязвимостей сайтов
Поиск информации по ip адрессу включая открытые порты
Создание одноразовых почтовых ящиков
Поиск информации по железу (Мак адресс, имей)</i>

Для указания цели достаточно просто отправить сообщение

<b>Beta 1.0.2</b>
''', BTN.menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
#Событие при нажатии на Save result
async def save_result_btn(message):
    tgid = message.chat.id
    text, markup = '''
Save result [В разработке]
''', BTN.save_result(tgid)
    return text, markup
#|===========================[Endcomands]===========================|

