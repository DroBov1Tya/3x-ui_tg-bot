user_agreement = '''
<b>User Agreement</b>

<b>1. Responsibility</b>
By using this bot, you agree that the owner of the bot is not responsible for any actions taken by you while using the VPN, including illegal activities, violations of third-party rights, and other consequences. ⚠️

<b>2. Use of VPN</b>
You use the VPN at your own risk. The owner of the bot cannot guarantee the safety or privacy of your actions online. 🔒

<b>-----------------------------------------</b>

<b>Пользовательское соглашение</b>

<b>1. Ответственность</b>
Используя данный бот, вы соглашаетесь с тем, что владелец бота не несет ответственности за любые действия, совершенные вами с использованием VPN, включая незаконные действия, нарушения прав третьих лиц и другие последствия. ⚠️

<b>2. Использование VPN</b>
Вы используете VPN на свой страх и риск. Владелец бота не может гарантировать безопасность или конфиденциальность ваших действий в Интернете. 🔒
'''


decline = '''
<b>Important Notice</b>

By using this bot, you acknowledge that you must agree to the User Agreement. Without acceptance of the terms, you cannot use the bot. Please read the agreement carefully. 📜

<b>Важное уведомление</b>

Используя этот бот, вы подтверждаете, что должны согласиться с Пользовательским соглашением. Без принятия условий вы не можете использовать бот. Пожалуйста, внимательно прочитайте соглашение. 📜
'''


language = '''
For the best results, please select your preferred language for the bot. 🏆
'''

menu_en = '''
<b>Welcome to VeilVoyager VPN 🌌</b>
_______________________

<b>🚀 Streamline your VPN setup effortlessly!</b>
Experience seamless connectivity at your fingertips.

<b>Features:</b>
✨ <i>Create VPN configurations with a single click</i>
'''

menu_ru = '''
<b>Добро пожаловать в VeilVoyager VPN 🌌</b>
_______________________

<b>🚀 Настройте VPN легко и быстро!</b>
Испытайте беспроблемное подключение одним касанием.

<b>Возможности:</b>
✨ <i>Создавайте VPN-конфигурации в один клик</i>
'''

help_cmd_en = '''
<b>🛠 Configuration Guide</b>

We're here to help you set up the configs on any platform all by yourself! Whether you're using Android, iOS, or a PC, our guides are designed to make the process as simple and hassle-free as possible.

📖 <b>Step-by-step instructions</b> will walk you through the entire setup process. No technical headaches—just follow the steps, and everything will work perfectly.

💡 <b>No unnecessary steps</b>—we've streamlined the process so you can get everything set up quickly and easily, without needing expert help.

🔧 <b>Support is available</b> if you run into any questions, but we're confident you'll be able to handle it on your own!

Choose your platform below and follow the guide:
'''

help_cmd_ru = '''
<b>🛠 Руководство по настройке</b>

Мы готовы помочь вам самостоятельно настроить конфигурации на любой платформе! Независимо от того, используете ли вы Android, iOS или ПК, наши руководства созданы для того, чтобы сделать процесс максимально простым и удобным.

📖 <b>Пошаговые инструкции</b> проведут вас через весь процесс настройки. Никаких технических заморочек — просто следуйте шагам, и всё будет работать идеально.

💡 <b>Без лишних шагов</b> — мы оптимизировали процесс, чтобы вы могли всё настроить быстро и легко, без необходимости обращаться за помощью к экспертам.

🔧 <b>Поддержка доступна</b>, если у вас возникнут вопросы, но мы уверены, что вы справитесь самостоятельно!

Выберите свою платформу ниже и следуйте руководству:
'''

learn_more_en = '''
<b>Our VPN Features:</b>

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
    '''

learn_more_ru = '''
<b>Наши функции VPN:</b>

🌍 Безлимитный доступ:
Обходите ограничения и наслаждайтесь любимыми веб-сайтами и приложениями без перебоев.

⚡ Высокая скорость:
До 300 Мбит/с, обеспечивая плавный просмотр и стриминг.

🔒 Защита данных:
Обезопасьте ваше соединение с помощью шифрования, особенно в общественных Wi-Fi сетях.

📱 Поддержка нескольких устройств:
Используйте одну учетную запись на всех ваших устройствах – iOS, Android, Windows и macOS.

🛡️ Продвинутая безопасность:
Протокол VLESS сохраняет ваш трафик невидимым и защищённым.

💼 Глобальные серверы:
Получите доступ к серверам в США, Европе и Азии для стабильных и быстрых подключений.

🔐 Гарантия конфиденциальности:
Оставайтесь анонимными в Интернете с возможностью оплаты с помощью криптовалюты для дополнительной безопасности.

Просто, надежно и безопасно.
'''

