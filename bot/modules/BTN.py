import json
from typing import List, Dict, Any
from random import choice
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from config import CC, onemonth, sixmonth, year

#|=============================[Admin panel]=============================|
# [🎫 Создать ваучер]
# [🏠 Menu]
# [❌ Delete]
def admin(tgid):
    btn1 = InlineKeyboardButton(text='🎫 Создать ваучер', callback_data=f'admin_create_voucher {tgid}')
    btn2 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    btn3 = InlineKeyboardButton(text='❌ Delete', callback_data=f'delete {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ 1 Month]
# [🕰️ 6 Months]
# [🌍 1 Year]
# [🏠 Menu]
def admin_create_voucher(tgid):
    btn1 = InlineKeyboardButton(text='⏳ 1 Month', callback_data=f'admin_create_voucher_one {tgid}')
    btn2 = InlineKeyboardButton(text='🕰️ 6 Months', callback_data=f'admin_create_voucher_six {tgid}')
    btn3 = InlineKeyboardButton(text='🌍 1 Year', callback_data=f'admin_create_voucher_year {tgid}')
    btn4 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4]
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


#|=============================[Menu]=============================|

def user_agreement(tgid):
    btn1 = InlineKeyboardButton(text='✅', callback_data=f'agree {tgid}')
    btn2 = InlineKeyboardButton(text='❌', callback_data=f'decline {tgid}')
    buttons = [
        [btn1, btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons) 
#--------------------------------------------------------------------------

# [🏴‍☠️ Create config]
# [📋 Learn more]
# [👤 Account]
def menu(tgid):
    btn1 = InlineKeyboardButton(text='🏴‍☠️ Create config', callback_data=f'config_menu {tgid}')
    btn2 = InlineKeyboardButton(text='📋 Learn more', callback_data=f'learn_more {tgid}')
    btn3 = InlineKeyboardButton(text='👤Account', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1],
        [btn2], 
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
# [🏴‍☠️ Создать конфиг]
# [📋 Узнать больше]
# [👤 Аккаунт]
def menu_ru(tgid):
    btn1 = InlineKeyboardButton(text='🏴‍☠️ Создать конфиг', callback_data=f'config_menu {tgid}')
    btn2 = InlineKeyboardButton(text='📋 Узнать больше', callback_data=f'learn_more {tgid}')
    btn3 = InlineKeyboardButton(text='👤 Аккаунт', callback_data=f'account_menu {tgid}')
    buttons = [
        [btn1],
        [btn2], 
        [btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#--------------------------------------------------------------------------

# [💳 Pay subscription]
# [🏠 Menu]
def account_menu(tgid):
    btn1 = InlineKeyboardButton(text='💳 Pay subscription', callback_data=f'pay_subscription {tgid}')
    btn2 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [💳 Оплатить подписку]
# [🏠 Меню]
def account_menu_ru(tgid):
    btn1 = InlineKeyboardButton(text='💳 Оплатить подписку', callback_data=f'top_up_balance {tgid}')
    btn2 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [₿ Pay with crypto]
# [👤 Back] [🏠 Menu]
def top_up_balance(tgid):
    btn1 = InlineKeyboardButton(text='₿ Pay with crypto', callback_data=f'pay_with_crypto {tgid}')
    btn2 = InlineKeyboardButton(text='👤 Back', callback_data=f'account_menu {tgid}')
    btn3 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2, btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [₿ Оплатить криптовалютой]
# [👤 Назад] [🏠 Меню]
def top_up_balance_ru(tgid):
    btn1 = InlineKeyboardButton(text='₿ Оплатить криптовалютой', callback_data=f'pay_with_crypto {tgid}')
    btn2 = InlineKeyboardButton(text='👤 Назад', callback_data=f'account_menu {tgid}')
    btn3 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2, btn3]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#--------------------------------------------------------------------------

# [🅣 USDT]
# [₿ Bitcoin]
# [Ł Litecoin]
# [💎 TON]
# [🔙 Back] [🏠 Menu]
def pay_with_crypto(tgid):
    # Создание кнопок для разных криптовалют с соответствующими эмодзи
    btn1 = InlineKeyboardButton(text='🅣 USDT', callback_data=f'pay_with_usdt {tgid}')
    btn2 = InlineKeyboardButton(text='₿ Bitcoin', callback_data=f'pay_with_btc {tgid}')
    btn3 = InlineKeyboardButton(text='Ł Litecoin', callback_data=f'pay_with_ltc {tgid}')
    btn4 = InlineKeyboardButton(text='💎 TON', callback_data=f'pay_with_ton {tgid}')
    btn5 = InlineKeyboardButton(text='🔙 Back', callback_data=f'top_up_balance {tgid}')
    btn6 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4],
        [btn5, btn6]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ 1 Month Subscription]
