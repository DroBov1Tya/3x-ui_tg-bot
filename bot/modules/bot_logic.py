import base64
import logging
import time
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

<b>Beta 0.6</b>
''', BTN.menu(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def help_cmd(tgid):
    text, markup = '''
<b>🛠 Configuration Guide</b>

We're here to help you set up the configs on any platform all by yourself! Whether you're using Android, iOS, or a PC, our guides are designed to make the process as simple and hassle-free as possible.

📖 <b>Step-by-step instructions</b> will walk you through the entire setup process. No technical headaches—just follow the steps, and everything will work perfectly.

💡 <b>No unnecessary steps</b>—we've streamlined the process so you can get everything set up quickly and easily, without needing expert help.

🔧 <b>Support is available</b> if you run into any questions, but we're confident you'll be able to handle it on your own!

Choose your platform below and follow the guide:
''', BTN.help(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def learn_more(tgid: int):
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

async def config_menu(tgid: int):
    servers = await api.servers_count()
    text, markup = '''
<b>🏴 Choose VPN country 🏴</b>
''', BTN.config_menu(tgid, servers)
    return text, markup
#--------------------------------------------------------------------------

async def account_menu(tgid: int):
    balance = await api.getbalance(tgid)
    subsctiption = await api.getsubsctiption(tgid)
    current_time = int(time.time())

    # Формируем статус подписки с помощью отдельной функции
    subscription_status = await format_subscription_status(subsctiption.get("subscription"), current_time)

    # Формируем вывод текста с учетом баланса
    text = f'''
<b>👤 Your Account</b>
Here you can manage your account settings and access all available features:

💰 <i>Your current balance:</i> <b>{balance.get("balance", 0)} units 💵</b>

📅 <i>Renew subscription</i> to continue enjoying our premium features.

⚙️ <i>Settings</i> to customize your experience to your preferences.

<b>📊 Subscription Status:</b> \n{subscription_status}
'''

    # Возвращаем текст и разметку
    markup = BTN.account_menu(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def top_up_ballance(tgid: int):
    text, markup = '''
<b>💸 Pay Methods</b>
We accept payments through the following methods:

- <i>Cryptocurrency</i> for instant and anonymous transactions.

''', BTN.top_up_ballance(tgid)
    return text, markup
#--------------------------------------------------------------------------

async def pay_subscription(tgid: int):
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
#--------------------------------------------------------------------------

#|=============================[SRC]=============================|
async def format_subscription_status(subscription_end: int, current_time: int) -> str:
    """
    Форматирует статус подписки с учетом оставшегося времени.
    """
    diff = subscription_end - current_time

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