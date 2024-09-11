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
#[🛜 Url menu]      [🧑‍💻 Ip menu]
#[💻 Hardware]      [👤Account]
def menu(tgid):
    btn1 = InlineKeyboardButton(text='🛜 Url menu', callback_data=f'url_menu {tgid}')
    btn2 = InlineKeyboardButton(text='🧑‍💻 Ip menu', callback_data=f'ip_menu {tgid}')
    btn3 = InlineKeyboardButton(text='💻 Hardware', callback_data=f'hardware_menu {tgid}')
    btn4 = InlineKeyboardButton(text='👤Account', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[☠️ Acunetix]        [🌎 Subdomains]
# [🦴 Fuzzing]      [🖥️ What cms]          
#[🔙 Назад]
def url_menu(tgid):
    btn1 = InlineKeyboardButton(text='☠️ Acunetix ❌', callback_data=f'acunetix {tgid}')
    btn2 = InlineKeyboardButton(text='🌎 Subdomains', callback_data=f'subdomains {tgid}')
    btn3 = InlineKeyboardButton(text='🦴 Fuzzing', callback_data=f'fuzzing {tgid}')
    btn4 = InlineKeyboardButton(text='🖥️ What cms', callback_data=f'what_cms {tgid}')
    btn5 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4],
        [btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[🪬 Nmap ❌]       [🔮 Ip lookup]
#[🔙 Назад]
def ip_menu(tgid):
    btn1 = InlineKeyboardButton(text='🪬 Nmap ❌', callback_data=f'nmap {tgid}')
    btn2 = InlineKeyboardButton(text='🔮 Ip lookup', callback_data=f'ip_lookup {tgid}')
    btn3 = InlineKeyboardButton(text='🩺 Check host', callback_data=f'checkhost {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[🗿 mac lookup]        [📱 Imei lookup]
#[🔙 Назад]
def hardware_menu(tgid):
    btn1 = InlineKeyboardButton(text='🗿 mac lookup', callback_data=f'mac_lookup {tgid}')
    btn2 = InlineKeyboardButton(text='📱 Imei lookup', callback_data=f'imei_lookup {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
#[✉️ Temp mail]     [💾 Saved results ❌]
#[💸 Оплата ❌]    [⚙️ Settings]
#[🔙 Назад]
def account_menu(tgid):
    btn1 = InlineKeyboardButton(text='✉️ Temp mail', callback_data=f'temp_mail {tgid}')
    btn2 = InlineKeyboardButton(text='💾 Saved results ❌', callback_data=f'saved_results {tgid}')
    btn3 = InlineKeyboardButton(text='💸 Оплата ❌', callback_data=f'pay {tgid}')
    btn4 = InlineKeyboardButton(text='⚙️ Settings ❌', callback_data=f'settings {tgid}')
    btn5 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4],
        [btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End menu]===========================|


#|=============================[Save result]=============================|
# [💾 Сохранить]     [🏠 Меню]
def save_result(tgid):
    btn1 = InlineKeyboardButton(text='💾 Сохранить', callback_data=f'save_result {tgid}')
    btn2 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End save result]===========================|

#|=============================[Saved resutls]=============================|
# [💾 Сохранить]     [🏠 Меню]
def saved_results(tgid):
    btn1 = InlineKeyboardButton(text='💾 Сохраненные результаты', callback_data=f'saved_results {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End saved results]===========================|

#|=============================[Subdomains]=============================|
# [🔎 Scan]
# [🔙 Назад]
def subdomains(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Scan subdomains', callback_data=f'subdomains_scan {tgid}')
    btn2 = InlineKeyboardButton(text='🎙️ DNS records', callback_data=f'dns {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'url_menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End subdomains]===========================|

#|=============================[Imei lookup scan]=============================|
# [🔎 Scan]
# [🏠 Меню]
def imei_lookup(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Scan', callback_data=f'Imei_lookup_check {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'hardware_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End Imei lookup scan]===========================|

#|=============================[Nmap]=============================|
# [🪬 Начать скан]          [🏴‍☠️ Поднять флаг]      
# [🏠 Меню]
def nmap(tgid):
    btn1 = InlineKeyboardButton(text='🪬 Начать скан ❌', callback_data=f'nmap_scan {tgid}')
    btn2 = InlineKeyboardButton(text='🏴‍☠️ Поднять флаг ❌', callback_data=f'nmap_flag {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'ip_menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End nmap]===========================|

#|=============================[Fuzzing]=============================|
# [🦴 Начать скан]          [🏴‍☠️ Поднять флаг]   
# [🏠 Меню]
def fuzzing(tgid):
    btn1 = InlineKeyboardButton(text='🦴 Начать скан', callback_data=f'fuzz {tgid}')
    btn2 = InlineKeyboardButton(text='🏴‍☠️ Поднять флаг ❌', callback_data=f'fuzzing_flag {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'url_menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End fuzzing]===========================|


#|=============================[Ip lookup]=============================|
#[🔎 Check]
#[🏠 Меню]
def ip_lookup(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Check', callback_data=f'ip_lookup_check {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'ip_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End ip_lookup]===========================|

#|=============================[DNS scan]=============================|
#[🔎 Check]
#[🏠 Меню]
def dns(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Check', callback_data=f'dns_scan {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'dns {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End DNS scan]===========================|

#|=============================[Checkhost]=============================|
#[🔎 Check]
#[🏠 Меню]
def checkhost(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Check', callback_data=f'checkhost_check {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'ip_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End Checkhost]===========================|

#|=============================[Mac lookup]=============================|
#[🔎 Check]
#[🏠 Меню]
def mac_lookup(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Check', callback_data=f'mac_lookup_check {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'hardware_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End Mac_lookup]===========================|

#|=============================[What cms]=============================|
#[🔎 Check]
#[🏠 Меню]
def what_cms(tgid):
    btn1 = InlineKeyboardButton(text='🔎 Check', callback_data=f'what_cms_check {tgid}')
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'url_menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End what cms]===========================|

#|=============================[Temp mail]=============================|
#[✉️ Создать почту]         [📬 Проверить почтовый ящик]
#[📨 Проверить письмо]     [🏠 Меню]
def temp_mail(tgid):
    btn1 = InlineKeyboardButton(text='✉️ Создать почту', callback_data=f'create_mail {tgid}')
    btn2 = InlineKeyboardButton(text='📬 Проверить почтовый ящик', callback_data=f'check_mailbox {tgid}')
    btn3 = InlineKeyboardButton(text='📨 Проверить письмо ❌', callback_data=f'check_mail_message {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3, btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|===========================[End temp mail]===========================|

#|=============================[Check mailbox]=============================|
#[🔄 Обновить]          [💾 Сохранить]
#[🔙 Назад]
def check_mailbox(tgid):
    btn1 = InlineKeyboardButton(text='🔄 Обновить', callback_data=f'check_mailbox {tgid}')
    btn2 = InlineKeyboardButton(text='💾 Сохранить', callback_data=f'save_result {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'temp_mail {tgid}')
    buttons = [
        [btn1, btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#|=========================[End Check mailbox]=========================|