# [🕰️ 6 Months Subscription]
# [🌍 1 Year Subscription]
# [🔙 Back] [🏠 Menu]
def pay_with_usdt(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ 1 Month Subscription ~{onemonth}$', callback_data=f'usdt_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ 6 Months Subscription ~{sixmonth}$', callback_data=f'usdt_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 1 Year Subscription ~{year}$', callback_data=f'usdt_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Back', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ 1 Month Subscription]
# [🕰️ 6 Months Subscription]
# [🌍 1 Year Subscription]
# [🔙 Back] [🏠 Menu]
def pay_with_btc(tgid):
    btn1 = InlineKeyboardButton(text=f'🕰️ 6 Months Subscription ~{sixmonth}$', callback_data=f'btc_six_months_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🌍 1 Year Subscription ~{year}$', callback_data=f'btc_year_subscription {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Back', callback_data=f'pay_with_crypto {tgid}')
    btn4 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3, btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ 1 Month Subscription]
# [🕰️ 6 Months Subscription]
# [🌍 1 Year Subscription]
# [🔙 Back] [🏠 Menu]
def pay_with_ltc(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ 1 Month Subscription ~{onemonth}$', callback_data=f'ltc_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ 6 Months Subscription ~{sixmonth}$', callback_data=f'ltc_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 1 Year Subscription ~{year}$', callback_data=f'ltc_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Back', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ 1 Month Subscription]
# [🕰️ 6 Months Subscription]
# [🌍 1 Year Subscription]
# [🔙 Back] [🏠 Menu]
def pay_with_ton(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ 1 Month Subscription ~{onemonth}$', callback_data=f'ton_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ 6 Months Subscription ~{sixmonth}$', callback_data=f'ton_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 1 Year Subscription ~{year}$', callback_data=f'ton_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Back', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [🅣 USDT]
# [₿ Bitcoin]
# [Ł Litecoin]
# [💎 TON]
# [🔙 Назад] [🏠 Меню]
def pay_with_crypto_ru(tgid):
    # Создание кнопок для разных криптовалют с соответствующими эмодзи
    btn1 = InlineKeyboardButton(text='🅣 USDT', callback_data=f'pay_with_usdt {tgid}')
    btn2 = InlineKeyboardButton(text='₿ Bitcoin', callback_data=f'pay_with_btc {tgid}')
    btn3 = InlineKeyboardButton(text='Ł Litecoin', callback_data=f'pay_with_ltc {tgid}')
    btn4 = InlineKeyboardButton(text='💎 TON', callback_data=f'pay_with_ton {tgid}')
    btn5 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'top_up_balance {tgid}')
    btn6 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4],
        [btn5, btn6]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ Подписка на 1 месяц]
# [🕰️ Подписка на 6 месяцев]
# [🌍 Подписка на 1 год]
# [🔙 Назад] [🏠 Меню]
def pay_with_usdt_ru(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ Подписка на 1 месяц ~{onemonth}$', callback_data=f'usdt_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ Подписка на 6 месяцев ~{sixmonth}$', callback_data=f'usdt_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 Подписка на 1 год ~{year}$', callback_data=f'usdt_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [🕰️ Подписка на 6 месяцев]
# [🌍 Подписка на 1 год]
# [🔙 Назад] [🏠 Меню]
def pay_with_btc_ru(tgid):
    btn1 = InlineKeyboardButton(text=f'🕰️ Подписка на 6 месяцев ~{sixmonth}$', callback_data=f'btc_six_months_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🌍 Подписка на 1 год ~{year}$', callback_data=f'btc_year_subscription {tgid}')
    btn3 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'pay_with_crypto {tgid}')
    btn4 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3, btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ Подписка на 1 месяц]
