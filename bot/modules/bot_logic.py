import base64
import logging
import time
from modules import lang_text
from modules import BTN, api
from config import logger, onemonth, sixmonth, year
#|=============================[Menu]=============================|
#Событие команды start
async def start_cmd(message):
        userinfo = await api.user_info(message.chat.id)
        is_banned = userinfo["user"]["is_banned"]
        if userinfo["Success"] and is_banned == False:
            text, markup = lang_text.language, BTN.choose_language(message.chat.id)
            return text, markup
        
        else: 
            text, markup = lang_text.user_agreement, BTN.user_agreement(message.chat.id)
            return text, markup
#--------------------------------------------------------------------------

async def agree(tgid):
    await api.agree(tgid)
    text, markup = await language_cmd(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def decline(tgid):
    text, markup = lang_text.decline, BTN.user_agreement(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def language_cmd(tgid):
    text, markup = '''
For the best experience, you can choose the bot's language. 🌐
''', BTN.choose_language(tgid)
    return text, markup
#--------------------------------------------------------------------------

# Собитие кнопки и команды Menu
async def menu_cmd(message):
    tgid = message.chat.id
    lang = (await api.check_language(tgid)).get("lang")
    if lang == "en":
        text, markup = lang_text.menu_en, BTN.menu(tgid)
        return text, markup
    
    elif lang == "ru":
        text, markup = lang_text.menu_ru, BTN.menu_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def help_cmd(tgid):
    lang = (await api.check_language(tgid)).get("lang")
    if lang == "en":
        text, markup = lang_text.help_cmd_en, BTN.help(tgid)
        return text, markup
    elif lang == "ru":
        text, markup = lang_text.help_cmd_ru, BTN.help_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def learn_more(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    if lang == "en":
        text, markup = lang_text.learn_more_en, BTN.back(tgid)
        return text, markup
    elif lang == "ru":
        text, markup = lang_text.learn_more_ru, BTN.back_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def create_config(message, hostname):
    tgid = message.chat.id
    config_limit = (await api.check_config_limit(tgid)).get("config_limit")
    lang = (await api.check_language(message.chat.id)).get("lang")
    config_ttl = (await api.getsubsctiption(tgid)).get("subscription") * 1000
    try:
        if config_limit > 0:
            data, qr_file = await api.create_config(message, hostname, config_ttl)

            if lang == "en":
                if not data:
                    text = "Your subscription has expired, would you like to renew it?"
                    markup = BTN.pay_with_crypto(tgid)
                    markup_delete = BTN.delete_message(tgid)
                    return text, markup, markup_delete, None, lang
                else:
                    config = data["config"]
                    await api.reduce_config_limit(tgid)
                    text, markup, markup_delete = f"{config}", BTN.menu(tgid), BTN.delete_message(tgid)
                    return text, markup, markup_delete, qr_file, lang
                
            elif lang == "ru":
                if not data:
                    text = "Ваша подписка закончилась, хотите её обновить?"
                    markup = BTN.pay_with_crypto(tgid)
                    markup_delete = BTN.delete_message_ru(tgid)
                    return text, markup, markup_delete, None, lang
                else:
                    config = data["config"]

                    text, markup, markup_delete = f"{config}", BTN.menu_ru(tgid), BTN.delete_message_ru(tgid)
                    return text, markup, markup_delete, qr_file, lang
        else:
            if lang == "en":
                text = "You have reached the configuration limit."
                markup = BTN.pay_subscription(tgid)
                markup_delete = BTN.delete_message(tgid)
                return text, markup, markup_delete, None, lang
            elif lang == "ru":
                text = "Вы исчерпали лимит конфигов."
                markup = BTN.pay_with_crypto(tgid)
                markup_delete = BTN.delete_message_ru(tgid)
                return text, markup, markup_delete, None, lang
    except Exception as e:
        # Обрабатываем любые исключения, которые могут возникнуть
        logger.error(f"Error in create_config: {str(e)}")
        if lang == "en":
            text = "An error occurred while generating the configuration. Please try again later."
            markup = BTN.menu(tgid)
            markup_delete = BTN.delete_message(tgid)
            return text, markup, markup_delete, None, lang
        elif lang == "ru":
            text = "Произошла ошибка при генерации конфига. Пожалуйста попробуйте позже."
            markup = BTN.menu_ru(tgid)
            markup_delete = BTN.delete_message_ru(tgid)
            return text, markup, markup_delete, None, lang
#--------------------------------------------------------------------------

async def config_menu(tgid: int):
    servers = await api.servers_count()
    config_limit = (await api.check_config_limit(tgid)).get("config_limit")
    lang = (await api.check_language(tgid)).get("lang")

    if servers is None:
        if lang == "en":
            text, markup = lang_text.config_menu_without_en, BTN.config_menu(tgid, servers)
            return text, markup
        elif lang == "ru":
            text, markup = lang_text.config_menu_without_ru, BTN.config_menu_ru(tgid, servers)
            return text, markup
    else:
        if lang == "en":
            text, markup = await lang_text.config_menu_en(config_limit), BTN.config_menu(tgid, servers)
            return text, markup
        elif lang == "ru":
            text, markup = await lang_text.config_menu_ru(config_limit), BTN.config_menu_ru(tgid, servers)
            return text, markup
#--------------------------------------------------------------------------

async def account_menu(tgid: int):
    subsctiption = await api.getsubsctiption(tgid)
    lang = (await api.check_language(tgid)).get("lang")
    current_time = int(time.time())
    # Формируем вывод текста с учетом баланса
    if lang == "en":
        subscription_status = await format_subscription_status(subsctiption.get("subscription"), current_time)
        text = await lang_text.account_menu_en(subscription_status)

        # Возвращаем текст и разметку
        markup = BTN.account_menu(tgid)
        return text, markup
    
    elif lang == "ru":
        subscription_status = await format_subscription_status_ru(subsctiption.get("subscription"), current_time)
        text = await lang_text.account_menu_ru(subscription_status)

        # Возвращаем текст и разметку
        markup = BTN.account_menu_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def top_up_balance(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    if lang == "en":
        text, markup = lang_text.top_up_balance_en, BTN.top_up_balance(tgid)
        return text, markup
    
    elif lang == "ru":
        text, markup = lang_text.top_up_balance_ru, BTN.top_up_balance_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def pay_with_crypto(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    if lang == "en":
        text, markup = lang_text.pay_subscription_en, BTN.pay_with_crypto(tgid)
        return text, markup
    elif lang == "ru":
        text, markup = lang_text.pay_subscription_ru, BTN.pay_with_crypto_ru (tgid)
        return text, markup
#--------------------------------------------------------------------------

async def pay_with_usdt(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    one_month_usd = onemonth
    six_month_usd = sixmonth  # 5 * 6 - 9% скидка
    twelve_month_usd = year  # 5 * 12 - 18% скидка

    if lang == "en":
        text = await lang_text.usdt_sub_en(one_month_usd, six_month_usd, twelve_month_usd)
        markup = BTN.pay_with_usdt(tgid)
        return text, markup
    
    elif lang == "ru":
        text = await lang_text.usdt_sub_ru(one_month_usd, six_month_usd, twelve_month_usd)
        markup = BTN.pay_with_usdt_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def pay_with_btc(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    crypto_type = "BTC"
    six_month_crypto, twelve_month_crypto = await api.calculate_subscription_prices(crypto_type)
    
    if lang == "en":
        text = await lang_text.bct_sub_en(six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_btc(tgid)
        return text, markup
    
    elif lang == "ru":
        text = await lang_text.bct_sub_ru(six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_btc_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def pay_with_ltc(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    crypto_type = "LTC"
    one_month_crypto, six_month_crypto, twelve_month_crypto = await api.calculate_subscription_prices(crypto_type)

    if lang == "en":
        text = await lang_text.ltc_sub_en(one_month_crypto, six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_ltc(tgid)
        return text, markup
    
    elif lang == "ru":
        text = await lang_text.ltc_sub_ru(one_month_crypto, six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_ltc_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------

async def pay_with_ton(tgid: int):
    lang = (await api.check_language(tgid)).get("lang")
    crypto_type = "TON"
    one_month_crypto, six_month_crypto, twelve_month_crypto = await api.calculate_subscription_prices(crypto_type)

    if lang == "en":
        text = await lang_text.ton_sub_en(one_month_crypto, six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_ton(tgid)
        return text, markup
    
    elif lang == "ru":
        text = await lang_text.ton_sub_ru(one_month_crypto, six_month_crypto, twelve_month_crypto)
        markup = BTN.pay_with_ton_ru(tgid)
        return text, markup
#--------------------------------------------------------------------------


#|=============================[admins panel]=============================|
#Админка
async def admins_cmd(message):
    tgid = message.chat.id
    text, markup = '''
Админ - панель
<i>Основная функция - создание ваучеров</i>
''', BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_create_voucher(message):
    tgid = message.chat.id
    text, markup = lang_text.admin_createvoucher, BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_users(message):
    tgid = message.chat.id
    text, markup = "Управление", BTN.admin_users_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_ban(message, target):
    tgid = message.chat.id
    await api.admin_ban(target)
    text, markup = f"Пользователь {target} забанен", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_unban(message):
    tgid = message.chat.id
    target = await api.fetch_target(tgid)
    await api.admin_unban(target)
    text, markup = f"Пользователь {target} разбанен", BTN.admin(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_add_user(message, target):
    await api.admin_unban(target)
    text, markup = f"Пользователь {target} разбанен", BTN.admin(message.chat.id)
    await message.bot.send_message(chat_id=target, text = '''
<b>🏴 Выбор стран 🏴</b>
Выберете один из предложенных вариантов
''', reply_markup=BTN.menu(target))
    return text, markup

#|=============================[Admin Vouchers create]=============================|
async def admin_create_voucher_one(message):
    tgid = message.chat.id
    r = await api.admin_create_voucher_one()
    vaucher_code = r.get("voucher")
    text, markup = f"🎁 <b>1 month voucher code:</b> <code>{vaucher_code}</code>", BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_create_voucher_six(message):
    tgid = message.chat.id
    r = await api.admin_create_voucher_six()
    vaucher_code = r.get("voucher")
    text, markup = f"🎁<b>6 month voucher code:</b> <code>{vaucher_code}</code>", BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def admin_create_voucher_year(message):
    tgid = message.chat.id
    r = await api.admin_create_voucher_year()
    vaucher_code = r.get("voucher")
    text, markup = f"🎁 <b>1 year voucher code:</b> <code>{vaucher_code}</code>", BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------

#|=============================[SRC]=============================|
async def format_subscription_status(subscription_end: int, current_time: int) -> str:
    """
    Форматирует статус подписки с учетом оставшегося времени.
    """
    diff = subscription_end - current_time

    if diff is None:
        diff = 0

    if diff <= 0:
        return "❌ Your subscription has ended."

    days = diff // 86400
    hours = (diff % 86400) // 3600
    minutes = (diff % 3600) // 60

    if diff % 60 > 0:
        minutes += 1

    remaining_time_parts = []

    if days > 0:
        remaining_time_parts.append(f"🗓️ {days} day{'s' if days > 1 else ''}")
    if hours > 0:
        remaining_time_parts.append(f"⏰ {hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        remaining_time_parts.append(f"⌛ {minutes} minute{'s' if minutes > 1 else ''}")

    remaining_time = ', '.join(remaining_time_parts)

    return f"Subscription ends in {remaining_time}." if remaining_time else "⌛ Less than a minute left."
#--------------------------------------------------------------------------

async def format_subscription_status_ru(subscription_end: int, current_time: int) -> str:
    """
    Форматирует статус подписки с учетом оставшегося времени.
    """
    diff = subscription_end - current_time

    if diff <= 0:
        return "❌ Ваша подписка окончена."

    days = diff // 86400
    hours = (diff % 86400) // 3600
    minutes = (diff % 3600) // 60

    if diff % 60 > 0:
        minutes += 1

    remaining_time_parts = []
    if days == 1:
        remaining_time_parts.append(f"🗓️ {days} суток")
    elif days > 1:
        remaining_time_parts.append(f"🗓️ {days} суток")
    if hours > 0:
        remaining_time_parts.append(f"⏰ {hours} час{'a' if hours > 1 else ''}")
    if minutes > 0:
        remaining_time_parts.append(f"⌛ {minutes} минут{'ы' if minutes > 1 else ''}")

    remaining_time = ', '.join(remaining_time_parts)

    return f"Подписка истекает через {remaining_time}." if remaining_time else "⌛ Осталась менее минуты."

#--------------------------------------------------------------------------

async def set_language(message, lang):
    tgid = message.chat.id

    await api.set_language(tgid, lang)
    text, markup = await menu_cmd(message)
    return text, markup
#--------------------------------------------------------------------------