async def config_menu_en(config_limit):
    if config_limit > 0:
        text = f'''
<b>🏴‍☠️ Choose Your VPN Country 🏴‍☠️</b>

🌍 <b>Select a Country:</b>  
Choose a server location to enhance your browsing experience. Pick from various countries to access geo-restricted content and enjoy seamless connectivity!

🔒 <b>Stay Secure:</b>  
Connect through your chosen country for privacy and security while surfing the internet. Make your selection below! ✨

💼 <b>Configuration Limit:</b>  
You can create <b>{config_limit}</b> more configurations.

⏳ <b>Configuration Lifetime:</b>  
Configurations are valid for the duration of your subscription. If you renew your subscription, you'll need to create a new configuration to continue using the service.

⚠️ <b>Server Updates:</b>  
If a server you previously used is no longer available, any configurations created on that server will be returned to your configuration limit, allowing you to create new configurations on available servers.
'''
        return text
    elif config_limit == 0:
        text = f'''
<b>🏴‍☠️ Choose Your VPN Country 🏴‍☠️</b>

🌍 <b>Select a Country:</b>  
Choose a server location to enhance your browsing experience. Pick from various countries to access geo-restricted content and enjoy seamless connectivity!

🔒 <b>Stay Secure:</b>  
Connect through your chosen country for privacy and security while surfing the internet. Make your selection below! ✨

💼 <b>Configuration Limit:</b>  
<i>You have reached the limit of configurations.</i>

⏳ <b>Configuration Lifetime:</b>  
Configurations are valid for the duration of your subscription. If you renew your subscription, you'll need to create a new configuration to continue using the service.


⚠️ <b>Server Updates:</b>  
If a server you previously used is no longer available, any configurations created on that server will be returned to your configuration limit, allowing you to create new configurations on available servers.
'''
        return text

async def config_menu_ru(config_limit):
    if config_limit > 0:
        text = f'''
<b>🏴‍☠️ Выберите страну для VPN 🏴‍☠️</b>

🌍 <b>Выбор страны:</b>  
Выберите местоположение сервера для улучшения вашего интернет-опыта. Выбирайте из различных стран для доступа к гео-ограниченному контенту и наслаждайтесь бесперебойным соединением!

🔒 <b>Оставайтесь в безопасности:</b>  
Подключайтесь через выбранную страну для обеспечения конфиденциальности и безопасности в сети. Сделайте свой выбор ниже! ✨

💼 <b>Лимит конфигураций:</b>  
Вы можете создать еще <b>{config_limit}</b> конфигураций.

⏳ <b>Время жизни конфигурации:</b>  
Конфигурации действуют на протяжении времени, равного сроку вашей подписки. Если вы продлите подписку, для продолжения работы потребуется создать новую конфигурацию.

⚠️ <b>Обновление серверов:</b>  
Если сервер, на котором были созданы конфигурации, перестает быть доступен, созданные на нем конфигурации возвращаются в ваш лимит, что позволит вам создать новые конфигурации на доступных серверах.
    '''
        return text
    elif config_limit == 0:
        text = f'''
<b>🏴‍☠️ Выберите страну для VPN 🏴‍☠️</b>

🌍 <b>Выбор страны:</b>  
Выберите местоположение сервера для улучшения вашего интернет-опыта. Выбирайте из различных стран для доступа к гео-ограниченному контенту и наслаждайтесь бесперебойным соединением!

🔒 <b>Оставайтесь в безопасности:</b>  
Подключайтесь через выбранную страну для обеспечения конфиденциальности и безопасности в сети. Сделайте свой выбор ниже! ✨

💼 <b>Лимит конфигураций:</b>  
<i>Вы исчерпали лимит конфигураций.</i>

⏳ <b>Время жизни конфигурации:</b>  
Конфигурации действуют на протяжении времени, равного сроку вашей подписки. Если вы продлите подписку, для продолжения работы потребуется создать новую конфигурацию.

⚠️ <b>Обновление серверов:</b>  
Если сервер, на котором были созданы конфигурации, перестает быть доступен, созданные на нем конфигурации возвращаются в ваш лимит, что позволит вам создать новые конфигурации на доступных серверах.
    '''
        return text

config_menu_without_en = '''
<b>🏴‍☠️ Choose a Country for VPN 🏴‍☠️</b>

⚠️ <b>Servers temporarily unavailable:</b>  
New servers are currently being purchased. We will update the server list shortly, and you will be able to select a new location for your VPN connection.

🔒 <b>Stay secure:</b>  
Your data remains protected. We recommend waiting a bit until the new servers are available. ✨
'''

