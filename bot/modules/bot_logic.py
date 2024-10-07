import base64
import logging
from modules import BTN, api
from config import logger
#|=============================[Menu]=============================|
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
<b>Welcome to Spoof VeilVoyager 🌌</b>
_______________________

🚀 **Streamline your VPN setup effortlessly!**  
Experience seamless connectivity at your fingertips.

<b>Features:</b>
✨ <i>Create VPN configurations with a single click</i>

<b>Beta 0.5</b>
''', BTN.menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def learn_more(tgid):
    text, markup = f'''
Our VPN Features:

🌍 Unlimited access:
Bypass restrictions and enjoy your favorite websites and apps without interruptions.

⚡ Fast speed:
Up to 300 Mbps, ensuring smooth browsing and streaming.

🔒 Data protection:
Secure your connection with encryption, especially on public Wi-Fi.

📱 Multi-device support:
Use one account across all your devices – iOS, Android, Windows, and macOS.

🛡️ Advanced security:
VLESS protocol keeps your traffic invisible and secure.

💼 Global servers:
Access servers in the US, Europe, and Asia for stable and fast connections.

🔐 Privacy assured:
Stay anonymous online, with the option to pay via cryptocurrency for extra security.

Simple, reliable, and secure.
    ''', BTN.back(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def create_config(message, hostname):
    try:
        tgid = message.chat.id
        data, qr_file = await api.create_config(message, hostname)
        if not data:
            text = "Your subscription has expired, would you like to renew it?"
            markup = BTN.pay_subscription(tgid)
            markup_delete = BTN.delete_message(tgid)
            return text, markup, markup_delete, None
        else:
            print("111")
            config = data["config"]

            text, markup, markup_delete = f"{config}", BTN.menu(tgid), BTN.delete_message(tgid)
            return text, markup, markup_delete, qr_file
    
    except Exception as e:
        # Обрабатываем любые исключения, которые могут возникнуть
        logger.error(f"Error in create_config: {str(e)}")
        text = "An error occurred while generating the configuration. Please try again later."
        markup = BTN.menu(tgid)
        markup_delete = BTN.delete_message(tgid)
        return text, markup, markup_delete, None
#--------------------------------------------------------------------------
async def config_menu(tgid):
    servers = await api.servers_count()
    text, markup = '''
<b>🏴 Choose VPN country 🏴</b>
''', BTN.config_menu(tgid, servers)
    return text, markup
#--------------------------------------------------------------------------
async def account_menu(tgid):
    text, markup = '''
<b>👤 Account</b>
Manage your account settings and access various features:

- <i>Top up balance</i> to ensure uninterrupted service.

- <i>Pay subscription</i> to continue enjoying our premium features.

- <i>Settings</i> to customize your experience.

''', BTN.account_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def top_up_ballance(tgid):
    text, markup = '''
<b>💸 Pay Methods</b>
We accept payments through the following methods:

- <i>Cryptocurrency</i> for instant and anonymous transactions.

''', BTN.top_up_ballance(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def pay_subscription(tgid):
    text, markup = '''
<b>📅 Subscription Options</b>
Choose the subscription plan that best suits your needs and enjoy uninterrupted access to our services:

- <i>1 Month Subscription</i>: Perfect for those who want to try out our features.

- <i>6 Months Subscription</i>: A great choice for long-term users looking for value.

- <i>1 Year Subscription</i>: Best for frequent users who want to maximize savings.

''', BTN.pay_subscription(tgid)
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
    text, markup = '''
<b>Создание ваучеров</b>
<i>Здесь вы можете создать ваучер на подписку для пользователей на указанный срок. Выберите один из вариантов ниже, чтобы сгенерировать соответствующий ваучер:</i>

- <b>⏳ 1 Month</b>: Создаёт ваучер на 1 месяц подписки.

- <b>🕰️ 6 Months</b>: Создаёт ваучер на 6 месяцев подписки.

- <b>🌍 1 Year</b>: Создаёт ваучер на 1 год подписки.

Нажмите соответствующую кнопку для создания ваучера.
''', BTN.admin_create_voucher(tgid)
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
    text, markup = vaucher_code, BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_create_voucher_six(message):
    tgid = message.chat.id
    r = await api.admin_create_voucher_six()
    vaucher_code = r.get("voucher")
    text, markup = vaucher_code, BTN.admin_create_voucher(tgid)
    return text, markup
#--------------------------------------------------------------------------
async def admin_create_voucher_year(message):
    tgid = message.chat.id
    r = await api.admin_create_voucher_year()
    vaucher_code = r.get("voucher")
    text, markup = vaucher_code, BTN.admin_create_voucher(tgid)
    return text, markup
