import logging
from modules import bot_logic, api
from aiogram import Bot, types, F, Dispatcher, Router
from aiogram.filters.command import Command
from aiogram.types.input_file import InputFile
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from middlewares.message_middleware import message_middleware
from middlewares.callback_middleware import callback_middleware
from middlewares.inline_middleware import inline_middleware
from modules import lang_text

router = Router()

# Описание состояний для FSM
class VoucherStates(StatesGroup):
    waiting_for_voucher = State()

router.message.middleware(message_middleware())
router.callback_query.middleware(callback_middleware())
router.inline_query.middleware(inline_middleware())

#|=============================[Commands]=============================|
# Хэндлер на /start
@router.message(Command('start'))
async def start(message: types.Message):
    text, markup = await bot_logic.start_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на /menu
@router.message(Command('menu'))
async def menu(message: types.Message):
    text, markup = await bot_logic.menu_cmd(message)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на команду /voucher
@router.message(Command("voucher"))
async def start_voucher_process(message: Message, state: FSMContext):
    """
    Хэндлер для команды /voucher. Отправляет сообщение с просьбой ввести код ваучера
    и переводит пользователя в состояние ожидания кода ваучера.
    """
    language = await api.check_language(message.chat.id)
    if language.get("lang") == "en":
        await message.answer("🎫 Enter voucher code:")
        # Устанавливаем состояние ожидания ваучера
        await state.set_state(VoucherStates.waiting_for_voucher)
    elif language.get("lang") == "ru":
        await message.answer("🎫 Введите код ваучера:")
        # Устанавливаем состояние ожидания ваучера
        await state.set_state(VoucherStates.waiting_for_voucher)

@router.message(StateFilter(VoucherStates.waiting_for_voucher))
async def process_voucher_input(message: Message, state: FSMContext):
    """
    Хэндлер для обработки ввода ваучера. Проверяет код ваучера через API
    и активирует подписку, если ваучер валиден.
    """
    # Извлекаем введённый код ваучера
    voucher_code = message.text.strip()
    lang = (await api.check_language(message.chat.id)).get("lang")
    response = await api.check_voucher(message.chat.id, voucher_code)
    print(response)

    if lang == "en":
        # Проверяем ответ API
        if response["Success"]:
            r = await api.process_voucher(message.chat.id, voucher_code, lang)  # Активируем подписку через API
            print(r)
            if r["Success"]:
                await message.answer("The voucher has been activated! You have received a subscription.")
            else:
                await message.answer(r["Reason"])
        else:
            await message.answer(f"Error: {response['Reason']}")
    
    elif lang == "ru":
        # Проверяем ответ API
        if response["Success"]:
            await message.answer("Ваучер активирован! Вы получили подписку.")
            # Логика активации подписки в API
            await api.process_voucher(message.chat.id, voucher_code, lang)  # Активируем подписку через API
        else:
            await message.answer(f"Ошибка: {response['Reason']}")
    # После обработки очищаем состояние
    await state.clear()
#--------------------------------------------------------------------------

@router.message(Command('help'))
async def help(message: types.Message):
    text, markup = await bot_logic.help_cmd(message.chat.id)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.message(Command('language'))
async def help(message: types.Message):
    text, markup = await bot_logic.language_cmd(message.chat.id)
    await message.answer(text, reply_markup=markup)
#--------------------------------------------------------------------------

# Хэндлер на /admin
@router.message(Command('admin'))
async def admin(message: types.Message):
    r = await api.is_admin(message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admins_cmd(message)
        await message.answer(text, reply_markup=markup, )
#--------------------------------------------------------------------------
# #Хэндлер на любой текст 
@router.message(F.text)
async def anymsg(message: Message, bot: Bot, state: FSMContext):
    """
    Хэндлер для всех текстовых сообщений, который проверяет состояние пользователя.
    Если пользователь не вводит код ваучера, отображается стандартное меню.
    """
    # Проверяем текущее состояние пользователя
    current_state = await state.get_state()

    # Если пользователь не находится в состоянии ожидания ваучера
    if current_state != VoucherStates.waiting_for_voucher.state:
        text, markup = await bot_logic.menu_cmd(message)
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)

#|===========================[End Commands]===========================|




# CALLBACKS #
#|=============================[Utils]=============================|
# Обработчик для callback_data 'back'
@router.callback_query(F.data.startswith("menu "))
async def back(call: types.CallbackQuery):
    text, markup = await bot_logic.menu_cmd(call.message)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Коллбек на кнопку приятия соглашения 
@router.callback_query(F.data.startswith("agree "))
async def agree(call: types.CallbackQuery):
    text, markup = await bot_logic.agree(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("decline "))