# [🕰️ Подписка на 6 месяцев]
# [🌍 Подписка на 1 год]
# [🔙 Назад] [🏠 Меню]
def pay_with_ltc_ru(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ Подписка на 1 месяц ~{onemonth}$', callback_data=f'ltc_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ Подписка на 6 месяцев ~{sixmonth}$', callback_data=f'ltc_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 Подписка на 1 год ~{year}$', callback_data=f'ltc_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ Подписка на 1 месяц]
# [🕰️ Подписка на 6 месяцев]
# [🌍 Подписка на 1 год]
# [🔙 Назад] [🏠 Меню]
def pay_with_ton_ru(tgid):
    btn1 = InlineKeyboardButton(text=f'⏳ Подписка на 1 месяц ~{onemonth}$', callback_data=f'ton_one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text=f'🕰️ Подписка на 6 месяцев ~{sixmonth}$', callback_data=f'ton_six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text=f'🌍 Подписка на 1 год ~{year}$', callback_data=f'ton_year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'pay_with_crypto {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [⏳ Подписка на 1 месяц]
# [🕰️ Подписка на 6 месяцев]
# [🌍 Подписка на 1 год]
# [🔙 Назад] [🏠 Меню]
def pay_subscription_ru(tgid):
    btn1 = InlineKeyboardButton(text='⏳ Подписка на 1 месяц', callback_data=f'one_month_subscription {tgid}')
    btn2 = InlineKeyboardButton(text='🕰️ Подписка на 6 месяцев', callback_data=f'six_months_subscription {tgid}')
    btn3 = InlineKeyboardButton(text='🌍 Подписка на 1 год', callback_data=f'year_subscription {tgid}')
    btn4 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'account_menu {tgid}')
    btn5 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
        [btn2],
        [btn3],
        [btn4, btn5]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

def cryptopay(tgid, link):
    btn1 = InlineKeyboardButton(text='🪙 Оплатить', url = link)
    btn2 = InlineKeyboardButton(text='🔙 Назад', callback_data=f'pay_with_crypto {tgid}')
    buttons = [
        [btn1],
        [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

def help(tgid):
    telegraph_links = {
    'android': 'https://telegra.ph/VPN-Configuration-Guide-for-Android-10-08',
    'ios': 'https://telegra.ph/VPN-Configuration-Guide-10-08',
    'pc': 'https://telegra.ph/VPN-Configuration-Guide-for-PC-10-08'
    }

    btn1 = InlineKeyboardButton(text='🤖 Android', url=telegraph_links['android'])
    btn2 = InlineKeyboardButton(text='🍏 iOS', url=telegraph_links['ios'])
    btn3 = InlineKeyboardButton(text='💻 PC', url=telegraph_links['pc'])
    btn4 = InlineKeyboardButton(text='❌ Delete', callback_data=f'delete {tgid}')
    buttons = [
        [btn1, btn2, btn3],
        [btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

def help_ru(tgid):
    telegraph_links = {
        'android': 'https://telegra.ph/Rukovodstvo-po-nastrojke-VPN-dlya-Android-10-09',
        'ios': 'https://telegra.ph/VPN-Configuration-Guide-10-09',
        'pc': 'https://telegra.ph/Rukovodstvo-po-nastrojke-VPN-dlya-PK-10-09'
    }

    btn1 = InlineKeyboardButton(text='🤖 Android', url=telegraph_links['android'])
    btn2 = InlineKeyboardButton(text='🍏 iOS', url=telegraph_links['ios'])
    btn3 = InlineKeyboardButton(text='💻 ПК', url=telegraph_links['pc'])
    btn4 = InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete {tgid}')
    buttons = [
        [btn1, btn2, btn3],
        [btn4]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

#|=============================[Utilities]=============================|
#[❌ Delete]
def delete_message(tgid):
    btn1 = InlineKeyboardButton(text='❌ Delete', callback_data=f'delete {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

#[❌ Удалить]
def delete_message_ru(tgid):
    btn1 = InlineKeyboardButton(text='❌ Удалить', callback_data=f'delete {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#--------------------------------------------------------------------------

#[🇬🇧 English] [🇷🇺 Русский]
def choose_language(tgid):
    btn1 = InlineKeyboardButton(text='🇬🇧 English', callback_data=f'en_language {tgid}')
    btn2 = InlineKeyboardButton(text='🇷🇺 Русский', callback_data=f'ru_language {tgid}')
    buttons = [
        [btn1], [btn2]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [🏠 Menu]
def back(tgid):
    btn1 = InlineKeyboardButton(text='🏠 Menu', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

# [🏠 Меню]
def back_ru(tgid):
    btn1 = InlineKeyboardButton(text='🏠 Меню', callback_data=f'menu {tgid}')
    buttons = [
        [btn1],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

#--------------------------------------------------------------------------
#|===========================[End Utilities]===========================|

#|=============================[Config generation]=============================|
#[Dynamic]
#[🎰 Random]
#[🏠 Menu]
def config_menu(tgid: int, servers: Dict[str, Any]) -> InlineKeyboardMarkup:
    """
    Создает динамически расширяющиеся меню конфигурации с кнопками серверов и опцией случайного выбора хоста.

    Args:
        tgid (int): Идентификатор пользователя Telegram.
        servers (Dict[str, Any]): Словарь с информацией о серверах.

    Returns:
        InlineKeyboardMarkup: Разметка для меню с кнопками.
    """
    buttons: List[List[InlineKeyboardButton]] = []
    row: List[InlineKeyboardButton] = []

    # Кнопка для возврата в главное меню
    menu_button = InlineKeyboardButton(
        text="🏠 Menu", 
        callback_data=f'menu {tgid}'
    )
    
    if servers != None:
        for index, server in enumerate(servers.get('result', [])):
            hostname = server['hostname']
            country = CC.get(server["country"], "Unknown")

            button = InlineKeyboardButton(
                text=country,
                callback_data=f'create_config {tgid} {hostname}'
            )
            row.append(button)

            # Формируем ряд из трех кнопок
            if (index + 1) % 3 == 0:
                buttons.append(row)
                row = []

        # Добавляем оставшиеся кнопки в последний ряд, если есть
        if row:
            buttons.append(row)

        # Логика случайного выбора хоста
        if servers.get('result'):
            random_server = choice(servers['result'])
            random_hostname = random_server['hostname']
        else:
            random_hostname = 'no_servers'

        # Кнопка для случайного выбора сервера
        random_button = InlineKeyboardButton(
            text="🎰 Random", 
            callback_data=f'create_config {tgid} {random_hostname}'
        )

        # Добавляем кнопки в меню
        buttons.append([random_button])
        buttons.append([menu_button])

    else:
        buttons.append([menu_button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------

#[Dynamic]
#[🎰 Случайный]
#[🏠 Меню]
def config_menu_ru(tgid: int, servers: Dict[str, Any]) -> InlineKeyboardMarkup:
    """
    Создает динамически расширяющееся меню конфигурации с кнопками серверов и опцией случайного выбора хоста.

    Args:
        tgid (int): Идентификатор пользователя Telegram.
        servers (Dict[str, Any]): Словарь с информацией о серверах.

    Returns:
        InlineKeyboardMarkup: Разметка для меню с кнопками.
    """
    buttons: List[List[InlineKeyboardButton]] = []
    row: List[InlineKeyboardButton] = []

    # Кнопка для возврата в главное меню
    menu_button = InlineKeyboardButton(
        text="🏠 Меню", 
        callback_data=f'menu {tgid}'
    )
    
    if servers is not None:
        for index, server in enumerate(servers.get('result', [])):
            hostname = server['hostname']
            country = CC.get(server["country"], "Неизвестно")

            button = InlineKeyboardButton(
                text=country,
                callback_data=f'create_config {tgid} {hostname}'
            )
            row.append(button)

            # Формируем ряд из трех кнопок
            if (index + 1) % 3 == 0:
                buttons.append(row)
                row = []

        # Добавляем оставшиеся кнопки в последний ряд, если есть
        if row:
            buttons.append(row)

        # Логика случайного выбора хоста
        if servers.get('result'):
            random_server = choice(servers['result'])
            random_hostname = random_server['hostname']
        else:
            random_hostname = 'no_servers'

        # Кнопка для случайного выбора сервера
        random_button = InlineKeyboardButton(
            text="🎰 Случайный", 
            callback_data=f'create_config {tgid} {random_hostname}'
        )

        # Добавляем кнопки в меню
        buttons.append([random_button])
        buttons.append([menu_button])

    else:
        buttons.append([menu_button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
#--------------------------------------------------------------------------