config_menu_without_ru = '''
<b>🏴‍☠️ Выберите страну для VPN 🏴‍☠️</b>

⚠️ <b>Серверы временно недоступны:</b>  
В данный момент новые серверы находятся в процессе закупки. Мы скоро обновим список серверов, и вы сможете выбрать новое местоположение для VPN-подключения.

🔒 <b>Оставайтесь в безопасности:</b>  
Ваши данные по-прежнему под надежной защитой. Мы рекомендуем подождать немного до появления новых серверов. ✨
'''

async def account_menu_en(subscription_status): 
    text = f'''
<b>👤 Your Account</b>
Here you can manage your account settings and access all available features:

📅 <i>Renew subscription</i> to continue enjoying our premium features.

<b>📊 Subscription Status:</b> \n{subscription_status}
'''
    return text

async def account_menu_ru(subscription_status):
    text = f'''
<b>👤 Ваш аккаунт</b>
Здесь вы можете управлять настройками вашего аккаунта и получать доступ ко всем доступным функциям:

📅 <i>Продлите подписку</i>, чтобы продолжать пользоваться нашими премиум-функциями.

<b>📊 Статус подписки:</b> \n{subscription_status}

'''
    return text

top_up_balance_en = '''
<b>💸 Pay Methods</b>
We accept payments through the following methods:

- <i>Cryptocurrency</i> for instant and anonymous transactions.

'''

top_up_balance_ru = '''
<b>💸 Способы оплаты</b>
Мы принимаем платежи через следующие методы:

- <i>Криптовалюту</i> для мгновенных и анонимных транзакций.
'''

pay_subscription_en = '''
📅 <b>Subscription Options</b>
Choose the payment method that suits you best and enjoy uninterrupted access to our VPN services.

We use <b>CryptoBot Telegram</b> for fast and convenient cryptocurrency payments. Please select one of the available cryptocurrencies for payment:

- 💵 <b>USDT (TRC-20):</b> Ideal for stable and secure payments.

- ₿ <b>Bitcoin:</b> A reliable choice for those who prefer BTC.

- Ł <b>Litecoin:</b> A fast and lightweight alternative for payments.

- 💎 <b>TON:</b> The optimal choice for Telegram users.

Select your preferred cryptocurrency below:
'''

pay_subscription_ru = '''
📅 <b>Опции подписки</b>
Выберите удобный для вас способ оплаты и наслаждайтесь доступом к нашим VPN услугам.

Мы используем <b>CryptoBot Telegram</b> для быстрых и удобных платежей в криптовалюте. Выберите одну из доступных криптовалют для оплаты:

- <b>💰 USDT (TRC-20):</b> Подходит для стабильных и безопасных платежей.

- <b>₿ Bitcoin:</b> Надежный выбор для тех, кто предпочитает BTC.

- <b>Ł Litecoin:</b> Легкая и быстрая альтернатива для оплаты.

- <b>💎 TON:</b> Оптимальный выбор для пользователей Telegram.

Выберите криптовалюту для оплаты ниже:
'''

pay_with_crypto_en = '''
💼 <b>Select a payment method for your VPN subscription:</b>

You can pay for your subscription using the following cryptocurrencies:

1. 💰 USDT (TRC-20)
2. ₿ Bitcoin
3. Ł Litecoin
4. 💎 TON

<b>Choose your preferred payment method below:</b>
'''

pay_with_crypto_ru = '''
💼 <b>Выберите способ оплаты для подписки на VPN:</b>

Вы можете оплатить подписку с помощью следующих криптовалют:

1. 💰 USDT (TRC-20)
2. ₿ Bitcoin
3. Ł Litecoin
4. 💎 TON

<b>Выберите предпочтительный способ оплаты ниже:</b>
'''