async def decline(call: types.CallbackQuery):
    text, markup = await bot_logic.decline(call.message.chat.id)
    try:
        # Вместо редактирования сообщения, отправляем новое сообщение
        await call.bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
    except Exception as e:
        print(f"Error sending message: {e}")
#|===========================[End utils]===========================|

#|=============================[Admin panel buttons]=============================|
# Обработчик для callback_data 'admin_users'
@router.callback_query(F.data.startswith("admin_users "))
async def admin_users(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_users(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_ban'
@router.callback_query(F.data.startswith("admin_ban "))
async def admin_ban(call: types.CallbackQuery):
    var = call.data.split(" ")
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_ban(call.message, var[2])
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
# Обработчик для callback_data 'admin_unban'
@router.callback_query(F.data.startswith("admin_unban "))
async def admin_unban(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_unban(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher "))
async def admin_create_voucher(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_one "))
async def admin_create_voucher_one(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_one(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_six "))
async def admin_create_voucher_six(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_six(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("admin_create_voucher_year "))
async def admin_create_voucher_year(call: types.CallbackQuery):
    r = await api.is_admin(call.message.chat.id)
    if r['Success']:
        text, markup = await bot_logic.admin_create_voucher_year(call.message)
        await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------


#|=============================[Menu buttons]=============================|
# Обработчик для callback_data 'config_gen'
@router.callback_query(F.data.startswith("config_gen "))
async def config_gen(call: types.CallbackQuery):
    text, markup = await bot_logic.config_gen(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'countries'
@router.callback_query(F.data.startswith("config_menu "))
async def config_menu(call: types.CallbackQuery):
    text, markup = await bot_logic.config_menu(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'delete'
@router.callback_query(F.data.startswith("delete "))
async def delete(call: types.CallbackQuery):
    await call.message.delete()
#--------------------------------------------------------------------------

# Обработчик для callback_data 'create_config'
@router.callback_query(F.data.startswith("create_config "))
async def create_config(call: types.CallbackQuery):
    """
    Обработчик для callback-запросов, связанных с выбором страны.
    
    Args:
        call (types.CallbackQuery): Объект callback-запроса.
    """
    try:
        _, tgid, hostname = call.data.split(" ")
        # Получаем текст, разметку и файл QR-кода от логики бота
        text, markup, markup_delete, qr_file, lang = await bot_logic.create_config(call.message, hostname)
        print(lang)
        if lang == "en":
            if qr_file:
                # Попытка отправить файл как фото
                await call.message.answer_photo(
                    photo=types.FSInputFile(qr_file), 
                    caption=f"<code>{text}</code>", reply_markup=markup_delete
                )

                menu_text = lang_text.menu_en
            
                await call.message.answer(text = menu_text, reply_markup=markup)

            else:
                # If no QR file, send only the text
                await call.message.answer(
                    text=text,
                    reply_markup=markup
                )

        elif lang == "ru":
            if qr_file:
                # Попытка отправить файл как фото на русском
                await call.message.answer_photo(
                    photo=types.FSInputFile(qr_file), 
                    caption=f"<code>{text}</code>", reply_markup=markup_delete
                )

                menu_text = lang_text.menu_ru
            
                await call.message.answer(text=menu_text, reply_markup=markup)

            else:
                # Если файла QR нет, отправить только текст на русском
                await call.message.answer(
                    text=text,
                    reply_markup=markup
                )

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        if lang == "en":
            await call.message.answer(
                text=f"File not found. Please try again later.\n<code>{text}</code>", 
                reply_markup=markup
            )
        elif lang == "ru":
            await call.message.answer(
                text=f"Файл не найден. Пожалуйста, попробуйте позже.\n<code>{text}</code>", 
                reply_markup=markup
            )

    except ValueError as e:
        if lang == "en":
            # Обработка некорректных данных callback
            logging.error(f"Error in callback data: {e}")
            await call.message.answer(
                text="Invalid data. Please try again.",
                reply_markup=markup
            )
        elif lang == "ru":
            logging.error(f"Ошибка в данных callback: {e}")
            await call.message.answer(
                text="Некорректные данные. Пожалуйста, попробуйте снова.",
                reply_markup=markup
            )

    except Exception as e:
        if lang == "en":
            # Общая обработка ошибок на английском
            logging.error(f"Unknown error: {e}")
            await call.message.answer(
                text="An error occurred while processing your request.",
                reply_markup=markup
            )
        elif lang == "ru":
            # Общая обработка ошибок на русском
            logging.error(f"Неизвестная ошибка: {e}")
            await call.message.answer(
                text="Произошла ошибка при обработке вашего запроса.",
                reply_markup=markup
            )
#--------------------------------------------------------------------------

# Обработчик для callback_data 'learn more'
@router.callback_query(F.data.startswith("learn_more "))
async def learn_more(call: types.CallbackQuery):
    text, markup = await bot_logic.learn_more(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'en_language '
@router.callback_query(F.data.startswith("en_language "))
async def en_language(call: types.CallbackQuery):
    lang = "en"

    # Установка команд для конкретного пользователя
    commands = [
        types.BotCommand(command="/start", description="Start interacting with the bot"),
        types.BotCommand(command="/menu", description="Display the menu"),
        types.BotCommand(command="/voucher", description="Activate a voucher"),
        types.BotCommand(command="/language", description="Change bot language"),
        types.BotCommand(command="/help", description="Get help on using the bot")
    ]
    await call.message.bot.set_my_commands(commands)
    text, markup = await bot_logic.set_language(call.message, lang)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

# Обработчик для callback_data 'ru_language'
@router.callback_query(F.data.startswith("ru_language "))
async def ru_language(call: types.CallbackQuery):
    lang = "ru"
    commands = [
            types.BotCommand(command="/start", description="Начать взаимодействие с ботом"),
            types.BotCommand(command="/menu", description="Показать меню"),
            types.BotCommand(command="/voucher", description="Активировать ваучер"),
            types.BotCommand(command="/language", description="Изменить язык бота"),
            types.BotCommand(command="/help", description="Получить помощь по использованию бота")
        ]

    # Установка команд для пользователя
    await call.message.bot.set_my_commands(commands)
    # Логируем перед вызовом функции
    logging.info(f"User {call.from_user.id} selected language: {lang}")
    
    # Пробуем вызвать функцию и логируем результат
    try:
        text, markup = await bot_logic.set_language(call.message, lang)
        logging.info("Language set successfully, preparing to edit message.")
    except Exception as e:
        logging.error(f"Error while setting language: {e}")
        await call.message.answer("Произошла ошибка при смене языка.")
        return
    
    # Редактируем текст сообщения после успешного изменения
    await call.message.edit_text(text=text, reply_markup=markup)

#--------------------------------------------------------------------------
# Обработчик для callback_data 'account_menu'
@router.callback_query(F.data.startswith("account_menu "))
async def account_menu(call: types.CallbackQuery):
    text, markup = await bot_logic.account_menu(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
@router.callback_query(F.data.startswith("top_up_balance "))
async def top_up_balance(call: types.CallbackQuery):
    text, markup = await bot_logic.top_up_balance(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("pay_with_crypto "))
async def pay_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_crypto(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("pay_with_usdt "))
async def pay_with_usdt(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_usdt(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("pay_with_btc "))
async def pay_with_btc(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_btc(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("pay_with_ltc "))
async def pay_with_ltc(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_ltc(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

@router.callback_query(F.data.startswith("pay_with_ton "))
async def pay_with_ton(call: types.CallbackQuery):
    text, markup = await bot_logic.pay_with_ton(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------



#USDT TRC-20 оплата на месяц
@router.callback_query(F.data.startswith("usdt_one_month_subscription "))
async def one_month_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.one_month_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#USDT TRC-20 оплата на 6 месяцев
@router.callback_query(F.data.startswith("usdt_six_months_subscription "))
async def six_months_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.six_months_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#USDT TRC-20 оплата на год
@router.callback_query(F.data.startswith("usdt_year_subscription "))
async def year_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.year_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#BTC оплата на 6 месяцев
@router.callback_query(F.data.startswith("btc_six_months_subscription "))
async def six_months_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.six_months_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#BTC оплата на год
@router.callback_query(F.data.startswith("btc_year_subscription "))
async def year_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.year_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#LTC оплата на месяц
@router.callback_query(F.data.startswith("ltc_one_month_subscription "))
async def one_month_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.one_month_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#LTC оплата на 6 месяцев
@router.callback_query(F.data.startswith("ltc_six_months_subscription "))
async def six_months_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.six_months_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#LTC оплата на год
@router.callback_query(F.data.startswith("ltc_year_subscription "))
async def year_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.year_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#TON оплата на месяц
@router.callback_query(F.data.startswith("ton_one_month_subscription "))
async def one_month_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.one_month_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#TON оплата на 6 месяцев
@router.callback_query(F.data.startswith("ton_six_months_subscription "))
async def six_months_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.six_months_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------

#TON оплата на год
@router.callback_query(F.data.startswith("ton_year_subscription "))
async def year_subscription(call: types.CallbackQuery):
    text, markup = await bot_logic.year_subscription(call.message.chat.id)
    await call.message.edit_text(text=text, reply_markup=markup)
#--------------------------------------------------------------------------