async def usdt_sub_en(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Choose a payment method for your VPN subscription:</b>

🔹 <b>1 Month Subscription:</b> {one_month_crypto}$ 💰 USDT TRC-20
🔹 <b>6 Months Subscription:</b> {six_month_crypto}$ 💰 USDT TRC-20 (10% discount 🎫)  
🔹 <b>12 Months Subscription:</b> {twelve_month_crypto}$ 💰 USDT TRC-20 (18% discount 🎫)

💳 <b>Available payment methods:</b>

📊 <i>The price is fixed</i>
'''
    return text

async def usdt_sub_ru(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Выберите способ оплаты для вашей подписки на VPN:</b>

🔹 <b>1 месяц подписки:</b> {one_month_crypto}$ 💰 USDT TRC-20
🔹 <b>6 месяцев подписки:</b> {six_month_crypto}$ 💰 USDT TRC-20 (🎫 скидка 10%)  
🔹 <b>12 месяцев подписки:</b> {twelve_month_crypto}$ 💰 USDT TRC-20 (🎫 скидка 18%)

💳 <b>Доступные способы оплаты:</b>

📊 <i>Цена фиксированная</i>
'''
    return text

async def bct_sub_en(six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Select a payment method for your VPN subscription:</b>

🔹 <b>6 Months Subscription:</b> {six_month_crypto} ₿ BTC
🔹 <b>12 Months Subscription:</b> {twelve_month_crypto} ₿ BTC (10% discount 🎫)

💳 <b>Available payment method:</b>

🔹 ₿ <b>Bitcoin</b>

📊 <i>Prices are calculated based on the current cryptocurrency exchange rate</i>
'''
    return text

async def bct_sub_ru(six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Выберите способ оплаты для вашей подписки на VPN:</b>

🔹 <b>6 месяцев подписки:</b> {six_month_crypto} ₿ BTC
🔹 <b>12 месяцев подписки:</b> {twelve_month_crypto} ₿ BTC (🎫 скидка 10%)

💳 <b>Доступный способ оплаты:</b>

🔹 ₿ <b>Bitcoin</b>

📊 <i>Цена указана с учетом актуального курса криптовалюты</i>
'''
    return text

async def ltc_sub_en(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Select a payment method for your VPN subscription:</b>

🔹 <b>1 Month Subscription:</b> {one_month_crypto} Ł LTC
🔹 <b>6 Months Subscription:</b> {six_month_crypto} Ł LTC (10% discount 🎫)  
🔹 <b>12 Months Subscription:</b> {twelve_month_crypto} Ł LTC (18% discount 🎫)

💳 <b>Available payment method:</b>

🔹 Ł <b>Litecoin</b>

📊 <i>Prices are calculated based on the current cryptocurrency exchange rate</i>
'''
    return text

async def ltc_sub_ru(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Выберите способ оплаты для вашей подписки на VPN:</b>

🔹 <b>1 месяц подписки:</b> {one_month_crypto} Ł LTC
🔹 <b>6 месяцев подписки:</b> {six_month_crypto} Ł LTC (🎫 скидка 10%)  
🔹 <b>12 месяцев подписки:</b> {twelve_month_crypto} Ł LTC (🎫 скидка 18%)

💳 <b>Доступный способ оплаты:</b>

🔹 Ł <b>Litecoin</b>

📊 <i>Цена указана с учетом актуального курса криптовалюты</i>
'''
    return text

async def ton_sub_en(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Select a payment method for your VPN subscription:</b>

🔹 <b>1 Month Subscription:</b> {one_month_crypto} 💎 TON
🔹 <b>6 Months Subscription:</b> {six_month_crypto} 💎 TON (10% discount 🎫)  
🔹 <b>12 Months Subscription:</b> {twelve_month_crypto} 💎 TON (18% discount 🎫)

💳 <b>Available payment method:</b>

🔹 💎 <b>TON</b>

📊 <i>Prices are calculated based on the current cryptocurrency exchange rate</i>
'''
    return text

async def ton_sub_ru(one_month_crypto, six_month_crypto, twelve_month_crypto): 
    text = f'''
💼 <b>Выберите способ оплаты для вашей подписки на VPN:</b>

🔹 <b>1 месяц подписки:</b> {one_month_crypto} 💎 TON
🔹 <b>6 месяцев подписки:</b> {six_month_crypto} 💎 TON (🎫 скидка 10%)  
🔹 <b>12 месяцев подписки:</b> {twelve_month_crypto} 💎 TON (🎫 скидка 18%)

💳 <b>Доступный способ оплаты:</b>

🔹 💎 <b>TON</b>

📊 <i>Цена указана с учетом актуального курса криптовалюты</i>
'''
    return text

admin_createvoucher = '''
<b>Создание ваучеров</b>
<i>Здесь вы можете создать ваучер на подписку для пользователей на указанный срок. Выберите один из вариантов ниже, чтобы сгенерировать соответствующий ваучер:</i>

- <b>⏳ 1 Month</b>: Создаёт ваучер на 1 месяц подписки.

- <b>🕰️ 6 Months</b>: Создаёт ваучер на 6 месяцев подписки.

- <b>🌍 1 Year</b>: Создаёт ваучер на 1 год подписки.

Нажмите соответствующую кнопку для создания ваучера.
'''